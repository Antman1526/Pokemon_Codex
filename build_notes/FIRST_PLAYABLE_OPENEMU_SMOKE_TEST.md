# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

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
File exists and is 32M. This is build-artifact verification only; OpenEmu runtime checks remain unchecked below.
```

## Smoke Test Checklist

- [ ] ROM appears locally as `pokenexusred.gba`.
- [ ] ROM opens in OpenEmu.
- [ ] Title screen appears.
- [ ] New game starts.
- [ ] Player reaches Pallet bedroom.
- [ ] Save works.
- [ ] Reload works.

## Notes

Baseline FireRed-target build before Pokemon Nexus Red content edits.

## Applied Engine Patches

- `patches/engine/0001-pallet-bedroom-mom-intro.patch` - Pallet bedroom news and Mom intro text.

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
