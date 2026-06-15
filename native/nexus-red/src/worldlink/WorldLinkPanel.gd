extends PanelContainer

const OPENING_FEED_PATH := "res://content/worldlink/opening_feed.json"
const ROUTE_1_BATCH_PATH := "res://content/worldlink/route_1_rival_batch.json"
const VIRIDIAN_BATCH_PATH := "res://content/worldlink/viridian_story_batch.json"
const PEWTER_MUSEUM_BATCH_PATH := "res://content/worldlink/pewter_museum_anomaly_batch.json"
const MT_MOON_BATCH_PATH := "res://content/worldlink/mt_moon_faction_conflict_batch.json"
const MT_MOON_INTERIOR_BATCH_PATH := "res://content/worldlink/mt_moon_interior_split_batch.json"
const MT_MOON_FOSSIL_DECISION_BATCH_PATH := "res://content/worldlink/mt_moon_fossil_decision_batch.json"
const ROUTE_4_CERULEAN_BATCH_PATH := "res://content/worldlink/route_4_cerulean_approach_batch.json"
const CERULEAN_CITY_BATCH_PATH := "res://content/worldlink/cerulean_city_intro_batch.json"
const NUGGET_BRIDGE_BATCH_PATH := "res://content/worldlink/nugget_bridge_recruiter_batch.json"
const ROUTE_1_RUMORS_PATH := "res://content/encounters/route_1_rumors.json"

var save_state


func _ready() -> void:
	_build_worldlink()


func _build_worldlink() -> void:
	_clear_children()

	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	add_child(box)

	var title := Label.new()
	title.text = "WorldLink"
	title.add_theme_font_size_override("font_size", 28)
	title.add_theme_color_override("font_color", Color("b92732"))
	box.add_child(title)

	var feed := Label.new()
	feed.text = _build_feed_text()
	feed.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	feed.add_theme_font_size_override("font_size", 18)
	box.add_child(feed)

	var checklist := Label.new()
	checklist.text = _build_checklist_text()
	checklist.add_theme_font_size_override("font_size", 16)
	box.add_child(checklist)


func _clear_children() -> void:
	for child in get_children():
		remove_child(child)
		child.free()


func _build_feed_text() -> String:
	var item_index := _build_item_index()
	var ids := _active_message_ids()
	var feed_lines: Array[String] = ["Feed"]
	var rumor_lines: Array[String] = ["Route 1 Rumors"]

	for message_id in ids:
		var item: Dictionary = item_index.get(message_id, {})
		var text := _message_text(message_id, item)
		if message_id.begins_with("rumor_"):
			rumor_lines.append("- " + text)
		else:
			feed_lines.append("- " + text)

	if rumor_lines.size() == 1:
		rumor_lines.append("- No confirmed Route 1 rumors yet.")

	return "\n".join(feed_lines) + "\n\n" + "\n".join(rumor_lines)


func _build_checklist_text() -> String:
	return "Checklist\n%s Visit Oak\n%s Choose first partner\n%s Step onto Route 1\n%s Finish Blue Route 1 battle\n%s Check Route 1 rumors\n%s Reach Viridian City\n%s Talk to Red in Viridian\n%s Find Viridian Rocket clue\n%s Reach Pewter City\n%s Earn Boulder Badge\n%s Investigate Pewter Museum anomaly\n%s Reach Mt. Moon entrance\n%s Witness Rocket and Gold Dust clash\n%s Enter Mt. Moon interior\n%s Map the fossil split paths\n%s Reach fossil decision\n%s Choose Mt. Moon fossil\n%s Reach Route 4\n%s Hear Red's Cerulean warning\n%s Reach Cerulean City\n%s Meet Misty\n%s Identify Nugget Bridge threat\n%s Reach Nugget Bridge\n%s Scout bridge recruiters\n%s Defeat first bridge recruiter\n%s Defeat bridge captain\n%s Clear Nugget Bridge crisis" % [
		_checkmark(_flag("mom_opening_scene_seen")),
		_checkmark(_flag("starter_chosen")),
		_checkmark(_flag("route_1_reached")),
		_checkmark(_flag("blue_route_1_battle_finished")),
		_checkmark(_flag("route_1_rumors_unlocked")),
		_checkmark(_flag("viridian_city_reached")),
		_checkmark(_flag("viridian_red_scene_seen")),
		_checkmark(_flag("viridian_rocket_clue_found")),
		_checkmark(_flag("pewter_city_reached")),
		_checkmark(_flag("brock_pewter_badge_earned")),
		_checkmark(_flag("pewter_museum_anomaly_seen")),
		_checkmark(_flag("mt_moon_entrance_reached")),
		_checkmark(_flag("rocket_gold_dust_mt_moon_conflict_seen")),
		_checkmark(_flag("mt_moon_interior_1_reached")),
		_checkmark(_flag("fossil_choice_setup_seen")),
		_checkmark(_flag("mt_moon_fossil_decision_reached")),
		_checkmark(_flag("mt_moon_fossil_choice_made")),
		_checkmark(_flag("route_4_cerulean_approach_reached")),
		_checkmark(_flag("red_route_4_cerulean_warning_seen")),
		_checkmark(_flag("cerulean_city_reached")),
		_checkmark(_flag("misty_cerulean_intro_seen")),
		_checkmark(_flag("nugget_bridge_threat_setup_seen")),
		_checkmark(_flag("nugget_bridge_reached")),
		_checkmark(_flag("red_misty_nugget_bridge_scout_seen")),
		_checkmark(_flag("nugget_bridge_recruiter_1_battle_finished")),
		_checkmark(_flag("nugget_bridge_captain_battle_finished")),
		_checkmark(_flag("nugget_bridge_crisis_cleared")),
	]


func _checkmark(done: bool) -> String:
	if done:
		return "[x]"
	return "[ ]"


func _flag(flag_name: String) -> bool:
	if save_state == null:
		return false
	return bool(save_state.story_flags.get(flag_name, false))


func _active_message_ids() -> Array:
	if save_state != null and save_state.worldlink_queue.size() > 0:
		return save_state.worldlink_queue
	return [
		"red_route_1_tracks",
		"blue_first_battle_pressure",
		"oak_world_migration_alert",
		"nexus_island_locked",
	]


func _build_item_index() -> Dictionary:
	var index := {}
	_add_feed_items(index, OPENING_FEED_PATH, "feed")
	_add_feed_items(index, ROUTE_1_BATCH_PATH, "feed")
	_add_feed_items(index, VIRIDIAN_BATCH_PATH, "feed")
	_add_feed_items(index, PEWTER_MUSEUM_BATCH_PATH, "feed")
	_add_feed_items(index, MT_MOON_BATCH_PATH, "feed")
	_add_feed_items(index, MT_MOON_INTERIOR_BATCH_PATH, "feed")
	_add_feed_items(index, MT_MOON_FOSSIL_DECISION_BATCH_PATH, "feed")
	_add_feed_items(index, ROUTE_4_CERULEAN_BATCH_PATH, "feed")
	_add_feed_items(index, CERULEAN_CITY_BATCH_PATH, "feed")
	_add_feed_items(index, NUGGET_BRIDGE_BATCH_PATH, "feed")
	_add_feed_items(index, ROUTE_1_RUMORS_PATH, "rumors")
	return index


func _add_feed_items(index: Dictionary, path: String, key: String) -> void:
	var data := _load_json(path)
	var items: Array = data.get(key, [])
	for item in items:
		if typeof(item) == TYPE_DICTIONARY and item.has("id"):
			index[item.get("id")] = item


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) == TYPE_DICTIONARY:
		return parsed
	return {}


func _message_text(message_id: String, item: Dictionary) -> String:
	if item.has("text"):
		return str(item.get("text"))
	if message_id.begins_with("starter_chosen_"):
		return "Antman chose " + _pretty_id(message_id.trim_prefix("starter_chosen_")) + " as his first partner."
	if message_id.begins_with("blue_chose_"):
		return "Blue chose " + _pretty_id(message_id.trim_prefix("blue_chose_")) + " and immediately started talking strategy."
	if message_id == "route_1_reached":
		return "Antman reached Route 1 with Red watching the grass line."
	if message_id == "red_route_1_companion":
		return "Red joined Antman on Route 1 and marked the first anomaly trail."
	if message_id == "blue_route_1_battle_placeholder":
		return "Blue forced the first Route 1 battle beat. Full battle logic is the next combat milestone."
	if message_id == "blue_route_1_battle_finished":
		return "Blue's first Route 1 battle beat is complete. WorldLink activity is starting to spread."
	return "Update: " + _pretty_id(message_id)


func _pretty_id(raw_id: String) -> String:
	var words := raw_id.split("_")
	for index in range(words.size()):
		words[index] = words[index].capitalize()
	return " ".join(words)
