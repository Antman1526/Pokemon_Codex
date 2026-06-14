#!/usr/bin/env python3
"""Validate the Champion Blue emotional finale slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0037-champion-blue-emotional-finale.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-champion-blue-emotional-finale-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-champion-blue-emotional-finale.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0037-champion-blue-emotional-finale.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0037-champion-blue-emotional-finale.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "PokemonLeague_ChampionsRoom_Text_Intro",
            "I became Champion first",
            "I trained alone",
            "You beat my best",
            "Hall of Fame record",
            "comes first",
        ):
            if marker not in patch:
                errors.append(f"patch 0037 missing marker: {marker}")

    for doc, label, markers in (
        (
            SPEC,
            "Champion Blue emotional finale spec",
            ("Champion Blue Emotional Finale Design", "Blue", "Hall of Fame record comes first"),
        ),
        (
            PLAN,
            "Champion Blue emotional finale plan",
            ("Update Champion Blue text", "Export the engine delta", "Run full validation"),
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
    champion = read(ENGINE / "data" / "maps" / "PokemonLeague_ChampionsRoom_Frlg" / "scripts.inc")

    for marker in (
        "I became Champion first",
        "Red saw you",
        "I trained alone",
        "beat the friend who had",
        "everybody",
        "You beat my best",
        "WorldLink stays closed",
        "Red, Misty, and Brock",
        "are waiting outside this room",
        "Blue forgot that trust",
        "Hall of Fame record",
        "comes first",
        "World Circuit Passport comes",
        "after proof",
    ):
        if marker not in champion:
            errors.append(f"Champion room text missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    for event_id in (
        "champion_blue_emotional_finale",
        "oak_hall_of_fame_before_passport",
    ):
        if event_id not in act7.get("required_events", []):
            errors.append(f"Kanto act 7 missing event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_CHAMPION_BLUE_FINALE",
        "WL_KANTO_HALL_OF_FAME_BEFORE_PASSPORT",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    hof_message = next(
        (message for message in messages.get("messages", []) if message.get("id") == "WL_KANTO_HALL_OF_FAME_BEFORE_PASSPORT"),
        {},
    )
    hof_text = hof_message.get("text", "")
    for marker in ("Hall of Fame", "World Circuit Passport", "Johto remains locked"):
        if marker not in hof_text:
            errors.append(f"Hall of Fame WorldLink message missing marker: {marker}")

    band = rivals.get("progression_bands", {}).get("champion_blue_emotional_finale", {})
    if not band:
        errors.append("Rival progression missing champion_blue_emotional_finale band")
    else:
        companions = band.get("companions", {})
        rivals_data = band.get("rivals", {})
        if companions.get("red", {}).get("event") != "red_hall_of_fame_wait":
            errors.append("Champion band must include Red waiting at Hall of Fame")
        if rivals_data.get("blue", {}).get("event") != "blue_champion_loss_trust_breakthrough":
            errors.append("Champion band must include Blue's trust breakthrough")
        if rivals_data.get("lyra", {}).get("event") != "lyra_johto_locked_after_champion_tease":
            errors.append("Champion band must keep Lyra locked until passport")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0037-champion-blue-emotional-finale.patch",
        "validate_champion_blue_emotional_finale.py",
        "Champion Blue emotional finale",
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
        print("Champion Blue emotional finale validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Champion Blue emotional finale validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
