# Cerulean Misty Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Cerulean companion and Nugget Bridge Nexus setup slice.

**Architecture:** Keep the engine patch-driven. Apply patches `0001` through `0011`, edit untouched Cerulean/Route24 FRLG map scripts and object data, generate patch `0012`, then restore the engine to clean upstream.

**Tech Stack:** pokeemerald-expansion FRLG scripts/map JSON, YAML design data, Python validators, devkitARM GBA build.

---

### Task 1: Design Records

**Files:**
- Create: `docs/superpowers/specs/2026-06-13-cerulean-misty-bridge-design.md`
- Create: `docs/superpowers/plans/2026-06-13-cerulean-misty-bridge.md`
- Modify: `data_design/red_tag_battle_policy.yaml`

- [ ] Record the Cerulean surprise decisions.
- [ ] Add the plan.
- [ ] Update the Kanto tag-battle candidate from broad wording to the Cerulean bridge/Rocket arc.

### Task 2: Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/CeruleanCity_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/CeruleanCity_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/CeruleanCity_Gym_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/Route24_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/Route24_Frlg/map.json`
- Create: `patches/engine/0012-cerulean-misty-bridge-setup.patch`

- [ ] Apply patches `0001` through `0011`.
- [ ] Add Red and Misty city scenes in Cerulean.
- [ ] Add a post-Cascade Badge Misty scene pointer in the gym.
- [ ] Rewrite Nugget Bridge Rocket text around Nexus recruitment.
- [ ] Add Red's Route 24 tag-battle setup scene.
- [ ] Generate `0012` from only the Cerulean/Route24 changed files.

### Task 3: Validation And Build

**Files:**
- Create: `tools/validate_cerulean_misty_bridge.py`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] Add validator coverage for Red, Misty, Nugget Bridge Rocket, and patch presence.
- [ ] Run all validators.
- [ ] Build `pokenexusred.gba`.
- [ ] Verify the ROM header.
- [ ] Restore the engine submodule to clean upstream.

### Task 4: Commit And Push

- [ ] Confirm project status.
- [ ] Commit with message `Add Cerulean Misty Bridge setup`.
- [ ] Push the feature branch.
