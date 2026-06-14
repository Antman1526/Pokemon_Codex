# Sprout Tower Upper Floor Design

## Purpose

Sprout Tower upper floor is Johto's first real discipline test. The first floor was warning and pressure; the upper floor turns that pressure into a lesson, a rival clash, and the unlock for Falkner.

## Story Design

The Elder lesson is simple: flexibility before force. Sprout Tower bends in storms instead of breaking, and Antman's Johto journey has to learn that same rule before the first badge. Red is still outside, which keeps this as Antman's first solo Johto tradition win while preserving Red as the warm full-game friend waiting for the result.

Silver first battle scene happens immediately after the Elder's lesson. He rejects weakness, challenges Antman, and leaves before admitting the lesson landed. This should become a real trainer battle in the battle-data pass; for this map slice, the scene locks the narrative position and WorldLink state.

Moonlight leaves a cursed bell record behind after the confrontation. It proves the tower is not just haunted or old; somebody is rewriting what the bells mean. Gold Dust is less mystical and more transactional: their archive purchase failed, so they will look for a cleaner market route later. Falkner Gym unlocked is the final payoff. A Violet messenger confirms Zephyr Gym is open and the next WorldLink objective is Falkner.

## Implementation Scope

- Add `MAP_SPROUT_TOWER_UPPER` as a Johto indoor map using `LAYOUT_POKEMON_TOWER_3F`.
- Add a Sprout Tower 1F warp up to `MAP_SPROUT_TOWER_UPPER` and a return warp back to 1F.
- Set `FLAG_SPROUT_TOWER_UPPER_FLOOR_REACHED` on entry.
- Add Elder, Silver, Moonlight record, Gold Dust receipt, and Falkner unlock interactions.
- Advance active progression from `sprout_tower_upper_floor` to `falkner_gym_battle`.
- Keep Hoenn locked and make WorldLink point to Falkner Gym next.
- Tease the Field Checklist page as a story reward without building the full UI yet.

## Acceptance

The scene is complete when the validator sees the upper-floor map, 1F warp, flag, Elder lesson, Silver first battle scene, Moonlight cursed bell record, Gold Dust failed purchase receipt, Falkner Gym unlock, WorldLink updates, build notes, and a replayable engine patch.
