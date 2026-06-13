# Pokemon Nexus Red - macOS and OpenEmu Build Notes

Date: 2026-06-13
Target: build a `.gba` locally on macOS and test it in OpenEmu
Engine target: rh-hideout/pokeemerald-expansion or a project fork

## 1. Source Rule

Do not put ROM binaries in git. The repository should contain source, design data, tools, and build notes. Local `.gba`, `.sav`, `.srm`, `.ips`, `.bps`, and `.ups` files are ignored.

## 2. Primary References Checked

- rh-hideout/pokeemerald-expansion README: https://github.com/rh-hideout/pokeemerald-expansion
- pokeemerald-expansion build instructions: https://github.com/rh-hideout/pokeemerald-expansion/blob/upcoming/INSTALL.md
- pokeemerald-expansion macOS install guide: https://github.com/rh-hideout/pokeemerald-expansion/blob/master/docs/install/mac/MAC_OS.md

Current confirmed notes:

- `pokeemerald-expansion` is a GBA ROM hack base built on pret's pokeemerald decompilation.
- It is not a playable game by itself.
- The build command is `make`.
- The built ROM is expected as `pokeemerald.gba`.
- macOS setup requires Xcode command line tools, libpng, pkg-config, and devkitARM/devkitPro.

## 3. macOS Toolchain Checklist

Install Xcode command line tools:

```sh
xcode-select --install
```

Install Homebrew packages:

```sh
brew install libpng pkg-config
```

Install devkitPro/devkitARM:

1. Install the devkitPro pacman package for macOS from devkitPro.
2. Install GBA development packages:

```sh
sudo dkp-pacman -Sy
sudo dkp-pacman -S gba-dev
sudo dkp-pacman -S devkitarm-rules
```

Set zsh environment variables:

```sh
export DEVKITPRO=/opt/devkitpro
echo "export DEVKITPRO=$DEVKITPRO" >> ~/.zshrc
export DEVKITARM=$DEVKITPRO/devkitARM
echo "export DEVKITARM=$DEVKITARM" >> ~/.zshrc
echo "if [ -f ~/.zshrc ]; then . ~/.zshrc; fi" >> ~/.zprofile
```

Optional parallel build helper:

```sh
sysctl -n hw.ncpu
make -j$(sysctl -n hw.ncpu)
```

## 4. Recommended Repo Layout

```text
Pokemon_Codex/
  docs/
  data_design/
  tools/
  build_notes/
  engine/
    pokeemerald-expansion/    # fork/clone; do not commit generated ROMs
  patches/
  assets/
```

## 5. First Engine Setup Flow

Proposed local flow:

```sh
cd /Users/Antman/Desktop/Pokemon_Codex/engine
git clone https://github.com/rh-hideout/pokeemerald-expansion.git
cd pokeemerald-expansion
make -j$(sysctl -n hw.ncpu)
```

Expected output:

```text
pokeemerald.gba
```

Then manually open the built `.gba` in OpenEmu for smoke testing.

## 6. OpenEmu Smoke Test

For every playable milestone:

1. Open the `.gba` in OpenEmu.
2. Confirm title screen appears.
3. Start a new game.
4. Walk between maps.
5. Enter a battle.
6. Save in-game.
7. Quit OpenEmu.
8. Reopen the game.
9. Confirm save loads.
10. Play at least 30 minutes with no crash before calling a milestone stable.

## 7. Early Project-Specific Build Targets

The first real Pokemon Nexus Red build should not attempt all regions.

Build order:

1. vanilla engine boots,
2. title/name placeholder,
3. Pallet start,
4. starter selection prototype,
5. Blue/Ava/Dax opening,
6. WorldLink prototype,
7. Route 1-3 encounter changes,
8. Brock and first Rocket anomaly,
9. OpenEmu smoke test.

## 8. Known GBA Constraints

- A nine-region game must be compressed and chaptered.
- Save data must store progress flags, not complex simulated rival inventories.
- Following Pokemon should be phased, not guaranteed for every species at first.
- Dynamax and Tera should be restricted to specific battle contexts.
- Day/night should prefer an in-game clock unless RTC support is confirmed stable.

## 9. Local Engine Proof Status

Checked on: 2026-06-13

Engine source:

```text
engine/pokeemerald-expansion
```

The engine is tracked as a git submodule:

```text
https://github.com/rh-hideout/pokeemerald-expansion.git
```

Local dependency check:

- `make`: available
- `git`: available
- `python3`: available
- `brew`: available
- `pkg-config`: available
- `libpng` via pkg-config: available
- `arm-none-eabi-gcc`: missing
- `arm-none-eabi-as`: missing
- `dkp-pacman`: missing

Baseline build attempt:

```sh
cd /Users/Antman/Desktop/Pokemon_Codex/engine/pokeemerald-expansion
make -j$(sysctl -n hw.ncpu)
```

Result: failed before ROM output because the devkitARM toolchain is missing.

Representative errors:

```text
arm-none-eabi-gcc: command not found
arm-none-eabi-as: command not found
```

Next required step:

Install devkitPro/devkitARM, then rerun the baseline build.

Homebrew does not provide a local formula/cask for `devkitpro`, `devkitarm`, or `gba-dev` on this machine, so use the official devkitPro package installer flow described above.

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
