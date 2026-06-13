# Pokemon Nexus Red - WorldLink System Spec

Date: 2026-06-13
Target: GBA/OpenEmu, FireRed-first UI

## 1. Purpose

WorldLink is the signature system that makes Pokemon Nexus Red feel alive. It connects rival progress, companion updates, villain alerts, rare Pokemon sightings, travel unlocks, daycare notes, rematches, and the optional Pokedex checklist.

It should not feel like a smartphone. It should feel like a FireRed-era trainer device upgraded by Professor Oak and Silph technology for the World Pokedex Initiative.

## 2. Core Design Rules

- Keep text short.
- Batch minor updates.
- Do not interrupt battles or dungeons with low-priority messages.
- Major alerts can pop when safe.
- Every notification should either add flavor, point to content, or show rival/world movement.
- WorldLink is useful when ignored and rewarding when checked.
- The Pokedex checklist is optional and pull-based.

## 3. Unlock Flow

WorldLink is received from Professor Oak after starter selection and the Blue lab battle.

Opening state:

- Rival Feed unlocked.
- Alerts unlocked.
- Red Notes unlocked.
- Settings unlocked.

Unlock later:

- Pokedex Checklist: after Brock as beta, expanded after Kanto League.
- Companion Log: after Red's Route 1 companion beat.
- Rematch Board: after Misty or Vermilion.
- Daycare Remote: after first daycare access.
- Transit Pass: after Kanto League.
- Anomaly Tracker: after Rayquaza/Hoenn.

## 4. Main Menu

WorldLink top-level menu:

1. Feed
2. Rivals
3. Companions
4. Alerts
5. Pokedex
6. Rematches
7. Transit
8. Settings

MVP vertical slice can include only:

1. Feed
2. Rivals
3. Alerts
4. Settings

## 5. Feed

Feed is the default recent activity list.

Shows:

- unread messages,
- recent major alerts,
- recent rival movement,
- companion notes,
- rare encounter hints.

Rules:

- store a small fixed number of recent messages for GBA save safety,
- mark messages read after viewing,
- older messages can be archived or overwritten,
- major story messages should also set permanent story flags elsewhere.

Recommended MVP capacity:

- 16 recent messages.

Recommended full-game capacity:

- 32 recent messages if save space allows.

## 6. Rivals

Rivals page shows:

- current rival region,
- last known location,
- badge/trial count,
- latest activity,
- relationship tone,
- rematch availability,
- tag battle request if active.

MVP:

- Blue, Ava, Dax only.
- show current Kanto stage and latest message.

Full game:

- all 10 rivals.
- region filter.
- rival detail page.

## 7. Companions

Companion page tracks friends, not rivals.

Characters:

- Red
- Brock
- Misty
- May
- later optional companions if added

Shows:

- current status,
- next known meeting point if available,
- training/rematch availability,
- companion notes,
- tag battle availability.

Red should appear here more often than in the general feed, so he feels like a travel companion without becoming notification spam.

## 8. Alerts

Alerts page includes:

- villain activity,
- legendary anomalies,
- weather events,
- swarm/outbreak alerts,
- route hazards,
- major story reminders.

Priority levels:

- critical: story-blocking or major villain event,
- major: important optional or world event,
- minor: useful content hint,
- flavor: world movement.

## 9. Pokedex Checklist

This is optional and pull-based.

It should not nag the player. The player opens it when they want guidance.

Shows:

- caught/seen progress,
- missing species by region,
- habitat hints,
- time/weather requirements,
- swarm/outbreak hints,
- fossil/restoration needs,
- evolution item needs,
- legendary trial status.

Stages:

- Beta after Brock: simple Kanto habitat hints.
- Kanto League: regional missing list.
- Hoenn: weather/fishing filters.
- Alola: wormhole filter.
- Paldea/World Championship: pre-final full readiness checklist.

## 10. Rematches

Rematches page shows:

- gym leader rematches,
- rival rematches,
- companion training battles,
- trainer route rematches,
- tournament availability.

MVP:

- locked placeholder until after Misty/Vermilion.

Full:

- filter by region,
- show tier,
- show suggested level cap.

## 11. Transit

Transit is not unlocked immediately.

WorldLink Transit is not a quick-jump menu. It is a passport, timetable, and route-status page. The player still travels through in-world systems: trains, ferries, airports, Fly/Sky Pass points, wormholes, Academy gates, or story-specific transit NPCs.

Stages:

- Kanto local Fly/Sky Pass preview.
- Kanto League: World Circuit Passport.
- Johto/Hoenn: ferry/train.
- Alola: wormhole travel events.
- Paldea: Academy gate.
- Postgame: full world roam.

Rule: WorldLink may show where the player can go, but the player should not warp to a new region directly from WorldLink during the main story.

## 12. Settings

Settings page:

- notification mode: All, Major Only, Rivals Only, Silent.
- rival capture updates: All, Rare Only, Off.
- companion notes: On/Off.
- Pokedex hints: On/Checklist Only.
- Infinite Repel: On/Off after unlock.
- difficulty shortcut: view current mode; changes happen at Pokecenter terminal unless design later allows direct changes.

Default:

- Major Only.
- rare rival captures only.
- companion notes on.
- Pokedex checklist only.

## 13. Message Delivery

Immediate safe pop:

- major rival badge,
- rival region entry,
- villain alert,
- legendary anomaly,
- companion request,
- story unlock.

Batch until safe/town:

- common captures,
- minor rival movement,
- flavor notes,
- swarm hints,
- daycare updates.

Never interrupt:

- gym battle,
- trainer battle,
- cutscene,
- major dungeon boss,
- evolution,
- starter selection.

## 14. Save Data Approach

Do not store full rich messages if save space becomes tight.

Preferred:

- message ID,
- message parameter IDs if needed,
- read/unread bit,
- priority,
- timestamp/chapter sequence,
- source type.

MVP can use fixed scripted messages without dynamic parameters.

## 15. MVP Acceptance Criteria

WorldLink MVP is acceptable when:

- player receives WorldLink after Blue lab battle,
- Feed opens from key item or menu,
- at least 3 messages can queue,
- messages can be marked read,
- Blue/Ava/Dax statuses display,
- major Rocket alert appears after Brock,
- settings page can show notification mode,
- no message triggers during battle,
- save/load preserves queued/read state.

## 16. Full-Game Acceptance Criteria

Full WorldLink is complete when:

- all 10 rivals have status pages,
- Red/Brock/Misty/May have companion pages,
- Pokedex checklist supports all regions,
- rematch board supports gym/rival/companion rematches,
- transit page reflects unlocked regions,
- alerts cover villains, swarms, anomalies, and weather,
- player can reduce or silence notifications,
- no route or battle becomes spammed by updates.
