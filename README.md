# Pokemon Nexus Red

Pokemon Nexus Red is a native PC/Mac monster-taming RPG design project. It begins in Pallet Town with Antman, a new trainer following Red's path, and expands through Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea, and the final full-region Nexus Island chapter.

The project goal is to create a legal, phased build framework that Claude Code and Codex can implement chapter by chapter. Primary target: native PC/Mac standalone game. Legacy/prototype target: `.gba` playable in OpenEmu.

The native build is the recommended path for the complete all-nine-region game. The GBA/OpenEmu path remains a useful FireRed-style prototype/reference track, but it should not constrain the full game vision.

## Core Design

- 9 main-series regions connected by one meta-story.
- Classic FireRed-style visual identity, upgraded for native PC/Mac with HD pixel tiles, richer lighting, smoother UI, and widescreen readability.
- 39 starter choices: all 27 regional starters plus 12 special starters.
- 10 rivals traveling the same World Circuit.
- WorldLink notification feed for rival progress and world events.
- Team Rocket as the recurring villain network.
- New organizations: Phoenix, Moonlight, Gold Dust, Gas, Clover, and the hidden Nexus Order.
- Modern mechanics: Physical/Special split, Fairy type, Gen 9-style moves/abilities where supported, level caps, Nuzlocke tools, reusable TMs, Ability Capsules, Infinite Repel, and HM replacement key items.

## Important Files

- `docs/POKEMON_NEXUS_RED_FRAMEWORK.md` - main design framework and north-star document.
- `docs/DECISIONS_LOG.md` - locked user decisions for future sessions.
- `docs/CREATIVE_DIRECTION_BIBLE.md` - creative, visual, music, and tone direction.
- `docs/RED_COMPANION_SYSTEM.md` - Red as friend/travel companion.
- `docs/STARTER_SELECTION_SYSTEM.md` - 39-starter opening flow and rival assignment rules.
- `docs/WORLDLINK_SYSTEM_SPEC.md` - WorldLink UI, notification, checklist, rival, companion, and transit system.
- `docs/superpowers/specs/2026-06-13-title-opening-companion-design.md` - approved title-screen, opening, Red AI, WorldLink pause, and Brock/Misty companion direction.
- `docs/REGION_CONTENT_BLUEPRINT.md` - full 9-region content plan.
- `docs/PC_MAC_NATIVE_BUILD_STRATEGY.md` - primary native Windows/macOS build strategy.
- `docs/GBA_OPENEMU_BUILD_STRATEGY.md` - how to keep the project on the `.gba` and OpenEmu path.
- `data_design/platform_targets.yaml` - structured target-platform decision data.
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
python3 tools/validate_native_platform_strategy.py
python3 tools/validate_native_godot_shell.py
python3 tools/validate_native_starter_slice.py
python3 tools/validate_native_route1_slice.py
python3 tools/validate_native_battle_placeholder_slice.py
python3 tools/validate_native_worldlink_route1_slice.py
python3 tools/validate_native_route1_wild_encounter_slice.py
python3 tools/validate_native_wild_encounter_loop_slice.py
python3 tools/validate_native_wild_command_menu_slice.py
python3 tools/validate_native_route1_party_panel_slice.py
python3 tools/validate_native_viridian_city_slice.py
python3 tools/validate_native_viridian_story_slice.py
python3 tools/validate_native_route2_gate_slice.py
python3 tools/validate_native_route2_catch_tutorial_slice.py
python3 tools/validate_native_early_migration_pool.py
python3 tools/validate_native_playable_migration_triggers.py
python3 tools/validate_native_route3_migration_scene.py
python3 tools/validate_native_viridian_forest_slice.py
python3 tools/validate_native_pewter_city_slice.py
python3 tools/validate_native_brock_gym_placeholder.py
python3 tools/validate_native_pewter_museum_anomaly.py
python3 tools/validate_native_mt_moon_entrance_slice.py
python3 tools/validate_native_mt_moon_interior_slice.py
python3 tools/validate_native_mt_moon_rocket_battle.py
python3 tools/validate_native_mt_moon_gold_dust_battle.py
python3 tools/validate_native_mt_moon_fossil_decision.py
python3 tools/validate_native_route4_cerulean_approach.py
python3 tools/validate_native_cerulean_city_intro.py
python3 tools/validate_native_nugget_bridge_recruiter.py
python3 tools/validate_native_nugget_bridge_resolution.py
python3 tools/validate_native_misty_gym_placeholder.py
python3 tools/validate_native_route25_bill_intro.py
python3 tools/validate_native_cerulean_rocket_house.py
python3 tools/validate_native_route5_underground_path.py
python3 tools/validate_native_vermilion_city_arrival.py
python3 tools/validate_native_ss_anne_ticket_office.py
python3 tools/validate_native_ss_anne_boarding.py
python3 tools/validate_native_ss_anne_blue_battle.py
python3 tools/validate_native_ss_anne_cargo_hold.py
python3 tools/validate_native_ss_anne_captain_cabin.py
python3 tools/validate_native_vermilion_power_sabotage.py
python3 tools/validate_native_lt_surge_gym_placeholder.py
python3 tools/validate_native_route11_handoff.py
python3 tools/validate_native_diglett_cave_detour.py
python3 tools/validate_native_route2_east_field_lab.py
python3 tools/validate_native_route9_rock_tunnel_approach.py
python3 tools/validate_native_rock_tunnel_interior.py
python3 tools/validate_native_lavender_outskirts.py
godot --headless --path native/nexus-red --check-only --quit
godot --headless --path native/nexus-red --script tests/smoke_test.gd
godot --headless --path native/nexus-red --script tests/starter_slice_test.gd
godot --headless --path native/nexus-red --script tests/route1_slice_test.gd
godot --headless --path native/nexus-red --script tests/battle_placeholder_test.gd
godot --headless --path native/nexus-red --script tests/worldlink_route1_test.gd
godot --headless --path native/nexus-red --script tests/route1_wild_encounter_test.gd
godot --headless --path native/nexus-red --script tests/wild_encounter_loop_test.gd
godot --headless --path native/nexus-red --script tests/wild_command_menu_test.gd
godot --headless --path native/nexus-red --script tests/route1_party_panel_test.gd
godot --headless --path native/nexus-red --script tests/viridian_city_test.gd
godot --headless --path native/nexus-red --script tests/viridian_story_test.gd
godot --headless --path native/nexus-red --script tests/route2_forest_gate_test.gd
godot --headless --path native/nexus-red --script tests/route2_catch_tutorial_test.gd
godot --headless --path native/nexus-red --script tests/early_migration_pool_test.gd
godot --headless --path native/nexus-red --script tests/playable_migration_triggers_test.gd
godot --headless --path native/nexus-red --script tests/route3_migration_scene_test.gd
godot --headless --path native/nexus-red --script tests/viridian_forest_test.gd
godot --headless --path native/nexus-red --script tests/pewter_city_test.gd
godot --headless --path native/nexus-red --script tests/brock_gym_placeholder_test.gd
godot --headless --path native/nexus-red --script tests/pewter_museum_anomaly_test.gd
godot --headless --path native/nexus-red --script tests/mt_moon_entrance_test.gd
godot --headless --path native/nexus-red --script tests/mt_moon_interior_test.gd
godot --headless --path native/nexus-red --script tests/mt_moon_rocket_battle_test.gd
godot --headless --path native/nexus-red --script tests/mt_moon_gold_dust_battle_test.gd
godot --headless --path native/nexus-red --script tests/mt_moon_fossil_decision_test.gd
godot --headless --path native/nexus-red --script tests/route4_cerulean_approach_test.gd
godot --headless --path native/nexus-red --script tests/cerulean_city_intro_test.gd
godot --headless --path native/nexus-red --script tests/nugget_bridge_recruiter_test.gd
godot --headless --path native/nexus-red --script tests/nugget_bridge_resolution_test.gd
godot --headless --path native/nexus-red --script tests/misty_gym_placeholder_test.gd
godot --headless --path native/nexus-red --script tests/route25_bill_intro_test.gd
godot --headless --path native/nexus-red --script tests/cerulean_rocket_house_test.gd
godot --headless --path native/nexus-red --script tests/route5_underground_path_test.gd
godot --headless --path native/nexus-red --script tests/vermilion_city_arrival_test.gd
godot --headless --path native/nexus-red --script tests/ss_anne_ticket_office_test.gd
godot --headless --path native/nexus-red --script tests/ss_anne_boarding_test.gd
godot --headless --path native/nexus-red --script tests/ss_anne_blue_battle_test.gd
godot --headless --path native/nexus-red --script tests/ss_anne_cargo_hold_test.gd
godot --headless --path native/nexus-red --script tests/ss_anne_captain_cabin_test.gd
godot --headless --path native/nexus-red --script tests/vermilion_power_sabotage_test.gd
godot --headless --path native/nexus-red --script tests/lt_surge_gym_placeholder_test.gd
godot --headless --path native/nexus-red --script tests/route11_handoff_test.gd
godot --headless --path native/nexus-red --script tests/diglett_cave_detour_test.gd
godot --headless --path native/nexus-red --script tests/route2_east_field_lab_test.gd
godot --headless --path native/nexus-red --script tests/route9_rock_tunnel_approach_test.gd
godot --headless --path native/nexus-red --script tests/rock_tunnel_interior_test.gd
godot --headless --path native/nexus-red --script tests/lavender_outskirts_test.gd
```

## Legal Rule

Do not commit or distribute copyrighted ROM files. Development should produce source changes and legal patch files only.
