# Implementation Plan: Native PC/Mac Migration

Date: 2026-06-14
Target: `POKEMON NEXUS RED` native Windows/macOS build.

## Overview

Move the complete all-nine-region Pokemon Nexus Red vision from a GBA-first implementation path to a native PC/Mac game path. The GBA patch-stack remains a prototype/reference track. The native game should be built as one source project that exports to Windows PC and macOS.

## Architecture Decisions

- Use Godot 4 as the recommended engine for the native build.
- Keep story/content data-driven so nine regions, 10 rivals, companions, encounters, trainers, marts, and WorldLink notifications can scale.
- Preserve classic FireRed-style visual direction with upgraded HD pixel visuals, richer lighting, smoother UI, and widescreen readability without binding the project to GBA memory, save, or UI constraints.
- Start with a Kanto shell and bedroom/lab loop before porting large Pokemon datasets.

## Phase 1: Native Shell

### Task 1: Install/verify Godot

Acceptance:

- `godot --version` or `godot4 --version` works locally.
- Export templates are installed.
- Windows and macOS export presets can be listed or created.

Verification:

```sh
godot --version
godot --headless --version
```

Files likely touched:

- `build_notes/PC_MAC_NATIVE_BUILD_NOTES.md`

### Task 2: Create `native/nexus-red/` project scaffold

Acceptance:

- Godot project opens.
- Main scene boots.
- Title text says `POKEMON NEXUS RED`.
- Input map includes confirm, cancel, menu, sprint, and WorldLink.

Verification:

```sh
godot --headless --path native/nexus-red --check-only --quit
```

Files likely touched:

- `native/nexus-red/project.godot`
- `native/nexus-red/src/`
- `native/nexus-red/scenes/`

### Task 3: Add data loader foundation

Acceptance:

- Native project can load region/chapter data from structured files.
- Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea, and Nexus Island IDs are recognized.
- Current region defaults to Kanto.

Verification:

```sh
godot --headless --path native/nexus-red --run-tests
python3 tools/validate_design_data.py
```

Files likely touched:

- `native/nexus-red/src/data/`
- `native/nexus-red/content/regions/`
- `data_design/region_chapters.yaml`

## Phase 2: First Playable Native Loop

### Task 4: Build bedroom/Mom/Oak intro

Acceptance:

- New game starts in Antman's bedroom.
- Mom scene establishes the strange global migration/news hook.
- Red appears as a warm friend before Oak's lab.
- Oak starts the World Pokedex Initiative.

Verification:

```sh
godot --path native/nexus-red
```

Manual check:

- Start new game and reach Oak's lab without console errors.

### Task 5: Build 39-starter selection prototype

Acceptance:

- All 27 regional starters and 12 special starters appear.
- Player can select one starter.
- Blue receives the first rival counterpick.
- Ava and Dax receive valid starters.
- First Blue pressure dialogue appears after starter selection.

Verification:

```sh
python3 tools/validate_design_data.py
python3 tools/validate_native_starter_slice.py
godot --headless --path native/nexus-red --script tests/starter_slice_test.gd
```

Manual check:

- Select at least one starter from each regional group.

### Task 6: Add first WorldLink prototype

Acceptance:

- WorldLink opens from menu/input.
- Feed shows Blue, Ava, Dax, and Red-related opening entries.
- Notifications pause in dungeon-tagged spaces once dungeon flags exist.

Verification:

```sh
godot --headless --path native/nexus-red --run-tests
python3 tools/validate_native_platform_strategy.py
```

## Phase 3: Kanto Brock Slice

### Task 7: Build Route 1/Viridian/Pewter traversal

Acceptance:

- Player can walk onto a first Route 1 prototype.
- Red appears for the first warm route companion scene.
- Blue battle placeholder records first battle pressure before the real battle engine exists.
- Encounter levels scale with early progression.

Verification:

```sh
python3 tools/validate_native_route1_slice.py
godot --headless --path native/nexus-red --script tests/route1_slice_test.gd
```

### Task 8: Build Brock and Pewter Museum anomaly

Acceptance:

- Brock is Standard-mainline-hard, with harder presets available.
- Red cannot fight the gym for Antman.
- Pewter Museum anomaly introduces the Nexus hook after Brock.

Verification:

- Win Brock battle on Standard.
- Confirm museum scene unlocks only after the badge.

### Task 7.5: Build shared battle placeholder

Acceptance:

- Blue's Route 1 pressure can open a shared battle placeholder screen.
- The screen shows player starter and Blue starter.
- Save state records battle started, result, and finished flags.
- The screen returns to Route 1 after completion.

Verification:

```sh
python3 tools/validate_native_battle_placeholder_slice.py
godot --headless --path native/nexus-red --script tests/battle_placeholder_test.gd
```

### Task 7.6: Add Route 1 WorldLink rumors

Acceptance:

- Blue's Route 1 placeholder battle unlocks the first encounter-rumor layer.
- WorldLink queues Blue, Ava, Dax, Red, and a Johto rival tease after the battle.
- WorldLink renders opening feed, rival batch data, and Route 1 rumors from JSON.
- The feature remains a data/checklist slice until the real encounter engine exists.

Verification:

```sh
python3 tools/validate_native_worldlink_route1_slice.py
godot --headless --path native/nexus-red --script tests/worldlink_route1_test.gd
```

### Task 7.7: Add Route 1 wild encounter shell

Acceptance:

- Route 1 can request a deterministic first wild encounter from JSON data.
- A reusable wild encounter placeholder screen can show the wild creature and player starter.
- Save state records encounter start, result, first-wild seen/caught flags, party roster, and captured creatures.
- The first playable shell remains balanced for pre-Brock progression and does not claim the full battle/capture engine is complete.

Verification:

```sh
python3 tools/validate_native_route1_wild_encounter_slice.py
godot --headless --path native/nexus-red --script tests/route1_wild_encounter_test.gd
```

### Task 7.8: Add minimal wild encounter loop

Acceptance:

- Route 1 wild encounters initialize deterministic HP from encounter data.
- Full-HP capture is blocked in the first loop.
- A simple player attack lowers wild HP without knocking out the tutorial catch.
- A damaged first wild encounter can be caught with a deterministic `catch_success` result.
- Red gives first-capture coaching during the loop.

Verification:

```sh
python3 tools/validate_native_wild_encounter_loop_slice.py
godot --headless --path native/nexus-red --script tests/wild_encounter_loop_test.gd
```

### Task 7.9: Add wild encounter command menu

Acceptance:

- Wild encounters display visible Fight, Catch, and Run commands.
- Fight lowers wild HP through the existing minimal loop.
- Catch remains visible and produces `catch_success` after damage.
- Run remains available through the visible command menu.
- Existing keyboard shortcut behavior still works while the UI matures.

Verification:

```sh
python3 tools/validate_native_wild_command_menu_slice.py
godot --headless --path native/nexus-red --script tests/wild_command_menu_test.gd
```

### Task 7.10: Add Route 1 party status panel

Acceptance:

- Route 1 can show/hide a small field party panel from the menu input.
- The panel reads the actual save-state party roster.
- The panel shows Antman's starter and the first caught Route 1 creature after capture.
- The panel also summarizes captured creatures, giving a base for the later full party menu.

Verification:

```sh
python3 tools/validate_native_route1_party_panel_slice.py
godot --headless --path native/nexus-red --script tests/route1_party_panel_test.gd
```

### Task 7.11: Add Viridian City shell

Acceptance:

- Route 1 can transition north into Viridian City.
- Viridian City is a playable world scene with upgraded FireRed-style placeholder layout.
- The city includes a Pokemon Center shell with Nurse Joy dialogue and a healing flag.
- The city includes a Poke Mart shell that reflects Antman's starting $100000 travel fund.
- Save state records Viridian arrival, Center visit, and Mart visit.

Verification:

```sh
python3 tools/validate_native_viridian_city_slice.py
godot --headless --path native/nexus-red --script tests/viridian_city_test.gd
```

### Task 7.12: Add Viridian Red/Rocket story beat

Acceptance:

- Viridian City has a Red companion check-in.
- Viridian City can surface the first Rocket clue through a Mart shipment lead.
- Save state records the Red scene, Rocket clue, and Viridian story WorldLink queue.
- WorldLink renders the Viridian Red/Rocket/Blue story batch from JSON.

Verification:

```sh
python3 tools/validate_native_viridian_story_slice.py
godot --headless --path native/nexus-red --script tests/viridian_story_test.gd
```

### Task 7.13: Add Route 2 / Viridian Forest gate shell

Acceptance:

- Viridian City can transition north into a Route 2 / Viridian Forest Gate scene after the Rocket clue.
- Red remains the active companion and warns Antman about Rocket activity beyond Viridian.
- Save state records the Route 2 forest gate and Red warning flags.
- The gate can return to Viridian City for the first playable route loop.

Verification:

```sh
python3 tools/validate_native_route2_gate_slice.py
godot --headless --path native/nexus-red --script tests/route2_forest_gate_test.gd
```

### Task 7.14: Add Route 2 catch tutorial encounter

Acceptance:

- Route 2 has its own pre-Brock encounter data that returns to the Viridian Forest Gate scene.
- Red can trigger a first Route 2 catch tutorial before the forest dungeon.
- Save state records Route 2 tutorial seen/caught flags and captures Pidgey.
- The shared wild encounter shell can return to Route 2 instead of always returning to Route 1.

Verification:

```sh
python3 tools/validate_native_route2_catch_tutorial_slice.py
godot --headless --path native/nexus-red --script tests/route2_catch_tutorial_test.gd
```

### Task 7.15: Add Routes 1-3 full starter and bonus migration pool

Acceptance:

- Routes 1-3 have a data contract for all 27 official regional starters.
- Routes 1-3 include the 12 bonus early choices: Eevee, Pikachu, Dratini, Abra, Gastly, Larvitar, Sandile, Kubfu, Staryu, Shroomish, Rockruff, and Ralts.
- The migration pool stays in a pre-Brock level band and distributes 13 entries per route.
- EncounterService exposes query helpers for the full pool, per-route entries, and individual species.

Verification:

```sh
python3 tools/validate_native_early_migration_pool.py
godot --headless --path native/nexus-red --script tests/early_migration_pool_test.gd
```

### Task 7.16: Make Route 1 and Route 2 migration encounters playable

Acceptance:

- EncounterService can pick the next uncaught early migration species for a route.
- Route 1 can trigger its migration encounter pool from the playable scene.
- Route 2 / Viridian Forest Gate can trigger its migration encounter pool from the playable scene.
- Route 1 normal grass surfaces migration starters after the first deterministic wild catch.
- Route 2 normal grass surfaces migration starters after the Red catch tutorial catch.
- Captured migration species are skipped on later migration picks.

Verification:

```sh
python3 tools/validate_native_playable_migration_triggers.py
godot --headless --path native/nexus-red --script tests/playable_migration_triggers_test.gd
```

### Task 7.17: Add playable Route 3 migration scene

Acceptance:

- Route 2 / Viridian Forest Gate can transition north into Route 3.
- Route 3 records save-state progress and keeps Red as the active companion.
- Route 3 can trigger its migration encounter pool, starting with Chespin.
- Wild encounters that start on Route 3 return to Route 3.

Verification:

```sh
python3 tools/validate_native_route3_migration_scene.py
godot --headless --path native/nexus-red --script tests/route3_migration_scene_test.gd
```

### Task 7.18: Add Viridian Forest mini-dungeon shell

Acceptance:

- Route 2 / Viridian Forest Gate can transition into Viridian Forest.
- Viridian Forest records save-state progress and keeps Red as the active companion.
- Viridian Forest contains a first Rocket scout story beat.
- Viridian Forest can return to the gate or continue forward to Route 3.

Verification:

```sh
python3 tools/validate_native_viridian_forest_slice.py
godot --headless --path native/nexus-red --script tests/viridian_forest_test.gd
```

### Task 7.19: Add Pewter City Brock/Red intro shell

Acceptance:

- Route 3 can transition into Pewter City.
- Pewter City records save-state progress.
- Brock appears as a friendly first-gym mentor, not just a boss gate.
- Red gives pre-Brock training advice that respects the expanded starter pool.

Verification:

```sh
python3 tools/validate_native_pewter_city_slice.py
godot --headless --path native/nexus-red --script tests/pewter_city_test.gd
```

### Task 7.20: Add Brock Pewter Gym placeholder battle

Acceptance:

- Pewter City can start a Brock gym placeholder battle.
- Brock battle data documents Geodude, Onix, and a level cap balanced around the expanded starter pool.
- Save state records Brock battle start, finish, and badge flags.
- The placeholder battle screen can render non-Blue opponent data.

Verification:

```sh
python3 tools/validate_native_brock_gym_placeholder.py
godot --headless --path native/nexus-red --script tests/brock_gym_placeholder_test.gd
```

### Task 7.21: Add post-Brock Pewter Museum anomaly hook

Acceptance:

- Pewter Museum anomaly interaction is gated behind Brock's badge.
- Red stays as the active companion and helps stop a Rocket fossil-reading theft.
- Bill pings WorldLink with the first explicit fossil/Nexus energy connection.
- Save state and WorldLink record the museum anomaly for the Kanto story checklist.

Verification:

```sh
python3 tools/validate_native_pewter_museum_anomaly.py
godot --headless --path native/nexus-red --script tests/pewter_museum_anomaly_test.gd
```

### Task 7.22: Add Mt. Moon entrance faction-conflict shell

Acceptance:

- Pewter City can transition forward to Mt. Moon only after the museum anomaly.
- Red remains the active companion and warns Antman at the cave mouth.
- Team Rocket and Team Gold Dust appear in conflict over fossil crates.
- The scene introduces a Nexus Fossil mystery item without resolving the full dungeon.
- Save state and WorldLink record Mt. Moon entrance progress and faction conflict.

Verification:

```sh
python3 tools/validate_native_mt_moon_entrance_slice.py
godot --headless --path native/nexus-red --script tests/mt_moon_entrance_test.gd
```

### Task 7.23: Add Mt. Moon first interior fossil split setup

Acceptance:

- Mt. Moon entrance can transition into the first interior room after the faction conflict.
- Red remains the active companion and starts mapping the cave.
- Team Rocket takes the left path with the Dome Fossil crate.
- Team Gold Dust takes the right path after the Helix Fossil signal.
- The Nexus Fossil remains a deeper unresolved signal.
- Save state and WorldLink record the first interior room and fossil split.

Verification:

```sh
python3 tools/validate_native_mt_moon_interior_slice.py
godot --headless --path native/nexus-red --script tests/mt_moon_interior_test.gd
```

### Task 7.24: Add Mt. Moon Rocket left-path placeholder battle

Acceptance:

- Mt. Moon Interior 1 can start a Rocket Grunt placeholder battle after fossil split scouting.
- Red is present as story support and blocks the second Rocket, but true tag combat remains deferred.
- Battle data documents a post-Brock level cap, Rocket faction identity, and Zubat/Rattata opener team.
- Save state records battle start, finish, and Red tag setup flags.
- Placeholder battle return sends the player back to Mt. Moon Interior 1.

Verification:

```sh
python3 tools/validate_native_mt_moon_rocket_battle.py
godot --headless --path native/nexus-red --script tests/mt_moon_rocket_battle_test.gd
```

### Task 7.25: Add Mt. Moon Gold Dust right-path placeholder battle

Acceptance:

- Mt. Moon Interior 1 can start a Gold Dust Prospector placeholder battle after fossil split scouting.
- Battle data documents a post-Brock level cap, Gold Dust faction identity, and mineral/ground opener team.
- Save state records battle start, finish, and Gold Dust Helix claim blocked flags.
- Placeholder battle return sends the player back to Mt. Moon Interior 1.
- The battle pairs with the Rocket left-path fight so the fossil decision can require both factions to be pressured.

Verification:

```sh
python3 tools/validate_native_mt_moon_gold_dust_battle.py
godot --headless --path native/nexus-red --script tests/mt_moon_gold_dust_battle_test.gd
```

### Task 7.26: Add Mt. Moon fossil decision scene

Acceptance:

- Mt. Moon Interior 1 can transition to a fossil decision scene only after both faction battles are finished.
- The decision scene presents Dome Fossil and Helix Fossil as the immediate choice.
- Choosing one fossil records a persistent single-choice flag and does not choose the other fossil.
- The Nexus Fossil remains unresolved as a deeper cave signal.
- Save state and WorldLink record fossil decision reached, fossil choice made, and the deeper Nexus signal.

Verification:

```sh
python3 tools/validate_native_mt_moon_fossil_decision.py
godot --headless --path native/nexus-red --script tests/mt_moon_fossil_decision_test.gd
```

### Task 7.27: Add Route 4 Cerulean approach bridge

Acceptance:

- Mt. Moon fossil decision can transition forward to Route 4 only after Dome or Helix is chosen.
- Route 4 becomes the first playable step toward Cerulean after Mt. Moon.
- Red stays as the active companion and warns that Misty, Rocket, Gold Dust, and Cerulean Bridge are about to converge.
- Save state and WorldLink record Route 4 arrival, Red's Cerulean warning, and the Cerulean Bridge threat tease.
- Route 4 can return to the fossil decision scene for now until the Cerulean City slice exists.

Verification:

```sh
python3 tools/validate_native_route4_cerulean_approach.py
godot --headless --path native/nexus-red --script tests/route4_cerulean_approach_test.gd
```

### Task 7.28: Add Cerulean City Misty intro

Acceptance:

- Route 4 can transition into Cerulean City after Red's Route 4 warning is seen.
- Cerulean City becomes a playable city shell with the gym, Pokemon Center, and Nugget Bridge visually represented.
- Misty is introduced as a strong local ally, but she does not become a full companion yet.
- Misty and Red identify Nugget Bridge as the immediate crisis before the gym challenge.
- Save state and WorldLink record Cerulean arrival, Misty's intro, and Rocket/Gold Dust pressure around Nugget Bridge.
- Cerulean can return to Route 4 until the Nugget Bridge slice exists.

Verification:

```sh
python3 tools/validate_native_cerulean_city_intro.py
godot --headless --path native/nexus-red --script tests/cerulean_city_intro_test.gd
```

### Task 7.29: Add Nugget Bridge recruiter setup

Acceptance:

- Cerulean City can transition to Nugget Bridge after Misty's intro identifies the threat.
- Nugget Bridge becomes a playable bridge shell with Red and Misty scouting Rocket and Gold Dust recruitment pressure.
- The first bridge recruiter can start a placeholder battle.
- Battle data documents a Cerulean-appropriate level cap, faction recruiter identity, and early Rocket/Gold Dust front team.
- Placeholder battle return sends the player back to Nugget Bridge.
- Save state and WorldLink record bridge arrival, bridge scouting, and first recruiter battle completion.

Verification:

```sh
python3 tools/validate_native_nugget_bridge_recruiter.py
godot --headless --path native/nexus-red --script tests/nugget_bridge_recruiter_test.gd
```

### Task 7.30: Resolve Nugget Bridge and unlock Misty's gym

Acceptance:

- Nugget Bridge captain battle stays locked until the first bridge recruiter is defeated.
- The bridge captain can start a placeholder battle after the first recruiter is cleared.
- Battle data documents a Cerulean-appropriate level cap, mixed Rocket/Gold Dust captain identity, and bridge capstone team.
- Placeholder battle return sends the player back to Nugget Bridge.
- Defeating the bridge captain clears the Nugget Bridge crisis and unlocks Misty's gym as the next story target.
- Save state and WorldLink record bridge captain completion and crisis cleared status.

Verification:

```sh
python3 tools/validate_native_nugget_bridge_resolution.py
godot --headless --path native/nexus-red --script tests/nugget_bridge_resolution_test.gd
```

### Task 7.31: Add Misty Cerulean Gym placeholder battle

Acceptance:

- Misty's gym remains locked until the Nugget Bridge crisis is cleared.
- Cerulean City can start the Misty placeholder gym battle after the bridge captain is defeated.
- Battle data documents a Cerulean-appropriate level cap, Water specialty, Staryu/Starmie team, and Cascade Badge reward.
- Placeholder battle return sends the player back to Cerulean City.
- Save state and WorldLink record Misty's gym start, completion, and Cascade Badge status.
- WorldLink checklist adds the Misty gym and Cascade Badge steps before the Route 25/Bill thread.

Verification:

```sh
python3 tools/validate_native_misty_gym_placeholder.py
godot --headless --path native/nexus-red --script tests/misty_gym_placeholder_test.gd
```

### Task 7.32: Add Route 25 Bill intro and first Nexus network decode

Acceptance:

- Cerulean City keeps Route 25 locked until Antman earns the Cascade Badge.
- After Cascade Badge, Cerulean can transition to Route 25 and Bill's cottage.
- Route 25 records Red as the active companion and positions Misty as a recurring friend after her gym arc.
- Bill introduces the storage-network anomaly as the first explicit Nexus network decode, not a quick-travel WorldLink jump.
- Save state and WorldLink record Route 25 reached, Bill's intro, the storage-network clue, and the first Nexus decode.
- WorldLink checklist adds Route 25, Bill, and first Nexus network decode milestones.

Verification:

```sh
python3 tools/validate_native_route25_bill_intro.py
godot --headless --path native/nexus-red --script tests/route25_bill_intro_test.gd
```

### Task 7.33: Add Cerulean Rocket house theft and stolen TM recovery

Acceptance:

- Cerulean's Rocket house stays locked until Bill's Route 25 intro has explained the WorldLink/storage clue.
- Cerulean can transition into the burglarized Rocket house scene after Bill's intro.
- The house scene records the stolen TM clue and connects classic Rocket theft to the southbound Vermilion shipping route.
- The Rocket TM thief can start a placeholder battle and returns the player to the house after completion.
- Defeating the thief records the stolen TM recovery and unlocks Route 5 toward Vermilion as the next story target.
- WorldLink checklist adds Cerulean theft, stolen TM recovery, and Route 5/Vermilion path unlock milestones.

Verification:

```sh
python3 tools/validate_native_cerulean_rocket_house.py
godot --headless --path native/nexus-red --script tests/cerulean_rocket_house_test.gd
```

### Task 7.34: Add Route 5 Underground Path setup toward Vermilion

Acceptance:

- Cerulean City keeps Route 5 locked until the stolen TM is recovered and the Vermilion path flag is set.
- After stolen TM recovery, Cerulean can transition to Route 5 and the Underground Path entrance.
- Route 5 records Red as the active companion while Misty and Bill contribute scouting context.
- The Underground Path setup reinforces that WorldLink is not a quick-travel shortcut; the player moves through an in-world route.
- Save state and WorldLink record Route 5 reached, Underground Path scouted, Vermilion shipping lead, and Vermilion City teased.
- WorldLink checklist adds Route 5, Underground Path scouting, and Vermilion shipping lead milestones.

Verification:

```sh
python3 tools/validate_native_route5_underground_path.py
godot --headless --path native/nexus-red --script tests/route5_underground_path_test.gd
```

### Task 7.35: Add Vermilion City arrival shell

Acceptance:

- Route 5 keeps Vermilion locked until Underground Path scouting records the Vermilion shipping lead.
- Route 5 can transition to a playable Vermilion City shell after the shipping lead is seen.
- Vermilion City visually represents the Pokemon Center, Mart, Lt. Surge's gym, and harbor/S.S. Anne area.
- The arrival scene records Red as the active companion while Misty scouts the harbor and Bill follows the S.S. Anne manifest lead.
- Save state and WorldLink record Vermilion reached, harbor scouted, S.S. Anne ticket lead, and Surge power-sabotage tease.
- The slice sets up the next S.S. Anne or Surge sabotage chapter without implementing those events yet.

Verification:

```sh
python3 tools/validate_native_vermilion_city_arrival.py
godot --headless --path native/nexus-red --script tests/vermilion_city_arrival_test.gd
```

### Task 7.36: Add S.S. Anne ticket office and harbor manifest setup

Acceptance:

- Vermilion keeps the S.S. Anne ticket office locked until the harbor is scouted and the ticket lead is found.
- After Vermilion scouting, Vermilion can transition to a playable S.S. Anne ticket office scene.
- The ticket office scene records Red guarding the harbor, Misty watching the waterline, and Bill decoding the edited ship manifest.
- Save state and WorldLink record S.S. Anne ticket office reached, manifest checked, Bill's manifest anomaly decode, Red's harbor guard scene, and boarding pass earned.
- WorldLink checklist adds the ticket office, manifest, Bill decode, and S.S. Anne boarding pass milestones.
- The slice sets up the next S.S. Anne ship chapter without implementing the ship interior yet.

Verification:

```sh
python3 tools/validate_native_ss_anne_ticket_office.py
godot --headless --path native/nexus-red --script tests/ss_anne_ticket_office_test.gd
```

### Task 7.37: Add S.S. Anne boarding and main deck setup

Acceptance:

- The ticket office keeps S.S. Anne boarding locked until Antman earns the boarding pass.
- After the boarding pass, the ticket office can transition to a playable S.S. Anne main deck scene.
- The main deck scene records Red as the active companion, Misty watching the tide, Bill finding Rocket cargo edits, Blue being aboard, and the Captain's Trail Cutter lead.
- Save state and WorldLink record S.S. Anne boarded, Red's boarding scene, Blue's ship rival tease, Rocket cargo-hold clue, and Captain Trail Cutter lead.
- WorldLink checklist adds S.S. Anne boarding, Blue ship tease, Rocket cargo clue, and Trail Cutter lead milestones.
- The slice sets up the next Blue ship battle, Rocket cargo hold, and Captain/Trail Cutter payoff without implementing them yet.

Verification:

```sh
python3 tools/validate_native_ss_anne_boarding.py
godot --headless --path native/nexus-red --script tests/ss_anne_boarding_test.gd
```

### Task 7.38: Add Blue S.S. Anne rival battle placeholder

Acceptance:

- The S.S. Anne main deck keeps Blue's ship battle locked until the main deck scouting scene has identified Blue aboard.
- After deck scouting, the main deck can start a `blue_ss_anne` placeholder battle.
- Blue's S.S. Anne battle data uses the dynamic Blue starter plus classic ship-era pressure picks.
- Save state and WorldLink record Blue's ship battle started, finished, and a small rival-respect beat.
- Battle completion returns the player to the S.S. Anne main deck.
- WorldLink checklist adds Blue's S.S. Anne battle and ship-respect milestones.

Verification:

```sh
python3 tools/validate_native_ss_anne_blue_battle.py
godot --headless --path native/nexus-red --script tests/ss_anne_blue_battle_test.gd
```

### Task 7.39: Add S.S. Anne Rocket cargo hold investigation

Acceptance:

- The S.S. Anne main deck keeps the cargo hold locked until Blue's ship battle is complete.
- After Blue's ship battle, the main deck can transition to a playable S.S. Anne cargo hold scene.
- The cargo hold scene records Red guarding the stairs, Misty reading the lower-deck waterline, Bill decoding cargo data, Rocket cargo manifest recovery, and the first hidden Nexus Order crate symbol.
- Save state and WorldLink record cargo hold reached, Rocket cargo manifest recovered, Nexus Order crate symbol seen, Bill cargo decode, Misty's waterline clue, Red's guard beat, and Captain path unlocked.
- WorldLink checklist adds cargo hold entry, Rocket manifest, Nexus Order crate symbol, and Captain path milestones.
- The slice sets up the next Captain/Trail Cutter or Rocket cargo battle payoff without implementing it yet.

Verification:

```sh
python3 tools/validate_native_ss_anne_cargo_hold.py
godot --headless --path native/nexus-red --script tests/ss_anne_cargo_hold_test.gd
```

### Task 7.40: Add S.S. Anne Captain cabin and Trail Cutter payoff

Acceptance:

- The S.S. Anne cargo hold keeps the Captain cabin locked until the Rocket cargo investigation unlocks the Captain path.
- After cargo investigation, the cargo hold can transition to a playable S.S. Anne Captain cabin scene.
- The Captain cabin scene records Red as the active companion while Misty confirms the waterline clue, Bill validates the cargo manifest, and the Captain hands Antman the Trail Cutter.
- Save state and WorldLink record Captain cabin reached, Captain seasick scene, Trail Cutter obtained, Trail Cutter field tool unlocked, and Lt. Surge gym access unlocked.
- WorldLink checklist adds Captain cabin entry, Captain help, Trail Cutter, and Lt. Surge gym access milestones.
- The slice sets up the next Vermilion/Lt. Surge sabotage chapter without implementing Surge's gym battle yet.

Verification:

```sh
python3 tools/validate_native_ss_anne_captain_cabin.py
godot --headless --path native/nexus-red --script tests/ss_anne_captain_cabin_test.gd
```

### Task 7.41: Add Vermilion power sabotage setup

Acceptance:

- Vermilion keeps the Surge power sabotage branch locked until Trail Cutter is unlocked from the S.S. Anne Captain cabin payoff.
- After Trail Cutter, Vermilion can transition to a playable power sabotage service-yard scene behind Lt. Surge's gym.
- The scene introduces Team Gas as a Kanto threat while keeping Rocket involved as the faction that first breached the grid.
- Red and Misty help Antman prepare for Surge's battle tempo, while Bill decodes a power-grid relay loop tied back to the S.S. Anne Nexus mark.
- Save state and WorldLink record power sabotage reached, Rocket/Team Gas sabotage exposed, Team Gas Kanto debut, Red/Misty Surge prep, Bill power decode, and Lt. Surge gym battle unlocked.
- WorldLink checklist adds the power sabotage, Rocket/Team Gas exposure, Red/Misty prep, and Surge gym battle unlock milestones.
- The slice sets up the next Lt. Surge gym battle placeholder without implementing the gym battle yet.

Verification:

```sh
python3 tools/validate_native_vermilion_power_sabotage.py
godot --headless --path native/nexus-red --script tests/vermilion_power_sabotage_test.gd
```

### Task 7.42: Add Lt. Surge gym placeholder battle

Acceptance:

- The Vermilion power sabotage scene keeps Lt. Surge's gym battle locked until the sabotage scene is resolved.
- After the sabotage scene, Antman can start the `lt_surge_vermilion_gym` placeholder battle from the Vermilion service-yard scene.
- The battle data documents a mainline-hard electric team with Voltorb, Pikachu, and Raichu, level cap 26, and Thunder Badge reward.
- Save state and WorldLink record Surge battle started, Surge battle finished, Thunder Badge earned, Surge respect scene, and Route 11 path unlocked.
- Battle completion returns the player to the Vermilion power sabotage scene so the next route handoff can be built from there.
- WorldLink checklist adds Lt. Surge gym challenge, Thunder Badge, and Route 11 unlock milestones.

Verification:

```sh
python3 tools/validate_native_lt_surge_gym_placeholder.py
godot --headless --path native/nexus-red --script tests/lt_surge_gym_placeholder_test.gd
```

### Task 7.43: Add Route 11 eastbound handoff

Acceptance:

- The Vermilion power sabotage scene keeps Route 11 locked until Antman earns the Thunder Badge and the Route 11 path flag is unlocked.
- After Lt. Surge, Antman can leave the Vermilion service yard for a playable Route 11 shell.
- Route 11 records Red as the active full-game companion while Misty rotates to water-route support and Bill decodes a new Nexus relay.
- Rocket and Team Gas fallout continues east of Vermilion instead of ending at Surge's gym.
- A Snorlax roadblock is teased as the next classic Kanto obstacle, pushing the player toward Diglett's Cave without quick-jumping regions.
- Save state and WorldLink record Route 11 reached, Red's eastbound scene, Misty's handoff, Bill's signal decode, Rocket/Team Gas fallout, and the Snorlax roadblock.
- WorldLink checklist adds Route 11, faction fallout, Route 11 Nexus signal, and Snorlax roadblock milestones.

Verification:

```sh
python3 tools/validate_native_route11_handoff.py
godot --headless --path native/nexus-red --script tests/route11_handoff_test.gd
```

### Task 7.44: Add Diglett's Cave detour and Echo Flute lead

Acceptance:

- Route 11 keeps Diglett's Cave locked until the Route 11 handoff confirms the Snorlax roadblock.
- After the Route 11 handoff, Antman can enter a playable Diglett's Cave detour scene from Route 11.
- Diglett's Cave records Red as the active full-game companion and uses Bill to map a Nexus relay under the tunnel.
- Rocket and Team Gold Dust continue the faction-war thread through cave survey crates and mineral maps.
- The scene confirms Snorlax still blocks Route 12 and introduces the Echo Flute as the next field-tool lead rather than clearing Snorlax immediately.
- Save state and WorldLink record Diglett's Cave reached, Red's cave guard beat, Bill's relay map, Rocket/Gold Dust argument, Snorlax Route 12 block confirmation, and Echo Flute lead.
- WorldLink checklist adds Diglett's Cave, the cave Nexus relay, Route 12 Snorlax confirmation, and Echo Flute lead milestones.

Verification:

```sh
python3 tools/validate_native_diglett_cave_detour.py
godot --headless --path native/nexus-red --script tests/diglett_cave_detour_test.gd
```

### Task 7.45: Add Route 2 east field lab and Rock Tunnel lead

Acceptance:

- Diglett's Cave keeps the Route 2 east field lab locked until the Echo Flute lead has been found.
- After the cave detour scene, Antman can exit to a playable Route 2 east field lab scene.
- Red stays as the active full-game companion and confirms the party is still moving through physical Kanto routes.
- Bill and an Oak aide turn the Echo Flute lead into a field-tool frequency decoder without waking Snorlax yet.
- Rocket and Team Moonlight are connected through sleep-signal residue, preserving the custom faction web while pointing toward Lavender.
- The scene unlocks Route 9 toward Rock Tunnel as the next recommended physical path.
- Save state and WorldLink record the field lab reached, Red's east-exit confirmation, Bill's Echo Flute decoder, Oak aide field-tool brief, Rocket/Moonlight sleep trace, Lavender signal path, and Route 9/Rock Tunnel unlock.
- WorldLink checklist adds Route 2 east field lab, Echo Flute frequency, Rocket/Moonlight sleep trace, and Route 9/Rock Tunnel milestones.

Verification:

```sh
python3 tools/validate_native_route2_east_field_lab.py
godot --headless --path native/nexus-red --script tests/route2_east_field_lab_test.gd
```

### Task 7.46: Add Route 9 Rock Tunnel approach

Acceptance:

- Route 2 east field lab keeps Route 9 locked until the lab decodes and unlocks the Rock Tunnel path.
- After the lab scene, Antman can transition to a playable Route 9 Rock Tunnel approach scene.
- Route 9 records Red as the active full-game companion and frames the route as a meaningful trainer-lane preparation beat.
- Bill warns that Rock Tunnel needs darkness planning before the Lavender tower signal can be followed safely.
- Team Moonlight visibly debuts on Route 9 while Rocket's supply cache shows the faction conflict is converging on the same tunnel route.
- The scene confirms the Lavender tower signal and unlocks Rock Tunnel entry as the next story route without entering the dungeon yet.
- Save state and WorldLink record Route 9 reached, Red's trainer-lane beat, Bill's darkness warning, Team Moonlight's Route 9 debut, Rocket's supply cache, Lavender tower signal confirmation, and Rock Tunnel entry unlock.
- WorldLink checklist adds Route 9, Rock Tunnel preparation, Team Moonlight Route 9 exposure, and Rock Tunnel entry milestones.

Verification:

```sh
python3 tools/validate_native_route9_rock_tunnel_approach.py
godot --headless --path native/nexus-red --script tests/route9_rock_tunnel_approach_test.gd
```

### Task 7.47: Add Rock Tunnel interior shell

Acceptance:

- Route 9 keeps Rock Tunnel locked until Red scouts the trainer lane, Team Moonlight mark, Rocket cache, and Lavender signal.
- After Route 9 scouting, Antman can transition into a playable Rock Tunnel interior scene.
- Rock Tunnel records Red as the active full-game companion and frames the dungeon as a companion survival beat, not a quick regional jump.
- Bill tracks the Echo Flute trace through Rock Tunnel toward Lavender.
- Team Moonlight pressures the cave with sleep/dream signals while Rocket's dark cache shows Giovanni's network is monitoring the faction conflict.
- The Flash Lantern field-tool need is introduced before deeper cave travel.
- The Lavender exit path is unlocked for the next Kanto beat without implementing Lavender yet.
- Save state and WorldLink record Rock Tunnel reached, Red's guidance, Bill's Lavender echo trace, Team Moonlight cave pressure, Rocket dark cache, Flash Lantern need, and Lavender exit path unlock.
- WorldLink checklist adds Enter Rock Tunnel, Track Lavender echo, Pressure Team Moonlight in Rock Tunnel, and Unlock Lavender exit path milestones.

Verification:

```sh
python3 tools/validate_native_rock_tunnel_interior.py
godot --headless --path native/nexus-red --script tests/rock_tunnel_interior_test.gd
```

### Task 7.48: Add Lavender outskirts and Pokemon Tower signal setup

Acceptance:

- Rock Tunnel keeps the Lavender exit locked until the interior scene unlocks the Lavender exit path.
- After the Rock Tunnel interior beat, Antman can transition into a playable Lavender outskirts scene.
- Lavender outskirts records Red as the active full-game companion and marks the tonal shift from route adventure into Kanto's haunted story arc.
- Bill decodes the Echo Flute pulse as a Pokemon Tower signal rather than a normal route beacon.
- Team Moonlight presence in Lavender is introduced as grief/dream pressure around Pokemon Tower.
- Rocket surveillance is visible on the road, making Giovanni feel ahead of Antman instead of merely reacting.
- Pokemon Tower is confirmed and unlocked as the next story route without implementing the tower interior yet.
- Save state and WorldLink record Lavender outskirts reached, Red's Lavender arrival warning, Bill's Pokemon Tower signal decode, Team Moonlight's Lavender presence, Rocket surveillance, Pokemon Tower signal confirmation, and Pokemon Tower entry unlock.
- WorldLink checklist adds Reach Lavender outskirts, Decode Pokemon Tower signal, Spot Moonlight in Lavender, and Unlock Pokemon Tower entry milestones.

Verification:

```sh
python3 tools/validate_native_lavender_outskirts.py
godot --headless --path native/nexus-red --script tests/lavender_outskirts_test.gd
```

### Task 7.49: Add Pokemon Tower first floor and deeper-path lock

Acceptance:

- Lavender outskirts keeps Pokemon Tower locked until the outskirts scene confirms Bill's tower signal and unlocks tower entry.
- After the Lavender outskirts beat, Antman can transition into a playable Pokemon Tower first floor scene.
- Pokemon Tower records Red as the active full-game companion and frames the tower as a story dungeon rather than a normal route.
- Bill detects Echo Flute distortion inside Pokemon Tower.
- Team Moonlight pressure is present around the memorial floor and Rocket has a lookout watching the stairs.
- The Cubone and Mr. Fuji thread is introduced as part of the main Lavender mystery.
- The Silph Scope need is introduced, and the deeper Pokemon Tower path stays locked until that future thread is resolved.
- Save state and WorldLink record Pokemon Tower first floor reached, Red's tower guard beat, Bill's Echo Flute distortion, Team Moonlight tower pressure, Rocket tower lookout, Cubone/Mr. Fuji thread, Silph Scope need, and deeper tower path lock.
- WorldLink checklist adds Enter Pokemon Tower, Decode tower Echo Flute distortion, Find Cubone and Mr. Fuji thread, and Lock deeper tower behind Silph Scope milestones.

Verification:

```sh
python3 tools/validate_native_pokemon_tower_first_floor.py
godot --headless --path native/nexus-red --script tests/pokemon_tower_first_floor_test.gd
```

### Task 7.50: Add Route 8 Celadon road and Silph Scope lead

Acceptance:

- Pokemon Tower keeps the Route 8/Celadon lead locked until the first-floor investigation records the Silph Scope need.
- After the tower first-floor beat, Antman can transition to a playable Route 8 Celadon road scene.
- Route 8 keeps the journey physical, moving west from Lavender toward Celadon instead of jumping through WorldLink.
- Red remains the active full-game companion and frames the road as a deliberate Rocket trap.
- Bill traces the Silph Scope signal toward Celadon, tying the Lavender/Pokemon Tower arc into Celadon's Rocket/Game Corner arc.
- Team Moonlight's shadow follows Antman out of Lavender, showing that the custom faction conflict is spreading across routes.
- The Underground Path to Celadon is unlocked as the next physical travel step, with Celadon teased as the next major hub.
- Save state and WorldLink record Route 8 reached, Red's westbound warning, Bill's Silph Scope-to-Celadon trace, Rocket Game Corner lead, Team Moonlight Route 8 shadow, Underground Path to Celadon unlock, and Celadon City tease.
- WorldLink checklist adds Reach Route 8, Trace Silph Scope toward Celadon, Find Rocket Game Corner lead, and Unlock Underground Path to Celadon milestones.

Verification:

```sh
python3 tools/validate_native_route8_celadon_road.py
godot --headless --path native/nexus-red --script tests/route8_celadon_road_test.gd
```

### Task 7.51: Add Celadon Underground Path and arrival setup

Acceptance:

- Route 8 keeps the Celadon Underground Path locked until the Route 8 scene unlocks the Underground Path to Celadon.
- After Route 8 scouting, Antman can enter a playable Celadon Underground Path scene.
- The scene keeps travel physical from Lavender to Celadon rather than using WorldLink as a shortcut.
- Red remains the active full-game companion and guards the underpass because Rocket expects the Silph Scope trail to be followed.
- Bill traces the strongest Silph Scope/Game Corner signal from the underpass into Celadon.
- Rocket smugglers use the underpass to connect Lavender pressure points with Celadon's city front.
- Team Moonlight plants a dream poster in the underpass, blending Lavender's haunting pressure into Celadon's Rocket arc.
- Celadon City arrival is unlocked as the next major Kanto hub without implementing Celadon City yet.
- Save state and WorldLink record Celadon Underground Path reached, Red's underpass guard beat, Bill's Game Corner signal trace, Rocket underpass smuggler, Team Moonlight dream poster, Silph Scope/Game Corner confirmation, and Celadon City arrival unlock.
- WorldLink checklist adds Enter Celadon Underground Path, Trace Game Corner signal, Spot Moonlight dream poster, and Unlock Celadon City arrival milestones.

Verification:

```sh
python3 tools/validate_native_celadon_underground_path.py
godot --headless --path native/nexus-red --script tests/celadon_underground_path_test.gd
```

### Task 7.52: Add Celadon City arrival and Game Corner exterior setup

Acceptance:

- Celadon Underground Path keeps Celadon City locked until the underpass scene records the arrival unlock.
- After the underpass scene, Antman can enter a playable Celadon City arrival scene.
- Red remains the active full-game companion and frames Celadon as Rocket hiding in public.
- Bill traces the Silph Scope signal to the Game Corner exterior, setting up the next investigation without entering the dungeon yet.
- Rocket's Game Corner front is visible as a public city-facing operation.
- Team Moonlight follows the Lavender pressure into Celadon through a city dream ad.
- Erika and Celadon Gym are visible and teased, but the immediate story pressure remains the Game Corner.
- Game Corner investigation is unlocked as the next story beat.
- Save state and WorldLink record Celadon City reached, Red's city arrival beat, Bill's Game Corner exterior signal, Rocket Game Corner front, Team Moonlight Celadon ad, Erika gym tease, and Game Corner investigation unlock.
- WorldLink checklist adds Reach Celadon City, Scout Game Corner exterior, Spot Moonlight city ad, Tease Erika's gym, and Unlock Game Corner investigation milestones.

Verification:

```sh
python3 tools/validate_native_celadon_city_arrival.py
godot --headless --path native/nexus-red --script tests/celadon_city_arrival_test.gd
```

### Task 7.53: Add Celadon Game Corner exterior and Rocket guard pressure

Acceptance:

- Celadon City keeps the Game Corner exterior locked until the city arrival scene unlocks the investigation.
- After Celadon scouting, Antman can enter a playable Game Corner exterior scene from Celadon City.
- Red remains the active full-game companion and reads the public front as a Rocket trap.
- Bill traces a Coin Case/Silph Scope echo at the front door, connecting the classic Game Corner setup to the larger Nexus signal mystery.
- Team Moonlight's sleep coin ad keeps the Lavender/Celadon pressure blended instead of leaving the arc as Rocket-only.
- The Rocket Game Corner guard is exposed and battle-unlocked from the exterior scene.
- A placeholder Rocket guard battle uses battle data and returns to the Game Corner exterior.
- Defeating the guard records the poster-switch lead and unlocks the hideout-entry lead without implementing the full hideout yet.
- Save state and WorldLink record Game Corner exterior reached, Red's door guard read, Bill's Coin Case signal, Rocket guard exposure, Moonlight sleep coin ad, guard battle unlock, guard battle finish, poster-switch lead, and hideout-entry unlock.
- WorldLink checklist adds Reach Game Corner exterior, Expose Rocket Game Corner guard, Battle Game Corner guard, and Unlock hideout-entry lead milestones.

Verification:

```sh
python3 tools/validate_native_celadon_game_corner_exterior.py
godot --headless --path native/nexus-red --script tests/celadon_game_corner_exterior_test.gd
```

### Task 7.54: Add Celadon Rocket Hideout entry floor

Acceptance:

- The Game Corner exterior keeps the Rocket Hideout entry locked until the poster-switch/hideout-entry lead is unlocked.
- After the Rocket guard battle and poster-switch lead, Antman can enter a playable Celadon Rocket Hideout entry scene.
- Red remains the active full-game companion and guards the entry stairs without taking over the player's role.
- Bill traces the hideout elevator signal back to the Silph Scope pattern.
- The elevator/Lift Key barrier is visible and recorded as the next dungeon gating problem.
- Giovanni is foreshadowed through a command terminal instead of appearing too early.
- Team Moonlight interference appears inside Rocket's hideout, keeping the custom faction war blended into the classic Celadon Rocket arc.
- The Hideout B1F path is unlocked as the next dungeon step, but the full B1F scene is deferred.
- Save state and WorldLink record Rocket Hideout entry reached, Red's entry watch, Bill's elevator signal, Lift Key requirement, Giovanni command, Team Moonlight interference, and Hideout B1F path unlock.
- WorldLink checklist adds Reach Rocket Hideout entry, Trace hideout elevator signal, Find Lift Key requirement, Hear Giovanni command, and Unlock Hideout B1F path milestones.

Verification:

```sh
python3 tools/validate_native_celadon_rocket_hideout_entry.py
godot --headless --path native/nexus-red --script tests/celadon_rocket_hideout_entry_test.gd
```

### Task 7.55: Add Celadon Rocket Hideout B1F maze scout

Acceptance:

- The Rocket Hideout entry keeps B1F locked until the entry-floor scouting beat unlocks the B1F path.
- After the entry-floor beat, Antman can transition into a playable Celadon Rocket Hideout B1F scene.
- Red remains the active full-game companion and guards Antman through the first real Rocket maze floor without taking over the player's role.
- Bill traces the Silph Scope machinery through B1F, connecting the Celadon dungeon to the Lavender/Pokemon Tower problem.
- Rocket's classic spinner-tile maze is visible and recorded as the first hideout dungeon hazard.
- Team Gold Dust has infiltrated B1F for a coin cache/relic ledger, keeping the custom faction war active inside Rocket territory.
- Team Moonlight signal bleed interferes with Rocket's maze controls, keeping the Lavender/Celadon pressure blended.
- The Lift Key trail points deeper, and the Hideout B2F path is unlocked as the next dungeon step while the actual B2F scene is deferred.
- Save state and WorldLink record Rocket Hideout B1F reached, Red's maze guard beat, Bill's Silph Scope machine trace, Rocket spinner maze, Gold Dust infiltration, Team Moonlight signal bleed, Lift Key deeper trail, and Hideout B2F path unlock.
- WorldLink checklist adds Reach Rocket Hideout B1F, Map Rocket spinner maze, Spot Gold Dust infiltration, Trace Moonlight hideout signal, and Unlock Hideout B2F path milestones.

Verification:

```sh
python3 tools/validate_native_celadon_rocket_hideout_b1f.py
godot --headless --path native/nexus-red --script tests/celadon_rocket_hideout_b1f_test.gd
```

### Task 7.56: Add Celadon Rocket Hideout B2F patrol and Silph Scope crate

Acceptance:

- Rocket Hideout B1F keeps B2F locked until the B1F scouting beat unlocks the B2F path.
- After B1F scouting, Antman can transition into a playable Celadon Rocket Hideout B2F scene.
- Red remains the active full-game companion and blocks the corridor while Antman handles the B2F patrol.
- Bill identifies a stolen Silph Scope crate on B2F, tying the Celadon dungeon directly back to Lavender and Pokemon Tower.
- A Rocket patrol battle is unlocked from the B2F scene using placeholder battle data and returns to B2F after completion.
- Team Gold Dust is actively breaching B2F for a ledger/coin cache, creating a live faction conflict inside Rocket territory.
- Team Moonlight control-room interference disrupts Rocket's lower-floor route system.
- The Lift Key route points deeper toward B3F, but B3F remains locked until the B2F patrol battle is finished.
- Save state and WorldLink record Rocket Hideout B2F reached, Red's patrol warning, Bill's stolen Silph Scope crate, B2F patrol unlock/start/finish, Rocket and Gold Dust B2F conflict, Team Moonlight control-room interference, Lift Key B3F route, and Hideout B3F path unlock.
- WorldLink checklist adds Reach Rocket Hideout B2F, Find stolen Silph Scope crate, Battle B2F Rocket patrol, Spot B2F faction conflict, and Unlock Hideout B3F path milestones.

Verification:

```sh
python3 tools/validate_native_celadon_rocket_hideout_b2f.py
godot --headless --path native/nexus-red --script tests/celadon_rocket_hideout_b2f_test.gd
```

### Task 7.57: Add Celadon Rocket Hideout B3F Lift Key chamber

Acceptance:

- Rocket Hideout B2F keeps B3F locked until the B2F patrol battle is finished.
- After the B2F patrol is cleared, Antman can transition into a playable Celadon Rocket Hideout B3F scene.
- Red remains the active full-game companion and protects the corridor while Antman pushes the Lift Key chamber.
- Bill traces a hidden Nexus Order elevator signal under Rocket's B3F wiring, keeping the meta-villain thread alive inside the classic Rocket arc.
- B3F contains the Lift Key chamber, a Rocket Admin block, a recovered Gold Dust ledger, and a Team Moonlight sleep panel wired into Rocket's alarms.
- A Rocket Admin battle is unlocked from B3F using placeholder battle data and returns to B3F after completion.
- Defeating the Rocket Admin records the Rocket Lift Key and unlocks the future hideout elevator/Giovanni route.
- Save state and WorldLink record Rocket Hideout B3F reached, Red's Lift Key warning, Bill's Nexus Order elevator trace, Rocket Admin battle unlock/start/finish, Gold Dust ledger recovered, Team Moonlight sleep panel, Giovanni elevator route, Rocket Lift Key obtained, and Hideout elevator path unlock.
- WorldLink checklist adds Reach Rocket Hideout B3F, Trace Nexus Order elevator, Battle B3F Rocket Admin, Obtain Rocket Lift Key, and Unlock Hideout elevator path milestones.

Verification:

```sh
python3 tools/validate_native_celadon_rocket_hideout_b3f.py
godot --headless --path native/nexus-red --script tests/celadon_rocket_hideout_b3f_test.gd
```

### Task 7.58: Add Celadon Rocket Hideout elevator command route

Acceptance:

- Rocket Hideout B3F keeps the elevator locked until the Rocket Admin is beaten and the Rocket Lift Key/elevator path are unlocked.
- After the Lift Key is obtained, Antman can transition into a playable Celadon Rocket Hideout elevator scene.
- Red remains the active full-game companion and guards the elevator line while Antman restores the route.
- Bill decodes a Nexus Order elevator override hidden under Rocket's command wiring, strengthening the hidden meta-villain thread inside Celadon.
- The elevator scene contains a restored Rocket panel, Gold Dust ledger clue, Team Moonlight sleep signal, and Giovanni command floor route.
- Inspecting the elevator records the command floor route and unlocks the Rocket command floor path for the next slice.
- Save state and WorldLink record Rocket Hideout elevator reached, Red's elevator guard, Bill's Nexus Order elevator override, Rocket elevator panel restored, Gold Dust ledger decoded, Team Moonlight sleep signal, Giovanni command floor route, and Rocket command floor path unlock.
- WorldLink checklist adds Reach Rocket Hideout elevator, Decode Nexus Order elevator override, Restore Rocket elevator panel, Find Giovanni command floor route, and Unlock Rocket command floor milestones.

Verification:

```sh
python3 tools/validate_native_celadon_rocket_hideout_elevator.py
godot --headless --path native/nexus-red --script tests/celadon_rocket_hideout_elevator_test.gd
```

## Checkpoint

The native migration is healthy when:

- The Godot project boots locally.
- New game reaches Oak's lab.
- Starter choice persists in save state.
- WorldLink can open.
- A Windows and macOS export command is documented, even if final packaging polish is later.

## Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Godot not installed locally | Blocks native build verification | Install Godot and export templates before scaffold implementation |
| Scope explosion from all Pokemon data | High | Build shell and Kanto loop first; add species data by generation/channel |
| Copyrighted asset handling | High | Use placeholders/original assets in repo; do not commit extracted commercial assets |
| Battle engine complexity | High | Implement a minimal battle loop first, then add modern mechanics incrementally |
| Region content volume | High | Use templates and data pipelines, not one-off scene scripting |

## Open Questions

- Confirmed direction: Godot 4 as a 2D HD pixel RPG engine with a classic FireRed-style structure and original/custom assets.
- Should the initial native battle engine be built in GDScript first, or C# from the start for stronger typing?
- Should PC controls prioritize keyboard/controller only, or include mouse-driven menus?
