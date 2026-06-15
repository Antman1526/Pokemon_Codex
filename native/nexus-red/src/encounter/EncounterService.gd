extends RefCounted

const ROUTE_1_WILD_PATH := "res://content/encounters/route_1_wild_encounters.json"
const ROUTE_2_WILD_PATH := "res://content/encounters/route_2_wild_encounters.json"
const EARLY_MIGRATION_PATH := "res://content/encounters/route_1_to_3_migration_encounters.json"


func pick_route_1_encounter(save_state = null) -> Dictionary:
	var data := _load_json(ROUTE_1_WILD_PATH)
	var encounters: Array = data.get("encounters", [])
	if encounters.is_empty():
		return {}

	if save_state == null or not save_state.story_flags.get("route_1_first_wild_seen", false):
		var first := _find_encounter(encounters, "route_1_first_wild")
		if not first.is_empty():
			return first

	var fallback := _find_encounter(encounters, "route_1_common_rattata")
	if not fallback.is_empty():
		return fallback
	return encounters[0]


func pick_route_2_encounter(save_state = null) -> Dictionary:
	var data := _load_json(ROUTE_2_WILD_PATH)
	var encounters: Array = data.get("encounters", [])
	if encounters.is_empty():
		return {}

	if save_state == null or not save_state.story_flags.get("route_2_catch_tutorial_seen", false):
		var first := _find_encounter(encounters, "route_2_red_catch_tutorial_pidgey")
		if not first.is_empty():
			return first

	var fallback := _find_encounter(encounters, "route_2_common_caterpie")
	if not fallback.is_empty():
		return fallback
	return encounters[0]


func get_early_migration_pool() -> Array:
	var data := _load_json(EARLY_MIGRATION_PATH)
	return data.get("encounters", [])


func get_early_migration_encounters_for_route(route_id: String) -> Array:
	var matches: Array = []
	for encounter in get_early_migration_pool():
		if typeof(encounter) == TYPE_DICTIONARY and encounter.get("route_id", "") == route_id:
			matches.append(encounter)
	return matches


func find_early_migration_species(species_name: String) -> Dictionary:
	for encounter in get_early_migration_pool():
		if typeof(encounter) == TYPE_DICTIONARY and encounter.get("species", "") == species_name:
			return encounter
	return {}


func pick_early_migration_encounter(route_id: String, save_state = null) -> Dictionary:
	var encounters := get_early_migration_encounters_for_route(route_id)
	if encounters.is_empty():
		return {}
	for encounter in encounters:
		if typeof(encounter) != TYPE_DICTIONARY:
			continue
		var species := str(encounter.get("species", ""))
		if save_state == null or not save_state.captured_creatures.has(species):
			return encounter
	return encounters[0]


func _find_encounter(encounters: Array, encounter_id: String) -> Dictionary:
	for encounter in encounters:
		if typeof(encounter) == TYPE_DICTIONARY and encounter.get("id", "") == encounter_id:
			return encounter
	return {}


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("Missing encounter data: " + path)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Could not open encounter data: " + path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) == TYPE_DICTIONARY:
		return parsed
	push_error("Invalid encounter JSON: " + path)
	return {}
