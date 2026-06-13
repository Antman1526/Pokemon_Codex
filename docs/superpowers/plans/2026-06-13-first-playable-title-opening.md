# First Playable Title and Opening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the first Pokemon Nexus Red `.gba` milestone that builds from source, boots in OpenEmu, presents early Nexus Red identity, and starts the player in the Pallet bedroom intro path.

**Architecture:** Use `pokeemerald-expansion` as the engine source and build the `firered` target so the first milestone inherits FRLG maps and title-screen structure. Keep implementation incremental: first prove the toolchain, then change ROM/title identity, then modify existing FRLG Pallet scripts before adding custom systems like WorldLink and 39-starter menus. Treat custom art as a later replacement layer; the first milestone may use text/header identity and existing FRLG graphics.

**Tech Stack:** GBA C/decomp workflow, `pokeemerald-expansion`, GNU Make, devkitPro/devkitARM, `arm-none-eabi-*`, map/script `.inc` files, JSON map data, OpenEmu smoke testing on macOS.

---

## Scope Notes

This plan covers the first buildable milestone only:

- local toolchain proof,
- FireRed-target baseline build,
- Pokemon Nexus Red ROM/title identity placeholder,
- Pallet bedroom/Mom/Oak intro script direction,
- Red/Blue/Ava/Dax opening staging plan,
- verification and documentation.

This plan does not implement all 39 starters, WorldLink UI, full rival simulation, Brock, or custom title art. Those become follow-up plans after a `.gba` boot and save/load smoke test.

## File Structure

Files to modify during execution:

- `engine/pokeemerald-expansion/Makefile`  
  Build metadata surface for `TITLE`, `GAME_CODE`, `BUILD_NAME`, and target selection. Prefer command-line overrides first; edit only if a persistent project target is needed.

- `engine/pokeemerald-expansion/src/title_screen_frlg.c`  
  FRLG title-screen logic and asset references. First implementation should avoid heavy code changes unless a visible placeholder text/sprite is required.

- `engine/pokeemerald-expansion/graphics/title_screen_frlg/firered/game_title_logo.png`  
  Existing FRLG title logo asset. Do not replace in the first task unless the build toolchain is already proven.

- `engine/pokeemerald-expansion/data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc`  
  Start-room script surface for Antman's bedroom intro.

- `engine/pokeemerald-expansion/data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc`  
  Mom dialogue and post-starter healing behavior.

- `engine/pokeemerald-expansion/data/maps/PalletTown_Frlg/scripts.inc`  
  Red/Blue outdoor staging near Pallet grass line.

- `engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`  
  Oak, Blue, starter scene, and first battle staging.

- `build_notes/ENGINE_PROOF_STATUS.md`  
  Update after each build attempt with exact command/result.

- `build_notes/MAC_OPENEMU_BUILD_NOTES.md`  
  Update after the first successful `.gba` and OpenEmu smoke test.

Files to create during execution:

- `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`  
  Human-readable smoke-test record for first boot, title identity, new game start, save, reload, and first Pallet scene.

- `patches/engine/0001-pallet-bedroom-mom-intro.patch`  
  Project-owned patch for the first Pallet bedroom and Mom text changes. Keep engine customizations in patch files until the project has a writable engine fork; do not commit parent gitlinks pointing at local-only submodule commits.

- `patches/engine/0002-pallet-red-blue-scene.patch`  
  Project-owned patch for the first outdoor Red/Blue Pallet scene.

- `patches/engine/0003-oak-lab-nexus-intro.patch`  
  Project-owned patch for Oak's Nexus Red lab framing.

Engine patch rule:

- The `engine/pokeemerald-expansion` submodule tracks upstream engine source.
- Local engine source edits may be applied in the worktree to build and test.
- Committed project changes must be stored as patch files under `patches/engine/`.
- Do not commit a submodule pointer to a local-only engine commit.
- Before final merge, the submodule should be clean or intentionally documented as patched for local build testing.

---

## Task 1: Install and Verify GBA Toolchain

**Files:**
- Modify: `build_notes/ENGINE_PROOF_STATUS.md`

- [ ] **Step 1: Check current missing tools**

Run:

```bash
command -v arm-none-eabi-gcc || true
command -v arm-none-eabi-as || true
command -v dkp-pacman || true
```

Expected before install:

```text
No paths printed for arm-none-eabi-gcc, arm-none-eabi-as, or dkp-pacman.
```

- [ ] **Step 2: Install devkitPro/devkitARM**

Use the official devkitPro macOS installer flow. After installation, open a new terminal session or source the shell profile that devkitPro updates.

Expected environment:

```bash
echo "$DEVKITPRO"
echo "$DEVKITARM"
```

Expected result:

```text
/opt/devkitpro
/opt/devkitpro/devkitARM
```

- [ ] **Step 3: Verify tools resolve**

Run:

```bash
command -v arm-none-eabi-gcc
command -v arm-none-eabi-as
command -v dkp-pacman
```

Expected after install:

```text
/opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc
/opt/devkitpro/devkitARM/bin/arm-none-eabi-as
/opt/devkitpro/tools/bin/dkp-pacman
```

- [ ] **Step 4: Update engine proof notes**

Edit `build_notes/ENGINE_PROOF_STATUS.md` so the "Confirmed missing" section becomes:

```markdown
Confirmed installed:

- arm-none-eabi-gcc
- arm-none-eabi-as
- dkp-pacman
```

- [ ] **Step 5: Commit**

Run:

```bash
git add build_notes/ENGINE_PROOF_STATUS.md
git commit -m "Document devkitARM toolchain readiness"
```

Expected:

```text
[main <hash>] Document devkitARM toolchain readiness
```

---

## Task 2: Build Clean FireRed Baseline

**Files:**
- Modify: `build_notes/ENGINE_PROOF_STATUS.md`
- Create: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Clean ignored build output**

Run:

```bash
git -C engine/pokeemerald-expansion clean -fdX
```

Expected:

```text
Removing build/
```

If no build artifacts exist, the command may print nothing.

- [ ] **Step 2: Build the FireRed target**

Run:

```bash
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered
```

Expected:

```text
tools/gbafix/gbafix pokefirered.gba ...
```

The exact build log is long. The required output file is:

```text
/Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokefirered.gba
```

- [ ] **Step 3: Verify ROM file exists**

Run:

```bash
ls -lh /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokefirered.gba
```

Expected:

```text
-rw-r--r-- ... pokefirered.gba
```

- [ ] **Step 4: Create smoke-test note**

Create `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md` with:

```markdown
# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
make -j"$(sysctl -n hw.ncpu)" firered
```

Output ROM:

```text
engine/pokeemerald-expansion/pokefirered.gba
```

## Smoke Test Checklist

- [ ] ROM opens in OpenEmu.
- [ ] Title screen appears.
- [ ] New game starts.
- [ ] Player reaches Pallet bedroom.
- [ ] Save works.
- [ ] Reload works.

## Notes

Baseline FireRed-target build before Pokemon Nexus Red content edits.
```

- [ ] **Step 5: Commit**

Run:

```bash
git add build_notes/ENGINE_PROOF_STATUS.md build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Record FireRed baseline build smoke test"
```

Expected:

```text
[main <hash>] Record FireRed baseline build smoke test
```

---

## Task 3: Apply First ROM Header Identity

**Files:**
- Modify: `build_notes/MAC_OPENEMU_BUILD_NOTES.md`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Build with temporary Nexus Red ROM header**

Run:

```bash
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Expected output file:

```text
/Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokenexusred.gba
```

Reasoning:

- `TITLE="NEXUS RED"` fits the GBA 12-character title header.
- `GAME_CODE=BNRE` gives the local build a project-specific game code.
- `BUILD_NAME=nexusred` produces `pokenexusred.gba`.

- [ ] **Step 2: Verify ROM file exists**

Run:

```bash
ls -lh /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokenexusred.gba
```

Expected:

```text
-rw-r--r-- ... pokenexusred.gba
```

- [ ] **Step 3: Record header command**

Append this to `build_notes/MAC_OPENEMU_BUILD_NOTES.md`:

```markdown
## 10. First Nexus Red Header Build

Use this command for the first Pokemon Nexus Red identity build:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Expected local ROM:

```text
engine/pokeemerald-expansion/pokenexusred.gba
```

This changes ROM header identity and output filename before custom title art replacement.
```

- [ ] **Step 4: Update smoke-test checklist**

In `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`, change the build section output ROM to:

```text
engine/pokeemerald-expansion/pokenexusred.gba
```

Add this checklist item:

```markdown
- [ ] ROM appears locally as `pokenexusred.gba`.
```

- [ ] **Step 5: Commit**

Run:

```bash
git add build_notes/MAC_OPENEMU_BUILD_NOTES.md build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Document first Nexus Red header build"
```

Expected:

```text
[main <hash>] Document first Nexus Red header build
```

---

## Task 4: Replace Pallet Bedroom and Mom Intro Text

**Files:**
- Temporarily modify for build: `engine/pokeemerald-expansion/data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc`
- Temporarily modify for build: `engine/pokeemerald-expansion/data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc`
- Create: `patches/engine/0001-pallet-bedroom-mom-intro.patch`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Update bedroom TV/NES text**

In `engine/pokeemerald-expansion/data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc`, replace:

```asm
PalletTown_PlayersHouse_2F_Text_PlayedWithNES::
	.string "{PLAYER} played with the NES.\p"
	.string "…Okay!\n"
	.string "It's time to go!$"
```

with:

```asm
PalletTown_PlayersHouse_2F_Text_PlayedWithNES::
	.string "{PLAYER} checked the news.\p"
	.string "Strange weather is moving across\n"
	.string "KANTO before sunrise.\p"
	.string "PROF. OAK says unusual POKéMON\n"
	.string "tracks were found near PALLET.$"
```

- [ ] **Step 2: Update bedroom sign/help text**

In the same file, replace:

```asm
PalletTown_PlayersHouse_2F_Text_PressLRForHelp::
	.string "It's a posted notice…\p"
	.string "If you're confused, ask for HELP!\n"
	.string "Press the L or R Button!$"
```

with:

```asm
PalletTown_PlayersHouse_2F_Text_PressLRForHelp::
	.string "A note from MOM is on the desk.\p"
	.string "PROF. OAK called early.\n"
	.string "He asked for you by name.$"
```

- [ ] **Step 3: Update Mom pre-lab dialogue**

In `engine/pokeemerald-expansion/data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc`, replace:

```asm
PalletTown_PlayersHouse_1F_Text_AllBoysLeaveOakLookingForYou::
	.string "MOM: …Right.\n"
	.string "All boys leave home someday.\l"
	.string "It said so on TV.\p"
	.string "Oh, yes. PROF. OAK, next door, was\n"
	.string "looking for you.$"
```

with:

```asm
PalletTown_PlayersHouse_1F_Text_AllBoysLeaveOakLookingForYou::
	.string "MOM: PROF. OAK called before\n"
	.string "sunrise. He sounded worried.\p"
	.string "They say strange POKéMON tracks\n"
	.string "appeared near ROUTE 1.\p"
	.string "PALLET has seen great trainers\n"
	.string "leave before, {PLAYER}.\p"
	.string "But this morning feels different.$"
```

- [ ] **Step 4: Update Mom alternate gender dialogue**

In the same file, replace:

```asm
PalletTown_PlayersHouse_1F_Text_AllGirlsLeaveOakLookingForYou::
	.string "MOM: …Right.\n"
	.string "All girls dream of traveling.\l"
	.string "It said so on TV.\p"
	.string "Oh, yes. PROF. OAK, next door, was\n"
	.string "looking for you.$"
```

with:

```asm
PalletTown_PlayersHouse_1F_Text_AllGirlsLeaveOakLookingForYou::
	.string "MOM: PROF. OAK called before\n"
	.string "sunrise. He sounded worried.\p"
	.string "They say strange POKéMON tracks\n"
	.string "appeared near ROUTE 1.\p"
	.string "PALLET has seen great trainers\n"
	.string "leave before, {PLAYER}.\p"
	.string "But this morning feels different.$"
```

- [ ] **Step 5: Generate project patch**

Run from the parent repo root:

```bash
mkdir -p patches/engine
git -C engine/pokeemerald-expansion diff -- \
  data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc \
  data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc \
  > patches/engine/0001-pallet-bedroom-mom-intro.patch
test -s patches/engine/0001-pallet-bedroom-mom-intro.patch
```

Expected:

```text
patches/engine/0001-pallet-bedroom-mom-intro.patch exists and is non-empty.
```

- [ ] **Step 6: Build**

If the patch is not already applied to the submodule source, apply it from the parent repo root:

```bash
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
```

Run:

```bash
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Expected:

```text
pokenexusred.gba
```

- [ ] **Step 7: Record patch application in smoke-test note**

Append this to `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`:

```markdown
## Engine Patches To Apply Before Build

- `patches/engine/0001-pallet-bedroom-mom-intro.patch` - Pallet bedroom news and Mom intro text.
```

- [ ] **Step 8: Restore submodule source after build**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- \
  data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc \
  data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc
```

Expected:

```text
git -C engine/pokeemerald-expansion status --short
```

shows only ignored build artifacts, not modified source files.

- [ ] **Step 9: Commit**

Run:

```bash
git add patches/engine/0001-pallet-bedroom-mom-intro.patch build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Add Pallet bedroom and Mom intro text"
```

Expected:

```text
[main <hash>] Add Pallet bedroom and Mom intro text
```

---

## Task 5: Add First Pallet Outdoor Red and Blue Scene

**Files:**
- Temporarily modify for build: `engine/pokeemerald-expansion/data/maps/PalletTown_Frlg/scripts.inc`
- Inspect: `engine/pokeemerald-expansion/data/maps/PalletTown_Frlg/map.json`
- Create: `patches/engine/0002-pallet-red-blue-scene.patch`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Inspect Pallet object IDs**

Run:

```bash
sed -n '1,220p' /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/data/maps/PalletTown_Frlg/map.json
sed -n '1,220p' /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/data/maps/PalletTown_Frlg/scripts.inc
```

Expected:

```text
The map JSON lists existing object events and the script file lists labels for Pallet NPCs.
```

- [ ] **Step 2: Choose safe first implementation**

Use existing Pallet NPC/object slots for the first scene if available. If no safe Red/Blue object slot exists, implement the first pass as dialogue on the existing Oak route-block scene rather than adding new object events.

Script text for first pass:

```asm
PalletTown_Frlg_Text_RedTracks::
	.string "RED: Morning, {PLAYER}.\p"
	.string "I was hoping you would see this\n"
	.string "before the adults cleaned it up.\p"
	.string "These tracks are wrong for PALLET,\n"
	.string "but I do not think it is danger yet.\p"
	.string "Stay close today. If OAK is right,\n"
	.string "your road starts bigger than mine did.$"

PalletTown_Frlg_Text_BluePressure::
	.string "BLUE: So RED noticed you now?\p"
	.string "Great. Come on, {PLAYER}.\n"
	.string "OAK is waiting at the LAB.$"
```

- [ ] **Step 3: Generate project patch**

Run from the parent repo root:

```bash
mkdir -p patches/engine
git -C engine/pokeemerald-expansion diff -- \
  data/maps/PalletTown_Frlg/scripts.inc \
  > patches/engine/0002-pallet-red-blue-scene.patch
test -s patches/engine/0002-pallet-red-blue-scene.patch
```

Expected:

```text
patches/engine/0002-pallet-red-blue-scene.patch exists and is non-empty.
```

- [ ] **Step 4: Build**

Apply project patches in order from the parent repo root if not already applied:

```bash
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0002-pallet-red-blue-scene.patch
```

Run:

```bash
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Expected:

```text
pokenexusred.gba
```

- [ ] **Step 5: Manual OpenEmu check**

Open:

```text
/Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokenexusred.gba
```

Expected:

```text
Player can leave the house and see first Pallet outdoor story text without a crash.
```

- [ ] **Step 6: Record patch in smoke-test note**

Add this line under `## Engine Patches To Apply Before Build` in `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`:

```markdown
- `patches/engine/0002-pallet-red-blue-scene.patch` - first outdoor Red/Blue Pallet scene.
```

- [ ] **Step 7: Restore submodule source after build**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- data/maps/PalletTown_Frlg/scripts.inc
```

Expected:

```text
git -C engine/pokeemerald-expansion status --short
```

shows only ignored build artifacts, not modified source files.

- [ ] **Step 8: Commit**

Run:

```bash
git add patches/engine/0002-pallet-red-blue-scene.patch build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Add first Red and Blue Pallet scene"
```

Expected:

```text
[main <hash>] Add first Red and Blue Pallet scene
```

---

## Task 6: Reframe Oak Lab Intro Text

**Files:**
- Temporarily modify for build: `engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`
- Create: `patches/engine/0003-oak-lab-nexus-intro.patch`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Find Oak starter-scene dialogue labels**

Run:

```bash
rg -n "ChooseStarter|starter|POKéMON|RIVAL|OAK|Bulbasaur|Charmander|Squirtle|Pokedex|POKéDEX" /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc
```

Expected:

```text
Labels for Oak starter selection and rival battle dialogue are printed.
```

- [ ] **Step 2: Replace Oak's first explanation with Nexus Red framing**

Use this text for Oak's first starter-scene explanation:

```asm
	.string "OAK: KANTO's first routes are\n"
	.string "showing impossible migration.\p"
	.string "These POKéMON should not all be\n"
	.string "near PALLET.\p"
	.string "The LEAGUE calls it a survey.\n"
	.string "I call it a warning.\p"
	.string "{PLAYER}, I want you in the\n"
	.string "WORLD POKéDEX INITIATIVE.$"
```

- [ ] **Step 3: Replace Blue pressure line**

Use this text for Blue's pre-battle pressure:

```asm
	.string "BLUE: A world tour, huh?\p"
	.string "Fine by me. Bigger road,\n"
	.string "bigger stage.\p"
	.string "And I still beat you first.$"
```

- [ ] **Step 4: Generate project patch**

Run from the parent repo root:

```bash
mkdir -p patches/engine
git -C engine/pokeemerald-expansion diff -- \
  data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc \
  > patches/engine/0003-oak-lab-nexus-intro.patch
test -s patches/engine/0003-oak-lab-nexus-intro.patch
```

Expected:

```text
patches/engine/0003-oak-lab-nexus-intro.patch exists and is non-empty.
```

- [ ] **Step 5: Build**

Apply project patches in order from the parent repo root if not already applied:

```bash
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0002-pallet-red-blue-scene.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0003-oak-lab-nexus-intro.patch
```

Run:

```bash
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Expected:

```text
pokenexusred.gba
```

- [ ] **Step 6: Record patch in smoke-test note**

Add this line under `## Engine Patches To Apply Before Build` in `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`:

```markdown
- `patches/engine/0003-oak-lab-nexus-intro.patch` - Oak lab Nexus Red framing.
```

- [ ] **Step 7: Restore submodule source after build**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc
```

Expected:

```text
git -C engine/pokeemerald-expansion status --short
```

shows only ignored build artifacts, not modified source files.

- [ ] **Step 8: Commit**

Run:

```bash
git add patches/engine/0003-oak-lab-nexus-intro.patch build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Reframe Oak lab intro for Nexus Red"
```

Expected:

```text
[main <hash>] Reframe Oak lab intro for Nexus Red
```

---

## Task 7: Update Smoke Test and Push

**Files:**
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`
- Modify: `build_notes/MAC_OPENEMU_BUILD_NOTES.md`

- [ ] **Step 1: Complete smoke-test results**

Update `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md` checklist to reflect actual OpenEmu results:

```markdown
## Smoke Test Checklist

- [x] ROM opens in OpenEmu.
- [x] Title screen appears.
- [x] New game starts.
- [x] Player reaches Pallet bedroom.
- [x] Bedroom news text appears.
- [x] Mom intro text appears.
- [x] Player can reach Oak's Lab.
- [x] Save works.
- [x] Reload works.
```

If a checklist item fails, leave it unchecked and add a concrete note under `## Notes`.

- [ ] **Step 2: Validate design data**

Run:

```bash
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
python3 tools/validate_design_data.py
```

Expected:

```text
Design data validation passed.
```

- [ ] **Step 3: Check git status**

Run:

```bash
git status --short --branch
```

Expected:

```text
## main...origin/main
```

or:

```text
## main...origin/main [ahead 1]
```

- [ ] **Step 4: Push**

Run:

```bash
git push
```

Expected:

```text
main -> main
```

---

## Self-Review

Spec coverage:

- Custom title concept is covered by Task 3 and deferred asset replacement notes.
- Bedroom/Mom/Oak intro is covered by Tasks 4 and 6.
- Red and Blue opening presence is covered by Task 5.
- Engine proof and OpenEmu target are covered by Tasks 1, 2, and 7.
- WorldLink pause behavior and mandatory Brock/Misty recurrence are not implemented here because they are outside the first bootable opening milestone; they remain documented in the approved spec and need their own implementation plans.

Placeholder scan:

- This plan contains no `TBD`, `TODO`, or unspecified implementation steps.
- Discovery steps are explicit commands with expected outputs.

Risk notes:

- If `make firered` fails after devkitARM installation, stop and update `build_notes/ENGINE_PROOF_STATUS.md` with the exact compiler/linker error before changing game content.
- If Pallet outdoor object edits are too risky for the first pass, attach the Red/Blue text to an existing safe Pallet event and commit that small version first.
- Do not commit `.gba`, `.sav`, `.srm`, `.ips`, or `.bps` files.
