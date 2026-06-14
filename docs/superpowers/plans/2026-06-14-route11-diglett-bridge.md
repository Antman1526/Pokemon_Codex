# Route 11 Diglett Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a post-Surge Route 11/Diglett's Cave bridge that advances rival pressure, companion warmth, and Trail Cutter field-tool setup.

**Architecture:** Keep engine changes in one replayable patch, with project-owned design data and a validator in the parent repo. The engine patch adds NPC objects and dialogue only; field-tool mechanics remain a later milestone.

**Tech Stack:** pokeemerald-expansion FireRed target, FRLG map scripts, YAML design data, Python validation scripts, patch replay workflow.

---

### Task 1: Validator First

**Files:**
- Create: `tools/validate_route11_diglett_bridge.py`

- [ ] **Step 1: Write the failing validator**

Create a validator that checks for:
- `patches/engine/0016-route11-diglett-bridge.patch`
- Route 11 Red and Blue object/script markers in the patch
- Route 11 dialogue markers: `Trail Cutter`, `WorldLink`, `ROCK TUNNEL`, `DIGLETT'S CAVE`
- Diglett's Cave marker: `not a region shortcut`
- Route 11 East Entrance marker: `Checklist`
- design data markers in `data_design/kanto_chapter.yaml`, `data_design/kanto_worldlink_messages.yaml`, and `data_design/rival_progression_kanto.yaml`

- [ ] **Step 2: Run validator to verify it fails**

Run:

```bash
python3 tools/validate_route11_diglett_bridge.py
```

Expected: failure because the patch and design data markers do not exist yet.

### Task 2: Design Data

**Files:**
- Modify: `data_design/kanto_chapter.yaml`
- Modify: `data_design/kanto_worldlink_messages.yaml`
- Modify: `data_design/rival_progression_kanto.yaml`

- [ ] **Step 1: Add Act 4 bridge entries**

Add Route 11 and Diglett's Cave to the Rock Tunnel/Celadon/Lavender act. Add events for the rival race checkpoint, Trail Cutter ground ping, Brock's cave-prep advisory, and Rock Tunnel checklist handoff.

- [ ] **Step 2: Add WorldLink messages**

Add `WL_KANTO_ROUTE11_RIVAL_RACE`, `WL_KANTO_DIGLETT_TRAIL_CUTTER_PING`, and `WL_KANTO_ROCK_TUNNEL_CHECKLIST`.

- [ ] **Step 3: Add rival progression band**

Add `route11_diglett_bridge` with Red, Brock, Blue, Ava, Dax, and Lyra updates.

### Task 3: Engine Patch

**Files:**
- Create: `patches/engine/0016-route11-diglett-bridge.patch`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/Route11_Frlg/map.json`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/Route11_Frlg/scripts.inc`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/DiglettsCave_SouthEntrance_Frlg/scripts.inc`
- Modify through patch only: `engine/pokeemerald-expansion/data/maps/Route11_EastEntrance_1F_Frlg/scripts.inc`

- [ ] **Step 1: Replay previous patches**

Run:

```bash
git -C engine/pokeemerald-expansion restore .
for patch in $(ls patches/engine/000*.patch patches/engine/001[0-5]-*.patch | sort); do
  git -C engine/pokeemerald-expansion apply ../../${patch}
done
```

- [ ] **Step 2: Add Route 11 NPCs and scripts**

Add Red and Blue NPC objects to Route 11. Add Red's Trail Cutter guidance and Blue's rival-race dialogue.

- [ ] **Step 3: Add cave and gate text**

Update the Diglett's Cave South Entrance old man and Route 11 East Entrance guard text.

- [ ] **Step 4: Export patch**

Run:

```bash
git -C engine/pokeemerald-expansion diff > patches/engine/0016-route11-diglett-bridge.patch
git -C engine/pokeemerald-expansion restore .
```

### Task 4: Verification

**Files:**
- Modify: `build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md`

- [ ] **Step 1: Run route validator**

Run:

```bash
python3 tools/validate_route11_diglett_bridge.py
```

Expected: `Route 11 Diglett bridge validation passed.`

- [ ] **Step 2: Replay all patches and run validators**

Run all existing validators plus the new Route 11 validator after patch replay.

- [ ] **Step 3: Build ROM**

Run:

```bash
export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export PATH="$DEVKITARM/bin:$PATH"
make -C engine/pokeemerald-expansion -j"$(sysctl -n hw.ncpu)" firered TITLE="NEXUS RED" GAME_CODE=BNRE BUILD_NAME=nexusred
```

- [ ] **Step 4: Verify header**

Run the ROM header checker and confirm title `NEXUS RED`, game code `BNRE`, and 32 MB ROM size.

### Task 5: Commit

**Files:**
- Stage all files changed by this plan.

- [ ] **Step 1: Check cleanliness**

Run:

```bash
git diff --check
git status --short
git -C engine/pokeemerald-expansion status --short
```

- [ ] **Step 2: Commit and push**

Run:

```bash
git commit -m "Add Route 11 Diglett bridge setup"
git push origin feature/first-playable-title-opening
```
