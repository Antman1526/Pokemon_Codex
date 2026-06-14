# Saffron Arrival and Silph Lower Floors Implementation Plan

**Goal:** Add Saffron arrival, Red's Silph split, and the first Silph Co. lower-floor lockdown setup.

**Architecture:** Parent repo owns docs, design data, validators, and exported engine patches. Engine edits are replayed from clean patches, exported as `0026-saffron-silph-lower-floors.patch`, then restored clean.

## Task 1: Validator and Design Contract

- [x] Write `tools/validate_saffron_silph_lower_floors.py`.
- [x] Run it before implementation and confirm it fails for missing markers.

## Task 2: Design Data

- [x] Add Saffron/Silph lower-floor events to `data_design/kanto_chapter.yaml`.
- [x] Add WorldLink messages for Saffron arrival, lobby lockdown, and lower-floor routing.
- [x] Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax.

## Task 3: Engine Patch

- [x] Add Red to Saffron City with pre/post-Soul Badge arrival dialogue.
- [x] Update Saffron/Silph sign text for the lower-floor objective.
- [x] Update Silph 1F lobby, 2F logistics, and 3F Blue clue text.
- [x] Export isolated engine patch `0026-saffron-silph-lower-floors.patch`.

## Task 4: Verification and Shipping

- [x] Run the targeted validator.
- [x] Replay all engine patches from clean source.
- [x] Run the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [x] Verify ROM header title `NEXUS RED` and game code `BNRE`.
- [x] Restore engine source, commit, and push.
