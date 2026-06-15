# Pokemon Nexus Red - Decisions Log

Date started: 2026-06-13

This file records locked design decisions so future Claude/Codex sessions do not reopen settled questions.

## Locked Decisions

### Platform

Decision: Pokemon Nexus Red now targets a native PC/Mac standalone game for the complete all-nine-region build.

Implication: use a Godot 4 custom 2D RPG framework as the recommended primary path. The GBA/OpenEmu path remains a legacy prototype/reference track and can still be used for nostalgia-first experiments, but it should not limit the full game vision.

Decision: the complete nine-region version is one native game exported to Windows PC and macOS, not two separate games and not a single GBA ROM.

Implication: package as `.exe` for Windows and `.app`/`.dmg` for macOS from the same source project. Keep content data-driven so the same story, Pokemon availability, WorldLink, companions, rivals, and region progression power both desktop targets.

### Region Scope

Decision: all nine main-series regions must be represented as complete, satisfying story chapters.

Implication: every region needs a serious main arc, gym/trial progression, villain conflict, rival content, side activities, and a legendary/mechanic climax. On GBA, this should mean full-feeling curated chapters rather than tile-for-tile retail remakes.

### Protagonist and Red

Decision: Antman is a new Pallet Town trainer following Red's path. Red is a friend and early travel companion, not the player character.

Implication: Red can appear in the beginning, travel with Antman during key sections, teach lessons silently or through sparse dialogue, and become an emotional anchor for the classic Kanto identity.

### Difficulty

Decision: Standard difficulty should be closer to Radical Red than vanilla mainline, but less punishing.

Implication: Standard should use smart teams, level caps, useful held items, and better AI, but avoid hard counters, excessive punishment, and mandatory competitive optimization. Hard/Expert can carry the more serious ROM-hack challenge.

### Pokemon Availability

Decision: all Pokemon through Generation 9 should be catchable before the final boss.

Implication: the main story must include a complete availability plan using routes, swarms, fishing, gifts, fossils, breeding, raids, wormholes, anomalies, and late-region unlocks. Postgame can improve hunting methods, but should not be required for base species completion.

### Region Length

Decision: each region should target 10+ hours of main story.

Implication: the full main story target rises to roughly 100-130 hours, with completionist play well beyond that. The game must avoid grind padding by using meaningful bosses, exploration, rivals, collection, and side stories.

### Art Direction

Decision: classic FireRed style, but much better visuals.

Implication: the game should keep top-down tile-based towns, routes, interiors, caves, forests, gyms, labs, and battle presentation, while upgrading to HD pixel tiles, richer palettes, weather/day-night lighting, smoother animation, polished menus, improved battle effects, and widescreen-native readability.

### Starter Scope

Decision: the first playable design should include all 39 starter choices, not a reduced starter prototype.

Implication: the starter selector can be mechanically simple at first, but the content scope must include all nine regional starter trios plus the 12 special starters from the beginning.

### First Battle

Decision: Blue is the mandatory first battle.

Implication: Blue remains the classic first rival pressure point, while Dax and Ava enter immediately after as parallel rivals with their own early encounters.

### Brock Difficulty

Decision: Brock should be friendly-mainline hard on Standard, with difficulty options for harder versions.

Implication: Standard Brock should be beatable by normal players who explore and catch early Pokemon. Hard/Expert/Nuzlocke Brock can add stronger teams, held items, and sharper AI.

### Repository Target

Decision: use `https://github.com/Antman1526/Pokemon_Codex` as the GitHub repository target.

Implication: local git should be initialized with this remote, but generated ROM/save/patch artifacts must remain ignored.

### Red Frequency

Decision: Red should appear frequently across the entire game as a true travel companion.

Implication: Red can follow Antman, talk during exploration, help train, and join tag battles. He should not participate in gym battles or other major solo tests where Antman needs to prove himself.

### Brock, Misty, and May Friend Arcs

Decision: Brock, Misty, and May become recurring friends with dedicated scenes.

Implication: Brock becomes an early mentor for training, field survival, and Rock/Ground strategy. Misty becomes a water-route, confidence, and battle-tempo friend. May becomes the Hoenn field-research friend who connects ecology, weather, and the wider World Circuit.

### Ash, Blue, Bill, and Red Companion Model

Decision: Red is the primary full-game companion. Ash, Misty, and Brock are long-term recurring travel-party companions. Blue is the rival who becomes an anti-hero ally, May is the Hoenn ecology companion, and Bill is the technical network ally.

Implication: Red remains the most important companion and should not be replaced by Ash. Ash, Misty, and Brock make the journey feel like a traveling-party story, while Blue, May, and Bill rotate in for major arcs to avoid overcrowding.

### Nexus Island Final Chapter

Decision: the final chapter is Nexus Island, a full final-region-scale island, not a small postgame zone or only a championship hub.

Implication: Nexus Island needs towns, routes, caves, ruins, beaches, forests, mountains, research labs, villain bases, hidden bosses, final rival battles, a full multi-faction war, a Rocket metropolis, legendary convergence, and the final Giovanni battle.

### Native Faction Model

Decision: the native PC/Mac plan uses Rocket, Magma, Aqua, Phoenix, Moonlight, Gold Dust, Gas, Clover, plus the hidden Nexus Order. Later canonical teams such as Galactic, Plasma, Flare, Skull, Macro Cosmos, and Star are dropped as active faction IDs.

Implication: preserve each region's story spirit through the custom faction war instead of carrying every canonical villain team as a separate active organization.

### Battle Gimmick Scope

Decision: Dynamax and Terastallization should not dominate the early game, but controlled usability can unlock after the third region.

Implication: Kanto, Johto, and Hoenn should not use player-controlled Dynamax/Tera. After Hoenn, controlled facilities or limited story contexts can let players experiment. Galar and Paldea still remain the full story homes for Dynamax and Tera.

### National Dex Guidance

Decision: WorldLink should provide an optional checklist/guide for catching all Pokemon before the final boss, without actively pushing the player.

Implication: add a Pokedex Readiness checklist with missing-species summaries, habitat hints, swarm reports, and remaining legendary/fossil/evolution needs. It should be pull-based: the player opens it when they want help.

### Next Design Priority

Decision: deepen Full Kanto first.

Implication: Kanto must become the tone-setting 12-15 hour foundation with Red, Blue, Ava, Dax, Rocket, Moonlight, Phoenix, Gold Dust, early rare Pokemon, and a complete Indigo League arc.

### WorldLink Travel Role

Decision: WorldLink is not a quick-jump system to other regions.

Implication: WorldLink can show travel unlocks, route status, tickets, and destination information, but actual travel must happen through in-world methods such as trains, ferries, airports, Fly/Sky Pass points, wormholes, or Academy gates.

### Red Battle Control

Decision: Red is AI-controlled in tag battles.

Implication: Red should feel like a companion with his own agency. The player controls Antman's side; Red's team and behavior are tuned through AI/team scripts.

### Engine Proof Priority

Decision: the best next build step is engine proof/build readiness.

Implication: add `pokeemerald-expansion` as the engine source reference, verify local macOS build dependencies, and document blockers before implementing custom systems.

### First Build Title Identity

Decision: the first build should carry the Pokemon Nexus Red title identity.

Implication: even if the first title screen is placeholder-quality, the project should stop presenting itself as generic Emerald as early as practical.

### Custom Title-Screen Concept

Decision: create a custom title-screen concept before implementation.

Implication: the target concept is Red and Pikachu overlooking Pallet's dawn coastline/cliff while a red-gold Nexus rift forms a fractured world-map silhouette in the sky. Placeholder execution is allowed for first build, but the creative target is locked.

### Opening Story Intro

Decision: include a short bedroom, Mom, and Oak intro before the lab.

Implication: the game opens with Antman at home, news of strange weather/migration/League outages, Mom grounding the moment emotionally, Red noticing impossible Pallet tracks, Blue applying pressure, and Oak introducing the World Pokedex Initiative.

### Red AI Team Model

Decision: Red remains AI-controlled and uses chapter-based teams with limited adaptive slots.

Implication: Red's team should feel recognizable by chapter while one or two slots can adapt to Antman's starter, difficulty, and battle context for fun and support.

### WorldLink Dungeon Pause

Decision: WorldLink notifications pause during caves, dungeons, hideouts, ruins, towers, and other focus-heavy spaces.

Implication: queued updates should be delivered through a compact "While You Were Away" digest when Antman returns to a safe area.

### Mandatory Brock and Misty Companions

Decision: Brock and Misty are mandatory recurring story companions after their gym arcs.

Implication: they rotate in and out across the story as friends, mentors, and tag-battle allies, but they do not become permanent followers or fight Antman's gym battles.

## 2026-06-15

### PSDK Primary Engine Pivot

Decision: Pokemon Studio / PSDK becomes the recommended primary production engine for the native PC/Mac all-nine-region build.

Implication: the existing Godot project under `native/nexus-red/` remains a validated prototype/reference slice, but new production work should move toward a safe `psdk/nexus-red/` scaffold, Pokemon Studio data workflows, Tiled-to-PSDK maps, and PSDK Ruby scripts for custom systems.

### Godot Reference Track

Decision: do not discard the Godot work.

Implication: the Godot Kanto slices remain useful for behavior tests, story flow references, and migration notes, but they should not be expanded as the production engine while PSDK is the active primary target.
