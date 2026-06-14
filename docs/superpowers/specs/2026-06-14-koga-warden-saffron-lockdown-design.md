# Koga Warden Notes and Saffron Lockdown Design

## Intent

This slice turns Fuchsia from a side route into the required preparation arc before Saffron. The player clears the Safari Field Log pressure, faces Koga as the first serious status-control Gym Leader, learns that Gold Dust copied the Warden's rare-habitat notes, and receives a WorldLink handoff toward Saffron/Silph Co.

## Story Beats

- Koga frames the Soul Badge as proof that Antman can fight through attrition, not just raw type advantage.
- Koga confirms that Gold Dust collectors are copying Safari route notes and selling the data to anyone who can weaponize rare Pokemon access.
- The Warden's house preserves the classic Gold Teeth and HM04 flow, but his restored dialogue now mentions the stolen habitat notebook and the need to protect the preserve.
- Saffron Rocket lockdown dialogue escalates after the Fuchsia arc: Rocket wants Silph systems, Gold Dust wants rare-habitat markets, and Blue has already bounced off the security line.
- WorldLink updates the checklist after the Soul Badge: Saffron is still Kanto-only progress, not a region jump.

## Implementation Shape

- Add design markers to `data_design/kanto_chapter.yaml` under `act_5_saffron_fuchsia`.
- Add WorldLink message ids for Koga status clear, Warden notes theft, and Saffron lockdown handoff.
- Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax around the Soul Badge handoff.
- Export one engine patch, `0025-koga-warden-saffron-lockdown.patch`, scoped to Fuchsia Gym, Warden's House, and Saffron City scripts.
- Keep battle mechanics stable for this slice; trainer-party/stat edits are deferred until the dedicated difficulty tuning pass.

## Verification

- `tools/validate_koga_warden_saffron_lockdown.py` must verify design data, build notes, and the engine patch markers.
- Full validator suite must pass after replaying patches from a clean engine checkout.
- ROM must build as a `.gba` with title `NEXUS RED` and game code `BNRE` for OpenEmu.
