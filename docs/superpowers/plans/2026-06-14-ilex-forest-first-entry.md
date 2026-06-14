# Ilex Forest First Entry Implementation Plan

## Steps

1. Add a failing validator for Ilex Forest first entry.
2. Update Johto chapter data, WorldLink messages, rival progression, and build notes.
3. Add `MAP_ILEX_FOREST`, Azalea-to-Ilex travel, and Ilex event flags in the engine patch.
4. Export `patches/engine/0056-ilex-forest-first-entry.patch`.
5. Replay the full engine patch stack from a clean engine.
6. Run every validator.
7. Build the FireRed target ROM as `NEXUS RED` with game code `BNRE`.
8. Verify the `.gba` header and clean the nested engine before committing.

## Design Decisions

- Field Tool static appears now as a prototype; the full Field Tool suite waits until Goldenrod.
- Celebi is teased through a shrine whisper, not a catchable event.
- Moonlight is the main Ilex antagonist.
- Silver helps once without admitting it and does not battle.
- Following Pokemon is teased but saved for Goldenrod.
