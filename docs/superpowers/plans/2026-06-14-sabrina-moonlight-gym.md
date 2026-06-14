# Sabrina Moonlight Gym Implementation Plan

**Goal:** Add the Saffron Gym Moonlight-distortion chapter after Silph while preserving the classic Sabrina battle flow.

**Architecture:** Parent repo owns docs, design data, validators, and exported engine patches. Engine edits are replayed from clean patches, exported as `0029-sabrina-moonlight-gym.patch`, then restored clean.

## Task 1: Validator and Design Contract

- [x] Write `tools/validate_sabrina_moonlight_gym.py`.
- [x] Run it before implementation and confirm it fails for missing markers.

## Task 2: Design Data

- [x] Add Sabrina Moonlight events to `data_design/kanto_chapter.yaml`.
- [x] Add WorldLink messages for Gym distortion, Red/Misty gate support, and Marsh Badge stabilization.
- [x] Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax.

## Task 3: Engine Patch

- [x] Add Red and Misty outside Saffron Gym.
- [x] Add a Moonlight Veil Gym interaction.
- [x] Rewrite Sabrina/Gym text around Moonlight distortion and WorldLink stabilization.
- [x] Export isolated engine patch `0029-sabrina-moonlight-gym.patch`.

## Task 4: Verification and Shipping

- [x] Run the targeted validator.
- [x] Replay all engine patches from clean source.
- [x] Run the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [x] Verify ROM header title `NEXUS RED` and game code `BNRE`.
- [x] Restore engine source, commit, and push.
