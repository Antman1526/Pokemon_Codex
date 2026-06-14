# Viridian Giovanni Sponsor Pressure Plan

## Steps

1. Add a failing validator for the Viridian Giovanni sponsor-pressure slice.
2. Update Giovanni's Viridian Gym text while preserving the existing trainer battle, badge flag, and TM26 reward flow.
3. Add an Earth Badge WorldLink message that routes Antman toward Victory Road and keeps Johto locked until Indigo clearance.
4. Update Kanto chapter data with the sponsor-pressure events.
5. Update WorldLink and rival progression data for Red, companions, rivals, and the locked Johto tease.
6. Export the engine delta as `0034-viridian-giovanni-sponsor-pressure.patch`.
7. Run full validation, replay the patch stack from a clean engine tree, build the ROM, and verify the `NEXUS RED`/`BNRE` header.

## Validation

- `python3 tools/validate_viridian_giovanni_sponsor_pressure.py`
- Full `tools/validate_*.py` suite
- Clean patch replay into `engine/pokeemerald-expansion`
- `make -C engine/pokeemerald-expansion ... firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`

