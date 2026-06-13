# Pokemon Nexus Red - GBA/OpenEmu Build Strategy

Date: 2026-06-13
Target player format: `.gba` playable in OpenEmu on macOS
Preferred engine direction: pokeemerald-expansion or a compatible pokeemerald decomp fork

## 1. Platform Decision

Pokemon Nexus Red should stay on the GBA path. That means the project must be built from source into a `.gba` file, then distributed only as a legal patch. OpenEmu can play the final patched `.gba` locally, but the project repository must not contain copyrighted ROM binaries.

Decision: all nine regions must be done as complete, satisfying story chapters. On GBA, this should mean full-feeling curated regional campaigns, not full tile-for-tile recreations of nine retail games. Player-facing visuals should be FireRed-first even if the codebase uses pokeemerald-expansion.

## 2. What OpenEmu Compatibility Means

OpenEmu compatibility should be tested like a release requirement, not assumed.

Minimum rules:

- Output must be a normal GBA ROM file with `.gba` extension.
- Save type must be stable and emulator-friendly.
- Avoid unusual mapper assumptions or emulator-specific hacks.
- Do not require BIOS-only behavior for normal gameplay.
- Day/night should not depend exclusively on real-time clock hardware. Use an in-game clock based on playtime/steps, with RTC support as an optional enhancement if the engine supports it cleanly.
- Keep input simple: D-pad, A/B, Start/Select, L/R.
- Avoid menus that require mouse, keyboard, or touch-style interaction.
- Test new builds in at least one strict emulator and OpenEmu before calling a milestone playable.

## 3. GBA Reality Check

The GBA route is the right emotional fit because the player wants a ROM playable in OpenEmu. It is also the harder technical route.

Big risks:

- GBA ROM space is limited compared with PC fangames.
- All Pokemon through Gen 9 require large species, forms, learnsets, move, ability, icon, cry, and sprite data.
- Nine regions worth of maps, events, music, trainers, and scripts can exceed practical content budgets.
- Following sprites for every Pokemon/form are a huge asset burden.
- A dynamic 10-rival simulation can consume save data and script complexity quickly.
- Mega, Z-Moves, Dynamax, and Tera together can create battle UI and balance problems.

Design response:

- Compress each region to the strongest story route.
- Reuse global system templates.
- Use data tables instead of one-off scripts.
- Phase optional content into postgame or later patches.
- Build one vertical slice first and prove the ROM remains stable.

## 4. Region Compression Policy

Each region should include enough content to feel authentic without copying every map.

Every region gets:

- Starting arrival hub.
- 4-6 major towns/cities.
- 6-10 routes or equivalent traversal zones.
- 2-4 iconic dungeons/landmarks.
- All region gym leaders/trials represented.
- Main villain arc.
- One legendary climax.
- One rival milestone chain.
- One regional mechanic spotlight.
- Optional postgame expansion hooks.

Each region may cut:

- Redundant short routes.
- Duplicate interiors.
- Non-critical houses.
- Low-value side NPCs.
- Repeated tutorial spaces.
- Minor backtracking.

Proposed pacing: a region should feel like a strong 5-10 hour RPG chapter, not a whole standalone 25-hour game. The complete game can still be very long because there are nine chapters, a final tournament, and postgame loops.

## 5. Long Game Length Target

Target total playtime:

- Main story only: 70-100 hours.
- Main story plus major side quests: 110-150 hours.
- Completionist/postgame: 180+ hours.

Do not create length through grinding. Length should come from:

- meaningful battles,
- rival competition,
- region-specific mechanics,
- optional legendary quests,
- rematches,
- team-building choices,
- exploration rewards,
- Pokedex completion,
- postgame facilities.

## 6. Chapter Build Order

### Milestone 0 - Engine Proof

Goal: build a `.gba` from source and boot it in OpenEmu.

Deliverables:

- clean source checkout/fork,
- local build notes,
- no ROM binaries committed,
- generated `.gba` ignored by git,
- OpenEmu smoke test,
- save/load smoke test.

Current local status:

- `pokeemerald-expansion` is added as a git submodule at `engine/pokeemerald-expansion`.
- `libpng` and `pkg-config` are available through Homebrew.
- Baseline build currently cannot produce a `.gba` because `devkitARM` / `arm-none-eabi-*` tools are not installed.
- Next required local setup step is devkitPro/devkitARM installation.

### Milestone 1 - Kanto Nexus Vertical Slice

Scope:

- Pallet Town,
- Route 1,
- Viridian City,
- Route 2,
- Viridian Forest,
- Pewter City,
- Brock Gym,
- first Rocket anomaly event.

Systems:

- 39-choice starter prototype,
- three starting rivals,
- WorldLink notifications,
- $100,000 start,
- running/bike from beginning,
- early route rare encounter policy,
- Infinite Repel,
- first level cap,
- expanded Pokecenter prototype.

### Milestone 2 - Full Kanto

Scope:

- 8 gyms,
- Team Rocket expansion,
- Pokemon Tower Moonlight event,
- Celadon Gold Dust event,
- Cinnabar Phoenix event,
- Silph Co. Nexus foreshadowing,
- Indigo League,
- Kanto rematches.

### Milestone 3 - Johto Bridge

Scope:

- condensed Johto,
- Silver rival chain,
- Radio Tower,
- Burned Tower/Bell Tower,
- Ho-Oh/Lugia anomaly,
- day/night deepening.

### Milestone 4 - Hoenn Climate Arc

Scope:

- weather-first Hoenn route,
- Magma/Aqua conflict,
- Devon/Weather Institute,
- dive/water traversal,
- Rayquaza climax,
- expanded fishing.

### Milestone 5 - Sinnoh/Hisui Myth Arc

Scope:

- Mt. Coronet,
- lake guardians,
- Galactic,
- Phoenix ancient revival,
- Hisui flashback instances,
- Giratina/Distortion event.

### Milestone 6 - Unova Public Conflict

Scope:

- Castelia,
- Plasma split,
- N arc,
- Rocket/Gold Dust market,
- truth/ideals choice,
- battle facility seed.

### Milestone 7 - Kalos Beauty and Weapon Arc

Scope:

- Lumiose,
- Mega Evolution,
- Flare,
- AZ,
- ultimate weapon,
- customization expansion.

### Milestone 8 - Alola Wormhole Arc

Scope:

- island challenge structure,
- Skull/Aether,
- Z-Moves,
- Ultra Beast bosses,
- wormhole travel events.

### Milestone 9 - Galar Energy Arc

Scope:

- stadium gyms,
- Marnie/Hop/Bede chain,
- Macro Cosmos,
- Rocket betting ring,
- Dynamax restricted to power spots,
- Eternatus theft.

### Milestone 10 - Paldea Final Reveal

Scope:

- Academy hub,
- Team Star,
- Titans,
- Area Zero,
- Tera,
- Phoenix/Nexus final setup.

### Milestone 11 - World Nexus Championship

Scope:

- champion ladder,
- 10-rival tournament,
- villain invasion,
- Meridian Engine dungeon,
- final boss,
- postgame unlocks.

## 7. Save Data Strategy

Rival and world systems must be careful with persistent state.

Save data should track:

- current region,
- chapter progress,
- region badge/trial clear flags,
- rival chapter state,
- rival relationship values,
- pending WorldLink notification bitset,
- major villain state,
- unlocked transit locations,
- difficulty settings,
- Nuzlocke settings,
- caught/seen data,
- postgame facility progress.

Recommendation: do not simulate full rival parties and inventories in save data. Store rival progress IDs and generate teams from templates.

## 8. Content Budget Strategy

Use "content templates" to make the game big without making it fragile:

- trainer class templates,
- gym rematch templates,
- rival team templates,
- mart inventory tiers,
- Pokecenter service scripts,
- regional encounter table patterns,
- villain admin encounter templates,
- legendary trial templates,
- transport unlock templates.

Avoid writing every event as a unique one-off. One-off scripting is where giant ROM hacks become hard to maintain.

## 9. OpenEmu Test Gates

Every playable milestone should pass:

- boots to title,
- starts new game,
- saves,
- closes and reloads save,
- opens WorldLink,
- enters/exits Pokemon Center,
- enters a battle,
- wins/loses a battle,
- changes map,
- receives a notification,
- uses a key item,
- no obvious audio failure,
- no broken text boxes,
- no crash after 30 minutes of play.

## 10. Hard Design Calls

Proposed:

- GBA remains the required target.
- Regions are compressed but story-faithful.
- Kanto gets the most complete treatment.
- Later regions are built as premium chapters, not full retail remakes.
- OpenEmu compatibility is a release gate.
- The first real build goal is a Kanto `.gba` vertical slice, not all nine regions at once.
