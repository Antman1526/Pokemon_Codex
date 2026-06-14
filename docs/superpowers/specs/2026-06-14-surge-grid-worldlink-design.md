# Surge Grid And WorldLink Feed Design

## Goal

Make Lt. Surge's badge chapter feel like the first real systems test after the S.S. Anne. The original gym identity stays intact: trash-can switches, Electric pressure, Thunder Badge, and Shock Wave. The Nexus Red layer adds a Rocket power-grid sabotage beat, Red/Misty training context, a Gold Dust clue in the Fan Club, and the first compact rival notification batch that makes WorldLink feel alive without building the full feed UI yet.

## Proposed Direction

- Rocket sabotages the Vermilion Gym power grid before Surge. This turns the trash-switch puzzle into a security reset, not a replacement puzzle.
- Red handles the pre-Surge training advice: Ground answers, bench depth, and not overleveling.
- Misty supports from the harbor side: she frames the gym's power issue as connected to the S.S. Anne current and Johto signal.
- Trail Cutter is introduced as a WorldLink field-tool registration after the Thunder Badge, but the full HM replacement system remains a later milestone.
- Team Gold Dust leaves one clue in the Pokemon Fan Club: a collector asked about pedigree records and a Celadon buyer, foreshadowing their next Kanto appearance.
- The rival notification batch after Surge includes Blue, Ava, Dax, and one Johto-rival tease. Johto is still locked.

## Story Beats

1. After the S.S. Anne crisis, Red and Misty warn Antman that Vermilion's power grid is pulsing in the same rhythm as the ship manifest.
2. Inside the Gym, a Rocket grid thief is caught trying to piggyback on Surge's electric locks. Beating the thief explains why the classic trash switches are unstable.
3. Lt. Surge respects Antman more because Antman cleared the sabotage before challenging him. Surge remains brash and military-coded, but not oblivious.
4. Surge's team is tuned to the documented cap: Voltorb 21, Pikachu 22, Raichu 24.
5. After the Thunder Badge, WorldLink registers a Trail Cutter prototype and posts a compact rival feed:
   - Blue cleared the S.S. Anne and is rushing Route 11.
   - Ava logged the harbor's Johto resonance.
   - Dax beat a Sailor and is training for Surge.
   - A Johto trainer named Lyra is visible as a locked regional profile: Lyra / Johto.
6. The Fan Club worker hints that Gold Dust is looking for rare lineage records and will likely surface again in Celadon.

## Implementation Boundaries

- This milestone does not implement the full WorldLink UI.
- This milestone does not remove HM01 mechanically.
- This milestone does not add companion rematches.
- This milestone does not unlock Johto travel.
- This milestone uses standard scripts, one new Rocket trainer, and text-only WorldLink alerts.

## Acceptance Criteria

- Vermilion Gym contains a Rocket sabotage NPC with a battle around level 23.
- Gym dialogue links Rocket's sabotage to Surge's electric locks and the S.S. Anne manifest.
- Surge's Pikachu is level 22 and Raichu remains level 24.
- Surge's post-badge reward text mentions Trail Cutter registration without claiming the HM replacement system is complete.
- A post-Surge WorldLink rival notification batch mentions Blue, Ava, Dax, and Lyra as a locked Johto profile.
- Fan Club text includes a Gold Dust/Celadon buyer clue.
- Design data includes the Surge sabotage, Trail Cutter prototype, Gold Dust Fan Club clue, and rival feed batch.
- Validation covers the new patch, map objects/scripts, trainer constants/data, Surge team level, Fan Club clue, WorldLink data, and build notes.
