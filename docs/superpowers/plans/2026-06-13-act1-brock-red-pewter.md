# Act 1 Brock, Red Training, and Pewter Museum Plan

## Implementation Steps

1. Apply existing engine patches `0001` through `0007` to the clean upstream engine checkout.
2. Add Red companion NPC scenes to Route 1, Viridian City, and Pewter City map scripts and object data.
3. Rebalance `TRAINER_LEADER_BROCK` to Geodude/Nosepass/Onix at a level-14 cap.
4. Add a post-Brock WorldLink alert in Pewter Gym pointing to the museum.
5. Add a post-badge Pewter Museum NPC/script hook for the Rocket fossil anomaly.
6. Add a project validator that checks Red scenes, Brock balance, and museum hook.
7. Generate new engine patch files and restore the submodule to clean upstream.
8. Reapply all patches, run validators, build the FireRed ROM target, and update build notes.

## Patch Targets

- `patches/engine/0008-red-route1-viridian-pewter-training.patch`
- `patches/engine/0009-brock-expanded-starter-pool-balance.patch`
- `patches/engine/0010-pewter-museum-rocket-anomaly-hook.patch`

## Verification Commands

```sh
python3 tools/validate_design_data.py
python3 tools/validate_nexus_milestone.py
python3 tools/validate_act1_brock_red_pewter.py
cd engine/pokeemerald-expansion
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

## Risk Notes

- Adding objects to FRLG maps is low risk, but coordinates must avoid blocking vanilla triggers.
- Museum hook is intentionally script-only for this slice. A new service-tunnel map would expand scope and needs a separate map/layout pass.
- The build should be validated after all patches are applied together because the engine submodule is not the source of truth.
