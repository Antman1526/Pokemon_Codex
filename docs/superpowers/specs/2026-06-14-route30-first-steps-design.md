# Route 30 First Steps Design

## Decision

Route 30 is Johto's first trainer-road pressure test. It should be more active than Route 29, but still not a difficulty spike after Kanto Champion status.

## Player Experience

Lyra walks the road physically and frames Route 30 as the first place Johto expects Antman to read trainers, routes, and rumors at the same time. Red is not physically present; he uses a WorldLink check-in so the companion system feels broader than one follower sprite. A Gold Dust scout watches Sprout Tower records from the roadside, while a Moonlight pilgrim hints that the tower's bells are dreaming wrong. Silver battle waits until Sprout Tower; on Route 30, his absence should feel intentional. The road ends by pointing Antman toward Mr. Pokemon's house.

## Scope

- Add playable `MAP_ROUTE30` using Route 3's safe FRLG layout.
- Connect Cherrygrove east to Route 30 and Route 30 west to Cherrygrove.
- Set `FLAG_ROUTE30_FIRST_STEPS_REACHED`.
- Add Lyra road support, Red WorldLink check-in, trainer-road pressure, Gold Dust scout, Moonlight pilgrim, and Mr. Pokemon objective text.
- Advance WorldLink from Route 30 to `mr_pokemon_house_first_visit`.
- Keep Hoenn locked.

## Follow-Up

Mr. Pokemon's house should become the next small hub. It should pay off the original Johto errand, give Elm a reason to escalate toward Violet, and plant the first concrete clue that Sprout Tower's records are being edited.
