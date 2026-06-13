# Pokemon Nexus Red - Title Screen Brief

Date: 2026-06-13

## Approved Concept

Red, Antman, and Blue stand with their backs to the camera at sunrise, facing a glowing region-map Nexus over Pallet Town. The image should feel warm, adventurous, and classic rather than dark.

## Required Logo Text

```text
POKEMON NEXUS RED
```

## First GBA Implementation Rule

Do not block the playable ROM on final title art. The first graphics milestone may preserve FireRed title animation while the ROM header and build notes identify the game as Nexus Red. Full title art replacement should use the FRLG title asset path:

```text
engine/pokeemerald-expansion/graphics/title_screen_frlg/firered/
```

## Art Direction

- Foreground: Red, Antman, and Blue facing away.
- Midground: Pallet coastline or Route 1 ridge.
- Sky: sunrise gold and soft red.
- Nexus: glowing ring made from nine region-map silhouettes.
- Mood: hopeful first day of a huge journey.

## GBA Constraints To Respect

- Work inside GBA tile and palette limits.
- Keep high-contrast logo readability.
- Prefer a staged replacement: concept image, indexed-color mockup, then compressed engine asset.
- Verify in OpenEmu after every asset insertion.
