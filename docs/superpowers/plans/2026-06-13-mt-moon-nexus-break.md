# Mt. Moon Nexus Break Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Mt. Moon Nexus Break story slice and record Red tag battles as a recurring full-game design pillar.

**Architecture:** The engine remains patch-driven. Apply patches `0001` through `0010`, edit the Mt. Moon FRLG map scripts/object data, generate patch `0011`, then restore the engine to clean upstream. Project-owned validators prove the patch stack recreates the behavior.

**Tech Stack:** pokeemerald-expansion FRLG scripts/map JSON, project patch files, Python validators, devkitARM GBA build.

---

### Task 1: Design Artifacts

**Files:**
- Create: `docs/superpowers/specs/2026-06-13-mt-moon-nexus-break-design.md`
- Create: `docs/superpowers/plans/2026-06-13-mt-moon-nexus-break.md`
- Create: `data_design/red_tag_battle_policy.yaml`

- [ ] Write the Mt. Moon spec with Red, Rocket, Miguel, fossil artifact, and Option B recurring tag-battle rules.
- [ ] Write this implementation plan.
- [ ] Add `data_design/red_tag_battle_policy.yaml` so future region work has a concrete Red tag-battle policy.

### Task 2: Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/MtMoon_1F_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/MtMoon_1F_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/MtMoon_B2F_Frlg/scripts.inc`
- Create: `patches/engine/0011-mt-moon-nexus-break.patch`

- [ ] Apply patches `0001` through `0010`.
- [ ] Add Red's Mt. Moon companion object and dialogue on 1F.
- [ ] Rewrite Rocket, Miguel, and fossil text on B2F.
- [ ] Generate `0011` from only the Mt. Moon changed files.
- [ ] Restore the engine submodule to clean upstream.

### Task 3: Validation And Build

**Files:**
- Create: `tools/validate_mt_moon_nexus_break.py`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] Add a validator for patch file presence, Red object/dialogue, Rocket Nexus text, Miguel rewrite, and fossil artifact text.
- [ ] Apply patches `0001` through `0011`.
- [ ] Run `python3 tools/validate_design_data.py`.
- [ ] Run `python3 tools/validate_nexus_milestone.py`.
- [ ] Run `python3 tools/validate_act1_brock_red_pewter.py`.
- [ ] Run `python3 tools/validate_mt_moon_nexus_break.py`.
- [ ] Build the ROM with `make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.
- [ ] Verify the GBA header is `NEXUS RED` / `BNRE`.
- [ ] Restore the engine submodule to clean upstream.

### Task 4: Commit And Push

**Files:**
- Commit all project-owned docs, data, patch, validator, and build-note changes.

- [ ] Confirm `git -C engine/pokeemerald-expansion status --short` is empty.
- [ ] Commit with message `Add Mt Moon Nexus Break slice`.
- [ ] Push `feature/first-playable-title-opening`.
