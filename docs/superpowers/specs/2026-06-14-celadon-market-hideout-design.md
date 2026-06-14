# Celadon Market Hideout Design

## Goal

Turn Celadon into Kanto's first bright-city corruption chapter. The original flow stays intact: the player reaches Celadon, hears rumors about the Game Corner, finds the Rocket poster switch, opens the hideout, and can challenge Erika. The Nexus Red layer adds Team Gold Dust's buyer network, Erika as a calm ally against rare Pokemon trafficking, and the first controlled Ability Capsule access point.

## Proposed Direction

Proposed: Gold Dust appears before the Game Corner hideout as a buyer, not a battler. Rocket owns the basement and the visible crime. Gold Dust is more polished: collectors, auction brokers, pedigree records, rare stones, and shiny rumors. They are interested in buying what Rocket steals, but they do not trust Rocket.

Proposed: Erika should not become an exposition machine. She remains gentle and classic, but her post-battle text shows she understands Celadon's plant and perfume trade well enough to notice rare-growth specimens being laundered through the Game Corner economy.

Proposed: Celadon introduces Ability Capsules as a limited Department Store field trial. This gives players meaningful team-tuning before midgame without also opening Nature Mints, Bottle Caps, and EV rooms at the same time.

## Story Beats

1. Celadon Restaurant includes a Team Gold Dust buyer who speaks like a collector, not a thug. The buyer hints that Rocket's stolen Silph Scope and rare Pokemon prizes are being valued as "anchors" for region trade.
2. The Restaurant worker's basement rumor is rewritten to mention Rocket noise under the Game Corner and a Gold Dust buyer asking too many questions.
3. Game Corner NPCs mention unfair odds, rare Pokemon prizes, and Rocket laundering coins into relic purchases.
4. The Rocket poster text gains a WorldLink pulse before the hideout opens, making the classic switch feel connected to the larger journey.
5. The Game Corner Rocket grunt dialogue references Rocket's irritation with Gold Dust buyers.
6. Celadon Department Store 2F gains a scientist vendor who sells Ability Capsules and describes the system as an early trainer-support field trial.
7. Erika's intro stays mostly classic. Her post-battle/TM text points Antman toward the Game Corner if he has not dealt with it and frames Rainbow Badge as a patience/status-control lesson.

## System And Data Impact

- Add `patches/engine/0019-celadon-market-hideout.patch`.
- Add a Gold Dust buyer object/script to `CeladonCity_Restaurant_Frlg`.
- Add an Ability Capsule vendor object/script to `CeladonCity_DepartmentStore_2F_Frlg`.
- Rewrite selected Game Corner text around Rocket, Gold Dust, WorldLink, and the poster switch.
- Rewrite selected Erika text to connect Celadon Gym to the market investigation while preserving the original battle.
- Update Kanto act data with Celadon-specific events.
- Add WorldLink messages for Celadon market readings, Game Corner hideout, Erika's advice, and Ability Capsule access.
- Add a rival progression band for Celadon market pressure.
- Add validator coverage for patch text, data markers, build notes, and the Ability Capsule item.

## Acceptance Criteria

- The patch chain can be replayed from a clean engine checkout.
- The ROM builds as `pokenexusred.gba` with title `NEXUS RED` and game code `BNRE`.
- Celadon Restaurant contains a Team Gold Dust buyer and rumor text.
- Game Corner preserves the Rocket poster/hideout flow while adding WorldLink and Gold Dust pressure.
- Department Store 2F sells `ITEM_ABILITY_CAPSULE`.
- Erika's text references Celadon's rare trade without removing the original Rainbow Badge/TM reward.
- Design validators include this milestone and pass.

## Deferred

- No Gold Dust battle in Celadon yet.
- No full Nature Mint or IV/EV service yet.
- No Rocket Hideout floor redesign in this slice.
- No Game Corner prize table overhaul yet.
