# Ilex Forest First Entry Design

## Purpose

This slice makes Ilex Forest the first Johto route that feels old enough to resist WorldLink. After the Hive Badge, Antman enters a forest where the original Farfetch'd/Cut memory is still present, but the new Nexus story turns it into a Field Tool signal problem. The player should feel movement toward Goldenrod, but not a straight road.

## Proposed Direction

Ilex introduces Field Tool static as a prototype, not the full HM replacement suite. Trail Cutter, Cave Lantern, and future tools are now treated as pieces of a larger Field Tool system, but the full menu waits until Goldenrod where the city can support a proper QoL hub.

Moonlight is the main Ilex threat. They are not stealing Slowpoke or buying routes; they are trying to tune the forest shrine so memory becomes a path. Celebi appears only as a shrine whisper. The player sees that time is involved, but Celebi is not catchable or fully named as an active story partner yet.

Silver helps once without admitting it. He leaves a cut branch and a warning trace, proving he is not simply cruel. Red is present at the forest edge as emotional support, but lets Antman and Silver's tension breathe inside the trees.

Following Pokemon remains a Goldenrod reward. Ilex teases it through a "lead Pokemon reacts" line at the shrine, but does not turn the system on yet.

## Story Beats

- Red checks in at the forest edge and says old forests need quiet more than orders.
- Lyra explains the classic Farfetch'd forest route memory.
- A Farfetch'd blocks the old Cut path while Field Tool static bends the signal.
- Moonlight studies the shrine and treats memory as route control.
- Silver secretly clears part of the path, refuses credit, and leaves no battle.
- Celebi's shrine flickers once and hints that time remembers Antman.
- WorldLink marks Goldenrod City as the next required Johto node and keeps Hoenn locked.

## Systems And Unlocks

- Adds `MAP_ILEX_FOREST` with the Viridian Forest layout.
- Adds `FLAG_ILEX_FOREST_FIRST_ENTRY_REACHED`, `FLAG_ILEX_FIELD_TOOL_STATIC_REACHED`, and `FLAG_ILEX_SILVER_SECRET_ASSIST_REACHED`.
- Advances WorldLink from `ilex_forest_first_entry` to `goldenrod_city_first_arrival`.
- Adds `field_tool_static_prototype` and `following_pokemon_goldenrod_tease`.
- Keeps full Field Tool expansion, following Pokemon, and Goldenrod's QoL hub for later slices.

## Validation

The slice is valid when Ilex Forest is reachable from Azalea, the new flags and map are present, scripts include Red, Lyra, Farfetch'd, Moonlight, Silver, Celebi shrine, and Goldenrod handoff markers, Johto design data records the forest events, and the ROM builds as `NEXUS RED` / `BNRE`.
