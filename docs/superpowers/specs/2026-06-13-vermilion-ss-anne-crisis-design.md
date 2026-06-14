# Vermilion S.S. Anne Crisis Design

## Goal

Turn Vermilion and the S.S. Anne into the first Kanto set piece where the long journey feels bigger than a local badge quest. The classic S.S. Anne beats stay intact: ticket check, Blue's corridor battle, seasick Captain, and Cut reward. The Nexus Red twist is that Blue is jealous of Red traveling with Antman, Misty follows the harbor investigation but only joins after the ship crisis, and Rocket, Team Gold Dust, and a hidden Johto-linked scout all fight over a passenger manifest that hints at the next region without unlocking it.

## Approved Decisions

- Build both: a pre-Vermilion Blue jealousy beat and the Vermilion/S.S. Anne story arc.
- Misty becomes a recurring companion after the S.S. Anne crisis, not immediately after Route 25.
- Team Gold Dust's leader remains mysterious in Kanto.
- The S.S. Anne includes a three-way faction conflict.
- Vermilion Harbor gives the first strong WorldLink hint that Johto is the next region, while WorldLink still keeps Johto locked until Kanto's core story is complete. Johto remains locked until Kanto's League and Rocket/Nexus arc are resolved.

## Story Design

Blue appears in Vermilion before Antman boards the S.S. Anne. He has heard that Red is traveling with Antman and takes it personally: Blue thinks Red is treating Antman like the real rival while Blue is still trying to prove he owns the journey. Red stays warm and calm, and Misty watches the harbor signal without formally joining yet.

On the S.S. Anne, Blue's classic rival battle remains the main corridor challenge. His text now reflects jealousy, WorldLink pressure, and the ship's foreign-trainer scale. After that battle, a new crisis beat on the 2F corridor reveals three factions moving at once:

- Rocket wants the passenger manifest because it shows which ports and badge systems can be used to pull regions together.
- Team Gold Dust wants the same manifest because it points to rare physical anchors, fossils, coins, bells, and relics that can be sold or hoarded.
- A hidden Johto-linked scout, called a Bell Tower courier in this slice, is not a full villain reveal. They are trying to keep Johto's tower data out of both criminal groups' hands.

The Captain still gives Cut, but his seasickness now has a Nexus explanation: the ship's compass and manifest were disturbed by a golden bell-mark signal from across the sea. After the crisis, Vermilion Harbor updates: Misty commits to recurring travel scenes, Red confirms the road is getting larger, and the harbor sign or sailor gives a WorldLink-style note that Johto is detected but locked until Kanto is resolved.

## Implementation Boundaries

- This patch uses scripted NPCs and standard battles only.
- Red and Misty are story companions here, not true overworld follow/AI systems yet.
- The three-way conflict is represented by dialogue and a two-trainer battle against Rocket plus Gold Dust, with the Johto courier as the third party who interrupts the theft and points forward.
- Johto must not become selectable travel in this patch.
- Companion rematches remain reserved for the later Friends system.

## Acceptance Criteria

- Vermilion City contains Red, Blue, and Misty story objects near the harbor or ship path.
- Blue's Vermilion dialogue explicitly reacts to Red traveling with Antman.
- Misty's Vermilion dialogue changes after the S.S. Anne crisis and states she is joining the journey as a recurring friend.
- Blue's S.S. Anne rival text is rewritten around jealousy, WorldLink pressure, and classic Cut progression.
- S.S. Anne 2F contains Rocket, Team Gold Dust, and Bell Tower courier crisis dialogue.
- The crisis includes a standard battle or two-trainer battle against Rocket and Gold Dust balanced around the Lt. Surge approach.
- The Captain's Office references the manifest, Johto signal, and Cut as a field tool without removing the original reward.
- WorldLink progression data records Vermilion Harbor as the first Johto lock hint.
- Validation covers the patch file, Vermilion scenes, S.S. Anne crisis markers, new trainer constants/data, Captain text, companion timing, and WorldLink lock data.
