#!/usr/bin/env python3
"""Validate the Mt. Moon Nexus Break slice."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0011-mt-moon-nexus-break.patch"
POLICY = ROOT / "data_design" / "red_tag_battle_policy.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_file() -> list[str]:
    if not PATCH.exists():
        return ["missing patch file: 0011-mt-moon-nexus-break.patch"]
    if PATCH.stat().st_size == 0:
        return ["empty patch file: 0011-mt-moon-nexus-break.patch"]
    return []


def validate_red_scene() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "MtMoon_1F_Frlg" / "scripts.inc")
    mt_moon = load_map("MtMoon_1F_Frlg")

    for marker in (
        "MtMoon_1F_EventScript_RedNexusBreak",
        "the museum scan led",
        "Soon we'll fight side by side",
        "MISTY's badge",
    ):
        if marker not in scripts:
            errors.append(f"Mt. Moon 1F missing Red marker: {marker}")

    has_red = any(
        obj.get("graphics_id") == "OBJ_EVENT_GFX_RED"
        and obj.get("script") == "MtMoon_1F_EventScript_RedNexusBreak"
        for obj in mt_moon.get("object_events", [])
    )
    if not has_red:
        errors.append("Mt. Moon 1F missing Red companion object")

    return errors


def validate_b2f_story() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "MtMoon_B2F_Frlg" / "scripts.inc")

    required_markers = (
        "MtMoon_B2F_Text_NexusDomeLogged",
        "MtMoon_B2F_Text_NexusHelixLogged",
        "Antman's first Nexus artifact",
        "Ancient DNA makes a perfect anchor",
        "badge network",
        "museum scan woke the fossils",
        "Tell RED the cave reacted",
        "CINNABAR can read it",
    )
    for marker in required_markers:
        if marker not in scripts:
            errors.append(f"Mt. Moon B2F missing story marker: {marker}")

    dome_log_after_flag = "setflag FLAG_GOT_DOME_FOSSIL\n\tsetflag FLAG_GOT_FOSSIL_FROM_MT_MOON\n\tmsgbox MtMoon_B2F_Text_NexusDomeLogged"
    helix_log_after_flag = "setflag FLAG_GOT_HELIX_FOSSIL\n\tsetflag FLAG_GOT_FOSSIL_FROM_MT_MOON\n\tmsgbox MtMoon_B2F_Text_NexusHelixLogged"
    if dome_log_after_flag not in scripts:
        errors.append("Dome fossil must log as Nexus artifact after fossil flags")
    if helix_log_after_flag not in scripts:
        errors.append("Helix fossil must log as Nexus artifact after fossil flags")

    return errors


def validate_tag_battle_policy() -> list[str]:
    errors: list[str] = []
    if not POLICY.exists():
        return ["missing data_design/red_tag_battle_policy.yaml"]

    data = yaml.safe_load(read(POLICY))
    policy = data.get("red_tag_battle_policy", {})
    if policy.get("design_status") != "approved_direction":
        errors.append("red_tag_battle_policy design_status must be approved_direction")
    if "gym" not in policy.get("gym_rule", "").lower():
        errors.append("red_tag_battle_policy must preserve no-gyms rule")

    cadence = policy.get("region_cadence", {})
    required_regions = {
        "kanto", "johto", "hoenn", "sinnoh_hisui", "unova",
        "kalos", "alola", "galar", "paldea",
    }
    missing = sorted(required_regions - set(cadence))
    if missing:
        errors.append("red_tag_battle_policy missing regions: " + ", ".join(missing))

    kanto = cadence.get("kanto", {})
    if "Mt. Moon" not in kanto.get("early_seed", ""):
        errors.append("Kanto tag-battle policy must seed at Mt. Moon")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_file())
    errors.extend(validate_red_scene())
    errors.extend(validate_b2f_story())
    errors.extend(validate_tag_battle_policy())

    if errors:
        print("Mt. Moon Nexus Break validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Mt. Moon Nexus Break validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
