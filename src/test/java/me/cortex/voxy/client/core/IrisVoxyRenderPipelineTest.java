package me.cortex.voxy.client.core;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IrisVoxyRenderPipelineTest {
    @Test
    void autoRewritesLegacyBslShadowSamplerCalls() {
        String bslSource = """
                #version 150
                uniform sampler2DShadow shadowtex0;

                float sampleShadow(vec3 coord) {
                    return shadow2D(shadowtex0, coord).x;
                }
                """;

        String rewritten = IrisGlslCompat.applyFixes(bslSource);

        assertFalse(rewritten.contains("shadow2D("));
        assertTrue(rewritten.contains("texture("));
    }
}
