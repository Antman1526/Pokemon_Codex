# Rocket Hideout B1F Infiltration Design

Date: 2026-06-14

## Goal

Turn the first Rocket Hideout floor into Kanto's first true criminal infrastructure reveal. The classic Game Corner basement flow stays intact: Antman opens the poster switch, enters the Rocket Hideout, fights grunts, follows the maze, and pushes toward Giovanni and the Silph Scope. The Nexus Red layer adds Red as a warm field companion, a working Portable PC beta terminal, Rocket logistics pressure, and a Gold Dust ledger that proves Celadon's buyer network is feeding off Rocket thefts.

## Creative Direction

Proposed: B1F should feel less like "random basement grunts" and more like the surface of a larger machine. Rocket is not only stealing Pokemon; it is moving crates, prize lists, Silph Scope parts, and region-anchor records through Celadon. Gold Dust does not control the hideout. They are the rich buyer class watching Rocket's mess and converting stolen Pokemon into auctions, pedigree files, and rare-object value.

Proposed: Red appears near the entrance and speaks warmly. He does not solve the hideout for Antman. He reminds Antman to move carefully, calls out the difference between Rocket noise and Gold Dust patience, and frames the Portable PC beta as Bill's practical support for a long journey.

Proposed: Portable PC beta should be functional in this controlled hideout terminal by reusing the existing PC event script. This is not the full portable field menu yet. It is a story-safe prototype that proves storage access can be introduced before the full Act 5 unlock.

## Story Beats

1. Red meets Antman just inside Rocket Hideout B1F and notes that the basement is louder than the Game Corner upstairs.
2. Rocket grunts reveal the hideout is tracking coin flow, Silph Scope parts, and rare prize movement.
3. One terminal opens the PC menu as a Portable PC beta, described as a Bill/Oak/WorldLink field test.
4. A ledger clue mentions Team Gold Dust, the Celadon buyer, pedigree records, and "rare anchors."
5. The final B1F guard still opens the barrier, preserving the original floor progression toward the deeper hideout.

## Scope

Included:

- Add `patches/engine/0020-rocket-hideout-b1f.patch`.
- Add Red object/script near the Rocket Hideout B1F entrance.
- Add a functional Portable PC beta terminal script that calls the existing PC event script.
- Add a Gold Dust ledger clue in B1F.
- Rewrite selected B1F Rocket grunt text around logistics, Gold Dust, Silph Scope, and coin laundering.
- Update Kanto act data, WorldLink messages, rival progression, and build notes.
- Add validator coverage for patch text, design data, WorldLink messages, rival data, and build notes.

Deferred:

- Full Rocket Hideout redesign across all floors.
- Full Portable PC field menu/key item.
- Giovanni team overhaul.
- Gold Dust battle inside the hideout.
- Friends/rematch system.

## Acceptance Criteria

- Rocket Hideout B1F includes a Red companion check.
- Rocket Hideout B1F includes a functional or clearly marked Portable PC beta terminal.
- Rocket Hideout B1F includes a Gold Dust ledger clue.
- Grunt text references Rocket logistics, Silph Scope, coin traffic, and Team Gold Dust pressure.
- Design data includes `rocket_hideout_b1f_infiltration`, `red_hideout_entry_check`, `rocket_coin_logistics`, `gold_dust_ledger_clue`, and `portable_pc_beta_terminal`.
- WorldLink messages include `WL_KANTO_ROCKET_HIDEOUT_B1F`, `WL_KANTO_GOLD_DUST_LEDGER`, and `WL_KANTO_PORTABLE_PC_BETA`.
- Rival progression includes a Rocket Hideout B1F band for Red, Misty, Brock, Blue, Ava, Dax, and Lyra.
- Full validator suite and GBA build pass after replaying all engine patches.
