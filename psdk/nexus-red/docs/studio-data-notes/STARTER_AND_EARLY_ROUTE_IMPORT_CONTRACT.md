# Starter And Early Route Import Contract

Purpose: preserve Antman's first-partner and early catchability requirements when the Godot reference data is imported into Pokemon Studio / PSDK.

This is a source-of-truth migration contract, not final balance polish. The first PSDK project must import these choices before adding broader Route 1-3 encounter variety.

## Selectable First Partners

Oak's lab must offer 39 selectable first partners:

| Group | Species |
| --- | --- |
| Kanto | Bulbasaur, Charmander, Squirtle |
| Johto | Chikorita, Cyndaquil, Totodile |
| Hoenn | Treecko, Torchic, Mudkip |
| Sinnoh | Turtwig, Chimchar, Piplup |
| Unova | Snivy, Tepig, Oshawott |
| Kalos | Chespin, Fennekin, Froakie |
| Alola | Rowlet, Litten, Popplio |
| Galar | Grookey, Scorbunny, Sobble |
| Paldea | Sprigatito, Fuecoco, Quaxly |
| Special | Eevee, Pikachu, Dratini, Abra, Gastly, Larvitar, Sandile, Kubfu, Staryu, Shroomish, Rockruff, Ralts |

Implementation notes:

- The first 27 entries stay in generation order so the starter selector is predictable.
- The 12 special partners appear after the official starter set.
- Blue must receive a counter-pick from `native/nexus-red/content/starters/starter_choices.json`.
- Ava and Dax must retain their priority-pool assignment behavior.
- The starter event must add the selected species to the player's party immediately and set a story flag equivalent to `starter_chosen`.

## Early Catchability Requirement

All 39 first-partner species must also be catchable before the first major difficulty wall. The first PSDK import uses Routes 1-3 as the migration anomaly cluster.

| Route | Species | Target level band |
| --- | --- | --- |
| Route 1 | Bulbasaur, Charmander, Squirtle, Chikorita, Cyndaquil, Totodile, Eevee, Pikachu, Abra, Gastly, Ralts, Shroomish, Rockruff | 4-5 |
| Route 2 | Treecko, Torchic, Mudkip, Turtwig, Chimchar, Piplup, Snivy, Tepig, Oshawott, Sandile, Staryu, Dratini, Larvitar | 5-6 |
| Route 3 | Chespin, Fennekin, Froakie, Rowlet, Litten, Popplio, Grookey, Scorbunny, Sobble, Sprigatito, Fuecoco, Quaxly, Kubfu | 6-7 |

## Encounter Import Table

Use these rows as the initial PSDK encounter import target.

| Route | Species | Level | Weight | Time |
| --- | --- | ---: | ---: | --- |
| Route 1 | Bulbasaur | 4 | 4 | morning |
| Route 1 | Charmander | 4 | 4 | day |
| Route 1 | Squirtle | 4 | 4 | evening |
| Route 1 | Chikorita | 4 | 3 | morning |
| Route 1 | Cyndaquil | 4 | 3 | day |
| Route 1 | Totodile | 4 | 3 | evening |
| Route 1 | Eevee | 4 | 3 | any |
| Route 1 | Pikachu | 5 | 2 | morning |
| Route 1 | Abra | 5 | 2 | day |
| Route 1 | Gastly | 5 | 2 | night |
| Route 1 | Ralts | 5 | 2 | morning |
| Route 1 | Shroomish | 5 | 2 | morning |
| Route 1 | Rockruff | 5 | 2 | day |
| Route 2 | Treecko | 5 | 3 | morning |
| Route 2 | Torchic | 5 | 3 | day |
| Route 2 | Mudkip | 5 | 3 | evening |
| Route 2 | Turtwig | 5 | 3 | morning |
| Route 2 | Chimchar | 5 | 3 | day |
| Route 2 | Piplup | 5 | 3 | evening |
| Route 2 | Snivy | 5 | 3 | morning |
| Route 2 | Tepig | 5 | 3 | day |
| Route 2 | Oshawott | 5 | 3 | evening |
| Route 2 | Sandile | 6 | 2 | day |
| Route 2 | Staryu | 6 | 2 | evening |
| Route 2 | Dratini | 6 | 1 | night |
| Route 2 | Larvitar | 6 | 1 | night |
| Route 3 | Chespin | 6 | 3 | morning |
| Route 3 | Fennekin | 6 | 3 | day |
| Route 3 | Froakie | 6 | 3 | evening |
| Route 3 | Rowlet | 6 | 3 | morning |
| Route 3 | Litten | 6 | 3 | day |
| Route 3 | Popplio | 6 | 3 | evening |
| Route 3 | Grookey | 7 | 3 | morning |
| Route 3 | Scorbunny | 7 | 3 | day |
| Route 3 | Sobble | 7 | 3 | evening |
| Route 3 | Sprigatito | 7 | 3 | morning |
| Route 3 | Fuecoco | 7 | 3 | day |
| Route 3 | Quaxly | 7 | 3 | evening |
| Route 3 | Kubfu | 7 | 1 | day |

## Balance Rules

- Keep all early migration encounters between levels 4 and 7.
- Keep Dratini, Larvitar, and Kubfu at weight 1 until a later balance pass.
- Do not put all 39 species in every route table; Route 1 must still feel like early Kanto with strange migration sightings.
- Rattata, Pidgey, Caterpie, Weedle, Spearow, Jigglypuff, and Nidoran can remain common local wildlife around these migration slots.
- If PSDK encounter slots require compression, preserve species coverage first, then time-of-day flavor, then exact weight values.

## Verification

The current Godot reference data is verified by:

```bash
python3 tools/validate_native_starter_slice.py
python3 tools/validate_native_early_migration_pool.py
python3 tools/validate_design_data.py
python3 tools/validate_native_platform_strategy.py
```

When the PSDK project is created, add a PSDK-specific validator that compares Studio/PSDK data against this contract.
