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

`NexusRed::KantoStory.complete_celadon_rocket_hideout_entry(state, location:, area_type:)` resolves the first Rocket Hideout entry room after the Game Corner poster switch. It requires the Rocket Game Corner guard battle, keeps Red active, records Bill's elevator/Silph Scope signal, the Lift Key requirement, Giovanni's command terminal, Team Moonlight interference inside Rocket's signal, and unlocks the B1F hideout path while keeping deeper access gated.

`NexusRed::KantoStory.complete_celadon_rocket_hideout_b1f(state, location:, area_type:)` resolves the first full Rocket Hideout dungeon floor. It requires the hideout entry room, records Red guarding the spinner maze, Bill tracing the Silph Scope machine pattern, Rocket's maze control, Gold Dust infiltration, Team Moonlight signal bleed, and unlocks the B2F path while the Lift Key trail continues deeper.

`NexusRed::KantoStory.complete_celadon_rocket_hideout_b2f(state, location:, area_type:)` resolves the second Rocket Hideout dungeon floor. It requires B1F completion, keeps Red active, records the B2F patrol warning, Bill's stolen Silph Scope crate trace, Rocket/Gold Dust ledger conflict, Team Moonlight control-room interference, and returns a `battle_hook` for the `rocket_hideout_b2f_patrol` villain battle at level cap 32.

`NexusRed::KantoStory.complete_rocket_hideout_b2f_patrol_battle(state, location:, result:, area_type:)` records the B2F Rocket patrol result after the map battle returns. It marks the patrol started/finished flags, records Red opening the B3F route, unlocks the Rocket Hideout B3F path, and points the next hook to `celadon_rocket_hideout_b3f`.

`NexusRed::KantoStory.complete_celadon_rocket_hideout_b3f(state, location:, area_type:)` resolves the Lift Key chamber after the B2F patrol is cleared. It records Red's Lift Key warning, Bill's hidden Nexus Order elevator trace, the Rocket Admin battle unlock, Gold Dust ledger recovery, Team Moonlight sleep-panel clue, Giovanni's elevator route, and returns a `battle_hook` for the `rocket_hideout_b3f_admin` villain-admin battle at level cap 33.

`NexusRed::KantoStory.complete_rocket_hideout_b3f_admin_battle(state, location:, result:, area_type:)` records the Rocket B3F Admin battle result after the map battle returns. It marks the admin started/finished flags, grants the Rocket Lift Key story flag, opens the Rocket Hideout elevator path, records Red holding the corridor, and points the next hook to `celadon_rocket_hideout_elevator`.

`NexusRed::KantoStory.complete_celadon_rocket_hideout_elevator(state, location:, area_type:)` resolves the restored elevator route after the Rocket Lift Key is obtained. It records Red guarding the elevator line, Bill decoding the Nexus Order override, Rocket's panel restoration, Gold Dust ledger decoding, Team Moonlight's elevator sleep signal, Giovanni's command-floor route, and unlocks the next hook `celadon_rocket_command_floor`.

`NexusRed::KantoStory.complete_celadon_rocket_command_floor(state, location:, area_type:)` resolves the Giovanni command-floor confrontation after the elevator route. It records Red guarding the entrance, Bill decoding the hidden Nexus Order terminal, Rocket command-terminal activity, the Silph Scope reward, and unlocks Pokemon Tower's deeper path plus Erika's gym path.

`NexusRed::KantoStory.complete_pokemon_tower_silph_scope_floor(state, location:, area_type:)` resolves the return to Pokemon Tower after the Silph Scope is obtained. It reveals the Marowak spirit, records Team Moonlight's fading spirit pressure, logs Red/Bill support scenes, and opens Mr. Fuji's rescue path plus the Poke Flute lead.

`NexusRed::KantoStory.complete_pokemon_tower_fuji_rescue(state, location:, area_type:)` resolves the Mr. Fuji rescue floor after the Silph Scope tower beat. It records Rocket's tower guard losing control, Red covering the stairwell, Mr. Fuji's rescue, the Poke Flute reward, and unlocks the Route 12 Snorlax wake path.

`NexusRed::KantoStory.complete_route_12_snorlax_wake(state, location:, area_type:)` resolves the Poke Flute roadblock clear. It marks the Route 12 Snorlax static encounter at level 35, clears Team Moonlight's sleep echo, unlocks the southbound path toward Fuchsia, and turns on the Super Rod tier in the four-rod fishing progression.

`NexusRed::KantoStory.complete_route_12_fishing_pier(state, location:, area_type:)` resolves the first southbound Route 12 stop after Snorlax. It records the Fishing Guru beat, Misty's Super Rod/water-route advice, Bill tracing Safari anomaly spikes, Clover and Gold Dust competing over rare-encounter rumors, and opens `fuchsia_city_arrival` as the next Kanto hook.

`NexusRed::KantoStory.complete_fuchsia_city_arrival(state, location:, area_type:)` resolves the first Fuchsia City setup beat. It introduces Koga's poison/hazard pressure, opens the Safari Zone gate, confirms the Safari anomaly, records Clover's preserve front, Gold Dust's rare buyer network, Rocket's Warden surveillance, and points the next hook to `safari_zone_anomaly`.

`NexusRed::KantoStory.complete_safari_zone_anomaly(state, location:, area_type:)` resolves the first Safari Zone investigation. It records Clover's luck-lure machine manipulating rare encounters, Gold Dust's poacher ledger market, Rocket stealing Warden files, Red/Misty/Bill preserve support scenes, a Clover admin battle hook, and unlocks `koga_gym_prep` as the next Fuchsia beat.

`NexusRed::KantoStory.complete_koga_gym_prep(state, location:, area_type:)` resolves the Fuchsia dojo preparation beat after the Safari anomaly. It unlocks Fuchsia Gym access, antidote prep, poison-hazard training, and the `koga_soul_badge_battle` hook while keeping Red as Antman's main companion and using Misty, Brock, and Bill for training/support scenes only before the actual gym battle.

`NexusRed::KantoStory.complete_koga_soul_badge_battle(state, location:, result:, area_type:)` records Koga's Soul Badge battle result after the PSDK gym battle returns. It grants the Soul Badge, unlocks Tide Rider field travel as the HM-free Surf equivalent, resolves the poison/hazard lesson, records Red/Misty/Brock post-battle support, and opens `saffron_city_arrival` as the next Rocket/Silph escalation hook.

`NexusRed::KantoStory.complete_saffron_city_arrival(state, location:, area_type:)` resolves the first Saffron City arrival beat after Koga. It turns Rocket into an infrastructure-scale threat through the Silph lockdown, upgrades Portable PC to full access through Bill's Silph relay, records Sabrina/Moonlight interference, keeps the Nexus Order as hidden sponsor static, logs Blue's rival check-in, and opens `silph_co_lobby_lockdown`.

`NexusRed::KantoStory.complete_silph_co_lobby_lockdown(state, location:, area_type:)` resolves the first Silph Co infiltration checkpoint. It records Red holding the lobby, Bill tracing the Silph firewall, Rocket locking elevators and card-key doors, Gold Dust buyers chasing components, Moonlight dream static leaking through Sabrina's pressure, and a hidden Nexus Order boardroom sponsor trace while opening `silph_co_2f_key_search`.

`NexusRed::KantoStory.complete_silph_co_2f_key_search(state, location:, area_type:)` resolves the first office-floor Silph Co checkpoint. It keeps Red as the active companion while he escorts employees, records Bill tracing a Card Key backdoor under a hidden Nexus Order sponsor account, escalates Rocket/Gold Dust/Moonlight faction pressure, and opens `silph_co_3f_warp_panel_ambush`.

`NexusRed::KantoStory.complete_silph_co_3f_warp_panel_ambush(state, location:, area_type:)` resolves the first Silph warp-panel trap. It records Red holding the employee rescue route, Blue interrupting the ambush through a side warp, Bill confirming Master Ball pressure from a hidden Nexus Order sponsor trace, and opens `silph_co_5f_elevator_route`.

`NexusRed::KantoStory.complete_silph_co_5f_elevator_route(state, location:, area_type:)` resolves the Card Key/elevator routing checkpoint. It records Red guarding the stairwell fallback, Bill rerouting the elevator grid toward 7F, Blue pressuring Rocket guards, Rocket moving Master Ball files, and Gold Dust/Moonlight interference while opening `silph_co_7f_executive_floor`.

`NexusRed::KantoStory.complete_silph_co_7f_executive_floor(state, location:, area_type:)` resolves the executive-floor hostage and boardroom-lock checkpoint. It records Red guarding the route, Blue pressuring Rocket's executive guards, Bill tracing the boardroom lock to a hidden sponsor credential, and opens `silph_co_10f_president_suite`.

`NexusRed::KantoStory.complete_silph_co_10f_president_suite(state, location:, area_type:)` resolves the president-suite rescue checkpoint. It records Red protecting the rescue route, Bill unlocking the suite, Blue finding Giovanni's boardroom trail, Rocket losing immediate control of the Master Ball prototype, and opens `silph_co_giovanni_boardroom`.

`NexusRed::KantoStory.complete_silph_co_giovanni_boardroom(state, location:, area_type:)` resolves the Silph takeover. Giovanni retreats with enough signal data to remain the long-game antagonist, Red and Blue block Rocket reinforcements, Bill caches the hidden sponsor signal, the Master Ball prototype is secured, and `saffron_sabrina_aftermath` opens while Nexus Order stays hidden.

`NexusRed::KantoStory.complete_saffron_sabrina_aftermath(state, location:, area_type:)` resolves Saffron's post-Silph cleanup. It records Red stabilizing the streets, Bill analyzing the cached signal, Sabrina identifying Moonlight psychic residue, Rocket and Gold Dust retreat fallout, and opens `sabrina_gym_prep`.

`NexusRed::KantoStory.complete_sabrina_gym_prep(state, location:, area_type:)` resolves the pre-Mind Badge setup. Sabrina reopens the Gym, stabilizes the psychic warp trial, Moonlight dream static weakens, Nexus Order remains a hidden observer, and Red waits outside so Antman takes the Gym challenge solo.

`NexusRed::KantoStory.complete_sabrina_mind_badge_challenge(state, location:, result:, area_type:)` resolves Sabrina's Gym battle. It awards the canonical Marsh Badge, breaks Moonlight pressure over Saffron, keeps Nexus Order hidden, records Red/Sabrina/Bill exit scenes, and opens `cinnabar_island_arrival`.

`NexusRed::KantoStory.complete_cinnabar_island_arrival(state, location:, area_type:)` resolves the first Cinnabar step after Saffron. It opens Pokemon Mansion and Cinnabar Lab access, introduces Phoenix research assistants, records Red's restraint scene plus Bill/Brock lab ethics support, keeps Nexus Order hidden, and opens `pokemon_mansion_mewtwo_echoes`.

`NexusRed::KantoStory.complete_pokemon_mansion_mewtwo_echoes(state, location:, area_type:)` resolves the Mansion investigation. It recovers Mewtwo-era gene-lab records, exposes Phoenix revival notes and Rocket file raids, keeps Nexus Order hidden, pauses WorldLink as a story dungeon, and opens `blaine_revival_warning`.

`NexusRed::KantoStory.complete_blaine_revival_warning(state, location:, area_type:)` resolves Blaine's Cinnabar Lab warning after the Mansion records. It recovers the Cinnabar Gym key, audits the revival machine with Bill, lets Red and Brock frame the ethics of Phoenix's doctrine, records Rocket burning lab evidence, keeps Nexus Order hidden, and opens `blaine_volcano_badge_prep`.

`NexusRed::KantoStory.complete_blaine_volcano_badge_prep(state, location:, area_type:)` resolves the companion training beat before the Cinnabar Gym. Red drills sun-pressure discipline, Misty teaches water-answer planning, Brock covers rock/ground counterplay, Rocket and Phoenix leave final courtyard traces, Nexus Order stays hidden, and the hook opens `blaine_volcano_badge_battle`.

`NexusRed::KantoStory.complete_blaine_volcano_badge_battle(state, location:, result:, area_type:)` resolves the solo Volcano Badge battle. It awards the Volcano Badge, closes the Cinnabar Phoenix setback, records Rocket recall traffic toward Viridian, keeps Nexus Order hidden, and opens `viridian_gym_return` for Giovanni's final Kanto badge arc.

`NexusRed::KantoStory.complete_viridian_gym_return(state, location:, area_type:)` resolves the return to Viridian Gym after Blaine. It reopens Giovanni's Gym, records Red's final warning, gives Bill a Silph/Cinnabar/Viridian signal triangle scene, lets Blue mark rival standings outside the Gym, keeps Nexus Order hidden, and opens `giovanni_earth_badge_battle`.

`NexusRed::KantoStory.complete_giovanni_earth_badge_battle(state, location:, result:, area_type:)` resolves Giovanni's solo Earth Badge battle. It awards the Earth Badge, collapses Rocket's public Kanto Gym cover, keeps Giovanni active as a global shadow, logs the hidden Indigo signal, and opens `victory_road_rival_standings`.

`NexusRed::KantoStory.complete_victory_road_rival_standings(state, location:, area_type:)` resolves the first Indigo/Victory Road bridge after Giovanni. It keeps Red active, has Bill open the Indigo signal watchlist, posts a WorldLink standings digest for Blue, Ava, and Dax, keeps Nexus Order hidden in the static, and opens `blue_pre_league_or_champion_battle`.

`NexusRed::KantoStory.complete_blue_pre_league_or_champion_battle(state, location:, result:, area_type:)` resolves Blue's final pre-Indigo rival battle at the Victory Road gate. Red watches without assisting, Bill detects hidden Champion room static, Blue's dynamic starter slot remains compatible with the 39-starter opening, and the hook opens `red_watches_league`.

`NexusRed::KantoStory.complete_red_watches_league(state, location:, area_type:)` resolves Red's Indigo companion vow before the Elite Four. Red stays with Antman emotionally while refusing to interfere, Bill maps hidden League static through the Elite Four rooms, Nexus Order remains unrevealed, and the hook opens `elite_four`.

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
