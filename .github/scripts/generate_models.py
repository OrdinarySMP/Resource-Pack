#!/usr/bin/env python3

import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path.cwd()
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "build" / "release-pack"
OUTPUT_ASSETS = OUTPUT_DIR / "assets"
REGISTRY_PATH = OUTPUT_DIR / "models.json"

METADATA_FIELDS = {"owners", "owner", "name", "category"}
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
GROUP_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{1,16}$")

models = {}
errors = []
audit = defaultdict(list)
scanned_entries = 0


def load_json(path):
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def find_dispatches(value):
    """Find CustomModelData range_dispatch entries recursively."""
    if isinstance(value, dict):
        dispatch_type = str(value.get("type", "")).removeprefix("minecraft:")
        prop = str(value.get("property", "")).removeprefix("minecraft:")

        if (
            dispatch_type == "range_dispatch"
            and prop == "custom_model_data"
            and isinstance(value.get("entries"), list)
        ):
            for entry in value["entries"]:
                if isinstance(entry, dict):
                    yield entry

        for child in value.values():
            yield from find_dispatches(child)

    elif isinstance(value, list):
        for child in value:
            yield from find_dispatches(child)


def item_id_from_path(path):
    """
    assets/<namespace>/items/<path>.json
    becomes <namespace>:<path>
    """
    relative = path.relative_to(ASSETS_DIR)
    parts = relative.parts

    if len(parts) < 3 or parts[1] != "items":
        return None

    namespace = parts[0]
    item_path = Path(*parts[2:]).with_suffix("").as_posix()

    return f"{namespace}:{item_path}"


def validate_owner(owner, location):
    if not isinstance(owner, str) or not owner:
        errors.append(f"{location}: owner entries must be non-empty strings")
        return False

    if owner.startswith("@"):
        group = owner[1:]
        if not GROUP_PATTERN.fullmatch(group):
            errors.append(f"{location}: invalid group owner {owner!r}")
            return False
        return True

    if not USERNAME_PATTERN.fullmatch(owner):
        errors.append(f"{location}: invalid player owner {owner!r}")
        return False

    return True


def process_entry(entry, item_id, path):
    global scanned_entries
    scanned_entries += 1

    threshold = entry.get("threshold")
    model_data = entry.get("model")
    location = f"{path} (item {item_id}, threshold {threshold!r})"

    # Completely untagged entries are legacy models.
    # Report them, but never add them to the registry automatically.
    has_metadata = bool(METADATA_FIELDS.intersection(entry.keys()))

    if not has_metadata:
        for field in ("owners", "name", "category"):
            audit[field].append(location)
        return

    # Once any metadata is present, require all required fields.
    required = ("owners", "name", "category")
    missing = [field for field in required if field not in entry]

    if missing:
        errors.append(
            f"{location}: partially tagged entry is missing "
            + ", ".join(missing)
        )
        for field in missing:
            audit[field].append(location)
        return

    if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 0:
        errors.append(f"{location}: threshold must be a non-negative integer")
        return

    if not isinstance(model_data, dict):
        errors.append(f"{location}: model must be an object")
        return

    category = entry["category"]
    name = entry["name"]
    owners = entry["owners"]

    if not isinstance(category, str) or not NAME_PATTERN.fullmatch(category):
        errors.append(f"{location}: invalid category {category!r}")
        return

    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append(f"{location}: invalid model name {name!r}")
        return

    if not isinstance(owners, list) or not owners:
        errors.append(f"{location}: owners must be a non-empty array")
        return

    valid_owners = True
    for owner in owners:
        if not validate_owner(owner, location):
            valid_owners = False

    if not valid_owners:
        return

    if len(set(owners)) != len(owners):
        errors.append(f"{location}: duplicate owners in owners array")
        return

    key = (category, name)
    model = {
        "owners": owners,
        "custom_model_data": threshold,
        "items": {item_id},
    }

    if key in models:
        existing = models[key]

        if (
            existing["owners"] != owners
            or existing["custom_model_data"] != threshold
        ):
            errors.append(
                f"{location}: conflicting definitions for "
                f"{category}/{name}"
            )
            return

        existing["items"].add(item_id)
    else:
        models[key] = model


def strip_metadata(value):
    """
    Remove source-only metadata from range_dispatch entries.
    This runs on the staged release copy, never the source files.
    """
    changed = False

    if isinstance(value, dict):
        dispatch_type = str(value.get("type", "")).removeprefix("minecraft:")
        prop = str(value.get("property", "")).removeprefix("minecraft:")

        if (
            dispatch_type == "range_dispatch"
            and prop == "custom_model_data"
            and isinstance(value.get("entries"), list)
        ):
            for entry in value["entries"]:
                if isinstance(entry, dict) and "threshold" in entry and "model" in entry:
                    for field in METADATA_FIELDS:
                        if field in entry:
                            del entry[field]
                            changed = True

        for child in value.values():
            if strip_metadata(child):
                changed = True

    elif isinstance(value, list):
        for child in value:
            if strip_metadata(child):
                changed = True

    return changed


def main():
    if not ASSETS_DIR.is_dir():
        print("ERROR: assets/ directory not found.", file=sys.stderr)
        return 1

    for required_file in ("pack.mcmeta", "pack.png"):
        if not (ROOT / required_file).is_file():
            print(f"ERROR: {required_file} not found.", file=sys.stderr)
            return 1

    # Start with a clean staging directory.
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True)
    shutil.copytree(ASSETS_DIR, OUTPUT_ASSETS)

    for filename in ("pack.mcmeta", "pack.png"):
        shutil.copy2(ROOT / filename, OUTPUT_DIR / filename)

    # Scan item model JSON files for tagged CustomModelData entries.
    for path in sorted(ASSETS_DIR.glob("*/items/**/*.json")):
        item_id = item_id_from_path(path)
        if not item_id:
            continue

        data = load_json(path)
        if data is None:
            continue

        for entry in find_dispatches(data):
            process_entry(entry, item_id, path.relative_to(ROOT))

    # Detect CustomModelData collisions between distinct registry models.
    threshold_owners = {}
    for (category, name), model in models.items():
        threshold = model["custom_model_data"]
        previous = threshold_owners.get(threshold)

        if previous is not None and previous != (category, name):
            errors.append(
                f"Duplicate CustomModelData {threshold}: "
                f"{previous[0]}/{previous[1]} and {category}/{name}"
            )
        else:
            threshold_owners[threshold] = (category, name)

    # Strip custom metadata from JSON files in the staged pack.
    # The original source assets remain untouched.
    for path in sorted(OUTPUT_ASSETS.rglob("*.json")):
        data = load_json(path)
        if data is None:
            continue

        if strip_metadata(data):
            with path.open("w", encoding="utf-8", newline="\n") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                file.write("\n")

    # Create the registry in the format expected by CmXBro.
    registry = {
        "version": 1,
        "categories": {},
    }

    for (category, name), model in sorted(models.items()):
        registry["categories"].setdefault(category, {})[name] = {
            "owners": model["owners"],
            "custom_model_data": model["custom_model_data"],
            "items": sorted(model["items"]),
        }

    with REGISTRY_PATH.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(registry, file, indent=2, ensure_ascii=False)
        file.write("\n")

    # Print the audit report for existing entries without metadata.
    print("\nResource pack model audit")
    print("=========================")
    print(f"Total entries scanned: {scanned_entries}")
    print(f"Models ready for registry: {len(models)}")

    missing_count = len(set(
        location
        for locations in audit.values()
        for location in locations
    ))
    print(f"Entries requiring metadata: {missing_count}")

    for field in ("owners", "name", "category"):
        locations = audit[field]
        print(f"\nMissing {field}: {len(locations)}")
        for location in locations:
            print(f"  - {location}")

    if errors:
        print("\nERRORS")
        print("======")
        for error in errors:
            print(f"  - {error}")

        print(
            "\nRegistry generation failed. "
            "Fix the errors before publishing this release.",
            file=sys.stderr,
        )
        return 1

    print(f"\nGenerated registry: {REGISTRY_PATH}")
    print(f"Staged resource pack: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
