extends RefCounted

const CATCH_SUCCESS := "catch_success"
const CATCH_BLOCKED := "catch_blocked"


func calculate_max_hp(encounter_data: Dictionary) -> int:
	var level := int(encounter_data.get("level", 1))
	return max(8, 12 + level * 3)


func calculate_attack_damage(player_species: String, encounter_data: Dictionary) -> int:
	var level := int(encounter_data.get("level", 1))
	var starter_bonus := 1
	if player_species != "":
		starter_bonus = 2
	return max(4, level + 3 + starter_bonus)


func can_capture(wild_hp: int, wild_max_hp: int) -> bool:
	return wild_hp > 0 and wild_hp < wild_max_hp


func capture_result(wild_hp: int, wild_max_hp: int) -> String:
	if can_capture(wild_hp, wild_max_hp):
		return CATCH_SUCCESS
	return CATCH_BLOCKED
