#!/usr/bin/env python3
"""Validate the Viridian Giovanni sponsor-pressure slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0034-viridian-giovanni-sponsor-pressure.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-viridian-giovanni-sponsor-pressure-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-viridian-giovanni-sponsor-pressure.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0034-viridian-giovanni-sponsor-pressure.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0034-viridian-giovanni-sponsor-pressure.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "ViridianCity_Gym_Text_WorldLinkEarthBadge",
            "My sponsor mistook Rocket for a lever",
            "The Meridian Gate was never mine alone",
            "WorldLink: Earth Badge verified",
            "Johto remains locked",
            "Victory Road route active",
        ):
            if marker not in patch:
                errors.append(f"patch 0034 missing marker: {marker}")

    for doc, label, markers in (
        (
            SPEC,
            "Viridian Giovanni sponsor pressure spec",
            ("Viridian Giovanni Sponsor Pressure Design", "classic eighth Gym", "Johto remains locked"),
        ),
        (
            PLAN,
            "Viridian Giovanni sponsor pressure plan",
            ("Update Giovanni's Viridian Gym text", "Export the engine delta", "Run full validation"),
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
    gym = read(ENGINE / "data" / "maps" / "ViridianCity_Gym_Frlg" / "scripts.inc")

    for marker in (
        "msgbox ViridianCity_Gym_Text_WorldLinkEarthBadge",
        "This Gym is not a hideout anymore",
        "My sponsor mistook Rocket for a lever",
        "The Meridian Gate was never mine alone",
        "WorldLink: Earth Badge verified",
        "Kanto badge circuit complete",
        "Victory Road route active",
        "Johto remains locked until",
        "Indigo clearance",
        "Do not mistake obedience for trust",
    ):
        if marker not in gym:
            errors.append(f"Viridian Gym scripts missing marker: {marker}")

    for marker in (
        "The Leader came back with Rocket",
        "shadows behind him",
        "sponsor orders",
        "Viridian is not just a Gym today",
    ):
        if marker not in gym:
            errors.append(f"Viridian Gym support text missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))

    act6 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_6_cinnabar_viridian"), {})
    for event_id in (
        "viridian_gym_sponsor_pressure",
        "giovanni_rocket_kanto_retreat",
        "earth_badge_worldlink_victory_road_handoff",
    ):
        if event_id not in act6.get("required_events", []):
            errors.append(f"Kanto act 6 missing event: {event_id}")

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    if "johto_travel" not in act7.get("unlocks", []):
        errors.append("Kanto act 7 must retain Johto travel unlock after Indigo")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_VIRIDIAN_SPONSOR_PRESSURE",
        "WL_KANTO_GIOVANNI_SPONSOR_CRACK",
        "WL_KANTO_EARTH_BADGE_VICTORY_ROAD",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    earth_badge_message = next(
        (message for message in messages.get("messages", []) if message.get("id") == "WL_KANTO_EARTH_BADGE_VICTORY_ROAD"),
        {},
    )
    earth_badge_text = earth_badge_message.get("text", "")
    for marker in ("Victory Road", "Johto remains locked", "Indigo"):
        if marker not in earth_badge_text:
            errors.append(f"Earth Badge WorldLink message missing marker: {marker}")

    band = rivals.get("progression_bands", {}).get("viridian_giovanni_sponsor_pressure", {})
    if not band:
        errors.append("Rival progression missing viridian_giovanni_sponsor_pressure band")
    else:
        companions = band.get("companions", {})
        rivals_data = band.get("rivals", {})
        if companions.get("red", {}).get("event") != "red_viridian_giovanni_sponsor_reflection":
            errors.append("Viridian band must include Red's sponsor reflection")
        if rivals_data.get("lyra", {}).get("event") != "lyra_johto_still_locked_tease":
            errors.append("Viridian band must keep Lyra as locked Johto tease")
        if "blue" not in rivals_data:
            errors.append("Viridian band must include Blue's Route 22 pressure")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0034-viridian-giovanni-sponsor-pressure.patch",
        "validate_viridian_giovanni_sponsor_pressure.py",
        "Viridian Giovanni sponsor pressure",
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
        print("Viridian Giovanni sponsor pressure validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Viridian Giovanni sponsor pressure validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
