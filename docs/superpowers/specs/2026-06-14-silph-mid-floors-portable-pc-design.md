# Silph Mid-Floors and Portable PC Design

## Intent

This slice turns Silph 4F-7F from a long office maze into the middle act of the Saffron rescue. Antman is no longer only climbing toward Giovanni: he is learning how Rocket controls infrastructure, how Gold Dust profits without standing in the room, how Red keeps civilians moving offscreen, and why Blue's rivalry cracks under real crisis pressure.

## Story Beats

- Silph 4F shows a Gold Dust terminal trace. Gold Dust is not occupying Silph directly; they are trying to buy output from Rocket-controlled systems.
- Silph 5F upgrades the Rocket Hideout beta into Portable PC full access through a stable Silph field terminal. The terminal opens the real PC script, making this a functional QoL payoff.
- Silph 6F frames Red as the warm full-game companion who is actively routing civilians and asking Antman to keep pushing upward.
- Silph 7F keeps the classic Blue battle but changes the emotional read: Blue is scared, angry, and trying to prove he still belongs in the same story as Antman and Red. Blue is not comic relief here.
- WorldLink logs the mid-floor checklist, Portable PC full access, and Blue's rivalry pressure without unlocking another region.

## Implementation Shape

- Add design markers to `data_design/kanto_chapter.yaml` under `act_5_saffron_fuchsia`.
- Add WorldLink messages for Silph 4F-7F, Portable PC full access, and Blue's Silph pressure scene.
- Add rival/companion progression for Red, Misty, Brock, Blue, Ava, and Dax around the middle floors.
- Add a Silph 5F clipboard object using `SilphCo_5F_EventScript_PortablePcFullAccess`, which jumps to `EventScript_PC` after text.
- Export `patches/engine/0027-silph-mid-floors-portable-pc.patch` scoped to Silph 4F-7F only.

## Scope Choice

Portable PC full access means stable PC access from a Silph field terminal in this slice. A Start-menu/key-item Portable PC is a later engine feature because it touches menu state, item registration, and field-use restrictions. This keeps the first build playable and still pays off the promise with real storage access.

## Verification

- `tools/validate_silph_mid_floors_portable_pc.py` must verify design data, build notes, and patch markers.
- Full validator suite must pass after replaying patches from a clean engine checkout.
- ROM must build as a `.gba` with title `NEXUS RED` and game code `BNRE`.
