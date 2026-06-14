extends Control

const TitleScreenScene := preload("res://scenes/ui/TitleScreen.tscn")
const BedroomScene := preload("res://scenes/world/Bedroom.tscn")
const OakLabScene := preload("res://scenes/world/OakLab.tscn")
const Route1Scene := preload("res://scenes/world/Route1.tscn")
const BattlePlaceholderScene := preload("res://scenes/battle/BattlePlaceholder.tscn")
const WildEncounterPlaceholderScene := preload("res://scenes/encounter/WildEncounterPlaceholder.tscn")
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
	oak_lab.go_to_route_1.connect(_on_go_to_route_1)
	_replace_screen(oak_lab)


func _on_return_to_bedroom() -> void:
	save_state.current_scene = "bedroom"
	_show_bedroom()


func _on_go_to_route_1() -> void:
	save_state.enter_route_1()
	var route_1 := Route1Scene.instantiate()
	route_1.save_state = save_state
	route_1.start_battle_placeholder.connect(_on_start_battle_placeholder)
	route_1.start_wild_encounter.connect(_on_start_wild_encounter)
	_replace_screen(route_1)


func _on_start_battle_placeholder(battle_id: String) -> void:
	save_state.start_battle_placeholder(battle_id)
	var battle := BattlePlaceholderScene.instantiate()
	battle.save_state = save_state
	battle.battle_id = battle_id
	battle.battle_finished.connect(_on_battle_placeholder_finished)
	_replace_screen(battle)


func _on_battle_placeholder_finished(result: String) -> void:
	save_state.finish_battle_placeholder(result)
	_on_go_to_route_1()


func _on_start_wild_encounter(encounter_data: Dictionary) -> void:
	if save_state.active_encounter_id == "":
		save_state.start_wild_encounter(encounter_data)
	var encounter := WildEncounterPlaceholderScene.instantiate()
	encounter.save_state = save_state
	encounter.encounter_data = save_state.active_encounter_data
	encounter.encounter_finished.connect(_on_wild_encounter_finished)
	_replace_screen(encounter)


func _on_wild_encounter_finished(result: String) -> void:
	save_state.finish_wild_encounter(result)
	_on_go_to_route_1()


func _replace_screen(next_screen: Control) -> void:
	if current_screen:
		current_screen.queue_free()
	current_screen = next_screen
	add_child(current_screen)
