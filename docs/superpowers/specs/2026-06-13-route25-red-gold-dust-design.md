# Route 25 Red And Gold Dust Design

## Goal

Make Route 25 the first playable Red tag-battle story moment while introducing Team Gold Dust as a rival villain faction that openly clashes with Team Rocket. Keep Bill's classic Sea Cottage story intact, but reveal that his teleporter accident happened because WorldLink energy is beginning to interfere with Kanto's badge and transport network.

## Approved Direction

- First playable Red tag battle location: Route 25.
- Villains: Team Rocket and Team Gold Dust both appear, argue, and turn on Antman and Red.
- Companion rematches: deferred to a later Friends system.
- Blue: reacts jealously before Vermilion because Red is traveling with Antman.
- WorldLink travel rule: regions unlock one at a time through story travel, not quick-jump selection.

## Proposed Creative Choices

- Bill is a friendly but reckless WorldLink-adjacent researcher. His classic Clefairy accident stays, but the accident is now caused by a Gold Dust fragment spiking the Sea Cottage teleporter.
- Team Gold Dust is not Team Rocket with new colors. It is a cartel of relic brokers, fossil thieves, and black-market collectors who want to own the physical anchors that make region travel possible. Rocket wants control; Gold Dust wants exclusive ownership and profit.
- Rocket and Gold Dust hate each other because Rocket's region-pull experiments are destabilizing artifacts that Gold Dust wants to sell intact.
- Red's first playable tag moment is implemented in this slice as a forced double battle framed by Red entering beside Antman. True AI-controlled Red partner support remains a separate engine task because the current scripting layer exposes standard double battles cleanly but not a safe story-partner injection command.

## Player Experience

- Route 25's original trainer path remains the lead-in to Bill.
- Near Sea Cottage, Red intercepts Antman and points out that Rocket is not alone.
- A Rocket operative and a Team Gold Dust broker argue over Bill's teleporter readings and the Mt. Moon fossil signal.
- They fight each other verbally first, then decide Antman and Red are the real problem.
- The player enters a double battle representing Antman and Red versus Rocket and Gold Dust.
- After victory, Red calls it their first real tag win and warns that villain factions will start colliding around every region node.
- Bill's Sea Cottage text is lightly rewritten so his mistake feels connected to WorldLink without making him a villain.

## WorldLink Region Rule

WorldLink is a story-travel system, not a teleport hub. Antman should unlock regions in order: Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea. During the main story, only the current region is actively accessible. Earlier regions can reopen later through explicit story systems, but the first pass through each region should feel like a committed journey with companions, rivals, bad guys, and region-specific Pokemon pacing.

## Acceptance Criteria

- `patches/engine/0013-route25-red-gold-dust-tag.patch` exists and applies after `0012`.
- Route 25 contains Red, Rocket, and Gold Dust story objects near Sea Cottage.
- Route 25 includes a battle script that uses `trainerbattle_two_trainers` for Rocket plus Gold Dust.
- Trainer data includes one new Rocket trainer and one new Gold Dust trainer balanced around the post-Misty Route 25 level range.
- Sea Cottage Bill text references WorldLink interference without removing the original Bill rescue flow.
- WorldLink progression data records one-region-at-a-time story travel.
- Validation covers Route 25 story markers, new trainers, Bill text, and WorldLink progression data.
