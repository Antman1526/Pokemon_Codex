# Pokemon Mansion Phoenix Field Test Design

## Intent

This slice turns Pokemon Mansion from a key hunt into the first real Act 6 pressure dungeon. Phoenix is still not a costumed army, but Antman now feels their hand inside the building: research language, recovery teams, ledgers, and a scientist battle that shows Phoenix hires serious people instead of loud grunts. The mansion remains true to FireRed: switches, diaries, broken science, Mew, Mewtwo, and the Secret Key path to Blaine.

## Story Shape

- 1F becomes the first Phoenix-linked battle by rewriting Scientist Ted as a contracted field tester. He still uses the existing trainer battle, so this stays low-risk and buildable.
- 2F diaries keep the original Mew discovery beats but add a restoration ledger layer: Phoenix is not interested in theft, they are interested in reconstructing lost life from records.
- 3F rewrites the Mewtwo birth warning around restraint. Mewtwo remains unresolved; the story only warns that creation without humility becomes danger.
- B1F makes the Secret Key becomes a Blaine handoff. The key still unlocks the Gym, but WorldLink frames it as permission to ask Blaine what Cinnabar knows about revival ethics.

## Scope

This patch deepens Pokemon Mansion and uses one existing trainer as the first Phoenix-linked battle. It does not rebalance Blaine, add new trainer classes, add custom Phoenix sprites, change Secret Key item mechanics, or implement Portable PC key-item functionality.

## Technical Notes

- Modify Pokemon Mansion 1F, 2F, 3F, and B1F script text.
- Keep map JSON mostly stable unless a sign is needed after applying prior patches.
- Add Kanto chapter markers, WorldLink messages, rival/companion feed entries, smoke-test checklist entries, and validator coverage.
- Export as `patches/engine/0031-pokemon-mansion-phoenix-field-test.patch` after replaying patches through `0030`.

## Follow-Up

The next Act 6 slice should be Blaine's Gym and the Phoenix/Blaine ethics confrontation. That is where fire difficulty, weather pressure, and the question of whether Phoenix gets a named commander should land.
