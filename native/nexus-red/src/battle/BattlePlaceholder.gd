extends Control

signal battle_finished(result)

const BATTLE_DATA_PATHS := {
	"blue_route_1": "res://content/battles/blue_route_1.json",
	"brock_pewter_gym": "res://content/battles/brock_pewter_gym.json",
	"mt_moon_rocket_left_path": "res://content/battles/mt_moon_rocket_left_path.json",
	"mt_moon_gold_dust_right_path": "res://content/battles/mt_moon_gold_dust_right_path.json",
}
const BLUE_COMPATIBILITY_MARKER := "Blue"

var save_state
var battle_id := "blue_route_1"
var dialogue_label: Label
var battle_data: Dictionary = {}


func _ready() -> void:
	battle_data = _load_battle_data(battle_id)
	_build_battle_screen()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		finish_placeholder_battle()


func _load_battle_data(id: String) -> Dictionary:
	var path: String = BATTLE_DATA_PATHS.get(id, "")
	if path == "":
		push_error("Unknown placeholder battle: " + id)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Missing battle data: " + path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Invalid battle data JSON: " + path)
		return {}
	return parsed


func _build_battle_screen() -> void:
	var backdrop := ColorRect.new()
	backdrop.color = Color("8fc8ee")
	backdrop.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(backdrop)

	var player_side := ColorRect.new()
	player_side.color = Color("77b85b")
	player_side.anchor_left = 0.06
	player_side.anchor_top = 0.58
	player_side.anchor_right = 0.46
	player_side.anchor_bottom = 0.82
	add_child(player_side)

	var opponent_side := ColorRect.new()
	opponent_side.color = Color("d6b36f")
	opponent_side.anchor_left = 0.54
	opponent_side.anchor_top = 0.16
	opponent_side.anchor_right = 0.94
	opponent_side.anchor_bottom = 0.4
	add_child(opponent_side)

	var title := Label.new()
	title.text = "%s - placeholder battle engine" % _battle_title()
	title.anchor_left = 0.05
	title.anchor_top = 0.04
	title.anchor_right = 0.95
	title.anchor_bottom = 0.12
	title.add_theme_font_size_override("font_size", 32)
	title.add_theme_color_override("font_color", Color("14243d"))
	add_child(title)

	var player_label := Label.new()
	player_label.text = "Antman sends out %s" % _player_starter()
	player_label.anchor_left = 0.08
	player_label.anchor_top = 0.64
	player_label.anchor_right = 0.44
	player_label.anchor_bottom = 0.72
	player_label.add_theme_font_size_override("font_size", 22)
	add_child(player_label)

	var opponent_label := Label.new()
	opponent_label.text = "%s sends out %s" % [_opponent_display_name(), _opponent_summary()]
	opponent_label.anchor_left = 0.56
	opponent_label.anchor_top = 0.22
	opponent_label.anchor_right = 0.92
	opponent_label.anchor_bottom = 0.3
	opponent_label.add_theme_font_size_override("font_size", 22)
	add_child(opponent_label)

	dialogue_label = Label.new()
	dialogue_label.text = "%s: This is a placeholder. The real battle engine comes next. Press Z or Enter to record the battle." % _opponent_display_name()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func finish_placeholder_battle() -> void:
	emit_signal("battle_finished", "placeholder_win")


func _player_starter() -> String:
	if save_state and save_state.player_starter != "":
		return save_state.player_starter
	return "player_starter"


func _blue_starter() -> String:
	if save_state and save_state.blue_starter != "":
		return save_state.blue_starter
	return "blue_starter"


func _battle_title() -> String:
	return str(battle_data.get("display_title", battle_id))


func _opponent_display_name() -> String:
	return str(battle_data.get("opponent", {}).get("display_name", "Opponent"))


func _opponent_summary() -> String:
	if battle_id == "blue_route_1":
		return _blue_starter()
	var slots: Array = battle_data.get("opponent", {}).get("slots", [])
	var names: Array[String] = []
	for slot in slots:
		if typeof(slot) == TYPE_DICTIONARY:
			names.append("%s Lv. %d" % [slot.get("species", "creature"), int(slot.get("level", 1))])
	if names.is_empty():
		return "placeholder team"
	return ", ".join(names)
