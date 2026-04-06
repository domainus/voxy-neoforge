# Voxy 0.2.13 Backport Design

## Goal

Backport all upstream Voxy changes from the upstream Fabric `0.2.9-alpha` baseline used by this NeoForge port through upstream `0.2.13-alpha`, while preserving Minecraft `1.21.1`, NeoForge `21.1.115`, Embeddium `1.0.15+mc1.21.1`, Iris `1.8.12+mc1.21.1`, and Monocle compatibility.

## Evidence

- Current port branch head: `03466999`
- Upstream head: `ebea10c8`
- Shared merge-base with upstream `dev`: `cff48664`
- Upstream version window:
  - `d0e879b6` moves upstream from `0.2.9-alpha` to `0.2.10-alpha`
  - `37230b6b` moves upstream to `0.2.11-alpha`
  - `e62beff1` moves upstream to `0.2.12-alpha`
  - `8e749ed4` moves upstream to `0.2.13-alpha`

The implementation target is the upstream change range `d0e879b6^..8e749ed4`, with later upstream commits treated as out of scope unless they are required to make the `0.2.13` range build or function correctly on this port.

## Constraints

- Keep NeoForge loader, metadata, access transformer, and mixin config layout intact.
- Keep Minecraft pinned to `1.21.1`.
- Preserve NeoForge-side integrations already established in this repo:
  - Embeddium render hooks and option integration
  - Iris and Monocle compatibility behavior
  - NeoForge config surface and event wiring where upstream Fabric code does not apply
- Use upstream Fabric code as the semantic source of truth for `0.2.13` behavior, but do not blindly replace platform files with Fabric loader code.
- Validate with `./gradlew build` before claiming completion.

## Approach Options

### Option 1: Commit-replay backport

Replay the upstream `0.2.9-alpha` to `0.2.13-alpha` delta conceptually onto the NeoForge port, adapting files that diverged for platform reasons.

Pros:
- Closest to "every upstream change"
- Best provenance for debugging regressions
- Makes later upstream syncs easier

Cons:
- Large conflict surface
- Requires explicit separation of platform-neutral and platform-specific code

### Option 2: Snapshot transplant

Replace local files with upstream `0.2.13-alpha` snapshots, then repair NeoForge compatibility afterward.

Pros:
- Faster initial import

Cons:
- Easier to lose port-specific behavior
- Harder to prove every upstream semantic landed correctly

### Option 3: Subsystem-by-subsystem manual cherry-pick

Individually port rendering, storage, config, and compatibility changes.

Pros:
- Lower immediate breakage risk

Cons:
- Weakest guarantee of full `0.2.13` coverage
- Higher chance of subtle omissions

## Chosen Design

Use Option 1.

The backport will be handled as a structured upstream sync:

1. Map the upstream `0.2.10` through `0.2.13` changes into three buckets:
   - Platform-neutral core/runtime logic
   - Rendering and shader pipeline logic
   - Fabric-only bootstrapping and loader-specific surface area
2. Import the upstream semantic changes for core, rendering, config, and storage into the NeoForge tree.
3. Reapply the current NeoForge-specific surface area on top:
   - `build.gradle`, `gradle.properties`, NeoForge metadata, access transformers
   - NeoForge lifecycle/event entrypoints
   - Embeddium integration classes and mixins
   - Iris/Monocle compatibility code paths
4. Resolve regressions until the port builds again on NeoForge `1.21.1`.

## File Ownership Boundaries

### Upstream-semantic source files

These should converge toward upstream `0.2.13-alpha` behavior:

- `src/main/java/me/cortex/voxy/client/**`
- `src/main/java/me/cortex/voxy/common/**`
- `src/main/java/me/cortex/voxy/commonImpl/**`
- `src/main/resources/assets/voxy/**`

### NeoForge platform files

These stay NeoForge-native and must not be overwritten by Fabric equivalents:

- `build.gradle`
- `gradle.properties`
- `settings.gradle`
- `src/main/resources/META-INF/neoforge.mods.toml`
- `src/main/resources/META-INF/accesstransformer.cfg`
- `src/main/resources/client.voxy.mixins.json`
- `src/main/resources/common.voxy.mixins.json`

### Compatibility-sensitive files

These need explicit reconciliation after upstream code is applied:

- `src/main/java/me/cortex/voxy/client/compat/**`
- `src/main/java/me/cortex/voxy/client/iris/**`
- `src/main/java/me/cortex/voxy/client/core/**`
- `src/main/java/me/cortex/voxy/client/mixin/embeddium/**`
- `src/main/java/me/cortex/voxy/client/mixin/iris/**`
- `src/main/java/me/cortex/voxy/client/mixin/sodium/**`
- `src/main/java/me/cortex/voxy/client/mixin/minecraft/**`

## Expected Conflict Areas

- Build system and dependency metadata: upstream Fabric Loom vs local NeoForge build.
- Sodium/Embeddium API drift: upstream Sodium package names and hooks vs local Embeddium adaptations.
- Iris pipeline evolution: upstream Iris changes may overwrite current Monocle- and shader-pack-specific fixes.
- Config/UI surface: upstream `0.2.13` introduces config and debug changes that may collide with current NeoForge config scaffolding.
- Storage/backend changes: RocksDB and storage abstractions changed significantly upstream and may need NeoForge-safe adaptation.

## Testing Strategy

- First gate: `./gradlew compileJava`
- Second gate: `./gradlew build`
- If build breaks due to mixins or API mismatches, fix them immediately before attempting further sync work.
- Final verification includes confirming the mod version is updated to `0.2.13-alpha` while retaining NeoForge `1.21.1` dependency pins.

## Out of Scope

- Upgrading Minecraft beyond `1.21.1`
- Converting the port back to Fabric
- Pulling in upstream commits after `8e749ed4` unless strictly required to keep the `0.2.13` backport coherent
