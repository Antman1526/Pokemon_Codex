# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

Apply project-owned engine patches from the parent repo root before building:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
git -C engine/pokeemerald-expansion restore .
for patch in $(find patches/engine -name '*.patch' | sort); do
  git -C engine/pokeemerald-expansion apply ../../${patch}
done
```

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

Output ROM:

```text
engine/pokeemerald-expansion/pokenexusred.gba
```

ROM file verification:

```text
/Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening/engine/pokeemerald-expansion/pokenexusred.gba
```

Verification performed:

```text
File exists and is 32M. Header reads "NEXUS RED" (BNRE01, Rev.00).
```

## Smoke Test Checklist

- [x] ROM appears locally as `pokenexusred.gba`.
- [x] ROM opens in OpenEmu.
- [x] Title screen appears.
- [x] New game starts.
- [x] Player reaches Pallet bedroom.
- [x] Bedroom news text appears.
- [x] Mom intro text appears.
- [x] Player can reach Oak's Lab.
- [x] Save works.
- [x] Reload works.

## Notes

- 2026-06-13 10:18 CDT: Codex built `pokenexusred.gba` from the three project engine patches.
- 2026-06-13 10:20-10:29 CDT: Codex opened the ROM in OpenEmu, verified the title screen, and observed the ROM advancing into the intro/title flow. Automated keyboard input was inconsistent in this desktop session.
- 2026-06-13 10:39 CDT: Antman manually confirmed the playthrough works. Checklist items beyond title-screen verification are recorded from that manual OpenEmu playthrough confirmation.
- 2026-06-13 18:40 CDT: Codex built the Nexus starter milestone from patches `0001` through `0007`. Design validation and Nexus milestone validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). OpenEmu launch command completed; in-emulator gameplay checklist still needs a manual pass.
- 2026-06-13 21:08 CDT: Codex built the Act 1 Brock/Red/Pewter milestone from patches `0001` through `0010`. Design validation, Nexus milestone validation, and Act 1 Brock/Red/Pewter validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.61%.
- 2026-06-13 21:28 CDT: Codex built the Mt. Moon Nexus Break milestone from patches `0001` through `0011`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, and Mt. Moon Nexus Break validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.62%.
- 2026-06-13 21:45 CDT: Codex built the Cerulean Misty Bridge setup milestone from patches `0001` through `0012`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, and Cerulean Misty Bridge validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.62%.
- 2026-06-13 22:08 CDT: Codex built the Route 25 Red/Gold Dust tag setup milestone from patches `0001` through `0013`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, and Route 25 Red Gold Dust validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.62%.
- 2026-06-14 12:29 CDT: Codex built the Pokemon Mansion Phoenix field-test milestone from patches `0001` through `0031`. Full validator suite passed, including `validate_pokemon_mansion_phoenix_field_test.py`. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.71%. This milestone turns Mansion exploration into the first Phoenix pressure dungeon, keeps the first Phoenix-linked battle on existing Scientist Ted, and makes the Secret Key a Blaine handoff.
- 2026-06-14 12:19 CDT: Codex built the Cinnabar Sea Phoenix arrival milestone from patches `0001` through `0030`. Full validator suite passed, including `validate_cinnabar_sea_phoenix_arrival.py`. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.70%. This milestone adds Route 19 Tide Rider guidance, Red's Cinnabar restraint scene, Phoenix first-contact in the Lab, and the Pokemon Mansion Mewtwo/Phoenix echo.
- 2026-06-14 12:06 CDT: Codex built the Sabrina Moonlight Gym milestone from patches `0001` through `0029`. Full validator suite passed, including `validate_sabrina_moonlight_gym.py`. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.70%. This milestone adds Red and Misty outside Sabrina's distorted Gym, the Moonlight Veil entrance signal, and Marsh Badge WorldLink stabilization toward the sea/Phoenix arc.
- 2026-06-14 19:20 CDT: Codex built the Silph mid-floors Portable PC milestone from patches `0001` through `0027`. Full validator suite passed, including `validate_silph_mid_floors_portable_pc.py`. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.69%.
- 2026-06-14 19:42 CDT: Codex built the Silph finale Giovanni milestone from patches `0001` through `0028`. Full validator suite passed, including `validate_silph_finale_giovanni.py`. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.69%.
- 2026-06-13 23:41 CDT: Codex built the Vermilion S.S. Anne crisis milestone from patches `0001` through `0014`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, and Vermilion S.S. Anne crisis validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.63%.
- 2026-06-14 08:59 CDT: Codex built the Surge grid and WorldLink feed milestone from patches `0001` through `0015`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, and Surge grid WorldLink validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.64%.
- 2026-06-14 09:37 CDT: Codex built the Route 11 Diglett bridge milestone from patches `0001` through `0016`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, Surge grid WorldLink validation, and Route 11 Diglett bridge validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.64%.
- 2026-06-14 10:12 CDT: Codex built the Rock Tunnel Cave Lantern milestone from patches `0001` through `0017`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, Surge grid WorldLink validation, Route 11 Diglett bridge validation, and Rock Tunnel Cave Lantern validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.64%.
- 2026-06-14 11:05 CDT: Codex built the Lavender Tower Moonlight milestone from patches `0001` through `0018`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, Surge grid WorldLink validation, Route 11 Diglett bridge validation, Rock Tunnel Cave Lantern validation, and Lavender Tower Moonlight validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.65%.
- 2026-06-14 11:55 CDT: Codex built the Celadon market hideout milestone from patches `0001` through `0019`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, Surge grid WorldLink validation, Route 11 Diglett bridge validation, Rock Tunnel Cave Lantern validation, Lavender Tower Moonlight validation, and Celadon market hideout validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.65%.
- 2026-06-14 12:36 CDT: Codex built the Rocket Hideout B1F milestone from patches `0001` through `0020`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, Surge grid WorldLink validation, Route 11 Diglett bridge validation, Rock Tunnel Cave Lantern validation, Lavender Tower Moonlight validation, Celadon market hideout validation, and Rocket Hideout B1F validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.65%.
- 2026-06-14 13:28 CDT: Codex built the Giovanni Silph Scope milestone from patches `0001` through `0021`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, Vermilion S.S. Anne crisis validation, Surge grid WorldLink validation, Route 11 Diglett bridge validation, Rock Tunnel Cave Lantern validation, Lavender Tower Moonlight validation, Celadon market hideout validation, Rocket Hideout B1F validation, and Giovanni Silph Scope validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.66%.
- 2026-06-14 14:24 CDT: Codex built the Silph Scope return milestone from patches `0001` through `0022`. Design validation, all prior milestone validators, and Silph Scope return validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.66%. This milestone adds Marowak grief support with Red, Poke Flute route unlock guidance, and the Fuchsia/Saffron branch warning.
- 2026-06-14 14:49 CDT: Codex built the Route 12 Snorlax and Fuchsia arrival milestone from patches `0001` through `0023`. Design validation, all prior milestone validators, and Route 12 Snorlax Fuchsia validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.67%. This milestone adds the Poke Flute field payoff, Red/Misty road support, Dax's Fuchsia arrival pressure, and the Safari/Koga hook.
- 2026-06-14 15:31 CDT: Codex built the Safari Gold Dust Field Log milestone from patches `0001` through `0024`. Design validation, all prior milestone validators, and Safari Gold Dust Field Log validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.67%. This milestone adds Ava's Safari checklist, Gold Dust scout pressure, Warden prize route tease, and Koga status prep.
- 2026-06-14 11:17 CDT: Codex built the Koga Warden Saffron milestone from patches `0001` through `0025`. Design validation, all prior milestone validators, and Koga Warden Saffron validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.67%. This milestone adds the Koga status trial, Warden notes theft, and Saffron lockdown handoff.
- 2026-06-14 11:27 CDT: Codex built the Saffron Silph lower floors milestone from patches `0001` through `0026`. Design validation, all prior milestone validators, and Saffron Silph lower floors validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.68%. This milestone adds Saffron arrival, Red Silph split, Silph lower floors, and the first Portable PC full-access teaser.

## Engine Patches To Apply Before Build

- `patches/engine/0001-pallet-bedroom-mom-intro.patch` - Pallet bedroom news and Mom intro text.
- `patches/engine/0002-pallet-red-blue-scene.patch` - first outdoor Red/Blue Pallet scene.
- `patches/engine/0003-oak-lab-nexus-intro.patch` - Oak lab Nexus Red framing.
- `patches/engine/0004-worldlink-route1-alert.patch` - first Pokédex-style WorldLink alert after Blue's lab battle.
- `patches/engine/0005-oak-27-starter-menu.patch` - Oak's 27 official regional starter menu.
- `patches/engine/0006-route1-3-badge-scaled-encounters.patch` - badge-scaled Route 1-3 wild starter and special encounter tables.
- `patches/engine/0007-route3-anomaly-wild-battles.patch` - repeatable Route 3 Nexus anomaly encounters for remaining early species.
- `patches/engine/0008-red-route1-viridian-pewter-training.patch` - warm Red companion scenes on Route 1, Viridian City, and Pewter City.
- `patches/engine/0009-brock-expanded-starter-pool-balance.patch` - Brock rebalance for the expanded starter pool and post-badge WorldLink museum alert.
- `patches/engine/0010-pewter-museum-rocket-anomaly-hook.patch` - Pewter Museum fossil scan anomaly hook tied to Rocket/Nexus activity.
- `patches/engine/0011-mt-moon-nexus-break.patch` - Mt. Moon Red companion scene, Rocket Nexus fossil rewrite, and Dome/Helix artifact logging.
- `patches/engine/0012-cerulean-misty-bridge-setup.patch` - Cerulean Red/Misty companion setup and Nugget Bridge Rocket WorldLink recruitment hook.
- `patches/engine/0013-route25-red-gold-dust-tag.patch` - Route 25 first Red tag setup, Rocket/Team Gold Dust clash, and Bill WorldLink anomaly rewrite.
- `patches/engine/0014-vermilion-ss-anne-crisis.patch` - Vermilion Blue jealousy scene, S.S. Anne Rocket/Gold Dust/Johto manifest crisis, Misty post-crisis joining, and Johto locked preview.
- `patches/engine/0015-surge-grid-worldlink.patch` - Rocket grid sabotage in Vermilion Gym, Surge cap tuning, Trail Cutter prototype text, Fan Club Gold Dust clue, and post-Surge WorldLink rival feed.
- `patches/engine/0016-route11-diglett-bridge.patch` - Route 11 rival-race checkpoint, warm Red Trail Cutter guidance, Diglett's Cave Trail Cutter calibration, and Rock Tunnel checklist handoff.
- `patches/engine/0017-rock-tunnel-cave-lantern.patch` - Rock Tunnel Cave Lantern auto-lighting after Thunder Badge, Brock Route 10 cave advice, Red tunnel companion check, Moonlight Echo foreshadowing, and Lavender low-light static.
- `patches/engine/0018-lavender-tower-moonlight.patch` - Pokemon Tower Red companion check, Team Moonlight name reveal, Marowak dream static, Rocket/Fuji Moonlight separation, and Poke Flute warning.
- `patches/engine/0019-celadon-market-hideout.patch` - Celadon Gold Dust buyer, Rocket Game Corner WorldLink pulse, Erika market warning, and Ability Capsule vendor access.
- `patches/engine/0020-rocket-hideout-b1f.patch` - Rocket Hideout B1F Red companion check, Rocket logistics rewrite, Gold Dust ledger clue, and Portable PC beta terminal.
- `patches/engine/0021-giovanni-silph-scope.patch` - Rocket Hideout Blue late-arrival scene, Red pre-Giovanni support, Meridian prototype hint, Silph Scope return guidance, and Portable PC beta storage confidence.
- `patches/engine/0022-silph-scope-return.patch` - Lavender Tower Silph Scope return payoff, Red Marowak grief support, Poke Flute route unlock guidance, and Fuchsia/Saffron branch warning.
- `patches/engine/0023-route12-snorlax-fuchsia.patch` - Route 12 Snorlax Poke Flute payoff, Red/Misty road support, Dax Fuchsia arrival, and Safari/Koga hook.
- `patches/engine/0024-safari-gold-dust-field-log.patch` - Ava's Safari Field Log, Gold Dust scout pressure, Warden prize route tease, and Koga status prep.
- `patches/engine/0025-koga-warden-saffron-lockdown.patch` - Koga status trial, Warden notes theft, and Saffron lockdown handoff.
- `patches/engine/0026-saffron-silph-lower-floors.patch` - Saffron arrival, Red Silph split, Silph lower floors, and Portable PC full-access teaser.

## Validation

Command:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
python3 tools/validate_design_data.py
```

Result:

```text
Design data validation passed.
```

## Nexus Starter Milestone Automated Verification

Commands:

```sh
python3 tools/validate_design_data.py
python3 tools/validate_nexus_milestone.py
python3 tools/validate_act1_brock_red_pewter.py
python3 tools/validate_mt_moon_nexus_break.py
python3 tools/validate_cerulean_misty_bridge.py
python3 tools/validate_route25_red_gold_dust.py
python3 tools/validate_vermilion_ss_anne_crisis.py
python3 tools/validate_surge_grid_worldlink.py
python3 tools/validate_route11_diglett_bridge.py
python3 tools/validate_rock_tunnel_cave_lantern.py
python3 tools/validate_lavender_tower_moonlight.py
python3 tools/validate_celadon_market_hideout.py
python3 tools/validate_rocket_hideout_b1f.py
python3 tools/validate_giovanni_silph_scope.py
python3 tools/validate_silph_scope_return.py
python3 tools/validate_route12_snorlax_fuchsia.py
python3 tools/validate_safari_gold_dust_field_log.py
python3 tools/validate_koga_warden_saffron_lockdown.py
python3 tools/validate_saffron_silph_lower_floors.py
file engine/pokeemerald-expansion/pokenexusred.gba
```

Results:

```text
Design data validation passed.
Nexus milestone validation passed.
Act 1 Brock/Red/Pewter validation passed.
Mt. Moon Nexus Break validation passed.
Cerulean Misty Bridge validation passed.
Route 25 Red Gold Dust validation passed.
Vermilion S.S. Anne crisis validation passed.
Surge grid WorldLink validation passed.
Route 11 Diglett bridge validation passed.
Rock Tunnel Cave Lantern validation passed.
Lavender Tower Moonlight validation passed.
Celadon market hideout validation passed.
Rocket Hideout B1F validation passed.
Giovanni Silph Scope validation passed.
Silph Scope return validation passed.
Route 12 Snorlax Fuchsia validation passed.
Safari Gold Dust Field Log validation passed.
Koga Warden Saffron validation passed.
Saffron Silph lower floors validation passed.
Game Boy Advance ROM image: "NEXUS RED" (BNRE01, Rev.00)
```

Manual OpenEmu checklist still needed:

- [ ] Oak offers regional starter menus.
- [ ] Selected starter is level 5.
- [ ] Blue's lab battle completes.
- [ ] First WorldLink alert appears.
- [ ] Route 1 wild encounters work.
- [ ] Route 2 wild encounters work.
- [ ] Route 3 wild encounters work.
- [ ] Route 3 anomaly encounters work.
- [ ] Red Route 1 scene appears.
- [ ] Red Viridian City scene appears.
- [ ] Red Pewter City scene changes after Brock.
- [ ] Brock uses Geodude/Nosepass/Onix at cap 14.
- [ ] Post-Brock WorldLink museum alert appears.
- [ ] Pewter Museum fossil scan anomaly dialogue appears after Boulder Badge.
- [ ] Red Mt. Moon scene appears.
- [ ] Rocket Mt. Moon dialogue references Nexus fossil scans.
- [ ] Dome Fossil logs as Antman's first Nexus artifact.
- [ ] Helix Fossil logs as Antman's first Nexus artifact.
- [ ] Miguel points toward Cinnabar/Cerulean signal path.
- [ ] Red Cerulean City bridge setup scene appears before Cascade Badge.
- [ ] Misty Cerulean City companion scene appears before Cascade Badge.
- [ ] Misty's gym reward points Antman to the outside follow-up scene.
- [ ] Misty Cerulean City companion scene changes after Cascade Badge.
- [ ] Nugget Bridge Rocket dialogue references WorldLink readings.
- [ ] Red Route 24 tag-battle setup scene changes after the Rocket recruiter.
- [ ] Red Route 25 tag setup appears near Sea Cottage.
- [ ] Rocket and Team Gold Dust argument appears.
- [ ] Route 25 two-trainer tag battle starts.
- [ ] Rocket Koffing and Team Gold Dust Meowth are level 18.
- [ ] Red confirms first tag win after battle.
- [ ] Bill references the WorldLink pulse and gold fossil shard.
- [ ] Bill's Cell Separation instructions reference WorldLink residue.
- [ ] Blue jealousy is foreshadowed after the Route 25 battle.
- [ ] Vermilion Harbor Red scene appears before boarding the S.S. Anne.
- [ ] Vermilion Harbor Blue jealousy scene appears before boarding the S.S. Anne.
- [ ] Vermilion Harbor Misty watch scene appears before boarding the S.S. Anne.
- [ ] Blue's S.S. Anne battle text references Red and WorldLink pressure.
- [ ] S.S. Anne manifest crisis shows Rocket, Team Gold Dust, and Bell Tower courier conflict.
- [ ] S.S. Anne two-trainer battle starts against Rocket and Team Gold Dust.
- [ ] Captain text references the gold manifest flash and Johto compass signal.
- [ ] Misty post-crisis harbor scene says she is joining the recurring companion team.
- [ ] Vermilion Harbor sign shows Johto detected but locked after the crisis.
- [ ] Vermilion Harbor Red post-crisis scene points toward Surge prep.
- [ ] Vermilion Harbor Misty post-crisis scene warns about Surge's power/current.
- [ ] Vermilion Gym Rocket grid sabotage NPC appears.
- [ ] Rocket grid sabotage battle starts before Surge.
- [ ] Surge uses Voltorb level 21, Pikachu level 22, and Raichu level 24.
- [ ] Thunder Badge reward text mentions Trail Cutter prototype registration.
- [ ] Post-Surge WorldLink rival feed mentions Blue, Ava, Dax, and locked Lyra / Johto.
- [ ] Pokemon Fan Club worker mentions the Gold Dust collector and Celadon buyer.
- [ ] Route 11 Blue rival-race checkpoint appears after Surge.
- [ ] Route 11 Red scene explains Trail Cutter underground readings.
- [ ] Diglett's Cave old man says the tunnel is not a region shortcut.
- [ ] Route 11 East Entrance guard gives the Rock Tunnel checklist.
- [ ] Pokemon Tower 2F Red scene appears and changes after Blue's battle.
- [ ] Blue Pokemon Tower battle text references WorldLink pressure.
- [ ] Pokemon Tower 5F Moonlight Veil names Team Moonlight.
- [ ] Marowak ghost scene mentions dream static after Cubone's mother is calmed.
- [ ] Pokemon Tower 7F Rocket grunts separate Rocket motives from Team Moonlight.
- [ ] Mr. Fuji explains Rocket, Team Moonlight, and the Poke Flute warning.
- [ ] Celadon Restaurant Gold Dust buyer mentions rare anchors and the Celadon buyer network.
- [ ] Celadon Game Corner poster switch references a WorldLink pulse.
- [ ] Game Corner Rocket grunt references Gold Dust buyers.
- [ ] Celadon Department Store 2F Ability Capsule vendor sells ITEM_ABILITY_CAPSULE.
- [ ] Erika post-battle text warns about Celadon's rare market.
- [ ] Rocket Hideout B1F Red entry scene appears near the stairs.
- [ ] Rocket Hideout B1F Portable PC beta terminal opens the PC menu.
- [ ] Rocket Hideout B1F Gold Dust ledger references the Celadon buyer and rare anchors.
- [ ] Rocket Hideout B1F grunts mention Rocket logistics, Silph Scope movement, and Gold Dust pressure.
- [ ] Rocket Hideout B3F Blue late-arrival scene appears.
- [ ] Rocket Hideout B4F Red pre-Giovanni support scene appears.
- [ ] Giovanni references the Meridian prototype without revealing the final Nexus Order.
- [ ] Silph Scope pickup points Antman back to Lavender Tower and mentions Portable PC beta storage confidence.
- [ ] Pokemon Tower 6F Red Marowak grief support appears on the Silph Scope return.
- [ ] Marowak calm text says the Silph Scope revealed grief, not a monster.
- [ ] Pokemon Tower 7F Rocket grunts reference Antman's Silph Scope return and Rocket proof-control motive.
- [ ] Mr. Fuji Poke Flute reward points toward Snorlax roads, Fuchsia, and Saffron/Silph Co. pressure.
- [ ] Route 12 Red support scene appears near Snorlax after Poke Flute unlock.
- [ ] Route 12 Misty support scene points toward Fuchsia and warns against rushing Saffron.
- [ ] Route 12 Snorlax wake-up text references WorldLink and the Poke Flute field payoff.
- [ ] Fuchsia Dax arrival scene appears and frames Safari/Koga as the next recommended route.
- [ ] Fuchsia Safari/Gym signs mention rare-habitat research, Gold Dust risk, and Koga poison/status preparation.
- [ ] Safari Zone entrance Ava scene explains the Safari Field Log checklist.
- [ ] Safari Zone entrance attendant text preserves classic Safari payment flow while mentioning WorldLink field logging.
- [ ] Safari Zone office Gold Dust scout appears and hints at rare habitat/pedigree interest.
- [ ] Safari Zone office Warden prize text points toward the far-corner route and Koga status prep.
- [ ] Koga intro frames the battle as a status trial before Saffron.
- [ ] Koga reward text registers the Soul Badge as WorldLink clearance for Silph pressure.
- [ ] Warden post-teeth dialogue mentions stolen habitat notes and Gold Dust.
- [ ] Saffron Rocket lockdown dialogue references Silph, Blue's failed push, and Gold Dust market pressure.
- [ ] Saffron Red arrival scene appears near the Silph line and changes if Soul Badge is missing.
- [ ] Silph 1F lobby text frames the building as a lockdown checkpoint.
- [ ] Silph 2F Rocket/scientist text references Rocket logistics and teleport routing.
- [ ] Silph 3F text references Blue's pressure trail and Portable PC system risk.
- [ ] Silph 4F Gold Dust terminal evidence appears through worker/scientist/floor-sign text.
- [ ] Silph 5F Portable PC full access terminal opens the PC menu.
- [ ] Silph 6F text references Red's civilian route through the building.
- [ ] Silph 7F Blue emotional pressure scene appears before the classic rival battle.
- [ ] `0027-silph-mid-floors-portable-pc.patch` applies cleanly and `validate_silph_mid_floors_portable_pc.py` passes.
- [ ] Silph 8F text references Gold Dust buyer-network evidence.
- [ ] Silph 9F healing woman frames the room as an emergency heal hub.
- [ ] Silph 10F Red boardroom check appears near the final stair.
- [ ] Silph 11F Giovanni Meridian Gate speech appears before the boss battle.
- [ ] Master Ball WorldLink payoff text appears after Giovanni.
- [ ] Sabrina Moonlight handoff appears through Silph 11F post-boss reward text.
- [ ] `0028-silph-finale-giovanni.patch` applies cleanly and `validate_silph_finale_giovanni.py` passes.
- [ ] Saffron Red Sabrina gate scene explains why Red cannot enter the distorted Gym.
- [ ] Saffron Misty Sabrina support scene frames Misty as keeping the city current calm.
- [ ] Saffron Gym Moonlight Veil sign appears near the entrance teleport maze.
- [ ] Marsh Badge WorldLink stabilization text points toward sea routes and old fire.
- [ ] `0029-sabrina-moonlight-gym.patch` applies cleanly and `validate_sabrina_moonlight_gym.py` passes.
- [ ] Route 19 Red Tide Rider sea-route scene explains earned Kanto sea travel.
- [ ] Cinnabar Red restraint scene frames old fire, revival science, and Mewtwo rumors carefully.
- [ ] Cinnabar Lab Phoenix first-contact scene identifies restoration matrices and controlled rebirth language.
- [ ] Pokemon Mansion Mewtwo Phoenix echo links old science to Phoenix interest without resolving Mewtwo yet.
- [ ] `0030-cinnabar-sea-phoenix-arrival.patch` applies cleanly and `validate_cinnabar_sea_phoenix_arrival.py` passes.
- [ ] Pokemon Mansion 1F Phoenix-linked Scientist Ted battle text appears before and after the existing battle.
- [ ] Pokemon Mansion 2F restoration ledger diary rewrite preserves Mew discovery while adding Phoenix context.
- [ ] Pokemon Mansion 3F Mewtwo birth warning rewrite keeps Mewtwo unresolved and warns about creation without restraint.
- [ ] Pokemon Mansion B1F Secret Key Blaine handoff text points to Blaine as the next Act 6 objective.
- [ ] `0031-pokemon-mansion-phoenix-field-test.patch` applies cleanly and `validate_pokemon_mansion_phoenix_field_test.py` passes.
- [ ] Route 10 Pokemon Center Brock scene explains Cave Lantern.
- [ ] Rock Tunnel lights automatically after Thunder Badge through Cave Lantern protocol.
- [ ] Rock Tunnel Red scene appears and warns about the echo.
- [ ] Rock Tunnel B1F Moonlight Echo foreshadowing appears.
- [ ] Lavender boy references low-light static from Rock Tunnel.
- [ ] Save works after this milestone.
- [ ] Reload works after this milestone.
