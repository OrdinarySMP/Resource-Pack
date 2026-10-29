# Asset structure

Custom models live in `assets/custom/models/`. Textures use the corresponding
category under `assets/custom/textures/`, including animation `.png.mcmeta`
sidecars. Minecraft item definitions stay in `assets/minecraft/items/`.

```text
block/
  filters/
item/
  cosmetics/
    hats/                 # astronaut, cat_ears, christmas, mushroom,
                          # pirate, star_wars, wizard, laurels, bottlers
    accessories/
    wings/
  equipment/
    sets/                 # blossom, cookie, crystal, ender, honey, honor,
                          # huntrix, salat
    weapons/
      lightsabers/
    fishing_rods/
    pickaxes/
  food/
    bakery/
    desserts/
    drinks/
    ice_cream/
    ingredients/
    meals/
  totems/
    players/
    animals/
    collections/          # christmas, halloween, demon_hunter, devils_toys
  decorations/
    paintings/
    signs/
      billboards/
    flowers/
    plushies/
    trophies/
    bouncepads/
    effects/
      blood/
      runes/
  games/
    cards/
    chips/
  stationery/
    letters/
  flags/
  collectibles/
    easter_eggs/
  materials/
  enchanted_books/
```

Choose the category by what an asset represents, independently of its Minecraft
base item, creator, owner, or season of introduction. Put a collection beneath
its category when useful; otherwise put the asset directly in the category.
Keep equipment sets and all their animation states together. New names should
use lowercase `snake_case`.

Use full words in asset identifiers: `boba_fett_helmet`, `ace_of_spades`,
`yellow_butterfly_wings`, and `progress_pride_flag`. Within the plushie and
totem folders, use the subject alone (`bee`, `alien`, `padbro_astronaut`).
For colored variants, put the color before the object (`black_wizard_hat`,
`purple_fairy_wings`). Use underscore-separated layer numbers such as
`christmas_lights_1`; keep animation state suffixes such as `_pulling_0` and
`_cast`. Animation sidecars retain the complete texture filename plus `.mcmeta`.

Model and texture filenames can differ when a model uses multiple layers or
shares a texture. Their references remain explicit in each JSON file. Move
animation sidecars with their texture and update model, parent, and texture
identifiers whenever an asset moves.

Ownership, registry names, categories, and CMD numbers belong to the item-entry
metadata; moving an asset does not change them. See
[the metadata conventions](.github/scripts/METADATA.md).

Run `python .github/scripts/generate_models.py` from the repository root to
validate the metadata and stage the release pack.
