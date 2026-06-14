# Violet City First Arrival Design

## Purpose

Violet City is Johto's first tradition hub and the first place where Antman learns that badges in this region are gated by history, not only strength. The city should feel calm on the surface, but every important NPC points toward Sprout Tower before Falkner.

## Story Design

Sprout Tower before Falkner is the rule of this slice. Falkner is not avoiding the player; he refuses to certify the Zephyr challenge while tower records are unstable. Red physically returns in Violet City after checking Cherrygrove records, giving Antman the warm full-game friendship beat the project needs. Lyra acts as the local guide and explains that Violet is built around bells, school, and flight discipline.

Silver waits at the tower gate and refuses the first battle until the tower makes the choice meaningful. Moonlight studies bell records as dream pressure, while Gold Dust wants tower archives as proof of rare lineage. This keeps Johto's original Sprout Tower identity intact while tying the tower directly to the Nexus Egg, Moonlight, and Gold Dust.

## Implementation Scope

- Add `MAP_VIOLET_CITY` as a Johto outdoor map using `LAYOUT_PEWTER_CITY`.
- Connect Route 30 east to Violet City and Violet west back to Route 30.
- Set `FLAG_VIOLET_CITY_FIRST_ARRIVAL_REACHED` on map transition.
- Add Red, Lyra, Falkner gate, Silver tower warning, Moonlight, Gold Dust, and sign interactions.
- Advance active progression from `violet_city_first_arrival` to `sprout_tower_first_floor`.
- Keep Hoenn locked and make WorldLink explicitly say Sprout Tower is next.

## Acceptance

The scene is complete when the validator sees the new map, Route 30 connection, flag, Red/Lyra/Falkner/Silver/Moonlight/Gold Dust scripts, WorldLink updates, Sprout Tower gate data, build notes, and a replayable engine patch.
