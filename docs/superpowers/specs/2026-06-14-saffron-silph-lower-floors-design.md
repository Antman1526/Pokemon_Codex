# Saffron Arrival and Silph Lower Floors Design

## Intent

This slice starts the occupied-Saffron chapter after Koga. The player enters Saffron as a real crisis zone, checks in with Red near Silph, and begins the first three floors of the Silph Co takeover without resolving the full dungeon. The goal is to make Saffron feel larger than a single building raid: Rocket controls the systems, Gold Dust has buyers circling rare-habitat data, Blue is already frustrated, and WorldLink is unstable but still keeping the route Kanto-only.

## Story Beats

- Red appears in Saffron and tells Antman he will split off inside Silph to keep civilians moving while Antman pushes upward.
- The Silph 1F receptionist reframes the lobby as a lockdown checkpoint, not normal corporate welcome text.
- Silph 2F introduces Rocket logistics: teleport tiles are being used as supply routing, not just puzzle gimmicks.
- Silph 3F introduces the Blue pressure clue: Blue came in fast, hit the wrong security layer, and is now somewhere deeper and angry.
- WorldLink records Saffron arrival, lower-floor lockdown, and Silph routing as the next Kanto-only objective.

## Implementation Shape

- Add design markers to `data_design/kanto_chapter.yaml` under `act_5_saffron_fuchsia`.
- Add WorldLink messages for Saffron arrival, Silph lobby lockdown, and lower-floor routing.
- Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax around the lower-floor infiltration.
- Export `patches/engine/0026-saffron-silph-lower-floors.patch` scoped to Saffron City and Silph Co floors 1-3.
- Keep full Portable PC access out of this slice; Silph first explains why the technology is valuable.

## Verification

- `tools/validate_saffron_silph_lower_floors.py` must verify design data, build notes, and patch markers.
- Full validator suite must pass after replaying patches from a clean engine checkout.
- ROM must build as a `.gba` with title `NEXUS RED` and game code `BNRE`.
