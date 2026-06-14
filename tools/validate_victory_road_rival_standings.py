#!/usr/bin/env python3
"""Validate the Victory Road rival standings and Indigo readiness slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0035-victory-road-rival-standings.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-victory-road-rival-standings-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-victory-road-rival-standings.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0035-victory-road-rival-standings.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0035-victory-road-rival-standings.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "Route22_Text_LateRivalIntro",
            "Red is waiting at the gate",
            "WorldLink standings",
            "Victory Road is not a shortcut",
            "World Circuit Passport",
        ):
            if marker not in patch:
                errors.append(f"patch 0035 missing marker: {marker}")

    for doc, label, markers in (
        (
            SPEC,
            "Victory Road rival standings spec",
            ("Victory Road Rival Standings Design", "Route 22 Blue", "World Circuit Passport"),
        ),
        (
            PLAN,
            "Victory Road rival standings plan",
            ("Update Route 22 late Blue text", "Export the engine delta", "Run full validation"),
        ),
    ):
        if not doc.exists():
            errors.append(f"missing {label}")
        else:
            text = read(doc)
            for marker in markers:
                if marker not in text:
                    errors.append(f"{label} missing marker: {marker}")
    return errors


def validate_engine_text() -> list[str]:
    errors: list[str] = []
    route22 = read(ENGINE / "data" / "maps" / "Route22_Frlg" / "scripts.inc")
    victory1 = read(ENGINE / "data" / "maps" / "VictoryRoad_1F_Frlg" / "scripts.inc")
    victory2 = read(ENGINE / "data" / "maps" / "VictoryRoad_2F_Frlg" / "scripts.inc")
    victory3 = read(ENGINE / "data" / "maps" / "VictoryRoad_3F_Frlg" / "scripts.inc")
    indigo = read(ENGINE / "data" / "maps" / "IndigoPlateau_PokemonCenter_1F_Frlg" / "scripts.inc")

    for marker in (
        "Red is waiting at the gate",
        "Misty and Brock sent League notes",
        "this is where I pass",
        "both of you",
        "Smell ya at Indigo",
    ):
        if marker not in route22:
            errors.append(f"Route 22 late rival text missing marker: {marker}")

    for marker in (
        "Victory Road is not a shortcut",
        "rival feed goes quiet",
        "in caves",
    ):
        if marker not in victory1:
            errors.append(f"Victory Road 1F text missing marker: {marker}")

    for marker in (
        "WorldLink standings",
        "Blue came through angry",
        "Ava marked safe switch routes",
    ):
        if marker not in victory2:
            errors.append(f"Victory Road 2F text missing marker: {marker}")

    for marker in (
        "Red stopped at the threshold",
        "Dax left training marks",
        "Kanto League does not",
        "allow partners",
    ):
        if marker not in victory3:
            errors.append(f"Victory Road 3F text missing marker: {marker}")

    for marker in (
        "Red, Misty, and Brock",
        "are outside",
        "World Circuit Passport",
        "Johto stays locked until the",
        "Champion record clears",
    ):
        if marker not in indigo:
            errors.append(f"Indigo Pokemon Center text missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    for event_id in (
        "route22_blue_league_pressure",
        "victory_road_rival_standings",
        "indigo_companion_ready_room",
    ):
        if event_id not in act7.get("required_events", []):
            errors.append(f"Kanto act 7 missing event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_ROUTE22_BLUE_LEAGUE_PRESSURE",
        "WL_KANTO_VICTORY_ROAD_RIVAL_STANDINGS",
        "WL_KANTO_INDIGO_COMPANION_READY",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    standings_message = next(
        (message for message in messages.get("messages", []) if message.get("id") == "WL_KANTO_VICTORY_ROAD_RIVAL_STANDINGS"),
        {},
    )
    standings_text = standings_message.get("text", "")
    for marker in ("Blue", "Ava", "Dax", "WorldLink pauses cave feed"):
        if marker not in standings_text:
            errors.append(f"Victory Road standings WorldLink message missing marker: {marker}")

    band = rivals.get("progression_bands", {}).get("victory_road_rival_standings", {})
    if not band:
        errors.append("Rival progression missing victory_road_rival_standings band")
    else:
        companions = band.get("companions", {})
        rivals_data = band.get("rivals", {})
        if companions.get("red", {}).get("event") != "red_victory_road_threshold":
            errors.append("Victory Road band must include Red's threshold scene")
        if rivals_data.get("blue", {}).get("event") != "blue_route22_final_kanto_pressure":
            errors.append("Victory Road band must include Blue's Route 22 pressure")
        if rivals_data.get("lyra", {}).get("event") != "lyra_indigo_lock_final_tease":
            errors.append("Victory Road band must keep Lyra locked until Champion record")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0035-victory-road-rival-standings.patch",
        "validate_victory_road_rival_standings.py",
        "Victory Road rival standings",
    ):
        if marker not in notes:
            errors.append(f"Build notes missing marker: {marker}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_docs())
    errors.extend(validate_engine_text())
    errors.extend(validate_design_data())
    errors.extend(validate_build_notes())

    if errors:
        print("Victory Road rival standings validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Victory Road rival standings validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
