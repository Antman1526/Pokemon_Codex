# Elm Lab First Visit Design

## Decision

Build Elm Lab as the first Johto interior immediately after New Bark arrival. This keeps WorldLink as a committed journey instead of a region menu: Antman enters New Bark, checks in with Elm, then earns the next road objective.

## Player Experience

Elm welcomes Antman into a temporary playable lab with Red and Lyra present. Lyra gives the first practical Johto route guidance, Red confirms he will walk the first stretch of Route 29 with Antman, and Elm updates the WorldLink checklist with habitat, friendship, and time-of-day notes. Silver remains mysterious: his signal has crossed Route 29, but the player has not met him yet.

## Scope

- Add a real `MAP_NEW_BARK_TOWN_ELM_LAB` interior using Oak Lab's safe FireRed layout.
- Add a New Bark door warp into Elm Lab and a return warp back to New Bark.
- Set `FLAG_ELM_LAB_FIRST_VISIT_REACHED`.
- Update Johto's active objective from Elm Lab to Route 29.
- Keep Hoenn locked.

## Follow-Up

Route 29 should become the next playable Johto route. It should carry Red as field support, Lyra as the Cherrygrove guide handoff, and Silver as a pre-contact shadow rather than an immediate battle.
