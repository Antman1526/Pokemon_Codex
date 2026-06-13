# Pokemon Nexus Red

Pokemon Nexus Red is a nine-region Pokemon ROM-hack/fan-game design project. It begins in Pallet Town with Antman, a new trainer following Red's path, and expands through Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, and Paldea.

The project goal is to create a legal, phased build framework that Claude Code and Codex can implement chapter by chapter. The initial target is a FireRed-feeling Kanto vertical slice from Pallet Town to Brock, then region expansion.

## Core Design

- 9 main-series regions connected by one meta-story.
- FireRed-first visual identity, built through a GBA/decomp workflow.
- 39 starter choices: all 27 regional starters plus 12 special starters.
- 10 rivals traveling the same World Circuit.
- WorldLink notification feed for rival progress and world events.
- Team Rocket as the recurring villain network.
- New organizations: Phoenix, Moonlight, Gold Dust, and Nexus Order.
- Modern mechanics: Physical/Special split, Fairy type, Gen 9-style moves/abilities where supported, level caps, Nuzlocke tools, reusable TMs, Ability Capsules, Infinite Repel, and HM replacement key items.

## Important Files

- `docs/POKEMON_NEXUS_RED_FRAMEWORK.md` - main design framework and north-star document.
- `docs/DECISIONS_LOG.md` - locked user decisions for future sessions.
- `docs/CREATIVE_DIRECTION_BIBLE.md` - creative, visual, music, and tone direction.
- `docs/RED_COMPANION_SYSTEM.md` - Red as friend/travel companion.
- `docs/STARTER_SELECTION_SYSTEM.md` - 39-starter opening flow and rival assignment rules.
- `docs/WORLDLINK_SYSTEM_SPEC.md` - WorldLink UI, notification, checklist, rival, companion, and transit system.
- `docs/REGION_CONTENT_BLUEPRINT.md` - full 9-region content plan.
- `docs/GBA_OPENEMU_BUILD_STRATEGY.md` - how to keep the project on the `.gba` and OpenEmu path.
- `docs/LONG_GAME_RETENTION_DESIGN.md` - pacing and replayability design for a very long game.
- `docs/CLAUDE_CODEX_GBA_TASK_ROADMAP.md` - phased task roadmap for Claude Code and Codex.
- `data_design/` - structured planning data for regions, rivals, starters, encounters, and WorldLink.
- `build_notes/MAC_OPENEMU_BUILD_NOTES.md` - macOS build and OpenEmu smoke-test notes.
- `build_notes/ENGINE_PROOF_STATUS.md` - current local engine build status and blocker.
- `tools/validate_design_data.py` - validates the YAML planning files.

## Validation

Run:

```sh
python3 tools/validate_design_data.py
```

## Legal Rule

Do not commit or distribute copyrighted ROM files. Development should produce source changes and legal patch files only.
