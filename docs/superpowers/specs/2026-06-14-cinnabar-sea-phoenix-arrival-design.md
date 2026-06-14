# Cinnabar Sea and Phoenix Arrival Design

## Intent

This slice opens Act 6 without turning WorldLink into a region-jump system. WorldLink remains Kanto-locked and uses the Marsh Badge stabilization to point Antman from Saffron toward the sea, Cinnabar, old fire, and revival science. The goal is forward adventure momentum: leave the psychic aftermath, cross the water, arrive somewhere strange, and meet Team Phoenix through research before a direct boss battle.

## Story Shape

- Route 19 becomes the practical Tide Rider handoff. Red meets Antman near the water and frames the sea route as earned travel, not a shortcut. Misty is referenced as the safety check behind the route.
- Cinnabar receives Red's restraint scene. Red is warm and present, but he warns Antman not to treat fossil revival, Mewtwo rumors, or Phoenix research like trophies. This keeps him as a full-game friend while preserving Antman's agency.
- Team Phoenix appears through lab research, not a costumed invasion. A Phoenix-linked researcher in Cinnabar Lab talks about restoration matrices, fossil data, and controlled rebirth, making Phoenix feel calmer and more dangerous than Rocket.
- Pokemon Mansion carries the Mewtwo echo. The first-floor signal links old science, mansion damage, and Phoenix interest without resolving Mewtwo or Blaine yet.

## Scope

This patch adds arrival scenes, route clarity, Phoenix first-contact, and Mewtwo foreshadowing. It does not implement a full field-use Surf replacement, rebalance Blaine, add Phoenix battle sprites, or alter Pokemon Mansion progression. Those belong to later Act 6 slices.

## Technical Notes

- Add a Red object and Tide Rider sign/scene to Route 19.
- Add a Red object to Cinnabar Island with pre/post Blaine-safe dialogue using existing badge flags where possible.
- Add a Phoenix researcher object to Cinnabar Lab Research Room.
- Add a Pokemon Mansion first-floor sign/script that logs the Mewtwo/Phoenix echo.
- Add Kanto chapter markers, WorldLink messages, rival/companion notification data, smoke-test checklist entries, and `validate_cinnabar_sea_phoenix_arrival.py` coverage.

## Follow-Up

The next Act 6 slices should tune Blaine, deepen Pokemon Mansion, and decide when the full Portable PC key item becomes player-facing. This slice keeps the build stable and makes Cinnabar feel like the next chapter of the same long journey.
