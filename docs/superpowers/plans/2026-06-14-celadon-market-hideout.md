# Celadon Market Hideout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Celadon market, Gold Dust buyer, Rocket Game Corner, Erika bridge, and Ability Capsule access milestone as patch `0019`.

**Architecture:** Keep implementation patch-driven. Write a validator first, update design data, replay patches `0001` through `0018`, edit Celadon maps/scripts, export only the incremental `0019` patch, restore the engine, replay all patches, run validators, build the ROM, and verify the ROM header.

**Tech Stack:** pokeemerald-expansion FRLG target, project-owned engine patches, Python validators, YAML design data, OpenEmu-compatible `.gba` build.

---

## Files

- Create: `tools/validate_celadon_market_hideout.py`
- Create: `patches/engine/0019-celadon-market-hideout.patch`
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`
- Engine source while patch is generated:
  - `engine/pokeemerald-expansion/data/maps/CeladonCity_Restaurant_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/CeladonCity_Restaurant_Frlg/map.json`
  - `engine/pokeemerald-expansion/data/maps/CeladonCity_GameCorner_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/CeladonCity_DepartmentStore_2F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/CeladonCity_DepartmentStore_2F_Frlg/map.json`
  - `engine/pokeemerald-expansion/data/maps/CeladonCity_Gym_Frlg/scripts.inc`

## Task 1: Validator Red

- [ ] **Step 1: Create validator**

Create `tools/validate_celadon_market_hideout.py` that checks:

- `patches/engine/0019-celadon-market-hideout.patch` exists.
- Patch text references the Restaurant, Game Corner, Department Store 2F, and Gym script/map files.
- Patch text includes `CeladonCity_Restaurant_EventScript_GoldDustBuyer`, `Team Gold Dust`, `Celadon buyer`, `Rocket Game Corner`, `WorldLink`, `ITEM_ABILITY_CAPSULE`, `Ability Capsule`, `CeladonCity_DepartmentStore_2F_EventScript_AbilityCapsuleVendor`, and `Erika`.
- Design data includes `celadon_gold_dust_buyer`, `rocket_game_corner_worldlink_pulse`, `ability_capsule_vendor_field_trial`, `erika_market_warning`, and `celadon_market_hideout`.
- WorldLink message data includes `WL_KANTO_CELADON_MARKET_SIGNAL`, `WL_KANTO_GAME_CORNER_HIDEOUT`, `WL_KANTO_ABILITY_CAPSULE_TRIAL`, and `WL_KANTO_ERIKA_MARKET_WARNING`.
- Rival progression includes `celadon_market_hideout` with Blue, Ava, Dax, Red, Misty, Brock, and Lyra markers.
- Build notes include `0019-celadon-market-hideout.patch` and `validate_celadon_market_hideout.py`.

- [ ] **Step 2: Run validator to verify failure**

Run:

```bash
python3 tools/validate_celadon_market_hideout.py
```

Expected: failure because the patch and markers are not implemented yet.

## Task 2: Design Data

- [ ] **Step 1: Update Kanto chapter**

Add `celadon_gold_dust_buyer`, `rocket_game_corner_worldlink_pulse`, `ability_capsule_vendor_field_trial`, and `erika_market_warning` under Act 4 required events.

- [ ] **Step 2: Add WorldLink messages**

Add messages for Celadon market signal, Game Corner hideout, Ability Capsule field trial, and Erika's market warning.

- [ ] **Step 3: Add rival progression band**

Add `celadon_market_hideout` with companion/rival notifications for Red, Misty, Brock, Blue, Ava, Dax, and Lyra.

## Task 3: Engine Patch

- [ ] **Step 1: Replay patches through 0018**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
for patch in $(ls patches/engine/*.patch | sort); do
  git -C engine/pokeemerald-expansion apply ../../${patch}
done
```

- [ ] **Step 2: Add Restaurant Gold Dust buyer**

Add a gentleman object and script in `CeladonCity_Restaurant_Frlg` that identifies him as a Team Gold Dust buyer looking for Rocket's rare anchors.

- [ ] **Step 3: Add Department Store Ability Capsule vendor**

Add a scientist object and a mart script selling `ITEM_ABILITY_CAPSULE` on Department Store 2F.

- [ ] **Step 4: Rewrite Game Corner text**

Update the basement rumor, poster switch, Rocket grunt, and selected NPC text to reference WorldLink, Rocket Game Corner, and Gold Dust buyers.

- [ ] **Step 5: Rewrite Erika text**

Keep the battle intact and adjust post-battle/TM text to point toward Celadon's rare trade and the patience/status-control lesson.

- [ ] **Step 6: Export incremental patch**

Reverse patches `0018` through `0001`, write the remaining diff to `patches/engine/0019-celadon-market-hideout.patch`, then restore the engine.

## Task 4: Verification

- [ ] **Step 1: Run new validator**

Run:

```bash
python3 tools/validate_celadon_market_hideout.py
```

Expected: pass.

- [ ] **Step 2: Replay all engine patches**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
for patch in $(ls patches/engine/*.patch | sort); do
  git -C engine/pokeemerald-expansion apply ../../${patch}
done
```

Expected: all patches apply cleanly.

- [ ] **Step 3: Run validators**

Run all validator scripts under `tools/validate_*.py`.

- [ ] **Step 4: Build ROM and verify header**

Build with `TITLE="NEXUS RED"` and `GAME_CODE=BNRE`, then verify title `NEXUS RED`, game code `BNRE`, and 32 MB ROM size.

## Task 5: Commit

- [ ] **Step 1: Restore engine clean**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
git status --short
```

- [ ] **Step 2: Commit and push**

Run:

```bash
git add docs/superpowers/specs/2026-06-14-celadon-market-hideout-design.md docs/superpowers/plans/2026-06-14-celadon-market-hideout.md tools/validate_celadon_market_hideout.py data_design/kanto_chapter.yaml data_design/kanto_worldlink_messages.yaml data_design/rival_progression_kanto.yaml build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md patches/engine/0019-celadon-market-hideout.patch
git commit -m "Add Celadon market hideout setup"
git push
```
