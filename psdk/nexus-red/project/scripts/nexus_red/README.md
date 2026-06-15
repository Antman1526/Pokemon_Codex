# Nexus Red PSDK Scripts

This folder contains custom Ruby scaffolding for the primary Pokemon Studio / PSDK build.

Current entrypoint:

- `000_seed_loader.rb` loads the generated PSDK seed registries from `Data/nexus_red_seed/generated/`.

Runtime services:

- `runtime/seed_data.rb` reads generated registries.
- `runtime/runtime_state.rb` builds the Nexus Red save-state scaffold.
- `runtime/world_link.rb` handles live, paused, and digest notifications.
- `runtime/*_progress.rb` and other service files track rivals, companions, factions, regions, gameplay options, field tools, Pokédex readiness, Center/Mart services, encounter-world state, and battle mechanics gating.

The loader is intentionally conservative. It only reads committed JSON seed files and prepares a guarded `PFM::GameState` extension when PSDK is available. Map events, battles, Pokemon creation, and UI calls should be added in later scripts after the blank PSDK project structure is confirmed in Pokemon Studio.

Seed refresh command:

```bash
python3 tools/generate_psdk_seed_data.py
```

Validation:

```bash
python3 tools/validate_psdk_ruby_scaffold.py
```

That validation includes Ruby syntax checks for the entrypoint and runtime files, plus a runtime smoke check that requires `000_seed_loader.rb` from the PSDK project root and reads every generated registry.
