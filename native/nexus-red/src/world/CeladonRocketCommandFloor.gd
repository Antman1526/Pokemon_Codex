extends Control

signal go_to_rocket_hideout_elevator
signal start_battle_placeholder(battle_id)

const GIOVANNI_BATTLE_ID := "giovanni_celadon_command_floor"

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_command_floor()
	if save_state:
		save_state.enter_celadon_rocket_command_floor()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_command_floor_scene()
	if event.is_action_pressed("ui_down"):
		trigger_giovanni_command_floor_battle()
	if event.is_action_pressed("cancel"):
		return_to_rocket_hideout_elevator()


func _build_command_floor() -> void:
	var floor := ColorRect.new()
	floor.color = Color("211d24")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var command_table := ColorRect.new()
	command_table.color = Color("4f2f35")
	command_table.anchor_left = 0.1
	command_table.anchor_top = 0.2
	command_table.anchor_right = 0.42
	command_table.anchor_bottom = 0.5
	add_child(command_table)

	var giovanni_platform := ColorRect.new()
	giovanni_platform.color = Color("3f3a31")
	giovanni_platform.anchor_left = 0.55
	giovanni_platform.anchor_top = 0.16
	giovanni_platform.anchor_right = 0.9
	giovanni_platform.anchor_bottom = 0.38
	add_child(giovanni_platform)

	var nexus_terminal := ColorRect.new()
	nexus_terminal.color = Color("315f78")
	nexus_terminal.anchor_left = 0.52
	nexus_terminal.anchor_top = 0.48
	nexus_terminal.anchor_right = 0.74
	nexus_terminal.anchor_bottom = 0.72
	add_child(nexus_terminal)

	var silph_cache := ColorRect.new()
	silph_cache.color = Color("7e8794")
	silph_cache.anchor_left = 0.14
	silph_cache.anchor_top = 0.62
	silph_cache.anchor_right = 0.34
	silph_cache.anchor_bottom = 0.82
	add_child(silph_cache)

	var gold_ledger := ColorRect.new()
	gold_ledger.color = Color("b98d2d")
	gold_ledger.anchor_left = 0.78
	gold_ledger.anchor_top = 0.5
	gold_ledger.anchor_right = 0.92
	gold_ledger.anchor_bottom = 0.68
	add_child(gold_ledger)

	var moonlight_signal := ColorRect.new()
	moonlight_signal.color = Color("6d65bf")
	moonlight_signal.anchor_left = 0.78
	moonlight_signal.anchor_top = 0.72
	moonlight_signal.anchor_right = 0.92
	moonlight_signal.anchor_bottom = 0.9
	add_child(moonlight_signal)

	var header := Label.new()
	header.text = "Celadon Rocket Command Floor"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.92
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(header)

	var giovanni_label := Label.new()
	giovanni_label.text = "Giovanni command dais"
	giovanni_label.anchor_left = 0.56
	giovanni_label.anchor_top = 0.39
	giovanni_label.anchor_right = 0.9
	giovanni_label.anchor_bottom = 0.45
	giovanni_label.add_theme_font_size_override("font_size", 17)
	giovanni_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(giovanni_label)

	var terminal_label := Label.new()
	terminal_label.text = "Nexus Order terminal"
	terminal_label.anchor_left = 0.5
	terminal_label.anchor_top = 0.73
	terminal_label.anchor_right = 0.76
	terminal_label.anchor_bottom = 0.79
	terminal_label.add_theme_font_size_override("font_size", 16)
	terminal_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(terminal_label)

	var scope_label := Label.new()
	scope_label.text = "Silph Scope cache"
	scope_label.anchor_left = 0.13
	scope_label.anchor_top = 0.83
	scope_label.anchor_right = 0.36
	scope_label.anchor_bottom = 0.89
	scope_label.add_theme_font_size_override("font_size", 16)
	scope_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(scope_label)

	var gold_label := Label.new()
	gold_label.text = "Gold Dust ledger"
	gold_label.anchor_left = 0.74
	gold_label.anchor_top = 0.49
	gold_label.anchor_right = 0.96
	gold_label.anchor_bottom = 0.55
	gold_label.add_theme_font_size_override("font_size", 16)
	gold_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(gold_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight signal"
	moonlight_label.anchor_left = 0.74
	moonlight_label.anchor_top = 0.91
	moonlight_label.anchor_right = 0.96
	moonlight_label.anchor_bottom = 0.97
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(moonlight_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.18
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(dialogue_label)


func trigger_rocket_command_floor_scene() -> void:
	if save_state:
		save_state.record_celadon_rocket_command_floor_scene()
	dialogue_label.text = "Red: I will hold the door. Bill found a Nexus Order terminal behind Giovanni's command system, Rocket stored the Silph Scope here, Gold Dust priced the cache, Team Moonlight left a signal, and beating Giovanni opens Pokemon Tower and Erika's gym path."


func trigger_giovanni_command_floor_battle() -> void:
	if save_state == null or not save_state.story_flags.get("giovanni_command_floor_battle_unlocked", false):
		dialogue_label.text = "Red: We need Bill's Nexus Order terminal trace and the Silph Scope cache mapped before we challenge Giovanni."
		return
	if save_state:
		save_state.start_battle_placeholder(GIOVANNI_BATTLE_ID)
	dialogue_label.text = "Giovanni: You have interfered enough. Red: Antman, win the Silph Scope and force Rocket out of Celadon."
	emit_signal("start_battle_placeholder", GIOVANNI_BATTLE_ID)


func return_to_rocket_hideout_elevator() -> void:
	emit_signal("go_to_rocket_hideout_elevator")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Giovanni's command floor. Press Z/Enter to inspect the Nexus Order terminal, Silph Scope cache, Gold Dust ledger, Moonlight signal, Pokemon Tower route, and Erika lead. Press Down to battle Giovanni or X/Esc to return."
