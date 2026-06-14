# New Bark Arrival Map Design

## Decision

Create the first real Johto playable map as a compact New Bark arrival slice. This is not a region menu, debug jump, or fast-travel shortcut. It is the first committed step of the one-region-at-a-time WorldLink journey after Kanto.

## Player Experience

After the Pallet World Circuit Gate departure is confirmed, Antman warps into a playable New Bark staging map. Red arrives with Antman as the warm full-game friend, Lyra greets the party in person for the first time, and Elm opens the first Johto objective remotely. Hoenn remains locked.

## Implementation Shape

- Reuse the existing FireRed Pallet layout for the first playable New Bark stand-in.
- Use `REGION_JOHTO` on the map data so this is a real Johto map from the engine's perspective.
- Keep map-name popup disabled for this slice because custom Johto map sections are not implemented yet.
- Add Red, Lyra, and Elm signal NPC interactions.
- Advance WorldLink planning from `new_bark_worldlink_arrival` to `elm_lab_first_visit`.

## Scope Boundary

This slice proves the journey can leave Kanto and enter Johto in a buildable ROM. Elm Lab, Route 29, Cherrygrove, Johto map art, and Lyra's first battle are separate follow-up slices.
