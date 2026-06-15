# Pokemon Nexus Red - PC/Mac Native Build Notes

Date: 2026-06-14
Updated: 2026-06-15

## Current Status

The primary production recommendation has changed to Pokemon Studio / PSDK.

The repository also contains a validated Godot reference prototype under:

```text
native/nexus-red/
```

The first playable slice currently covers:

- title screen,
- New Game flow,
- Antman's bedroom,
- Mom opening-scene prompt,
- transition to Professor Oak's lab,
- 39-starter selector prototype,
- Blue/Ava/Dax starter assignment state,
- first Blue pressure dialogue after starter selection,
- Route 1 walkable prototype,
- Red's first Route 1 companion scene,
- first Blue battle placeholder state,
- shared battle placeholder screen,
- Blue Route 1 placeholder battle data,
- placeholder WorldLink panel,
- save-state skeleton,
- native content data for regions, factions, companions, starters, and opening feed.

Godot is installed locally for the reference prototype:

```text
4.6.3.stable.official.7d41c59c4
```

The Homebrew cask installed `/Applications/Godot.app` and linked:

```text
/opt/homebrew/bin/godot
```

Matching Godot 4.6.3 export templates are installed at:

```text
~/Library/Application Support/Godot/export_templates/4.6.3.stable/
```

Confirmed template files include:

- `windows_release_x86_64.exe`
- `windows_release_arm64.exe`
- `macos.zip`

## Platform Pivot

The full nine-region Pokemon Nexus Red target is now native PC/Mac first, with Pokemon Studio / PSDK as the recommended production engine.

The Godot project remains useful for:

- automated behavior references,
- story and data proof slices,
- comparing implementation decisions before porting them to PSDK.

It should not be treated as the production all-region engine while the PSDK path is active.

The GBA/OpenEmu path remains useful for:

- nostalgia-first experiments,
- proving Kanto scenes quickly,
- preserving work already done,
- comparing FireRed-style presentation.

It should not be treated as the required format for the complete all-region release.

## Required Local Setup

Next required PSDK setup:

- Install/open Pokemon Studio.
- Create or open a blank PSDK project.
- Confirm where PSDK project data, maps, scripts, and generated files live.
- Document which generated/cache/export files must not be committed.

Godot 4 and export templates are installed for the reference prototype. Reconfirm with:

```sh
godot --version
godot --headless --version
```

Reference dev command:

```sh
godot --path native/nexus-red
```

Reference prototype validation:

```sh
python3 tools/validate_native_godot_shell.py
python3 tools/validate_native_starter_slice.py
python3 tools/validate_native_route1_slice.py
python3 tools/validate_native_battle_placeholder_slice.py
godot --headless --path native/nexus-red --check-only --quit
godot --headless --path native/nexus-red --script tests/smoke_test.gd
godot --headless --path native/nexus-red --script tests/starter_slice_test.gd
godot --headless --path native/nexus-red --script tests/route1_slice_test.gd
godot --headless --path native/nexus-red --script tests/battle_placeholder_test.gd
```

Old Godot reference export command shape:

```sh
godot --headless --path native/nexus-red --export-release "Windows Desktop" builds/windows/PokemonNexusRed.exe
godot --headless --path native/nexus-red --export-release "macOS" builds/macos/PokemonNexusRed.app
```

## Next Build Step

Next build step:

- perform the Pokemon Studio / PSDK setup spike,
- create the safe `psdk/nexus-red/` project scaffold,
- document the PSDK Git ignore/source-of-truth policy,
- map the existing Godot Kanto prototype data into PSDK concepts before importing content.

Do not port all nine regions at once. Prove a small PSDK Pallet/Route 1 loop first, then build chapter by chapter.
