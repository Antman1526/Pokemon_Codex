extends RefCounted

var player_name := "Antman"
var current_region := "kanto"
var current_scene := "bedroom"
var active_companion := "red"
var story_flags: Dictionary = {}
var worldlink_queue: Array[String] = []


func start_new_game(name: String) -> void:
	player_name = name
	current_region = "kanto"
	current_scene = "bedroom"
	active_companion = "red"
	story_flags = {
		"started_native_shell": true,
		"mom_opening_scene_seen": false,
	}
	worldlink_queue = [
		"red_route_1_tracks",
		"blue_first_battle_pressure",
		"oak_world_migration_alert",
	]


func set_flag(flag_name: String, value: bool) -> void:
	story_flags[flag_name] = value
