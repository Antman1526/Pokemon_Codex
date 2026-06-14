# World Map Guide Ingestion

Date: 2026-06-13

Source file:

`/Users/Antman/Downloads/Pokémon World Map Guide_ All Regions & How to Visit Them.pdf`

The PDF contains nine pages covering Kanto through Paldea. It is useful as a high-level visual identity and landmark reference for the full Pokemon Nexus Red region order. It is not detailed enough to drive exact map tiles, warp layout, or route-by-route implementation.

Project data added:

- `data_design/world_map_guide_sources.yaml`

Design decisions from this source:

- Preserve the requested region order: Kanto, Johto, Hoenn, Sinnoh/Hisui, Unova, Kalos, Alola, Galar, Paldea.
- Treat Kanto as the playable foundation and Johto as the first true inter-region continuation.
- Use each region's visual identity as a pacing anchor: Kanto foundation, Johto history, Hoenn land/sea, Sinnoh myth, Unova urban systems, Kalos beauty/weaponry, Alola islands/wormholes, Galar spectacle/energy, Paldea open convergence.
- Use canonical decomp/game-map data for exact implementation details.
