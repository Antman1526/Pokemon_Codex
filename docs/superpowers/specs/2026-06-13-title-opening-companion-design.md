# Pokemon Nexus Red - Title, Opening, and Companion Design

Date: 2026-06-13
Status: approved direction

## 1. Purpose

This spec locks the first-build identity and opening story direction for Pokemon Nexus Red. It covers the custom title-screen concept, the richer Pallet Town opening, Red's AI companion behavior, WorldLink dungeon notification behavior, and mandatory recurring companion roles for Brock and Misty.

## 2. Approved Design Direction

Pokemon Nexus Red should feel fun, warm, and adventurous first. The game can become difficult at times, but the first build must avoid feeling like only a challenge hack. Red, Brock, and Misty should make the journey feel like a long road with friends while Antman remains the trainer who earns badges and solves the central crisis.

## 3. Custom Title-Screen Concept

The first custom title concept is:

- Scene: Pallet Town coastline or cliff edge at dawn.
- Foreground: Red stands looking outward with Pikachu beside him.
- Sky: a faint red-gold Nexus rift forms a fractured world-map silhouette above the horizon.
- Logo: `Pokemon Nexus Red` sits over the horizon, with a subtle Nexus ring behind `Red`.
- Mood: hopeful, mysterious, and FireRed-rooted.

Implementation notes:

- First implementation may use placeholder graphics, palette swaps, or text-only title identity if needed to keep the `.gba` build moving.
- The title should stop presenting as generic Emerald as early as practical.
- The title concept should be documented before full asset replacement so artists and implementers can iterate without blocking engine proof.

## 4. Opening Story Flow

The game begins with a short bedroom, Mom, and Oak intro before the starter lab.

Approved opening beats:

1. Antman wakes in his Pallet Town bedroom.
2. The TV or radio reports strange weather, unusual Pokemon migration, and League communication problems.
3. Mom enters or calls from downstairs, saying Professor Oak has asked for Antman by name.
4. Mom gives emotional context: Pallet Town has seen great trainers leave before, but this morning feels different.
5. Antman exits the house and sees Red near the Pallet grass line with Pikachu.
6. Red warmly points out tracks or behavior that should not exist near Pallet, speaking like Antman's friend rather than a distant legend.
7. Blue interrupts, irritated that Red is taking Antman seriously and insisting Oak is waiting.
8. Ava appears with notes about wrong-region Pokemon appearing near Route 1.
9. Dax arrives late, already talking about racing to Brock.
10. Oak explains the World Pokedex Initiative and the impossible starter migration.
11. Antman chooses from the 39-starter system.
12. Blue receives a dramatic counter-pick and forces the mandatory first battle.
13. Oak gives Antman the WorldLink prototype after the first battle.
14. Red gives a short line that frames the journey as Antman's road, not a replay of Red's.

Tone rule: the opening should be creative and characterful, but compact enough for the first build. The first playable `.gba` should prove the feeling, not fully animate a cinematic prologue.

## 5. Red AI Companion Behavior

Red is AI-controlled in tag battles.

Approved team model:

- Red uses chapter-based teams so each region has a recognizable companion identity.
- Red's core team remains stable enough to feel like Red.
- One or two slots may adapt to Antman's starter family, difficulty, and current chapter needs.
- Red should support the player without solving fights alone.

Recommended first implementation:

- Kanto early tag team: Pikachu plus one support-leaning partner.
- Kanto midgame: Pikachu, Ivysaur/Charmeleon/Wartortle cameo slot, utility option.
- Late game: iconic Red-style roster, saved for major companion moments and postgame friend battle.

AI tuning rule: Red's AI should make competent choices, but scripted battles must prevent Red from sweeping every enemy before Antman meaningfully participates.

Dialogue tuning rule: early Red should be warmer and more talkative than classic silent Red because he is Antman's full-game friend. He should still be calm and observant, but his first scenes should make the friendship readable.

## 6. WorldLink Notification Pause Rules

WorldLink notifications pause during focus-heavy spaces.

Paused areas:

- caves,
- villain hideouts,
- deep forests,
- ancient ruins,
- towers,
- story dungeons,
- major cutscenes,
- boss events,
- gym battles,
- starter selection,
- evolutions.

When Antman exits a paused area, WorldLink should show a compact digest:

```text
While You Were Away
- Blue reached Cerulean City.
- Ava logged an unusual Grass-type nest near Route 3.
- Rocket chatter increased near Mt. Moon.
```

Design reason: this preserves immersion during dungeons while keeping the living-rival fantasy intact.

## 7. Mandatory Recurring Brock and Misty

Brock and Misty are mandatory recurring story companions after their gym arcs.

Brock role:

- early mentor,
- survival and route-prep teacher,
- fossil and breeding ethics voice,
- practical friend who helps make long journeys feel believable.

Misty role:

- confidence friend,
- water-route and fishing expert,
- tempo and speed-control teacher,
- energetic companion who keeps the journey fun and competitive.

Implementation rule: Brock and Misty should rotate in and out of the story. They should be mandatory recurring companions, but not permanent followers in every route.

## 8. Data and Build Impact

Required doc/data updates:

- mark title-screen concept as first-build design target,
- update Kanto vertical slice opening flow,
- update Red companion AI team rule,
- update WorldLink delivery rules with dungeon pause and digest behavior,
- mark Brock and Misty as mandatory recurring companions.

First-build scope remains engine proof first:

1. build baseline `.gba`,
2. confirm OpenEmu boot/save,
3. apply Pokemon Nexus Red title identity,
4. build Pallet bedroom/Mom/Oak intro,
5. build starter selection and Blue battle,
6. add WorldLink MVP.

## 9. Self-Review

- No placeholder decisions remain in this spec.
- The title concept does not block the first `.gba` build because placeholder implementation is allowed.
- WorldLink remains useful without interrupting caves and dungeons.
- Red, Brock, and Misty are recurring companions without taking Antman's agency.
