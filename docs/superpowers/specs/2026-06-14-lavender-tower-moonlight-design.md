# Lavender Tower Moonlight Design

## Goal

Make Lavender Town and Pokemon Tower feel like the first emotional horror chapter of Pokemon Nexus Red while preserving the original Kanto story: Blue challenges Antman in the Tower, Cubone's mother is revealed as Marowak, Team Rocket is abusing Pokemon, and Mr. Fuji gives the Poke Flute. The new layer is Team Moonlight, whose name is revealed for the first time as a faction that studies grief, dreams, and WorldLink echoes.

## Proposed Direction

Proposed: Pokemon Tower should not become a full Team Moonlight dungeon yet. Rocket remains the visible villain and keeps the original Fuji rescue arc. Team Moonlight appears through a fractured "Moonlight Veil" signal in the protected 5F zone, through Marowak's dream static, and through Rocket grunts complaining that Moonlight is interfering with Rocket's operation.

This keeps the scene readable for first-time players and makes Moonlight feel uncanny instead of just another group of grunts.

## Story Beats

1. Blue keeps his classic 2F Tower rival battle, but his post-battle dialogue now lands harder because he jokes about Cubone and Marowak while WorldLink is reading grief static.
2. Red appears on 2F as Antman's warm full-game friend. Before Blue, he warns that the Tower is not a place to race. After Blue, he says the Tower reacted when Blue spoke about Cubone and Marowak.
3. On 5F, the purified zone includes a Moonlight Veil signal. Team Moonlight identifies itself by name and says it does not steal Pokemon; it opens the dreams they leave behind.
4. On 6F, Marowak's ghost remains the original Cubone's mother reveal, but the text adds a dream-static layer so the player understands Moonlight is listening to grief.
5. On 7F, Rocket grunts still guard Mr. Fuji. Their rewritten dialogue makes it clear Rocket and Moonlight are not allies.
6. Mr. Fuji warns Antman that Rocket hurts Pokemon directly, while Team Moonlight is more dangerous because it turns sorrow into a signal.
7. The Poke Flute reward remains the classic functional reward, now framed as a tool that wakes sleeping Pokemon, not dreams.

## System And Data Impact

- Add `patches/engine/0018-lavender-tower-moonlight.patch`.
- Add a Red object and dialogue to `PokemonTower_2F_Frlg`.
- Add a Moonlight signal object and dialogue to `PokemonTower_5F_Frlg`.
- Rewrite selected text in `PokemonTower_6F_Frlg`, `PokemonTower_7F_Frlg`, and `LavenderTown_VolunteerPokemonHouse_Frlg`.
- Update Kanto act data with Tower-specific required events.
- Add WorldLink messages for Blue's Tower pressure, Moonlight's name reveal, and Fuji's warning.
- Add a rival progression band for Pokemon Tower.
- Add validator coverage so the milestone is replayable and protected.

## Acceptance Criteria

- The patch chain can be replayed from a clean engine checkout.
- The ROM builds as `pokenexusred.gba` with title `NEXUS RED` and game code `BNRE`.
- The Tower 2F Red scene exists and reacts to Blue's battle state.
- Team Moonlight is named on 5F, but no Moonlight battle is introduced yet.
- Rocket dialogue on 7F explicitly separates Rocket's motives from Moonlight's.
- Mr. Fuji and Poke Flute text preserve the classic reward while adding the dream-static warning.
- Design validators include this milestone and pass.

## Deferred

- No custom Team Moonlight sprites yet.
- No Friends menu or companion rematch system yet.
- No full WorldLink feed UI yet; messages remain planning data and scripted dialogue.
- No new wild encounter tables in this slice.
