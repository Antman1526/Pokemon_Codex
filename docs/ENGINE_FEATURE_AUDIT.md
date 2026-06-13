# Pokemon Nexus Red - Engine Feature Audit

Date: 2026-06-13
Purpose: map the desired design to likely pokeemerald-expansion support and project-specific work.

Status labels:

- likely_existing: expected to be present in pokeemerald-expansion or common decomp infrastructure.
- configure_or_integrate: likely available but needs config/data/content work.
- project_code_needed: custom Pokemon Nexus Red system.
- content_heavy: mostly asset/map/script/data volume.
- defer_or_phase: possible, but should not block the first playable `.gba`.

## 1. Battle and Pokemon Mechanics

| Feature | Status | Notes |
| --- | --- | --- |
| Physical/Special split | likely_existing | Treat as baseline engine requirement. Confirm in engine config. |
| Fairy type | likely_existing | Confirm type table, icons, and move data. |
| Gen 9 species/moves/abilities | configure_or_integrate | Expansion is the right family of engine; exact coverage must be audited after clone. |
| Expanded reusable TMs | configure_or_integrate | Needs TM list, mart unlocks, compatibility review. |
| Ability Capsule | configure_or_integrate | Needs item availability and UI behavior review. |
| Ability Patch | configure_or_integrate | Recommended alongside Capsule. |
| Modern held items | configure_or_integrate | Must be balanced by badge/region. |
| Strong battle AI | configure_or_integrate | Boss tiers need AI profile rules. |
| Mega Evolution | configure_or_integrate | Full unlock in Kalos; preview only before then. |
| Z-Moves | configure_or_integrate | Restrict to Alola and postgame facilities. |
| Dynamax/Gigantamax | configure_or_integrate | No player use in Kanto/Johto/Hoenn; controlled access can unlock after Hoenn, with Galar as full story home. |
| Terastallization | configure_or_integrate | No player use in Kanto/Johto/Hoenn; controlled access can unlock after Hoenn, with Paldea as full story home. |

## 2. Player QoL

| Feature | Status | Notes |
| --- | --- | --- |
| Infinite Repel | project_code_needed | May adapt existing repel logic; WorldLink toggle is custom. |
| Portable PC | configure_or_integrate | Debug PC features may exist; player-facing item needs design. |
| Portable healing | project_code_needed | Must be difficulty-gated to avoid killing attrition. |
| Skip text | configure_or_integrate | Confirm engine options. |
| Fast-forward | defer_or_phase | Emulator fast-forward exists; in-ROM battle/text speed is safer. |
| Running from start | configure_or_integrate | Simple new-game flag. |
| Bike from start | configure_or_integrate | Simple key item/event change. |
| Start with $100,000 | configure_or_integrate | New-game money constant/event. |
| Rare Candies in marts | configure_or_integrate | Needs mart data and level caps. |
| Trade evolution removal | configure_or_integrate | Use Link Cable item or level/item edits. |

## 3. Challenge and Difficulty

| Feature | Status | Notes |
| --- | --- | --- |
| Level caps | configure_or_integrate | Must support off/soft/hard/Nuzlocke. |
| Nuzlocke tools | project_code_needed | Some parts may exist, but integrated rules/UI are project-specific. |
| No in-battle items mode | configure_or_integrate | Difficulty setting and battle item checks. |
| Set/Switch mode options | likely_existing | Expose in difficulty preset. |
| Gym rematches | project_code_needed | Data-driven rematch board recommended. |
| Trainer rematches | configure_or_integrate | VS Seeker-style or terminal-based. |
| Boss AI tiers | configure_or_integrate | Design boss templates by mode. |

## 4. World Systems

| Feature | Status | Notes |
| --- | --- | --- |
| Day/night | configure_or_integrate | Prefer in-game clock for OpenEmu stability. |
| Weather | configure_or_integrate | Needs route tables, story weather, and battle weather rules. |
| Daycare/breeding | likely_existing | Needs remote status through Pokecenter/WorldLink. |
| Expanded Pokedex | configure_or_integrate | Requires habitat/evolution/location extensions. |
| All Pokemon catchable | content_heavy | Requires encounter, gift, fossil, event, swarm, postgame policy. |
| Overworld Pokemon | defer_or_phase | Use in showcase zones first. |
| Following Pokemon | defer_or_phase | Start with starters/favorites; full coverage is asset-heavy. |
| Fishing tiers | project_code_needed | Old/Good/Super/Mythic rod tables and chain logic. |
| Expanded Dig | project_code_needed | Mining, fossils, tunnels, hidden encounters. |
| Expanded Fly | project_code_needed | Region transit and emergency travel. |
| HM replacement | project_code_needed | Key item flags and map gate conversion. |

## 5. Pokemon Nexus Red Custom Systems

| Feature | Status | Notes |
| --- | --- | --- |
| 39 starter selection | project_code_needed | Multi-page menu or staged lab selection. |
| WorldLink notifications | project_code_needed | Core signature system. |
| 10 rival state model | project_code_needed | Store progress IDs, not full simulation. |
| Rival dynamic city encounters | project_code_needed | Hybrid scripted/simulated map appearances. |
| Region unlock table | project_code_needed | Controls World Circuit progression. |
| Transport hub | project_code_needed | Ferry/train/fly/wormhole/academy gates. |
| Nexus Order meta-plot flags | project_code_needed | Story state spine. |
| Expanded Pokecenter services | project_code_needed | Nurse Joy plus terminal systems. |
| Multi-region mart economy | project_code_needed | Badge/region-tiered inventory. |
| Team Phoenix/Moonlight/Gold Dust | content_heavy | New scripts, trainers, maps, music, sprites if custom. |

## 6. First Clone Audit Checklist

After the engine is cloned, inspect:

- `include/config/` for battle, overworld, item, and QoL flags.
- species data for Gen 9 coverage.
- move data for Gen 9 coverage.
- ability data for Gen 9 coverage.
- item data for Ability Capsule/Patch, mints, Bottle Caps.
- battle AI config/code.
- follower Pokemon implementation status.
- day/night and time systems.
- weather systems.
- map scripting conventions.
- save block capacity and custom save fields.
- debug menu availability.

## 7. First Engineering Recommendation

Build the Kanto vertical slice with only these custom systems first:

1. starter selection,
2. starting convenience flags,
3. three-rival opening,
4. WorldLink prototype,
5. route encounter edits,
6. Brock level cap,
7. first Rocket anomaly event.

Everything else should be data-designed now but implemented after the vertical slice proves the `.gba` is stable in OpenEmu.

## 8. FireRed-First Visual Requirement

The recommended technical base remains pokeemerald-expansion, but the player-facing direction is FireRed-first.

Audit after engine clone:

- which tilesets can be replaced safely,
- where title screen graphics are defined,
- menu frame and font options,
- overworld sprite dimensions,
- palette constraints,
- FireRed-style Kanto tileset compatibility,
- whether FireRed-inspired UI work conflicts with existing expansion UI features.
