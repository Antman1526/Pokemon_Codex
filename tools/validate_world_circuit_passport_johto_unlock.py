#!/usr/bin/env python3
"""Validate the World Circuit Passport and Johto unlock slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0038-world-circuit-passport-johto-unlock.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-world-circuit-passport-johto-unlock-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-world-circuit-passport-johto-unlock.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
REGION_PROGRESSION = ROOT / "data_design" / "worldlink_region_progression.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0038-world-circuit-passport-johto-unlock.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0038-world-circuit-passport-johto-unlock.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT",
            "PalletTown_ProfessorOaksLab_EventScript_WorldCircuitPassport",
            "World Circuit Passport",
            "Johto travel is now live",
            "Lyra's profile is live",
        ):
            if marker not in patch:
                errors.append(f"patch 0038 missing marker: {marker}")

    for doc, label, markers in (
        (
            SPEC,
            "World Circuit Passport Johto unlock spec",
            ("World Circuit Passport Johto Unlock Design", "Oak", "Johto becomes live"),
        ),
        (
            PLAN,
            "World Circuit Passport Johto unlock plan",
            ("Add passport flag and Oak Lab scene", "Export the engine delta", "Run full validation"),
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
    oak_lab = read(ENGINE / "data" / "maps" / "PalletTown_ProfessorOaksLab_Frlg" / "scripts.inc")
    flags = read(ENGINE / "include" / "constants" / "flags_frlg.h")

    if "#define FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT" not in flags:
        errors.append("flags_frlg.h missing FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT alias")

    for marker in (
        "goto_if_unset FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT",
        "PalletTown_ProfessorOaksLab_EventScript_WorldCircuitPassport",
        "setflag FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT",
        "Hall of Fame record cleared",
        "World Circuit Passport",
        "Johto travel is now live",
        "World Circuit Gate",
        "Lyra's profile is live",
        "New Bark Town",
    ):
        if marker not in oak_lab:
            errors.append(f"Oak Lab passport scene missing marker: {marker}")

    national_dex_index = oak_lab.find("PalletTown_ProfessorOaksLab_EventScript_TryStartNationalDexScene")
    passport_index = oak_lab.find("PalletTown_ProfessorOaksLab_EventScript_WorldCircuitPassport")
    if national_dex_index == -1 or passport_index == -1:
        errors.append("Oak Lab must contain both National Dex and Passport scripts")
    elif passport_index > national_dex_index:
        errors.append("Passport script should be defined before the National Dex helper for readable postgame flow")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))
    region_progression = yaml.safe_load(read(REGION_PROGRESSION))

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    for event_id in (
        "oak_world_circuit_passport",
        "world_circuit_gate_johto_unlock",
        "lyra_profile_goes_live",
    ):
        if event_id not in act7.get("required_events", []):
            errors.append(f"Kanto act 7 missing event: {event_id}")

    message_by_id = {message.get("id"): message for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_WORLD_CIRCUIT_UNLOCKED",
        "WL_KANTO_LYRA_PROFILE_LIVE",
    ):
        if message_id not in message_by_id:
            errors.append(f"WorldLink messages missing id: {message_id}")

    unlock_text = message_by_id.get("WL_KANTO_WORLD_CIRCUIT_UNLOCKED", {}).get("text", "")
    for marker in ("World Circuit Passport", "Johto travel", "World Circuit Gate"):
        if marker not in unlock_text:
            errors.append(f"World Circuit unlock message missing marker: {marker}")

    lyra_text = message_by_id.get("WL_KANTO_LYRA_PROFILE_LIVE", {}).get("text", "")
    for marker in ("Lyra", "live", "New Bark"):
        if marker not in lyra_text:
            errors.append(f"Lyra live message missing marker: {marker}")

    band = rivals.get("progression_bands", {}).get("world_circuit_passport_unlock", {})
    if not band:
        errors.append("Rival progression missing world_circuit_passport_unlock band")
    else:
        companions = band.get("companions", {})
        rivals_data = band.get("rivals", {})
        if companions.get("red", {}).get("event") != "red_pallet_sendoff":
            errors.append("Passport band must include Red Pallet sendoff")
        if companions.get("misty", {}).get("event") != "misty_world_circuit_sendoff":
            errors.append("Passport band must include Misty sendoff")
        if companions.get("brock", {}).get("event") != "brock_world_circuit_sendoff":
            errors.append("Passport band must include Brock sendoff")
        if rivals_data.get("blue", {}).get("event") != "blue_after_champion_quiet_departure":
            errors.append("Passport band must include Blue quiet departure")
        if rivals_data.get("lyra", {}).get("event") != "lyra_profile_live_new_bark":
            errors.append("Passport band must make Lyra live for New Bark")

    johto = next(
        (
            region
            for region in region_progression.get("worldlink_region_progression", {}).get("unlock_order", [])
            if region.get("region") == "johto"
        ),
        {},
    )
    if johto.get("unlock_state") != "unlocked_after_kanto_passport":
        errors.append("Johto region progression must unlock after Kanto passport")
    for marker in ("World Circuit Gate", "New Bark Town", "committed departure"):
        if marker not in johto.get("entry_method", ""):
            errors.append(f"Johto entry method missing marker: {marker}")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0038-world-circuit-passport-johto-unlock.patch",
        "validate_world_circuit_passport_johto_unlock.py",
        "World Circuit Passport",
        "Lyra's profile is live",
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
        print("World Circuit Passport Johto unlock validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("World Circuit Passport Johto unlock validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
