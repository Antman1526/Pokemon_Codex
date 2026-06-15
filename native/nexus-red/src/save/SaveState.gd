extends RefCounted

var player_name := "Antman"
var current_region := "kanto"
var current_scene := "bedroom"
var active_companion := "red"
var player_money := 100000
var player_starter := ""
var player_starter_group := ""
var blue_starter := ""
var ava_starter := ""
var dax_starter := ""
var active_battle_id := ""
var last_battle_result := ""
var active_encounter_id := ""
var active_encounter_data: Dictionary = {}
var encounter_return_scene := ""
var last_encounter_result := ""
var party_roster: Array[String] = []
var captured_creatures: Array[String] = []
var story_flags: Dictionary = {}
var worldlink_queue: Array[String] = []


func start_new_game(name: String) -> void:
	player_name = name
	current_region = "kanto"
	current_scene = "bedroom"
	active_companion = "red"
	player_money = 100000
	player_starter = ""
	player_starter_group = ""
	blue_starter = ""
	ava_starter = ""
	dax_starter = ""
	active_battle_id = ""
	last_battle_result = ""
	active_encounter_id = ""
	active_encounter_data = {}
	encounter_return_scene = ""
	last_encounter_result = ""
	party_roster = []
	captured_creatures = []
	story_flags = {
		"started_native_shell": true,
		"mom_opening_scene_seen": false,
		"starter_chosen": false,
		"blue_pressure_scene_seen": false,
		"route_1_reached": false,
		"red_route_1_companion_scene_seen": false,
		"blue_battle_placeholder_seen": false,
		"blue_route_1_battle_started": false,
		"blue_route_1_battle_finished": false,
		"route_1_rumors_unlocked": false,
		"worldlink_route_1_rival_batch_queued": false,
		"route_1_first_wild_seen": false,
		"route_1_first_wild_caught": false,
		"viridian_city_reached": false,
		"viridian_center_visited": false,
		"viridian_mart_visited": false,
		"viridian_red_scene_seen": false,
		"viridian_rocket_clue_found": false,
		"worldlink_viridian_story_batch_queued": false,
		"route_2_forest_gate_reached": false,
		"red_route_2_warning_seen": false,
		"route_2_catch_tutorial_seen": false,
		"route_2_catch_tutorial_caught": false,
		"viridian_forest_reached": false,
		"red_viridian_forest_scene_seen": false,
		"rocket_forest_scout_seen": false,
		"route_3_reached": false,
		"red_route_3_migration_scene_seen": false,
		"pewter_city_reached": false,
		"brock_pewter_intro_seen": false,
		"red_pewter_training_seen": false,
		"brock_pewter_gym_started": false,
		"brock_pewter_gym_finished": false,
		"brock_pewter_badge_earned": false,
		"pewter_museum_anomaly_seen": false,
		"worldlink_pewter_museum_batch_queued": false,
		"mt_moon_entrance_reached": false,
		"red_mt_moon_warning_seen": false,
		"rocket_gold_dust_mt_moon_conflict_seen": false,
		"nexus_fossil_hint_seen": false,
		"worldlink_mt_moon_faction_batch_queued": false,
		"mt_moon_interior_1_reached": false,
		"red_mt_moon_interior_support_seen": false,
		"rocket_mt_moon_left_path_seen": false,
		"gold_dust_mt_moon_right_path_seen": false,
		"fossil_choice_setup_seen": false,
		"worldlink_mt_moon_interior_split_batch_queued": false,
		"mt_moon_rocket_left_battle_started": false,
		"mt_moon_rocket_left_battle_finished": false,
		"red_mt_moon_tag_setup_seen": false,
		"mt_moon_gold_dust_right_battle_started": false,
		"mt_moon_gold_dust_right_battle_finished": false,
		"gold_dust_helix_claim_blocked": false,
		"mt_moon_fossil_decision_reached": false,
		"mt_moon_fossil_choice_made": false,
		"dome_fossil_chosen": false,
		"helix_fossil_chosen": false,
		"nexus_fossil_deeper_signal_seen": false,
		"worldlink_mt_moon_fossil_decision_batch_queued": false,
		"route_4_cerulean_approach_reached": false,
		"red_route_4_cerulean_warning_seen": false,
		"cerulean_bridge_threat_teased": false,
		"worldlink_route_4_cerulean_batch_queued": false,
		"cerulean_city_reached": false,
		"misty_cerulean_intro_seen": false,
		"nugget_bridge_threat_setup_seen": false,
		"worldlink_cerulean_city_batch_queued": false,
		"nugget_bridge_reached": false,
		"red_misty_nugget_bridge_scout_seen": false,
		"nugget_bridge_recruiter_1_battle_started": false,
		"nugget_bridge_recruiter_1_battle_finished": false,
		"nugget_bridge_captain_battle_started": false,
		"nugget_bridge_captain_battle_finished": false,
		"nugget_bridge_crisis_cleared": false,
		"misty_gym_unlocked": false,
		"misty_cerulean_gym_started": false,
		"misty_cerulean_gym_finished": false,
		"cascade_badge_earned": false,
		"misty_recurring_friend_unlocked": false,
		"route_25_bill_reached": false,
		"bill_route25_intro_seen": false,
		"bill_storage_network_clue_seen": false,
		"nexus_network_first_decode_seen": false,
		"worldlink_route_25_bill_batch_queued": false,
		"cerulean_rocket_house_reached": false,
		"cerulean_house_theft_seen": false,
		"rocket_stolen_tm_clue_seen": false,
		"cerulean_rocket_house_thief_battle_started": false,
		"cerulean_rocket_house_thief_battle_finished": false,
		"stolen_tm_recovered": false,
		"route_5_vermilion_path_unlocked": false,
		"worldlink_cerulean_rocket_house_batch_queued": false,
		"route_5_underground_path_reached": false,
		"underground_path_scouted": false,
		"vermilion_shipping_lead_seen": false,
		"vermilion_city_teased": false,
		"worldlink_route_5_underground_path_batch_queued": false,
		"vermilion_city_reached": false,
		"vermilion_harbor_scouted": false,
		"ss_anne_ticket_lead_seen": false,
		"surge_power_sabotage_teased": false,
		"worldlink_vermilion_city_arrival_batch_queued": false,
		"ss_anne_ticket_office_reached": false,
		"ss_anne_manifest_checked": false,
		"bill_manifest_decode_seen": false,
		"red_harbor_guard_scene_seen": false,
		"ss_anne_boarding_pass_earned": false,
		"worldlink_ss_anne_ticket_office_batch_queued": false,
		"ss_anne_main_deck_reached": false,
		"ss_anne_boarded": false,
		"red_ss_anne_boarding_scene_seen": false,
		"blue_ship_rival_teased": false,
		"rocket_cargo_hold_clue_seen": false,
		"captain_trail_cutter_lead_seen": false,
		"worldlink_ss_anne_boarding_batch_queued": false,
		"blue_ss_anne_battle_started": false,
		"blue_ss_anne_battle_finished": false,
		"blue_ss_anne_rival_respect_seen": false,
		"worldlink_ss_anne_blue_battle_batch_queued": false,
		"ss_anne_cargo_hold_reached": false,
		"rocket_cargo_manifest_recovered": false,
		"nexus_order_crate_symbol_seen": false,
		"bill_cargo_decode_seen": false,
		"misty_lower_deck_waterline_seen": false,
		"red_cargo_hold_guard_seen": false,
		"ss_anne_captain_path_unlocked": false,
		"worldlink_ss_anne_cargo_hold_batch_queued": false,
		"ss_anne_captain_cabin_reached": false,
		"captain_seasick_scene_seen": false,
		"trail_cutter_obtained": false,
		"trail_cutter_field_tool_unlocked": false,
		"surge_gym_access_unlocked": false,
		"worldlink_ss_anne_captain_cabin_batch_queued": false,
		"vermilion_power_sabotage_reached": false,
		"rocket_gas_power_sabotage_seen": false,
		"team_gas_kanto_debut_seen": false,
		"red_misty_surge_prep_seen": false,
		"bill_power_grid_decode_seen": false,
		"surge_gym_battle_unlocked": false,
		"worldlink_vermilion_power_sabotage_batch_queued": false,
		"surge_vermilion_gym_started": false,
		"surge_vermilion_gym_finished": false,
		"thunder_badge_earned": false,
		"surge_respect_scene_seen": false,
		"route_11_path_unlocked": false,
		"worldlink_vermilion_surge_gym_batch_queued": false,
		"route_11_reached": false,
		"red_route_11_eastbound_scene_seen": false,
		"misty_route_11_farewell_seen": false,
		"bill_route_11_signal_decode_seen": false,
		"rocket_gas_route_11_fallout_seen": false,
		"snorlax_roadblock_teased": false,
		"worldlink_route_11_handoff_batch_queued": false,
		"diglett_cave_detour_reached": false,
		"red_diglett_cave_guard_seen": false,
		"bill_diglett_cave_relay_map_seen": false,
		"rocket_gold_dust_cave_argument_seen": false,
		"snorlax_route_12_block_confirmed": false,
		"echo_flute_lead_seen": false,
		"worldlink_diglett_cave_detour_batch_queued": false,
		"route_2_east_field_lab_reached": false,
		"red_route_2_east_exit_seen": false,
		"bill_echo_flute_decoder_seen": false,
		"oak_aide_field_tool_brief_seen": false,
		"rocket_moonlight_sleep_signal_seen": false,
		"lavender_signal_path_teased": false,
		"route_9_rock_tunnel_path_unlocked": false,
		"worldlink_route_2_east_field_lab_batch_queued": false,
		"route_9_rock_tunnel_approach_reached": false,
		"red_route_9_trainer_lane_seen": false,
		"bill_rock_tunnel_darkness_warning_seen": false,
		"team_moonlight_route_9_debut_seen": false,
		"rocket_route_9_supply_cache_seen": false,
		"lavender_tower_signal_confirmed": false,
		"rock_tunnel_entry_unlocked": false,
		"worldlink_route_9_rock_tunnel_approach_batch_queued": false,
		"rock_tunnel_interior_reached": false,
		"red_rock_tunnel_guidance_seen": false,
		"bill_lavender_echo_trace_seen": false,
		"team_moonlight_cave_pressure_seen": false,
		"rocket_dark_cache_seen": false,
		"flash_lantern_needed_seen": false,
		"lavender_exit_path_unlocked": false,
		"worldlink_rock_tunnel_interior_batch_queued": false,
		"lavender_outskirts_reached": false,
		"red_lavender_arrival_seen": false,
		"bill_pokemon_tower_signal_decode_seen": false,
		"team_moonlight_lavender_presence_seen": false,
		"rocket_lavender_surveillance_seen": false,
		"pokemon_tower_signal_confirmed": false,
		"pokemon_tower_entry_unlocked": false,
		"worldlink_lavender_outskirts_batch_queued": false,
		"pokemon_tower_first_floor_reached": false,
		"red_pokemon_tower_guard_seen": false,
		"bill_tower_echo_flute_distortion_seen": false,
		"team_moonlight_tower_pressure_seen": false,
		"rocket_tower_grunt_seen": false,
		"cubone_mr_fuji_thread_seen": false,
		"silph_scope_need_seen": false,
		"pokemon_tower_deeper_path_locked": false,
		"worldlink_pokemon_tower_first_floor_batch_queued": false,
		"route_8_celadon_road_reached": false,
		"red_route_8_westbound_seen": false,
		"bill_silph_scope_celadon_trace_seen": false,
		"rocket_celadon_game_corner_lead_seen": false,
		"team_moonlight_route_8_shadow_seen": false,
		"underground_path_to_celadon_unlocked": false,
		"celadon_city_teased": false,
		"worldlink_route_8_celadon_road_batch_queued": false,
		"celadon_underground_path_reached": false,
		"red_celadon_underpass_guard_seen": false,
		"bill_game_corner_signal_trace_seen": false,
		"rocket_underpass_smuggler_seen": false,
		"team_moonlight_dream_poster_seen": false,
		"silph_scope_game_corner_confirmed": false,
		"celadon_city_arrival_unlocked": false,
		"worldlink_celadon_underground_path_batch_queued": false,
		"celadon_city_reached": false,
		"red_celadon_city_arrival_seen": false,
		"bill_game_corner_exterior_signal_seen": false,
		"rocket_game_corner_front_seen": false,
		"team_moonlight_celadon_ad_seen": false,
		"erika_gym_teased_seen": false,
		"game_corner_investigation_unlocked": false,
		"worldlink_celadon_city_arrival_batch_queued": false,
		"game_corner_exterior_reached": false,
		"red_game_corner_door_guard_seen": false,
		"bill_coin_case_signal_seen": false,
		"rocket_game_corner_guard_exposed": false,
		"team_moonlight_sleep_coin_seen": false,
		"game_corner_guard_battle_unlocked": false,
		"rocket_game_corner_guard_battle_started": false,
		"rocket_game_corner_guard_battle_finished": false,
		"rocket_hideout_switch_lead_seen": false,
		"game_corner_hideout_entry_unlocked": false,
		"worldlink_celadon_game_corner_exterior_batch_queued": false,
		"celadon_rocket_hideout_entry_reached": false,
		"red_hideout_entry_watch_seen": false,
		"bill_hideout_elevator_signal_seen": false,
		"rocket_lift_key_required_seen": false,
		"giovanni_hideout_command_seen": false,
		"team_moonlight_rocket_interference_seen": false,
		"rocket_hideout_b1f_path_unlocked": false,
		"worldlink_celadon_rocket_hideout_entry_batch_queued": false,
		"celadon_rocket_hideout_b1f_reached": false,
		"red_hideout_b1f_maze_guard_seen": false,
		"bill_silph_scope_machine_trace_seen": false,
		"rocket_spinner_maze_seen": false,
		"gold_dust_hideout_infiltration_seen": false,
		"team_moonlight_hideout_signal_bleed_seen": false,
		"lift_key_deeper_trail_seen": false,
		"rocket_hideout_b2f_path_unlocked": false,
		"worldlink_celadon_rocket_hideout_b1f_batch_queued": false,
		"celadon_rocket_hideout_b2f_reached": false,
		"red_hideout_b2f_patrol_warning_seen": false,
		"bill_stolen_silph_scope_crate_seen": false,
		"rocket_hideout_b2f_patrol_battle_unlocked": false,
		"rocket_hideout_b2f_patrol_battle_started": false,
		"rocket_hideout_b2f_patrol_battle_finished": false,
		"rocket_gold_dust_b2f_conflict_seen": false,
		"team_moonlight_control_room_interference_seen": false,
		"lift_key_b3f_route_seen": false,
		"rocket_hideout_b3f_path_unlocked": false,
		"worldlink_celadon_rocket_hideout_b2f_batch_queued": false,
		"celadon_rocket_hideout_b3f_reached": false,
		"red_hideout_b3f_lift_key_warning_seen": false,
		"bill_nexus_order_elevator_trace_seen": false,
		"rocket_admin_lift_key_battle_unlocked": false,
		"rocket_admin_lift_key_battle_started": false,
		"rocket_admin_lift_key_battle_finished": false,
		"gold_dust_ledger_recovered_seen": false,
		"team_moonlight_sleep_panel_seen": false,
		"giovanni_elevator_route_seen": false,
		"rocket_lift_key_obtained": false,
		"rocket_hideout_elevator_path_unlocked": false,
		"worldlink_celadon_rocket_hideout_b3f_batch_queued": false,
		"celadon_rocket_hideout_elevator_reached": false,
		"red_hideout_elevator_guard_seen": false,
		"bill_nexus_order_elevator_override_seen": false,
		"rocket_elevator_panel_restored_seen": false,
		"gold_dust_elevator_ledger_decoded_seen": false,
		"team_moonlight_elevator_sleep_signal_seen": false,
		"giovanni_command_floor_route_seen": false,
		"rocket_command_floor_path_unlocked": false,
		"worldlink_celadon_rocket_hideout_elevator_batch_queued": false,
		"worldlink_nugget_bridge_batch_queued": false,
	}
	worldlink_queue = [
		"red_route_1_tracks",
		"blue_first_battle_pressure",
		"oak_world_migration_alert",
		"nexus_island_locked",
	]


func set_flag(flag_name: String, value: bool) -> void:
	story_flags[flag_name] = value


func queue_worldlink_id(message_id: String) -> void:
	if not worldlink_queue.has(message_id):
		worldlink_queue.append(message_id)


func queue_worldlink_ids(message_ids: Array[String]) -> void:
	for message_id in message_ids:
		queue_worldlink_id(message_id)


func enter_route_1() -> void:
	current_scene = "route_1"
	set_flag("route_1_reached", true)
	queue_worldlink_id("route_1_reached")


func enter_viridian_city() -> void:
	current_scene = "viridian_city"
	set_flag("viridian_city_reached", true)
	queue_worldlink_id("viridian_city_reached")


func enter_route_2_forest_gate() -> void:
	current_scene = "route_2_forest_gate"
	active_companion = "red"
	set_flag("route_2_forest_gate_reached", true)
	set_flag("red_route_2_warning_seen", true)
	queue_worldlink_id("route_2_forest_gate_reached")


func enter_route_3() -> void:
	current_scene = "route_3"
	active_companion = "red"
	set_flag("route_3_reached", true)
	set_flag("red_route_3_migration_scene_seen", true)
	queue_worldlink_id("route_3_reached")


func enter_viridian_forest() -> void:
	current_scene = "viridian_forest"
	active_companion = "red"
	set_flag("viridian_forest_reached", true)
	set_flag("red_viridian_forest_scene_seen", true)
	queue_worldlink_id("viridian_forest_reached")


func record_rocket_forest_scout() -> void:
	set_flag("rocket_forest_scout_seen", true)
	queue_worldlink_id("rocket_forest_scout_seen")


func enter_pewter_city() -> void:
	current_scene = "pewter_city"
	active_companion = "red"
	set_flag("pewter_city_reached", true)
	queue_worldlink_id("pewter_city_reached")


func record_brock_pewter_intro() -> void:
	set_flag("brock_pewter_intro_seen", true)
	queue_worldlink_id("brock_pewter_intro_seen")


func record_red_pewter_training() -> void:
	active_companion = "red"
	set_flag("red_pewter_training_seen", true)
	queue_worldlink_id("red_pewter_training_seen")


func record_pewter_museum_anomaly() -> void:
	active_companion = "red"
	set_flag("pewter_museum_anomaly_seen", true)
	queue_pewter_museum_batch()


func queue_pewter_museum_batch() -> void:
	set_flag("worldlink_pewter_museum_batch_queued", true)
	queue_worldlink_ids([
		"wl_red_pewter_museum_scan",
		"wl_rocket_pewter_museum_anomaly",
		"wl_bill_fossil_energy_ping",
	])


func enter_mt_moon_entrance() -> void:
	current_scene = "mt_moon_entrance"
	active_companion = "red"
	set_flag("mt_moon_entrance_reached", true)
	set_flag("red_mt_moon_warning_seen", true)
	queue_worldlink_id("wl_red_mt_moon_warning")


func record_mt_moon_faction_conflict() -> void:
	active_companion = "red"
	set_flag("rocket_gold_dust_mt_moon_conflict_seen", true)
	set_flag("nexus_fossil_hint_seen", true)
	queue_mt_moon_faction_batch()


func queue_mt_moon_faction_batch() -> void:
	set_flag("worldlink_mt_moon_faction_batch_queued", true)
	queue_worldlink_ids([
		"wl_red_mt_moon_warning",
		"wl_rocket_mt_moon_fossil_grab",
		"wl_gold_dust_mt_moon_arrival",
		"wl_nexus_fossil_hint",
	])


func enter_mt_moon_interior_1() -> void:
	current_scene = "mt_moon_interior_1"
	active_companion = "red"
	set_flag("mt_moon_interior_1_reached", true)
	set_flag("red_mt_moon_interior_support_seen", true)
	queue_worldlink_id("wl_red_mt_moon_interior_support")


func record_mt_moon_split_path_scouting() -> void:
	active_companion = "red"
	set_flag("rocket_mt_moon_left_path_seen", true)
	set_flag("gold_dust_mt_moon_right_path_seen", true)
	set_flag("fossil_choice_setup_seen", true)
	queue_mt_moon_interior_split_batch()


func queue_mt_moon_interior_split_batch() -> void:
	set_flag("worldlink_mt_moon_interior_split_batch_queued", true)
	queue_worldlink_ids([
		"wl_red_mt_moon_interior_support",
		"wl_rocket_mt_moon_left_path",
		"wl_gold_dust_mt_moon_right_path",
		"wl_fossil_choice_setup",
	])


func enter_mt_moon_fossil_decision() -> void:
	current_scene = "mt_moon_fossil_decision"
	active_companion = "red"
	set_flag("mt_moon_fossil_decision_reached", true)
	set_flag("nexus_fossil_deeper_signal_seen", true)
	queue_mt_moon_fossil_decision_batch()


func choose_mt_moon_fossil(fossil_id: String) -> void:
	if bool(story_flags.get("mt_moon_fossil_choice_made", false)):
		return
	set_flag("mt_moon_fossil_choice_made", true)
	if fossil_id == "dome":
		set_flag("dome_fossil_chosen", true)
		set_flag("helix_fossil_chosen", false)
	elif fossil_id == "helix":
		set_flag("helix_fossil_chosen", true)
		set_flag("dome_fossil_chosen", false)
	queue_worldlink_id("wl_mt_moon_fossil_choice_made")


func queue_mt_moon_fossil_decision_batch() -> void:
	set_flag("worldlink_mt_moon_fossil_decision_batch_queued", true)
	queue_worldlink_ids([
		"wl_mt_moon_fossil_decision_reached",
		"wl_nexus_fossil_deeper_signal",
	])


func enter_route_4_cerulean_approach() -> void:
	current_scene = "route_4_cerulean_approach"
	active_companion = "red"
	set_flag("route_4_cerulean_approach_reached", true)
	queue_worldlink_id("wl_route_4_cerulean_approach")


func record_red_route_4_cerulean_warning() -> void:
	active_companion = "red"
	set_flag("red_route_4_cerulean_warning_seen", true)
	set_flag("cerulean_bridge_threat_teased", true)
	queue_route_4_cerulean_batch()


func queue_route_4_cerulean_batch() -> void:
	set_flag("worldlink_route_4_cerulean_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_4_cerulean_approach",
		"wl_red_route_4_cerulean_warning",
		"wl_cerulean_bridge_threat_tease",
	])


func enter_cerulean_city() -> void:
	current_scene = "cerulean_city"
	active_companion = "red"
	set_flag("cerulean_city_reached", true)
	queue_worldlink_id("wl_cerulean_city_reached")


func record_misty_cerulean_intro() -> void:
	active_companion = "red"
	set_flag("misty_cerulean_intro_seen", true)
	set_flag("nugget_bridge_threat_setup_seen", true)
	queue_cerulean_city_batch()


func queue_cerulean_city_batch() -> void:
	set_flag("worldlink_cerulean_city_batch_queued", true)
	queue_worldlink_ids([
		"wl_cerulean_city_reached",
		"wl_misty_cerulean_intro",
		"wl_nugget_bridge_threat_setup",
	])


func enter_nugget_bridge() -> void:
	current_scene = "nugget_bridge"
	active_companion = "red"
	set_flag("nugget_bridge_reached", true)
	queue_worldlink_id("wl_nugget_bridge_reached")


func record_nugget_bridge_scouting() -> void:
	active_companion = "red"
	set_flag("red_misty_nugget_bridge_scout_seen", true)
	queue_nugget_bridge_batch()


func queue_nugget_bridge_batch() -> void:
	set_flag("worldlink_nugget_bridge_batch_queued", true)
	queue_worldlink_ids([
		"wl_nugget_bridge_reached",
		"wl_nugget_bridge_scouting",
	])


func enter_route_25_bill() -> void:
	current_scene = "route_25_bill"
	active_companion = "red"
	set_flag("route_25_bill_reached", true)
	queue_worldlink_id("wl_route_25_bill_reached")


func record_bill_route25_intro() -> void:
	active_companion = "red"
	set_flag("bill_route25_intro_seen", true)
	set_flag("bill_storage_network_clue_seen", true)
	set_flag("nexus_network_first_decode_seen", true)
	queue_route_25_bill_batch()


func queue_route_25_bill_batch() -> void:
	set_flag("worldlink_route_25_bill_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_25_bill_reached",
		"wl_bill_route25_intro",
		"wl_bill_storage_network_clue",
		"wl_nexus_network_first_decode",
	])


func enter_cerulean_rocket_house() -> void:
	current_scene = "cerulean_rocket_house"
	active_companion = "red"
	set_flag("cerulean_rocket_house_reached", true)


func record_cerulean_house_theft() -> void:
	active_companion = "red"
	set_flag("cerulean_house_theft_seen", true)
	set_flag("rocket_stolen_tm_clue_seen", true)
	queue_cerulean_rocket_house_batch()


func queue_cerulean_rocket_house_batch() -> void:
	set_flag("worldlink_cerulean_rocket_house_batch_queued", true)
	queue_worldlink_ids([
		"wl_cerulean_house_theft_seen",
		"wl_rocket_stolen_tm_clue",
	])


func enter_route_5_underground_path() -> void:
	current_scene = "route_5_underground_path"
	active_companion = "red"
	set_flag("route_5_underground_path_reached", true)
	queue_worldlink_id("wl_route_5_underground_path_reached")


func record_underground_path_scouting() -> void:
	active_companion = "red"
	set_flag("underground_path_scouted", true)
	set_flag("vermilion_shipping_lead_seen", true)
	set_flag("vermilion_city_teased", true)
	queue_route_5_underground_path_batch()


func queue_route_5_underground_path_batch() -> void:
	set_flag("worldlink_route_5_underground_path_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_5_underground_path_reached",
		"wl_underground_path_scouted",
		"wl_vermilion_shipping_lead",
		"wl_vermilion_city_teased",
	])


func enter_vermilion_city() -> void:
	current_scene = "vermilion_city"
	active_companion = "red"
	set_flag("vermilion_city_reached", true)
	queue_worldlink_id("wl_vermilion_city_reached")


func record_vermilion_arrival_scene() -> void:
	active_companion = "red"
	set_flag("vermilion_harbor_scouted", true)
	set_flag("ss_anne_ticket_lead_seen", true)
	set_flag("surge_power_sabotage_teased", true)
	queue_vermilion_city_arrival_batch()


func queue_vermilion_city_arrival_batch() -> void:
	set_flag("worldlink_vermilion_city_arrival_batch_queued", true)
	queue_worldlink_ids([
		"wl_vermilion_city_reached",
		"wl_vermilion_harbor_scouted",
		"wl_ss_anne_ticket_lead",
		"wl_surge_power_sabotage_teased",
	])


func enter_ss_anne_ticket_office() -> void:
	current_scene = "ss_anne_ticket_office"
	active_companion = "red"
	set_flag("ss_anne_ticket_office_reached", true)
	queue_worldlink_id("wl_ss_anne_ticket_office_reached")


func record_ss_anne_ticket_office_scene() -> void:
	active_companion = "red"
	set_flag("ss_anne_manifest_checked", true)
	set_flag("bill_manifest_decode_seen", true)
	set_flag("red_harbor_guard_scene_seen", true)
	set_flag("ss_anne_boarding_pass_earned", true)
	queue_ss_anne_ticket_office_batch()


func queue_ss_anne_ticket_office_batch() -> void:
	set_flag("worldlink_ss_anne_ticket_office_batch_queued", true)
	queue_worldlink_ids([
		"wl_ss_anne_ticket_office_reached",
		"wl_ss_anne_manifest_checked",
		"wl_bill_manifest_decode_seen",
		"wl_red_harbor_guard_scene",
		"wl_ss_anne_boarding_pass_earned",
	])


func enter_ss_anne_main_deck() -> void:
	current_scene = "ss_anne_main_deck"
	active_companion = "red"
	set_flag("ss_anne_main_deck_reached", true)
	queue_worldlink_id("wl_ss_anne_boarded")


func record_ss_anne_deck_boarding_scene() -> void:
	active_companion = "red"
	set_flag("ss_anne_boarded", true)
	set_flag("red_ss_anne_boarding_scene_seen", true)
	set_flag("blue_ship_rival_teased", true)
	set_flag("rocket_cargo_hold_clue_seen", true)
	set_flag("captain_trail_cutter_lead_seen", true)
	queue_ss_anne_boarding_batch()


func queue_ss_anne_boarding_batch() -> void:
	set_flag("worldlink_ss_anne_boarding_batch_queued", true)
	queue_worldlink_ids([
		"wl_ss_anne_boarded",
		"wl_red_ss_anne_boarding_scene",
		"wl_blue_ship_rival_tease",
		"wl_rocket_cargo_hold_clue",
		"wl_captain_trail_cutter_lead",
	])


func queue_ss_anne_blue_battle_batch() -> void:
	set_flag("worldlink_ss_anne_blue_battle_batch_queued", true)
	queue_worldlink_ids([
		"wl_blue_ss_anne_battle_started",
		"wl_blue_ss_anne_battle_finished",
		"wl_blue_ss_anne_rival_respect",
	])


func enter_ss_anne_cargo_hold() -> void:
	current_scene = "ss_anne_cargo_hold"
	active_companion = "red"
	set_flag("ss_anne_cargo_hold_reached", true)
	queue_worldlink_id("wl_ss_anne_cargo_hold_reached")


func record_ss_anne_cargo_hold_investigation() -> void:
	active_companion = "red"
	set_flag("rocket_cargo_manifest_recovered", true)
	set_flag("nexus_order_crate_symbol_seen", true)
	set_flag("bill_cargo_decode_seen", true)
	set_flag("misty_lower_deck_waterline_seen", true)
	set_flag("red_cargo_hold_guard_seen", true)
	set_flag("ss_anne_captain_path_unlocked", true)
	queue_ss_anne_cargo_hold_batch()


func queue_ss_anne_cargo_hold_batch() -> void:
	set_flag("worldlink_ss_anne_cargo_hold_batch_queued", true)
	queue_worldlink_ids([
		"wl_ss_anne_cargo_hold_reached",
		"wl_rocket_cargo_manifest_recovered",
		"wl_nexus_order_crate_symbol_seen",
		"wl_bill_cargo_decode_seen",
		"wl_misty_lower_deck_waterline_seen",
		"wl_red_cargo_hold_guard_seen",
		"wl_ss_anne_captain_path_unlocked",
	])


func enter_ss_anne_captain_cabin() -> void:
	current_scene = "ss_anne_captain_cabin"
	active_companion = "red"
	set_flag("ss_anne_captain_cabin_reached", true)
	queue_worldlink_id("wl_ss_anne_captain_cabin_reached")


func record_ss_anne_captain_cabin_scene() -> void:
	active_companion = "red"
	set_flag("captain_seasick_scene_seen", true)
	set_flag("trail_cutter_obtained", true)
	set_flag("trail_cutter_field_tool_unlocked", true)
	set_flag("surge_gym_access_unlocked", true)
	queue_ss_anne_captain_cabin_batch()


func queue_ss_anne_captain_cabin_batch() -> void:
	set_flag("worldlink_ss_anne_captain_cabin_batch_queued", true)
	queue_worldlink_ids([
		"wl_ss_anne_captain_cabin_reached",
		"wl_captain_seasick_scene_seen",
		"wl_trail_cutter_obtained",
		"wl_trail_cutter_field_tool_unlocked",
		"wl_surge_gym_access_unlocked",
	])


func enter_vermilion_power_sabotage() -> void:
	current_scene = "vermilion_power_sabotage"
	active_companion = "red"
	set_flag("vermilion_power_sabotage_reached", true)
	queue_worldlink_id("wl_vermilion_power_sabotage_reached")


func record_vermilion_power_sabotage_scene() -> void:
	active_companion = "red"
	set_flag("rocket_gas_power_sabotage_seen", true)
	set_flag("team_gas_kanto_debut_seen", true)
	set_flag("red_misty_surge_prep_seen", true)
	set_flag("bill_power_grid_decode_seen", true)
	set_flag("surge_gym_battle_unlocked", true)
	queue_vermilion_power_sabotage_batch()


func queue_vermilion_power_sabotage_batch() -> void:
	set_flag("worldlink_vermilion_power_sabotage_batch_queued", true)
	queue_worldlink_ids([
		"wl_vermilion_power_sabotage_reached",
		"wl_rocket_gas_power_sabotage",
		"wl_team_gas_kanto_debut",
		"wl_red_misty_surge_prep",
		"wl_bill_power_grid_decode",
		"wl_surge_gym_battle_unlocked",
	])


func queue_vermilion_surge_gym_batch() -> void:
	set_flag("worldlink_vermilion_surge_gym_batch_queued", true)
	queue_worldlink_ids([
		"wl_surge_vermilion_gym_started",
		"wl_surge_vermilion_gym_finished",
		"wl_thunder_badge_earned",
		"wl_surge_respect_scene",
		"wl_route_11_path_unlocked",
	])


func enter_route_11() -> void:
	current_scene = "route_11"
	active_companion = "red"
	set_flag("route_11_reached", true)
	queue_worldlink_id("wl_route_11_reached")


func record_route_11_handoff_scene() -> void:
	active_companion = "red"
	set_flag("red_route_11_eastbound_scene_seen", true)
	set_flag("misty_route_11_farewell_seen", true)
	set_flag("bill_route_11_signal_decode_seen", true)
	set_flag("rocket_gas_route_11_fallout_seen", true)
	set_flag("snorlax_roadblock_teased", true)
	queue_route_11_handoff_batch()


func queue_route_11_handoff_batch() -> void:
	set_flag("worldlink_route_11_handoff_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_11_reached",
		"wl_red_route_11_eastbound_scene",
		"wl_misty_route_11_farewell",
		"wl_bill_route_11_signal_decode",
		"wl_rocket_gas_route_11_fallout",
		"wl_snorlax_roadblock_teased",
	])


func enter_diglett_cave_detour() -> void:
	current_scene = "diglett_cave_detour"
	active_companion = "red"
	set_flag("diglett_cave_detour_reached", true)
	queue_worldlink_id("wl_diglett_cave_detour_reached")


func record_diglett_cave_detour_scene() -> void:
	active_companion = "red"
	set_flag("red_diglett_cave_guard_seen", true)
	set_flag("bill_diglett_cave_relay_map_seen", true)
	set_flag("rocket_gold_dust_cave_argument_seen", true)
	set_flag("snorlax_route_12_block_confirmed", true)
	set_flag("echo_flute_lead_seen", true)
	queue_diglett_cave_detour_batch()


func queue_diglett_cave_detour_batch() -> void:
	set_flag("worldlink_diglett_cave_detour_batch_queued", true)
	queue_worldlink_ids([
		"wl_diglett_cave_detour_reached",
		"wl_red_diglett_cave_guard",
		"wl_bill_diglett_cave_relay_map",
		"wl_rocket_gold_dust_cave_argument",
		"wl_snorlax_route_12_block_confirmed",
		"wl_echo_flute_lead_seen",
	])


func enter_route_2_east_field_lab() -> void:
	current_scene = "route_2_east_field_lab"
	active_companion = "red"
	set_flag("route_2_east_field_lab_reached", true)
	queue_worldlink_id("wl_route_2_east_field_lab_reached")


func record_route_2_field_lab_scene() -> void:
	active_companion = "red"
	set_flag("red_route_2_east_exit_seen", true)
	set_flag("bill_echo_flute_decoder_seen", true)
	set_flag("oak_aide_field_tool_brief_seen", true)
	set_flag("rocket_moonlight_sleep_signal_seen", true)
	set_flag("lavender_signal_path_teased", true)
	set_flag("route_9_rock_tunnel_path_unlocked", true)
	queue_route_2_east_field_lab_batch()


func queue_route_2_east_field_lab_batch() -> void:
	set_flag("worldlink_route_2_east_field_lab_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_2_east_field_lab_reached",
		"wl_red_route_2_east_exit",
		"wl_bill_echo_flute_decoder",
		"wl_oak_aide_field_tool_brief",
		"wl_rocket_moonlight_sleep_signal",
		"wl_lavender_signal_path_teased",
		"wl_route_9_rock_tunnel_path_unlocked",
	])


func enter_route_9_rock_tunnel_approach() -> void:
	current_scene = "route_9_rock_tunnel_approach"
	active_companion = "red"
	set_flag("route_9_rock_tunnel_approach_reached", true)
	queue_worldlink_id("wl_route_9_rock_tunnel_approach_reached")


func record_route_9_approach_scene() -> void:
	active_companion = "red"
	set_flag("red_route_9_trainer_lane_seen", true)
	set_flag("bill_rock_tunnel_darkness_warning_seen", true)
	set_flag("team_moonlight_route_9_debut_seen", true)
	set_flag("rocket_route_9_supply_cache_seen", true)
	set_flag("lavender_tower_signal_confirmed", true)
	set_flag("rock_tunnel_entry_unlocked", true)
	queue_route_9_rock_tunnel_approach_batch()


func queue_route_9_rock_tunnel_approach_batch() -> void:
	set_flag("worldlink_route_9_rock_tunnel_approach_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_9_rock_tunnel_approach_reached",
		"wl_red_route_9_trainer_lane",
		"wl_bill_rock_tunnel_darkness_warning",
		"wl_team_moonlight_route_9_debut",
		"wl_rocket_route_9_supply_cache",
		"wl_lavender_tower_signal_confirmed",
		"wl_rock_tunnel_entry_unlocked",
	])


func enter_rock_tunnel_interior() -> void:
	current_scene = "rock_tunnel_interior"
	active_companion = "red"
	set_flag("rock_tunnel_interior_reached", true)
	queue_worldlink_id("wl_rock_tunnel_interior_reached")


func record_rock_tunnel_interior_scene() -> void:
	active_companion = "red"
	set_flag("red_rock_tunnel_guidance_seen", true)
	set_flag("bill_lavender_echo_trace_seen", true)
	set_flag("team_moonlight_cave_pressure_seen", true)
	set_flag("rocket_dark_cache_seen", true)
	set_flag("flash_lantern_needed_seen", true)
	set_flag("lavender_exit_path_unlocked", true)
	queue_rock_tunnel_interior_batch()


func queue_rock_tunnel_interior_batch() -> void:
	set_flag("worldlink_rock_tunnel_interior_batch_queued", true)
	queue_worldlink_ids([
		"wl_rock_tunnel_interior_reached",
		"wl_red_rock_tunnel_guidance",
		"wl_bill_lavender_echo_trace",
		"wl_team_moonlight_cave_pressure",
		"wl_rocket_dark_cache",
		"wl_flash_lantern_needed",
		"wl_lavender_exit_path_unlocked",
	])


func enter_lavender_outskirts() -> void:
	current_scene = "lavender_outskirts"
	active_companion = "red"
	set_flag("lavender_outskirts_reached", true)
	queue_worldlink_id("wl_lavender_outskirts_reached")


func record_lavender_outskirts_scene() -> void:
	active_companion = "red"
	set_flag("red_lavender_arrival_seen", true)
	set_flag("bill_pokemon_tower_signal_decode_seen", true)
	set_flag("team_moonlight_lavender_presence_seen", true)
	set_flag("rocket_lavender_surveillance_seen", true)
	set_flag("pokemon_tower_signal_confirmed", true)
	set_flag("pokemon_tower_entry_unlocked", true)
	queue_lavender_outskirts_batch()


func queue_lavender_outskirts_batch() -> void:
	set_flag("worldlink_lavender_outskirts_batch_queued", true)
	queue_worldlink_ids([
		"wl_lavender_outskirts_reached",
		"wl_red_lavender_arrival",
		"wl_bill_pokemon_tower_signal_decode",
		"wl_team_moonlight_lavender_presence",
		"wl_rocket_lavender_surveillance",
		"wl_pokemon_tower_signal_confirmed",
		"wl_pokemon_tower_entry_unlocked",
	])


func enter_pokemon_tower_first_floor() -> void:
	current_scene = "pokemon_tower_first_floor"
	active_companion = "red"
	set_flag("pokemon_tower_first_floor_reached", true)
	queue_worldlink_id("wl_pokemon_tower_first_floor_reached")


func record_pokemon_tower_first_floor_scene() -> void:
	active_companion = "red"
	set_flag("red_pokemon_tower_guard_seen", true)
	set_flag("bill_tower_echo_flute_distortion_seen", true)
	set_flag("team_moonlight_tower_pressure_seen", true)
	set_flag("rocket_tower_grunt_seen", true)
	set_flag("cubone_mr_fuji_thread_seen", true)
	set_flag("silph_scope_need_seen", true)
	set_flag("pokemon_tower_deeper_path_locked", true)
	queue_pokemon_tower_first_floor_batch()


func queue_pokemon_tower_first_floor_batch() -> void:
	set_flag("worldlink_pokemon_tower_first_floor_batch_queued", true)
	queue_worldlink_ids([
		"wl_pokemon_tower_first_floor_reached",
		"wl_red_pokemon_tower_guard",
		"wl_bill_tower_echo_flute_distortion",
		"wl_team_moonlight_tower_pressure",
		"wl_rocket_tower_grunt_seen",
		"wl_cubone_mr_fuji_thread",
		"wl_silph_scope_need_seen",
		"wl_pokemon_tower_deeper_path_locked",
	])


func enter_route_8_celadon_road() -> void:
	current_scene = "route_8_celadon_road"
	active_companion = "red"
	set_flag("route_8_celadon_road_reached", true)
	queue_worldlink_id("wl_route_8_celadon_road_reached")


func record_route_8_celadon_road_scene() -> void:
	active_companion = "red"
	set_flag("red_route_8_westbound_seen", true)
	set_flag("bill_silph_scope_celadon_trace_seen", true)
	set_flag("rocket_celadon_game_corner_lead_seen", true)
	set_flag("team_moonlight_route_8_shadow_seen", true)
	set_flag("underground_path_to_celadon_unlocked", true)
	set_flag("celadon_city_teased", true)
	queue_route_8_celadon_road_batch()


func queue_route_8_celadon_road_batch() -> void:
	set_flag("worldlink_route_8_celadon_road_batch_queued", true)
	queue_worldlink_ids([
		"wl_route_8_celadon_road_reached",
		"wl_red_route_8_westbound",
		"wl_bill_silph_scope_celadon_trace",
		"wl_rocket_celadon_game_corner_lead",
		"wl_team_moonlight_route_8_shadow",
		"wl_underground_path_to_celadon_unlocked",
		"wl_celadon_city_teased",
	])


func enter_celadon_underground_path() -> void:
	current_scene = "celadon_underground_path"
	active_companion = "red"
	set_flag("celadon_underground_path_reached", true)
	queue_worldlink_id("wl_celadon_underground_path_reached")


func record_celadon_underground_path_scene() -> void:
	active_companion = "red"
	set_flag("red_celadon_underpass_guard_seen", true)
	set_flag("bill_game_corner_signal_trace_seen", true)
	set_flag("rocket_underpass_smuggler_seen", true)
	set_flag("team_moonlight_dream_poster_seen", true)
	set_flag("silph_scope_game_corner_confirmed", true)
	set_flag("celadon_city_arrival_unlocked", true)
	queue_celadon_underground_path_batch()


func queue_celadon_underground_path_batch() -> void:
	set_flag("worldlink_celadon_underground_path_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_underground_path_reached",
		"wl_red_celadon_underpass_guard",
		"wl_bill_game_corner_signal_trace",
		"wl_rocket_underpass_smuggler",
		"wl_team_moonlight_dream_poster",
		"wl_silph_scope_game_corner_confirmed",
		"wl_celadon_city_arrival_unlocked",
	])


func enter_celadon_city() -> void:
	current_scene = "celadon_city"
	active_companion = "red"
	set_flag("celadon_city_reached", true)
	queue_worldlink_id("wl_celadon_city_reached")


func record_celadon_city_arrival_scene() -> void:
	active_companion = "red"
	set_flag("red_celadon_city_arrival_seen", true)
	set_flag("bill_game_corner_exterior_signal_seen", true)
	set_flag("rocket_game_corner_front_seen", true)
	set_flag("team_moonlight_celadon_ad_seen", true)
	set_flag("erika_gym_teased_seen", true)
	set_flag("game_corner_investigation_unlocked", true)
	queue_celadon_city_arrival_batch()


func queue_celadon_city_arrival_batch() -> void:
	set_flag("worldlink_celadon_city_arrival_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_city_reached",
		"wl_red_celadon_city_arrival",
		"wl_bill_game_corner_exterior_signal",
		"wl_rocket_game_corner_front",
		"wl_team_moonlight_celadon_ad",
		"wl_erika_gym_teased",
		"wl_game_corner_investigation_unlocked",
	])


func enter_celadon_game_corner_exterior() -> void:
	current_scene = "celadon_game_corner_exterior"
	active_companion = "red"
	set_flag("game_corner_exterior_reached", true)
	queue_worldlink_id("wl_game_corner_exterior_reached")


func record_celadon_game_corner_exterior_scene() -> void:
	active_companion = "red"
	set_flag("red_game_corner_door_guard_seen", true)
	set_flag("bill_coin_case_signal_seen", true)
	set_flag("rocket_game_corner_guard_exposed", true)
	set_flag("team_moonlight_sleep_coin_seen", true)
	set_flag("game_corner_guard_battle_unlocked", true)
	queue_celadon_game_corner_exterior_batch()


func queue_celadon_game_corner_exterior_batch() -> void:
	set_flag("worldlink_celadon_game_corner_exterior_batch_queued", true)
	queue_worldlink_ids([
		"wl_game_corner_exterior_reached",
		"wl_red_game_corner_door_guard",
		"wl_bill_coin_case_signal",
		"wl_rocket_game_corner_guard_exposed",
		"wl_team_moonlight_sleep_coin",
		"wl_game_corner_guard_battle_unlocked",
	])


func enter_celadon_rocket_hideout_entry() -> void:
	current_scene = "celadon_rocket_hideout_entry"
	active_companion = "red"
	set_flag("celadon_rocket_hideout_entry_reached", true)
	queue_worldlink_id("wl_celadon_rocket_hideout_entry_reached")


func record_celadon_rocket_hideout_entry_scene() -> void:
	active_companion = "red"
	set_flag("red_hideout_entry_watch_seen", true)
	set_flag("bill_hideout_elevator_signal_seen", true)
	set_flag("rocket_lift_key_required_seen", true)
	set_flag("giovanni_hideout_command_seen", true)
	set_flag("team_moonlight_rocket_interference_seen", true)
	set_flag("rocket_hideout_b1f_path_unlocked", true)
	queue_celadon_rocket_hideout_entry_batch()


func queue_celadon_rocket_hideout_entry_batch() -> void:
	set_flag("worldlink_celadon_rocket_hideout_entry_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_rocket_hideout_entry_reached",
		"wl_red_hideout_entry_watch",
		"wl_bill_hideout_elevator_signal",
		"wl_rocket_lift_key_required",
		"wl_giovanni_hideout_command",
		"wl_team_moonlight_rocket_interference",
		"wl_rocket_hideout_b1f_path_unlocked",
	])


func enter_celadon_rocket_hideout_b1f() -> void:
	current_scene = "celadon_rocket_hideout_b1f"
	active_companion = "red"
	set_flag("celadon_rocket_hideout_b1f_reached", true)
	queue_worldlink_id("wl_celadon_rocket_hideout_b1f_reached")


func record_celadon_rocket_hideout_b1f_scene() -> void:
	active_companion = "red"
	set_flag("red_hideout_b1f_maze_guard_seen", true)
	set_flag("bill_silph_scope_machine_trace_seen", true)
	set_flag("rocket_spinner_maze_seen", true)
	set_flag("gold_dust_hideout_infiltration_seen", true)
	set_flag("team_moonlight_hideout_signal_bleed_seen", true)
	set_flag("lift_key_deeper_trail_seen", true)
	set_flag("rocket_hideout_b2f_path_unlocked", true)
	queue_celadon_rocket_hideout_b1f_batch()


func queue_celadon_rocket_hideout_b1f_batch() -> void:
	set_flag("worldlink_celadon_rocket_hideout_b1f_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_rocket_hideout_b1f_reached",
		"wl_red_hideout_b1f_maze_guard",
		"wl_bill_silph_scope_machine_trace",
		"wl_rocket_spinner_maze",
		"wl_gold_dust_hideout_infiltration",
		"wl_team_moonlight_hideout_signal_bleed",
		"wl_lift_key_deeper_trail",
		"wl_rocket_hideout_b2f_path_unlocked",
	])


func enter_celadon_rocket_hideout_b2f() -> void:
	current_scene = "celadon_rocket_hideout_b2f"
	active_companion = "red"
	set_flag("celadon_rocket_hideout_b2f_reached", true)
	queue_worldlink_id("wl_celadon_rocket_hideout_b2f_reached")


func record_celadon_rocket_hideout_b2f_scene() -> void:
	active_companion = "red"
	set_flag("red_hideout_b2f_patrol_warning_seen", true)
	set_flag("bill_stolen_silph_scope_crate_seen", true)
	set_flag("rocket_hideout_b2f_patrol_battle_unlocked", true)
	set_flag("rocket_gold_dust_b2f_conflict_seen", true)
	set_flag("team_moonlight_control_room_interference_seen", true)
	set_flag("lift_key_b3f_route_seen", true)
	queue_celadon_rocket_hideout_b2f_batch()


func queue_celadon_rocket_hideout_b2f_batch() -> void:
	set_flag("worldlink_celadon_rocket_hideout_b2f_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_rocket_hideout_b2f_reached",
		"wl_red_hideout_b2f_patrol_warning",
		"wl_bill_stolen_silph_scope_crate",
		"wl_rocket_hideout_b2f_patrol_unlocked",
		"wl_rocket_gold_dust_b2f_conflict",
		"wl_team_moonlight_control_room_interference",
		"wl_lift_key_b3f_route_seen",
	])


func enter_celadon_rocket_hideout_b3f() -> void:
	current_scene = "celadon_rocket_hideout_b3f"
	active_companion = "red"
	set_flag("celadon_rocket_hideout_b3f_reached", true)
	queue_worldlink_id("wl_celadon_rocket_hideout_b3f_reached")


func record_celadon_rocket_hideout_b3f_scene() -> void:
	active_companion = "red"
	set_flag("red_hideout_b3f_lift_key_warning_seen", true)
	set_flag("bill_nexus_order_elevator_trace_seen", true)
	set_flag("rocket_admin_lift_key_battle_unlocked", true)
	set_flag("gold_dust_ledger_recovered_seen", true)
	set_flag("team_moonlight_sleep_panel_seen", true)
	set_flag("giovanni_elevator_route_seen", true)
	queue_celadon_rocket_hideout_b3f_batch()


func queue_celadon_rocket_hideout_b3f_batch() -> void:
	set_flag("worldlink_celadon_rocket_hideout_b3f_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_rocket_hideout_b3f_reached",
		"wl_red_hideout_b3f_lift_key_warning",
		"wl_bill_nexus_order_elevator_trace",
		"wl_rocket_admin_lift_key_battle_unlocked",
		"wl_gold_dust_ledger_recovered",
		"wl_team_moonlight_sleep_panel",
		"wl_giovanni_elevator_route_seen",
	])


func enter_celadon_rocket_hideout_elevator() -> void:
	current_scene = "celadon_rocket_hideout_elevator"
	active_companion = "red"
	set_flag("celadon_rocket_hideout_elevator_reached", true)
	queue_worldlink_id("wl_celadon_rocket_hideout_elevator_reached")


func record_celadon_rocket_hideout_elevator_scene() -> void:
	active_companion = "red"
	set_flag("red_hideout_elevator_guard_seen", true)
	set_flag("bill_nexus_order_elevator_override_seen", true)
	set_flag("rocket_elevator_panel_restored_seen", true)
	set_flag("gold_dust_elevator_ledger_decoded_seen", true)
	set_flag("team_moonlight_elevator_sleep_signal_seen", true)
	set_flag("giovanni_command_floor_route_seen", true)
	set_flag("rocket_command_floor_path_unlocked", true)
	queue_celadon_rocket_hideout_elevator_batch()


func queue_celadon_rocket_hideout_elevator_batch() -> void:
	set_flag("worldlink_celadon_rocket_hideout_elevator_batch_queued", true)
	queue_worldlink_ids([
		"wl_celadon_rocket_hideout_elevator_reached",
		"wl_red_hideout_elevator_guard",
		"wl_bill_nexus_order_elevator_override",
		"wl_rocket_elevator_panel_restored",
		"wl_gold_dust_elevator_ledger_decoded",
		"wl_team_moonlight_elevator_sleep_signal",
		"wl_giovanni_command_floor_route_seen",
		"wl_rocket_command_floor_path_unlocked",
	])


func record_viridian_center_visit() -> void:
	set_flag("viridian_center_visited", true)
	queue_worldlink_id("viridian_center_visited")


func record_viridian_mart_visit() -> void:
	set_flag("viridian_mart_visited", true)
	queue_worldlink_id("viridian_mart_visited")


func record_viridian_red_scene() -> void:
	active_companion = "red"
	set_flag("viridian_red_scene_seen", true)
	queue_viridian_story_batch()
	queue_worldlink_id("wl_red_viridian_checkin")


func record_viridian_rocket_clue() -> void:
	set_flag("viridian_rocket_clue_found", true)
	queue_viridian_story_batch()
	queue_worldlink_id("wl_rocket_viridian_clue")


func queue_viridian_story_batch() -> void:
	set_flag("worldlink_viridian_story_batch_queued", true)
	queue_worldlink_ids([
		"wl_red_viridian_checkin",
		"wl_blue_viridian_sighting",
	])


func choose_starter(selection: Dictionary) -> void:
	player_starter = selection.get("player_starter", "")
	player_starter_group = selection.get("player_starter_group", "")
	blue_starter = selection.get("blue_starter", "")
	ava_starter = selection.get("ava_starter", "")
	dax_starter = selection.get("dax_starter", "")
	current_scene = "oak_lab"
	set_flag("starter_chosen", true)
	set_flag("blue_pressure_scene_seen", true)
	_add_to_party(player_starter)
	queue_worldlink_id("starter_chosen_" + player_starter.to_lower())
	queue_worldlink_id("blue_chose_" + blue_starter.to_lower())


func record_red_route_1_scene() -> void:
	active_companion = "red"
	set_flag("red_route_1_companion_scene_seen", true)
	queue_worldlink_id("red_route_1_companion")


func record_blue_battle_placeholder() -> void:
	set_flag("blue_battle_placeholder_seen", true)
	queue_worldlink_id("blue_route_1_battle_placeholder")


func unlock_route_1_rumors() -> void:
	set_flag("route_1_rumors_unlocked", true)
	queue_worldlink_ids([
		"rumor_route_1_unusual_tracks",
		"rumor_route_1_starter_migration",
		"rumor_route_1_blue_shortcut",
	])


func queue_route_1_rival_batch() -> void:
	set_flag("worldlink_route_1_rival_batch_queued", true)
	queue_worldlink_ids([
		"wl_blue_route_1_battle_done",
		"wl_ava_route_1_capture",
		"wl_dax_route_1_training",
		"wl_red_route_1_checkin",
		"wl_silver_johto_tease",
	])


func start_battle_placeholder(battle_id: String) -> void:
	active_battle_id = battle_id
	last_battle_result = ""
	if battle_id == "blue_route_1":
		set_flag("blue_route_1_battle_started", true)
	if battle_id == "blue_ss_anne":
		set_flag("blue_ss_anne_battle_started", true)
		queue_worldlink_id("wl_blue_ss_anne_battle_started")
	if battle_id == "brock_pewter_gym":
		set_flag("brock_pewter_gym_started", true)
	if battle_id == "mt_moon_rocket_left_path":
		set_flag("mt_moon_rocket_left_battle_started", true)
		set_flag("red_mt_moon_tag_setup_seen", true)
	if battle_id == "mt_moon_gold_dust_right_path":
		set_flag("mt_moon_gold_dust_right_battle_started", true)
		set_flag("gold_dust_helix_claim_blocked", true)
	if battle_id == "nugget_bridge_recruiter_1":
		set_flag("nugget_bridge_recruiter_1_battle_started", true)
	if battle_id == "nugget_bridge_captain":
		set_flag("nugget_bridge_captain_battle_started", true)
	if battle_id == "misty_cerulean_gym":
		set_flag("misty_cerulean_gym_started", true)
	if battle_id == "cerulean_rocket_house_thief":
		set_flag("cerulean_rocket_house_thief_battle_started", true)
	if battle_id == "lt_surge_vermilion_gym":
		set_flag("surge_vermilion_gym_started", true)
		queue_worldlink_id("wl_surge_vermilion_gym_started")
	if battle_id == "rocket_game_corner_guard":
		set_flag("rocket_game_corner_guard_battle_started", true)
	if battle_id == "rocket_hideout_b2f_patrol":
		set_flag("rocket_hideout_b2f_patrol_battle_started", true)
	if battle_id == "rocket_hideout_b3f_admin":
		set_flag("rocket_admin_lift_key_battle_started", true)


func finish_battle_placeholder(result: String) -> void:
	last_battle_result = result
	if active_battle_id == "blue_route_1":
		set_flag("blue_route_1_battle_finished", true)
		queue_worldlink_id("blue_route_1_battle_finished")
		unlock_route_1_rumors()
		queue_route_1_rival_batch()
	if active_battle_id == "blue_ss_anne":
		set_flag("blue_ss_anne_battle_finished", true)
		set_flag("blue_ss_anne_rival_respect_seen", true)
		queue_ss_anne_blue_battle_batch()
	if active_battle_id == "brock_pewter_gym":
		set_flag("brock_pewter_gym_finished", true)
		set_flag("brock_pewter_badge_earned", true)
		queue_worldlink_id("brock_pewter_gym_finished")
	if active_battle_id == "mt_moon_rocket_left_path":
		set_flag("mt_moon_rocket_left_battle_finished", true)
		queue_worldlink_id("mt_moon_rocket_left_battle_finished")
	if active_battle_id == "mt_moon_gold_dust_right_path":
		set_flag("mt_moon_gold_dust_right_battle_finished", true)
		queue_worldlink_id("mt_moon_gold_dust_right_battle_finished")
	if active_battle_id == "nugget_bridge_recruiter_1":
		set_flag("nugget_bridge_recruiter_1_battle_finished", true)
		queue_worldlink_id("nugget_bridge_recruiter_1_battle_finished")
		queue_worldlink_id("wl_nugget_bridge_recruiter_1_battle_finished")
	if active_battle_id == "nugget_bridge_captain":
		set_flag("nugget_bridge_captain_battle_finished", true)
		set_flag("nugget_bridge_crisis_cleared", true)
		set_flag("misty_gym_unlocked", true)
		queue_worldlink_id("wl_nugget_bridge_captain_battle_finished")
		queue_worldlink_id("wl_nugget_bridge_crisis_cleared")
	if active_battle_id == "misty_cerulean_gym":
		set_flag("misty_cerulean_gym_finished", true)
		set_flag("cascade_badge_earned", true)
		set_flag("misty_recurring_friend_unlocked", true)
		queue_worldlink_id("wl_misty_cerulean_gym_finished")
		queue_worldlink_id("wl_misty_cascade_badge_earned")
		queue_worldlink_id("wl_misty_recurring_friend_unlocked")
	if active_battle_id == "cerulean_rocket_house_thief":
		set_flag("cerulean_rocket_house_thief_battle_finished", true)
		set_flag("stolen_tm_recovered", true)
		set_flag("route_5_vermilion_path_unlocked", true)
		queue_worldlink_id("wl_stolen_tm_recovered")
		queue_worldlink_id("wl_route_5_vermilion_path_unlocked")
	if active_battle_id == "lt_surge_vermilion_gym":
		set_flag("surge_vermilion_gym_finished", true)
		set_flag("thunder_badge_earned", true)
		set_flag("surge_respect_scene_seen", true)
		set_flag("route_11_path_unlocked", true)
		queue_vermilion_surge_gym_batch()
	if active_battle_id == "rocket_game_corner_guard":
		set_flag("rocket_game_corner_guard_battle_finished", true)
		set_flag("rocket_hideout_switch_lead_seen", true)
		set_flag("game_corner_hideout_entry_unlocked", true)
		queue_worldlink_id("wl_rocket_game_corner_guard_battle_finished")
		queue_worldlink_id("wl_rocket_hideout_switch_lead_seen")
		queue_worldlink_id("wl_game_corner_hideout_entry_unlocked")
	if active_battle_id == "rocket_hideout_b2f_patrol":
		set_flag("rocket_hideout_b2f_patrol_battle_finished", true)
		set_flag("rocket_hideout_b3f_path_unlocked", true)
		queue_worldlink_id("wl_rocket_hideout_b2f_patrol_finished")
		queue_worldlink_id("wl_rocket_hideout_b3f_path_unlocked")
	if active_battle_id == "rocket_hideout_b3f_admin":
		set_flag("rocket_admin_lift_key_battle_finished", true)
		set_flag("rocket_lift_key_obtained", true)
		set_flag("rocket_hideout_elevator_path_unlocked", true)
		queue_worldlink_id("wl_rocket_admin_lift_key_battle_finished")
		queue_worldlink_id("wl_rocket_lift_key_obtained")
		queue_worldlink_id("wl_rocket_hideout_elevator_path_unlocked")
	active_battle_id = ""


func start_wild_encounter(encounter: Dictionary) -> void:
	active_encounter_data = encounter.duplicate(true)
	active_encounter_id = str(active_encounter_data.get("id", ""))
	encounter_return_scene = str(active_encounter_data.get("return_scene", current_scene))
	last_encounter_result = ""
	if active_encounter_id == "route_1_first_wild":
		set_flag("route_1_first_wild_seen", true)
	if active_encounter_id == "route_2_red_catch_tutorial_pidgey":
		set_flag("route_2_catch_tutorial_seen", true)
	queue_worldlink_id(active_encounter_id + "_seen")


func finish_wild_encounter(result: String) -> void:
	last_encounter_result = result
	if result in ["catch_success", "placeholder_catch"] and not active_encounter_data.is_empty():
		var species := str(active_encounter_data.get("species", ""))
		if species != "":
			_add_capture(species)
		if active_encounter_id == "route_1_first_wild":
			set_flag("route_1_first_wild_caught", true)
			queue_worldlink_id("route_1_first_wild_caught")
		if active_encounter_id == "route_2_red_catch_tutorial_pidgey":
			set_flag("route_2_catch_tutorial_caught", true)
			queue_worldlink_id("route_2_catch_tutorial_caught")
	active_encounter_id = ""
	active_encounter_data = {}


func _add_capture(species: String) -> void:
	if not captured_creatures.has(species):
		captured_creatures.append(species)
	_add_to_party(species)


func _add_to_party(species: String) -> void:
	if species == "":
		return
	if party_roster.has(species):
		return
	if party_roster.size() < 6:
		party_roster.append(species)
