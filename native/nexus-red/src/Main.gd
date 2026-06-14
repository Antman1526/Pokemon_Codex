extends Control

const TitleScreenScene := preload("res://scenes/ui/TitleScreen.tscn")
const BedroomScene := preload("res://scenes/world/Bedroom.tscn")
const OakLabScene := preload("res://scenes/world/OakLab.tscn")
const SaveState := preload("res://src/save/SaveState.gd")
const GAME_TITLE := "POKEMON NEXUS RED"

var save_state := SaveState.new()
var current_screen: Control


func _ready() -> void:
	show_title_screen()


func show_title_screen() -> void:
	var title_screen := TitleScreenScene.instantiate()
	title_screen.start_new_game.connect(_on_start_new_game)
	_replace_screen(title_screen)


func _on_start_new_game() -> void:
	save_state.start_new_game("Antman")
	_show_bedroom()


func _show_bedroom() -> void:
	var bedroom := BedroomScene.instantiate()
	bedroom.save_state = save_state
	bedroom.go_to_oak_lab.connect(_on_go_to_oak_lab)
	_replace_screen(bedroom)


func _on_go_to_oak_lab() -> void:
	save_state.current_scene = "oak_lab"
	var oak_lab := OakLabScene.instantiate()
	oak_lab.save_state = save_state
	oak_lab.return_to_bedroom.connect(_on_return_to_bedroom)
	_replace_screen(oak_lab)


func _on_return_to_bedroom() -> void:
	save_state.current_scene = "bedroom"
	_show_bedroom()


func _replace_screen(next_screen: Control) -> void:
	if current_screen:
		current_screen.queue_free()
	current_screen = next_screen
	add_child(current_screen)
