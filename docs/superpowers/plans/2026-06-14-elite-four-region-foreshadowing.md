# Elite Four Region Foreshadowing Plan

## Steps

1. Add a failing validator for Elite Four region foreshadowing.
2. Update Elite Four text for Lorelei, Bruno, Agatha, and Lance while preserving battles and progression flags.
3. Update Kanto Act 7 planning events.
4. Add WorldLink messages for Elite Four region signals and Lance's World Circuit warning.
5. Add rival/companion progression for Red, Misty, Brock, Blue, Ava, Dax, and Lyra.
6. Export the engine delta as `0036-elite-four-region-foreshadowing.patch`.
7. Run full validation, replay the patch stack from a clean engine tree, build the ROM, and verify the `NEXUS RED`/`BNRE` header.

## Validation

- `python3 tools/validate_elite_four_region_foreshadowing.py`
- Full `tools/validate_*.py` suite
- Clean patch replay into `engine/pokeemerald-expansion`
- `make -C engine/pokeemerald-expansion ... firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred`
