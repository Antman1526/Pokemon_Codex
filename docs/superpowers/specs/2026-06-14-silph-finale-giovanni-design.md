# Silph Finale and Giovanni Design

## Intent

This slice completes the occupied-Saffron chapter without rushing into another region. Silph 8F-11F becomes the upper-floor payoff to every earlier clue: Rocket uses systems, Gold Dust buys what Rocket steals, Red protects people without stealing Antman's boss moment, Giovanni sees Silph as an infrastructure prototype, and the restored Master Ball project causes Team Moonlight's next signal to bloom around Sabrina's Gym.

## Story Beats

- Silph 8F shows that Gold Dust still has no uniformed presence in the tower; they are the buyer network waiting for Rocket to deliver Master Ball specifications and rare-route records.
- Silph 9F turns the healing room into an emergency hub. This keeps the long dungeon friendly-mainline-hard instead of punishing, and it reinforces that Silph employees are actively surviving the occupation.
- Silph 10F adds Red at the final stair. Red reaches the final stair, confirms the civilians are moving, and tells Antman that Giovanni is his fight. Red stays warm and talkative but does not help in boss battles.
- Silph 11F reframes Giovanni's original business proposition. Giovanni calls Silph the first Meridian Gate: a proof that storage, capture tech, badges, rare habitats, and region routes can be lined up into one controllable network.
- The Master Ball is a responsibility, not a trophy. The President gives it as emergency trust, warns that Gold Dust would turn it into an auction crown, and says WorldLink is now stable enough to guide Antman toward Sabrina.
- Sabrina becomes the next required Kanto chapter. The Silph network is restored, but Moonlight pressure reacts to it from Saffron Gym.

## Implementation Shape

- Add design markers to `data_design/kanto_chapter.yaml` under `act_5_saffron_fuchsia`.
- Add WorldLink messages for upper floors, Red's boardroom check, Giovanni's Meridian Gate reveal, Master Ball restoration, and the Sabrina/Moonlight handoff.
- Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax after the Silph finale.
- Add a Red object to Silph 10F with `SilphCo_10F_EventScript_RedBoardroomCheck`.
- Rewrite selected Silph 8F-11F text while preserving the original map flow, Giovanni battle, Master Ball reward, and post-battle Rocket cleanup flags.
- Export `patches/engine/0028-silph-finale-giovanni.patch` scoped to Silph 8F-11F only.

## Verification

- `tools/validate_silph_finale_giovanni.py` must verify design data, build notes, and patch markers.
- Full validator suite must pass after replaying patches from a clean engine checkout.
- ROM must build as a `.gba` with title `NEXUS RED` and game code `BNRE`.
