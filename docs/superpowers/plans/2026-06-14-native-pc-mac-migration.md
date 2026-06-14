# Implementation Plan: Native PC/Mac Migration

Date: 2026-06-14
Target: `POKEMON NEXUS RED` native Windows/macOS build.

## Overview

Move the complete all-nine-region Pokemon Nexus Red vision from a GBA-first implementation path to a native PC/Mac game path. The GBA patch-stack remains a prototype/reference track. The native game should be built as one source project that exports to Windows PC and macOS.

## Architecture Decisions

- Use Godot 4 as the recommended engine for the native build.
- Keep story/content data-driven so nine regions, 10 rivals, companions, encounters, trainers, marts, and WorldLink notifications can scale.
- Preserve FireRed-first visual direction without binding the project to GBA memory, save, or UI constraints.
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
godot --headless --path native/nexus-red --check-only
```

Files likely touched:

- `native/nexus-red/project.godot`
- `native/nexus-red/src/`
- `native/nexus-red/scenes/`

### Task 3: Add data loader foundation

Acceptance:

- Native project can load region/chapter data from structured files.
- Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea, and World Nexus Championship IDs are recognized.
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

Verification:

```sh
python3 tools/validate_design_data.py
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

- Player can walk from Pallet to Route 1, Viridian, and Pewter.
- Red appears for warm training scenes.
- Encounter levels scale with early progression.

Verification:

- Manual 20-minute smoke test.

### Task 8: Build Brock and Pewter Museum anomaly

Acceptance:

- Brock is Standard-mainline-hard, with harder presets available.
- Red cannot fight the gym for Antman.
- Pewter Museum anomaly introduces the Nexus hook after Brock.

Verification:

- Win Brock battle on Standard.
- Confirm museum scene unlocks only after the badge.

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

- Should the first native art style use placeholder FireRed-like tiles, HD pixel art, or a clean original chibi style?
- Should the initial native battle engine be built in GDScript first, or C# from the start for stronger typing?
- Should PC controls prioritize keyboard/controller only, or include mouse-driven menus?
