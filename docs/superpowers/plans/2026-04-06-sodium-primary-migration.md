# Sodium Primary Migration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Sodium `1.21.1/stable` the primary renderer integration for this branch while preserving Embeddium compatibility where the API delta is small enough to maintain safely.

**Architecture:** Reorient the branch around Sodium-shaped renderer integrations and references, then keep Embeddium as an optional compatibility layer through targeted adapters and mixin gating. Avoid always-on imports of renderer-specific internals in common or Iris-only code paths so the mod remains startup-safe when only one renderer is present.

**Tech Stack:** NeoForge 1.21.1, Sodium `1.21.1/stable`, Embeddium `1.0.15+mc1.21.1`, Iris `1.8.12+mc1.21.1`, Bash, Python `unittest`, Gradle.

---

## Chunk 1: Reference And Docs

### Task 1: Refresh and document the Sodium reference checkout

**Files:**
- Modify: `.reference/sodium`
- Modify: `AGENTS.md`
- Modify: `scripts/README.md`
- Test: `scripts/test_pull_latest_log.py` (no behavior change expected; keep existing script docs intact)

- [ ] **Step 1: Fast-forward the local Sodium reference checkout**

Run:
```bash
git -C .reference/sodium fetch origin 1.21.1/stable
git -C .reference/sodium checkout 1.21.1/stable
git -C .reference/sodium pull --ff-only origin 1.21.1/stable
```

Expected: `Already up to date` or a fast-forward on `.reference/sodium`.

- [ ] **Step 2: Update AGENTS.md to make Sodium the primary renderer reference**

Edit:
- `.reference/embeddium/` reference lines
- renderer/version tables
- compatibility notes that currently treat Embeddium as primary

Required changes:
- state `.reference/sodium/` is the primary renderer reference checkout
- keep Embeddium documented as secondary compatibility reference when practical
- stop describing the active branch as Embeddium-first

- [ ] **Step 3: Update scripts/README.md reference usage**

Edit the validation workflow examples so renderer source checks prefer:
```bash
grep -r "@Mixin.*TargetClass" .reference/sodium/
```

Add a brief note that `.reference/sodium` is the primary renderer reference and Embeddium is retained for secondary compatibility checks.

- [ ] **Step 4: Review docs for stale Embeddium-primary wording**

Run:
```bash
rg -n "Embeddium.*primary|primary.*Embeddium|embeddium-compat|Embeddium for NeoForge|Use embeddium" AGENTS.md scripts/README.md gradle.properties build.gradle src/main/resources/assets/voxy/lang/en_us.json
```

Expected: only intentional Embeddium-secondary wording remains.

- [ ] **Step 5: Commit the documentation/reference refresh**

Run:
```bash
git add AGENTS.md scripts/README.md .reference/sodium
git commit -m "docs: make sodium the primary renderer reference"
```

### Task 2: Preserve the approved design and implementation artifacts

**Files:**
- Existing: `docs/superpowers/specs/2026-04-06-sodium-primary-design.md`
- Existing: `docs/superpowers/plans/2026-04-06-sodium-primary-migration.md`

- [ ] **Step 1: Ensure the plan still matches repo reality after the reference refresh**

Run:
```bash
git diff -- docs/superpowers/specs/2026-04-06-sodium-primary-design.md docs/superpowers/plans/2026-04-06-sodium-primary-migration.md
```

Expected: no changes required, or only minor wording updates.

## Chunk 2: Build And Dependency Direction

### Task 3: Restore Sodium as an active compile path

**Files:**
- Modify: `build.gradle`
- Modify: `gradle.properties`
- Test: `scripts/test_validate_mixins.py`

- [ ] **Step 1: Write the failing dependency-direction test**

Create or extend a small Python regression test, for example:
- `scripts/test_renderer_dependency_direction.py`

Test behavior:
- `build.gradle` must not exclude `src/main/java/me/cortex/voxy/client/mixin/sodium/**`
- `build.gradle` must include a Sodium compile dependency
- `build.gradle` may keep Embeddium compile-only dependency

- [ ] **Step 2: Run the test to verify it fails against the current Embeddium-first build script**

Run:
```bash
python3 scripts/test_renderer_dependency_direction.py
```

Expected: FAIL because Sodium is currently excluded and Embeddium is primary.

- [ ] **Step 3: Re-enable Sodium sources in build.gradle**

Required edits in `build.gradle`:
- remove the exclusions for:
  - `me/cortex/voxy/client/config/SodiumConfigBuilder.java`
  - `me/cortex/voxy/client/config/VoxySodiumOptions.java`
  - `me/cortex/voxy/client/compat/SodiumCompat.java`
  - `me/cortex/voxy/client/mixin/sodium/**`
- keep only exclusions that are truly Fabric-only and irrelevant on NeoForge

- [ ] **Step 4: Add Sodium as the primary renderer dependency**

Required edits:
- add compile-only dependency for the matching Sodium renderer artifact used by this branch
- keep Embeddium compile-only dependency where the secondary compat layer still needs it
- update comments so Sodium is described as primary and Embeddium as secondary

- [ ] **Step 5: Run the test to verify the dependency direction passes**

Run:
```bash
python3 scripts/test_renderer_dependency_direction.py
```

Expected: PASS.

- [ ] **Step 6: Run the existing mixin validator smoke test**

Run:
```bash
python3 scripts/test_validate_mixins.py
```

Expected: PASS.

- [ ] **Step 7: Commit the build-direction changes**

Run:
```bash
git add build.gradle gradle.properties scripts/test_renderer_dependency_direction.py
git commit -m "build: restore sodium as primary renderer dependency"
```

## Chunk 3: Mixin And Compat Gating

### Task 4: Make Sodium first-class in the mixin plugin

**Files:**
- Modify: `src/main/java/me/cortex/voxy/mixin/VoxyMixinPlugin.java`
- Modify: `src/main/resources/client.voxy.mixins.json`
- Test: `scripts/test_renderer_gating.py`

- [ ] **Step 1: Write the failing gating test**

Create:
- `scripts/test_renderer_gating.py`

Test behavior:
- `VoxyMixinPlugin` must recognize both Sodium and Embeddium renderer families
- Sodium mixins must not be excluded from active consideration
- renderer-dependent Iris mixins must not be gated on Iris alone if they also require a renderer-specific class

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
python3 scripts/test_renderer_gating.py
```

Expected: FAIL against the current Iris/Embeddium-only gating.

- [ ] **Step 3: Update VoxyMixinPlugin to support Sodium-primary logic**

Required logic:
- add Sodium class markers, for example:
  - `net.caffeinemc.mods.sodium.client.SodiumClientMod`
  - another stable Sodium-side class if needed
- treat `.mixin.sodium.` as active when Sodium is loaded or its classes are present
- retain `.mixin.embeddium.` as optional secondary support
- add a stricter condition for renderer-dependent Iris mixins

Recommended shape:
- helper methods such as `isSodiumPresent()`, `isEmbeddiumPresent()`
- a separate branch for mixed Iris+renderer requirements

- [ ] **Step 4: Split renderer-neutral and renderer-dependent Iris mixins if needed**

If `iris.MixinLevelRenderer` or similar files require renderer-specific internals, either:
- keep them renderer-neutral, or
- move renderer-specific variants into separate mixin classes/packages and gate them appropriately

Update `client.voxy.mixins.json` accordingly.

- [ ] **Step 5: Run the gating test again**

Run:
```bash
python3 scripts/test_renderer_gating.py
```

Expected: PASS.

- [ ] **Step 6: Commit the gating changes**

Run:
```bash
git add src/main/java/me/cortex/voxy/mixin/VoxyMixinPlugin.java src/main/resources/client.voxy.mixins.json scripts/test_renderer_gating.py
git commit -m "fix: gate sodium and embeddium mixins independently"
```

## Chunk 4: Sodium-Primary Runtime Compat

### Task 5: Prefer Sodium in runtime compat selection

**Files:**
- Modify: `src/main/java/me/cortex/voxy/client/compat/RendererCompatManager.java`
- Modify: `src/main/java/me/cortex/voxy/client/compat/EmbeddiumCompat.java`
- Create or Modify: `src/main/java/me/cortex/voxy/client/compat/SodiumCompat.java`
- Test: `scripts/test_renderer_manager_priority.py`

- [ ] **Step 1: Write the failing compat-manager priority test**

Create:
- `scripts/test_renderer_manager_priority.py`

Test behavior:
- `RendererCompatManager` should prefer Sodium before Embeddium
- Embeddium remains present as fallback behavior

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
python3 scripts/test_renderer_manager_priority.py
```

Expected: FAIL if Embeddium is still hard-coded as the primary path.

- [ ] **Step 3: Update RendererCompatManager to prefer Sodium**

Required behavior:
- if Sodium is loaded, return Sodium compat
- else if Embeddium is loaded, return Embeddium compat
- else return null / no compat

- [ ] **Step 4: Reconcile SodiumCompat with NeoForge usage**

Required work:
- inspect `src/main/java/me/cortex/voxy/client/compat/SodiumCompat.java`
- update imports, access points, and assumptions against `.reference/sodium`
- keep Embeddium-specific code isolated in `EmbeddiumCompat.java`

- [ ] **Step 5: Run the priority test again**

Run:
```bash
python3 scripts/test_renderer_manager_priority.py
```

Expected: PASS.

- [ ] **Step 6: Commit the compat-manager changes**

Run:
```bash
git add src/main/java/me/cortex/voxy/client/compat/RendererCompatManager.java src/main/java/me/cortex/voxy/client/compat/SodiumCompat.java src/main/java/me/cortex/voxy/client/compat/EmbeddiumCompat.java scripts/test_renderer_manager_priority.py
git commit -m "feat: prefer sodium renderer compatibility"
```

### Task 6: Reconcile renderer mixins with Sodium stable

**Files:**
- Modify: `src/main/java/me/cortex/voxy/client/mixin/sodium/**`
- Modify: `src/main/java/me/cortex/voxy/client/mixin/embeddium/**`
- Test: `scripts/test_renderer_no_hard_dependency.py`

- [ ] **Step 1: Write the failing renderer-import safety test**

Create:
- `scripts/test_renderer_no_hard_dependency.py`

Test behavior:
- always-on/common paths must not import Sodium or Embeddium internals unless gated
- Sodium-specific mixins live under `.mixin.sodium.`
- Embeddium-specific mixins live under `.mixin.embeddium.`

- [ ] **Step 2: Run the test to verify it fails where necessary**

Run:
```bash
python3 scripts/test_renderer_no_hard_dependency.py
```

Expected: FAIL if common paths still hard-reference a renderer-specific internal package.

- [ ] **Step 3: Compare the sodium mixins against `.reference/sodium`**

Run:
```bash
rg -n "class RenderSectionManager|setInfo|ChunkRenderMatrices|ChunkBuilder|SortBehavior" .reference/sodium/common/src .reference/sodium/neoforge/src -S
```

Expected: concrete source references for every active Sodium mixin target.

- [ ] **Step 4: Update Sodium mixins to the current `1.21.1/stable` API**

Focus on:
- `src/main/java/me/cortex/voxy/client/mixin/sodium/MixinRenderSectionManager.java`
- any restored Sodium config or renderer hook files

Use exact upstream signatures from `.reference/sodium`.

- [ ] **Step 5: Keep Embeddium mixins only where the same behavior is still maintainable**

For each file under `src/main/java/me/cortex/voxy/client/mixin/embeddium/**`:
- verify the target exists in Embeddium
- keep it if the logic is still equivalent
- otherwise disable via gating or remove from `client.voxy.mixins.json`

- [ ] **Step 6: Run the renderer-import safety test again**

Run:
```bash
python3 scripts/test_renderer_no_hard_dependency.py
```

Expected: PASS.

- [ ] **Step 7: Commit the mixin reconciliation**

Run:
```bash
git add src/main/java/me/cortex/voxy/client/mixin/sodium src/main/java/me/cortex/voxy/client/mixin/embeddium scripts/test_renderer_no_hard_dependency.py
git commit -m "refactor: make sodium mixins primary and embeddium optional"
```

## Chunk 5: Config And User-Facing Terminology

### Task 7: Make UI/config language Sodium-primary without breaking stored Embeddium settings

**Files:**
- Modify: `src/main/java/me/cortex/voxy/client/VoxyClient.java`
- Modify: `src/main/java/me/cortex/voxy/client/config/VoxyConfig.java`
- Modify: `src/main/java/me/cortex/voxy/client/config/VoxyNeoForgeConfig.java`
- Modify: `src/main/java/me/cortex/voxy/client/config/VoxyConfigMenu.java`
- Modify: `src/main/java/me/cortex/voxy/client/compat/EmbeddiumOptionsCompatManager.java`
- Modify: `src/main/resources/assets/voxy/lang/en_us.json`

- [ ] **Step 1: Write the failing terminology/config test**

Create:
- `scripts/test_renderer_terminology.py`

Test behavior:
- user-facing strings should prefer Sodium wording
- config compatibility may still preserve legacy Embeddium key names where migration would be risky

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
python3 scripts/test_renderer_terminology.py
```

Expected: FAIL while Embeddium-first text remains.

- [ ] **Step 3: Update user-facing text and config bridge code**

Required behavior:
- UI strings say Sodium where that is now the primary renderer path
- legacy persisted config compatibility remains intact where practical
- comments and helper names should be clarified where they would otherwise mislead future maintenance

- [ ] **Step 4: Run the terminology test again**

Run:
```bash
python3 scripts/test_renderer_terminology.py
```

Expected: PASS.

- [ ] **Step 5: Commit the config/text cleanup**

Run:
```bash
git add src/main/java/me/cortex/voxy/client/VoxyClient.java src/main/java/me/cortex/voxy/client/config src/main/java/me/cortex/voxy/client/compat/EmbeddiumOptionsCompatManager.java src/main/resources/assets/voxy/lang/en_us.json scripts/test_renderer_terminology.py
git commit -m "refactor: make sodium the primary user-facing renderer path"
```

## Chunk 6: Full Verification

### Task 8: Verify build and startup-safety guardrails

**Files:**
- Existing tests and build outputs only

- [ ] **Step 1: Run all Python guardrail tests**

Run:
```bash
python3 scripts/test_validate_mixins.py
python3 scripts/test_pull_latest_log.py
python3 scripts/test_iris_no_embeddium_dependency.py
python3 scripts/test_renderer_dependency_direction.py
python3 scripts/test_renderer_gating.py
python3 scripts/test_renderer_manager_priority.py
python3 scripts/test_renderer_no_hard_dependency.py
python3 scripts/test_renderer_terminology.py
```

Expected: all PASS.

- [ ] **Step 2: Run a full build**

Run:
```bash
./gradlew -Dorg.gradle.java.home=/var/home/linuxbrew/.linuxbrew/Cellar/openjdk@21/21.0.10/libexec build
```

Expected: `BUILD SUCCESSFUL`.

- [ ] **Step 3: Snapshot the latest local Prism log**

Run:
```bash
bash scripts/pull_latest_log.sh
```

Expected: `.tmp/logs/latest-1.21.1.log` is updated.

- [ ] **Step 4: Deploy the jar to a Sodium-based runtime and capture results**

Run the appropriate local deployment or manual jar replacement, then:
```bash
bash scripts/pull_latest_log.sh
rg -n -C 6 "(Exception|Caused by:|MixinTransformerError|ClassNotFoundException|Sodium|Embeddium)" .tmp/logs/latest-1.21.1.log
```

Expected: no new startup crash caused by Sodium-primary migration.

- [ ] **Step 5: If available, verify an Embeddium runtime as a secondary compatibility smoke test**

Expected: either successful startup or a narrowly scoped, documented feature limitation rather than a bootstrap crash.

- [ ] **Step 6: Commit the verification-backed migration**

Run:
```bash
git status --short
git commit -am "feat: migrate renderer compatibility to sodium primary"
```

Only commit after all verification steps are green.
