# Model metadata

Custom model data entries in `assets/*/items/**/*.json` carry three source-only
fields: `owners`, `name`, and `category`. The release generator removes these
fields from the staged resource pack and exports them to `models.json`.

- `owners`: player usernames or group names prefixed with `@`.
  `@public` is public access; `@staff` is staff access. `@unkown` is the
  requested placeholder for ownership that has not been established.
- `category` and `name`: identifiers beginning with a letter, followed by
  letters, digits, or underscores. Together they identify a registry model.
- Entries sharing a category/name must have identical owners and CMD and are
  combined into one registry model with multiple base items. Equipment types
  use separate names, for example `BlossomSword` and `BlossomPickaxe`.
- CMD numbers may repeat across different base items. Distinct registry models
  cannot claim the same base item and CMD.
- Vanilla reset entries have no metadata and are excluded from the registry
  and missing-metadata audit.

Run `python .github/scripts/generate_models.py` from the repository root to
validate metadata and stage a release under `build/release-pack/`.

## Initial CSV import

The initial metadata uses `Custom Model Data - OSMP S2.csv`, matched by base
item and CMD. Public rows use `@public`; private rows use their owner fields.
Comma/slash-separated owners are split into individual usernames. Existing
branch metadata is preserved. The CSV typos `ThePianoMan` and `SalatFurke9440`
are normalized to `ThePianoMann` and `SalatGurke9440`.

Additional base-item mappings reuse ownership from the same documented model.
The Honey, Honor, Ender, and Blossom equipment additions use PadBro, consistent
with their documented sets. Other undocumented entries use `@unkown`.

The CSV gives both Lilvyse totems the same name; the second is named
`TotemOfUndyingLilvyseVariant` to retain both CMDs.

The CSV-only Anubis Hat entry has no matching custom mapping. Bamboo at golden
carrot CMD 5569102 intentionally uses `minecraft:item/bamboo` and is registered
as food/Bamboo owned by PadBro, as documented in the CSV.
Spingus Coin (paper/9208801) and all
Crab Sword mappings and assets have been removed.

Vanilla reset thresholds have also been removed from the source dispatches.
Range dispatch selects the highest threshold at or below the supplied CMD, so
unassigned values between thresholds now retain the preceding custom model.
The dispatch-level fallback remains intact for values below the first threshold.
