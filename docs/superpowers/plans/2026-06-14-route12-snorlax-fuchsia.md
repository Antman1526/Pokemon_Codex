# Route 12 Snorlax Fuchsia Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Route 12 Snorlax Poke Flute payoff and first Fuchsia arrival hook.

**Architecture:** Parent repo stores the spec, plan, design data, validator, and exported engine patch. Engine source is edited only as a replay target, then restored clean after `patches/engine/0023-route12-snorlax-fuchsia.patch` is generated.

**Tech Stack:** Python validators, YAML design data, pokeemerald-expansion FRLG scripts/maps, Make/devkitARM build.

---

### Task 1: Add Failing Validator

**Files:**
- Create: `tools/validate_route12_snorlax_fuchsia.py`

- [x] **Step 1: Write validator for missing patch, design markers, WorldLink markers, rival markers, and build notes.**
- [x] **Step 2: Run `python3 tools/validate_route12_snorlax_fuchsia.py` and confirm it fails because implementation is not present.**

### Task 2: Add Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Add act 5 route-opening events before Silph Co.**
- [x] **Step 2: Add WorldLink messages for Route 12 Snorlax, Fuchsia path open, and deferred Saffron pressure.**
- [x] **Step 3: Add rival/companion progression band for Red, Misty, Dax, Blue, and Ava.**
- [x] **Step 4: Add build note entries, validator command, and manual smoke checklist items.**

### Task 3: Add Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/Route12_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/Route12_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/FuchsiaCity_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/FuchsiaCity_Frlg/scripts.inc`
- Create: `patches/engine/0023-route12-snorlax-fuchsia.patch`

- [x] **Step 1: Add Red and Misty support NPCs near Route 12 Snorlax.**
- [x] **Step 2: Extend Snorlax Poke Flute text and post-battle route guidance.**
- [x] **Step 3: Add Dax in Fuchsia as the first rival arrival hook.**
- [x] **Step 4: Rewrite Fuchsia city/Safari/Gym text with Safari/Koga/Gold Dust/Saffron pressure.**
- [x] **Step 5: Export the isolated engine diff as patch `0023`.**

### Task 4: Verify and Ship

**Files:**
- Build output: `engine/pokeemerald-expansion/pokenexusred.gba`

- [x] **Step 1: Run `python3 tools/validate_route12_snorlax_fuchsia.py`.**
- [x] **Step 2: Replay all engine patches from clean source.**
- [x] **Step 3: Run the full validator suite.**
- [x] **Step 4: Build the ROM with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.**
- [x] **Step 5: Verify ROM header title `NEXUS RED` and game code `BNRE`.**
- [ ] **Step 6: Restore engine source, commit, and push.**
