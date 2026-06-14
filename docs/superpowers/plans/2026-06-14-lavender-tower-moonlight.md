# Lavender Tower Moonlight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Pokemon Tower Moonlight reveal milestone as patch `0018`.

**Architecture:** Keep the parent repo as the source of truth. Write a validator first, update design data, replay patches `0001` through `0017`, edit the engine, export only the incremental `0018` patch, restore the engine clean, replay all patches, then build and verify the ROM header.

**Tech Stack:** pokeemerald-expansion FRLG target, project-owned engine patch files, Python validators, YAML design data, OpenEmu-compatible `.gba` build.

---

## Files

- Create: `tools/validate_lavender_tower_moonlight.py`
- Create: `patches/engine/0018-lavender-tower-moonlight.patch`
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`
- Engine source while patch is being generated:
  - `engine/pokeemerald-expansion/data/maps/PokemonTower_2F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/PokemonTower_2F_Frlg/map.json`
  - `engine/pokeemerald-expansion/data/maps/PokemonTower_5F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/PokemonTower_5F_Frlg/map.json`
  - `engine/pokeemerald-expansion/data/maps/PokemonTower_6F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/PokemonTower_7F_Frlg/scripts.inc`
  - `engine/pokeemerald-expansion/data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc`

## Task 1: Validator Red

- [ ] **Step 1: Create validator**

Create `tools/validate_lavender_tower_moonlight.py` that checks:

- `patches/engine/0018-lavender-tower-moonlight.patch` exists.
- Patch text references `PokemonTower_2F_Frlg`, `PokemonTower_5F_Frlg`, `PokemonTower_6F_Frlg`, `PokemonTower_7F_Frlg`, and `LavenderTown_VolunteerPokemonHouse_Frlg`.
- Patch text includes `PokemonTower_2F_EventScript_RedTowerCheck`, `OBJ_EVENT_GFX_RED`, `Team Moonlight`, `Moonlight Veil`, `dream static`, `WorldLink`, `Cubone's mother`, `Silph Scope`, `Poke Flute`, and `Rocket`.
- Design data includes `pokemon_tower_blue_rival_pressure`, `red_pokemon_tower_after_blue_check`, `team_moonlight_name_reveal`, `marowak_dream_static_layer`, and `fuji_rocket_moonlight_warning`.
- WorldLink message data includes `WL_KANTO_POKEMON_TOWER_BLUE_RACE`, `WL_KANTO_TEAM_MOONLIGHT_REVEALED`, and `WL_KANTO_FUJI_DREAM_STATIC`.
- Rival progression includes `pokemon_tower_moonlight_reveal`.
- Build notes include `0018-lavender-tower-moonlight.patch` and `validate_lavender_tower_moonlight.py`.

- [ ] **Step 2: Run validator to verify failure**

Run:

```bash
python3 tools/validate_lavender_tower_moonlight.py
```

Expected: failure because the design data and patch are not implemented yet.

## Task 2: Design Data

- [ ] **Step 1: Update Kanto chapter**

Add Tower events under `act_4_rock_tunnel_celadon_lavender`:

- `pokemon_tower_blue_rival_pressure`
- `red_pokemon_tower_after_blue_check`
- `team_moonlight_name_reveal`
- `marowak_dream_static_layer`
- `fuji_rocket_moonlight_warning`

- [ ] **Step 2: Add WorldLink messages**

Add messages for Blue's Tower race pressure, Team Moonlight revealed, and Fuji's dream-static warning.

- [ ] **Step 3: Add rival progression band**

Add `pokemon_tower_moonlight_reveal` with Red, Blue, Ava, Dax, Misty, Brock, and Lyra updates.

## Task 3: Engine Patch

- [ ] **Step 1: Replay patches through 0017**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
for patch in $(ls patches/engine/*.patch | sort); do
  git -C engine/pokeemerald-expansion apply ../../${patch}
done
```

- [ ] **Step 2: Modify Tower 2F**

Add Red object and `PokemonTower_2F_EventScript_RedTowerCheck`. Red gives pre-Blue warning and post-Blue support based on `VAR_MAP_SCENE_POKEMON_TOWER_2F`.

- [ ] **Step 3: Modify Tower 5F**

Add Moonlight Veil object and dialogue in the purified zone area.

- [ ] **Step 4: Modify Tower 6F**

Add dream-static language to Marowak's ghost scene without removing the original Cubone's mother reveal.

- [ ] **Step 5: Modify Tower 7F and Fuji home**

Rewrite Rocket/Fuji/Poke Flute text to separate Rocket from Moonlight and preserve the classic Poke Flute reward.

- [ ] **Step 6: Export incremental patch**

Reverse patches `0017` through `0001`, write the remaining diff to `patches/engine/0018-lavender-tower-moonlight.patch`, then restore the engine.

## Task 4: Verification

- [ ] **Step 1: Run new validator**

Run:

```bash
python3 tools/validate_lavender_tower_moonlight.py
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

- [ ] **Step 3: Run project validators**

Run all validator scripts under `tools/validate_*.py`.

- [ ] **Step 4: Build ROM**

Run:

```bash
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -C engine/pokeemerald-expansion -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Expected: `engine/pokeemerald-expansion/pokenexusred.gba` builds.

- [ ] **Step 5: Verify ROM header**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
rom = Path('engine/pokeemerald-expansion/pokenexusred.gba')
data = rom.read_bytes()
print('path:', rom.resolve())
print('size:', rom.stat().st_size)
print('title:', data[0xA0:0xAC].decode('ascii', errors='replace').rstrip('\0'))
print('game_code:', data[0xAC:0xB0].decode('ascii', errors='replace'))
PY
```

Expected title `NEXUS RED` and game code `BNRE`.

## Task 5: Commit

- [ ] **Step 1: Restore engine clean after verification**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
git status --short
```

Expected: parent repo shows only intended parent-level files; engine submodule has no working-tree diff.

- [ ] **Step 2: Commit and push**

Run:

```bash
git add docs/superpowers/specs/2026-06-14-lavender-tower-moonlight-design.md docs/superpowers/plans/2026-06-14-lavender-tower-moonlight.md tools/validate_lavender_tower_moonlight.py data_design/kanto_chapter.yaml data_design/kanto_worldlink_messages.yaml data_design/rival_progression_kanto.yaml build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md patches/engine/0018-lavender-tower-moonlight.patch
git commit -m "Add Lavender Tower Moonlight setup"
git push
```
