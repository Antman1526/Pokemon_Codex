# Pokemon Nexus Red - Nexus Identity, WorldLink, and Starter Expansion Design

Date: 2026-06-13
Status: approved direction, pending implementation plan

## 1. Purpose

This spec defines the next playable milestone after the first OpenEmu-confirmed build. The milestone gives Pokemon Nexus Red a clearer identity, proves the first WorldLink alert in-game, expands Oak's starter selection to the 27 official regional starters, and makes the remaining early special Pokemon catchable across Routes 1-3 without breaking progression.

## 2. Approved Creative Direction

The title-screen concept is Red, Antman, and Blue facing a glowing region-map Nexus. The logo text is `POKEMON NEXUS RED`. The tone is warm adventure: Pallet Town should feel like the beginning of a huge friendly journey, with mystery in the sky rather than a dark apocalypse.

First implementation may use GBA-safe temporary title identity work if the full asset pipeline is too risky for this milestone. The priority is to stop the build from feeling generic while preserving OpenEmu stability. Full pixel-art title replacement belongs in the next graphics-focused milestone after this one proves the insertion path.

## 3. Title Identity Scope

The milestone should prepare the title screen around the approved concept:

- Foreground story image: Red, Antman, and Blue face away from camera toward the Nexus.
- Nexus image: a glowing world-map ring that hints at all nine regions.
- Logo text: `POKEMON NEXUS RED`.
- Mood: sunrise, warm color, classic adventure energy.

Implementation rule: do not risk the ROM by forcing full custom title art before the asset format is understood. If the first engine patch can only safely preserve the FireRed title art while maintaining `NEXUS RED` header and documenting the replacement path, that is acceptable for this milestone.

## 4. WorldLink Prototype

WorldLink should first appear as a Pokédex-style alert after the Oak lab flow is established. It should feel like the World Pokédex Initiative is waking up, not like a modern phone.

Recommended first alert:

```text
WORLDLINK ALERT
RED logged fresh tracks on ROUTE 1.
BLUE marked himself "first to VIRIDIAN."
```

Design intent:

- Red feels helpful and observant.
- Blue turns the same discovery into a race.
- The alert proves that companions and rivals can update the player outside direct dialogue.
- The implementation can be a scripted message box first; a full notification feed belongs in a separate WorldLink-feed milestone.

WorldLink pause rules from the previous spec still apply. Future notifications pause in caves, dungeons, gyms, starter selection, boss events, and major cutscenes. This first alert should not fire inside those contexts.

## 5. Oak Starter Expansion

Oak's selection expands to all 27 official regional starters immediately.

Starter set:

- Kanto: Bulbasaur, Charmander, Squirtle
- Johto: Chikorita, Cyndaquil, Totodile
- Hoenn: Treecko, Torchic, Mudkip
- Sinnoh: Turtwig, Chimchar, Piplup
- Unova: Snivy, Tepig, Oshawott
- Kalos: Chespin, Fennekin, Froakie
- Alola: Rowlet, Litten, Popplio
- Galar: Grookey, Scorbunny, Sobble
- Paldea: Sprigatito, Fuecoco, Quaxly

Recommended UI:

1. Choose a region category.
2. Choose one of that region's three starters.
3. Confirm: `Begin with {species}?`
4. Give the starter at level 5.
5. Set starter metadata for future rival, WorldLink, and companion dialogue.

Do not add the 12 special starters to Oak's selection in this milestone. They should be catchable on Routes 1-3 first. Adding special Oak pages is a separate milestone after the 27-starter menu and Blue counter-pick behavior are stable.

## 6. Route 1-3 Catchable Expansion

All 27 official starters and the 12 special early Pokemon should be catchable by the end of Route 3, but their levels, rarity, and encounter timing must track game progression.

Special early Pokemon:

- Eevee
- Pikachu
- Dratini
- Abra
- Gastly
- Larvitar
- Sandile
- Kubfu
- Staryu
- Shroomish
- Rockruff
- Ralts

Progression rule:

- Route 1 should feel generous but not chaotic. Use low-level, safe early encounters.
- Route 2 can introduce trickier species and first rare finds.
- Route 3 can introduce rarer, stronger, or slower-growth Pokemon at controlled low levels.
- High-power species such as Dratini, Larvitar, and Kubfu must be rare and low-level, with move sets that do not trivialize Brock or early Rocket fights.
- Encounter levels should sit near the local trainer curve and below the next major boss cap.

Recommended distribution:

- Route 1: Kanto starters, Pikachu, Eevee, Ralts.
- Route 2: Johto, Hoenn, and Sinnoh starters, plus Abra, Gastly, Shroomish.
- Route 3: Unova, Kalos, Alola, Galar, and Paldea starters, plus Dratini, Larvitar, Sandile, Rockruff, Staryu, Kubfu.

## 7. Progression Scaling Rule

Wild Pokemon, trainer teams, rival teams, gym leaders, and Rocket encounters must scale together.

Implementation requirements:

- Wild encounter levels must remain in range for the current route.
- Trainers should not use evolved or high-BST teams before the player has reasonable access to counters.
- Gym leaders should remain mainline-hard with optional difficulty scaling, not Radical Red-punishing by default.
- Brock's first battle should account for the expanded starter pool and Route 1-3 catches.
- Blue's team should respond to the player's starter without hard-countering rare or advanced choices too aggressively.
- Rare early Pokemon can be exciting, but their learnsets, catch rates, and levels must prevent them from invalidating early progression.

Balance principle: the player may catch powerful Pokemon early, but the game should keep them interesting through level caps, learnset pacing, boss design, and trainer variety.

## 8. Implementation Boundaries

Use project-owned patch files for engine changes. Do not commit local-only submodule source edits or generated `.gba` files.

Expected patch separation:

- Title identity patch: title/header or documented title asset pipeline.
- WorldLink prototype patch: scripted Pokédex-style alert.
- Starter selection patch: 27 official starters in Oak's selection.
- Route 1-3 encounter patch: progression-scaled wild availability.
- Balance data patch: trainer/gym notes or data needed to keep levels coherent.

Each patch must build independently when applied in order after the existing first-playable patches.

## 9. Acceptance Criteria

The milestone is acceptable when:

- `pokenexusred.gba` builds with title/header identity intact.
- OpenEmu opens the ROM.
- The player can start a new game and reach Pallet bedroom.
- Oak can offer all 27 official starters.
- The selected starter is level 5 and usable in battle.
- Blue's first battle still starts and completes.
- Routes 1-3 contain the expanded early Pokemon pool with badge-scaled levels and rarity.
- The first WorldLink alert appears as a Pokédex-style story message.
- Brock and early trainers remain fair with the expanded player options.
- `python3 tools/validate_design_data.py` passes.

## 10. Open Questions For Later

- Whether the 12 special starters should also become Oak-selectable after the 27-starter system is stable.
- Whether WorldLink becomes a real menu/feed in the Pokédex or remains scripted story alerts until Viridian/Cerulean.
- Whether custom title pixel art should be generated first as concept art or hand-authored directly into GBA tile/palette constraints.

## 11. Self-Review

- This spec has no unresolved requirements.
- The title art scope is intentionally phased to avoid blocking the playable ROM.
- The user's progression concern is explicit: wild Pokemon, trainers, gym leaders, and rivals must scale together.
- The milestone is still large, so the implementation plan must split it into separately buildable patches with verification after each patch.
