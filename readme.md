# OrdinarySMP Resource Pack

Custom hats, tools, food, totems, decorations, and other models for OrdinarySMP.
Enable this folder as a Minecraft Java resource pack.

## Files

- `assets/custom/models/` — models grouped by purpose.
- `assets/custom/textures/` — matching textures and animation sidecars.
- `assets/minecraft/items/` — base-item definitions, CMD mappings, and metadata.

Asset filenames use `snake_case`; registry names use PascalCase. Carved-pumpkin
models and textures belong under `block/` to keep their atlas consistent.

## Build

From the repository root:

```sh
python .github/scripts/generate_models.py
```

The output is `build/release-pack/`: a pack with source metadata removed and a
separate `models.json` registry. Releases from `main` publish the ZIP and registry
to GitHub; the workflow uploads the ZIP to Pterodactyl.

See [AGENTS.md](AGENTS.md) for maintenance rules and metadata details.
