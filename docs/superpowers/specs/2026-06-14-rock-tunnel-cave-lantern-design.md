# Rock Tunnel Cave Lantern Design

## Goal

Turn Rock Tunnel into the first real HM-replacement proof point while building suspense for Lavender Town and Team Moonlight.

## Creative Direction

Rock Tunnel should feel like a warm adventure crossing that becomes stranger the deeper Antman goes. The player has already earned Thunder Badge and the Trail Cutter prototype, so WorldLink can now light caves through a `Cave Lantern` protocol. Brock appears at the Route 10 Pokemon Center as a practical mentor who trusts Antman and Red. Red appears inside Rock Tunnel as Antman's full-game friend, steadying the mood and pointing out that the darkness is listening. Moonlight remains a mystery signal, not a fully named enemy team reveal.

## Player Experience

- The player should no longer need a Flash user for Rock Tunnel after Thunder Badge.
- Brock should feel friendly, useful, and tied to cave survival without becoming a mandatory guide.
- Red should appear inside Rock Tunnel and sound warmer than classic silent Red.
- The tunnel should hint that Lavender's horror is different from Rocket crime and Gold Dust greed.
- The exit into Lavender should feel ominous but not derail the original Pokemon Tower storyline.

## Route Beats

1. Route 10 Pokemon Center: Brock gives Antman cave-prep advice and says WorldLink registered the Cave Lantern protocol.
2. Rock Tunnel 1F: entering after Thunder Badge automatically sets the existing Flash system flag so the cave is lit.
3. Rock Tunnel 1F: Red explains the Cave Lantern and warns that the tunnel echo repeats words it should not know.
4. Rock Tunnel B1F: a `Moonlight Echo` NPC/phenomenon whispers about dreams, graves, and the tower without naming Team Moonlight as an organization yet.
5. Lavender Town: the boy's ghost dialogue gains a new line tying Pokemon Tower to the same low-light static from Rock Tunnel.

## Systems Boundaries

This milestone uses existing Flash infrastructure by setting `FLAG_SYS_USE_FLASH`; it does not create a new bag item, icon, menu entry, or field-tool UI. That keeps the slice playable and proves the design direction before building the full field-tool interface.

## Implementation Targets

- Add Brock NPC to `Route10_PokemonCenter_1F_Frlg`.
- Add Cave Lantern explanation text that mentions WorldLink, Cave Lantern, Thunder Badge, repel control, and Red.
- Set `FLAG_SYS_USE_FLASH` in `RockTunnel_1F_OnTransition` after `FLAG_BADGE03_GET`.
- Add Red NPC and dialogue to Rock Tunnel 1F.
- Add Moonlight Echo NPC/dialogue to Rock Tunnel B1F.
- Expand Lavender boy ghost dialogue with low-light static foreshadowing.
- Update Kanto chapter data, WorldLink messages, rival progression, and build notes.

## Acceptance Criteria

- `patches/engine/0017-rock-tunnel-cave-lantern.patch` exists and applies after `0016`.
- Rock Tunnel 1F sets `FLAG_SYS_USE_FLASH` after Thunder Badge.
- Route 10 Pokemon Center includes Brock and Cave Lantern text.
- Rock Tunnel 1F includes Red and warm companion text.
- Rock Tunnel B1F includes Moonlight Echo foreshadowing without a full villain reveal.
- Lavender Town references Rock Tunnel low-light static.
- The ROM still builds as `NEXUS RED` / `BNRE`.
