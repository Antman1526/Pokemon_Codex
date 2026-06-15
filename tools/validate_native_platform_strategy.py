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
PSDK_DOC = ROOT / "docs" / "PSDK_NATIVE_BUILD_STRATEGY.md"
DECISIONS = ROOT / "docs" / "DECISIONS_LOG.md"
README = ROOT / "README.md"
BUILD_NOTES = ROOT / "build_notes" / "PC_MAC_NATIVE_BUILD_NOTES.md"
GBA_STRATEGY = ROOT / "docs" / "GBA_OPENEMU_BUILD_STRATEGY.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-native-pc-mac-migration.md"
PSDK_SCAFFOLD = ROOT / "psdk" / "nexus-red" / "README.md"
PSDK_GITIGNORE = ROOT / "psdk" / "nexus-red" / ".gitignore"
PSDK_SETUP_AUDIT = ROOT / "docs" / "psdk" / "PSDK_SETUP_AUDIT_2026-06-15.md"
PSDK_KANTO_MAPPING = ROOT / "psdk" / "nexus-red" / "docs" / "content-migration" / "KANTO_VERTICAL_SLICE_MAPPING.md"
PSDK_STARTER_IMPORT_CONTRACT = ROOT / "psdk" / "nexus-red" / "docs" / "studio-data-notes" / "STARTER_AND_EARLY_ROUTE_IMPORT_CONTRACT.md"
PSDK_SEED_MANIFEST = ROOT / "psdk" / "nexus-red" / "project" / "Data" / "nexus_red_seed" / "import_manifest.json"


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
    if strategy.get("primary_engine_recommendation") != "pokemon_studio_psdk":
        errors.append("platform strategy must recommend pokemon_studio_psdk")
    if strategy.get("prototype_engine") != "godot_4_custom_2d_rpg":
        errors.append("platform strategy must keep godot_4_custom_2d_rpg as prototype_engine")
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

    layout = data.get("native_project_layout", {})
    if layout.get("primary_root") != "psdk/nexus-red":
        errors.append("native_project_layout must set primary_root to psdk/nexus-red")
    if layout.get("godot_reference_root") != "native/nexus-red":
        errors.append("native_project_layout must keep native/nexus-red as Godot reference root")

    milestones = [item.get("id") for item in data.get("first_native_milestones", [])]
    for milestone in ("psdk_setup_spike", "psdk_project_scaffold", "psdk_pallet_intro", "godot_reference_shell"):
        if milestone not in milestones:
            errors.append(f"first_native_milestones missing {milestone}")

    return errors


def validate_docs() -> list[str]:
    errors: list[str] = []
    for path, label in (
        (DOC, "PC/Mac native build strategy"),
        (PSDK_DOC, "PSDK native build strategy"),
        (DECISIONS, "decisions log"),
        (README, "README"),
        (BUILD_NOTES, "PC/Mac build notes"),
        (GBA_STRATEGY, "GBA strategy"),
        (PLAN, "native migration plan"),
        (PSDK_SCAFFOLD, "PSDK scaffold README"),
        (PSDK_GITIGNORE, "PSDK scaffold gitignore"),
        (PSDK_SETUP_AUDIT, "PSDK setup audit"),
        (PSDK_KANTO_MAPPING, "PSDK Kanto migration mapping"),
        (PSDK_STARTER_IMPORT_CONTRACT, "PSDK starter import contract"),
        (PSDK_SEED_MANIFEST, "PSDK seed manifest"),
    ):
        if not path.exists():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")

    if errors:
        return errors

    doc = read(DOC)
    for marker in (
        "native PC/Mac build remains the primary target",
        "Pokemon Studio / PSDK",
        "validated prototype/reference",
        "Windows PC",
        "macOS",
        "This is not a GBA ROM anymore",
        "all Pokemon through Generation 9",
    ):
        if marker not in doc:
            errors.append(f"PC/Mac strategy missing marker: {marker}")

    psdk_doc = read(PSDK_DOC)
    for marker in (
        "Pokemon Studio plus Pokemon SDK",
        "PSDK",
        "psdk/nexus-red",
        "Tiled-to-PSDK",
        "Godot project under `native/nexus-red/` remains",
    ):
        if marker not in psdk_doc:
            errors.append(f"PSDK strategy missing marker: {marker}")

    decisions = read(DECISIONS)
    for marker in (
        "native PC/Mac standalone game",
        "Pokemon Studio / PSDK becomes the recommended primary production engine",
        "GBA/OpenEmu path remains a legacy prototype",
    ):
        if marker not in decisions:
            errors.append(f"decisions log missing platform marker: {marker}")

    readme = read(README)
    for marker in (
        "Primary target: native PC/Mac standalone game in Pokemon Studio / PSDK",
        "Prototype/reference targets",
        "docs/PSDK_NATIVE_BUILD_STRATEGY.md",
        "docs/PC_MAC_NATIVE_BUILD_STRATEGY.md",
    ):
        if marker not in readme:
            errors.append(f"README missing native marker: {marker}")

    build_notes = read(BUILD_NOTES)
    for marker in (
        "Pokemon Studio / PSDK",
        "validated Godot reference prototype",
        "psdk/nexus-red",
    ):
        if marker not in build_notes:
            errors.append(f"build notes missing PSDK marker: {marker}")

    gba_strategy = read(GBA_STRATEGY)
    if "Superseded for full-game target" not in gba_strategy:
        errors.append("GBA strategy must state it is superseded for the full-game target")

    plan = read(PLAN)
    for marker in (
        "Pokemon Studio / PSDK primary engine pivot",
        "Task P1",
        "Task P2",
        "Godot 4 project as a reference/prototype",
    ):
        if marker not in plan:
            errors.append(f"native migration plan missing marker: {marker}")

    scaffold = read(PSDK_SCAFFOLD)
    for marker in (
        "Pokemon Studio / PSDK",
        "Do not vendor PSDK binaries",
        "native/nexus-red",
        "KANTO_VERTICAL_SLICE_MAPPING.md",
        "STARTER_AND_EARLY_ROUTE_IMPORT_CONTRACT.md",
        "import_manifest.json",
    ):
        if marker not in scaffold:
            errors.append(f"PSDK scaffold missing marker: {marker}")

    psdk_gitignore = read(PSDK_GITIGNORE)
    for marker in (
        "psdk-binaries/",
        "pokemonsdk/",
        "ripped_assets/",
        "*.dmg",
        "*.exe",
    ):
        if marker not in psdk_gitignore:
            errors.append(f"PSDK gitignore missing marker: {marker}")

    setup_audit = read(PSDK_SETUP_AUDIT)
    for marker in (
        "Pokemon Studio v2.9.1",
        "/Users/Antman/Applications/Pokemon Studio.app",
        "Bundled PSDK marker",
        "codesign",
        "Do not commit PSDK binaries",
    ):
        if marker not in setup_audit:
            errors.append(f"PSDK setup audit missing marker: {marker}")

    kanto_mapping = read(PSDK_KANTO_MAPPING)
    for marker in (
        "39-Starter Contract",
        "Routes 1-3 Catchability Contract",
        "WorldLink",
        "Red",
        "native/nexus-red/content/starters/starter_choices.json",
        "STARTER_AND_EARLY_ROUTE_IMPORT_CONTRACT.md",
        "import_manifest.json",
    ):
        if marker not in kanto_mapping:
            errors.append(f"PSDK Kanto mapping missing marker: {marker}")

    starter_import = read(PSDK_STARTER_IMPORT_CONTRACT)
    for marker in (
        "Oak's lab must offer 39 selectable first partners",
        "Bulbasaur, Charmander, Squirtle",
        "Sprigatito, Fuecoco, Quaxly",
        "Eevee, Pikachu, Dratini, Abra, Gastly, Larvitar, Sandile, Kubfu, Staryu, Shroomish, Rockruff, Ralts",
        "Route 1",
        "Route 2",
        "Route 3",
        "Dratini | 6 | 1 | night",
        "Kubfu | 7 | 1 | day",
        "validate_native_early_migration_pool.py",
    ):
        if marker not in starter_import:
            errors.append(f"PSDK starter import contract missing marker: {marker}")

    seed_manifest = read(PSDK_SEED_MANIFEST)
    for marker in (
        "psdk_import_seed_manifest",
        "oak_lab_39_first_partner_selector",
        "routes_1_to_3_migration_encounters",
        "native/nexus-red/content/starters/starter_choices.json",
        "native/nexus-red/content/encounters/route_1_to_3_migration_encounters.json",
        "Red",
        "Antman",
        "worldlink_stub_unlocked",
    ):
        if marker not in seed_manifest:
            errors.append(f"PSDK seed manifest missing marker: {marker}")

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
