# Nexus Identity, WorldLink, and Starter Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the next Pokemon Nexus Red `.gba` milestone: stronger title identity documentation, first Pokédex-style WorldLink alert, Oak's 27 official regional starter selection, and Route 1-3 catchability for the remaining early Pokemon with badge-scaled levels.

**Architecture:** Keep engine edits as project-owned patch files under `patches/engine/` and restore the `pokeemerald-expansion` submodule after each build. Use FRLG script menus for the first 27-starter Oak selection instead of expanding the graphical three-Pokéball chooser. Validate progression with a project Python checker that reads the engine wild-encounter JSON and confirms early species coverage and level caps.

**Tech Stack:** `pokeemerald-expansion` FireRed target, FRLG event scripts, script multichoice tables, `src/data/wild_encounters.json`, `src/data/trainers_frlg.party`, devkitARM, OpenEmu, Python validation scripts.

---

## Scope And Order

This plan implements the next playable milestone after the first OpenEmu-confirmed build. It does not attempt full custom pixel-art title insertion, the full WorldLink feed, the 12 special starters in Oak's starter menu, or all nine-region content.

Patch order after the existing first-playable patches:

1. `patches/engine/0004-worldlink-route1-alert.patch`
2. `patches/engine/0005-oak-27-starter-menu.patch`
3. `patches/engine/0006-route1-3-badge-scaled-encounters.patch`
4. `patches/engine/0007-route3-anomaly-wild-battles.patch`

Existing required patches:

1. `patches/engine/0001-pallet-bedroom-mom-intro.patch`
2. `patches/engine/0002-pallet-red-blue-scene.patch`
3. `patches/engine/0003-oak-lab-nexus-intro.patch`

## File Structure

Project files:

- Create: `assets/title_screen/NEXUS_RED_TITLE_SCREEN_BRIEF.md`  
  Records the approved warm-adventure title-screen concept and GBA constraints.

- Create: `data_design/kanto_progression_scaling.yaml`  
  Records early level caps, wild level ranges, trainer expectations, and Brock balance target.

- Create: `tools/validate_nexus_milestone.py`  
  Validates the 27 Oak starter species list, Route 1-3 catchability coverage, rare-power placement, and route level ceilings.

- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`  
  Adds new patch list and smoke-test checklist for this milestone.

- Modify: `build_notes/MAC_OPENEMU_BUILD_NOTES.md`  
  Adds the next milestone build command and title identity status.

Temporary engine files used to generate patches:

- Modify: `engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`  
  Adds WorldLink alert and 27-starter Oak menu script.

- Modify: `engine/pokeemerald-expansion/include/constants/script_menu.h`  
  Adds Nexus starter multichoice ids.

- Modify: `engine/pokeemerald-expansion/src/data/script_menu.h`  
  Adds Nexus starter region and trio menu entries.

- Modify: `engine/pokeemerald-expansion/src/data/wild_encounters.json`  
  Replaces Route 1-3 FireRed and LeafGreen land tables with badge-scaled Nexus Red distributions.

- Modify: `engine/pokeemerald-expansion/data/maps/Route3_Frlg/scripts.inc`  
  Adds three scripted anomaly wild battles for Dratini, Larvitar, and Kubfu.

- Modify: `engine/pokeemerald-expansion/data/maps/Route3_Frlg/map.json`  
  Adds three route anomaly overworld objects that launch the scripted wild battles.

## Badge-Scaled Progression Targets

Use these caps for this milestone:

```yaml
early_kanto_progression:
  pallet_lab:
    starter_level: 5
    blue_lab_level: 5
  route_1:
    wild_levels: [2, 5]
    rare_slot_max_level: 5
  route_2:
    wild_levels: [3, 6]
    rare_slot_max_level: 6
  route_3:
    wild_levels: [5, 8]
    rare_slot_max_level: 8
    anomaly_static_level: 7
  brock:
    default_cap: 14
    target_feel: "mainline-hard, not Radical Red"
```

---

## Task 1: Add Title Identity Brief And Progression Data

**Files:**
- Create: `assets/title_screen/NEXUS_RED_TITLE_SCREEN_BRIEF.md`
- Create: `data_design/kanto_progression_scaling.yaml`
- Modify: `build_notes/MAC_OPENEMU_BUILD_NOTES.md`

- [x] **Step 1: Create title asset directory**

Run:

```bash
mkdir -p assets/title_screen
```

Expected:

```text
assets/title_screen exists.
```

- [x] **Step 2: Create title-screen brief**

Create `assets/title_screen/NEXUS_RED_TITLE_SCREEN_BRIEF.md` with:

```markdown
# Pokemon Nexus Red - Title Screen Brief

Date: 2026-06-13

## Approved Concept

Red, Antman, and Blue stand with their backs to the camera at sunrise, facing a glowing region-map Nexus over Pallet Town. The image should feel warm, adventurous, and classic rather than dark.

## Required Logo Text

```text
POKEMON NEXUS RED
```

## First GBA Implementation Rule

Do not block the playable ROM on final title art. The first graphics milestone may preserve FireRed title animation while the ROM header and build notes identify the game as Nexus Red. Full title art replacement should use the FRLG title asset path:

```text
engine/pokeemerald-expansion/graphics/title_screen_frlg/firered/
```

## Art Direction

- Foreground: Red, Antman, and Blue facing away.
- Midground: Pallet coastline or Route 1 ridge.
- Sky: sunrise gold and soft red.
- Nexus: glowing ring made from nine region-map silhouettes.
- Mood: hopeful first day of a huge journey.

## GBA Constraints To Respect

- Work inside GBA tile and palette limits.
- Keep high-contrast logo readability.
- Prefer a staged replacement: concept image, indexed-color mockup, then compressed engine asset.
- Verify in OpenEmu after every asset insertion.
```

- [x] **Step 3: Create progression scaling data**

Create `data_design/kanto_progression_scaling.yaml` with:

```yaml
# Badge-scaled early Kanto progression for Pokemon Nexus Red.

early_kanto_progression:
  design_goal: mainline_hard_with_options
  default_difficulty: classic_plus
  route_1:
    wild_level_min: 2
    wild_level_max: 5
    purpose: "first team texture, safe catches, no power spike"
    notable_species:
      - Bulbasaur
      - Charmander
      - Squirtle
      - Pikachu
      - Eevee
      - Ralts
  route_2:
    wild_level_min: 3
    wild_level_max: 6
    purpose: "Johto/Hoenn/Sinnoh expansion and first trickier catches"
    notable_species:
      - Chikorita
      - Cyndaquil
      - Totodile
      - Treecko
      - Torchic
      - Mudkip
      - Turtwig
      - Chimchar
      - Piplup
      - Abra
      - Gastly
      - Shroomish
  route_3:
    wild_level_min: 5
    wild_level_max: 8
    anomaly_static_level: 7
    purpose: "pre-Brock global starter promise, rare catches remain controlled"
    notable_species:
      - Snivy
      - Tepig
      - Oshawott
      - Chespin
      - Fennekin
      - Froakie
      - Rowlet
      - Litten
      - Popplio
      - Grookey
      - Scorbunny
      - Sobble
      - Sprigatito
      - Fuecoco
      - Quaxly
      - Sandile
      - Rockruff
      - Staryu
      - Dratini
      - Larvitar
      - Kubfu
  brock:
    level_cap: 14
    tuning: "mainline-hard, not punishing"
    rule: "Brock should respect expanded player options without requiring grinding."
  blue_lab:
    level: 5
    rule: "Blue counters by broad starter type, not by harsh rare-pick punishment."
```

- [x] **Step 4: Update macOS build notes**

Append this section to `build_notes/MAC_OPENEMU_BUILD_NOTES.md`:

```markdown
## 12. Nexus Identity And Starter Expansion Milestone

The next milestone keeps the ROM OpenEmu-first and uses project patches after the first-playable patches:

```text
0004-worldlink-route1-alert.patch
0005-oak-27-starter-menu.patch
0006-route1-3-badge-scaled-encounters.patch
0007-route3-anomaly-wild-battles.patch
```

Title art direction is tracked in:

```text
assets/title_screen/NEXUS_RED_TITLE_SCREEN_BRIEF.md
```

Badge-scaled progression data is tracked in:

```text
data_design/kanto_progression_scaling.yaml
```
```

- [x] **Step 5: Validate and commit**

Run:

```bash
python3 tools/validate_design_data.py
git add assets/title_screen/NEXUS_RED_TITLE_SCREEN_BRIEF.md data_design/kanto_progression_scaling.yaml build_notes/MAC_OPENEMU_BUILD_NOTES.md
git commit -m "Document Nexus title identity and early scaling"
```

Expected:

```text
Design data validation passed.
```

---

## Task 2: Add Nexus Milestone Validator

**Files:**
- Create: `tools/validate_nexus_milestone.py`

- [x] **Step 1: Create validator**

Create `tools/validate_nexus_milestone.py`:

```python
#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WILD_JSON = ROOT / "engine" / "pokeemerald-expansion" / "src" / "data" / "wild_encounters.json"

OFFICIAL_STARTERS = {
    "SPECIES_BULBASAUR", "SPECIES_CHARMANDER", "SPECIES_SQUIRTLE",
    "SPECIES_CHIKORITA", "SPECIES_CYNDAQUIL", "SPECIES_TOTODILE",
    "SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP",
    "SPECIES_TURTWIG", "SPECIES_CHIMCHAR", "SPECIES_PIPLUP",
    "SPECIES_SNIVY", "SPECIES_TEPIG", "SPECIES_OSHAWOTT",
    "SPECIES_CHESPIN", "SPECIES_FENNEKIN", "SPECIES_FROAKIE",
    "SPECIES_ROWLET", "SPECIES_LITTEN", "SPECIES_POPPLIO",
    "SPECIES_GROOKEY", "SPECIES_SCORBUNNY", "SPECIES_SOBBLE",
    "SPECIES_SPRIGATITO", "SPECIES_FUECOCO", "SPECIES_QUAXLY",
}

SPECIAL_EARLY = {
    "SPECIES_EEVEE", "SPECIES_PIKACHU", "SPECIES_DRATINI",
    "SPECIES_ABRA", "SPECIES_GASTLY", "SPECIES_LARVITAR",
    "SPECIES_SANDILE", "SPECIES_KUBFU", "SPECIES_STARYU",
    "SPECIES_SHROOMISH", "SPECIES_ROCKRUFF", "SPECIES_RALTS",
}

ROUTE_LEVEL_CAPS = {
    "MAP_ROUTE1": 5,
    "MAP_ROUTE2": 6,
    "MAP_ROUTE3": 8,
}

STATIC_ANOMALIES = {
    "SPECIES_DRATINI": 7,
    "SPECIES_LARVITAR": 7,
    "SPECIES_KUBFU": 7,
}

def iter_route_land_mons():
    data = json.loads(WILD_JSON.read_text())
    for group in data["wild_encounter_groups"]:
        if group.get("label") != "gWildMonHeaders":
            continue
        for encounter in group["encounters"]:
            route = encounter.get("map")
            if route not in ROUTE_LEVEL_CAPS:
                continue
            land = encounter.get("land_mons")
            if not land:
                continue
            yield route, encounter.get("base_label"), land["mons"]

def main():
    seen = set(STATIC_ANOMALIES)
    errors = []

    for route, label, mons in iter_route_land_mons():
        if len(mons) != 12:
            errors.append(f"{label} must have exactly 12 land slots, found {len(mons)}")
        cap = ROUTE_LEVEL_CAPS[route]
        for mon in mons:
            species = mon["species"]
            seen.add(species)
            if mon["min_level"] > mon["max_level"]:
                errors.append(f"{label} {species} has min level above max level")
            if mon["max_level"] > cap:
                errors.append(f"{label} {species} exceeds {route} cap {cap}")

    required = OFFICIAL_STARTERS | SPECIAL_EARLY
    missing = sorted(required - seen)
    if missing:
        errors.append("Missing early catchability: " + ", ".join(missing))

    if errors:
        print("Nexus milestone validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Nexus milestone validation passed.")

if __name__ == "__main__":
    main()
```

- [x] **Step 2: Run validator and verify it fails before route data patch**

Run:

```bash
python3 tools/validate_nexus_milestone.py
```

Expected before Task 6:

```text
Nexus milestone validation failed:
```

- [x] **Step 3: Commit failing validator**

Run:

```bash
git add tools/validate_nexus_milestone.py
git commit -m "Add Nexus milestone progression validator"
```

Expected:

```text
[feature/first-playable-title-opening <hash>] Add Nexus milestone progression validator
```

---

## Task 3: Add Pokédex-Style WorldLink Alert

**Files:**
- Temporarily modify: `engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`
- Create: `patches/engine/0004-worldlink-route1-alert.patch`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Apply existing engine patches**

Run from repo root:

```bash
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0002-pallet-red-blue-scene.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0003-oak-lab-nexus-intro.patch
```

Expected: no output.

- [x] **Step 2: Insert WorldLink alert after Blue's lab exit setup**

In `engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`, find `PalletTown_ProfessorOaksLab_EventScript_RivalExitAfterBattle` and add this call before the script releases control:

```asm
	call PalletTown_ProfessorOaksLab_EventScript_WorldLinkFirstAlert
```

Add this new script/text block near the other lab text:

```asm
PalletTown_ProfessorOaksLab_EventScript_WorldLinkFirstAlert::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	msgbox PalletTown_ProfessorOaksLab_Text_WorldLinkFirstAlert
	call EventScript_RestorePrevTextColor
	return

PalletTown_ProfessorOaksLab_Text_WorldLinkFirstAlert::
	.string "WORLDLINK ALERT\p"
	.string "RED logged fresh tracks\n"
	.string "on ROUTE 1.\p"
	.string "BLUE marked himself\n"
	.string "\"first to VIRIDIAN.\"$"
```

- [x] **Step 3: Build**

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

- [x] **Step 4: Generate patch**

Run from repo root:

```bash
git -C engine/pokeemerald-expansion diff -- data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc > patches/engine/0004-worldlink-route1-alert.patch
test -s patches/engine/0004-worldlink-route1-alert.patch
```

Expected: patch file exists and is non-empty.

- [x] **Step 5: Restore engine source**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc
```

Expected:

```bash
git -C engine/pokeemerald-expansion status --short
```

prints no modified tracked files.

- [x] **Step 6: Update smoke-test note**

Add this line under engine patches in `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`:

```markdown
- `patches/engine/0004-worldlink-route1-alert.patch` - first Pokédex-style WorldLink alert after Blue's lab battle.
```

- [x] **Step 7: Commit**

Run:

```bash
git add patches/engine/0004-worldlink-route1-alert.patch build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Add first WorldLink route alert"
```

Expected:

```text
[feature/first-playable-title-opening <hash>] Add first WorldLink route alert
```

---

## Task 4: Add Nexus Starter Multichoice Menus

**Files:**
- Temporarily modify: `engine/pokeemerald-expansion/include/constants/script_menu.h`
- Temporarily modify: `engine/pokeemerald-expansion/src/data/script_menu.h`

- [x] **Step 1: Add multichoice ids**

In `engine/pokeemerald-expansion/include/constants/script_menu.h`, append these enum entries before the enum terminator:

```c
    MULTI_NEXUS_STARTER_REGION,
    MULTI_NEXUS_STARTER_KANTO,
    MULTI_NEXUS_STARTER_JOHTO,
    MULTI_NEXUS_STARTER_HOENN,
    MULTI_NEXUS_STARTER_SINNOH,
    MULTI_NEXUS_STARTER_UNOVA,
    MULTI_NEXUS_STARTER_KALOS,
    MULTI_NEXUS_STARTER_ALOLA,
    MULTI_NEXUS_STARTER_GALAR,
    MULTI_NEXUS_STARTER_PALDEA,
```

- [x] **Step 2: Add starter menu actions**

In `engine/pokeemerald-expansion/src/data/script_menu.h`, add these menu lists before `sMultichoiceLists`:

```c
static const struct MenuAction sMultichoiceList_NexusStarterRegion[] =
{
    { COMPOUND_STRING("KANTO"), NULL },
    { COMPOUND_STRING("JOHTO"), NULL },
    { COMPOUND_STRING("HOENN"), NULL },
    { COMPOUND_STRING("SINNOH"), NULL },
    { COMPOUND_STRING("UNOVA"), NULL },
    { COMPOUND_STRING("KALOS"), NULL },
    { COMPOUND_STRING("ALOLA"), NULL },
    { COMPOUND_STRING("GALAR"), NULL },
    { COMPOUND_STRING("PALDEA"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterKanto[] =
{
    { COMPOUND_STRING("BULBASAUR"), NULL },
    { COMPOUND_STRING("CHARMANDER"), NULL },
    { COMPOUND_STRING("SQUIRTLE"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterJohto[] =
{
    { COMPOUND_STRING("CHIKORITA"), NULL },
    { COMPOUND_STRING("CYNDAQUIL"), NULL },
    { COMPOUND_STRING("TOTODILE"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterHoenn[] =
{
    { COMPOUND_STRING("TREECKO"), NULL },
    { COMPOUND_STRING("TORCHIC"), NULL },
    { COMPOUND_STRING("MUDKIP"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterSinnoh[] =
{
    { COMPOUND_STRING("TURTWIG"), NULL },
    { COMPOUND_STRING("CHIMCHAR"), NULL },
    { COMPOUND_STRING("PIPLUP"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterUnova[] =
{
    { COMPOUND_STRING("SNIVY"), NULL },
    { COMPOUND_STRING("TEPIG"), NULL },
    { COMPOUND_STRING("OSHAWOTT"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterKalos[] =
{
    { COMPOUND_STRING("CHESPIN"), NULL },
    { COMPOUND_STRING("FENNEKIN"), NULL },
    { COMPOUND_STRING("FROAKIE"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterAlola[] =
{
    { COMPOUND_STRING("ROWLET"), NULL },
    { COMPOUND_STRING("LITTEN"), NULL },
    { COMPOUND_STRING("POPPLIO"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterGalar[] =
{
    { COMPOUND_STRING("GROOKEY"), NULL },
    { COMPOUND_STRING("SCORBUNNY"), NULL },
    { COMPOUND_STRING("SOBBLE"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};

static const struct MenuAction sMultichoiceList_NexusStarterPaldea[] =
{
    { COMPOUND_STRING("SPRIGATITO"), NULL },
    { COMPOUND_STRING("FUECOCO"), NULL },
    { COMPOUND_STRING("QUAXLY"), NULL },
    { COMPOUND_STRING("BACK"), NULL },
};
```

- [x] **Step 3: Register menu lists**

In `sMultichoiceLists[]`, add:

```c
    [MULTI_NEXUS_STARTER_REGION] = MULTICHOICE(sMultichoiceList_NexusStarterRegion),
    [MULTI_NEXUS_STARTER_KANTO]  = MULTICHOICE(sMultichoiceList_NexusStarterKanto),
    [MULTI_NEXUS_STARTER_JOHTO]  = MULTICHOICE(sMultichoiceList_NexusStarterJohto),
    [MULTI_NEXUS_STARTER_HOENN]  = MULTICHOICE(sMultichoiceList_NexusStarterHoenn),
    [MULTI_NEXUS_STARTER_SINNOH] = MULTICHOICE(sMultichoiceList_NexusStarterSinnoh),
    [MULTI_NEXUS_STARTER_UNOVA]  = MULTICHOICE(sMultichoiceList_NexusStarterUnova),
    [MULTI_NEXUS_STARTER_KALOS]  = MULTICHOICE(sMultichoiceList_NexusStarterKalos),
    [MULTI_NEXUS_STARTER_ALOLA]  = MULTICHOICE(sMultichoiceList_NexusStarterAlola),
    [MULTI_NEXUS_STARTER_GALAR]  = MULTICHOICE(sMultichoiceList_NexusStarterGalar),
    [MULTI_NEXUS_STARTER_PALDEA] = MULTICHOICE(sMultichoiceList_NexusStarterPaldea),
```

- [x] **Step 4: Build to verify menu table compiles**

Apply patches `0001` through `0004`, then run:

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

Do not commit yet. Task 5 completes the Oak script before patch generation.

---

## Task 5: Replace Oak's Three Balls With 27-Starter Script Flow

**Files:**
- Temporarily modify: `engine/pokeemerald-expansion/data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc`
- Create: `patches/engine/0005-oak-27-starter-menu.patch`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Route all three starter balls to the Nexus menu**

Replace the bodies of `PalletTown_ProfessorOaksLab_EventScript_BulbasaurBall`, `PalletTown_ProfessorOaksLab_EventScript_SquirtleBall`, and `PalletTown_ProfessorOaksLab_EventScript_CharmanderBall` with:

```asm
	lock
	faceplayer
	goto_if_ge VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 3, PalletTown_ProfessorOaksLab_EventScript_LastPokeBall
	goto_if_eq VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 2, PalletTown_ProfessorOaksLab_EventScript_NexusStarterMenu
	msgbox PalletTown_ProfessorOaksLab_Text_ThoseArePokeBalls
	release
	end
```

- [x] **Step 2: Replace confirmation with generic species confirmation**

Replace `PalletTown_ProfessorOaksLab_EventScript_ConfirmStarterChoice` and the three species-specific confirmation labels with:

```asm
PalletTown_ProfessorOaksLab_EventScript_ConfirmStarterChoice::
	applymovement LOCALID_OAKS_LAB_PROF_OAK, Common_Movement_FaceRight
	waitmovement 0
	showmonpic PLAYER_STARTER_SPECIES, 10, 3
	textcolor NPC_TEXT_COLOR_MALE
	bufferspeciesname STR_VAR_1, PLAYER_STARTER_SPECIES
	msgbox PalletTown_ProfessorOaksLab_Text_NexusConfirmStarter, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_ChoseStarter
	goto_if_eq VAR_RESULT, NO, PalletTown_ProfessorOaksLab_EventScript_DeclinedStarter
	end

PalletTown_ProfessorOaksLab_Text_NexusConfirmStarter::
	.string "OAK: Begin your journey\n"
	.string "with {STR_VAR_1}?$"
```

- [x] **Step 3: Add region menu**

Add:

```asm
PalletTown_ProfessorOaksLab_EventScript_NexusStarterMenu::
	msgbox PalletTown_ProfessorOaksLab_Text_NexusStarterIntro
	multichoice 0, 0, MULTI_NEXUS_STARTER_REGION, FALSE
	switch VAR_RESULT
	case 0, PalletTown_ProfessorOaksLab_EventScript_NexusStarterKanto
	case 1, PalletTown_ProfessorOaksLab_EventScript_NexusStarterJohto
	case 2, PalletTown_ProfessorOaksLab_EventScript_NexusStarterHoenn
	case 3, PalletTown_ProfessorOaksLab_EventScript_NexusStarterSinnoh
	case 4, PalletTown_ProfessorOaksLab_EventScript_NexusStarterUnova
	case 5, PalletTown_ProfessorOaksLab_EventScript_NexusStarterKalos
	case 6, PalletTown_ProfessorOaksLab_EventScript_NexusStarterAlola
	case 7, PalletTown_ProfessorOaksLab_EventScript_NexusStarterGalar
	case 8, PalletTown_ProfessorOaksLab_EventScript_NexusStarterPaldea
	case 9, PalletTown_ProfessorOaksLab_EventScript_DeclinedStarter
	case MULTI_B_PRESSED, PalletTown_ProfessorOaksLab_EventScript_DeclinedStarter
	end

PalletTown_ProfessorOaksLab_Text_NexusStarterIntro::
	.string "OAK: These terminals hold\n"
	.string "regional starter records.\p"
	.string "Choose the region whose partner\n"
	.string "calls to you.$"
```

- [x] **Step 4: Add starter trio menus**

Add one menu label per region. Use this Kanto pattern and repeat with the species mappings below:

```asm
PalletTown_ProfessorOaksLab_EventScript_NexusStarterKanto::
	multichoice 0, 0, MULTI_NEXUS_STARTER_KANTO, FALSE
	switch VAR_RESULT
	case 0, PalletTown_ProfessorOaksLab_EventScript_SetStarterBulbasaur
	case 1, PalletTown_ProfessorOaksLab_EventScript_SetStarterCharmander
	case 2, PalletTown_ProfessorOaksLab_EventScript_SetStarterSquirtle
	case 3, PalletTown_ProfessorOaksLab_EventScript_NexusStarterMenu
	case MULTI_B_PRESSED, PalletTown_ProfessorOaksLab_EventScript_NexusStarterMenu
	end
```

Species set labels needed:

```text
SetStarterBulbasaur / Charmander / Squirtle
SetStarterChikorita / Cyndaquil / Totodile
SetStarterTreecko / Torchic / Mudkip
SetStarterTurtwig / Chimchar / Piplup
SetStarterSnivy / Tepig / Oshawott
SetStarterChespin / Fennekin / Froakie
SetStarterRowlet / Litten / Popplio
SetStarterGrookey / Scorbunny / Sobble
SetStarterSprigatito / Fuecoco / Quaxly
```

- [x] **Step 5: Add starter setter labels**

Use broad type mapping so Blue's first battle stays stable:

```asm
PalletTown_ProfessorOaksLab_EventScript_SetNexusGrassStarter::
	setvar PLAYER_STARTER_NUM, 0
	setvar RIVAL_STARTER_SPECIES, SPECIES_CHARMANDER
	setvar RIVAL_STARTER_ID, LOCALID_CHARMANDER_BALL
	goto PalletTown_ProfessorOaksLab_EventScript_ConfirmStarterChoice

PalletTown_ProfessorOaksLab_EventScript_SetNexusFireStarter::
	setvar PLAYER_STARTER_NUM, 2
	setvar RIVAL_STARTER_SPECIES, SPECIES_SQUIRTLE
	setvar RIVAL_STARTER_ID, LOCALID_SQUIRTLE_BALL
	goto PalletTown_ProfessorOaksLab_EventScript_ConfirmStarterChoice

PalletTown_ProfessorOaksLab_EventScript_SetNexusWaterStarter::
	setvar PLAYER_STARTER_NUM, 1
	setvar RIVAL_STARTER_SPECIES, SPECIES_BULBASAUR
	setvar RIVAL_STARTER_ID, LOCALID_BULBASAUR_BALL
	goto PalletTown_ProfessorOaksLab_EventScript_ConfirmStarterChoice
```

Each species setter sets `PLAYER_STARTER_SPECIES` and jumps to the matching broad type setter:

```asm
PalletTown_ProfessorOaksLab_EventScript_SetStarterBulbasaur::
	setvar PLAYER_STARTER_SPECIES, SPECIES_BULBASAUR
	goto PalletTown_ProfessorOaksLab_EventScript_SetNexusGrassStarter
```

Repeat for all 27 official starters.

- [x] **Step 6: Build and generate patch**

Run the Nexus Red build command. Then generate:

```bash
git -C engine/pokeemerald-expansion diff -- \
  include/constants/script_menu.h \
  src/data/script_menu.h \
  data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc \
  > patches/engine/0005-oak-27-starter-menu.patch
test -s patches/engine/0005-oak-27-starter-menu.patch
```

- [x] **Step 7: Restore engine source**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- \
  include/constants/script_menu.h \
  src/data/script_menu.h \
  data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc
```

- [x] **Step 8: Update smoke-test note and commit**

Add:

```markdown
- `patches/engine/0005-oak-27-starter-menu.patch` - Oak's 27 official regional starter menu.
```

Run:

```bash
git add patches/engine/0005-oak-27-starter-menu.patch build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Add Oak regional starter menu"
```

---

## Task 6: Add Badge-Scaled Route 1-3 Wild Tables

**Files:**
- Temporarily modify: `engine/pokeemerald-expansion/src/data/wild_encounters.json`
- Create: `patches/engine/0006-route1-3-badge-scaled-encounters.patch`

- [x] **Step 1: Replace Route 1 FireRed and LeafGreen land tables**

For both `sRoute1_FireRed` and `sRoute1_LeafGreen`, use these 12 slots:

```json
[
  {"min_level": 2, "max_level": 3, "species": "SPECIES_PIDGEY"},
  {"min_level": 2, "max_level": 3, "species": "SPECIES_RATTATA"},
  {"min_level": 3, "max_level": 3, "species": "SPECIES_BULBASAUR"},
  {"min_level": 3, "max_level": 3, "species": "SPECIES_CHARMANDER"},
  {"min_level": 3, "max_level": 3, "species": "SPECIES_SQUIRTLE"},
  {"min_level": 3, "max_level": 4, "species": "SPECIES_PIKACHU"},
  {"min_level": 3, "max_level": 4, "species": "SPECIES_EEVEE"},
  {"min_level": 3, "max_level": 4, "species": "SPECIES_RALTS"},
  {"min_level": 4, "max_level": 4, "species": "SPECIES_BULBASAUR"},
  {"min_level": 4, "max_level": 4, "species": "SPECIES_CHARMANDER"},
  {"min_level": 5, "max_level": 5, "species": "SPECIES_SQUIRTLE"},
  {"min_level": 4, "max_level": 5, "species": "SPECIES_EEVEE"}
]
```

- [x] **Step 2: Replace Route 2 FireRed and LeafGreen land tables**

For both `sRoute2_FireRed` and `sRoute2_LeafGreen`, use:

```json
[
  {"min_level": 3, "max_level": 4, "species": "SPECIES_CHIKORITA"},
  {"min_level": 3, "max_level": 4, "species": "SPECIES_CYNDAQUIL"},
  {"min_level": 3, "max_level": 4, "species": "SPECIES_TOTODILE"},
  {"min_level": 4, "max_level": 5, "species": "SPECIES_TREECKO"},
  {"min_level": 4, "max_level": 5, "species": "SPECIES_TORCHIC"},
  {"min_level": 4, "max_level": 5, "species": "SPECIES_MUDKIP"},
  {"min_level": 5, "max_level": 5, "species": "SPECIES_TURTWIG"},
  {"min_level": 5, "max_level": 5, "species": "SPECIES_CHIMCHAR"},
  {"min_level": 5, "max_level": 5, "species": "SPECIES_PIPLUP"},
  {"min_level": 4, "max_level": 6, "species": "SPECIES_ABRA"},
  {"min_level": 5, "max_level": 6, "species": "SPECIES_GASTLY"},
  {"min_level": 4, "max_level": 6, "species": "SPECIES_SHROOMISH"}
]
```

- [x] **Step 3: Replace Route 3 FireRed and LeafGreen land tables**

For both `sRoute3_FireRed` and `sRoute3_LeafGreen`, use:

```json
[
  {"min_level": 5, "max_level": 6, "species": "SPECIES_SNIVY"},
  {"min_level": 5, "max_level": 6, "species": "SPECIES_TEPIG"},
  {"min_level": 5, "max_level": 6, "species": "SPECIES_OSHAWOTT"},
  {"min_level": 6, "max_level": 7, "species": "SPECIES_CHESPIN"},
  {"min_level": 6, "max_level": 7, "species": "SPECIES_FENNEKIN"},
  {"min_level": 6, "max_level": 7, "species": "SPECIES_FROAKIE"},
  {"min_level": 7, "max_level": 7, "species": "SPECIES_ROWLET"},
  {"min_level": 7, "max_level": 7, "species": "SPECIES_LITTEN"},
  {"min_level": 7, "max_level": 7, "species": "SPECIES_POPPLIO"},
  {"min_level": 7, "max_level": 8, "species": "SPECIES_SANDILE"},
  {"min_level": 7, "max_level": 8, "species": "SPECIES_ROCKRUFF"},
  {"min_level": 6, "max_level": 8, "species": "SPECIES_STARYU"}
]
```

Route 3 scripted anomalies in Task 7 cover Dratini, Larvitar, and Kubfu. Galar and Paldea starters require Task 7 static anomaly events as well because the 36 total land slots cannot hold all 39 requested early species.

- [x] **Step 4: Run validator and expect remaining missing species**

Run:

```bash
python3 tools/validate_nexus_milestone.py
```

Expected before Task 7:

```text
Nexus milestone validation failed:
```

The missing list should include Galar/Paldea starters plus Dratini, Larvitar, and Kubfu.

- [x] **Step 5: Build and generate patch**

Run the Nexus Red build command, then:

```bash
git -C engine/pokeemerald-expansion diff -- src/data/wild_encounters.json > patches/engine/0006-route1-3-badge-scaled-encounters.patch
test -s patches/engine/0006-route1-3-badge-scaled-encounters.patch
```

- [x] **Step 6: Restore source and commit**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- src/data/wild_encounters.json
git add patches/engine/0006-route1-3-badge-scaled-encounters.patch
git commit -m "Add badge-scaled Route 1-3 encounters"
```

---

## Task 7: Add Route 3 Anomaly Wild Battles For Remaining Early Species

**Files:**
- Temporarily modify: `engine/pokeemerald-expansion/data/maps/Route3_Frlg/scripts.inc`
- Temporarily modify: `engine/pokeemerald-expansion/data/maps/Route3_Frlg/map.json`
- Temporarily modify: `tools/validate_nexus_milestone.py`
- Create: `patches/engine/0007-route3-anomaly-wild-battles.patch`

- [x] **Step 1: Add static anomaly species to validator**

Update `STATIC_ANOMALIES` in `tools/validate_nexus_milestone.py` to include the Galar and Paldea starters:

```python
STATIC_ANOMALIES = {
    "SPECIES_GROOKEY": 7,
    "SPECIES_SCORBUNNY": 7,
    "SPECIES_SOBBLE": 7,
    "SPECIES_SPRIGATITO": 7,
    "SPECIES_FUECOCO": 7,
    "SPECIES_QUAXLY": 7,
    "SPECIES_DRATINI": 7,
    "SPECIES_LARVITAR": 7,
    "SPECIES_KUBFU": 7,
}
```

- [x] **Step 2: Add Route 3 anomaly scripts**

Add to `Route3_Frlg/scripts.inc`:

```asm
Route3_EventScript_NexusAnomalyGalar::
	lock
	msgbox Route3_Text_NexusAnomalyGalar
	setwildbattle SPECIES_GROOKEY, 7
	dowildbattle
	setwildbattle SPECIES_SCORBUNNY, 7
	dowildbattle
	setwildbattle SPECIES_SOBBLE, 7
	dowildbattle
	release
	end

Route3_EventScript_NexusAnomalyPaldea::
	lock
	msgbox Route3_Text_NexusAnomalyPaldea
	setwildbattle SPECIES_SPRIGATITO, 7
	dowildbattle
	setwildbattle SPECIES_FUECOCO, 7
	dowildbattle
	setwildbattle SPECIES_QUAXLY, 7
	dowildbattle
	release
	end

Route3_EventScript_NexusAnomalyRare::
	lock
	msgbox Route3_Text_NexusAnomalyRare
	setwildbattle SPECIES_DRATINI, 7
	dowildbattle
	setwildbattle SPECIES_LARVITAR, 7
	dowildbattle
	setwildbattle SPECIES_KUBFU, 7
	dowildbattle
	release
	end

Route3_Text_NexusAnomalyGalar::
	.string "The POKéDEX pings softly.\p"
	.string "WORLDLINK: Three GALAR signals\n"
	.string "are moving through the grass.$"

Route3_Text_NexusAnomalyPaldea::
	.string "The POKéDEX screen glows warm.\p"
	.string "WORLDLINK: PALDEA readings\n"
	.string "are clustering nearby.$"

Route3_Text_NexusAnomalyRare::
	.string "The POKéDEX gives a sharp alert.\p"
	.string "WORLDLINK: Rare migration\n"
	.string "pressure detected.$"
```

- [x] **Step 3: Add Route 3 anomaly objects**

Add three object events to `Route3_Frlg/map.json`:

```json
{
  "type": "object",
  "graphics_id": "OBJ_EVENT_GFX_POKE_BALL",
  "x": 54,
  "y": 8,
  "elevation": 3,
  "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
  "movement_range_x": 0,
  "movement_range_y": 0,
  "trainer_type": "TRAINER_TYPE_NONE",
  "trainer_sight_or_berry_tree_id": "0",
  "script": "Route3_EventScript_NexusAnomalyGalar",
  "flag": "0"
}
```

Repeat with:

```text
x=58 y=8 script=Route3_EventScript_NexusAnomalyPaldea
x=62 y=8 script=Route3_EventScript_NexusAnomalyRare
```

- [x] **Step 4: Run validator**

Apply patches `0001` through `0007`, then run:

```bash
python3 tools/validate_nexus_milestone.py
```

Expected:

```text
Nexus milestone validation passed.
```

- [x] **Step 5: Build and generate patch**

Run the Nexus Red build command, then:

```bash
git -C engine/pokeemerald-expansion diff -- \
  data/maps/Route3_Frlg/scripts.inc \
  data/maps/Route3_Frlg/map.json \
  > patches/engine/0007-route3-anomaly-wild-battles.patch
test -s patches/engine/0007-route3-anomaly-wild-battles.patch
```

- [x] **Step 6: Restore source and commit**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- data/maps/Route3_Frlg/scripts.inc data/maps/Route3_Frlg/map.json
git add patches/engine/0007-route3-anomaly-wild-battles.patch tools/validate_nexus_milestone.py
git commit -m "Add Route 3 Nexus anomaly encounters"
```

---

## Task 8: Final Build, Smoke Test, And Push

**Files:**
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [x] **Step 1: Apply all milestone patches in order**

Run:

```bash
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0002-pallet-red-blue-scene.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0003-oak-lab-nexus-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0004-worldlink-route1-alert.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0005-oak-27-starter-menu.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0006-route1-3-badge-scaled-encounters.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0007-route3-anomaly-wild-battles.patch
```

- [x] **Step 2: Run validations**

Run:

```bash
python3 tools/validate_design_data.py
python3 tools/validate_nexus_milestone.py
```

Expected:

```text
Design data validation passed.
Nexus milestone validation passed.
```

- [x] **Step 3: Build ROM**

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

- [x] **Step 4: Verify ROM header**

Run:

```bash
file engine/pokeemerald-expansion/pokenexusred.gba
```

Expected:

```text
Game Boy Advance ROM image: "NEXUS RED" (BNRE01, Rev.00)
```

- [ ] **Step 5: OpenEmu smoke test**

OpenEmu launch command completed on 2026-06-13. Manual in-emulator gameplay verification is still pending.

Open:

```bash
open -a /Applications/OpenEmu.app /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokenexusred.gba
```

Verify:

```markdown
- [ ] ROM opens in OpenEmu.
- [ ] Title screen appears.
- [ ] New game starts.
- [ ] Player reaches Pallet bedroom.
- [ ] Oak offers regional starter menus.
- [ ] Selected starter is level 5.
- [ ] Blue's lab battle completes.
- [ ] First WorldLink alert appears.
- [ ] Route 1 wild encounters work.
- [ ] Route 2 wild encounters work.
- [ ] Route 3 wild encounters work.
- [ ] Route 3 anomaly encounters work.
- [ ] Save works.
- [ ] Reload works.
```

- [x] **Step 6: Restore submodule source**

Run:

```bash
git -C engine/pokeemerald-expansion restore -- \
  include/constants/script_menu.h \
  src/data/script_menu.h \
  data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc \
  src/data/wild_encounters.json \
  data/maps/Route3_Frlg/scripts.inc \
  data/maps/Route3_Frlg/map.json
```

Expected:

```bash
git -C engine/pokeemerald-expansion status --short
```

prints no modified tracked source files.

- [x] **Step 7: Update smoke-test note**

Update `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md` with actual Task 8 results. If a runtime check fails, leave it unchecked and add the exact failure under notes.

- [x] **Step 8: Commit and push**

Run:

```bash
git add build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md
git commit -m "Record Nexus starter milestone smoke test"
git push
```

Expected:

```text
feature/first-playable-title-opening -> feature/first-playable-title-opening
```

---

## Self-Review

Spec coverage:

- Title direction is covered by Task 1.
- WorldLink prototype is covered by Task 3.
- Oak's 27 official starters are covered by Tasks 4 and 5.
- Route 1-3 catchability and progression scaling are covered by Tasks 2, 6, and 7.
- OpenEmu `.gba` verification is covered by Task 8.

Scope risks:

- The first starter menu is script-driven, not the final polished terminal UI.
- Route 3 anomaly encounters are scripted wild battles because three normal land tables have only 36 slots and the requirement needs 39 early species.
- Brock remains mainline-hard for this milestone; deeper trainer/gym rebalance should become its own battle-design milestone after the expanded encounter pool is playable.

Question to carry into implementation:

- Should Route 3 anomaly encounters be repeatable until caught, or one-time challenge encounters? The best default for long-game retention is repeatable until caught, then weekly rematch in a future system.
