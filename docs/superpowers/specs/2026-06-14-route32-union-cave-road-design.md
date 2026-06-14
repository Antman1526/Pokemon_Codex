# Route 32 Union Cave Road Design

## Purpose

Route 32 is the first road after Johto's first badge. It should feel wider than the early errand routes: more habitat variety, clearer route guidance, and the first hint that Azalea's slow Rocket story is already moving under the surface.

## Story Design

Field Checklist becomes route-specific here. It is still implemented as story text in this slice, but it behaves like a real feature promise: active objective, habitat notes, time-of-day hooks, and safe next steps. This keeps the player oriented without turning WorldLink into a free travel menu.

Lyra physically guides Route 32 because Red should not be the answer to every road. Red stays in Violet and calls in as backup, reinforcing that he is Antman's full-game friend while still letting Johto's local cast matter.

Silver does not appear physically. His absence is the point: WorldLink catches a trace moving toward Union Cave, with no battle and no speech. Gold Dust pressures the route first with a toll/ownership angle, trying to turn a public road into a clean transaction. Rocket is teased at Union Cave as the next active enemy pressure, setting up the original Johto Slowpoke Well arc without rushing it.

Mareep, Wooper, and Togepi are hinted through the checklist and route dialogue. This keeps classic Johto identity visible immediately after Falkner while saving full encounter-table balancing for a dedicated wild-data pass.

## Implementation Scope

- Add `MAP_ROUTE32` as a Johto route using `LAYOUT_ROUTE3`.
- Add a Violet City connection to `MAP_ROUTE32` and a Route 32 connection back to Violet City.
- Set `FLAG_ROUTE32_FIRST_STEPS_REACHED` on entry.
- Set `FLAG_ROUTE32_FIELD_CHECKLIST_REVIEWED` from the route checklist interaction.
- Add Lyra road guide, Red Violet backup call, Field Checklist, Silver trace, Gold Dust toll, and Rocket Union Cave scripts.
- Advance active progression from `route_32_union_cave_road` to `union_cave_first_entry`; the player-facing handoff is `Union Cave next`.
- Keep Hoenn locked.

## Acceptance

The scene is complete when the validator sees the Route 32 map, Violet connection, Route 32 flags, Lyra physical guide, Red backup call, Field Checklist route page, Mareep/Wooper/Togepi hints, Silver trace with no battle, Gold Dust toll pressure, Rocket Union Cave tease, WorldLink updates, build notes, and a replayable engine patch.
