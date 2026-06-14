#!/usr/bin/env python3
"""Validate the first playable Slowpoke Well entry slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0054-slowpoke-well-first-entry.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-slowpoke-well-first-entry-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-slowpoke-well-first-entry.md"
JOHTO_CHAPTER = ROOT / "data_design" / "johto_chapter.yaml"
JOHTO_WORLDLINK = ROOT / "data_design" / "johto_worldlink_messages.yaml"
REGION_PROGRESSION = ROOT / "data_design" / "worldlink_region_progression.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    return yaml.safe_load(read(path))


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0054-slowpoke-well-first-entry.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0054-slowpoke-well-first-entry.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_SLOWPOKE_WELL_B1F",
            "SlowpokeWell_B1F_Frlg",
            "FLAG_SLOWPOKE_WELL_FIRST_ENTRY_REACHED",
            "FLAG_SLOWPOKE_WELL_KURT_PARTNER_REACHED",
            "FLAG_SLOWPOKE_WELL_ROCKET_EVIDENCE_REACHED",
            "SlowpokeWell_B1F_Frlg_Text_KurtPartner",
            "SlowpokeWell_B1F_Frlg_Text_RocketReturn",
            "SlowpokeWell_B1F_Frlg_Text_GoldDustEvidence",
            "SlowpokeWell_B1F_Frlg_Text_SlowpokeRescue",
            "SlowpokeWell_B1F_Frlg_Text_BugsyUnlock",
            "Bugsy Gym next",
        ):
            if marker not in patch:
                errors.append(f"patch 0054 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Slowpoke Well spec",
            ("Kurt enters the Well", "Gold Dust quietly betrays Rocket", "bugsy_gym_challenge"),
        ),
        (
            PLAN,
            "Slowpoke Well plan",
            ("Add a failing validator", "Add `MAP_SLOWPOKE_WELL_B1F`", "Build the ROM"),
        ),
    ):
        if not doc_path.exists():
            errors.append(f"missing {doc_name}")
            continue
        doc = read(doc_path)
        for marker in markers:
            if marker not in doc:
                errors.append(f"{doc_name} missing marker: {marker}")
    return errors


def validate_engine() -> list[str]:
    errors: list[str] = []
    flags = read(ENGINE / "include" / "constants" / "flags_frlg.h")
    map_groups = read(ENGINE / "data" / "maps" / "map_groups.json")
    azalea_map_path = ENGINE / "data" / "maps" / "AzaleaTown_Frlg" / "map.json"
    well_map_path = ENGINE / "data" / "maps" / "SlowpokeWell_B1F_Frlg" / "map.json"
    well_scripts_path = ENGINE / "data" / "maps" / "SlowpokeWell_B1F_Frlg" / "scripts.inc"

    for marker in (
        "#define FLAG_SLOWPOKE_WELL_FIRST_ENTRY_REACHED   0x0BE",
        "#define FLAG_SLOWPOKE_WELL_KURT_PARTNER_REACHED   0x0BF",
        "#define FLAG_SLOWPOKE_WELL_ROCKET_EVIDENCE_REACHED   0x0C0",
    ):
        if marker not in flags:
            errors.append(f"flags_frlg.h missing marker: {marker}")
    if '"SlowpokeWell_B1F_Frlg"' not in map_groups:
        errors.append("map_groups.json missing SlowpokeWell_B1F_Frlg")
    if not azalea_map_path.exists():
        errors.append("missing AzaleaTown_Frlg map.json before Slowpoke Well warp validation")
    elif '"dest_map": "MAP_SLOWPOKE_WELL_B1F"' not in read(azalea_map_path):
        errors.append("Azalea map missing warp to MAP_SLOWPOKE_WELL_B1F")

    if not well_map_path.exists():
        errors.append("missing SlowpokeWell_B1F_Frlg map.json")
    else:
        well_map = read(well_map_path)
        for marker in (
            '"id": "MAP_SLOWPOKE_WELL_B1F"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_ROCKET_HIDEOUT_B1F"',
            '"dest_map": "MAP_AZALEA_TOWN"',
            "SlowpokeWell_B1F_Frlg_EventScript_KurtPartner",
            "SlowpokeWell_B1F_Frlg_EventScript_RocketReturn",
            "SlowpokeWell_B1F_Frlg_EventScript_GoldDustEvidence",
            "SlowpokeWell_B1F_Frlg_EventScript_SlowpokeRescue",
            "SlowpokeWell_B1F_Frlg_EventScript_RedOutsideWatch",
            "SlowpokeWell_B1F_Frlg_EventScript_SilverTrace",
            "SlowpokeWell_B1F_Frlg_EventScript_BugsyUnlock",
        ):
            if marker not in well_map:
                errors.append(f"Slowpoke Well map.json missing marker: {marker}")

    if not well_scripts_path.exists():
        errors.append("missing SlowpokeWell_B1F_Frlg scripts.inc")
    else:
        scripts = read(well_scripts_path)
        for marker in (
            "SlowpokeWell_B1F_Frlg_MapScripts",
            "FLAG_SLOWPOKE_WELL_FIRST_ENTRY_REACHED",
            "FLAG_SLOWPOKE_WELL_KURT_PARTNER_REACHED",
            "FLAG_SLOWPOKE_WELL_ROCKET_EVIDENCE_REACHED",
            "KURT: This is not a market",
            "ROCKET: The tails are proof",
            "GOLD DUST: Rocket makes",
            "SLOWPOKE: ...Yawn...",
            "RED: I am outside",
            "SILVER TRACE: He saw",
            "WorldLink: Bugsy Gym next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Slowpoke Well scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act2 = next((act for act in johto.get("acts", []) if act.get("id") == "act_2_azalea_goldenrod"), {})
    for event_id in (
        "slowpoke_well_first_entry",
        "kurt_slowpoke_well_partner",
        "rocket_slowpoke_tail_operation",
        "gold_dust_betrays_rocket_evidence",
        "red_outside_well_watch",
        "silver_well_shadow_no_battle",
        "slowpoke_rescue_logged",
        "bugsy_gym_unlocked_after_well",
        "apricorn_first_batch_tease",
    ):
        if event_id not in act2.get("required_events", []):
            errors.append(f"Johto act 2 missing Slowpoke Well event: {event_id}")
    for unlock_id in (
        "slowpoke_well_live_map",
        "slowpoke_well_story_clear",
        "bugsy_gym_story_gate_open",
        "apricorn_balls_first_batch_tease",
        "johto_rematch_board_tier_1_tease",
    ):
        if unlock_id not in act2.get("unlocks", []):
            errors.append(f"Johto act 2 missing Slowpoke Well unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_SLOWPOKE_WELL_FIRST_ENTRY",
        "WL_JOHTO_KURT_WELL_PARTNER",
        "WL_JOHTO_GOLD_DUST_BETRAYS_ROCKET",
        "WL_JOHTO_SLOWPOKE_RESCUE",
        "WL_JOHTO_BUGSY_GYM_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"slowpoke_well", "azalea_gym"}:
        errors.append("current transition state must record Slowpoke Well or Azalea Gym as current safe hub")
    if transition.get("current_route") not in {"slowpoke_well", "bugsy_gym"}:
        errors.append("current transition state must keep current route as slowpoke_well or bugsy_gym")
    if transition.get("next_required_story_node") not in {"bugsy_gym_challenge", "ilex_forest_first_entry"}:
        errors.append("current transition state must advance next node to bugsy_gym_challenge or ilex_forest_first_entry")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_slowpoke_well_first_entry", {})
    if band.get("companions", {}).get("kurt", {}).get("event") != "slowpoke_well_partner":
        errors.append("Rival progression must set Kurt as Slowpoke Well partner")
    if band.get("companions", {}).get("red", {}).get("event") != "outside_well_watch":
        errors.append("Rival progression must set Red as outside Well watch")
    if band.get("rivals", {}).get("silver", {}).get("event") != "well_shadow_no_battle":
        errors.append("Rival progression must set Silver as Well shadow with no battle")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0054-slowpoke-well-first-entry.patch",
        "validate_slowpoke_well_first_entry.py",
        "Slowpoke Well first entry",
    ):
        if marker not in notes:
            errors.append(f"Build notes missing marker: {marker}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_docs())
    errors.extend(validate_engine())
    errors.extend(validate_design_data())
    errors.extend(validate_build_notes())

    if errors:
        print("Slowpoke Well first entry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Slowpoke Well first entry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
