# Falkner Zephyr Gym Design

## Purpose

Falkner / Zephyr Gym is Johto's first badge payoff after Sprout Tower. It should feel earned, calm, and sharp: less punishing than Radical Red, but built around a real Flying-type control lesson.

## Story Design

Red greets Antman after Sprout Tower before the badge challenge. He is warm, proud, and careful not to take over. The scene reinforces that Red is Antman's full-game friend, not a guide rail.

Ava checks in before Falkner because the cursed bell record needs immediate analysis. Her read is that Moonlight is changing route signals through sound, which means Johto's old systems are not just historical flavor; they are live infrastructure. That gives the Gym a reason to matter beyond the badge.

Falkner frames the battle as a Flying-type control lesson. Flying is not raw power here. It is tempo, wind, speed, pivoting, and reading when to bend. The badge scene registers the ZEPHYR BADGE as a story key without reusing Kanto's badge flags yet. The first Field Checklist page unlocks immediately after, giving the player a concrete QoL-style route guide without turning WorldLink into a free-region warp.

Silver does not interrupt the badge battle. He watches the result from outside the city route and leaves silently toward Route 32, which makes him feel more dangerous than another loud rival scene.

## Implementation Scope

- Add `MAP_VIOLET_CITY_GYM` as a Johto indoor map using `LAYOUT_PEWTER_CITY_GYM`.
- Add a Violet City warp into `MAP_VIOLET_CITY_GYM` and return warps back to Violet.
- Set `FLAG_FALKNER_GYM_REACHED` on Gym entry.
- Set `FLAG_ZEPHYR_BADGE_REGISTERED` during the Falkner battle scene.
- Add Red post-tower reunion, Ava bell analysis, Falkner battle scene, Field Checklist unlock, and Route 32 next interactions.
- Advance active progression from `falkner_gym_battle` to `route_32_union_cave_road`.
- Keep Hoenn locked.

## Acceptance

The scene is complete when the validator sees the Violet Gym map, Violet City warp, flags, Red post-tower reunion, Ava analysis, Falkner Flying-type control lesson, ZEPHYR BADGE registered text, Field Checklist page unlocked text, Route 32 next WorldLink text, build notes, and a replayable engine patch.
