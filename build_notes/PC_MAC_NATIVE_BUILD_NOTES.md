# Pokemon Nexus Red - PC/Mac Native Build Notes

Date: 2026-06-14

## Current Status

The repository does not yet contain a native PC/Mac game project.

`godot`, `godot4`, and `Godot` were not found on the local PATH during this check, so native exports cannot be built yet from this machine.

## Platform Pivot

The full nine-region Pokemon Nexus Red target is now native PC/Mac first.

The GBA/OpenEmu path remains useful for:

- nostalgia-first experiments,
- proving Kanto scenes quickly,
- preserving work already done,
- comparing FireRed-style presentation.

It should not be treated as the required format for the complete all-region release.

## Required Local Setup

Install Godot 4 and export templates, then confirm:

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
