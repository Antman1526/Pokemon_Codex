extends RefCounted

var player_name := "Antman"
var current_region := "kanto"
var current_scene := "bedroom"
var active_companion := "red"
var player_starter := ""
var player_starter_group := ""
var blue_starter := ""
var ava_starter := ""
var dax_starter := ""
var active_battle_id := ""
var last_battle_result := ""
var story_flags: Dictionary = {}
var worldlink_queue: Array[String] = []


func start_new_game(name: String) -> void:
	player_name = name
	current_region = "kanto"
	current_scene = "bedroom"
	active_companion = "red"
	player_starter = ""
	player_starter_group = ""
	blue_starter = ""
	ava_starter = ""
	dax_starter = ""
	active_battle_id = ""
	last_battle_result = ""
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


func choose_starter(selection: Dictionary) -> void:
	player_starter = selection.get("player_starter", "")
	player_starter_group = selection.get("player_starter_group", "")
	blue_starter = selection.get("blue_starter", "")
	ava_starter = selection.get("ava_starter", "")
	dax_starter = selection.get("dax_starter", "")
	current_scene = "oak_lab"
	set_flag("starter_chosen", true)
	set_flag("blue_pressure_scene_seen", true)
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


func finish_battle_placeholder(result: String) -> void:
	last_battle_result = result
	if active_battle_id == "blue_route_1":
		set_flag("blue_route_1_battle_finished", true)
		queue_worldlink_id("blue_route_1_battle_finished")
		unlock_route_1_rumors()
		queue_route_1_rival_batch()
	active_battle_id = ""
