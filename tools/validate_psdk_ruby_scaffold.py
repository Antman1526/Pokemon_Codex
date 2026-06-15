#!/usr/bin/env python3
"""Validate the PSDK Ruby scaffold for Nexus Red."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "psdk" / "nexus-red" / "project" / "scripts" / "nexus_red" / "000_seed_loader.rb"
README = ROOT / "psdk" / "nexus-red" / "project" / "scripts" / "nexus_red" / "README.md"

REQUIRED_MARKERS = (
    "module NexusRed",
    "module SeedData",
    "starter_selector",
    "early_encounters",
    "regions",
    "factions",
    "companions",
    "rivals_worldlink",
    "gameplay_systems",
    "RuntimeState",
    "PFM::GameState",
    "on_player_initialize(:nexus_red)",
    "on_expand_global_variables(:nexus_red)",
)

REQUIRED_REGISTRY_FILES = (
    "oak_lab_first_partner_selector.json",
    "routes_1_to_3_migration_encounters.json",
    "world_region_progression_spine.json",
    "custom_faction_war_registry.json",
    "core_companion_registry.json",
    "rival_worldlink_registry.json",
    "gameplay_systems_registry.json",
)


def validate() -> list[str]:
    errors: list[str] = []
    if not SCRIPT.exists():
        return [f"missing Ruby seed loader: {SCRIPT.relative_to(ROOT)}"]
    if not README.exists():
        errors.append(f"missing Ruby scaffold README: {README.relative_to(ROOT)}")

    content = SCRIPT.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in content:
            errors.append(f"Ruby seed loader missing marker: {marker}")
    for filename in REQUIRED_REGISTRY_FILES:
        if filename not in content:
            errors.append(f"Ruby seed loader missing registry file: {filename}")

    result = subprocess.run(
        ["ruby", "-c", str(SCRIPT)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        errors.append("Ruby syntax check failed:\n" + result.stdout)

    if README.exists():
        readme = README.read_text(encoding="utf-8")
        for marker in ("000_seed_loader.rb", "Data/nexus_red_seed/generated", "generate_psdk_seed_data.py"):
            if marker not in readme:
                errors.append(f"Ruby scaffold README missing marker: {marker}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("PSDK Ruby scaffold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PSDK Ruby scaffold validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
