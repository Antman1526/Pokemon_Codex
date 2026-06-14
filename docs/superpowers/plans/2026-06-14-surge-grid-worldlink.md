# Surge Grid And WorldLink Feed Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Lt. Surge grid-sabotage, Trail Cutter prototype, Fan Club Gold Dust clue, and first compact rival notification batch as patch `0015`.

**Architecture:** Preserve the project-owned patch stack. Apply patches through `0014`, edit engine map/script/trainer files, generate one `0015` patch, validate with a focused Python script, build the OpenEmu-compatible `.gba`, then restore the engine submodule clean.

**Tech Stack:** pokeemerald-expansion FireRed map scripts, FRLG trainer party data, YAML design files, Python validators, devkitARM build.

---

### Task 1: Update Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `data_design/kanto_boss_teams.yaml`
- Create: `docs/superpowers/specs/2026-06-14-surge-grid-worldlink-design.md`

- [ ] Add the Surge grid sabotage event to Kanto act 3.
- [ ] Add Trail Cutter prototype and WorldLink rival feed events to Kanto act 3.
- [ ] Add WorldLink messages for Surge prep, the post-Surge rival batch, and locked Lyra/Johto profile.
- [ ] Add rival progression entries for Blue, Ava, Dax, and Lyra around Vermilion.
- [ ] Ensure Surge design data remains Voltorb 21, Pikachu 22, Raichu 24.

### Task 2: Add Engine Patch 0015

**Files:**
- Modify in engine: `data/maps/VermilionCity_Gym_Frlg/map.json`
- Modify in engine: `data/maps/VermilionCity_Gym_Frlg/scripts.inc`
- Modify in engine: `data/maps/VermilionCity_PokemonFanClub_Frlg/scripts.inc`
- Modify in engine: `data/maps/VermilionCity_Frlg/scripts.inc`
- Modify in engine: `include/constants/opponents_frlg.h`
- Modify in engine: `src/data/trainers_frlg.party`
- Create: `patches/engine/0015-surge-grid-worldlink.patch`

- [ ] Add a Rocket sabotage NPC to Vermilion Gym.
- [ ] Add one Rocket trainer at level 23 with Electric-disruption flavor.
- [ ] Update Surge's intro/reward/post-battle text.
- [ ] Raise Surge's Pikachu to level 22.
- [ ] Add post-badge WorldLink rival feed text.
- [ ] Add Trail Cutter prototype text after Surge.
- [ ] Add Gold Dust/Celadon clue to Fan Club worker text.
- [ ] Update Red/Misty harbor post-crisis text for Surge prep.
- [ ] Generate patch `0015` against the `0001` through `0014` baseline.

### Task 3: Validate And Build

**Files:**
- Create: `tools/validate_surge_grid_worldlink.py`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] Add validator checks for patch file, Gym Rocket object/script, trainer constants/data, Surge team, Fan Club clue, WorldLink messages, and build notes.
- [ ] Update smoke-test notes with patch `0015`, validator command, and manual checks.
- [ ] Reapply all patches from clean engine state.
- [ ] Run all validators.
- [ ] Build `pokenexusred.gba` with `TITLE="NEXUS RED"` and `GAME_CODE=BNRE`.
- [ ] Verify ROM header.
- [ ] Restore engine clean.
- [ ] Commit and push.
