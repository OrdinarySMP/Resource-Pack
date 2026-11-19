# Resource pack maintenance

## Source layout

- Edit source assets, not the ignored `build/` output.
- Base-item definitions belong in `assets/<namespace>/items/`.
- Custom model JSON files belong in `assets/custom/models/`; textures belong in
  `assets/custom/textures/`. Mirror category paths where possible.
- Organize by purpose, then collection. Do not introduce creator or season folders.
- Use these existing categories:
  - `block/`: `filters`, `hats`, `accessories`, `bouncepads`.
  - `item/cosmetics/`: `wings`.
  - `item/equipment/`: `sets`, `weapons/lightsabers`, `fishing_rods`, `pickaxes`.
  - `item/food/`: `bakery`, `desserts`, `drinks`, `ice_cream`, `ingredients`, `meals`.
  - `item/totems/`: `players`, `animals`, `collections`.
  - `item/decorations/`: `paintings`, `signs/billboards`, `flowers`, `plushies`,
    `trophies`, `effects/blood`, `effects/runes`.
  - Other item categories: `games/cards`, `games/chips`, `stationery/letters`,
    `flags`, `collectibles/easter_eggs`, `materials`, `enchanted_books`.
- Keep equipment sets and their animation states together.

## Naming and references

- Asset paths use lowercase `snake_case` and full words: `boba_fett_helmet`,
  `ace_of_spades`, `yellow_butterfly_wings`, `progress_pride_flag`.
- Put colors before the object: `black_wizard_hat`, `purple_fairy_wings`.
- Within plushie and totem folders, use short subject names such as `bee`,
  `alien`, and `padbro_astronaut`.
- Separate texture layer numbers with underscores, such as `christmas_lights_1`.
  Preserve animation suffixes such as `_pulling_0` and `_cast`.
- Move `.png.mcmeta` sidecars with their PNG. Preserve shared textures and layers;
  model and texture filenames need not always match.
- When moving assets, update model, parent, and texture references across the
  pack. Preserve geometry, UVs, animation data, and existing credits.
- Asset moves must not change CMDs or owners. Registry renames change lookup names.

## Credits

- Always ask for creator credits and original source links when adding or
  importing models or textures, unless the user has already supplied them.
  For adapted assets, ask for both the original creator and the adapter.
- Record each texture and its credit in `credits/CREDITS.md`. If the user does
  not know the source, list it in `credits/MISSING_SOURCES.md`; do not guess or
  assume that an asset's owner is its creator.
- Keep both credit lists and their texture paths current when assets are moved,
  removed, or attributed. Shared textures need only one entry per list.

## Rendering constraints

- Carved-pumpkin models **and textures** use matching `block/hats/`,
  `block/accessories/`, or `block/bouncepads/` paths. Their vanilla fallback uses
  the block atlas; moving model JSON alone does not move textures between atlases.
- Do not mix item-atlas and block-atlas textures in a rendered model.
- Models with explicit elements should have a resolvable `particle` texture,
  for example `"particle": "#0"`. Check inherited texture variables too.
- Do not leave face textures pointing to undefined variables such as `#missing`.
- Use valid model parent identifiers, such as `minecraft:block/carved_pumpkin`.
- Prefer the CMD dispatch outside state conditions to avoid duplicate metadata;
  `spyglass.json` is an example. Preserve the selected model in every state.

## CMD metadata

### CustomModelData numbering

- New models must use sequential CustomModelData values, starting at `1001`.
- Each new model gets the next available value. Values are assigned per model,
  not per item.
- Never reuse an existing value for another model on the same base item.
- Do not renumber existing models, even if values are removed or gaps appear.
- Older models may still use randomly assigned CustomModelData values from the
  previous system. Keep these values unchanged for compatibility.
- The sequential numbering convention applies to all newly added models.

CMD values may repeat across different base items, but distinct registry models
must not claim the same base-item/CMD pair.

Each registered custom-model-data dispatch entry carries:

```json
{
  "threshold": 1001,
  "model": {"type": "model", "model": "custom:item/totems/animals/bee"},
  "owners": ["xKellfeine"],
  "name": "BeeTotem",
  "category": "totem"
}
```

- `owners` is a non-empty array of player usernames or `@group` identifiers.
  Use `@public` for public access and `@staff` for staff access. The intentional
  placeholder for undocumented ownership is **`@unknown`**.
- `category` uses singular `snake_case`, based on purpose rather than base item:
  `plushie`, `card`, `letter`, `material`, `blood_effect`, `easter_egg`, etc.
- `name` uses PascalCase: `BeePlushie`, `AlarmLetter`, `FishTrophy`,
  `PrincessBillboard`, `HoneyPickaxe`, `AceOfSpades`, `MonaLisa1x2Painting`.
  Preserve proper-name capitalization.
- Optional `display_name` is a non-empty string applied as the item's custom name
  after the texture is applied. It is emitted as `"name"` in `models.json` and
  omitted when unset. Grouped entries must share the same `display_name`.
- Totem names use `<Subject>Totem`, with `Christmas`, `Halloween`, `DemonHunter`,
  or `Toy` prefixes where needed. Keep `SoulTotem` and `HalloweenSoulTotem`
  distinct; the second Lilvyse variant is `LilvyseVariantTotem`.
- The generator groups entries by `(category, name)`. Grouped entries must have
  identical owners and CMDs; their base items are combined in the registry.
- Untagged custom entries are audited but omitted from the registry. Partially
  tagged entries fail validation. Check the audit even when the build exits zero.

## Validation and release

- Run `python .github/scripts/generate_models.py` from the repository root after
  asset or metadata changes, unless the user requests inspection only.
- Review errors and missing-metadata counts. Verify affected model/parent/texture
  paths, inherited variables, atlas consistency, and state-dependent rendering.
  The generator validates metadata and JSON, not all rendering constraints.
- Source metadata is stripped only in `build/release-pack/`. The registry is
  `build/release-pack/models.json`; do not remove metadata from source entries.
- Keep the ZIP root as `assets/`, `pack.mcmeta`, and `pack.png`; the registry is
  currently a separate release asset.
- `.github/workflows/release.yml` and `.releaserc.json` release from `main`.
  Manual dispatch on another branch does not make it a release branch.
- Current workflow limitations: duplicate ZIP upload, uploads gated on a newly
  published release (retry risk).
- The registry is uploaded to every server in the `MODELS_JSON_SERVERS` secret
  (JSON array with per-server host, ID, token, upload dir and optional console
  command), separately from the ZIP's Pterodactyl upload.
- Commit messages follow `@commitlint/config-conventional`, e.g.
  `feat: add a model`, `fix: correct texture references`, `refactor: organize assets`.
