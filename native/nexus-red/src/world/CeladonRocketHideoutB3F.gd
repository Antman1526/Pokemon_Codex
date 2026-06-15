extends Control

signal go_to_rocket_hideout_b2f
signal go_to_rocket_hideout_elevator
signal start_battle_placeholder(battle_id)

const ADMIN_BATTLE_ID := "rocket_hideout_b3f_admin"

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_b3f()
	if save_state:
		save_state.enter_celadon_rocket_hideout_b3f()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_hideout_b3f_scene()
	if event.is_action_pressed("ui_down"):
		trigger_rocket_hideout_b3f_admin_battle()
	if event.is_action_pressed("ui_right"):
		trigger_rocket_hideout_elevator_entry()
	if event.is_action_pressed("cancel"):
		return_to_rocket_hideout_b2f()


func _build_b3f() -> void:
	var floor := ColorRect.new()
	floor.color = Color("272631")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var lift_key_chamber := ColorRect.new()
	lift_key_chamber.color = Color("5f5461")
	lift_key_chamber.anchor_left = 0.08
	lift_key_chamber.anchor_top = 0.18
	lift_key_chamber.anchor_right = 0.4
	lift_key_chamber.anchor_bottom = 0.52
	add_child(lift_key_chamber)

	var admin_block := ColorRect.new()
	admin_block.color = Color("442b34")
	admin_block.anchor_left = 0.46
	admin_block.anchor_top = 0.18
	admin_block.anchor_right = 0.9
	admin_block.anchor_bottom = 0.36
	add_child(admin_block)

	var nexus_trace := ColorRect.new()
	nexus_trace.color = Color("315f78")
	nexus_trace.anchor_left = 0.44
	nexus_trace.anchor_top = 0.44
	nexus_trace.anchor_right = 0.62
	nexus_trace.anchor_bottom = 0.68
	add_child(nexus_trace)

	var gold_ledger := ColorRect.new()
	gold_ledger.color = Color("b98d2d")
	gold_ledger.anchor_left = 0.68
	gold_ledger.anchor_top = 0.48
	gold_ledger.anchor_right = 0.9
	gold_ledger.anchor_bottom = 0.68
	add_child(gold_ledger)

	var moonlight_panel := ColorRect.new()
	moonlight_panel.color = Color("6d65bf")
	moonlight_panel.anchor_left = 0.1
	moonlight_panel.anchor_top = 0.62
	moonlight_panel.anchor_right = 0.34
	moonlight_panel.anchor_bottom = 0.82
	add_child(moonlight_panel)

	var elevator := ColorRect.new()
	elevator.color = Color("211f27")
	elevator.anchor_left = 0.68
	elevator.anchor_top = 0.76
	elevator.anchor_right = 0.9
	elevator.anchor_bottom = 0.9
	add_child(elevator)

	var header := Label.new()
	header.text = "Celadon Rocket Hideout - B3F"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.9
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(header)

	var key_label := Label.new()
	key_label.text = "Lift Key chamber"
	key_label.anchor_left = 0.12
	key_label.anchor_top = 0.53
	key_label.anchor_right = 0.4
	key_label.anchor_bottom = 0.59
	key_label.add_theme_font_size_override("font_size", 17)
	key_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(key_label)

	var admin_label := Label.new()
	admin_label.text = "Rocket Admin block"
	admin_label.anchor_left = 0.56
	admin_label.anchor_top = 0.24
	admin_label.anchor_right = 0.86
	admin_label.anchor_bottom = 0.31
	admin_label.add_theme_font_size_override("font_size", 17)
	admin_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(admin_label)

	var nexus_label := Label.new()
	nexus_label.text = "Nexus Order elevator trace"
	nexus_label.anchor_left = 0.38
	nexus_label.anchor_top = 0.69
	nexus_label.anchor_right = 0.66
	nexus_label.anchor_bottom = 0.75
	nexus_label.add_theme_font_size_override("font_size", 16)
	nexus_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(nexus_label)

	var gold_label := Label.new()
	gold_label.text = "Gold Dust ledger"
	gold_label.anchor_left = 0.68
	gold_label.anchor_top = 0.69
	gold_label.anchor_right = 0.9
	gold_label.anchor_bottom = 0.75
	gold_label.add_theme_font_size_override("font_size", 16)
	gold_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(gold_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight sleep panel"
	moonlight_label.anchor_left = 0.1
	moonlight_label.anchor_top = 0.83
	moonlight_label.anchor_right = 0.36
	moonlight_label.anchor_bottom = 0.89
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(moonlight_label)

	var elevator_label := Label.new()
	elevator_label.text = "Giovanni elevator"
	elevator_label.anchor_left = 0.69
	elevator_label.anchor_top = 0.91
	elevator_label.anchor_right = 0.94
	elevator_label.anchor_bottom = 0.97
	elevator_label.add_theme_font_size_override("font_size", 16)
	elevator_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(elevator_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.17
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(dialogue_label)


func trigger_rocket_hideout_b3f_scene() -> void:
	if save_state:
		save_state.record_celadon_rocket_hideout_b3f_scene()
	dialogue_label.text = "Red: B3F is the Lift Key chamber. Bill found a Nexus Order elevator trace under Rocket's wiring, a Rocket Admin is holding the Lift Key, Gold Dust dropped a ledger, Team Moonlight wired a sleep panel, and Giovanni's elevator route opens after the admin falls."


func trigger_rocket_hideout_b3f_admin_battle() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_admin_lift_key_battle_unlocked", false):
		dialogue_label.text = "Red: We need Bill's Nexus Order elevator trace and the Lift Key chamber mapped before fighting the Rocket Admin."
		return
	if save_state:
		save_state.start_battle_placeholder(ADMIN_BATTLE_ID)
	dialogue_label.text = "Rocket Admin: Giovanni left the Lift Key with me. Red: Antman, win it and we cut off Rocket's elevator."
	emit_signal("start_battle_placeholder", ADMIN_BATTLE_ID)


func trigger_rocket_hideout_elevator_entry() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_hideout_elevator_path_unlocked", false):
		dialogue_label.text = "Red: The elevator route stays locked until the Rocket Admin is beaten and the Lift Key is ours."
		return
	dialogue_label.text = "Red: The elevator is open. Giovanni's Celadon route is finally exposed."
	emit_signal("go_to_rocket_hideout_elevator")


func return_to_rocket_hideout_b2f() -> void:
	emit_signal("go_to_rocket_hideout_b2f")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Rocket Hideout B3F. Press Z/Enter to map the Lift Key chamber, Bill's Nexus Order elevator trace, the Rocket Admin, Gold Dust ledger, Team Moonlight sleep panel, and Giovanni elevator. Press Down for the admin battle, Right for the elevator, or X/Esc to return."
