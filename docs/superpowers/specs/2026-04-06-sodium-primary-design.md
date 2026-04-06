# Sodium Primary Compatibility Design

## Goal

Make Sodium `1.21.1/stable` the primary renderer compatibility target for this branch while preserving Embeddium compatibility where the APIs are still close enough to support without excessive duplication.

## Current State

- The repository already contains a Sodium reference checkout at `.reference/sodium`.
- That checkout is already on CaffeineMC Sodium branch `1.21.1/stable`.
- The current codebase and docs are still centered on Embeddium as the primary renderer path.
- `build.gradle` excludes most Sodium integration files and compiles against Embeddium.
- Some optional-mod gating is too coarse, especially for Iris-related code that may indirectly depend on renderer internals.

## Desired Outcome

- Sodium becomes the default reference renderer for implementation decisions and compatibility work.
- Sodium integrations are restored as active build inputs.
- Embeddium support remains available where package-only or small signature adaptations make it practical.
- Renderer-dependent Iris paths do not hard-crash when one renderer is absent.
- Documentation reflects Sodium as the primary reference and Embeddium as a secondary supported path.

## Approach

### 1. Reference and Documentation

- Treat `.reference/sodium` as the primary renderer reference in project docs.
- Update `AGENTS.md` and `scripts/README.md` to point renderer reference checks at `.reference/sodium`.
- Keep Embeddium mentioned as a practical compatibility target rather than the primary branch identity.

### 2. Build and Dependency Direction

- Re-enable Sodium source/config integration files currently excluded in `build.gradle`.
- Add Sodium compile-time dependency as the primary renderer dependency for this branch.
- Keep Embeddium compile-only support where practical for compatibility shims and alternative runtime usage.
- Preserve Iris compile-time support as before.

### 3. Compatibility Layer Direction

- Prefer Sodium package/class names in active integrations.
- Retain Embeddium compatibility through:
  - shared logic where method signatures line up
  - small renderer-specific adapters when package names diverge
  - mod/mixin gating in `VoxyMixinPlugin` and compat managers

### 4. Mixin and Optional-Mod Gating

- Restore Sodium mixins as first-class supported integrations.
- Keep Embeddium mixins optional and only apply them when Embeddium is actually present.
- Tighten Iris mixin gating so renderer-dependent Iris code is only active when the required renderer internals are available.

### 5. Runtime Compatibility Strategy

- `RendererCompatManager` should prefer Sodium when both are theoretically available.
- Embeddium support should continue only for paths that can be maintained with small deltas.
- If a code path requires materially different renderer internals, the branch should favor Sodium behavior and disable the incompatible Embeddium-specific feature rather than carrying large duplicate implementations.

## Files Expected To Change

### Docs / metadata

- `AGENTS.md`
- `scripts/README.md`
- `gradle.properties`
- `build.gradle`

### Compat selection / optional-mod detection

- `src/main/java/me/cortex/voxy/mixin/VoxyMixinPlugin.java`
- `src/main/java/me/cortex/voxy/client/compat/RendererCompatManager.java`
- `src/main/java/me/cortex/voxy/client/compat/EmbeddiumCompat.java`
- new Sodium compat equivalents where needed

### Sodium and Embeddium integrations

- `src/main/java/me/cortex/voxy/client/mixin/sodium/**`
- `src/main/java/me/cortex/voxy/client/mixin/embeddium/**`
- renderer-dependent config integration classes under `src/main/java/me/cortex/voxy/client/config/**`

### Iris / renderer-dependent safety

- `src/main/java/me/cortex/voxy/client/core/util/IrisUtil.java`
- `src/main/java/me/cortex/voxy/client/mixin/iris/**`

## Risks

### API divergence

Sodium and Embeddium are similar but not identical on NeoForge/Fabric-adjacent internal paths. The practical preservation rule is important here: only keep shared or low-cost compatibility surfaces.

### Config integration split

The current config/UI code contains both Sodium and Embeddium naming/history. This can produce user-facing confusion if the code is switched without cleanup.

### Optional-mod startup crashes

This is the highest immediate risk. Any class literal or import from a renderer-specific internal package in an always-on path can crash game startup before runtime checks execute.

## Testing Plan

- Build after dependency and source-set changes.
- Add targeted source-level regression tests for renderer-optional startup safety.
- Validate one Sodium runtime first.
- Validate one Embeddium runtime second to confirm practical preservation paths still hold.

## Recommendation

Implement the migration incrementally:

1. Documentation and dependency direction.
2. Optional-mod gating cleanup.
3. Restore Sodium source paths and compat selection.
4. Reconcile remaining Embeddium shims only where the maintenance cost stays low.
