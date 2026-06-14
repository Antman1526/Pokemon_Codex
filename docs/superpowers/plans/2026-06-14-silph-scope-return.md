# Silph Scope Return Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Lavender Tower Silph Scope return payoff with Red support, Marowak clarity, Fuji route unlock guidance, WorldLink messages, and validation.

**Architecture:** Keep project-owned source of truth in parent repo docs/data/validators and export engine changes as `patches/engine/0022-silph-scope-return.patch`. Engine source remains a replay target, not the committed source.

**Tech Stack:** Python validators, YAML design data, pokeemerald-expansion FRLG scripts/maps, Make/devkitARM build.

---

### Task 1: Add Failing Validator

**Files:**
- Create: `tools/validate_silph_scope_return.py`

- [x] **Step 1: Write validator for missing patch, design markers, WorldLink markers, rival markers, and build notes.**
- [x] **Step 2: Run `python3 tools/validate_silph_scope_return.py` and confirm it fails because implementation is not present.**

### Task 2: Add Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Add act 4 return events after `silph_scope_worldlink_return`.**
- [x] **Step 2: Add WorldLink messages for Marowak, Poke Flute, and the Saffron/Fuchsia branch.**
- [x] **Step 3: Add rival/companion progression band for the Lavender return.**
- [x] **Step 4: Add build note placeholders for patch and validator.**

### Task 3: Add Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonTower_6F_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonTower_6F_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonTower_7F_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc`
- Create: `patches/engine/0022-silph-scope-return.patch`

- [x] **Step 1: Add Red to Pokemon Tower 6F with `PokemonTower_6F_EventScript_RedMarowakSupport`.**
- [x] **Step 2: Extend Marowak event text to include Silph Scope, Red support, and Team Moonlight grief framing.**
- [x] **Step 3: Rewrite Fuji/rocket payoff text to point toward Poke Flute, Snorlax, Fuchsia, and Saffron.**
- [x] **Step 4: Export the engine diff into `0022-silph-scope-return.patch` and restore engine source.**

### Task 4: Verify and Ship

**Files:**
- Build output: `engine/pokeemerald-expansion/pokenexusred.gba`

- [x] **Step 1: Run `python3 tools/validate_silph_scope_return.py` and confirm it passes.**
- [x] **Step 2: Replay all engine patches from clean source.**
- [x] **Step 3: Run the full validator suite.**
- [x] **Step 4: Build with `make -C engine/pokeemerald-expansion ... BUILD_NAME=nexusred`.**
- [x] **Step 5: Verify ROM header title `NEXUS RED` and game code `BNRE`.**
- [ ] **Step 6: Restore engine source, commit, and push.**
