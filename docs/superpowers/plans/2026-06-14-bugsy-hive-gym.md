# Bugsy Hive Gym Implementation Plan

## Steps

1. Add a failing validator for the Bugsy Hive Gym slice.
2. Update Johto design data, WorldLink messages, rival progression, and build notes.
3. Add `MAP_AZALEA_GYM`, the Azalea-to-Gym warp, and the Bugsy/Hive/Apricorn flags in the engine patch.
4. Export `patches/engine/0055-bugsy-hive-gym.patch`.
5. Replay the full engine patch stack from a clean engine.
6. Run every validator.
7. Build the FireRed target ROM as `NEXUS RED` with game code `BNRE`.
8. Verify the `.gba` header and clean the nested engine before committing.

## Design Decisions

- Bugsy opens with a short swarm lesson instead of a plain gym room.
- Kurt gives a limited first-batch Apricorn reward before the gym.
- Red is present as a warm full-game friend but does not assist in gym battles.
- Silver appears after the Hive Badge as an Ilex Forest pressure trace without a battle.
- Johto Rematch Board tier 1 becomes live after the Hive Badge.
