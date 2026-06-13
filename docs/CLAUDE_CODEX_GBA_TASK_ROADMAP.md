# Pokemon Nexus Red - Claude/Codex GBA Task Roadmap

Date: 2026-06-13
Purpose: turn the design into buildable tasks for Claude Code and Codex while preserving the `.gba`/OpenEmu target.

## Operating Rules

- Do not ask an agent to "build all 9 regions."
- Do not commit ROM files.
- Do not distribute `.gba` outputs.
- Build source and legal patch artifacts only.
- Each task must have a testable acceptance condition.
- Every milestone should produce a ROM that boots or a data/doc artifact that can be validated.

## Phase 0 - Repository and Engine Foundation

### Task 0.1 - Initialize Source Repo

Create the project repo layout:

```text
Pokemon_Codex/
  docs/
  data_design/
  tools/
  engine/
  patches/
  assets/
  build_notes/
```

Acceptance:

- directories exist,
- README explains legal ROM rule,
- `.gba`, `.sav`, `.srm`, `.ips`, `.bps` outputs are ignored unless explicitly intended for local release packaging.

### Task 0.2 - Choose and Build Engine

Use pokeemerald-expansion or the selected pokeemerald-based fork.

Acceptance:

- source builds locally,
- generated `.gba` boots in OpenEmu,
- save/load works,
- build steps documented in `build_notes/MAC_OPENEMU_BUILD_NOTES.md`.

### Task 0.3 - Feature Flag Audit

Map requested features to engine support.

Acceptance:

- `docs/ENGINE_FEATURE_AUDIT.md` lists each requested feature,
- each feature is marked existing, configurable, needs code, needs data, or deferred.

## Phase 1 - Data Design Foundation

### Task 1.1 - Region Chapter Data

Create `data_design/region_chapters.yaml`.

Acceptance:

- all 9 regions plus World Championship represented,
- each has arrival hub, major beats, villain focus, mechanic focus, unlock requirements, exit condition.

### Task 1.2 - Rival Data

Create `data_design/rivals.yaml`.

Acceptance:

- 10 rivals represented,
- each has personality, role, team archetype, relationship defaults, chapter appearances, notification behavior.

### Task 1.3 - Starter and Encounter Data

Create `data_design/starter_pools.yaml` and `data_design/early_encounter_policy.yaml`.

Acceptance:

- all 27 regional starters included,
- 12 special starters included,
- Route 1-3 encounter policy totals are valid,
- Dratini/Larvitar/Kubfu are flagged as balance-sensitive.

### Task 1.4 - Notification Templates

Create `data_design/worldlink_notifications.yaml`.

Acceptance:

- rival badge, capture, loss, win, region entry, request, villain alert, legendary anomaly, daycare update, swarm alert categories exist.

## Phase 2 - Kanto Vertical Slice

### Task 2.1 - Opening Flow

Modify New Game flow for Antman/Red-era start.

Acceptance:

- player begins in Pallet Town,
- Professor Oak introduces World Pokedex Initiative,
- Blue, Ava, and Dax are present,
- player receives WorldLink.

### Task 2.2 - 39 Starter Prototype

Implement a functional starter choice method.

Acceptance:

- player can choose any of the 39 starters,
- starter is added correctly,
- rival starter logic avoids duplicate softlocks,
- selected starter is recorded for later dialogue.

### Task 2.3 - Starting Convenience

Implement start-of-game resources.

Acceptance:

- player starts with $100,000,
- running enabled,
- bike or equivalent enabled,
- basic balls available,
- Infinite Repel toggle available or unlockable before Brock.

### Task 2.4 - First WorldLink Notifications

Implement minimal notification storage and display.

Acceptance:

- at least three messages can be queued,
- player can open WorldLink and read them,
- one rival capture notification triggers before Viridian,
- one rival badge/race notification triggers around Brock.

### Task 2.5 - Brock and Rocket Anomaly

Implement Pewter climax.

Acceptance:

- Brock has Standard and Hard team templates,
- level cap applies,
- first Rocket anomaly event triggers after Brock,
- event foreshadows Meridian Engine without naming Nexus Order.

## Phase 3 - Kanto Full Arc

Build full Kanto with Rocket, Moonlight, Gold Dust, and Phoenix foreshadowing.

Acceptance:

- all 8 Kanto badges obtainable,
- Silph Co. Rocket climax works,
- Lavender Moonlight event works,
- Celadon Gold Dust event works,
- Cinnabar Phoenix event works,
- Indigo League works,
- Johto unlock flag is set.

## Phase 4 - Systems Before More Regions

Do not add Johto before these systems are stable:

- region unlock table,
- transport hub,
- rematch board,
- expanded Pokecenter terminal,
- level cap settings,
- starter/encounter data validators,
- save/load regression test,
- OpenEmu smoke test.

## Phase 5 - Region Chapter Expansion

Add one region at a time in this order:

1. Johto
2. Hoenn
3. Sinnoh/Hisui
4. Unova
5. Kalos
6. Alola
7. Galar
8. Paldea
9. World Nexus Championship

Rule: each region must be playable, testable, and shippable before the next begins.

## Phase 6 - OpenEmu Release Candidate

Acceptance:

- game boots in OpenEmu,
- new game works,
- save/load works,
- no copyrighted ROM committed,
- patch generation documented,
- known issues listed,
- at least one 30-minute no-crash route test passes.

