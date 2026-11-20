# Ordinary SMP Resource Pack

Custom hats, tools, food, totems, decorations, trophies, and other models for Ordinary SMP.

This repository contains the assets for the Ordinary SMP Minecraft Java resource pack.

## Contribution Guidelines

All contributions should follow these guidelines to keep the pack consistent with the spirit of Ordinary SMP.

### What We're Looking For

- **Cosmetic Items:** Hats, gear, trophies, banners, decorations, and other visual items.
- **Event & Achievement Rewards:** Custom items earned through events or completing challenges.
- **Easter Eggs:** Fun, hidden items that don't affect gameplay or cause confusion.
- **Other Creative Ideas:** Unique additions that fit the server's overall style.

### General Rules

- All submissions must follow our community guidelines and be suitable for all ages.
- Items should fit the vanilla Minecraft aesthetic and our HermitCraft-like server atmosphere.
- Items must not give players an unfair gameplay advantage.
- Avoid visuals that could be confused with existing Minecraft items or mislead players during gameplay.
- Avoid unnecessarily large textures, models, or other assets that could impact pack size or performance.

## Adding Content

When contributing new items or models, please follow these conventions:

- Asset filenames must use `snake_case`.
- Registry names must use `PascalCase`.
- Place models and textures in the appropriate category folders.
- Carved-pumpkin models and textures must go under `block/` to keep their atlas consistent.
- Every category must have a non-empty description in `descriptions.json`.
- All textures must be credited in [CREDITS.md](credits/CREDITS.md).
- **Tools:** When adding a new tool model, make sure it is applied to all material variants of that tool (wooden, stone, copper, iron, golden, diamond, and netherite).

### CustomModelData

CustomModelData values must be assigned sequentially, starting at `1001`.

- Each new model gets the next available value.
- Every model must have its own unique CustomModelData value.
- Never reuse a value already assigned to another model.
- CMD values may repeat across different base items, but distinct registry models
  must not claim the same base-item/CMD pair.
- Do not renumber existing models, even if values are removed or gaps appear.

**Note:** Older models may still use randomly assigned CustomModelData values from our previous system. These are kept for compatibility and should not be changed. The sequential numbering rule applies to all new models.

## Submitting Your Contribution

1. Create your design and prepare the necessary models and textures.
2. Submit your contribution through a pull request or the designated [Discord ticket](https://discord.com/channels/1216052687645184010/1216108845831688262).
3. The admin team will review submissions to make sure they follow the guidelines.

Approved contributions may be added to the resource pack!

## Credits

Thank you to the artists and creators whose textures and models appear in this pack.

- [Texture credits](credits/CREDITS.md) - Individual credits and original sources.
- [Missing texture credits](credits/MISSING_SOURCES.md) - Credits and sources we are still working to recover.

If your textures are included in this pack and your credit is missing or incorrect, please let us know so we can give you proper credit.