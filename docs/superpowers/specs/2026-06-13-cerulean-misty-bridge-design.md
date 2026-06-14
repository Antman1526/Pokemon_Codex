# Cerulean Misty Bridge Design

## Goal

Turn Cerulean into the first city where the long-game companion structure becomes visible. Red should be preparing for the first true tag-battle arc, Misty should become a recurring friend through a story scene after her gym, and Nugget Bridge should stay classic while gaining a Nexus/Rocket layer.

## Surprise Decisions

- First true Red tag battle target: the Rocket/Cerulean bridge arc, not before Misty and not S.S. Anne.
- Misty companion timing: after a separate post-gym Cerulean scene, not immediately inside the badge reward.
- Nugget Bridge: keep the five-trainer bridge classic, but add a Nexus warning and rewrite Rocket's offer around WorldLink recruitment.
- Misty difficulty: mainline hard for the required badge fight, with optional spike content reserved for rematches and challenge modes.

## Player Experience

- Red appears in Cerulean and identifies the bridge as Rocket's next recruitment filter.
- Misty remains the gym leader first. After Antman earns the Cascade Badge, she appears outside as a friend and Cerulean contact.
- Nugget Bridge's Rocket recruiter now knows about Antman's Mt. Moon fossil artifact and tries to recruit him because Rocket wants people who can trigger Nexus responses.
- Red appears on Route 24 to confirm that a real tag battle is coming soon, but he still does not fight gyms for Antman.

## Acceptance Criteria

- `patches/engine/0012-cerulean-misty-bridge-setup.patch` exists and applies after `0011`.
- Cerulean City contains Red and Misty companion objects.
- Misty's city dialogue changes after the Cascade Badge.
- Misty's gym reward points to the city scene without making Misty fight the gym for Antman.
- Route 24 Rocket dialogue references Nexus/WorldLink recruitment.
- Route 24 Red dialogue marks the Rocket bridge arc as the first true Red tag-battle candidate.
- Validation covers the above.
