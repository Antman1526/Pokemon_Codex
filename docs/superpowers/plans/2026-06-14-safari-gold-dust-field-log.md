# Safari Gold Dust Field Log Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Ava's Safari Field Log setup, Gold Dust rare-habitat scouting, and Koga status-prep framing.

**Architecture:** Keep the parent repo as source of truth for docs, design data, validators, and exported patches. Edit the replayed engine target only to generate `patches/engine/0024-safari-gold-dust-field-log.patch`, then restore it clean.

**Tech Stack:** Python validators, YAML design data, pokeemerald-expansion FRLG scripts/maps, Make/devkitARM build.

---

### Task 1: Add Failing Validator

**Files:**
- Create: `tools/validate_safari_gold_dust_field_log.py`

- [x] **Step 1: Write validator for patch, design data, WorldLink messages, rival progression, and build notes.**
- [x] **Step 2: Run `python3 tools/validate_safari_gold_dust_field_log.py` and confirm it fails before implementation.**

### Task 2: Add Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Add Safari Field Log and Gold Dust scout events to act 5.**
- [x] **Step 2: Add WorldLink messages for Safari checklist, Gold Dust scouting, and Koga status prep.**
- [x] **Step 3: Add rival/companion progression for Ava, Dax, Blue, Red, and Misty.**
- [x] **Step 4: Add build-note patch, validator, and manual smoke checklist entries.**

### Task 3: Add Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/FuchsiaCity_SafariZone_Office_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/FuchsiaCity_SafariZone_Office_Frlg/scripts.inc`
- Create: `patches/engine/0024-safari-gold-dust-field-log.patch`

- [x] **Step 1: Add Ava to Safari entrance with field-log checklist dialogue.**
- [x] **Step 2: Add Gold Dust scout to Safari office with collector/protection tension.**
- [x] **Step 3: Rewrite existing Safari entrance/office text to mention WorldLink, rare habitats, Warden route, and Koga prep.**
- [x] **Step 4: Export isolated engine diff as patch `0024`.**

### Task 4: Verify and Ship

**Files:**
- Build output: `engine/pokeemerald-expansion/pokenexusred.gba`

- [x] **Step 1: Run `python3 tools/validate_safari_gold_dust_field_log.py`.**
- [x] **Step 2: Replay all engine patches from clean source.**
- [x] **Step 3: Run the full validator suite.**
- [x] **Step 4: Build the ROM with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`.**
- [x] **Step 5: Verify ROM header title `NEXUS RED` and game code `BNRE`.**
- [x] **Step 6: Restore engine source, commit, and push.**
