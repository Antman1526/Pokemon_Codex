# Sprout Tower First Floor Design

## Purpose

Sprout Tower 1F is Johto's first indoor tradition test. It should feel quiet, old, and tense, with the original tower concept preserved while the Nexus Egg makes the records feel newly dangerous.

## Story Design

Red stays outside because this is Antman's first solo Johto tradition test. He is still warm and present, but he trusts Antman to enter without him. Inside, Silver appears for a first-floor confrontation, but there is no battle yet. He wants the first real fight to happen higher in the tower, where weakness, pride, and Johto's old lessons matter.

Moonlight is the main threat in this slice. Their pilgrim says the bells are being written over, turning the tower's calm spiritual tradition into a dream-record problem. Gold Dust is present as a secondary pressure: they want clean archives, lineage proof, and ownership language. The Elder points Antman upward and frames the upper floor as the next story gate. This is the Silver first-floor confrontation, but it is not the actual Silver battle.

## Implementation Scope

- Add `MAP_SPROUT_TOWER_1F` as a Johto indoor map using `LAYOUT_POKEMON_TOWER_2F`.
- Add a Violet City warp into Sprout Tower 1F and a return warp back to Violet.
- Set `FLAG_SPROUT_TOWER_FIRST_FLOOR_REACHED` on transition.
- Add Silver, Moonlight, Gold Dust, Elder, and Red-outside-note interactions.
- Advance active progression from `sprout_tower_first_floor` to `sprout_tower_upper_floor`.
- Keep Hoenn locked and make WorldLink point to the tower upper floor.

## Acceptance

The scene is complete when the validator sees the new tower map, Violet warp, flag, Silver no-battle confrontation, Moonlight main threat, Gold Dust archive pressure, Elder upper-floor handoff, Red stays outside, WorldLink updates, build notes, and a replayable engine patch.
