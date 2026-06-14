#!/usr/bin/env python3
"""Validate the Misty-led Vermilion Surge refinement slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0032-vermilion-misty-surge-refinement.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-vermilion-misty-surge-refinement-design.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_and_spec() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0032-vermilion-misty-surge-refinement.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0032-vermilion-misty-surge-refinement.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MISTY: Surge is not just a Gym",
            "MISTY was right. Bring GROUND answers",
            "gold lapel pin",
        ):
            if marker not in patch:
                errors.append(f"patch 0032 missing marker: {marker}")

    if not SPEC.exists():
        errors.append("missing Vermilion Misty Surge refinement spec")
    else:
        spec = read(SPEC)
        for marker in ("Misty-led Surge prep", "gold lapel pin", "Trail Cutter remains a prototype"):
            if marker not in spec:
                errors.append(f"spec missing marker: {marker}")
    return errors


def validate_engine_text() -> list[str]:
    errors: list[str] = []
    vermilion = read(ENGINE / "data" / "maps" / "VermilionCity_Frlg" / "scripts.inc")
    gym = read(ENGINE / "data" / "maps" / "VermilionCity_Gym_Frlg" / "scripts.inc")
    fan_club = read(ENGINE / "data" / "maps" / "VermilionCity_PokemonFanClub_Frlg" / "scripts.inc")

    for marker in (
        "MISTY: Surge is not just a Gym",
        "Water loses to electricity if you",
        "Win the badge your way",
        "I will keep the harbor calm",
    ):
        if marker not in vermilion:
            errors.append(f"Vermilion Misty prep missing marker: {marker}")

    for marker in (
        "MISTY was right. Bring GROUND answers",
        "before you challenge SURGE",
        "TRAIL CUTTER prototype",
        "Full HM replacement system",
        "pending",
    ):
        if marker not in gym:
            errors.append(f"Vermilion Gym refinement missing marker: {marker}")

    for marker in (
        "gold lapel pin",
        "blank auction card",
        "No name. Just a dust mark",
        "CELADON",
    ):
        if marker not in fan_club:
            errors.append(f"Fan Club Gold Dust clue missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))

    act3 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_3_cerulean_to_vermilion"), {})
    for event_id in (
        "misty_led_surge_prep_refinement",
        "fan_club_gold_lapel_mystery_refinement",
    ):
        if event_id not in act3.get("required_events", []):
            errors.append(f"Kanto act 3 missing refinement event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    if "WL_KANTO_MISTY_SURGE_PREP" not in message_ids:
        errors.append("WorldLink messages missing Misty Surge prep id")

    vermilion = rivals.get("progression_bands", {}).get("vermilion_surge", {})
    misty_event = vermilion.get("companions", {}).get("misty", {}).get("event")
    if misty_event != "misty_led_surge_training_and_harbor_watch":
        errors.append("Rival progression must mark Misty as the Surge prep lead")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0032-vermilion-misty-surge-refinement.patch",
        "validate_vermilion_misty_surge_refinement.py",
        "Misty-led Surge prep",
    ):
        if marker not in notes:
            errors.append(f"Build notes missing marker: {marker}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_and_spec())
    errors.extend(validate_engine_text())
    errors.extend(validate_design_data())
    errors.extend(validate_build_notes())

    if errors:
        print("Vermilion Misty Surge refinement validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Vermilion Misty Surge refinement validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
