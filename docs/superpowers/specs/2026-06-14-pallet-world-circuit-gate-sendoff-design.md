# Pallet World Circuit Gate Sendoff Design

## Purpose

This slice turns Oak's World Circuit Passport reward into a committed departure beat. It gives Antman a visible Pallet sendoff with Red, Misty, Brock, and Blue after Kanto's Hall of Fame proof, while keeping the full New Bark Town arrival for the next implementation slice.

## Chosen Direction

Proposed: Red leads the sendoff because he is Antman's full-game friend, not a silent cameo. Misty validates the sea route, Brock checks supplies and tower readiness, and Blue appears briefly with pressure that is quieter than his earlier jealousy. Lyra speaks through WorldLink from New Bark Town so Johto feels alive before the player sees it.

The scene must explicitly say this is not a quick region menu. WorldLink can confirm that New Bark Town is stable, but there is no direct Johto warp in this slice. The actual region handoff should happen in a later New Bark arrival slice.

## Implementation Contract

- Add Pallet companion objects for Red, Misty, Brock, and Blue.
- Hide those objects until `FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT` is set.
- Use `FLAG_USED_WORLD_CIRCUIT_GATE_SENDOFF` to make Red's full scene one-time.
- Let each companion keep a repeatable short line afterward.
- Do not add a Johto map warp yet.
- Update design data so Kanto act 7 now includes the gate sendoff as a distinct beat after Oak's Passport ceremony.

## Tone

Warmer adventure. Red is reassuring and talkative. Misty is confident and perceptive. Brock is practical. Blue is still competitive, but the loss to Antman changed the edge of his dialogue.
