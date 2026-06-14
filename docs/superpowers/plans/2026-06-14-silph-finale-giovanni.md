# Silph Finale and Giovanni Implementation Plan

**Goal:** Complete Silph Co. 8F-11F with Red's final stair check, Giovanni's Meridian Gate reveal, Master Ball payoff, and the Sabrina/Moonlight handoff.

**Architecture:** Parent repo owns docs, design data, validators, and exported engine patches. Engine edits are replayed from clean patches, exported as `0028-silph-finale-giovanni.patch`, then restored clean.

## Task 1: Validator and Design Contract

- [x] Write `tools/validate_silph_finale_giovanni.py`.
- [x] Run it before implementation and confirm it fails for missing markers.

## Task 2: Design Data

- [x] Add Silph finale events to `data_design/kanto_chapter.yaml`.
- [x] Add WorldLink messages for upper floors, Red, Giovanni, Master Ball, and Sabrina.
- [x] Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax.

## Task 3: Engine Patch

- [x] Update Silph 8F text with Gold Dust buyer-network evidence.
- [x] Update Silph 9F text as an emergency heal hub.
- [x] Add Red to Silph 10F near the final stair.
- [x] Rewrite Silph 11F Giovanni and Master Ball payoff text.
- [x] Export isolated engine patch `0028-silph-finale-giovanni.patch`.

## Task 4: Verification and Shipping

- [x] Run the targeted validator.
- [x] Replay all engine patches from clean source.
- [x] Run the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [x] Verify ROM header title `NEXUS RED` and game code `BNRE`.
- [x] Restore engine source, commit, and push.
