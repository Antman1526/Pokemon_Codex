# Route 12 Snorlax And Fuchsia Arrival Design Spec

## Goal

Turn the Poke Flute reward into a real playable road gate: Antman, Red, and Misty wake the Route 12 Snorlax, WorldLink confirms the Fuchsia road is open, Dax injects rival energy around the encounter, and Fuchsia City becomes the next Kanto destination while Saffron remains visible pressure for a later Silph Co. slice.

## Player Experience

- Antman reaches Route 12 after receiving the Poke Flute from Mr. Fuji.
- Red and Misty stand near the sleeping Snorlax as recurring companions. Red keeps the moment steady; Misty reads the water-road current and warns that the Fuchsia path is safer than rushing Saffron blind.
- The Snorlax event remains classic FireRed structure: ask to use Poke Flute, wake Snorlax, battle level 30 Snorlax, remove the roadblock.
- The text now frames Snorlax as the first field proof that Fuji's gift changes the journey, not just an inventory reward.
- Fuchsia arrival introduces the Safari Zone and Koga as two parallel hooks: catch rare Pokemon under special rules, then prepare for a poison/status gym.
- WorldLink keeps Johto locked and flags Saffron/Silph Co. as rising pressure, not the active route.

## Required Story Markers

- `route12_snorlax_poke_flute_gate`
- `red_misty_snorlax_support`
- `dax_snorlax_rival_pressure`
- `fuchsia_arrival_safari_koga_hook`
- `saffron_pressure_deferred`

## Required WorldLink Markers

- `WL_KANTO_ROUTE12_SNORLAX_AWAKENED`
- `WL_KANTO_FUCHSIA_PATH_OPEN`
- `WL_KANTO_SAFFRON_PRESSURE_DEFERRED`

## Required Rival/Companion Markers

- `route12_snorlax_fuchsia_path`
- `red_snorlax_field_support`
- `misty_fuchsia_current_advice`
- `dax_snorlax_wakeup_report`
- `blue_saffron_impatience_warning`
- `ava_safari_rare_habitat_research`

## Scope Boundary

This slice does not rebalance Koga, implement Safari Zone rewards, unlock Surf/Tide Rider, or resolve Silph Co. It creates the Route 12 road-opening event and first Fuchsia story landing so the next slice can build Safari/Koga deliberately.
