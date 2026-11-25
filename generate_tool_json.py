
import json
from pathlib import Path

# Folder containing the item model JSON files
ITEMS_DIR = Path("assets/minecraft/items")

MATERIALS = [
    "wooden",
    "stone",
    "iron",
    "golden",
    "diamond",
    "copper"
]

TOOLS = [
    "axe",
    "hoe",
    "pickaxe",
    "shovel",
    "sword"
]


def generate_models():
    for tool in TOOLS:
        source_file = ITEMS_DIR / f"netherite_{tool}.json"

        if not source_file.exists():
            print(f"[SKIP] Missing source: {source_file.name}")
            continue

        # Read the Netherite model
        with source_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        for material in MATERIALS:
            target_name = f"{material}_{tool}.json"
            target_file = ITEMS_DIR / target_name

            # Change only the fallback model
            data_copy = json.loads(json.dumps(data))
            data_copy["model"]["fallback"]["model"] = (
                f"minecraft:item/{material}_{tool}"
            )

            # Write the generated model
            with target_file.open("w", encoding="utf-8") as file:
                json.dump(data_copy, file, indent=4)
                file.write("\n")

            print(f"[OK] Generated {target_name}")


if __name__ == "__main__":
    generate_models()
