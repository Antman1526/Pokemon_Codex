# Mt. Moon Nexus Break Design

## Goal

Pay off the Pewter Museum anomaly inside Mt. Moon while keeping the FireRed story recognizable. Rocket is still hunting fossils, Miguel still guards the Dome/Helix choice, and Antman still exits toward Cerulean, but the cave now proves that Team Rocket is chasing Nexus energy rather than simple fossil profit.

## Player Experience

- Red appears near the Mt. Moon entrance as Antman's warm companion. He explains that the museum scan points into the cave, says he will watch a second route, and frames future tag battles as part of their journey together.
- Team Rocket dialogue shifts from generic fossil theft to fossil DNA, League badge signals, and region-pulling experiments.
- Miguel is rewritten as a nervous researcher who tried to protect the fossils because they started reacting after the museum scan.
- Choosing Dome or Helix remains the same item/gameplay flow, but the text marks the chosen fossil as Antman's first Nexus artifact.
- After the fossil choice, Miguel points Antman toward Cerulean and warns that Misty's badge network may be the next signal point.

## Option B Recurring Direction

Red tag battles should become a full-game pillar, but not every Red scene should force combat. The pattern should be:

- Red gives field guidance in towns/routes.
- Red joins mandatory or optional tag battles during story dungeons and villain operations.
- Red never fights gym battles for Antman.
- Each region gets at least two meaningful Red cooperation moments: one early trust-building fight and one late villain-arc fight.
- The first true reusable tag-battle implementation should be built as a dedicated engine feature, not faked by ordinary double battles.

## Implementation Scope

This patch seeds the recurring Red tag-battle direction through dialogue and story state, then rewrites the Mt. Moon story beats. It does not implement the reusable partner-battle engine yet.

## Acceptance Criteria

- `patches/engine/0011-mt-moon-nexus-break.patch` exists and applies after patches `0001` through `0010`.
- Red appears as a talkable NPC on `MtMoon_1F_Frlg`.
- Mt. Moon Rocket dialogue references Nexus/fossil scan stakes.
- Miguel dialogue references the fossil reaction and Cerulean signal path.
- Dome/Helix fossil acquisition text marks the fossil as a Nexus artifact.
- A validator confirms the above against the patched engine tree.
- The ROM builds as `pokenexusred.gba` for OpenEmu.
