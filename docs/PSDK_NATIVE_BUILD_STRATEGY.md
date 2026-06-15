# Pokemon Nexus Red - Pokemon Studio / PSDK Strategy

Date: 2026-06-15

## Decision

Pokemon Nexus Red should pivot its primary PC/Mac implementation path to Pokemon Studio plus Pokemon SDK, abbreviated here as PSDK.

The existing Godot project under `native/nexus-red/` remains valuable as a playable prototype, design proof, and automated-test reference. It should not be expanded as the primary all-nine-region production engine unless PSDK proves blocked after a real setup spike.

## Why PSDK Is Now Primary

Pokemon Studio / PSDK is purpose-built for this exact game class: classic top-down creature-collector RPGs with data-driven creatures, moves, abilities, items, trainers, encounters, maps, events, and battle systems.

Primary-source facts checked on 2026-06-15:

- Pokemon Studio is a standalone editor for editing game data, settings, texts, updating Pokemon SDK, and managing Tiled-to-PSDK map conversion.
- PSDK is the underlying game engine/starter kit used by Pokemon Studio projects.
- The official Pokemon Studio GitHub releases are active in 2026, with the v2.9.x release line updating the PSDK submodule.
- Pokemon Studio development requires Node.js, while PSDK scripting/content customization uses Ruby and project data files.

Primary links:

- https://github.com/PokemonWorkshop/PokemonStudio
- https://github.com/PokemonWorkshop/PokemonStudio/releases
- https://pokemonworkshop.com/en/documentation/get-started/
- https://pokemonworkshop.com/en/sdk/
- https://gitlab.com/pokemonsdk/pokemonsdk

## Engine Roles

Primary production engine:

- Pokemon Studio / PSDK.
- Use for the real PC/Mac all-region build.
- Use Studio for data editing, trainer teams, species, moves, items, texts, maps, and project compilation.
- Use PSDK Ruby scripts/plugins for custom systems: WorldLink, companion AI, faction-war logic, region gating, rival simulation, and QoL extensions.

Reference/prototype engine:

- Godot 4 project under `native/nexus-red/`.
- Preserve as a tested vertical-slice prototype and story/data reference.
- Do not keep adding full production content to Godot while PSDK is primary.

Legacy reference:

- GBA/OpenEmu path remains a nostalgia and ROM-hack reference only.
- It is not the complete all-nine-region target.

## Legal And Asset Policy

Do not commit commercial ROMs, extracted ROM assets, or copyrighted ripped asset packs.

PSDK may make it easier to achieve FireRed/LeafGreen-style presentation, but the repository still needs a clean asset policy:

- Store original/custom assets or legally cleared placeholders in repo.
- Document any external asset source and license before import.
- Keep Pokemon-style design references in docs, but avoid relying on proprietary assets for distributable builds.
- Treat built game exports as local/dev artifacts unless legal review says otherwise.

## Proposed Repository Layout

```text
psdk/
  nexus-red/
    README.md
    project/
      Data/
      Graphics/
      Audio/
      scripts/
      maps/
    docs/
      content-migration/
      studio-data-notes/

native/nexus-red/
  Godot prototype and automated reference tests
```

The first PSDK commit should not vendor large binaries blindly. Start by documenting the expected project root, then scaffold only files that are safe, text-based, and Git-friendly.

## Migration Plan

### Phase 0 - PSDK Setup Spike

Acceptance:

- Pokemon Studio installed or buildable locally on macOS.
- PSDK binaries/project creation path confirmed.
- A blank or sample PSDK project opens.
- The project can be versioned without committing generated caches, binaries, or unsafe assets.
- The team documents which files are source-of-truth text/data files.

### Phase 1 - PSDK Project Scaffold

Acceptance:

- `psdk/nexus-red/` exists with a clear README.
- Project naming, legal asset policy, and Git ignore rules are documented.
- Kanto-first content migration map exists: Pallet, Oak lab, Route 1, Viridian, Pewter.
- 39-starter contract is mapped from the Godot JSON/prototype data to PSDK data concepts.

### Phase 2 - Kanto First Playable In PSDK

Acceptance:

- Title/new-game flow starts the Red-era Pallet opening.
- Antman, Red, Blue, Oak, Mom, and first partner selection exist.
- Routes 1-3 support all 27 official starters plus 12 special early choices through progression-safe availability.
- WorldLink is stubbed as a menu or event-driven UI.
- Red is represented as the primary recurring companion.

### Phase 3 - Custom Systems

Acceptance:

- WorldLink feed and checklist are implemented in Ruby/PSDK scripts.
- Companion system supports Red first, then Ash/Misty/Brock.
- Rival simulation data supports at least Blue, Ava, and Dax before scaling to 10 rivals.
- Faction IDs use Rocket, Magma, Aqua, Phoenix, Moonlight, Gold Dust, Gas, Clover, and Nexus Order.

## Immediate Next Step

Create the PSDK project scaffold and installation notes, then prove a blank PSDK project can run locally before porting the current Godot Kanto scenes.
