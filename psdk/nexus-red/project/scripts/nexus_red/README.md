# Nexus Red PSDK Scripts

This folder contains custom Ruby scaffolding for the primary Pokemon Studio / PSDK build.

Current entrypoint:

- `000_seed_loader.rb` loads the generated PSDK seed registries from `Data/nexus_red_seed/generated/`.

Runtime services:

- `runtime/seed_data.rb` reads generated registries.
- `runtime/runtime_state.rb` builds the Nexus Red save-state scaffold.
- `runtime/world_link.rb` handles live, paused, and digest notifications.
- `runtime/*_progress.rb` and other service files track starter selection, early migration encounters, rivals, companions, factions, regions, gameplay options, field tools, Pokédex readiness, Center/Mart services, encounter-world state, and battle mechanics gating.

Route 1-3 migration map events should call `NexusRed::EarlyMigrationEncounters.prepare_map_event_encounter(state, route_id, time:, max_level:)`. The method returns a PSDK-friendly encounter payload, records the species as seen in the Pokédex, and skips species already caught by the player.

Route 1 can use `NexusRed::Route1MigrationEvent.trigger(state, time:, max_level:)` as its first concrete adapter. It stores a pending wild-migration battle request through `NexusRed::MapEventBridge.pending_battle_request(state)`; the later PSDK map command should consume that request and hand its species key and level to the final wild battle launcher.

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
