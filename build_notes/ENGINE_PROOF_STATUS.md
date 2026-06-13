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

## Toolchain Check

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
command -v arm-none-eabi-gcc
command -v arm-none-eabi-as
command -v dkp-pacman
```

Result:

```text
/opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc
/opt/devkitpro/devkitARM/bin/arm-none-eabi-as
/usr/local/bin/dkp-pacman
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

Default shell resolution:

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

Explicit build-session verification:

```sh
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
command -v arm-none-eabi-gcc
command -v arm-none-eabi-as
command -v dkp-pacman
arm-none-eabi-gcc --version | sed -n '1p'
```

Result:

```text
/opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc
/opt/devkitpro/devkitARM/bin/arm-none-eabi-as
/usr/local/bin/dkp-pacman
arm-none-eabi-gcc (devkitARM) 16.1.0
```

## Interpretation

This is no longer a toolchain installation blocker. devkitARM is installed and
usable when the build command exports `DEVKITPRO`, `DEVKITARM`, and `PATH`.
Permanent shell configuration is still recommended later for convenience, but
it was not required for the successful baseline build recorded below.

## Proven Build Command

The clean FireRed baseline build has succeeded with this command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered
```

## FireRed Baseline Build - 2026-06-13

Clean command:

```sh
git -C engine/pokeemerald-expansion clean -fdX
```

Clean result:

```text
Exit code 0. No ignored build output was printed for removal.
```

Build command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered
```

Build result:

```text
Exit code 0.
tools/gbafix/gbafix pokefirered.elf -t"POKEMON FIRE" -cBPRE -m01 -r0 --silent
arm-none-eabi-objcopy -O binary pokefirered.elf pokefirered.gba
tools/gbafix/gbafix pokefirered.gba -p --silent
```

Final linker memory usage:

```text
Memory region         Used Size  Region Size  %age Used
           EWRAM:      226864 B       256 KB     86.54%
           IWRAM:       28644 B        32 KB     87.41%
             ROM:    27044024 B        32 MB     80.60%
```

Build warnings observed:

```text
ld: warning: ignoring file '/usr/local/lib/libz.dylib': found architecture 'i386', required architecture 'arm64'
arm-none-eabi-ld: warning: ../../pokefirered.elf has a LOAD segment with RWX permissions
```

These warnings did not fail the baseline build. They have not been fully
investigated or accepted as harmless. Before release packaging, re-check whether
the `/usr/local/lib/libz.dylib` architecture warning is coming from stale local
library search paths and whether the `RWX permissions` linker warning is
expected for this engine/toolchain combination.

ROM verification:

```sh
ls -lh /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokefirered.gba
```

Result:

```text
-rwxr-xr-x@ 1 Antman  staff    32M Jun 13 02:48 /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokefirered.gba
```

Interpretation:

The clean FireRed target baseline builds successfully with explicit devkitPro
shell exports. Generated engine build output and `pokefirered.gba` remain
ignored build artifacts and should not be committed.
