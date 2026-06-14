# Vermilion Misty Surge Refinement Design

Date: 2026-06-14

## Goal

Refine the existing Vermilion/S.S. Anne/Lt. Surge milestone to match the approved direction: Misty should lead the pre-Surge training scene, Rocket sabotage should still happen before the true Gym battle, Trail Cutter should be introduced as an early prototype, and Gold Dust should leave a mysterious Fan Club clue that points toward Celadon without overexplaining the organization.

## Design

Misty-led Surge prep becomes the emotional and tactical bridge after the S.S. Anne crisis. Red remains the full-game friend and field companion, but Misty owns this moment because she understands currents, pressure, and the danger of meeting electricity head-on. Her harbor dialogue now tells Antman to ground the voltage, cut the route, and win the badge his way. She does not assist inside the Gym battle; the badge remains the player's achievement.

The Rocket grid sabotage remains mandatory before Surge. The sabotage payoff now confirms Misty was right, making her prep scene mechanically relevant without adding a tag battle or changing Surge's team in this refinement.

Trail Cutter remains a prototype. Surge's reward text confirms the field-tool path is waking up, while the full HM replacement system is still pending. This preserves the long-game HM replacement arc and avoids pretending the system is complete before the Route 11/Diglett's Cave calibration.

The Fan Club clue is made stranger and less direct. Instead of naming a Gold Dust collector openly, the club now mentions a gold lapel pin, a blank auction card, a Celadon stamp, and a dust mark. This preserves mystery while still guiding the player toward the Celadon buyer arc.

## Scope

Included:

- Update Misty's post-S.S. Anne Vermilion dialogue into a Surge prep scene.
- Update the Gym sabotage payoff to reference Misty's advice.
- Update Surge's Trail Cutter text to name the full HM replacement system as pending.
- Update the Fan Club Gold Dust clue to be mysterious.
- Update Kanto design data, WorldLink message planning, rival progression, build notes, and validator coverage.

Not included:

- No new Lt. Surge team tuning.
- No new Misty tag battle.
- No full HM replacement implementation.
- No new rival rematch or Friends system.

## Acceptance

- `validate_vermilion_misty_surge_refinement.py` passes after patches are applied.
- Full patch replay applies cleanly through `0032`.
- Existing validators still pass.
- The ROM builds with title `NEXUS RED` and game code `BNRE`.
