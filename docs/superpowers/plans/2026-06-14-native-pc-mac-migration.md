# Implementation Plan: Native PC/Mac Migration

Date: 2026-06-14
Target: `POKEMON NEXUS RED` native Windows/macOS build.

## Overview

Move the complete all-nine-region Pokemon Nexus Red vision from a GBA-first implementation path to a native PC/Mac game path. The GBA patch-stack remains a prototype/reference track. The native game should be built as one source project that exports to Windows PC and macOS.

## Architecture Decisions

- Use Godot 4 as the recommended engine for the native build.
- Keep story/content data-driven so nine regions, 10 rivals, companions, encounters, trainers, marts, and WorldLink notifications can scale.
- Preserve classic FireRed-style visual direction with upgraded HD pixel visuals, richer lighting, smoother UI, and widescreen readability without binding the project to GBA memory, save, or UI constraints.
- Start with a Kanto shell and bedroom/lab loop before porting large Pokemon datasets.

## Phase 1: Native Shell

### Task 1: Install/verify Godot

Acceptance:

- `godot --version` or `godot4 --version` works locally.
- Export templates are installed.
- Windows and macOS export presets can be listed or created.

Verification:

```sh
godot --version
godot --headless --version
```

Files likely touched:

- `build_notes/PC_MAC_NATIVE_BUILD_NOTES.md`

### Task 2: Create `native/nexus-red/` project scaffold

Acceptance:

- Godot project opens.
- Main scene boots.
- Title text says `POKEMON NEXUS RED`.
- Input map includes confirm, cancel, menu, sprint, and WorldLink.

Verification:

```sh
godot --headless --path native/nexus-red --check-only --quit
```

Files likely touched:

- `native/nexus-red/project.godot`
- `native/nexus-red/src/`
- `native/nexus-red/scenes/`

### Task 3: Add data loader foundation

Acceptance:

- Native project can load region/chapter data from structured files.
- Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea, and Nexus Island IDs are recognized.
- Current region defaults to Kanto.

Verification:

```sh
godot --headless --path native/nexus-red --run-tests
python3 tools/validate_design_data.py
```

Files likely touched:

- `native/nexus-red/src/data/`
- `native/nexus-red/content/regions/`
- `data_design/region_chapters.yaml`

## Phase 2: First Playable Native Loop

### Task 4: Build bedroom/Mom/Oak intro

Acceptance:

- New game starts in Antman's bedroom.
- Mom scene establishes the strange global migration/news hook.
- Red appears as a warm friend before Oak's lab.
- Oak starts the World Pokedex Initiative.

Verification:

```sh
godot --path native/nexus-red
```

Manual check:

- Start new game and reach Oak's lab without console errors.

### Task 5: Build 39-starter selection prototype

Acceptance:

- All 27 regional starters and 12 special starters appear.
- Player can select one starter.
- Blue receives the first rival counterpick.
- Ava and Dax receive valid starters.
- First Blue pressure dialogue appears after starter selection.

Verification:

```sh
python3 tools/validate_design_data.py
python3 tools/validate_native_starter_slice.py
godot --headless --path native/nexus-red --script tests/starter_slice_test.gd
```

Manual check:

- Select at least one starter from each regional group.

### Task 6: Add first WorldLink prototype

Acceptance:

- WorldLink opens from menu/input.
- Feed shows Blue, Ava, Dax, and Red-related opening entries.
- Notifications pause in dungeon-tagged spaces once dungeon flags exist.

Verification:

```sh
godot --headless --path native/nexus-red --run-tests
python3 tools/validate_native_platform_strategy.py
```

## Phase 3: Kanto Brock Slice

### Task 7: Build Route 1/Viridian/Pewter traversal

Acceptance:

- Player can walk onto a first Route 1 prototype.
- Red appears for the first warm route companion scene.
- Blue battle placeholder records first battle pressure before the real battle engine exists.
- Encounter levels scale with early progression.

Verification:

```sh
python3 tools/validate_native_route1_slice.py
godot --headless --path native/nexus-red --script tests/route1_slice_test.gd
```

### Task 8: Build Brock and Pewter Museum anomaly

Acceptance:

- Brock is Standard-mainline-hard, with harder presets available.
- Red cannot fight the gym for Antman.
- Pewter Museum anomaly introduces the Nexus hook after Brock.

Verification:

- Win Brock battle on Standard.
- Confirm museum scene unlocks only after the badge.

### Task 7.5: Build shared battle placeholder

Acceptance:

- Blue's Route 1 pressure can open a shared battle placeholder screen.
- The screen shows player starter and Blue starter.
- Save state records battle started, result, and finished flags.
- The screen returns to Route 1 after completion.

Verification:

```sh
python3 tools/validate_native_battle_placeholder_slice.py
godot --headless --path native/nexus-red --script tests/battle_placeholder_test.gd
```

### Task 7.6: Add Route 1 WorldLink rumors

Acceptance:

- Blue's Route 1 placeholder battle unlocks the first encounter-rumor layer.
- WorldLink queues Blue, Ava, Dax, Red, and a Johto rival tease after the battle.
- WorldLink renders opening feed, rival batch data, and Route 1 rumors from JSON.
- The feature remains a data/checklist slice until the real encounter engine exists.

Verification:

```sh
python3 tools/validate_native_worldlink_route1_slice.py
godot --headless --path native/nexus-red --script tests/worldlink_route1_test.gd
```

### Task 7.7: Add Route 1 wild encounter shell

Acceptance:

- Route 1 can request a deterministic first wild encounter from JSON data.
- A reusable wild encounter placeholder screen can show the wild creature and player starter.
- Save state records encounter start, result, first-wild seen/caught flags, party roster, and captured creatures.
- The first playable shell remains balanced for pre-Brock progression and does not claim the full battle/capture engine is complete.

Verification:

```sh
python3 tools/validate_native_route1_wild_encounter_slice.py
godot --headless --path native/nexus-red --script tests/route1_wild_encounter_test.gd
```

### Task 7.8: Add minimal wild encounter loop

Acceptance:

- Route 1 wild encounters initialize deterministic HP from encounter data.
- Full-HP capture is blocked in the first loop.
- A simple player attack lowers wild HP without knocking out the tutorial catch.
- A damaged first wild encounter can be caught with a deterministic `catch_success` result.
- Red gives first-capture coaching during the loop.

Verification:

```sh
python3 tools/validate_native_wild_encounter_loop_slice.py
godot --headless --path native/nexus-red --script tests/wild_encounter_loop_test.gd
```

### Task 7.9: Add wild encounter command menu

Acceptance:

- Wild encounters display visible Fight, Catch, and Run commands.
- Fight lowers wild HP through the existing minimal loop.
- Catch remains visible and produces `catch_success` after damage.
- Run remains available through the visible command menu.
- Existing keyboard shortcut behavior still works while the UI matures.

Verification:

```sh
python3 tools/validate_native_wild_command_menu_slice.py
godot --headless --path native/nexus-red --script tests/wild_command_menu_test.gd
```

### Task 7.10: Add Route 1 party status panel

Acceptance:

- Route 1 can show/hide a small field party panel from the menu input.
- The panel reads the actual save-state party roster.
- The panel shows Antman's starter and the first caught Route 1 creature after capture.
- The panel also summarizes captured creatures, giving a base for the later full party menu.

Verification:

```sh
python3 tools/validate_native_route1_party_panel_slice.py
godot --headless --path native/nexus-red --script tests/route1_party_panel_test.gd
```

### Task 7.11: Add Viridian City shell

Acceptance:

- Route 1 can transition north into Viridian City.
- Viridian City is a playable world scene with upgraded FireRed-style placeholder layout.
- The city includes a Pokemon Center shell with Nurse Joy dialogue and a healing flag.
- The city includes a Poke Mart shell that reflects Antman's starting $100000 travel fund.
- Save state records Viridian arrival, Center visit, and Mart visit.

Verification:

```sh
python3 tools/validate_native_viridian_city_slice.py
godot --headless --path native/nexus-red --script tests/viridian_city_test.gd
```

### Task 7.12: Add Viridian Red/Rocket story beat

Acceptance:

- Viridian City has a Red companion check-in.
- Viridian City can surface the first Rocket clue through a Mart shipment lead.
- Save state records the Red scene, Rocket clue, and Viridian story WorldLink queue.
- WorldLink renders the Viridian Red/Rocket/Blue story batch from JSON.

Verification:

```sh
python3 tools/validate_native_viridian_story_slice.py
godot --headless --path native/nexus-red --script tests/viridian_story_test.gd
```

### Task 7.13: Add Route 2 / Viridian Forest gate shell

Acceptance:

- Viridian City can transition north into a Route 2 / Viridian Forest Gate scene after the Rocket clue.
- Red remains the active companion and warns Antman about Rocket activity beyond Viridian.
- Save state records the Route 2 forest gate and Red warning flags.
- The gate can return to Viridian City for the first playable route loop.

Verification:

```sh
python3 tools/validate_native_route2_gate_slice.py
godot --headless --path native/nexus-red --script tests/route2_forest_gate_test.gd
```

### Task 7.14: Add Route 2 catch tutorial encounter

Acceptance:

- Route 2 has its own pre-Brock encounter data that returns to the Viridian Forest Gate scene.
- Red can trigger a first Route 2 catch tutorial before the forest dungeon.
- Save state records Route 2 tutorial seen/caught flags and captures Pidgey.
- The shared wild encounter shell can return to Route 2 instead of always returning to Route 1.

Verification:

```sh
python3 tools/validate_native_route2_catch_tutorial_slice.py
godot --headless --path native/nexus-red --script tests/route2_catch_tutorial_test.gd
```

### Task 7.15: Add Routes 1-3 full starter and bonus migration pool

Acceptance:

- Routes 1-3 have a data contract for all 27 official regional starters.
- Routes 1-3 include the 12 bonus early choices: Eevee, Pikachu, Dratini, Abra, Gastly, Larvitar, Sandile, Kubfu, Staryu, Shroomish, Rockruff, and Ralts.
- The migration pool stays in a pre-Brock level band and distributes 13 entries per route.
- EncounterService exposes query helpers for the full pool, per-route entries, and individual species.

Verification:

```sh
python3 tools/validate_native_early_migration_pool.py
godot --headless --path native/nexus-red --script tests/early_migration_pool_test.gd
```

### Task 7.16: Make Route 1 and Route 2 migration encounters playable

Acceptance:

- EncounterService can pick the next uncaught early migration species for a route.
- Route 1 can trigger its migration encounter pool from the playable scene.
- Route 2 / Viridian Forest Gate can trigger its migration encounter pool from the playable scene.
- Captured migration species are skipped on later migration picks.

Verification:

```sh
python3 tools/validate_native_playable_migration_triggers.py
godot --headless --path native/nexus-red --script tests/playable_migration_triggers_test.gd
```

### Task 7.17: Add playable Route 3 migration scene

Acceptance:

- Route 2 / Viridian Forest Gate can transition north into Route 3.
- Route 3 records save-state progress and keeps Red as the active companion.
- Route 3 can trigger its migration encounter pool, starting with Chespin.
- Wild encounters that start on Route 3 return to Route 3.

Verification:

```sh
python3 tools/validate_native_route3_migration_scene.py
godot --headless --path native/nexus-red --script tests/route3_migration_scene_test.gd
```

## Checkpoint

The native migration is healthy when:

- The Godot project boots locally.
- New game reaches Oak's lab.
- Starter choice persists in save state.
- WorldLink can open.
- A Windows and macOS export command is documented, even if final packaging polish is later.

## Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Godot not installed locally | Blocks native build verification | Install Godot and export templates before scaffold implementation |
| Scope explosion from all Pokemon data | High | Build shell and Kanto loop first; add species data by generation/channel |
| Copyrighted asset handling | High | Use placeholders/original assets in repo; do not commit extracted commercial assets |
| Battle engine complexity | High | Implement a minimal battle loop first, then add modern mechanics incrementally |
| Region content volume | High | Use templates and data pipelines, not one-off scene scripting |

## Open Questions

- Confirmed direction: Godot 4 as a 2D HD pixel RPG engine with a classic FireRed-style structure and original/custom assets.
- Should the initial native battle engine be built in GDScript first, or C# from the start for stronger typing?
- Should PC controls prioritize keyboard/controller only, or include mouse-driven menus?
