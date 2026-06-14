# Giovanni Silph Scope Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Rocket Hideout Giovanni/Silph Scope payoff as patch `0021`.

**Architecture:** Keep the classic Rocket Hideout progression intact and add narrative pressure through small map objects, script text, and design data. Engine source changes are exported into one patch; the parent repo stores the validator, spec, plan, and build notes.

**Tech Stack:** pokeemerald-expansion FRLG target, event scripts, map JSON, YAML design data, Python validators, devkitARM GBA build.

---

## Files

- Add: `patches/engine/0021-giovanni-silph-scope.patch`
- Add: `tools/validate_giovanni_silph_scope.py`
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`
- Temporary engine edits before patch export:
  - `engine/pokeemerald-expansion/data/maps/RocketHideout_B3F_Frlg/map.json`
  - `engine/pokeemerald-expansion/data/maps/RocketHideout_B3F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/RocketHideout_B4F_Frlg/map.json`
  - `engine/pokeemerald-expansion/data/maps/RocketHideout_B4F_Frlg/scripts.inc`

## Tasks

- [x] Add failing validator `tools/validate_giovanni_silph_scope.py`.
- [x] Run validator and confirm it fails because patch/data/build notes are missing.
- [x] Update Kanto act data with Blue's late arrival, Red's pre-boss check, Giovanni's Meridian hint, Silph Scope return, and Portable PC beta storage handshake.
- [x] Add WorldLink messages for Blue in the hideout, Giovanni's Meridian hint, and Silph Scope return guidance.
- [x] Add rival progression band for the Giovanni/Silph Scope payoff.
- [x] Update build notes with pending `0021`.
- [x] Replay patches `0001` through `0020` into the engine.
- [x] Add Blue object/script to Rocket Hideout B3F.
- [x] Add Red object/script to Rocket Hideout B4F.
- [x] Rewrite B3F grunt text.
- [x] Rewrite Giovanni and Silph Scope pickup text.
- [x] Export engine diff as `patches/engine/0021-giovanni-silph-scope.patch`.
- [x] Restore engine and verify `tools/validate_giovanni_silph_scope.py` passes.
- [x] Replay all patches and run the full validator suite.
- [x] Build `pokenexusred.gba` with `TITLE="NEXUS RED"` and `GAME_CODE=BNRE`.
- [x] Verify ROM header and size.
- [x] Update build notes from pending to complete.
- [ ] Restore engine source clean, commit, and push.

## Risk Notes

- Do not add a full Portable PC key item in this slice; that belongs to Silph Co.
- Keep Giovanni's full conspiracy knowledge limited. He may hint at Meridian infrastructure, but the Nexus Order name should remain unrevealed.
- Avoid adding new trainer IDs unless the boss battle itself is being rebalanced. This slice should build reliably through script and map edits.
