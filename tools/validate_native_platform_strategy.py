#!/usr/bin/env python3
"""Validate the PC/Mac native platform strategy files."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_design" / "platform_targets.yaml"
DOC = ROOT / "docs" / "PC_MAC_NATIVE_BUILD_STRATEGY.md"
DECISIONS = ROOT / "docs" / "DECISIONS_LOG.md"
README = ROOT / "README.md"
BUILD_NOTES = ROOT / "build_notes" / "PC_MAC_NATIVE_BUILD_NOTES.md"
GBA_STRATEGY = ROOT / "docs" / "GBA_OPENEMU_BUILD_STRATEGY.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-native-pc-mac-migration.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_data() -> list[str]:
    errors: list[str] = []
    if not DATA.exists():
        return ["missing data_design/platform_targets.yaml"]

    data = load_yaml(DATA)
    strategy = data.get("platform_strategy", {})
    if strategy.get("primary_target") != "native_pc_mac":
        errors.append("platform strategy must set primary_target to native_pc_mac")
    if strategy.get("primary_engine_recommendation") != "godot_4_custom_2d_rpg":
        errors.append("platform strategy must recommend godot_4_custom_2d_rpg")
    if strategy.get("legacy_target") != "gba_openemu_prototype":
        errors.append("platform strategy must keep GBA/OpenEmu as legacy prototype")

    targets = data.get("native_targets", {})
    for target in ("windows", "macos"):
        if target not in targets:
            errors.append(f"native_targets missing required target: {target}")
        elif not targets[target].get("required"):
            errors.append(f"{target} target must be required")

    carryover = set(data.get("non_negotiable_design_carryover", []))
    for marker in (
        "all_9_regions_in_order",
        "red_full_game_warm_companion",
        "10_rivals_worldlink_progress",
        "all_pokemon_through_gen_9_catchable_before_final_boss",
        "dynamax_and_tera_after_hoenn",
    ):
        if marker not in carryover:
            errors.append(f"non_negotiable_design_carryover missing {marker}")

    milestones = [item.get("id") for item in data.get("first_native_milestones", [])]
    for milestone in ("native_shell", "pallet_intro", "kanto_brock_slice"):
        if milestone not in milestones:
            errors.append(f"first_native_milestones missing {milestone}")

    return errors


def validate_docs() -> list[str]:
    errors: list[str] = []
    for path, label in (
        (DOC, "PC/Mac native build strategy"),
        (DECISIONS, "decisions log"),
        (README, "README"),
        (BUILD_NOTES, "PC/Mac build notes"),
        (GBA_STRATEGY, "GBA strategy"),
        (PLAN, "native migration plan"),
    ):
        if not path.exists():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")

    if errors:
        return errors

    doc = read(DOC)
    for marker in (
        "native PC/Mac build becomes the primary target",
        "Godot 4",
        "Windows PC",
        "macOS",
        "This is not a GBA ROM anymore",
        "all Pokemon through Generation 9",
    ):
        if marker not in doc:
            errors.append(f"PC/Mac strategy missing marker: {marker}")

    decisions = read(DECISIONS)
    for marker in (
        "native PC/Mac standalone game",
        "Godot 4 custom 2D RPG framework",
        "GBA/OpenEmu path remains a legacy prototype",
    ):
        if marker not in decisions:
            errors.append(f"decisions log missing platform marker: {marker}")

    readme = read(README)
    for marker in (
        "Primary target: native PC/Mac standalone game",
        "Legacy/prototype target: `.gba` playable in OpenEmu",
        "docs/PC_MAC_NATIVE_BUILD_STRATEGY.md",
    ):
        if marker not in readme:
            errors.append(f"README missing native marker: {marker}")

    gba_strategy = read(GBA_STRATEGY)
    if "Superseded for full-game target" not in gba_strategy:
        errors.append("GBA strategy must state it is superseded for the full-game target")

    plan = read(PLAN)
    for marker in (
        "Native Shell",
        "First Playable Native Loop",
        "Kanto Brock Slice",
        "Godot 4",
    ):
        if marker not in plan:
            errors.append(f"native migration plan missing marker: {marker}")

    return errors


def main() -> int:
    errors = validate_data()
    errors.extend(validate_docs())

    if errors:
        print("Native platform strategy validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Native platform strategy validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
