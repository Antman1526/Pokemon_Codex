# Route 11 Diglett Bridge Design

## Goal

Build the first post-Surge travel bridge so the player feels Kanto opening up without making WorldLink a quick-jump region menu.

## Creative Direction

Route 11 becomes a rival-race checkpoint. Blue is ahead and loud about it, Red stays warm and practical, and Diglett's Cave becomes the first place where the Trail Cutter prototype reacts to terrain. The player is not sent to Johto, Lavender, or Celadon yet. Instead, the game teaches that WorldLink detects future routes before those routes are safe.

## Player Experience

- After Thunder Badge, Route 11 should feel active instead of empty.
- Blue should be visible as a rival racing ahead, but this slice should not add another mandatory Blue battle.
- Red should talk like Antman's full-game friend: warm, observant, and useful without stealing gym victories.
- Diglett's Cave should preview expanded field-tool logic through story text, not claim the full HM replacement system is complete.
- The Route 11 gate should point the player toward the next real route: back through Cerulean toward Rock Tunnel.

## Route Beats

1. Blue appears on Route 11 and frames the route as a race toward the next Kanto mystery.
2. Red appears near the Diglett's Cave side of Route 11 and explains that Trail Cutter is pinging underground movement.
3. Diglett's Cave's old man explains that the cave is not a region shortcut. It is a natural tunnel that lets WorldLink compare underground routes.
4. The Route 11 east gate guard gives a checklist-style hint: clear Route 11 trainers, inspect Diglett's Cave, return toward Cerulean, prepare for Rock Tunnel.
5. WorldLink planning data records new rival and companion updates for Blue, Red, Brock, Ava, Dax, and Lyra.

## Systems Boundaries

This milestone remains text/script-first. It does not add real Trail Cutter collision behavior, new Dig mechanics, or new map gating. Those should come after the story has established field tools clearly enough to test.

## Implementation Targets

- Add Route 11 Red and Blue NPC objects.
- Add Route 11 scripts/text for Red's Trail Cutter guidance and Blue's rival-race pressure.
- Update Diglett's Cave South Entrance old man text.
- Update Route 11 East Entrance guard text with a clear next-step checklist.
- Update Kanto chapter data, WorldLink message data, and rival progression data.
- Add a validator that fails until all markers are present.

## Acceptance Criteria

- `patches/engine/0016-route11-diglett-bridge.patch` exists and applies after patches `0001` through `0015`.
- Route 11 map has Red and Blue NPC objects with scripts.
- Route 11 scripts mention `Trail Cutter`, `WorldLink`, `Blue`, `Rock Tunnel`, and `Diglett's Cave`.
- Diglett's Cave South Entrance explains that the tunnel is not a region shortcut.
- Route 11 East Entrance guard gives a checklist-style Rock Tunnel handoff.
- Design data includes Route 11, Diglett's Cave, WorldLink messages, and rival progression.
- The ROM still builds as `NEXUS RED` / `BNRE`.
