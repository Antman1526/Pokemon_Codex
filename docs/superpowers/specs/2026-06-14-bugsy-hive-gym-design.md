# Bugsy Hive Gym First Challenge Design

## Purpose

This slice turns the Slowpoke Well rescue into Azalea's recovery beat and opens Bugsy's Gym as the next Johto badge objective. The player should feel that Azalea is breathing again, but Johto is not returning to normal: Rocket's return is public, Gold Dust has learned how to profit from public damage, and Silver is studying Antman's choices before Ilex Forest.

## Proposed Direction

Bugsy does not open with a normal gym lobby. He starts with a short swarm lesson: Rocket did not beat Azalea with strength, but with coordinated pressure. Bugsy reframes Bug-type strategy as rhythm, priority, and group positioning, which makes the Hive Badge feel mechanically distinct from Falkner's wind-control lesson.

Kurt gives Antman a first-batch Apricorn reward before the gym. This is not the full Apricorn Ball system yet; it is a proof of trust and a reminder that Johto's old craft serves Pokemon first. The full repeatable Apricorn menu remains a later Goldenrod/Johto system.

Red appears in the gym as Antman's friend but respects the gym boundary. He can talk and encourage, but he cannot help with the badge fight. Silver appears only as an Ilex-side pressure trace after the badge, keeping his next real conflict for the forest road.

## Story Beats

- Bugsy's aide confirms the town emergency is over and the gym is open.
- Kurt thanks Antman with a first-batch Apricorn set and warns that tools become dangerous when they become status symbols.
- Red says he will watch and train afterward, but this badge belongs to Antman.
- Bugsy teaches that a swarm is coordination, not chaos, and registers the Hive Badge.
- Silver refuses a post-gym battle and moves toward Ilex Forest.
- WorldLink marks Ilex Forest as the next required Johto node and keeps Hoenn locked.

## Systems And Unlocks

- Adds `MAP_AZALEA_GYM` with FireRed-compatible gym layout.
- Adds `FLAG_BUGSY_GYM_REACHED`, `FLAG_HIVE_BADGE_REGISTERED`, and `FLAG_APRICORN_FIRST_BATCH_RECEIVED`.
- Advances WorldLink state from `bugsy_gym_challenge` to `ilex_forest_first_entry`.
- Promotes Johto Rematch Board tier 1 from tease to live after the Hive Badge.
- Keeps full Apricorn crafting, deeper Field Tool expansion, and real companion rematches for later systems.

## Validation

The slice is valid when the patch stack can add Azalea Gym from a clean engine, the new map sets the Bugsy/Hive/Apricorn flags, Johto design data contains the recovery events, WorldLink messages include Hive Badge and Ilex handoff alerts, and the ROM builds as `NEXUS RED` / `BNRE`.
