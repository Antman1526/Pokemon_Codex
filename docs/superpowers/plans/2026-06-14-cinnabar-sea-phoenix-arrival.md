# Cinnabar Sea Phoenix Arrival Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first Act 6 Cinnabar arrival slice with Tide Rider route guidance, Red's restraint scene, Team Phoenix first-contact, and a Pokemon Mansion Mewtwo echo.

**Architecture:** Parent repo owns validators, specs, design data, smoke notes, and exported engine patches. Engine edits are replayed from clean patches, exported as `0030-cinnabar-sea-phoenix-arrival.patch`, verified, then restored clean.

**Tech Stack:** pokeemerald-expansion FireRed target, map JSON/script includes, Python validators, exported numbered patch files.

---

### Task 1: Validator and Spec Contract

**Files:**
- Create: `tools/validate_cinnabar_sea_phoenix_arrival.py`
- Create: `docs/superpowers/specs/2026-06-14-cinnabar-sea-phoenix-arrival-design.md`

- [x] **Step 1: Write the failing validator**

Run: `python3 tools/validate_cinnabar_sea_phoenix_arrival.py`

Expected: FAIL for missing patch, Kanto design markers, WorldLink messages, rival band, spec markers, and smoke-test entries.

- [x] **Step 2: Write the design spec**

The spec must include `Cinnabar Sea and Phoenix Arrival Design`, `WorldLink remains Kanto-locked`, `Red's restraint scene`, `Team Phoenix appears through lab research`, and `Pokemon Mansion carries the Mewtwo echo`.

### Task 2: Parent Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Add Act 6 event markers**

Add `route19_tide_rider_handoff`, `cinnabar_arrival_old_fire`, `red_cinnabar_restraint_scene`, `phoenix_lab_first_contact`, and `pokemon_mansion_mewtwo_phoenix_echo` to `act_6_cinnabar_viridian`.

- [x] **Step 2: Add WorldLink messages**

Add `WL_KANTO_TIDE_RIDER_SEA_ROUTE`, `WL_KANTO_CINNABAR_OLD_FIRE`, `WL_KANTO_PHOENIX_FIRST_CONTACT`, and `WL_KANTO_MANSION_MEWTWO_ECHO`.

- [x] **Step 3: Add rival/companion notification band**

Add `cinnabar_sea_phoenix_arrival` with Red, Misty, Brock, Blue, Ava, and Dax events.

- [x] **Step 4: Add smoke-test checklist entries**

Add Route 19 Red Tide Rider, Cinnabar Red restraint, Cinnabar Lab Phoenix first-contact, Pokemon Mansion Mewtwo Phoenix echo, and patch/validator entries.

### Task 3: Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/Route19_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/Route19_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/CinnabarIsland_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/CinnabarIsland_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/CinnabarIsland_PokemonLab_ResearchRoom_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/CinnabarIsland_PokemonLab_ResearchRoom_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonMansion_1F_Frlg/map.json`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonMansion_1F_Frlg/scripts.inc`
- Create: `patches/engine/0030-cinnabar-sea-phoenix-arrival.patch`

- [x] **Step 1: Replay existing patches from clean source**

Run: `git -C engine/pokeemerald-expansion restore . && for patch in $(find patches/engine -name '*.patch' | sort); do git -C engine/pokeemerald-expansion apply ../../${patch}; done`

- [x] **Step 2: Add Route 19 Tide Rider scene**

Add Red near the water with `Route19_EventScript_RedSeaRoute` and a Tide Rider sign/scene explaining sea-route travel after Saffron.

- [x] **Step 3: Add Cinnabar Red restraint scene**

Add Red to Cinnabar Island with `CinnabarIsland_EventScript_RedCinnabarRestraint`, warning that old fire and old science require restraint.

- [x] **Step 4: Add Phoenix researcher first-contact**

Add a lab researcher with `CinnabarIsland_PokemonLab_ResearchRoom_EventScript_PhoenixResearcher` describing restoration matrices and Phoenix's controlled-rebirth philosophy.

- [x] **Step 5: Add Pokemon Mansion Mewtwo echo**

Add `PokemonMansion_1F_EventScript_PhoenixMewtwoEcho` to a sign or inspectable object on 1F.

- [x] **Step 6: Export isolated patch**

Export only the touched engine files to `patches/engine/0030-cinnabar-sea-phoenix-arrival.patch`.

### Task 4: Verification and Shipping

- [x] **Step 1: Run targeted validator**

Run: `python3 tools/validate_cinnabar_sea_phoenix_arrival.py`

Expected: `Cinnabar sea Phoenix validation passed.`

- [x] **Step 2: Replay all patches and run full validators**

Run clean patch replay and every `tools/validate_*.py`.

- [x] **Step 3: Build and verify ROM**

Run the FireRed build with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`, then verify header bytes read `NEXUS RED` and `BNRE`.

- [x] **Step 4: Restore engine, commit, and push**

Restore `engine/pokeemerald-expansion`, commit parent repo changes, and push the feature branch.
