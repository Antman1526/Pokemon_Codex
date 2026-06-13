# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

Apply project-owned engine patches from the parent repo root before building:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
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

This smoke-test note now describes the patched first-playable build path. OpenEmu runtime verification is still pending; only the local ROM artifact has been verified.

## Engine Patches To Apply Before Build

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
