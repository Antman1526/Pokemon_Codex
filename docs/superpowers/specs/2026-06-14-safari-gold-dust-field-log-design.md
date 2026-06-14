# Safari Gold Dust Field Log Design Spec

## Goal

Make Fuchsia's Safari Zone feel like a major Kanto exploration chapter instead of a side minigame: Ava introduces a WorldLink Safari Field Log checklist, Gold Dust starts probing rare habitats, and Koga is framed as the next battle lesson in poison, status control, and patience before Saffron/Silph Co.

## Player Experience

- Antman reaches the Safari Zone entrance after Route 12 opens the Fuchsia path.
- Ava appears inside the Safari entrance as the research rival who understands rare habitats better than the battle-focused rivals.
- Ava gives a lightweight checklist-style briefing: log rare habitats, look for the Warden's prize route, watch for Gold Dust collectors, and prepare status answers for Koga.
- A well-dressed Gold Dust scout appears in the Safari office pretending to be a collector. He does not battle yet; he makes it clear Gold Dust values rare Pokemon, preserve maps, and pedigree records.
- Existing Safari play remains classic: payment, Safari Balls, timer/steps, and exit behavior are unchanged.
- The Safari office text now makes the Warden's prize and far-corner objective feel like part of Nexus Red's long-route checklist, not just a hidden HM callback.

## Required Story Markers

- `safari_field_log_checklist`
- `ava_safari_research_scene`
- `gold_dust_safari_scout`
- `warden_prize_route_tease`
- `koga_status_preparation`
- `saffron_after_safari_pressure`

## Required WorldLink Markers

- `WL_KANTO_SAFARI_FIELD_LOG`
- `WL_KANTO_GOLD_DUST_SAFARI_SCOUT`
- `WL_KANTO_KOGA_STATUS_PREP`

## Required Rival/Companion Markers

- `safari_gold_dust_field_log`
- `ava_safari_field_log`
- `dax_safari_competition`
- `blue_saffron_loss_rumor`
- `red_misty_fuchsia_check`

## Scope Boundary

This slice does not change Safari encounter tables, add a new UI checklist, rebalance Koga, or implement the full Surf/Tide Rider reward. It makes the existing Safari entrance and office carry the next story/QoL layer while preserving stable mechanics.
