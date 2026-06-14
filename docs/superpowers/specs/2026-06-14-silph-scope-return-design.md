# Silph Scope Return Design Spec

## Goal

Make the return to Lavender Tower after Giovanni feel like a major Kanto story payoff: the Silph Scope reveals the truth, Red supports Antman through the Marowak scene, Mr. Fuji turns the rescue into the Poke Flute route unlock, and WorldLink frames the next branch toward Snorlax, Fuchsia, and Saffron without unlocking another region early.

## Player Experience

- Antman returns to Pokemon Tower with the Silph Scope after defeating Giovanni.
- Red is present on the sixth floor as a warm full-game friend, not a gym-battle crutch.
- The Marowak event keeps the classic FireRed structure, but the text clarifies that the Silph Scope reveals grief while Team Moonlight listens to what grief leaves behind.
- Rocket grunts on the seventh floor now react to Antman arriving with the Scope and imply Rocket wanted to weaponize proof, not ghosts.
- Mr. Fuji's home reward becomes a clear route-forward beat: the Poke Flute opens Snorlax roads, Fuchsia becomes reachable, and Saffron/Silph Co. pressure is building.

## Required Story Markers

- `silph_scope_tower_return`
- `red_marowak_grief_support`
- `marowak_spirit_calmed`
- `fuji_poke_flute_route_open`
- `snorlax_path_objective`
- `saffron_fuchsia_branch_warning`

## Required WorldLink Markers

- `WL_KANTO_MAROWAK_CALMED`
- `WL_KANTO_POKE_FLUTE_ROUTE_OPEN`
- `WL_KANTO_SAFFRON_FUCHSIA_BRANCH`

## Required Rival/Companion Markers

- `silph_scope_lavender_return`
- `red_marowak_grief_support`
- `misty_tower_aftercare_call`
- `brock_fuji_route_call`
- `blue_tower_pressure_reconsidered`
- `ava_marowak_signal_research`
- `dax_snorlax_training_report`
- `lyra_poke_flute_locked_profile`

## Scope Boundary

This slice does not implement Snorlax battles, Fuchsia, Saffron, or full Portable PC. It only makes the Silph Scope return and Poke Flute unlock legible, emotional, and testable.
