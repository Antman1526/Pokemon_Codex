# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

Apply project-owned engine patches from the parent repo root before building:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0002-pallet-red-blue-scene.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0003-oak-lab-nexus-intro.patch
```

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Output ROM:

```text
engine/pokeemerald-expansion/pokenexusred.gba
```

ROM file verification:

```text
/Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokenexusred.gba
```

Verification performed:

```text
File exists and is 32M. Header reads "NEXUS RED" (BNRE01, Rev.00).
```

## Smoke Test Checklist

- [x] ROM appears locally as `pokenexusred.gba`.
- [x] ROM opens in OpenEmu.
- [x] Title screen appears.
- [x] New game starts.
- [x] Player reaches Pallet bedroom.
- [x] Bedroom news text appears.
- [x] Mom intro text appears.
- [x] Player can reach Oak's Lab.
- [x] Save works.
- [x] Reload works.

## Notes

- 2026-06-13 10:18 CDT: Codex built `pokenexusred.gba` from the three project engine patches.
- 2026-06-13 10:20-10:29 CDT: Codex opened the ROM in OpenEmu, verified the title screen, and observed the ROM advancing into the intro/title flow. Automated keyboard input was inconsistent in this desktop session.
- 2026-06-13 10:39 CDT: Antman manually confirmed the playthrough works. Checklist items beyond title-screen verification are recorded from that manual OpenEmu playthrough confirmation.

## Engine Patches To Apply Before Build

- `patches/engine/0001-pallet-bedroom-mom-intro.patch` - Pallet bedroom news and Mom intro text.
- `patches/engine/0002-pallet-red-blue-scene.patch` - first outdoor Red/Blue Pallet scene.
- `patches/engine/0003-oak-lab-nexus-intro.patch` - Oak lab Nexus Red framing.
- `patches/engine/0004-worldlink-route1-alert.patch` - first Pokédex-style WorldLink alert after Blue's lab battle.
- `patches/engine/0005-oak-27-starter-menu.patch` - Oak's 27 official regional starter menu.
- `patches/engine/0006-route1-3-badge-scaled-encounters.patch` - badge-scaled Route 1-3 wild starter and special encounter tables.
- `patches/engine/0007-route3-anomaly-wild-battles.patch` - repeatable Route 3 Nexus anomaly encounters for remaining early species.

## Validation

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
python3 tools/validate_design_data.py
```

Result:

```text
Design data validation passed.
```
