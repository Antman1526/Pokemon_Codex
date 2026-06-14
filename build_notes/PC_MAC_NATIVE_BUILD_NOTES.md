# Pokemon Nexus Red - PC/Mac Native Build Notes

Date: 2026-06-14

## Current Status

The repository does not yet contain a native PC/Mac game project.

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

Expected future export commands:

```sh
godot --headless --path native/nexus-red --export-release "Windows Desktop" builds/windows/PokemonNexusRed.exe
godot --headless --path native/nexus-red --export-release "macOS" builds/macos/PokemonNexusRed.app
```

## Next Build Step

Create `native/nexus-red/` as a Godot project with:

- title/menu scene,
- Antman's bedroom scene,
- input map,
- save skeleton,
- region/chapter data loader,
- WorldLink UI placeholder,
- local validation command.

Do not port all nine regions at once. Start with a playable native Kanto shell, then expand chapter by chapter.
