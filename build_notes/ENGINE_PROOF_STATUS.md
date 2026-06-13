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
Blocked: devkitARM is installed on disk, but the current shell does not
resolve arm-none-eabi tools because DEVKITPRO/DEVKITARM and PATH are not set.
```

Confirmed available:

- make
- git
- python3
- brew
- pkg-config
- libpng via pkg-config

Confirmed installed on disk:

- arm-none-eabi-gcc
- arm-none-eabi-as
- dkp-pacman

Current shell resolution:

```sh
command -v arm-none-eabi-gcc || true
command -v arm-none-eabi-as || true
command -v dkp-pacman || true
```

Result:

```text
/usr/local/bin/dkp-pacman
```

Environment check:

```sh
printf 'DEVKITPRO=%s\n' "$DEVKITPRO"
printf 'DEVKITARM=%s\n' "$DEVKITARM"
```

Result:

```text
DEVKITPRO=
DEVKITARM=
```

Disk check:

```text
/opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc
/opt/devkitpro/devkitARM/bin/arm-none-eabi-as
/usr/local/bin/dkp-pacman
```

Package check:

```sh
dkp-pacman -Q devkitARM
```

Result:

```text
devkitARM r68-1
```

Homebrew check:

```text
brew search devkitpro devkitarm gba-dev
```

Result:

```text
No formulae or casks found.
```

The official devkitPro macOS installer appears to have installed devkitARM,
but the shell environment still needs to be configured.

## Interpretation

This is a local shell configuration blocker, not a design blocker and not an
engine selection failure. The next build step is configuring devkitPro in the
shell so `arm-none-eabi-gcc` and `arm-none-eabi-as` resolve without absolute
paths, then rerunning the baseline `make`.

## Next Step

Configure the shell environment, then verify:

```sh
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
command -v arm-none-eabi-gcc
command -v arm-none-eabi-as
command -v dkp-pacman
```

After those commands resolve, rerun:

```sh
cd /Users/Antman/Desktop/Pokemon_Codex/engine/pokeemerald-expansion
make -j$(sysctl -n hw.ncpu)
```
