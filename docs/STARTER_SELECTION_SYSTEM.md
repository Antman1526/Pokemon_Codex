# Pokemon Nexus Red - 39 Starter Selection System

Date: 2026-06-13
Scope: first playable Kanto build and final opening flow

## 1. Goal

The starter scene must sell the game's promise immediately: this is Pallet Town, but the whole Pokemon world is already leaking in. The player can choose from all 27 official regional starters plus 12 special starters before the first Blue battle.

The system must be reliable before it is pretty. A simple FireRed-feeling category menu is better than an ambitious custom UI that blocks the first `.gba` build.

## 2. Starter Count

Total choices: 39.

- 27 official starters across 9 regions.
- 12 special starters: Eevee, Pikachu, Dratini, Abra, Gastly, Larvitar, Sandile, Kubfu, Staryu, Shroomish, Rockruff, Ralts.

## 3. Recommended GBA UI Flow

Use a two-step menu.

Step 1: choose category.

- Kanto
- Johto
- Hoenn
- Sinnoh
- Unova
- Kalos
- Alola
- Galar
- Paldea
- Special A
- Special B
- Special C
- Special D

Step 2: choose one of three Pokemon.

Official categories map cleanly to each region's trio. Special categories use four sets of three:

- Special A: Eevee, Pikachu, Ralts
- Special B: Abra, Gastly, Staryu
- Special C: Shroomish, Rockruff, Sandile
- Special D: Dratini, Larvitar, Kubfu

Why this structure:

- GBA menus stay readable.
- Every page has three choices.
- Special D clearly warns the player these are advanced/high-power starts.
- It avoids a huge single scrolling list.

## 4. Scene Flow

1. Oak explains the World Pokedex Initiative.
2. Oak says the lab prepared regional starter data after Kanto's route anomalies.
3. Red quietly says, "Pick the one you trust."
4. Player opens starter category menu.
5. Player chooses category.
6. Player chooses species.
7. Confirmation prompt: "Begin with {species}?"
8. Starter is created at level 5.
9. Starter receives project origin metadata.
10. Blue chooses a counter-pick.
11. Ava chooses a support/research starter.
12. Dax chooses an offense starter.
13. Blue challenges Antman immediately.

## 5. Starter Metadata

Store:

- selected species,
- selected category,
- starter power band,
- starter original region,
- whether starter is special,
- whether starter is high-power/advanced.

Uses:

- rival dialogue,
- Blue counter-pick,
- Ava/Dax non-duplication,
- WorldLink flavor,
- Pokedex origin note,
- balancing warnings,
- future companion comments.

## 6. Power Bands

### Safe

Most official starters, Eevee, Pikachu, Abra, Gastly, Staryu, Shroomish, Rockruff, Ralts, Sandile.

### High Value

Froakie, Scorbunny, Sprigatito, Fuecoco, Ralts, Dratini, Larvitar, Kubfu.

### Advanced

Dratini, Larvitar, Kubfu.

Advanced starters are allowed because the vision asks for them, but the game should warn the player:

"This Pokemon grows slowly and may make the early journey unusual. Choose it anyway?"

Do not nerf the player's choice. Balance through level caps, early moves, and encounter answers.

## 7. Blue Counter-Pick Logic

Blue's starter should feel like a classic counter without requiring 39 bespoke rival teams.

Recommended rule:

1. If player chooses Grass/Fire/Water official starter, Blue chooses the same region's type advantage starter where possible.
2. If player chooses a non-trio special starter, Blue chooses from a Kanto counter pool based on broad matchup.
3. If matchup is ambiguous, Blue chooses Charmander/Squirtle/Bulbasaur according to a fixed priority that creates a fair first battle.

Examples:

- Player Bulbasaur -> Blue Charmander.
- Player Charmander -> Blue Squirtle.
- Player Squirtle -> Blue Bulbasaur.
- Player Treecko -> Blue Torchic.
- Player Froakie -> Blue Chespin.
- Player Pikachu -> Blue Bulbasaur or Sandile if later data supports it; for opening reliability, Bulbasaur is safer.
- Player Gastly -> Blue Squirtle with an early legal move.
- Player Dratini -> Blue Squirtle or Bulbasaur; avoid Ice/Fairy hard counter in the lab.
- Player Kubfu -> Blue Charmander or Squirtle; do not punish with a Psychic/Fairy counter in battle one.

## 8. Ava Starter Logic

Ava should avoid direct duplication and lean toward research/support.

Priority pool:

- Chikorita
- Popplio
- Sprigatito
- Ralts
- Eevee
- Rowlet

Rule:

- choose the first available priority starter not chosen by player or Blue.
- if all are blocked, choose Chikorita fallback with dialogue explaining Oak had another prepared.

## 9. Dax Starter Logic

Dax should avoid direct duplication and lean toward offense.

Priority pool:

- Cyndaquil
- Torchic
- Chimchar
- Scorbunny
- Fuecoco
- Froakie

Rule:

- choose the first available priority starter not chosen by player, Blue, or Ava.
- if all are blocked, choose Cyndaquil fallback.

## 10. Early Moves Rule

Every starter must be viable at level 5.

Requirements:

- at least one damaging move,
- no broken late-game move at start,
- no softlock-causing move-only setup,
- advanced starters get modest early moves.

Examples:

- Abra cannot start with only Teleport. Give a basic Psychic or Normal damaging move if engine data would otherwise break the start.
- Gastly needs a reliable early damaging move that can hit early route threats.
- Dratini and Larvitar should not start with oppressive coverage.
- Kubfu should be strong but not fully online.

## 11. Lab Presentation

FireRed-first feel:

- Oak's lab remains familiar.
- Use machines, capsules, or data terminals rather than 39 physical Pokeballs.
- Each category can be represented by a "regional starter terminal."
- Special starters use "anomaly candidate terminal."

Suggested layout:

- left side: official regional terminals,
- right side: special anomaly terminal,
- center: Oak, Red, Blue, Ava, Dax.

## 12. Failure Cases to Prevent

- Player exits without starter.
- Rival chooses same species as player unless intentionally allowed.
- Starter has no valid damaging move.
- Starter species not available in engine data.
- Starter category var not set.
- Blue battle starts before party is valid.
- WorldLink receives starter message before starter var exists.
- Special starter confirmation loops incorrectly.

## 13. Acceptance Criteria

The starter system is acceptable when:

- all 39 starters can be selected,
- all starters are level 5,
- all starters have legal usable moves,
- Blue gets a valid non-duplicate starter/counter,
- Ava and Dax get valid non-duplicate starters,
- starter species/category/power band are stored,
- Blue lab battle works after every starter choice,
- save/load after starter choice preserves data,
- OpenEmu smoke test passes.

