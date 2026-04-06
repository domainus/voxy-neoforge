#!/usr/bin/env python3
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_GRADLE = REPO_ROOT / "build.gradle"


class RendererDependencyDirectionTest(unittest.TestCase):
    def test_build_gradle_keeps_sodium_active_and_embeddium_secondary(self) -> None:
        contents = BUILD_GRADLE.read_text(encoding="utf-8")

        self.assertIn(
            'compileOnly "maven.modrinth:sodium:mc1.21.1-0.6.13-neoforge"',
            contents,
            "Sodium compile dependency must stay active in build.gradle",
        )
        self.assertIn(
            'compileOnly "maven.modrinth:embeddium:${project.embeddium_version}"',
            contents,
            "Embeddium should remain available as the secondary compatibility dependency",
        )
        self.assertNotIn(
            "exclude 'me/cortex/voxy/client/mixin/sodium/**'",
            contents,
            "Sodium mixins must not be excluded from compilation",
        )
        self.assertIn(
            "Sodium is the primary renderer target for this branch.",
            contents,
            "build.gradle comments should reflect the Sodium-primary direction",
        )


if __name__ == "__main__":
    unittest.main()
