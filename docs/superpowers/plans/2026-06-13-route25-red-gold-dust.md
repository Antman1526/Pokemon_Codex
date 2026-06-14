# Route 25 Red Gold Dust Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first Route 25 Red tag-battle story moment and introduce Team Gold Dust as Rocket's hostile rival faction.

**Architecture:** Keep the engine patch-driven. Apply patches `0001` through `0012`, edit Route 25, Sea Cottage, and FRLG trainer data, generate patch `0013`, then restore the engine to clean upstream. Record WorldLink as one-region-at-a-time story progression in design data.

**Tech Stack:** pokeemerald-expansion FRLG map scripts/map JSON, FRLG trainer party data, YAML design data, Python validators, devkitARM GBA build.

---

### Task 1: Design Records

**Files:**
- Create: `docs/superpowers/specs/2026-06-13-route25-red-gold-dust-design.md`
- Create: `docs/superpowers/plans/2026-06-13-route25-red-gold-dust.md`
- Create: `data_design/worldlink_region_progression.yaml`
- Modify: `data_design/red_tag_battle_policy.yaml`

- [ ] Record Route 25 as the first playable Red tag battle.
- [ ] Record Team Gold Dust's Kanto debut and hostility toward Rocket.
- [ ] Record WorldLink's one-region-at-a-time travel rule.
- [ ] Update Kanto's tag-battle policy from candidate wording to Route 25 implementation wording.

### Task 2: Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/Route25_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/Route25_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/Route25_SeaCottage_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/src/data/trainers_frlg.party`
- Create: `patches/engine/0013-route25-red-gold-dust-tag.patch`

- [ ] Apply patches `0001` through `0012`.
- [ ] Add Red, Rocket, and Gold Dust objects near Sea Cottage.
- [ ] Add a Route 25 script that uses `trainerbattle_two_trainers`.
- [ ] Add post-battle dialogue confirming Antman and Red's first tag win.
- [ ] Add one new Rocket trainer and one new Gold Dust trainer around level 18.
- [ ] Rewrite Bill's first request text to mention WorldLink interference while preserving his classic rescue flow.
- [ ] Generate `0013` from only the Route 25, Sea Cottage, and trainer data files.

### Task 3: Validation And Build

**Files:**
- Create: `tools/validate_route25_red_gold_dust.py`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] Add validator coverage for patch presence, Route 25 objects/scripts, trainer data, Bill text, and WorldLink progression data.
- [ ] Run all validators.
- [ ] Build `pokenexusred.gba`.
- [ ] Verify the ROM header.
- [ ] Restore the engine submodule to clean upstream.

### Task 4: Commit And Push

- [ ] Confirm project status.
- [ ] Commit with message `Add Route 25 Red Gold Dust tag setup`.
- [ ] Push the feature branch.
