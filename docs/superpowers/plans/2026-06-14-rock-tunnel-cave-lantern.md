# Rock Tunnel Cave Lantern Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Rock Tunnel Cave Lantern slice so Thunder Badge enables automatic cave lighting, Brock gives cave guidance, Red supports Antman, and Moonlight is foreshadowed before Lavender.

**Architecture:** Keep engine changes in `patches/engine/0017-rock-tunnel-cave-lantern.patch`. Use existing `FLAG_SYS_USE_FLASH` behavior for lighting; do not create a new item system yet. Project-owned design data and validation live in the parent repo.

**Tech Stack:** pokeemerald-expansion FireRed target, FRLG map scripts, JSON map events, YAML design data, Python validation scripts, patch replay workflow.

---

### Task 1: Validator First

**Files:**
- Create: `tools/validate_rock_tunnel_cave_lantern.py`

- [ ] **Step 1: Write the failing validator**

Create a validator that checks:
- `patches/engine/0017-rock-tunnel-cave-lantern.patch`
- `FLAG_SYS_USE_FLASH` in Rock Tunnel 1F transition
- `OBJ_EVENT_GFX_BROCK` and `Route10_PokemonCenter_1F_EventScript_BrockCaveLantern`
- `OBJ_EVENT_GFX_RED` and `RockTunnel_1F_EventScript_RedCaveLantern`
- `RockTunnel_B1F_EventScript_MoonlightEcho`
- text markers `Cave Lantern`, `WorldLink`, `Thunder Badge`, `Moonlight Echo`, `low-light static`
- design data markers and build-note markers

- [ ] **Step 2: Run validator to verify it fails**

Run:

```bash
python3 tools/validate_rock_tunnel_cave_lantern.py
```

Expected: failure because patch and markers are missing.

### Task 2: Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`

- [ ] **Step 1: Add Act 4 events**

Add:
- `cave_lantern_auto_flash_protocol`
- `brock_route10_cave_lantern_advice`
- `red_rock_tunnel_companion_check`
- `moonlight_echo_low_light_static`
- `lavender_low_light_static_arrival`

- [ ] **Step 2: Add WorldLink messages**

Add:
- `WL_KANTO_CAVE_LANTERN_READY`
- `WL_KANTO_RED_ROCK_TUNNEL_CHECK`
- `WL_KANTO_MOONLIGHT_ECHO`

- [ ] **Step 3: Add rival/companion progression**

Add `rock_tunnel_lavender_approach` with Brock, Red, Misty, Blue, Ava, Dax, and Lyra updates.

### Task 3: Engine Patch

**Files:**
- Create: `patches/engine/0017-rock-tunnel-cave-lantern.patch`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/Route10_PokemonCenter_1F_Frlg/map.json`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/Route10_PokemonCenter_1F_Frlg/scripts.inc`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/RockTunnel_1F_Frlg/map.json`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/RockTunnel_1F_Frlg/scripts.inc`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/RockTunnel_B1F_Frlg/map.json`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/RockTunnel_B1F_Frlg/scripts.inc`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/LavenderTown_Frlg/scripts.inc`

- [ ] **Step 1: Replay patches 0001-0016**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
for patch in $(ls patches/engine/*.patch | sort); do
  git -C engine/pokeemerald-expansion apply ../../${patch}
done
```

- [ ] **Step 2: Add Cave Lantern scripting**

Set `FLAG_SYS_USE_FLASH` in Rock Tunnel 1F after Thunder Badge. Add Brock, Red, Moonlight Echo, and Lavender low-light static text.

- [ ] **Step 3: Export incremental patch**

Reverse patches `0001` through `0016`, export diff to `0017`, then restore the engine.

### Task 4: Verification

**Files:**
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Run new validator**

Run:

```bash
python3 tools/validate_rock_tunnel_cave_lantern.py
```

Expected: `Rock Tunnel Cave Lantern validation passed.`

- [ ] **Step 2: Replay all patches and run validators**

Run all existing validators plus the new validator after patch replay.

- [ ] **Step 3: Build ROM and verify header**

Build `firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`, then verify title `NEXUS RED`, game code `BNRE`, and size `33554432`.

### Task 5: Commit

**Files:**
- Stage all files changed by this plan.

- [ ] **Step 1: Check cleanliness**

Run:

```bash
git diff --check
git status --short
git -C engine/pokeemerald-expansion status --short
```

- [ ] **Step 2: Commit and push**

Run:

```bash
git commit -m "Add Rock Tunnel Cave Lantern setup"
git push origin feature/first-playable-title-opening
```
