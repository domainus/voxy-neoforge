#!/usr/bin/env python3
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDERER_MANAGER = REPO_ROOT / "src/main/java/me/cortex/voxy/client/compat/RendererCompatManager.java"


class RendererCompatPriorityTest(unittest.TestCase):
    def test_renderer_manager_prefers_sodium_then_falls_back_to_embeddium(self) -> None:
        contents = RENDERER_MANAGER.read_text(encoding="utf-8")

        sodium_marker = 'if (ModCompat.isModLoaded("sodium") || ModCompat.isClassPresent("net.caffeinemc.mods.sodium.client.SodiumClientMod")) {'
        embeddium_marker = 'if (ModCompat.isModLoaded("embeddium")) {'

        self.assertIn(sodium_marker, contents)
        self.assertIn(embeddium_marker, contents)
        self.assertLess(
            contents.index(sodium_marker),
            contents.index(embeddium_marker),
            "RendererCompatManager must try Sodium before Embeddium",
        )
        self.assertIn('Class.forName("me.cortex.voxy.client.compat.SodiumCompat")', contents)
        self.assertIn('Class.forName("me.cortex.voxy.client.compat.EmbeddiumCompat")', contents)


if __name__ == "__main__":
    unittest.main()
