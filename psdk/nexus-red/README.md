# Pokemon Nexus Red PSDK Project

This directory is reserved for the primary Pokemon Studio / PSDK implementation of `POKEMON NEXUS RED`.

Status: setup scaffold only. Do not vendor PSDK binaries, generated caches, commercial ROM assets, ripped graphics/audio, or large local export artifacts here.

## Intended Layout

```text
psdk/nexus-red/
  project/
    Data/
      nexus_red_seed/
    Graphics/
    Audio/
    scripts/
    maps/
  docs/
    content-migration/
    studio-data-notes/
```

## First Setup Goals

- Install/open Pokemon Studio on macOS.
- Create or open a blank PSDK project.
- Identify the source-of-truth project files Studio expects.
- Decide which generated files must be ignored.
- Map the existing Godot prototype data into PSDK concepts before importing content.
- Generate the PSDK seed files with `python3 tools/generate_psdk_seed_data.py`.

## Migration Source Material

- Godot reference prototype: `native/nexus-red/`
- Main design framework: `docs/POKEMON_NEXUS_RED_FRAMEWORK.md`
- PSDK primary strategy: `docs/PSDK_NATIVE_BUILD_STRATEGY.md`
- PC/Mac strategy: `docs/PC_MAC_NATIVE_BUILD_STRATEGY.md`

## Local Setup Evidence

- Setup audit: `docs/psdk/PSDK_SETUP_AUDIT_2026-06-15.md`
- Kanto migration map: `psdk/nexus-red/docs/content-migration/KANTO_VERTICAL_SLICE_MAPPING.md`
- Starter and early-route import contract: `psdk/nexus-red/docs/studio-data-notes/STARTER_AND_EARLY_ROUTE_IMPORT_CONTRACT.md`
- PSDK import seed manifest: `psdk/nexus-red/project/Data/nexus_red_seed/import_manifest.json`
- Generated seed data: `psdk/nexus-red/project/Data/nexus_red_seed/generated/`
- Ignore guardrails: `psdk/nexus-red/.gitignore`

## Seed Data Commands

```bash
python3 tools/generate_psdk_seed_data.py
python3 tools/generate_psdk_seed_data.py --check
python3 tools/validate_psdk_seed_manifest.py
```
