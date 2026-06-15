# Pokemon Nexus Red - PC/Mac Native Build Strategy

Date: 2026-06-14
Platform decision: native PC/Mac build becomes the primary target for the full nine-region game.
Legacy target: the `.gba`/OpenEmu work remains useful as a prototype and nostalgia reference, but it is no longer the recommended target for the full all-region release.

## 1. High-Level Decision

Pokemon Nexus Red should move to a native desktop fan-game architecture for the complete vision: Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea, and the final full-region Nexus Island chapter, all Pokemon through Generation 9, full companion arcs, WorldLink, 10 rivals, modern battle systems, and long-form region progression.

Proposed: build one native game, not two separate versions. The same project exports to:

- Windows PC: `.exe` plus data/content folder or installer.
- macOS: `.app` plus `.dmg` or zipped app bundle.

This is not a GBA ROM anymore. It is one Pokemon-style desktop game that can carry the entire design without GBA memory, save, UI, audio, and asset constraints.

## 2. Recommended Engine

Proposed: Godot 4, custom 2D RPG framework.

Why this is the best fit:

- Exports to Windows and macOS from one codebase.
- Strong 2D TileMap, UI, input, animation, audio, and data-loading support.
- No RPG Maker dependency for players.
- Better long-term control than Pokemon Essentials for WorldLink, 10 rivals, companion AI, regional unlocks, and all nine regions.
- Easier for Claude Code and Codex to modify than a binary editor workflow.
- Supports data-driven content, which is required for a project this large.

Not recommended as primary:

- GBA decomp only: excellent nostalgia, too constrained for all nine full regions and every requested system.
- RPG Maker/Pokemon Essentials only: fast for Pokemon fangame conventions, weaker for a custom PC/Mac package, custom UI, large data pipeline, and long-term source control hygiene.
- Unity: capable, but heavier licensing/project overhead for a 2D Pokemon-style RPG.

## 3. Game Identity

Title: `POKEMON NEXUS RED`

Subtitle direction: `A World Circuit Adventure`

Tone: warmer adventure with serious villain pressure. Red is Antman's primary full-game friend and recurring AI companion. Ash, Misty, and Brock are long-term recurring travel-party companions, while Blue, May, and Bill rotate into major arcs.

Primary player fantasy:

- Start in Pallet Town as Antman, a new trainer following Red's path.
- Travel one region at a time, in story order.
- See rivals progress through WorldLink without turning region travel into quick-jump teleporting.
- Complete a full global Pokemon journey where every region's original story spirit is honored, twisted through the custom faction war, and tied into the Meridian/Nexus crisis.
- End on Nexus Island, a full final-region chapter where Giovanni, Team Rocket, every rival, every companion, all visible factions, and the hidden Nexus Order collide.

## 4. Native Architecture

Recommended project root:

```text
native/nexus-red/
  project.godot
  src/
    battle/
    world/
    ui/
    data/
    companions/
    worldlink/
    save/
  content/
    regions/
      kanto/
      johto/
      hoenn/
      sinnoh_hisui/
      unova/
      kalos/
      alola/
      galar/
      paldea/
      nexus_island/
    trainers/
    pokemon/
    moves/
    items/
    dialogue/
    music/
  tests/
  exports/
```

Data first, scenes second. Region chapters, trainers, encounters, marts, WorldLink notifications, companion scenes, faction wars, and boss teams should live in structured data files. Godot scenes should render and execute that data, not hard-code every event.

Internal source should use generic names such as creature, trainer, region, faction, companion, and WorldLink. Design docs can preserve Pokemon-style references, but source/data should stay swap-friendly where practical.

## 5. Core Systems To Build Natively

### World And Region Flow

- One-region-at-a-time progression.
- Kanto starts locked as the only playable region.
- Johto unlocks only after Kanto's League/Nexus departure.
- Hoenn unlocks only after Johto's Radio Tower/Lugia-Ho-Oh crisis.
- Later regions unlock through story transit, not menu teleporting.
- WorldLink shows passports, tickets, route status, rival activity, and checklists.

### Battle Engine

Build a custom Pokemon-style battle engine with:

- Physical/Special split.
- Fairy type.
- Abilities, hidden abilities, Ability Capsules, Ability Patches.
- Modern moves and Gen 9-style mechanics.
- Level caps by difficulty.
- Difficulty presets.
- Smart but readable boss AI.
- Optional Nuzlocke rules.
- Mega Evolution in Kalos onward.
- Z-Moves in Alola onward.
- Dynamax and Tera usable only after Hoenn, with their full story homes in Galar and Paldea.

### Pokemon Data

All Pokemon through Generation 9 must be represented by data tables:

- species,
- forms,
- base stats,
- types,
- abilities,
- learnsets,
- evolutions,
- catch rates,
- habitats,
- regional availability,
- sprites/animations or placeholder art references.

Rule: all base Pokemon must be catchable before the final boss through normal story, optional routes, swarms, gifts, fossils, breeding, fishing, raids, wormholes, anomalies, or legendary quests.

### WorldLink

WorldLink is a signature native UI system, not a simple message box. It should look like a polished HD FireRed-era trainer device, not a modern phone.

Pages:

- Feed: rival captures, badge wins, villain alerts, companion notes.
- Map: current region route status and next story objective.
- Rivals: 10 rival profiles, progress, recent team notes.
- Companions: Red, Ash, Brock, Misty, May, Bill, Blue, and rotating regional allies.
- Pokedex Checklist: optional catch guidance, not forced guidance.
- Settings: notification frequency, digest mode, difficulty/Nuzlocke toggles.

Rule: WorldLink notifications pause during caves, dungeons, hideouts, ruins, towers, and major focus spaces. When the player returns to a safe hub, queued updates arrive as a compact digest.

### Companions

Red is the primary full-game companion:

- appears frequently,
- travels with Antman during story routes,
- talks more than retail Red because he is Antman's friend,
- helps train the player,
- joins AI-controlled tag battles,
- never fights Antman's gym battles for him.

Ash, Brock, and Misty become long-term recurring companions after their Kanto arcs. Blue remains the rival-to-ally pressure point, May becomes the major Hoenn field-research companion, and Bill becomes the technical systems ally. Later chapters add regional companions without replacing Red.

### Visual Direction

Classic FireRed style, upgraded for native PC/Mac:

- top-down tile-based towns, routes, interiors, caves, forests, gyms, labs, and battle presentation;
- higher-detail HD pixel tiles and cleaner palettes;
- smoother character animation;
- weather and day/night lighting;
- improved water, grass, cave, and city effects;
- polished menus and WorldLink UI;
- widescreen-native layout while preserving FireRed readability.

Visual quality bar: the final native build should look identical in readability and game-feel to the best FireRed-style ROM hacks, and better where native resolution, lighting, animation, UI, and effects can improve it. Use original/custom or legally safe placeholder assets while matching the top-down GBA Pokemon composition: tile density, character scale, route readability, town silhouettes, battle framing, and menu clarity. Do not pivot to 3D, painterly art, or a modern phone-app interface to chase fidelity.

### QoL And Player Options

Native build should include all requested QoL:

- Infinite/toggleable Repels.
- Portable PC.
- Portable healing with difficulty limits.
- Skip text.
- Faster battle/text options.
- Infinite Rare Candies in marts.
- Nature changers.
- Easy EV training.
- IV maxing.
- Trade evolution replacements.
- Trainer rematches.
- Gym rematches.
- Expanded marts.
- 4 fishing rod tiers.
- Bike and running from start.
- Expanded Dig and Fly utility.
- Enhanced Pokemon Center and Mart services.
- Start with `$100,000`.

## 6. Build Commands

Godot 4.6.3 and matching export templates are installed on this machine. Use commands shaped like:

```sh
godot --headless --path native/nexus-red --export-release "Windows Desktop" builds/windows/PokemonNexusRed.exe
godot --headless --path native/nexus-red --export-release "macOS" builds/macos/PokemonNexusRed.app
```

Expected local dev command:

```sh
godot --path native/nexus-red
```

Until export presets exist in the Godot project, repository validation should focus on data/spec consistency and headless project checks rather than binary export.

## 7. Migration Plan

### Phase 0 - Platform Pivot

Deliverables:

- PC/Mac native strategy.
- Updated decisions log.
- Platform target data.
- Validation script.
- GBA path marked as legacy prototype/reference.

### Phase 1 - Native Prototype Shell

Deliverables:

- Godot project scaffold.
- Boot screen with `POKEMON NEXUS RED`.
- Main menu.
- New game starts in Antman's bedroom.
- Save/load skeleton.
- Keyboard/controller input.
- Data loader for region/chapter YAML or converted JSON.

### Phase 2 - Kanto Native Vertical Slice

Scope:

- Bedroom, Mom, Oak intro.
- 39-starter selection.
- Blue first battle.
- Red warm companion scenes.
- Route 1, Viridian, Pewter.
- Brock, Red training, Pewter Museum anomaly.
- WorldLink feed prototype.

### Phase 3 - Full Kanto

Scope:

- All Kanto gyms.
- Rocket, Moonlight, Phoenix, Gold Dust arcs.
- Misty and Brock companion arcs.
- Indigo League.
- Kanto Pokedex availability tier.

### Phase 4 - Johto Through Paldea

Build each region as a complete chapter, in order:

1. Johto
2. Hoenn
3. Sinnoh/Hisui
4. Unova
5. Kalos
6. Alola
7. Galar
8. Paldea
9. Nexus Island

Each chapter must include its original story spine, Nexus twist, custom faction conflict, companion/rival content, mechanic spotlight, and exit hook.

Canonical later-region villain teams such as Galactic, Plasma, Flare, Skull, Macro Cosmos, and Star are not active faction IDs in the native plan. Their story themes are preserved through Rocket, Magma, Aqua, Phoenix, Moonlight, Gold Dust, Gas, Clover, and the hidden Nexus Order.

## 8. Legal And Asset Rules

Do not commit or distribute copyrighted commercial ROMs.

For a private fan project, the repo can describe Pokemon-style content and local user-owned assets. For any public release, asset and naming strategy must be reviewed carefully. The safest engineering rule is:

- source code, original data, original scripts, and original tooling may be committed;
- copyrighted ROM binaries, extracted commercial assets, and private keys/secrets must not be committed;
- placeholder/open/original art should be used until the asset policy is finalized.

## 9. Success Criteria

The native direction is ready when:

- Windows and macOS are documented as first-class targets.
- The repository clearly says native PC/Mac is the primary full-game path.
- GBA/OpenEmu is documented as legacy prototype/reference.
- Platform targets are machine-validated.
- The next implementation task can scaffold `native/nexus-red/` without reopening the engine decision.
- Nexus Island is documented as the full final-region chapter.

## 10. Immediate Next Recommendation

Next build slice: create the Godot project scaffold and bootable title/menu/bedroom prototype.

Do not start by implementing all Pokemon data. Start with the shell, save state, region/chapter loader, and Kanto bedroom intro. The project needs a playable native loop before it needs hundreds of species fully wired.
