# Azalea First Arrival Design

## Intent

Azalea should not open with immediate chaos. The first arrival is a tense quiet scene: the town looks traditional and small, but every local knows the Slowpoke Well is wrong. This gives the player a breath after Union Cave while making the next Rocket crisis feel personal instead of mechanical.

## Story Shape

- Lyra meets Antman at the town edge and says Azalea's silence is not peace.
- Red stays outside the direct crisis and watches the route back to Union Cave, keeping Antman as the lead.
- Kurt appears before the Well as the town's moral center: old, stubborn, and furious that outsiders are treating Slowpoke as inventory.
- Team Rocket is guarding the Well entrance, but Gold Dust is nearby trying to turn the tail market into a legal commodity.
- Bugsy's Gym is visible but blocked until the Well crisis is resolved.
- Apricorn Balls are teased through Kurt now, then unlocked after the Slowpoke Well resolution.

## Player-Facing Content

- Add `MAP_AZALEA_TOWN` as a Johto town reached from Union Cave.
- Add a Union Cave warp into Azalea and an Azalea warp back into Union Cave.
- Add Azalea NPC/object touchpoints for Lyra, Red, Kurt, Rocket, Gold Dust, Bugsy's aide, Silver trace, and the Slowpoke Well lock.
- Add flags for Azalea first arrival, Kurt warning, and Slowpoke Well gate check.
- Advance WorldLink from `azalea_first_arrival` to `slowpoke_well_first_entry`; Hoenn remains locked.

## Systems Notes

- Azalea introduces the first town-specific checklist page: local services, Gym lock, story blocker, Apricorn tease, and next objective.
- This slice does not add Slowpoke Well as a dungeon yet. The next milestone should add the Well map, Rocket scene, Red's optional tag support decision, and the reward path toward Bugsy.
- The first playable ROM remains OpenEmu-compatible as a `.gba` build from replayable engine patches.
