extends Control

signal go_to_rocket_hideout_b1f
signal go_to_rocket_hideout_b3f
signal start_battle_placeholder(battle_id)

const PATROL_BATTLE_ID := "rocket_hideout_b2f_patrol"

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_b2f()
	if save_state:
		save_state.enter_celadon_rocket_hideout_b2f()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_hideout_b2f_scene()
	if event.is_action_pressed("ui_down"):
		trigger_rocket_hideout_b2f_patrol_battle()
	if event.is_action_pressed("ui_right"):
		trigger_rocket_hideout_b3f_entry()
	if event.is_action_pressed("cancel"):
		return_to_rocket_hideout_b1f()


func _build_b2f() -> void:
	var floor := ColorRect.new()
	floor.color = Color("292832")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var patrol_corridor := ColorRect.new()
	patrol_corridor.color = Color("59525f")
	patrol_corridor.anchor_left = 0.08
	patrol_corridor.anchor_top = 0.18
	patrol_corridor.anchor_right = 0.92
	patrol_corridor.anchor_bottom = 0.32
	add_child(patrol_corridor)

	var crate_room := ColorRect.new()
	crate_room.color = Color("3d4f6a")
	crate_room.anchor_left = 0.08
	crate_room.anchor_top = 0.4
	crate_room.anchor_right = 0.36
	crate_room.anchor_bottom = 0.68
	add_child(crate_room)

	var gold_dust_breach := ColorRect.new()
	gold_dust_breach.color = Color("b98d2d")
	gold_dust_breach.anchor_left = 0.64
	gold_dust_breach.anchor_top = 0.4
	gold_dust_breach.anchor_right = 0.9
	gold_dust_breach.anchor_bottom = 0.68
	add_child(gold_dust_breach)

	var moonlight_control := ColorRect.new()
	moonlight_control.color = Color("6d65bf")
	moonlight_control.anchor_left = 0.4
	moonlight_control.anchor_top = 0.44
	moonlight_control.anchor_right = 0.6
	moonlight_control.anchor_bottom = 0.74
	add_child(moonlight_control)

	var b3f_stairs := ColorRect.new()
	b3f_stairs.color = Color("211f27")
	b3f_stairs.anchor_left = 0.72
	b3f_stairs.anchor_top = 0.76
	b3f_stairs.anchor_right = 0.9
	b3f_stairs.anchor_bottom = 0.9
	add_child(b3f_stairs)

	var header := Label.new()
	header.text = "Celadon Rocket Hideout - B2F"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.9
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(header)

	var patrol_label := Label.new()
	patrol_label.text = "Rocket patrol line"
	patrol_label.anchor_left = 0.34
	patrol_label.anchor_top = 0.22
	patrol_label.anchor_right = 0.68
	patrol_label.anchor_bottom = 0.29
	patrol_label.add_theme_font_size_override("font_size", 18)
	patrol_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(patrol_label)

	var crate_label := Label.new()
	crate_label.text = "Stolen Silph Scope crate"
	crate_label.anchor_left = 0.08
	crate_label.anchor_top = 0.69
	crate_label.anchor_right = 0.38
	crate_label.anchor_bottom = 0.75
	crate_label.add_theme_font_size_override("font_size", 16)
	crate_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(crate_label)

	var gold_label := Label.new()
	gold_label.text = "Gold Dust breach"
	gold_label.anchor_left = 0.66
	gold_label.anchor_top = 0.69
	gold_label.anchor_right = 0.9
	gold_label.anchor_bottom = 0.75
	gold_label.add_theme_font_size_override("font_size", 16)
	gold_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(gold_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight control room"
	moonlight_label.anchor_left = 0.37
	moonlight_label.anchor_top = 0.75
	moonlight_label.anchor_right = 0.65
	moonlight_label.anchor_bottom = 0.81
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(moonlight_label)

	var stairs_label := Label.new()
	stairs_label.text = "B3F Lift Key route"
	stairs_label.anchor_left = 0.69
	stairs_label.anchor_top = 0.91
	stairs_label.anchor_right = 0.94
	stairs_label.anchor_bottom = 0.97
	stairs_label.add_theme_font_size_override("font_size", 16)
	stairs_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(stairs_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.17
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(dialogue_label)


func trigger_rocket_hideout_b2f_scene() -> void:
	if save_state:
		save_state.record_celadon_rocket_hideout_b2f_scene()
	dialogue_label.text = "Red: B2F has a Rocket patrol guarding a stolen Silph Scope crate. Bill says the crate matches the Lavender signal, Gold Dust is fighting Rocket over a ledger, Team Moonlight is interfering from the control room, and the Lift Key route continues toward B3F."


func trigger_rocket_hideout_b2f_patrol_battle() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_hideout_b2f_patrol_battle_unlocked", false):
		dialogue_label.text = "Red: We need Bill's Silph Scope crate trace and the patrol route before we start a Rocket fight on B2F."
		return
	if save_state:
		save_state.start_battle_placeholder(PATROL_BATTLE_ID)
	dialogue_label.text = "Rocket Patrol: That crate is Giovanni property. Red: Antman, take the patrol while I block the corridor."
	emit_signal("start_battle_placeholder", PATROL_BATTLE_ID)


func trigger_rocket_hideout_b3f_entry() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_hideout_b3f_path_unlocked", false):
		dialogue_label.text = "Red: B3F stays locked until the B2F Rocket patrol is down and the Lift Key route is clear."
		return
	dialogue_label.text = "Red: B3F is open. The Lift Key trail and Giovanni's route both point lower."
	emit_signal("go_to_rocket_hideout_b3f")


func return_to_rocket_hideout_b1f() -> void:
	emit_signal("go_to_rocket_hideout_b1f")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Rocket Hideout B2F. Press Z/Enter to trace the patrol, stolen Silph Scope crate, Gold Dust breach, Team Moonlight control room, and Lift Key route. Press Down for the patrol battle, Right for B3F, or X/Esc to return."
