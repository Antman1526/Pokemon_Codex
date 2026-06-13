# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered
```

Output ROM:

```text
engine/pokeemerald-expansion/pokefirered.gba
```

Verified ROM:

```text
/Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokefirered.gba
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
