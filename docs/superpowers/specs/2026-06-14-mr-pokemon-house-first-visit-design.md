# Mr. Pokemon House First Visit Design

## Purpose

Mr. Pokemon's house preserves the classic Johto egg errand, but the scene now reveals that the egg is part of the Nexus story. The visit should feel small, strange, and important: a quiet house at the end of Route 30 where the original Johto storyline suddenly touches Antman's larger nine-region journey.

## Story Design

Mr. Pokemon gives Antman the `Nexus Egg`, explaining that it was found beside Sprout Tower records that should not have left Violet City. Oak physically appears at the house, making the moment feel like the original Gold/Silver story while acknowledging that Antman is already a Kanto Champion-level traveler. Oak's line is the key thesis: the old story is still true, but the map is larger now.

Ava joins through a remote feed from Elm's research network. The Ava remote feed marks the egg as a living WorldLink signal, not just an unusual Pokemon egg. This lets the rival system participate without crowding the house with too many physical characters. Elm's handoff points the player toward Violet City and warns that Sprout Tower records were edited before Antman arrived in Johto.

## Implementation Scope

- Add `MAP_MR_POKEMONS_HOUSE` as an indoor Johto map using `LAYOUT_ROUTE25_SEA_COTTAGE`.
- Connect Route 30 to the house with a simple warp.
- Set `FLAG_MR_POKEMON_HOUSE_FIRST_VISIT_REACHED` on transition.
- Add Mr. Pokemon, Oak, Ava's remote researcher proxy, and Elm handoff NPCs.
- Advance the active story node from `mr_pokemon_house_first_visit` to `violet_city_first_arrival`.
- Keep Hoenn locked; WorldLink can preview danger but cannot skip Johto progression.

## Acceptance

The scene is complete when the validator sees the new map, Route 30 warp, flag, Nexus Egg dialogue, Oak physically appears, Ava remote feed, Violet City handoff, Johto design-data updates, build notes, and a replayable engine patch.
