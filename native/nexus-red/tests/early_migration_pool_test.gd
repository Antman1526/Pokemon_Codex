extends SceneTree


func _init() -> void:
	print("early_migration_pool_test")
	var encounter_service_script := load("res://src/encounter/EncounterService.gd")
	if encounter_service_script == null:
		push_error("EncounterService did not load.")
		quit(1)
		return

	var service = encounter_service_script.new()
	var pool: Array = service.get_early_migration_pool()
	var required_species: Array[String] = [
		"Bulbasaur", "Charmander", "Squirtle",
		"Chikorita", "Cyndaquil", "Totodile",
		"Treecko", "Torchic", "Mudkip",
		"Turtwig", "Chimchar", "Piplup",
		"Snivy", "Tepig", "Oshawott",
		"Chespin", "Fennekin", "Froakie",
		"Rowlet", "Litten", "Popplio",
		"Grookey", "Scorbunny", "Sobble",
		"Sprigatito", "Fuecoco", "Quaxly",
		"Eevee", "Pikachu", "Dratini", "Abra", "Gastly", "Larvitar",
		"Sandile", "Kubfu", "Staryu", "Shroomish", "Rockruff", "Ralts",
	]
	if pool.size() != required_species.size():
		push_error("Early migration pool must have exactly 39 entries.")
		quit(1)
		return

	var seen := {}
	for encounter in pool:
		var species := str(encounter.get("species", ""))
		seen[species] = true
		var route_id := str(encounter.get("route_id", ""))
		if not route_id in ["route_1", "route_2", "route_3"]:
			push_error("Early migration encounter had invalid route_id: " + route_id)
			quit(1)
			return
		var level := int(encounter.get("level", 0))
		if level < 3 or level > 7:
			push_error("%s was outside the pre-Brock level band." % species)
			quit(1)
			return
		if str(encounter.get("return_scene", "")) == "":
			push_error("%s did not define a return scene." % species)
			quit(1)
			return

	for species in required_species:
		if not seen.has(species):
			push_error("Early migration pool missing " + species)
			quit(1)
			return

	for route_id in ["route_1", "route_2", "route_3"]:
		var route_entries: Array = service.get_early_migration_encounters_for_route(route_id)
		if route_entries.size() != 13:
			push_error("%s must expose exactly 13 early migration encounters." % route_id)
			quit(1)
			return

	var kubfu: Dictionary = service.find_early_migration_species("Kubfu")
	if kubfu.get("route_id", "") != "route_3":
		push_error("Kubfu should be reserved for Route 3 in the early migration pool.")
		quit(1)
		return
	var sprigatito: Dictionary = service.find_early_migration_species("Sprigatito")
	if sprigatito.get("route_id", "") != "route_3":
		push_error("Sprigatito should appear on Route 3 in the early migration pool.")
		quit(1)
		return

	print("Native early migration pool smoke test passed.")
	quit(0)
