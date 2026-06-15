# Kanto Vertical Slice Mapping To PSDK

This file maps the current Godot reference prototype into Pokemon Studio / PSDK implementation concepts.

## Source References

- Godot reference root: `native/nexus-red/`
- Starter data: `native/nexus-red/content/starters/starter_choices.json`
- Early migration pool: `native/nexus-red/content/encounters/route_1_to_3_migration_encounters.json`
- PSDK import contract: `psdk/nexus-red/docs/studio-data-notes/STARTER_AND_EARLY_ROUTE_IMPORT_CONTRACT.md`
- PSDK import seed manifest: `psdk/nexus-red/project/Data/nexus_red_seed/import_manifest.json`
- WorldLink batches: `native/nexus-red/content/worldlink/`
- Main story docs: `docs/POKEMON_NEXUS_RED_FRAMEWORK.md`
- PSDK strategy: `docs/PSDK_NATIVE_BUILD_STRATEGY.md`

## First PSDK Playable Scope

Target: a small but real PSDK Pallet-to-Route-1 loop.

Required beats:

1. Antman starts in bedroom.
2. Mom establishes the strange migration/news hook.
3. Red appears as Antman's warm full-game friend.
4. Oak starts the World Pokedex Initiative.
5. Player chooses from the 39 first-partner contract.
6. Blue receives a counter-pick and applies first rival pressure.
7. Route 1 introduces Red's companion presence and first wild/catch setup.
8. WorldLink is stubbed as a menu/event feed or placeholder event until custom UI scripting is ready.

## Godot-To-PSDK Concept Mapping

| Current Godot concept | PSDK target concept |
| --- | --- |
| `SaveState.gd` story flags | PSDK game variables/switches plus custom Ruby state helpers |
| Scene scripts under `src/world/` | PSDK maps/events plus Ruby helper scripts |
| `content/starters/starter_choices.json` | Pokemon Studio creature/trainer data plus starter-selection event data |
| `content/encounters/route_1_to_3_migration_encounters.json` | Studio encounter zones or custom encounter table data |
| `content/worldlink/*.json` | Custom WorldLink data files consumed by PSDK Ruby scripts |
| `BattlePlaceholder.gd` | Native PSDK battle calls and trainer data |
| Godot labels/dialogue text | PSDK event text entries/translations |
| Godot route transition signals | Map transfers and event commands |

## 39-Starter Contract

The first PSDK import must preserve:

- all 27 official regional starters,
- 12 special starters: Eevee, Pikachu, Dratini, Abra, Gastly, Larvitar, Sandile, Kubfu, Staryu, Shroomish, Rockruff, Ralts,
- Blue counter-pick rules,
- Ava/Dax starter assignment,
- early Routes 1-3 catchability,
- pre-Brock level safety.

Detailed import rows live in `psdk/nexus-red/docs/studio-data-notes/STARTER_AND_EARLY_ROUTE_IMPORT_CONTRACT.md`.
Machine-readable source/target mappings live in `psdk/nexus-red/project/Data/nexus_red_seed/import_manifest.json`.
Generated seed data is refreshed with `python3 tools/generate_psdk_seed_data.py`.

## Routes 1-3 Catchability Contract

Current Godot reference distribution:

- Route 1: Kanto/Johto starters plus Eevee, Pikachu, Abra, Gastly, Ralts, Shroomish, Rockruff.
- Route 2: Hoenn/Sinnoh/Unova starters plus Sandile, Staryu, Dratini, Larvitar.
- Route 3: Kalos/Alola/Galar/Paldea starters plus Kubfu.

Keep the levels progression-safe:

- Route 1: mostly level 4-5.
- Route 2: mostly level 5-6.
- Route 3: mostly level 6-7.
- High-power species such as Dratini, Larvitar, and Kubfu should stay rare and later within the first-route cluster.

## Custom Systems To Script In PSDK

Initial Ruby/custom-system targets:

- WorldLink feed/checklist data loader.
- Companion state for Red.
- Rival state for Blue, Ava, and Dax.
- Starter-selection rules.
- Dungeon notification pause/digest rules.
- Faction ID registry: Rocket, Magma, Aqua, Phoenix, Moonlight, Gold Dust, Gas, Clover, Nexus Order.

## Do Not Import Yet

Do not import all regions, all creature data overrides, or final art/audio at once.

The first PSDK implementation should prove:

- project opens,
- map transfer works,
- starter selection works,
- one battle works through PSDK,
- one encounter table works,
- one WorldLink-style event can display.
