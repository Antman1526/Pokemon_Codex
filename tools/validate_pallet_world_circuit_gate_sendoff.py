#!/usr/bin/env python3
"""Validate the Pallet World Circuit Gate sendoff slice."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0039-pallet-world-circuit-gate-sendoff.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-pallet-world-circuit-gate-sendoff-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-pallet-world-circuit-gate-sendoff.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
REGION_PROGRESSION = ROOT / "data_design" / "worldlink_region_progression.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0039-pallet-world-circuit-gate-sendoff.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0039-pallet-world-circuit-gate-sendoff.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "FLAG_HIDE_WORLD_CIRCUIT_GATE_COMPANIONS",
            "FLAG_USED_WORLD_CIRCUIT_GATE_SENDOFF",
            "PalletTown_EventScript_RedWorldCircuitGate",
            "World Circuit Gate",
            "LYRA: New Bark Town signal stable",
        ):
            if marker not in patch:
                errors.append(f"patch 0039 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Pallet World Circuit Gate sendoff spec",
            ("committed departure", "no direct Johto warp", "Red, Misty, Brock, and Blue"),
        ),
        (
            PLAN,
            "Pallet World Circuit Gate sendoff plan",
            ("Add a failing validator", "Patch Pallet Town", "Build the ROM"),
        ),
    ):
        if not doc_path.exists():
            errors.append(f"missing {doc_name}")
            continue
        doc = read(doc_path)
        for marker in markers:
            if marker not in doc:
                errors.append(f"{doc_name} missing marker: {marker}")
    return errors


def validate_engine_flags_and_map() -> list[str]:
    errors: list[str] = []
    flags = read(ENGINE / "include" / "constants" / "flags_frlg.h")
    scripts = read(ENGINE / "data" / "maps" / "PalletTown_Frlg" / "scripts.inc")
    pallet = load_map("PalletTown_Frlg")

    for marker in (
        "#define FLAG_HIDE_WORLD_CIRCUIT_GATE_COMPANIONS 0x021",
        "#define FLAG_USED_WORLD_CIRCUIT_GATE_SENDOFF    0x022",
    ):
        if marker not in flags:
            errors.append(f"flags_frlg.h missing marker: {marker}")

    expected_objects = {
        "OBJ_EVENT_GFX_RED": "PalletTown_EventScript_RedWorldCircuitGate",
        "OBJ_EVENT_GFX_MISTY": "PalletTown_EventScript_MistyWorldCircuitGate",
        "OBJ_EVENT_GFX_BROCK": "PalletTown_EventScript_BrockWorldCircuitGate",
        "OBJ_EVENT_GFX_BLUE": "PalletTown_EventScript_BlueWorldCircuitGate",
    }
    for gfx, script in expected_objects.items():
        if not any(
            obj.get("graphics_id") == gfx
            and obj.get("script") == script
            and obj.get("flag") == "FLAG_HIDE_WORLD_CIRCUIT_GATE_COMPANIONS"
            for obj in pallet.get("object_events", [])
        ):
            errors.append(f"Pallet map missing companion object {gfx} -> {script}")

    for marker in (
        "PalletTown_EventScript_UpdateWorldCircuitGateCompanions",
        "goto_if_set FLAG_RECEIVED_WORLD_CIRCUIT_PASSPORT",
        "setflag FLAG_HIDE_WORLD_CIRCUIT_GATE_COMPANIONS",
        "clearflag FLAG_HIDE_WORLD_CIRCUIT_GATE_COMPANIONS",
        "PalletTown_EventScript_RedWorldCircuitGate",
        "goto_if_set FLAG_USED_WORLD_CIRCUIT_GATE_SENDOFF",
        "setflag FLAG_USED_WORLD_CIRCUIT_GATE_SENDOFF",
        "World Circuit Gate",
        "RED: This is the first road",
        "MISTY: The sea route is quiet",
        "BROCK: I packed extra supplies",
        "{RIVAL}: Do not make Johto think",
        "LYRA: New Bark Town signal stable",
        "No direct Johto warp yet",
    ):
        if marker not in scripts:
            errors.append(f"Pallet scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))
    regions = yaml.safe_load(read(REGION_PROGRESSION))

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    for event_id in (
        "pallet_world_circuit_gate_sendoff",
        "red_misty_brock_blue_departure_scene",
        "new_bark_signal_stable_no_warp",
    ):
        if event_id not in act7.get("required_events", []):
            errors.append(f"Kanto act 7 missing event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_PALLET_GATE_SENDOFF",
        "WL_KANTO_NEW_BARK_SIGNAL_STABLE",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    band = rivals.get("progression_bands", {}).get("pallet_world_circuit_gate_sendoff", {})
    for companion in ("red", "misty", "brock"):
        if companion not in band.get("companions", {}):
            errors.append(f"Rival progression missing companion at gate: {companion}")
    if band.get("rivals", {}).get("blue", {}).get("event") != "quiet_johto_departure_pressure":
        errors.append("Rival progression must give Blue quiet Johto departure pressure")
    if "lyra" not in band.get("rivals", {}):
        errors.append("Rival progression must keep Lyra live from New Bark")

    johto = next(
        (entry for entry in regions.get("worldlink_region_progression", {}).get("unlock_order", []) if entry.get("region") == "johto"),
        {},
    )
    if johto.get("unlock_state") != "unlocked_after_kanto_passport":
        errors.append("Johto must remain unlocked_after_kanto_passport")
    if "Pallet World Circuit Gate" not in johto.get("entry_method", ""):
        errors.append("Johto entry method must mention Pallet World Circuit Gate")
    if "no direct Johto warp" not in regions.get("worldlink_region_progression", {}).get("travel_feel", ""):
        errors.append("Region progression travel feel must explicitly say no direct Johto warp in this slice")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0039-pallet-world-circuit-gate-sendoff.patch",
        "validate_pallet_world_circuit_gate_sendoff.py",
        "Pallet World Circuit Gate sendoff",
    ):
        if marker not in notes:
            errors.append(f"Build notes missing marker: {marker}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_docs())
    errors.extend(validate_engine_flags_and_map())
    errors.extend(validate_design_data())
    errors.extend(validate_build_notes())

    if errors:
        print("Pallet World Circuit Gate sendoff validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Pallet World Circuit Gate sendoff validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
