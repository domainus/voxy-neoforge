#!/usr/bin/env python3
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MIXIN_PLUGIN = REPO_ROOT / "src/main/java/me/cortex/voxy/mixin/VoxyMixinPlugin.java"
CLIENT_MIXINS = REPO_ROOT / "src/main/resources/client.voxy.mixins.json"


class RendererGatingTest(unittest.TestCase):
    def test_mixin_plugin_gates_sodium_and_embeddium_independently(self) -> None:
        plugin = MIXIN_PLUGIN.read_text(encoding="utf-8")

        self.assertIn(
            'private static final String SODIUM_CLASS = "net.caffeinemc.mods.sodium.client.SodiumClientMod";',
            plugin,
        )
        self.assertIn(
            'private static final String EMBEDDIUM_CLASS = "org.embeddedt.embeddium.impl.Embeddium";',
            plugin,
        )
        self.assertIn('if (mixinClassName.contains(".mixin.sodium.")) {', plugin)
        self.assertIn('if (mixinClassName.contains(".mixin.embeddium.")) {', plugin)
        self.assertIn('return isLoadedOrPresent("sodium", SODIUM_CLASS, SODIUM_WORLD_RENDERER_CLASS);', plugin)
        self.assertIn('return isLoadedOrPresent("embeddium", EMBEDDIUM_CLASS, EMBEDDIUM_PRELAUNCH_CLASS);', plugin)

    def test_client_mixin_config_registers_sodium_and_embeddium_mixins(self) -> None:
        mixins = CLIENT_MIXINS.read_text(encoding="utf-8")

        self.assertIn('"sodium.MixinDefaultChunkRenderer"', mixins)
        self.assertIn('"sodium.MixinRenderSectionManager"', mixins)
        self.assertIn('"embeddium.MixinDefaultChunkRenderer"', mixins)
        self.assertIn('"embeddium.MixinRenderSectionManager"', mixins)


if __name__ == "__main__":
    unittest.main()
