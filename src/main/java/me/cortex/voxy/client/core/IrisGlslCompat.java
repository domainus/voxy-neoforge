package me.cortex.voxy.client.core;

import java.util.Locale;

final class IrisGlslCompat {
    private static final String GLSL_COMPAT_FIXES_MODE =
            System.getProperty("voxy.irisGlslCompatFixes", "auto").toLowerCase(Locale.ROOT);

    private IrisGlslCompat() {
    }

    static String mode() {
        return GLSL_COMPAT_FIXES_MODE;
    }

    static boolean shouldApplyFixes(String source) {
        if (source == null || source.isBlank()) {
            return false;
        }
        return switch (GLSL_COMPAT_FIXES_MODE) {
            case "true" -> true;
            case "false" -> false;
            default -> source.contains("shadow2D(") || source.contains("shadow2DLod(");
        };
    }

    static String applyFixes(String source) {
        if (source == null) {
            return null;
        }
        if (!shouldApplyFixes(source)) {
            return source;
        }
        source = source.replace("shadow2D(", "texture(");
        source = source.replace("shadow2DLod(", "textureLod(");
        return source;
    }
}
