# Victory Road Rival Standings Plan

## Steps

1. Add a failing validator for the Victory Road rival standings slice.
2. Update Route 22 late Blue text to frame the battle as final Kanto League pressure.
3. Update Victory Road trainer/support text to carry WorldLink standings, Blue pressure, Ava route notes, Dax training marks, and Red's threshold choice.
4. Update Indigo Pokemon Center text to clarify companion support, solo League rules, and World Circuit Passport timing.
5. Update Kanto chapter, WorldLink message, rival progression, and build-note data.
6. Export the engine delta as `0035-victory-road-rival-standings.patch`.
7. Run full validation, replay the patch stack from a clean engine tree, build the ROM, and verify the `NEXUS RED`/`BNRE` header.

## Validation

- `python3 tools/validate_victory_road_rival_standings.py`
- Full `tools/validate_*.py` suite
- Clean patch replay into `engine/pokeemerald-expansion`
- `make -C engine/pokeemerald-expansion ... firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`

