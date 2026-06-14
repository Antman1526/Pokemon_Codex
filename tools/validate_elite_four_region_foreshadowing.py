#!/usr/bin/env python3
"""Validate the Elite Four region-foreshadowing slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0036-elite-four-region-foreshadowing.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-elite-four-region-foreshadowing-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-elite-four-region-foreshadowing.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0036-elite-four-region-foreshadowing.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0036-elite-four-region-foreshadowing.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "PokemonLeague_LoreleisRoom_Text_Intro",
            "ice islands past KANTO",
            "Johto keeps old discipline",
            "Moonlight listens to grief",
            "Dragons carry old maps",
        ):
            if marker not in patch:
                errors.append(f"patch 0036 missing marker: {marker}")

    for doc, label, markers in (
        (
            SPEC,
            "Elite Four region foreshadowing spec",
            ("Elite Four Region Foreshadowing Design", "Lorelei", "Johto", "World Circuit"),
        ),
        (
            PLAN,
            "Elite Four region foreshadowing plan",
            ("Update Elite Four text", "Export the engine delta", "Run full validation"),
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
    lorelei = read(ENGINE / "data" / "maps" / "PokemonLeague_LoreleisRoom_Frlg" / "scripts.inc")
    bruno = read(ENGINE / "data" / "maps" / "PokemonLeague_BrunosRoom_Frlg" / "scripts.inc")
    agatha = read(ENGINE / "data" / "maps" / "PokemonLeague_AgathasRoom_Frlg" / "scripts.inc")
    lance = read(ENGINE / "data" / "maps" / "PokemonLeague_LancesRoom_Frlg" / "scripts.inc")

    for marker in (
        "ice islands past KANTO",
        "A badge is a passport",
        "Alola keeps warm seas",
    ):
        if marker not in lorelei:
            errors.append(f"Lorelei text missing marker: {marker}")

    for marker in (
        "Johto keeps old discipline",
        "bells, towers, and vows",
        "Strength is a tradition",
    ):
        if marker not in bruno:
            errors.append(f"Bruno text missing marker: {marker}")

    for marker in (
        "Moonlight listens to grief",
        "Lavender was only the first door",
        "Do not let it wear your face",
    ):
        if marker not in agatha:
            errors.append(f"Agatha text missing marker: {marker}")

    for marker in (
        "Dragons carry old maps",
        "Blackthorn",
        "World Circuit",
        "Blue is Champion now",
    ):
        if marker not in lance:
            errors.append(f"Lance text missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    for event_id in (
        "elite_four_region_foreshadowing",
        "lorelei_alola_ice_island_signal",
        "bruno_johto_tradition_signal",
        "agatha_moonlight_grief_signal",
        "lance_world_circuit_dragon_warning",
    ):
        if event_id not in act7.get("required_events", []):
            errors.append(f"Kanto act 7 missing event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_ELITE_FOUR_REGION_SIGNALS",
        "WL_KANTO_LANCE_WORLD_CIRCUIT_WARNING",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    signals_message = next(
        (message for message in messages.get("messages", []) if message.get("id") == "WL_KANTO_ELITE_FOUR_REGION_SIGNALS"),
        {},
    )
    signals_text = signals_message.get("text", "")
    for marker in ("Lorelei", "Bruno", "Agatha", "Lance"):
        if marker not in signals_text:
            errors.append(f"Elite Four WorldLink message missing marker: {marker}")

    band = rivals.get("progression_bands", {}).get("elite_four_region_foreshadowing", {})
    if not band:
        errors.append("Rival progression missing elite_four_region_foreshadowing band")
    else:
        companions = band.get("companions", {})
        rivals_data = band.get("rivals", {})
        if companions.get("red", {}).get("event") != "red_elite_four_silent_watch":
            errors.append("Elite Four band must include Red's silent watch")
        if rivals_data.get("blue", {}).get("event") != "blue_champion_room_waiting":
            errors.append("Elite Four band must include Blue waiting as Champion")
        if rivals_data.get("lyra", {}).get("event") != "lyra_lance_blackthorn_tease":
            errors.append("Elite Four band must include Lyra Blackthorn tease")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0036-elite-four-region-foreshadowing.patch",
        "validate_elite_four_region_foreshadowing.py",
        "Elite Four region foreshadowing",
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
        print("Elite Four region foreshadowing validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Elite Four region foreshadowing validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
