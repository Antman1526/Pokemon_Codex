# Blaine Phoenix Ethics Design

Date: 2026-06-14

## Goal

Pay off the Pokemon Mansion Secret Key handoff by making Blaine the first adult authority who directly names the moral problem behind Team Phoenix. The Gym remains a classic quiz Gym and fire-type battle, but its text now turns Cinnabar's old science into a question the player must carry into Viridian and later regions.

## Design

Blaine is not a Phoenix member. He is a witness. He knows Cinnabar's revival science, Mew/Mewtwo rumor pressure, and fossil restoration records were purchased and reframed by outside funders. His position is simple: Recovery is not ownership, and creation without restraint becomes control.

The classic quiz Gym stays intact. The player still answers questions, fights existing Gym trainers if wrong, battles Blaine, receives the Volcano Badge, and gets TM38. The story layer changes the meaning of those rooms: quiz facts become pressure tests, Gym trainers reference consent before revival, and the Gym Guy frames Blaine as someone who knows Phoenix science too well.

The Volcano Badge reward adds a WorldLink handoff toward Viridian. This keeps region flow strict: no new region unlock, no Mewtwo resolution, no Phoenix boss battle yet. Instead, Blaine's warning points back to Giovanni and the final Kanto badge.

## Scope

Included:

- Update Blaine's intro, defeat, TM, post-battle, and WorldLink reward text.
- Update selected Gym support text around Phoenix ethics.
- Add `blaine_phoenix_ethics_gym` and `volcano_badge_worldlink_viridian_handoff` to Act 6.
- Add WorldLink messages for Blaine's Phoenix warning and the Viridian handoff.
- Add a rival/companion progression band for Red, Brock, Blue, Ava, and Dax.

Not included:

- No Blaine team rebalance yet.
- No new Phoenix commander sprite or boss battle.
- No full Sky Pass/Fly replacement implementation.
- No Viridian Gym changes in this slice.

## Acceptance

- `validate_blaine_phoenix_ethics.py` passes after patches are applied.
- Full patch replay applies cleanly through `0033`.
- Existing validators still pass.
- The ROM builds with title `NEXUS RED` and game code `BNRE`.
