#!/usr/bin/env python3
"""Validate the first native Godot shell for Pokemon Nexus Red."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native" / "nexus-red"
DATA_DIR = ROOT / "data_design"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def require_file(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
        return ""
    return read(path)


def validate_project_files() -> list[str]:
    errors: list[str] = []
    files = {
        "project": NATIVE / "project.godot",
        "main_scene": NATIVE / "scenes" / "Main.tscn",
        "title_scene": NATIVE / "scenes" / "ui" / "TitleScreen.tscn",
        "bedroom_scene": NATIVE / "scenes" / "world" / "Bedroom.tscn",
        "main_script": NATIVE / "src" / "Main.gd",
        "title_script": NATIVE / "src" / "ui" / "TitleScreen.gd",
        "bedroom_script": NATIVE / "src" / "world" / "Bedroom.gd",
        "worldlink_script": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "save_script": NATIVE / "src" / "save" / "SaveState.gd",
        "region_data": NATIVE / "content" / "regions" / "regions.json",
        "faction_data": NATIVE / "content" / "factions" / "factions.json",
        "companion_data": NATIVE / "content" / "companions" / "companions.json",
        "worldlink_data": NATIVE / "content" / "worldlink" / "opening_feed.json",
    }

    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    project = contents["project"]
    for marker in (
        'config/name="POKEMON NEXUS RED"',
        'run/main_scene="res://scenes/Main.tscn"',
        "worldlink",
        "sprint",
        "confirm",
        "cancel",
    ):
        if marker not in project:
            errors.append(f"project.godot missing marker: {marker}")

    for name, marker in (
        ("main_script", "POKEMON NEXUS RED"),
        ("title_script", "New Game"),
        ("title_script", "start_new_game"),
        ("bedroom_scene", "Antman's Bedroom"),
        ("bedroom_script", "Mom"),
        ("worldlink_script", "WorldLink"),
        ("save_script", "current_region"),
    ):
        if marker not in contents[name]:
            errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    for path in (
        NATIVE / "src" / "creature",
        NATIVE / "src" / "trainer",
        NATIVE / "src" / "region",
        NATIVE / "src" / "faction",
        NATIVE / "src" / "companion",
        NATIVE / "src" / "worldlink",
    ):
        if not path.exists():
            errors.append(f"Missing generic internal directory: {path.relative_to(ROOT)}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    regions = load_yaml(DATA_DIR / "region_chapters.yaml").get("regions", {})
    companions = load_yaml(DATA_DIR / "companions.yaml").get("companions", {})

    if "nexus_island" not in regions:
        errors.append("region_chapters.yaml missing final nexus_island chapter")
    else:
        island = regions["nexus_island"]
        if island.get("order") != 10:
            errors.append("nexus_island must be order 10")
        if "full_final_region" not in island.get("mechanic_focus", []):
            errors.append("nexus_island must include full_final_region mechanic focus")
        if "team_rocket" not in island.get("villain_focus", []):
            errors.append("nexus_island must include Team Rocket")
        if "nexus_order" not in island.get("villain_focus", []):
            errors.append("nexus_island must include hidden Nexus Order")

    for dropped_id in ("world_nexus_championship",):
        if dropped_id in regions:
            errors.append(f"region_chapters.yaml should replace {dropped_id} with nexus_island")

    all_villains = {faction for region in regions.values() for faction in region.get("villain_focus", [])}
    for faction in (
        "team_rocket",
        "team_magma",
        "team_aqua",
        "team_phoenix",
        "team_moonlight",
        "team_gold_dust",
        "team_gas",
        "team_clover",
        "nexus_order",
    ):
        if faction not in all_villains:
            errors.append(f"Missing required faction in region villain focus: {faction}")

    for canonical_drop in (
        "team_galactic",
        "team_plasma",
        "team_flare",
        "team_skull",
        "macro_cosmos",
        "team_star",
    ):
        if canonical_drop in all_villains:
            errors.append(f"Canonical dropped team should not be active faction: {canonical_drop}")

    red = companions.get("red", {})
    if red.get("role") != "primary_full_game_companion":
        errors.append("Red must be primary_full_game_companion in companions.yaml")

    for companion_id in ("ash", "misty", "brock", "blue", "may", "bill"):
        if companion_id not in companions:
            errors.append(f"companions.yaml missing companion: {companion_id}")

    return errors


def main() -> int:
    errors = validate_project_files()
    errors.extend(validate_design_data())

    if errors:
        print("Native Godot shell validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Native Godot shell validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
