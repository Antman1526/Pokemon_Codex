# Pokemon Nexus Red - Kanto Vertical Slice Spec

Date: 2026-06-13
Milestone: first playable `.gba` target for OpenEmu
Scope: Pallet Town through Boulder Badge

## 1. Player Promise

The first playable build should prove the fantasy immediately: this begins like Pokemon Red, but the world is bigger, stranger, and more alive. Within the first hour, the player should choose from the full starter concept, meet three rivals, receive WorldLink updates, catch unusual Pokemon on early routes, battle Brock under a level cap, and see the first sign that Team Rocket is involved in something global.

## 2. Playable Map Scope

Required:

- Pallet Town
- Professor Oak's Lab
- Route 1
- Viridian City
- Viridian Pokecenter and Mart
- Route 2
- Viridian Forest
- Pewter City
- Pewter Pokecenter and Mart
- Pewter Gym
- short post-Brock Rocket anomaly scene

Optional if time allows:

- Route 22 rival battle pocket
- Museum lobby with Phoenix fossil foreshadowing
- closed Route 3 gate with Kubfu monastery rumor

## 3. Opening Flow

1. Player wakes in Pallet Town.
2. Mom mentions Oak called about the World Pokedex Initiative.
3. Outside, Red is watching the Pallet grass line and quietly points out unfamiliar Pokemon tracks.
4. Blue blocks the player and says Oak is waiting.
5. Ava arrives with field notes about "wrong-region Pokemon" near Route 1.
6. Dax arrives late, already talking about beating Brock first.
7. Oak explains that Kanto's first routes are showing impossible migration.
8. Player chooses starter from the full 39-choice system.
9. Blue receives a counter-pick.
10. Ava receives a research-oriented starter.
11. Dax receives an offense-oriented starter.
12. First rival battle occurs against Blue.
13. Red briefly joins the walk to Route 1 or gives the player a quiet warning before leaving.
14. Oak gives WorldLink.
15. WorldLink immediately logs the first cohort status update.

## 4. Starter Selection MVP

The perfect final UI can wait. The MVP must be reliable and must include all 39 choices.

Required first implementation:

- region category menu,
- then starter choice menu,
- four Special category pages for the 12 extra starters.

Categories:

- Kanto
- Johto
- Hoenn
- Sinnoh
- Unova
- Kalos
- Alola
- Galar
- Paldea
- Special A
- Special B
- Special C
- Special D

Special starters:

- Special A: Eevee, Pikachu, Ralts
- Special B: Abra, Gastly, Staryu
- Special C: Shroomish, Rockruff, Sandile
- Special D: Dratini, Larvitar, Kubfu

Rules:

- Starter must be level 5.
- Starter must have legal early moves.
- Starter should receive a project origin flag for later dialogue.
- Blue, Ava, and Dax should receive non-duplicate starters through deterministic assignment rules.
- Kubfu is allowed as a starter because the player explicitly requested it, but wild Kubfu should be event-gated.

## 5. Rival Opening Behavior

### Blue

Role: classic rival.
First battle: mandatory lab battle.
Tone: "This world tour thing is just a bigger stage for me to beat you on."

### Ava

Role: friendly researcher.
First battle: optional Route 1 tutorial-style battle or no battle until Viridian.
Tone: "If these Pokemon are appearing here, something is pulling them."

### Dax

Role: aggressive battler.
First battle: early Route 1/Route 2 challenge.
Tone: "Badges do not wait. Brock is the first checkpoint."

## 6. WorldLink MVP

WorldLink must support:

- queue message,
- display message list,
- mark read,
- trigger message by story flag.

Minimum messages:

1. After leaving Oak's Lab:
   - "WorldLink initialized. Cohort trainers registered: Blue, Ava, Dax."
2. On Route 1:
   - "Ava spotted a Johto starter near Route 1. Oak wants habitat notes."
3. On Viridian entry:
   - "Dax challenged a Bug Catcher near Viridian Forest and is heading for Pewter."
4. After Brock:
   - "WorldLink Alert: Rocket activity detected near the museum service tunnel."

## 7. Route Encounter Philosophy

The first routes should feel exciting but not chaotic.

Route 1:

- mostly familiar early Pokemon,
- rotating rare official starters,
- Eevee/Pikachu/Ralts/Abra-style special excitement,
- one ultra-rare Dratini-style surprise.

Route 2:

- forest edge Pokemon,
- Gastly at night,
- Rockruff/Sandile as unusual migration signs,
- Larvitar as ultra-rare.

Viridian Forest:

- should not contain every starter,
- should showcase Grass/Bug/Electric/Fairy surprises,
- rare Rowlet/Snivy/Treecko/Chespin-style encounters.

Route 3 if included:

- broader post-Brock starter pool,
- Kubfu monastery/event hint,
- fossil/Phoenix foreshadowing.

## 8. Brock Battle Design

Brock should remain recognizable but not trivialized by starter choice.

Standard Mode:

- level cap: 12
- team: Geodude, Onix
- friendly-mainline hard tuning
- modern moves but not oppressive
- held items optional

Hard Mode:

- level cap: 14
- team: Geodude, Onix, regional rock wildcard
- better AI
- one anti-Water/Grass coverage surprise, but not unfair

Expert/Nuzlocke:

- level cap: 14
- team can include Geodude, Onix, Nosepass or Roggenrola
- held Berry/Sturdy-style interaction if supported
- no in-battle items if rules enabled

Design intent:

- Players who chose Charmander, Pikachu, Gastly, or Fire starters should have answers through early catches.
- Players who chose Water/Grass should still need to respect Onix.
- Standard should be challenging but fair for a normal Pokemon player.
- Hard/Expert/Nuzlocke should satisfy players who want Radical Red-style pressure.

## 9. First Rocket Anomaly

After Brock, the player exits the gym and WorldLink reports an alert near the Pewter Museum service tunnel.

Scene:

- Rocket grunts are stealing fossil scan data, not fossils.
- Ava identifies the data as "too advanced for normal fossil restoration."
- Dax rushes in and triggers a double battle.
- A Rocket grunt mentions a buyer with a gold lapel pin and a woman named Dr. Venn.
- A strange device briefly flickers and shows silhouettes of faraway regions.

Purpose:

- Team Rocket is active.
- Gold Dust is indirectly present.
- Team Phoenix is foreshadowed.
- The Meridian Engine is hinted at without being named.

## 10. Pokecenter and Mart MVP

Viridian/Pewter Pokecenters:

- normal healing,
- Nurse Joy next-gym hint,
- WorldLink terminal,
- difficulty/level cap explanation,
- PC access if engine supports it.

Viridian/Pewter Marts:

- basic balls and medicine,
- Repel or Infinite Repel unlock,
- no Rare Candy until after Brock unless debug build.

After Brock:

- Rare Candy appears in Modern/Challenge modes,
- Great Ball appears,
- first rematch board teaser appears.

## 11. OpenEmu Acceptance Test

The vertical slice is acceptable when:

- built `.gba` opens in OpenEmu,
- new game starts,
- starter selection works for at least one starter in each category,
- Blue/Ava/Dax intro sequence completes,
- WorldLink can show queued messages,
- Route 1 battle works,
- Viridian/Pewter map transitions work,
- Brock can be beaten,
- post-Brock Rocket anomaly completes,
- game saves and reloads,
- no crash in a 30-minute smoke test.
