# Pokemon Nexus Red - Decisions Log

Date started: 2026-06-13

This file records locked design decisions so future Claude/Codex sessions do not reopen settled questions.

## Locked Decisions

### Platform

Decision: Pokemon Nexus Red targets a `.gba` ROM playable in OpenEmu on macOS.

Implication: use pokeemerald-expansion or a compatible pokeemerald decomp fork. Do not switch to Pokemon Essentials unless the project goal changes.

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

Decision: FireRed-first visual style.

Implication: the game should feel visually closest to FireRed in tiles, palette clarity, UI nostalgia, and Kanto identity. Because the recommended engine path is still pokeemerald-expansion, implementation may use Emerald-compatible internals, but the player-facing art direction should be FireRed-first with custom polish.

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

### Battle Gimmick Scope

Decision: Dynamax and Terastallization should not dominate the early game, but controlled usability can unlock after the third region.

Implication: Kanto, Johto, and Hoenn should not use player-controlled Dynamax/Tera. After Hoenn, controlled facilities or limited story contexts can let players experiment. Galar and Paldea still remain the full story homes for Dynamax and Tera.

### National Dex Guidance

Decision: WorldLink should provide an optional checklist/guide for catching all Pokemon before the final boss, without actively pushing the player.

Implication: add a Pokedex Readiness checklist with missing-species summaries, habitat hints, swarm reports, and remaining legendary/fossil/evolution needs. It should be pull-based: the player opens it when they want help.

### Next Design Priority

Decision: deepen Full Kanto first.

Implication: Kanto must become the tone-setting 12-15 hour foundation with Red, Blue, Ava, Dax, Rocket, Moonlight, Phoenix, Gold Dust, early rare Pokemon, and a complete Indigo League arc.
