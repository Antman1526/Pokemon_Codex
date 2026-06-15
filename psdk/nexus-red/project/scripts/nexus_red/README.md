# Nexus Red PSDK Scripts

This folder contains custom Ruby scaffolding for the primary Pokemon Studio / PSDK build.

Current entrypoint:

- `000_seed_loader.rb` loads the generated PSDK seed registries from `Data/nexus_red_seed/generated/`.

Runtime services:

- `runtime/seed_data.rb` reads generated registries.
- `runtime/runtime_state.rb` builds the Nexus Red save-state scaffold.
- `runtime/world_link.rb` handles live, paused, and digest notifications.
- `runtime/*_progress.rb` and other service files track starter selection, party/PC storage, portable PC access, field healing, Kanto story beats, early migration encounters, rivals, companions, factions, regions, gameplay options, field tools, Pokédex readiness, Center/Mart services, encounter-world state, and battle mechanics gating.

Route 1-3 migration map events should call `NexusRed::EarlyMigrationEncounters.prepare_map_event_encounter(state, route_id, time:, max_level:)`. The method returns a PSDK-friendly encounter payload, records the species as seen in the Pokédex, and skips species already caught by the player.

Route 1-3 can use `NexusRed::Route1MigrationEvent.trigger`, `NexusRed::Route2MigrationEvent.trigger`, and `NexusRed::Route3MigrationEvent.trigger` as their first concrete adapters. They delegate to `NexusRed::RouteMigrationEventAdapter.trigger_route`, which stores a pending wild-migration battle request through `NexusRed::MapEventBridge.pending_battle_request(state)`; the later PSDK map command should consume that request and hand its species key and level to the final wild battle launcher.

`NexusRed::WildBattleLauncher.launch_pending_request(state)` consumes the pending request and builds the validated wild-battle launch payload. It records launch history and exposes `species_key`, `level`, map id, route id, and source event id. The payload now includes PSDK BattleInfo script lines based on the official scripted battle flow: create `Battle::Logic::BattleInfo`, add the player party, generate a wild `PFM::Pokemon`, add it to enemy bank 1 without trainer metadata, then call `$scene.call_scene(Battle::Scene, bi)`.

When running inside a loaded PSDK runtime, `NexusRed::WildBattleLauncher.execute_pending_request(state)` consumes the same pending request and performs that BattleInfo flow directly. Outside PSDK it remains safe for validation because it returns the launch payload without attempting to call missing engine constants.

After a wild battle returns, map scripts should call `NexusRed::WildBattleResults.record_result(state, outcome: 'caught')` or another outcome such as `fled`. Caught outcomes record the species through `PokedexAvailability.record_caught`, add it to `party_species` when there is room, otherwise add it to `pc_box_species`, and let the Route 1-3 migration adapters advance to the next uncaught species.

`NexusRed::PartyStorage` owns the current six-slot party cap and PC overflow list. Starter selection and caught wild battles both route through this service. It also exposes `deposit_species`, `withdraw_species`, and `swap_species` for the future portable PC and Pokemon Center PC interfaces.

`NexusRed::PortablePC` wraps `PartyStorage` for field/menu use. It starts locked, unlocks from a story source with `unlock(state, source:, access_level:)`, exposes `open` and `summary`, and forwards `deposit`, `withdraw`, and `swap` while recording the last action for later UI feedback. Kanto can use `access_level: 'lite'` after Brock/Red training, then upgrade to full access later in the journey.

`NexusRed::FieldHealing` wraps the portable healing QoL rule from the active difficulty profile. It starts locked, unlocks from a story source with charges, stores lightweight party conditions until real PSDK HP/status binding is connected, and exposes `heal_team` plus `restore_species`. Casual difficulty uses full portable healing without charge consumption, Standard/Hard consume charges, and Expert/Nuzlocke block field healing in paused danger areas such as caves and villain hideouts.

`NexusRed::KantoStory.complete_brock(state, location:, area_type:)` is the first integrated Kanto map-script reward bundle. It marks the Boulder Badge flags, records the Pewter Rocket alert, unlocks the after-Brock QoL tier, enables Pewter rare candies, unlocks portable PC lite and field healing, records the Red/Brock post-gym scenes, and advances the Kanto story to Act 2. The method is idempotent so repeated map triggers do not duplicate rewards or reset charges.

`NexusRed::KantoStory.complete_pewter_museum_anomaly(state, location:, area_type:, partner_id:)` resolves the post-Brock museum service tunnel event. It requires the Boulder Badge, marks the museum Rocket event flag, records Team Rocket fossil-scanner theft activity, adds an early Team Phoenix conflict clue, records the partner backup scene, and queues a paused story alert when called from a villain hideout area.

`NexusRed::KantoStory.complete_mt_moon_operation(state, location:, area_type:, rival_id:)` resolves the Act 2 Mt. Moon story bridge. It requires the museum clue, records Rocket Moon Stone extraction, marks the Gold Dust invoice hint and Ava Clefairy night notes, logs the Rocket/Gold Dust double-cross, records Ava as a rival story clue, and pauses the story alert while the player is inside the cave.

`NexusRed::KantoStory.complete_nugget_bridge_qualifier(state, location:, area_type:, rival_ids:)` resolves the Nugget Bridge World Circuit qualifier. It requires Mt. Moon completion, records the Rocket bridge recruitment probe, updates rival World Circuit movement, activates Misty in Cerulean without following yet, records her bridge crisis scene, and leaves the story in Act 2 for the Misty battle.

`NexusRed::KantoStory.complete_misty_battle(state, gym_location:, join_location:, area_type:)` resolves the Cascade Badge and Route 25 companion entry. It requires Nugget Bridge completion, records the Misty battle, unlocks the Old Rod and rematch board tier flag, marks Misty's Route 25 companion flag, makes Misty follow Antman, and advances Kanto into Act 3 toward Bill and Vermilion.

`NexusRed::KantoStory.complete_bill_storage_anomaly(state, location:, area_type:)` resolves Bill's Route 25 storage metadata hook. It requires Misty completion, activates Bill as a non-following technical ally, records storage intro and Route 25 systems scenes, logs Rocket storage metadata probing, stores a reusable storage anomaly record linked to PC, Portable PC, WorldLink, and region progression, and points the Act 3 route toward S.S. Anne.

`NexusRed::KantoStory.complete_ss_anne_manifest(state, location:, area_type:, rival_id:)` resolves the S.S. Anne Act 3 bridge. It requires Bill's storage anomaly, marks the foreign Trainer traffic, Blue ship battle, and Rocket smuggling manifest events, records Rocket manifest activity, updates Blue through WorldLink, gives Misty and Red companion scenes, and points the chapter toward Lt. Surge in Vermilion.

`NexusRed::KantoStory.complete_vermilion_power_sabotage(state, location:, area_type:)` resolves the service-yard branch behind Lt. Surge's gym. It requires the S.S. Anne manifest, records Rocket's power-room break-in, debuts Team Gas through poison exhaust grid sabotage, logs their faction conflict, records Red/Misty/Bill prep scenes, and unlocks the Surge gym battle.

`NexusRed::KantoStory.complete_lt_surge_battle(state, location:, area_type:)` resolves the Thunder Badge battle after the power sabotage is cleared. It marks the Thunder Badge and Route 11 path flags, unlocks the Good Rod and VS Seeker lead, records Red and Misty post-Surge scenes, and advances Kanto into the Rock Tunnel/Celadon/Lavender act.

`NexusRed::KantoStory.complete_route_11_handoff(state, location:, area_type:)` resolves the eastbound road after Surge. It requires the Thunder Badge, records Red's full-game companion scene, Misty's route-support handoff, Bill's Route 11 relay decode, Rocket/Team Gas fallout, and the Snorlax roadblock that pushes the player toward Diglett's Cave.

`NexusRed::KantoStory.complete_diglett_cave_detour(state, location:, area_type:)` resolves the physical cave detour around the sleeping roadblock. It requires Route 11 completion, records Red's cave guard scene, Bill's Nexus relay map, Rocket and Gold Dust arguing over stolen survey crates, Route 12 Snorlax confirmation, and the Echo Flute lead toward the Route 2 east field lab.

`NexusRed::KantoStory.complete_route_2_east_field_lab(state, location:, area_type:)` resolves the Route 2 east field lab after Diglett's Cave. It turns the Echo Flute lead into Bill's sleep-frequency decoder, records Oak's aide field-tool brief through the story flags, links Rocket residue with Team Moonlight's Lavender sleep signal, and unlocks Route 9 toward Rock Tunnel as the next physical path.

`NexusRed::KantoStory.complete_route_9_rock_tunnel_approach(state, location:, area_type:)` resolves the Route 9 approach after the Route 2 east field lab. It keeps the journey on foot toward Rock Tunnel, records Red's trainer-lane support, Bill's darkness warning, Team Moonlight's first Route 9 marker, Rocket's nearby supply cache, the Lavender tower signal confirmation, and unlocks the Rock Tunnel interior hook.

`NexusRed::KantoStory.complete_rock_tunnel_interior(state, location:, area_type:)` resolves the Rock Tunnel interior after Route 9. It records Red guiding Antman through a blackout, Bill tracing the Echo Flute toward Lavender, Team Moonlight pressuring the cave, Rocket's dark cache, unlocks `cave_lantern` as the Flash field-tool replacement, and opens the Lavender outskirts hook.

`NexusRed::KantoStory.complete_lavender_outskirts(state, location:, area_type:)` resolves the Lavender arrival after Rock Tunnel. It keeps the scene emotional and investigative, records Red grounding Antman at the town edge, Bill decoding Pokemon Tower as the Echo Flute source, Team Moonlight hiding behind Lavender grief pressure, Rocket surveillance around the tower route, and unlocks the Pokemon Tower first-floor hook.

`NexusRed::KantoStory.complete_pokemon_tower_first_floor(state, location:, area_type:)` resolves the first allowed Pokemon Tower investigation. It records Red guarding Antman, Bill detecting Echo Flute distortion, Team Moonlight pressure, the visible Rocket grunt, the Cubone and Mr. Fuji thread, and locks deeper tower progress behind the Silph Scope while opening Route 8 toward Celadon.

`NexusRed::KantoStory.complete_route_8_celadon_road(state, location:, area_type:, rival_id:)` resolves the westbound Route 8 bridge after Pokemon Tower. It records Red keeping Antman on the physical road to Celadon, Bill tracing the Silph Scope signal, Rocket's Game Corner lead, Team Moonlight's spreading shadow, Blue crossing paths on the same clue, and unlocks the Celadon Underground Path hook.

`NexusRed::KantoStory.complete_celadon_underground_path(state, location:, area_type:)` resolves the quiet underpass scene before Celadon City. It requires Route 8 completion, records Red guarding the underpass stairs, Bill confirming the Game Corner signal, Rocket using the corridor as a smuggler route, Team Moonlight planting a dream poster clue, confirms the Silph Scope lead, and unlocks the Celadon City arrival hook.

`NexusRed::KantoStory.complete_celadon_city_arrival(state, location:, area_type:)` resolves the first public Celadon City investigation beat. It requires the Celadon Underground Path, keeps Red as the active companion, records Bill's Game Corner exterior signal, Rocket's visible Game Corner front, Team Moonlight's city dream ads, Erika's gym tease, and unlocks the Game Corner exterior as the next story hook.

`NexusRed::KantoStory.complete_celadon_game_corner_exterior(state, location:, area_type:)` resolves the public Game Corner scouting beat. It requires Celadon City arrival, records Red watching the door guard, Bill's Coin Case/Silph Scope signal, Rocket's exposed floor guard, Team Moonlight's sleep coin ad, and returns a `battle_hook` for the `rocket_game_corner_guard` villain battle.

`NexusRed::KantoStory.complete_rocket_game_corner_guard_battle(state, location:, result:, area_type:)` records the Rocket Game Corner guard battle result after the map battle returns. It marks the battle started/finished flags, records Red spotting the guarded poster switch, unlocks the Game Corner hideout-entry lead, and points the next hook to `celadon_rocket_hideout_entry`.

The loader is intentionally conservative. It only reads committed JSON seed files and prepares a guarded `PFM::GameState` extension when PSDK is available. Map events, battles, Pokemon creation, and UI calls should be added in later scripts after the blank PSDK project structure is confirmed in Pokemon Studio.

Seed refresh command:

```bash
python3 tools/generate_psdk_seed_data.py
```

Validation:

```bash
python3 tools/validate_psdk_ruby_scaffold.py
```

That validation includes Ruby syntax checks for the entrypoint and runtime files, plus a runtime smoke check that requires `000_seed_loader.rb` from the PSDK project root and reads every generated registry.
