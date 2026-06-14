extends SceneTree


func _init() -> void:
	var title_scene := load("res://scenes/ui/TitleScreen.tscn")
	var bedroom_scene := load("res://scenes/world/Bedroom.tscn")
	var save_state_script := load("res://src/save/SaveState.gd")

	if title_scene == null:
		push_error("Title scene did not load.")
		quit(1)
		return
	if bedroom_scene == null:
		push_error("Bedroom scene did not load.")
		quit(1)
		return
	if save_state_script == null:
		push_error("SaveState did not load.")
		quit(1)
		return

	var title = title_scene.instantiate()
	root.add_child(title)
	title._ready()
	if title.name != "TitleScreen":
		push_error("Title screen instantiated with unexpected name.")
		quit(1)
		return
	title.queue_free()

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	if save_state.current_region != "kanto" or save_state.active_companion != "red":
		push_error("SaveState did not initialize Kanto with Red as active companion.")
		quit(1)
		return

	var bedroom = bedroom_scene.instantiate()
	bedroom.save_state = save_state
	root.add_child(bedroom)
	bedroom._ready()
	bedroom._play_mom_scene()
	if not save_state.story_flags.get("mom_opening_scene_seen", false):
		push_error("Mom opening scene did not update save flag.")
		quit(1)
		return
	bedroom._toggle_worldlink()
	if bedroom.worldlink_panel == null:
		push_error("WorldLink panel did not open.")
		quit(1)
		return

	print("Native Godot shell smoke test passed.")
	quit(0)
