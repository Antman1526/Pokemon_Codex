# Union Cave First Entry Design

## Intent

Union Cave becomes Johto's first true enclosed road after Falkner: not a shortcut, not a menu transition, and not a full dungeon finale yet. The player enters from Route 32, sees Rocket remnants and Gold Dust actively fighting over the same passage, gets the first cave-specific Field Checklist page, and learns that Azalea is the next story gate.

## Story Shape

- Lyra enters the mouth of Union Cave with Antman, then frames the cave as the point where Johto stops being purely quiet and pastoral.
- Rocket remnants are using the cave as a supply route toward Slowpoke Well.
- Gold Dust is trying to "legalize" the passage by buying route rights and charging controlled access.
- Red appears only for an emergency WorldLink instability beat, making him feel present without letting him carry every obstacle.
- Silver is not fought here. He leaves a silent exit trace toward Azalea, preserving tension for later.

## Player-Facing Content

- Add `MAP_UNION_CAVE_1F` as a Johto underground map using a stable existing cave layout.
- Add a Route 32 warp into Union Cave and a Union Cave warp back to Route 32.
- Add NPC/object touchpoints for Lyra, Red, Rocket, Gold Dust, Ava's checklist relay, Silver trace, and the blocked Azalea exit.
- Add flags for first entry, cave checklist review, and Red's emergency scene.
- Keep Hoenn locked and set `azalea_first_arrival` as the next required story node.
- After Azalea first arrival is implemented, the same journey chain should continue forward to `slowpoke_well_first_entry`.

## Systems Notes

- Cave Field Checklist should teach the player that cave routes can have repel guidance, darkness/escape rope reminders, and time-sensitive rare encounter notes.
- This slice does not add full wild encounter balancing, cave trainers, or Azalea map content yet. Those belong in the Azalea/Kurt/Slowpoke Well follow-up.
- The first playable ROM remains OpenEmu-compatible as a `.gba` build from replayable engine patches.
