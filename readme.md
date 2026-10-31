# OrdinarySMP Resource Pack

Custom hats, tools, food, totems, decorations, and other models for OrdinarySMP.
Enable this folder as a Minecraft Java resource pack.

## Files

- `assets/custom/models/` — models grouped by purpose.
- `assets/custom/textures/` — matching textures and animation sidecars.
- `assets/minecraft/items/` — base-item definitions, CMD mappings, and metadata.
- `descriptions.json` — category descriptions included in the generated registry.

Every registered category requires a non-empty description in `descriptions.json`.
Run `python .github/scripts/generate_models.py` to generate the release pack and
`build/release-pack/models.json`. CI runs the same validation on pushes and pull
requests and fails if a category description is missing or blank.

Asset filenames use `snake_case`; registry names use PascalCase. Carved-pumpkin
models and textures belong under `block/` to keep their atlas consistent.

See [AGENTS.md](AGENTS.md) for maintenance rules and metadata details.

## Credits

Thank you to the artists and creators whose textures and models appear in this pack.
See [Texture credits](credits/CREDITS.md) for individual credits and original sources,
and [Missing texture credits](credits/MISSING_SOURCES.md) for credits we are still recovering.

If your textures are included in this pack and your credit is missing or incorrect,
please let us know so we can give you proper credit.
