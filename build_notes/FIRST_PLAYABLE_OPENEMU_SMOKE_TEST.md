# Pokemon Nexus Red - First Playable OpenEmu Smoke Test

Date: 2026-06-13

## Build

Apply project-owned engine patches from the parent repo root before building:

```sh
cd /Users/Antman/.config/superpowers/worktrees/Pokemon_Codex/first-playable-title-opening
git apply --directory=engine/pokeemerald-expansion patches/engine/0001-pallet-bedroom-mom-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0002-pallet-red-blue-scene.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0003-oak-lab-nexus-intro.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0004-worldlink-route1-alert.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0005-oak-27-starter-menu.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0006-route1-3-badge-scaled-encounters.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0007-route3-anomaly-wild-battles.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0008-red-route1-viridian-pewter-training.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0009-brock-expanded-starter-pool-balance.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0010-pewter-museum-rocket-anomaly-hook.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0011-mt-moon-nexus-break.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0012-cerulean-misty-bridge-setup.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0013-route25-red-gold-dust-tag.patch
git apply --directory=engine/pokeemerald-expansion patches/engine/0014-vermilion-ss-anne-crisis.patch
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
- 2026-06-13 23:41 CDT: Codex built the Vermilion S.S. Anne crisis milestone from patches `0001` through `0014`. Design validation, Nexus milestone validation, Act 1 Brock/Red/Pewter validation, Mt. Moon Nexus Break validation, Cerulean Misty Bridge validation, Route 25 Red Gold Dust validation, and Vermilion S.S. Anne crisis validation passed. Header reads `"NEXUS RED"` (`BNRE01`, Rev.00). Build completed with ROM usage at 80.63%.

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
- [ ] Save works after this milestone.
- [ ] Reload works after this milestone.
