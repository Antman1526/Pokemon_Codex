# PSDK Setup Audit - 2026-06-15

Purpose: record the current local Pokemon Studio / PSDK readiness state before creating or importing the production `POKEMON NEXUS RED` PSDK project.

## Official Source Check

Checked primary sources on 2026-06-15:

- Pokemon Studio latest GitHub release page shows `Pokemon Studio v2.9.1` as latest.
- Pokemon Studio README describes Studio as a standalone editor for game data, settings, texts, PSDK updates, and Tiled-to-PSDK map conversion.
- Pokemon Workshop getting-started docs point users to download the latest Pokemon Studio release first.
- Pokemon Studio v2.9.0 release notes state PSDK submodule was updated to `26.53`.
- Pokemon Studio version 3.0 is not ready for production use yet; current production planning should assume 2.9.x workflows.

References:

- https://github.com/PokemonWorkshop/PokemonStudio
- https://github.com/PokemonWorkshop/PokemonStudio/releases
- https://pokemonworkshop.com/en/documentation/get-started/
- https://pokemonworkshop.com/en/sdk/
- https://gitlab.com/pokemonsdk/pokemonsdk

## Local Machine Check

Machine:

- Architecture: `arm64`
- macOS: `26.5`

Local tools:

- Node: `/opt/homebrew/bin/node`, `v26.3.0`
- npm: `/opt/homebrew/bin/npm`, `11.16.0`
- Ruby: `/usr/bin/ruby`, `ruby 2.6.10p210`
- Git: `/opt/homebrew/bin/git`
- Godot reference tool: `/opt/homebrew/bin/godot`

Pokemon Studio:

- Installed app: `/Users/Antman/Applications/Pokemon Studio.app`
- Bundle identifier: `com.electron.pokemon-studio`
- Bundle version: `2.9.1`
- App size: about `333M`
- Downloaded archive still present: `/Users/Antman/Downloads/PokemonStudio-2.9.1.zip`
- Downloaded archive size: about `125M`

Bundled PSDK:

- Bundle path: `/Users/Antman/Applications/Pokemon Studio.app/Contents/Resources/psdk-binaries/`
- Bundled PSDK marker: `pokemonsdk/version.txt` contains `6709`
- Bundled files include `Game.rb`, `make_release.rb`, `make_update.rb`, and PSDK documentation markdown.

## Risks / Follow-Up

- `codesign --verify --deep --strict` reported: `code has no resources but signature indicates they must be present`.
- `spctl -a -vv` returned the same signature/resource complaint in shell output.
- There is no Pokemon Studio app in `/Applications`; the detected install is under the user application folder.
- Node source-development requirement from the Studio README is version-specific; local Node is newer. This matters only if building Studio from source, not necessarily for using the packaged app.
- No production PSDK project has been created in this repository yet.

## Current Decision

Proceed with PSDK as the primary production path, but treat the next task as a setup spike:

1. Launch Pokemon Studio manually or through a controlled desktop check.
2. Create a blank PSDK project in a temporary location first.
3. Inspect generated files before copying anything into `psdk/nexus-red/`.
4. Commit only safe source/data/script files and project metadata.
5. Do not commit PSDK binaries, generated exports, caches, commercial assets, ripped graphics/audio, save files, or local machine state.
