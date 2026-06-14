# Pokemon Mansion Phoenix Field Test Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deepen Pokemon Mansion into the first Phoenix pressure dungeon while preserving the classic Secret Key route to Blaine.

**Architecture:** Parent repo owns specs, validators, design data, smoke notes, and numbered engine patches. Engine edits are replayed from a clean source tree, exported as `0031-pokemon-mansion-phoenix-field-test.patch`, verified, built, then restored clean.

**Tech Stack:** pokeemerald-expansion FireRed target, map script includes, Python validators, exported patch stack.

---

### Task 1: Validator and Spec Contract

**Files:**
- Create: `tools/validate_pokemon_mansion_phoenix_field_test.py`
- Create: `docs/superpowers/specs/2026-06-14-pokemon-mansion-phoenix-field-test-design.md`

- [x] **Step 1: Write the failing validator**

Run: `python3 tools/validate_pokemon_mansion_phoenix_field_test.py`

Expected: FAIL for missing patch, design markers, WorldLink messages, rival feed, spec markers, and smoke-test entries.

- [x] **Step 2: Write the design spec**

The spec must include `Pokemon Mansion Phoenix Field Test Design`, `first Phoenix-linked battle`, `Secret Key becomes a Blaine handoff`, `Mewtwo remains unresolved`, and `does not rebalance Blaine`.

### Task 2: Parent Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Add Act 6 Mansion markers**

Add `mansion_phoenix_field_test`, `mansion_restoration_ledger`, `mansion_mewtwo_birth_warning`, and `secret_key_blaine_handoff`.

- [x] **Step 2: Add WorldLink messages**

Add `WL_KANTO_MANSION_PHOENIX_FIELD_TEST`, `WL_KANTO_RESTORATION_LEDGER`, and `WL_KANTO_SECRET_KEY_BLAINE_HANDOFF`.

- [x] **Step 3: Add rival/companion notification band**

Add `pokemon_mansion_phoenix_field_test` with Red, Brock, Ava, Blue, and Dax notifications.

- [x] **Step 4: Add smoke-test checklist entries**

Add Mansion 1F, 2F, 3F, B1F, patch, and validator checks.

### Task 3: Engine Patch

**Files:**
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonMansion_1F_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonMansion_2F_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonMansion_3F_Frlg/scripts.inc`
- Modify: `engine/pokeemerald-expansion/data/maps/PokemonMansion_B1F_Frlg/scripts.inc`
- Create: `patches/engine/0031-pokemon-mansion-phoenix-field-test.patch`

- [x] **Step 1: Replay patches through `0030` from clean source**

Run: `git -C engine/pokeemerald-expansion restore . && for patch in $(find patches/engine -name '*.patch' | sort); do git -C engine/pokeemerald-expansion apply ../../${patch}; done`

- [x] **Step 2: Rewrite 1F Ted battle text**

Keep `TRAINER_SCIENTIST_TED`, but frame him as a Phoenix field test contractor.

- [x] **Step 3: Rewrite 2F diary text**

Keep Mew discovery and naming beats, adding restoration ledger language.

- [x] **Step 4: Rewrite 3F Mewtwo birth text**

Keep Mewtwo unresolved and frame creation without restraint as the danger.

- [x] **Step 5: Rewrite B1F Secret Key and final diary text**

Connect the Secret Key to Blaine, old science, and WorldLink's next objective.

- [x] **Step 6: Export isolated patch**

Export only the touched Mansion script files to `0031-pokemon-mansion-phoenix-field-test.patch`.

### Task 4: Verification and Shipping

- [x] **Step 1: Run targeted validator**

Run: `python3 tools/validate_pokemon_mansion_phoenix_field_test.py`

Expected: `Pokemon Mansion Phoenix validation passed.`

- [x] **Step 2: Replay all patches and run full validators**

Run clean patch replay and every `tools/validate_*.py`.

- [x] **Step 3: Build and verify ROM**

Run FireRed build with `TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`, then verify header bytes read `NEXUS RED` and `BNRE`.

- [x] **Step 4: Restore engine, commit, and push**

Restore `engine/pokeemerald-expansion`, commit parent repo changes, and push the feature branch.
