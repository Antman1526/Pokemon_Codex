# Sabrina Moonlight Gym Design

## Intent

This slice makes Sabrina the emotional aftermath of Silph rather than a disconnected sixth badge. Saffron is physically free, but the restored Silph network has made the city's psychic signal loud enough for Team Moonlight to touch. The Gym stays true to the original warp-maze structure and Sabrina remains the Gym Leader, not a villain. Moonlight is an interference layer pressing on dreams, mirrors, and the player's sense of direction.

## Story Beats

- Red and Misty appear outside Saffron Gym after Silph. Red cannot enter with Antman because the Gym rejects companion resonance; he stays warm and direct, framing this as Antman's psychic trial.
- Misty steadies the city outside. She reads the Moonlight interference like water under moonlight and tells Antman to move carefully rather than rush the maze.
- Inside the Gym, a Moonlight Veil interaction near the entrance warns that the warp tiles are repeating more than space. This keeps WorldLink guidance present without turning the Gym into a tutorial.
- Sabrina keeps the classic battle flow, but her text acknowledges that her vision has been contaminated by grief static from Lavender and the restored Silph network.
- The Marsh Badge stabilizes Saffron's psychic signal. WorldLink stays Kanto-locked and points the next route toward Cinnabar/Phoenix foreshadowing.

## Scope Choice

This slice does not rebalance Sabrina's team or implement a Portable PC key item. It focuses on story, map scripting, and route clarity. Sabrina team tuning should happen with the late-Kanto level curve in the next combat pass.

## Implementation Shape

- Add Red and Misty objects to Saffron City near the Gym with post-Silph/pre-Sabrina and post-Sabrina dialogue.
- Add a Moonlight Veil background interaction to Saffron Gym.
- Rewrite Sabrina, Gym Guy, selected trainer, sign, and TM text around Moonlight distortion while preserving battle and reward scripts.
- Add design data, WorldLink messages, rival/companion progression, build-note smoke checks, and `0029-sabrina-moonlight-gym.patch`.

## Verification

- `tools/validate_sabrina_moonlight_gym.py` must verify design data, build notes, and patch markers.
- Full validator suite must pass after replaying patches from a clean engine checkout.
- ROM must build as a `.gba` with title `NEXUS RED` and game code `BNRE`.
