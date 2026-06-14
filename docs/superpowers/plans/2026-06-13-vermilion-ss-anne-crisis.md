# Vermilion S.S. Anne Crisis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Blue jealousy, Vermilion Harbor, and S.S. Anne faction-crisis milestone as patch `0014`.

**Architecture:** Keep the parent repo patch-driven workflow. Apply patches `0001` through `0013`, edit the engine tree, generate one project-owned patch, then restore the engine tree. Store story policy in YAML and verify with a focused Python validator.

**Tech Stack:** pokeemerald-expansion FireRed maps/scripts, FRLG trainer party text data, project YAML design files, Python validators.

---

### Task 1: Record The Story Decisions

**Files:**
- Create: `docs/superpowers/specs/2026-06-13-vermilion-ss-anne-crisis-design.md`
- Modify: `data_design/companions.yaml`
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/worldlink_region_progression.yaml`

- [ ] Add the approved story spec.
- [ ] Update Misty's Kanto presence to include post-S.S. Anne joining.
- [ ] Update Kanto act 3 required events to name Blue jealousy, S.S. Anne faction crisis, and Johto harbor hint.
- [ ] Update WorldLink region progression to record Vermilion Harbor as a locked Johto preview.

### Task 2: Add Engine Patch 0014

**Files:**
- Modify in engine: `data/maps/VermilionCity_Frlg/map.json`
- Modify in engine: `data/maps/VermilionCity_Frlg/scripts.inc`
- Modify in engine: `data/maps/SSAnne_2F_Corridor_Frlg/map.json`
- Modify in engine: `data/maps/SSAnne_2F_Corridor_Frlg/scripts.inc`
- Modify in engine: `data/maps/SSAnne_CaptainsOffice_Frlg/scripts.inc`
- Modify in engine: `include/constants/opponents_frlg.h`
- Modify in engine: `src/data/trainers_frlg.party`
- Create: `patches/engine/0014-vermilion-ss-anne-crisis.patch`

- [ ] Add Vermilion Red, Blue, and Misty story objects.
- [ ] Add Vermilion scripts for Blue jealousy, Red harbor warning, Misty pre-crisis watch, Misty post-crisis joining, and Johto locked WorldLink hint.
- [ ] Rewrite S.S. Anne Blue rival intro/post-battle text.
- [ ] Add S.S. Anne 2F crisis objects for Rocket, Gold Dust, and Bell Tower courier.
- [ ] Add a two-trainer battle against Rocket and Gold Dust.
- [ ] Add trainer constants and trainer parties around level 22.
- [ ] Rewrite Captain text to include the manifest and Johto signal while preserving HM01.
- [ ] Generate patch `0014` against the `0001` through `0013` baseline.

### Task 3: Add Validator And Build Notes

**Files:**
- Create: `tools/validate_vermilion_ss_anne_crisis.py`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] Add validator checks for design data, patch presence, Vermilion object/scripts, S.S. Anne crisis scripts, trainer constants/data, and Captain text.
- [ ] Add patch `0014` and the new validator to the smoke-test notes.
- [ ] Add manual checklist items for Blue jealousy, S.S. Anne crisis, Misty joining, and Johto lock hint.

### Task 4: Verify, Build, Commit

**Files:**
- Verify all touched files.

- [ ] Restore engine clean.
- [ ] Reapply every patch in `patches/engine/*.patch` in sorted order.
- [ ] Run all existing validators plus `python3 tools/validate_vermilion_ss_anne_crisis.py`.
- [ ] Build FireRed with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [ ] Verify ROM header reads `NEXUS RED` and `BNRE`.
- [ ] Restore engine clean again.
- [ ] Commit with message `Add Vermilion S.S. Anne crisis setup`.
- [ ] Push `feature/first-playable-title-opening`.
