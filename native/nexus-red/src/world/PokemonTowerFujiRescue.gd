extends Control

signal go_to_pokemon_tower_silph_scope_floor
signal go_to_route_12_snorlax_wake
signal start_battle_placeholder(battle_id)

const FUJI_RESCUE_BATTLE_ID := "rocket_tower_fuji_guard"

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_fuji_rescue_floor()
	if save_state:
		save_state.enter_pokemon_tower_fuji_rescue()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_pokemon_tower_fuji_rescue_scene()
	if event.is_action_pressed("ui_down"):
		trigger_fuji_rescue_battle()
	if event.is_action_pressed("ui_right"):
		trigger_route_12_snorlax_wake_path()
	if event.is_action_pressed("cancel"):
		return_to_pokemon_tower_silph_scope_floor()


func _build_fuji_rescue_floor() -> void:
	var floor := ColorRect.new()
	floor.color = Color("292336")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var shrine_path := ColorRect.new()
	shrine_path.color = Color("695b76")
	shrine_path.anchor_left = 0.08
	shrine_path.anchor_top = 0.54
	shrine_path.anchor_right = 0.92
	shrine_path.anchor_bottom = 0.7
	add_child(shrine_path)

	var fuji_corner := ColorRect.new()
	fuji_corner.color = Color("d7c9aa")
	fuji_corner.anchor_left = 0.68
	fuji_corner.anchor_top = 0.18
	fuji_corner.anchor_right = 0.88
	fuji_corner.anchor_bottom = 0.42
	add_child(fuji_corner)

	var rocket_guard := ColorRect.new()
	rocket_guard.color = Color("2a2025")
	rocket_guard.anchor_left = 0.42
	rocket_guard.anchor_top = 0.24
	rocket_guard.anchor_right = 0.58
	rocket_guard.anchor_bottom = 0.46
	add_child(rocket_guard)

	var moonlight_signal := ColorRect.new()
	moonlight_signal.color = Color("7562ba")
	moonlight_signal.anchor_left = 0.16
	moonlight_signal.anchor_top = 0.22
	moonlight_signal.anchor_right = 0.34
	moonlight_signal.anchor_bottom = 0.42
	add_child(moonlight_signal)

	var flute_case := ColorRect.new()
	flute_case.color = Color("c7d6e5")
	flute_case.anchor_left = 0.2
	flute_case.anchor_top = 0.76
	flute_case.anchor_right = 0.4
	flute_case.anchor_bottom = 0.9
	add_child(flute_case)

	var snorlax_marker := ColorRect.new()
	snorlax_marker.color = Color("6b8e9b")
	snorlax_marker.anchor_left = 0.64
	snorlax_marker.anchor_top = 0.76
	snorlax_marker.anchor_right = 0.86
	snorlax_marker.anchor_bottom = 0.9
	add_child(snorlax_marker)

	var header := Label.new()
	header.text = "Pokemon Tower - Mr. Fuji Rescue"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.92
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(header)

	var fuji_label := Label.new()
	fuji_label.text = "Mr. Fuji"
	fuji_label.anchor_left = 0.7
	fuji_label.anchor_top = 0.43
	fuji_label.anchor_right = 0.9
	fuji_label.anchor_bottom = 0.5
	fuji_label.add_theme_font_size_override("font_size", 16)
	fuji_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(fuji_label)

	var guard_label := Label.new()
	guard_label.text = "Rocket tower guard"
	guard_label.anchor_left = 0.4
	guard_label.anchor_top = 0.47
	guard_label.anchor_right = 0.62
	guard_label.anchor_bottom = 0.54
	guard_label.add_theme_font_size_override("font_size", 16)
	guard_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(guard_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight retreat signal"
	moonlight_label.anchor_left = 0.12
	moonlight_label.anchor_top = 0.43
	moonlight_label.anchor_right = 0.38
	moonlight_label.anchor_bottom = 0.5
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(moonlight_label)

	var flute_label := Label.new()
	flute_label.text = "Poke Flute case"
	flute_label.anchor_left = 0.18
	flute_label.anchor_top = 0.91
	flute_label.anchor_right = 0.42
	flute_label.anchor_bottom = 0.98
	flute_label.add_theme_font_size_override("font_size", 16)
	flute_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(flute_label)

	var snorlax_label := Label.new()
	snorlax_label.text = "Snorlax wake path"
	snorlax_label.anchor_left = 0.62
	snorlax_label.anchor_top = 0.91
	snorlax_label.anchor_right = 0.9
	snorlax_label.anchor_bottom = 0.98
	snorlax_label.add_theme_font_size_override("font_size", 16)
	snorlax_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(snorlax_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.18
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(dialogue_label)


func trigger_pokemon_tower_fuji_rescue_scene() -> void:
	if save_state:
		save_state.record_pokemon_tower_fuji_rescue_scene()
	dialogue_label.text = "Red: Mr. Fuji is safe if we beat the Rocket guard. Bill says the Moonlight signal is retreating, Rocket kept the Poke Flute here to control Snorlax, and this battle opens the sleeping-road path."


func trigger_fuji_rescue_battle() -> void:
	if save_state == null or not save_state.story_flags.get("fuji_rescue_battle_unlocked", false):
		dialogue_label.text = "Red: We need Bill's clean signal read, Rocket's guard position, Moonlight's retreat trace, Mr. Fuji, the Poke Flute, and the Snorlax path confirmed before we fight."
		return
	if save_state:
		save_state.start_battle_placeholder(FUJI_RESCUE_BATTLE_ID)
	dialogue_label.text = "Rocket Guard: Boss wanted the flute locked down. Red: Antman, clear the way to Mr. Fuji."
	emit_signal("start_battle_placeholder", FUJI_RESCUE_BATTLE_ID)


func trigger_route_12_snorlax_wake_path() -> void:
	if save_state == null or not bool(save_state.story_flags.get("poke_flute_obtained", false)) or not bool(save_state.story_flags.get("snorlax_wake_path_unlocked", false)):
		dialogue_label.text = "Red: Route 12 stays blocked until we rescue Mr. Fuji and recover the Poke Flute."
		return
	dialogue_label.text = "Red: Route 12 is open to try now. Bill says the Poke Flute should wake Snorlax and clear the sleeping-road block."
	emit_signal("go_to_route_12_snorlax_wake")


func return_to_pokemon_tower_silph_scope_floor() -> void:
	emit_signal("go_to_pokemon_tower_silph_scope_floor")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Mr. Fuji's rescue floor. Press Z/Enter to mark Bill's clean signal, Rocket's guard, Moonlight's retreat, the Poke Flute, and the Snorlax wake path. Press Down to battle, Right for Route 12, or X/Esc to return."
