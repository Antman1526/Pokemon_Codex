# Champion Blue Emotional Finale Plan

## Steps

1. Add a failing validator for Champion Blue's emotional finale.
2. Update Champion Blue text while preserving battle flow, flags, Oak entrance, and Hall of Fame warp.
3. Update Oak's Champion room text to clarify trust and defer the World Circuit Passport.
4. Update Kanto Act 7, WorldLink messages, rival progression, and build notes.
5. Export the engine delta as `0037-champion-blue-emotional-finale.patch`.
6. Run full validation, replay the patch stack from a clean engine tree, build the ROM, and verify the `NEXUS RED`/`BNRE` header.

## Validation

- `python3 tools/validate_champion_blue_emotional_finale.py`
- Full `tools/validate_*.py` suite
- Clean patch replay into `engine/pokeemerald-expansion`
- `make -C engine/pokeemerald-expansion ... firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`

