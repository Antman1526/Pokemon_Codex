# Pokemon Nexus Red - PC/Mac Native Build Notes

Date: 2026-06-14

## Current Status

The repository contains the first native Godot shell under:

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

Godot is installed locally:

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

The full nine-region Pokemon Nexus Red target is now native PC/Mac first.

The GBA/OpenEmu path remains useful for:

- nostalgia-first experiments,
- proving Kanto scenes quickly,
- preserving work already done,
- comparing FireRed-style presentation.

It should not be treated as the required format for the complete all-region release.

## Required Local Setup

Godot 4 and export templates are installed. Reconfirm with:

```sh
godot --version
godot --headless --version
```

Expected future dev command:

```sh
godot --path native/nexus-red
```

Native shell validation:

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

Expected future export commands:

```sh
godot --headless --path native/nexus-red --export-release "Windows Desktop" builds/windows/PokemonNexusRed.exe
godot --headless --path native/nexus-red --export-release "macOS" builds/macos/PokemonNexusRed.app
```

## Next Build Step

Next build step:

- add Route 1 encounter-rumor data without full combat,
- add the first WorldLink rival notification batch after Route 1,
- start the battle engine data model behind the placeholder screen,
- keep full battle mechanics and full creature data out of scope until the placeholder battle flow is stable.

Do not port all nine regions at once. Keep expanding the playable native Kanto shell, then build chapter by chapter.
