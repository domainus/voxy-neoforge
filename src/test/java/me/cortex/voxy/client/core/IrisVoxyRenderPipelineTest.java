package me.cortex.voxy.client.core;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IrisVoxyRenderPipelineTest {
    private static final Path BSL_LIGHT_SHAFTS = Path.of(
            ".reference", "bsl shaders", "shaders", "lib", "atmospherics", "lightShafts.glsl"
    );

    @Test
    void autoRewritesLegacyBslShadowSamplerCalls() throws IOException {
        String bslSource = Files.readString(BSL_LIGHT_SHAFTS);

        String rewritten = IrisGlslCompat.applyFixes(bslSource);

        assertFalse(rewritten.contains("shadow2D("));
        assertTrue(rewritten.contains("texture("));
    }
}
