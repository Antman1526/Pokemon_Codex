# Silph Mid-Floors and Portable PC Implementation Plan

**Goal:** Add Silph Co. 4F-7F middle-act story texture and a functional Portable PC full-access terminal.

**Architecture:** Parent repo owns docs, design data, validators, and exported engine patches. Engine edits are replayed from clean patches, exported as `0027-silph-mid-floors-portable-pc.patch`, then restored clean.

## Task 1: Validator and Design Contract

- [x] Write `tools/validate_silph_mid_floors_portable_pc.py`.
- [x] Run it before implementation and confirm it fails for missing markers.

## Task 2: Design Data

- [x] Add Silph 4F-7F events to `data_design/kanto_chapter.yaml`.
- [x] Add WorldLink messages for Silph mid-floors, Portable PC full access, and Blue pressure.
- [x] Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax.

## Task 3: Engine Patch

- [x] Update Silph 4F text with Gold Dust terminal/buyer evidence.
- [x] Add Silph 5F Portable PC full access terminal that opens `EventScript_PC`.
- [x] Update Silph 6F text with Red civilian-routing context.
- [x] Rewrite Silph 7F Blue scene to feel personal and urgent while preserving the classic battle.
- [x] Export isolated engine patch `0027-silph-mid-floors-portable-pc.patch`.

## Task 4: Verification and Shipping

- [x] Run the targeted validator.
- [x] Replay all engine patches from clean source.
- [x] Run the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [x] Verify ROM header title `NEXUS RED` and game code `BNRE`.
- [x] Restore engine source, commit, and push.
