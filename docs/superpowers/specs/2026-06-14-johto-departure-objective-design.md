# Johto Departure Objective Design

## Purpose

This slice turns the Pallet World Circuit Gate from a sendoff into the first active Johto objective. It confirms that Antman has committed to the next region, opens Elm and Lyra as immediate Johto voices, and teases Silver without starting the Elm Lab theft yet.

## Chosen Direction

Proposed: Elm and Lyra speak first because Johto should start warmer than Kanto's rival pressure. Red remains present as Antman's friend and early Johto support, but the player still owns the route. Silver is only a profile tease here; his first physical interruption should happen in the New Bark or Cherrygrove slice.

This creates no Hoenn unlock and does not turn WorldLink into a free travel menu. The next required story node is `new_bark_worldlink_arrival`.

## Contract

- Add `FLAG_JOHTO_DEPARTURE_CONFIRMED`.
- Red's post-sendoff Gate interaction sets the flag once.
- Gate text includes Elm, Lyra, Silver, and the Johto objective.
- Hoenn remains locked.
- Add Johto Act 1 data for New Bark through Violet.
