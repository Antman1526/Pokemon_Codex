# Pokemon Nexus Red - Engine Proof Status

Date: 2026-06-13

## Current Result

The engine source reference has been added successfully:

```text
engine/pokeemerald-expansion
```

It is tracked as a git submodule pointing to:

```text
https://github.com/rh-hideout/pokeemerald-expansion.git
```

## Build Attempt

Command:

```sh
cd /Users/Antman/Desktop/Pokemon_Codex/engine/pokeemerald-expansion
make -j$(sysctl -n hw.ncpu)
```

Result:

```text
Failed: devkitARM / arm-none-eabi tools missing.
```

Confirmed available:

- make
- git
- python3
- brew
- pkg-config
- libpng via pkg-config

Confirmed missing:

- arm-none-eabi-gcc
- arm-none-eabi-as
- dkp-pacman

Homebrew check:

```text
brew search devkitpro devkitarm gba-dev
```

Result:

```text
No formulae or casks found.
```

Use the official devkitPro macOS installer path rather than Homebrew.

## Interpretation

This is a local toolchain blocker, not a design blocker and not an engine selection failure. The next build step is installing devkitPro/devkitARM on macOS, then rerunning the baseline `make`.

## Next Step

Install devkitPro/devkitARM using the official macOS package flow, then verify:

```sh
command -v arm-none-eabi-gcc
command -v arm-none-eabi-as
command -v dkp-pacman
```

After those commands resolve, rerun:

```sh
cd /Users/Antman/Desktop/Pokemon_Codex/engine/pokeemerald-expansion
make -j$(sysctl -n hw.ncpu)
```
