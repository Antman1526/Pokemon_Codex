#!/usr/bin/env python3
"""Validate the Blaine Phoenix ethics and Volcano Badge handoff slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0033-blaine-phoenix-ethics.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-blaine-phoenix-ethics-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-blaine-phoenix-ethics.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0033-blaine-phoenix-ethics.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0033-blaine-phoenix-ethics.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "CinnabarIsland_Gym_Text_BlaineIntro",
            "Phoenix calls old fire rebirth",
            "Recovery is not ownership",
            "WorldLink: Volcano Badge verified",
            "Viridian's door is moving",
        ):
            if marker not in patch:
                errors.append(f"patch 0033 missing marker: {marker}")

    for doc, label, markers in (
        (
            SPEC,
            "Blaine Phoenix ethics spec",
            ("Blaine Phoenix Ethics Design", "classic quiz Gym", "Recovery is not ownership"),
        ),
        (
            PLAN,
            "Blaine Phoenix ethics plan",
            ("Update Blaine's intro", "Export the engine delta", "Run full validation"),
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
    gym = read(ENGINE / "data" / "maps" / "CinnabarIsland_Gym_Frlg" / "scripts.inc")

    for marker in (
        "Phoenix calls old fire rebirth",
        "Recovery is not ownership",
        "creation without restraint",
        "WorldLink: Volcano Badge verified",
        "Phoenix ethics logged",
        "Viridian's door is moving",
        "Ask why a thing should return",
    ):
        if marker not in gym:
            errors.append(f"Cinnabar Gym scripts missing marker: {marker}")

    for marker in (
        "BLAINE kept the quiz machines",
        "consent before revival",
        "life is not a trophy",
    ):
        if marker not in gym:
            errors.append(f"Cinnabar Gym support text missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))

    act6 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_6_cinnabar_viridian"), {})
    for event_id in (
        "blaine_phoenix_ethics_gym",
        "volcano_badge_worldlink_viridian_handoff",
    ):
        if event_id not in act6.get("required_events", []):
            errors.append(f"Kanto act 6 missing event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_BLAINE_PHOENIX_ETHICS",
        "WL_KANTO_VOLCANO_BADGE_VIRIDIAN_HANDOFF",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    band = rivals.get("progression_bands", {}).get("blaine_phoenix_ethics", {})
    if not band:
        errors.append("Rival progression missing blaine_phoenix_ethics band")
    else:
        if band.get("companions", {}).get("red", {}).get("event") != "red_after_blaine_restraint_reflection":
            errors.append("Blaine band must include Red's post-Blaine restraint reflection")
        if "blue" not in band.get("rivals", {}):
            errors.append("Blaine band must include Blue's Cinnabar pressure")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0033-blaine-phoenix-ethics.patch",
        "validate_blaine_phoenix_ethics.py",
        "Blaine Phoenix ethics",
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
        print("Blaine Phoenix ethics validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Blaine Phoenix ethics validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
