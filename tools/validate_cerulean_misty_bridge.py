#!/usr/bin/env python3
"""Validate the Cerulean Misty Bridge setup slice."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0012-cerulean-misty-bridge-setup.patch"
POLICY = ROOT / "data_design" / "red_tag_battle_policy.yaml"
WORLD_MAP_GUIDE = ROOT / "data_design" / "world_map_guide_sources.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_file() -> list[str]:
    if not PATCH.exists():
        return ["missing patch file: 0012-cerulean-misty-bridge-setup.patch"]
    if PATCH.stat().st_size == 0:
        return ["empty patch file: 0012-cerulean-misty-bridge-setup.patch"]
    return []


def validate_cerulean_city() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "CeruleanCity_Frlg" / "scripts.inc")
    city = load_map("CeruleanCity_Frlg")

    for marker in (
        "CeruleanCity_EventScript_RedBridgeSetup",
        "CeruleanCity_EventScript_MistyCompanion",
        "I won't fight",
        "CASCADEBADGE network",
        "WorldLink picked up the same pulse",
    ):
        if marker not in scripts:
            errors.append(f"Cerulean City missing marker: {marker}")

    object_events = city.get("object_events", [])
    has_red = any(
        obj.get("graphics_id") == "OBJ_EVENT_GFX_RED"
        and obj.get("script") == "CeruleanCity_EventScript_RedBridgeSetup"
        for obj in object_events
    )
    if not has_red:
        errors.append("Cerulean City missing Red bridge setup object")

    has_misty = any(
        obj.get("graphics_id") == "OBJ_EVENT_GFX_MISTY"
        and obj.get("script") == "CeruleanCity_EventScript_MistyCompanion"
        for obj in object_events
    )
    if not has_misty:
        errors.append("Cerulean City missing Misty companion object")

    return errors


def validate_cerulean_gym() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "CeruleanCity_Gym_Frlg" / "scripts.inc")

    for marker in (
        "CeruleanCity_Gym_Text_MistyMeetOutside",
        "Meet me outside the GYM",
        "badge battle had to\\l",
        "stay yours",
    ):
        if marker not in scripts:
            errors.append(f"Cerulean Gym missing marker: {marker}")

    give_tm_sequence = (
        "setflag FLAG_GOT_TM03_FROM_MISTY\n"
        "\tmsgbox CeruleanCity_Gym_Text_ExplainTM03\n"
        "\tmsgbox CeruleanCity_Gym_Text_MistyMeetOutside"
    )
    if give_tm_sequence not in scripts:
        errors.append("Misty must point to outside scene after giving TM03")

    return errors


def validate_route24() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "Route24_Frlg" / "scripts.inc")
    route = load_map("Route24_Frlg")

    for marker in (
        "Route24_EventScript_RedTagSetup",
        "WorldLink readings",
        "A fossil woke up MT. MOON",
        "Your CASCADEBADGE woke CERULEAN",
        "First real tag",
        "you and me",
    ):
        if marker not in scripts:
            errors.append(f"Route 24 missing marker: {marker}")

    has_red = any(
        obj.get("graphics_id") == "OBJ_EVENT_GFX_RED"
        and obj.get("script") == "Route24_EventScript_RedTagSetup"
        for obj in route.get("object_events", [])
    )
    if not has_red:
        errors.append("Route 24 missing Red tag setup object")

    return errors


def validate_policy() -> list[str]:
    errors: list[str] = []
    if not POLICY.exists():
        return ["missing data_design/red_tag_battle_policy.yaml"]

    data = yaml.safe_load(read(POLICY))
    kanto = data.get("red_tag_battle_policy", {}).get("region_cadence", {}).get("kanto", {})
    candidate = kanto.get("first_true_tag_battle_candidate", "")
    if "Route 25" not in candidate:
        errors.append("Kanto first true tag battle must now point to Route 25")
    if "classic Nugget Bridge" not in candidate:
        errors.append("Kanto tag battle policy must preserve classic Nugget Bridge first")

    return errors


def validate_world_map_guide() -> list[str]:
    errors: list[str] = []
    if not WORLD_MAP_GUIDE.exists():
        return ["missing data_design/world_map_guide_sources.yaml"]

    data = yaml.safe_load(read(WORLD_MAP_GUIDE))
    guide = data.get("world_map_guide_sources", [{}])[0]
    regions = guide.get("region_order", [])
    if len(regions) != 9:
        errors.append(f"World map guide must list 9 regions, found {len(regions)}")
    region_ids = {region.get("region") for region in regions}
    expected = {
        "kanto",
        "johto",
        "hoenn",
        "sinnoh_hisui",
        "unova",
        "kalos",
        "alola",
        "galar",
        "paldea",
    }
    missing = sorted(expected - region_ids)
    if missing:
        errors.append("World map guide missing regions: " + ", ".join(missing))

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_file())
    errors.extend(validate_cerulean_city())
    errors.extend(validate_cerulean_gym())
    errors.extend(validate_route24())
    errors.extend(validate_policy())
    errors.extend(validate_world_map_guide())

    if errors:
        print("Cerulean Misty Bridge validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Cerulean Misty Bridge validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
