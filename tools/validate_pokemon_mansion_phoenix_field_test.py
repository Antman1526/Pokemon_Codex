#!/usr/bin/env python3
"""Validate the Pokemon Mansion Phoenix field-test and Secret Key slice."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str, errors: list[str]) -> str:
    full_path = ROOT / path
    if not full_path.exists():
        errors.append(f"Missing {path}")
        return ""
    return full_path.read_text(encoding="utf-8")


def require_markers(name: str, text: str, markers: tuple[str, ...], errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{name} missing marker: {marker}")


def validate_patch(errors: list[str]) -> None:
    patch_path = ROOT / "patches/engine/0031-pokemon-mansion-phoenix-field-test.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0031-pokemon-mansion-phoenix-field-test.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Pokemon Mansion Phoenix patch",
        patch,
        (
            "data/maps/PokemonMansion_1F_Frlg/scripts.inc",
            "data/maps/PokemonMansion_2F_Frlg/scripts.inc",
            "data/maps/PokemonMansion_3F_Frlg/scripts.inc",
            "data/maps/PokemonMansion_B1F_Frlg/scripts.inc",
            "PokemonMansion_1F_Text_TedIntro",
            "Phoenix field test",
            "restoration ledger",
            "Mewtwo",
            "Secret Key",
            "Blaine",
            "WorldLink",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml", errors)
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "mansion_phoenix_field_test",
            "mansion_restoration_ledger",
            "mansion_mewtwo_birth_warning",
            "secret_key_blaine_handoff",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml", errors)
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_MANSION_PHOENIX_FIELD_TEST",
            "WL_KANTO_RESTORATION_LEDGER",
            "WL_KANTO_SECRET_KEY_BLAINE_HANDOFF",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml", errors)
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "pokemon_mansion_phoenix_field_test",
            "red_mansion_restraint_check",
            "brock_mansion_revival_ethics",
            "ava_mansion_phoenix_field_test",
            "blue_secret_key_pressure",
            "dax_mansion_switch_report",
        ),
        errors,
    )


def validate_docs(errors: list[str]) -> None:
    spec = read("docs/superpowers/specs/2026-06-14-pokemon-mansion-phoenix-field-test-design.md", errors)
    require_markers(
        "Pokemon Mansion Phoenix spec",
        spec,
        (
            "Pokemon Mansion Phoenix Field Test Design",
            "first Phoenix-linked battle",
            "Secret Key becomes a Blaine handoff",
            "Mewtwo remains unresolved",
            "does not rebalance Blaine",
        ),
        errors,
    )

    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md", errors)
    require_markers(
        "build notes",
        notes,
        (
            "0031-pokemon-mansion-phoenix-field-test.patch",
            "validate_pokemon_mansion_phoenix_field_test.py",
            "Pokemon Mansion 1F Phoenix-linked Scientist Ted battle text",
            "Pokemon Mansion 2F restoration ledger diary rewrite",
            "Pokemon Mansion 3F Mewtwo birth warning rewrite",
            "Pokemon Mansion B1F Secret Key Blaine handoff text",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_docs(errors)

    if errors:
        print("Pokemon Mansion Phoenix validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Pokemon Mansion Phoenix validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
