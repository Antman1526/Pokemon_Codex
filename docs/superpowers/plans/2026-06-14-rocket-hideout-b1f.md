# Rocket Hideout B1F Implementation Plan

Date: 2026-06-14

## Objective

Implement the Rocket Hideout B1F infiltration slice as patch `0020`, using existing map scripts and the existing PC event script where possible.

## Files

- Add: `patches/engine/0020-rocket-hideout-b1f.patch`
- Add: `tools/validate_rocket_hideout_b1f.py`
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `docs/GBA_OPENEMU_BUILD_STRATEGY.md`
- Temporary engine edits before patch export:
  - `engine/pokeemerald-expansion/data/maps/RocketHideout_B1F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/RocketHideout_B1F_Frlg/map.json`

## Steps

- [x] Add failing validator for the Rocket Hideout B1F milestone.
- [x] Update Kanto act data with the B1F infiltration, Red check, Rocket logistics, Gold Dust ledger, and Portable PC beta terminal.
- [x] Add WorldLink messages for B1F infiltration, Gold Dust ledger, and Portable PC beta.
- [x] Add rival progression band for the hideout infiltration.
- [x] Update build notes pending milestone line.
- [x] Replay patches `0001` through `0019` into the engine.
- [x] Add Red object/script near the B1F entrance.
- [x] Add Portable PC beta terminal and call `EventScript_PC`.
- [x] Add Gold Dust ledger clue.
- [x] Rewrite selected B1F grunt text.
- [x] Export the engine diff to `patches/engine/0020-rocket-hideout-b1f.patch`.
- [x] Restore engine source and replay all patches.
- [x] Run the new validator and the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED"` and `GAME_CODE=BNRE`.
- [x] Verify ROM header and size.
- [x] Update build notes with final build details.
- [ ] Restore engine source clean, commit, and push.

## Risk Notes

- `EventScript_PC` depends on the player facing a valid PC tile for visual screen-on effects. The PC menu should still be callable, but if the visual effect is tile-sensitive the terminal will be treated as a controlled beta rather than the final portable implementation.
- B1F should stay a focused story and QoL slice. Deeper hideout floors should remain for the next milestone.
