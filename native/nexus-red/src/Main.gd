extends Control

const TitleScreenScene := preload("res://scenes/ui/TitleScreen.tscn")
const BedroomScene := preload("res://scenes/world/Bedroom.tscn")
const OakLabScene := preload("res://scenes/world/OakLab.tscn")
const Route1Scene := preload("res://scenes/world/Route1.tscn")
const ViridianCityScene := preload("res://scenes/world/ViridianCity.tscn")
const Route2ForestGateScene := preload("res://scenes/world/Route2ForestGate.tscn")
const ViridianForestScene := preload("res://scenes/world/ViridianForest.tscn")
const Route3Scene := preload("res://scenes/world/Route3.tscn")
const PewterCityScene := preload("res://scenes/world/PewterCity.tscn")
const MtMoonEntranceScene := preload("res://scenes/world/MtMoonEntrance.tscn")
const MtMoonInterior1Scene := preload("res://scenes/world/MtMoonInterior1.tscn")
const MtMoonFossilDecisionScene := preload("res://scenes/world/MtMoonFossilDecision.tscn")
const Route4CeruleanApproachScene := preload("res://scenes/world/Route4CeruleanApproach.tscn")
const CeruleanCityScene := preload("res://scenes/world/CeruleanCity.tscn")
const NuggetBridgeScene := preload("res://scenes/world/NuggetBridge.tscn")
const Route25BillScene := preload("res://scenes/world/Route25Bill.tscn")
const CeruleanRocketHouseScene := preload("res://scenes/world/CeruleanRocketHouse.tscn")
const Route5UndergroundPathScene := preload("res://scenes/world/Route5UndergroundPath.tscn")
const VermilionCityScene := preload("res://scenes/world/VermilionCity.tscn")
const SSAnneTicketOfficeScene := preload("res://scenes/world/SSAnneTicketOffice.tscn")
const SSAnneMainDeckScene := preload("res://scenes/world/SSAnneMainDeck.tscn")
const SSAnneCargoHoldScene := preload("res://scenes/world/SSAnneCargoHold.tscn")
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
	route_1.go_to_viridian_city.connect(_on_go_to_viridian_city)
	_replace_screen(route_1)


func _on_go_to_viridian_city() -> void:
	_show_viridian_city()


func _show_viridian_city() -> void:
	var viridian_city := ViridianCityScene.instantiate()
	viridian_city.save_state = save_state
	viridian_city.go_to_route_1.connect(_on_go_to_route_1)
	viridian_city.go_to_route_2_forest_gate.connect(_on_go_to_route_2_forest_gate)
	_replace_screen(viridian_city)


func _on_go_to_route_2_forest_gate() -> void:
	_show_route_2_forest_gate()


func _show_route_2_forest_gate() -> void:
	var route_2_gate := Route2ForestGateScene.instantiate()
	route_2_gate.save_state = save_state
	route_2_gate.go_to_viridian_city.connect(_on_go_to_viridian_city)
	route_2_gate.go_to_viridian_forest.connect(_on_go_to_viridian_forest)
	route_2_gate.go_to_route_3.connect(_on_go_to_route_3)
	route_2_gate.start_wild_encounter.connect(_on_start_wild_encounter)
	_replace_screen(route_2_gate)


func _on_go_to_viridian_forest() -> void:
	_show_viridian_forest()


func _show_viridian_forest() -> void:
	var forest := ViridianForestScene.instantiate()
	forest.save_state = save_state
	forest.go_to_route_2_forest_gate.connect(_on_go_to_route_2_forest_gate)
	forest.go_to_route_3.connect(_on_go_to_route_3)
	_replace_screen(forest)


func _on_go_to_route_3() -> void:
	_show_route_3()


func _show_route_3() -> void:
	var route_3 := Route3Scene.instantiate()
	route_3.save_state = save_state
	route_3.go_to_route_2_forest_gate.connect(_on_go_to_route_2_forest_gate)
	route_3.go_to_pewter_city.connect(_on_go_to_pewter_city)
	route_3.start_wild_encounter.connect(_on_start_wild_encounter)
	_replace_screen(route_3)


func _on_go_to_pewter_city() -> void:
	_show_pewter_city()


func _show_pewter_city() -> void:
	var pewter := PewterCityScene.instantiate()
	pewter.save_state = save_state
	pewter.go_to_route_3.connect(_on_go_to_route_3)
	pewter.go_to_mt_moon_entrance.connect(_on_go_to_mt_moon_entrance)
	pewter.start_battle_placeholder.connect(_on_start_battle_placeholder)
	_replace_screen(pewter)


func _on_go_to_mt_moon_entrance() -> void:
	_show_mt_moon_entrance()


func _show_mt_moon_entrance() -> void:
	var mt_moon := MtMoonEntranceScene.instantiate()
	mt_moon.save_state = save_state
	mt_moon.go_to_pewter_city.connect(_on_go_to_pewter_city)
	mt_moon.go_to_mt_moon_interior_1.connect(_on_go_to_mt_moon_interior_1)
	_replace_screen(mt_moon)


func _on_go_to_mt_moon_interior_1() -> void:
	_show_mt_moon_interior_1()


func _show_mt_moon_interior_1() -> void:
	var interior := MtMoonInterior1Scene.instantiate()
	interior.save_state = save_state
	interior.go_to_mt_moon_entrance.connect(_on_go_to_mt_moon_entrance)
	interior.go_to_mt_moon_fossil_decision.connect(_on_go_to_mt_moon_fossil_decision)
	interior.start_battle_placeholder.connect(_on_start_battle_placeholder)
	_replace_screen(interior)


func _on_go_to_mt_moon_fossil_decision() -> void:
	_show_mt_moon_fossil_decision()


func _show_mt_moon_fossil_decision() -> void:
	var decision := MtMoonFossilDecisionScene.instantiate()
	decision.save_state = save_state
	decision.go_to_mt_moon_interior_1.connect(_on_go_to_mt_moon_interior_1)
	decision.go_to_route_4_cerulean_approach.connect(_on_go_to_route_4_cerulean_approach)
	_replace_screen(decision)


func _on_go_to_route_4_cerulean_approach() -> void:
	_show_route_4_cerulean_approach()


func _show_route_4_cerulean_approach() -> void:
	var route4 := Route4CeruleanApproachScene.instantiate()
	route4.save_state = save_state
	route4.go_to_mt_moon_fossil_decision.connect(_on_go_to_mt_moon_fossil_decision)
	route4.go_to_cerulean_city.connect(_on_go_to_cerulean_city)
	_replace_screen(route4)


func _on_go_to_cerulean_city() -> void:
	_show_cerulean_city()


func _show_cerulean_city() -> void:
	var cerulean := CeruleanCityScene.instantiate()
	cerulean.save_state = save_state
	cerulean.go_to_route_4_cerulean_approach.connect(_on_go_to_route_4_cerulean_approach)
	cerulean.go_to_nugget_bridge.connect(_on_go_to_nugget_bridge)
	cerulean.start_battle_placeholder.connect(_on_start_battle_placeholder)
	cerulean.go_to_route_25_bill.connect(_on_go_to_route_25_bill)
	cerulean.go_to_cerulean_rocket_house.connect(_on_go_to_cerulean_rocket_house)
	cerulean.go_to_route_5_underground_path.connect(_on_go_to_route_5_underground_path)
	_replace_screen(cerulean)


func _on_go_to_nugget_bridge() -> void:
	_show_nugget_bridge()


func _show_nugget_bridge() -> void:
	var bridge := NuggetBridgeScene.instantiate()
	bridge.save_state = save_state
	bridge.go_to_cerulean_city.connect(_on_go_to_cerulean_city)
	bridge.start_battle_placeholder.connect(_on_start_battle_placeholder)
	_replace_screen(bridge)


func _on_go_to_route_25_bill() -> void:
	_show_route_25_bill()


func _show_route_25_bill() -> void:
	var route25 := Route25BillScene.instantiate()
	route25.save_state = save_state
	route25.go_to_cerulean_city.connect(_on_go_to_cerulean_city)
	_replace_screen(route25)


func _on_go_to_cerulean_rocket_house() -> void:
	_show_cerulean_rocket_house()


func _show_cerulean_rocket_house() -> void:
	var house := CeruleanRocketHouseScene.instantiate()
	house.save_state = save_state
	house.go_to_cerulean_city.connect(_on_go_to_cerulean_city)
	house.start_battle_placeholder.connect(_on_start_battle_placeholder)
	_replace_screen(house)


func _on_go_to_route_5_underground_path() -> void:
	_show_route_5_underground_path()


func _show_route_5_underground_path() -> void:
	var route5 := Route5UndergroundPathScene.instantiate()
	route5.save_state = save_state
	route5.go_to_cerulean_city.connect(_on_go_to_cerulean_city)
	route5.go_to_vermilion_city.connect(_on_go_to_vermilion_city)
	_replace_screen(route5)


func _on_go_to_vermilion_city() -> void:
	_show_vermilion_city()


func _show_vermilion_city() -> void:
	var vermilion := VermilionCityScene.instantiate()
	vermilion.save_state = save_state
	vermilion.go_to_route_5_underground_path.connect(_on_go_to_route_5_underground_path)
	vermilion.go_to_ss_anne_ticket_office.connect(_on_go_to_ss_anne_ticket_office)
	_replace_screen(vermilion)


func _on_go_to_ss_anne_ticket_office() -> void:
	_show_ss_anne_ticket_office()


func _show_ss_anne_ticket_office() -> void:
	var ticket_office := SSAnneTicketOfficeScene.instantiate()
	ticket_office.save_state = save_state
	ticket_office.go_to_vermilion_city.connect(_on_go_to_vermilion_city)
	ticket_office.go_to_ss_anne_main_deck.connect(_on_go_to_ss_anne_main_deck)
	_replace_screen(ticket_office)


func _on_go_to_ss_anne_main_deck() -> void:
	_show_ss_anne_main_deck()


func _show_ss_anne_main_deck() -> void:
	var deck := SSAnneMainDeckScene.instantiate()
	deck.save_state = save_state
	deck.go_to_ss_anne_ticket_office.connect(_on_go_to_ss_anne_ticket_office)
	deck.go_to_ss_anne_cargo_hold.connect(_on_go_to_ss_anne_cargo_hold)
	deck.start_battle_placeholder.connect(_on_start_battle_placeholder)
	_replace_screen(deck)


func _on_go_to_ss_anne_cargo_hold() -> void:
	_show_ss_anne_cargo_hold()


func _show_ss_anne_cargo_hold() -> void:
	var cargo := SSAnneCargoHoldScene.instantiate()
	cargo.save_state = save_state
	cargo.go_to_ss_anne_main_deck.connect(_on_go_to_ss_anne_main_deck)
	_replace_screen(cargo)


func _on_start_battle_placeholder(battle_id: String) -> void:
	save_state.start_battle_placeholder(battle_id)
	var battle := BattlePlaceholderScene.instantiate()
	battle.save_state = save_state
	battle.battle_id = battle_id
	battle.battle_finished.connect(_on_battle_placeholder_finished)
	_replace_screen(battle)


func _on_battle_placeholder_finished(result: String) -> void:
	var battle_return_scene := save_state.current_scene
	save_state.finish_battle_placeholder(result)
	if battle_return_scene == "pewter_city":
		_show_pewter_city()
	elif battle_return_scene == "mt_moon_interior_1":
		_show_mt_moon_interior_1()
	elif battle_return_scene == "nugget_bridge":
		_show_nugget_bridge()
	elif battle_return_scene == "cerulean_city":
		_show_cerulean_city()
	elif battle_return_scene == "cerulean_rocket_house":
		_show_cerulean_rocket_house()
	elif battle_return_scene == "ss_anne_main_deck":
		_show_ss_anne_main_deck()
	else:
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
	var return_scene := save_state.encounter_return_scene
	save_state.finish_wild_encounter(result)
	_return_from_wild_encounter(return_scene)


func _return_from_wild_encounter(return_scene: String) -> void:
	if return_scene == "route_2_forest_gate":
		_show_route_2_forest_gate()
	elif return_scene == "route_3":
		_show_route_3()
	else:
		_on_go_to_route_1()


func _replace_screen(next_screen: Control) -> void:
	if current_screen:
		current_screen.queue_free()
	current_screen = next_screen
	add_child(current_screen)
