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


func finish_battle_placeholder(result: String) -> void:
	last_battle_result = result
	if active_battle_id == "blue_route_1":
		set_flag("blue_route_1_battle_finished", true)
		queue_worldlink_id("blue_route_1_battle_finished")
		unlock_route_1_rumors()
		queue_route_1_rival_batch()
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
