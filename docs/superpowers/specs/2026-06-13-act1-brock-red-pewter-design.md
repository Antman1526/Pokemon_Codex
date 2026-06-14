# Act 1 Brock, Red Training, and Pewter Museum Design

## Goal

Make the first badge feel like the opening chapter of a long adventure instead of a vanilla checkpoint. Red should feel present, warm, and useful before Pewter; Brock should account for the 27-starter pool without becoming a punishing wall; and Pewter Museum should become the first clear Rocket/Nexus anomaly hook after the Boulder Badge.

## Proposed Player Experience

- Route 1 introduces Red as Antman's active travel friend. He is not silent or distant here; he checks on the player, talks through early capture choices, and frames the expanded starter pool as something strange but exciting.
- Viridian City gives Red a second training beat focused on building a bench, avoiding overleveling, and reading the WorldLink alerts without turning him into a forced guide.
- Pewter City places Red near the gym as a friendly pre-Brock coach. Before the badge he gives type-neutral advice for players who picked any starter. After the badge he points Antman toward the museum and signals that he is checking the ridge toward Mt. Moon.
- Brock remains recognizably Brock: Rock type, first real badge test, straightforward gym structure. The rebalance makes him resilient against the giant starter pool by adding a third Rock body, but keeps the cap at 14 and avoids Radical Red-style punishment this early.
- The museum hook should fire after Brock, not before. It should imply Rocket is scanning fossils for a region-pulling anomaly, tying the classic Old Amber/Kanto fossil story into the Nexus meta-plot.

## Implementation Scope

This first build uses recurring Red NPC scenes, not the full follow-AI system. That is deliberate. The user-approved goal is early adventure feel; a true AI companion with battle participation should be built later as a dedicated engine feature after map/script pacing is proven.

## Brock Balance

Proposed standard team for first implementation:

- Geodude, level 12
- Nosepass, level 12
- Onix, level 14

Rationale:

- Geodude preserves the original lesson.
- Nosepass adds durability and a second Rock profile without introducing too much coverage.
- Onix remains the ace and badge-cap anchor.
- No held items and no brutal coverage yet. Difficulty options can later swap in harder variants.

## Pewter Museum Hook

After Brock, the gym should provide a WorldLink-style alert that sends the player to Pewter Museum. Inside the museum, a new post-badge scientist/scout beat should describe the fossil scan anomaly and Rocket interest. This keeps the mainline museum/fossil identity intact while making it part of the new multi-region conspiracy.

## Acceptance Criteria

- Red appears as a talkable warm companion scene on Route 1, in Viridian City, and in Pewter City.
- Red's Pewter dialogue changes after the Boulder Badge.
- Brock's team is updated to a three-Pokemon cap-14 team balanced around the expanded starter pool.
- After Brock, the player receives a clear WorldLink-style pointer to Pewter Museum.
- Pewter Museum contains a post-Boulder-Badge Nexus/Rocket fossil anomaly hook.
- Validation scripts assert the presence of these Act 1 pieces.
- The ROM still builds as `pokenexusred.gba`.

## Deferred

- Full AI-controlled Red following the player between maps.
- Red joining trainer battles outside gyms.
- Repeatable Brock rematch teams by difficulty.
- Museum service-tunnel dungeon and Rocket double battle.
