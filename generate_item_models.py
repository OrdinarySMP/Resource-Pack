
import json
import sys
from pathlib import Path

NAMESPACE = "custom"


def generate_models():
    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "python generate_item_models.py "
            "assets/custom/textures/item/food/bakery"
        )
        input("\nPress Enter to exit...")
        return

    texture_folder = Path(sys.argv[1])

    if not texture_folder.is_dir():
        print(f"ERROR: Folder not found: {texture_folder.resolve()}")
        input("\nPress Enter to exit...")
        return

    # Convert the textures directory to its matching models directory.
    parts = texture_folder.parts

    try:
        textures_index = parts.index("textures")
    except ValueError:
        print("ERROR: The folder path must contain a 'textures' directory.")
        input("\nPress Enter to exit...")
        return

    model_folder = Path(
        *parts[:textures_index],
        "models",
        *parts[textures_index + 1:]
    )

    # Choose the model parent based on the folder path.
    parent = (
        "minecraft:item/handheld"
        if "equipment" in parts
        else "minecraft:item/generated"
    )

    created = 0
    skipped = 0

    # Get the namespace and textures root.
    assets_index = parts.index("assets")
    namespace = parts[assets_index + 1]
    textures_root = Path(*parts[:textures_index + 1])

    for png in texture_folder.glob("*.png"):
        if not png.is_file() or png.suffix.lower() != ".png":
            continue

        relative_path = png.relative_to(texture_folder)

        # Preserve the subfolder structure in the models directory.
        json_path = model_folder / relative_path.with_suffix(".json")
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # Build the texture identifier.
        texture_path = (
            f"{namespace}:"
            f"{png.relative_to(textures_root).with_suffix('').as_posix()}"
        )

        if json_path.exists():
            skipped += 1
            continue

        model = {
            "parent": parent,
            "textures": {
                "layer0": texture_path
            }
        }

        json_path.write_text(
            json.dumps(model, indent=4) + "\n",
            encoding="utf-8"
        )

        print(f"Created: {json_path}")
        created += 1

    print(f"\nDone! Created {created} models, skipped {skipped} existing files.")
    print(f"Parent used: {parent}")
    print(f"Output folder: {model_folder.resolve()}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    generate_models()