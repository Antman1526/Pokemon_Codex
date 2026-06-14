# Koga Warden Notes and Saffron Lockdown Implementation Plan

**Goal:** Add Koga's status-control story payoff, the Warden habitat-notes theft, and the first Saffron lockdown handoff.

**Architecture:** Parent repo owns design data, docs, validators, and exported engine patches. Engine source is replayed from clean patches, edited only to generate `patches/engine/0025-koga-warden-saffron-lockdown.patch`, then restored clean.

## Task 1: Validator and Design Contract

- [x] Write `tools/validate_koga_warden_saffron_lockdown.py`.
- [x] Run it before implementation and confirm it fails for missing markers.

## Task 2: Design Data

- [x] Add Koga status trial and Saffron lockdown events to `data_design/kanto_chapter.yaml`.
- [x] Add WorldLink messages for Soul Badge clear, Warden notes theft, and Saffron handoff.
- [x] Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax.

## Task 3: Engine Patch

- [x] Update Fuchsia Gym dialogue to frame Koga as the status trial before Saffron.
- [x] Update Warden's House dialogue to preserve the Gold Teeth/HM04 flow while revealing stolen habitat notes.
- [x] Update Saffron Rocket lockdown dialogue to reference Silph, Blue's failed push, and Gold Dust market pressure.
- [x] Export isolated engine patch `0025-koga-warden-saffron-lockdown.patch`.

## Task 4: Verification and Shipping

- [x] Run the targeted validator.
- [x] Replay all engine patches from clean source.
- [x] Run the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [x] Verify ROM header title `NEXUS RED` and game code `BNRE`.
- [x] Restore engine source, commit, and push.
