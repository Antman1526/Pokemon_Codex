# Cherrygrove First Arrival Design

## Decision

Cherrygrove is a friendly guide with surveillance tension. It should feel like a safe Johto town at first, then reveal that Johto's oldest travel customs already work like a quiet WorldLink network.

## Player Experience

Red checks in warmly and lets Antman breathe after Route 29. Lyra welcomes Antman to the first real Johto checkpoint and explains that local guides remember every traveler. The Cherrygrove guide rewards exploration with Map Card access and an Apricorn Case tease, but his wording makes it clear he is also part of an old guide network that watches unusual routes. Silver warning: he gives his first direct warning without a battle, saying he sees Antman following maps and companions instead of instinct. A Gold Dust receipt points toward old tower records, keeping Ecruteak and Sprout Tower pressure alive without rushing the player.

## Scope

- Add playable `MAP_CHERRYGROVE_CITY` using Viridian City's safe FRLG layout.
- Connect Route 29 north to Cherrygrove and Cherrygrove south to Route 29.
- Set `FLAG_CHERRYGROVE_FIRST_ARRIVAL_REACHED`.
- Add Red, Lyra, Guide, Silver, and Gold Dust receipt interactions.
- Advance WorldLink from Cherrygrove to `route_30_first_steps`.
- Keep Hoenn locked.

## Follow-Up

Route 30 should introduce Johto's first trainer road and Mr. Pokemon's house setup. It should also decide whether Silver's first battle happens on Route 30 or waits until Sprout Tower.
