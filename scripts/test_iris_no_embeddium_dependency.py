#!/usr/bin/env python3
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FILES = [
    REPO_ROOT / "src/main/java/me/cortex/voxy/client/core/util/IrisUtil.java",
    REPO_ROOT / "src/main/java/me/cortex/voxy/client/mixin/iris/MixinLevelRenderer.java",
]
FORBIDDEN = "org.embeddedt.embeddium.impl.render.chunk.ChunkRenderMatrices"


class IrisNoEmbeddiumDependencyTest(unittest.TestCase):
    def test_iris_viewport_capture_path_does_not_import_embeddium_internals(self) -> None:
        offenders = []
        for file_path in FILES:
            contents = file_path.read_text(encoding="utf-8")
            if FORBIDDEN in contents:
                offenders.append(str(file_path.relative_to(REPO_ROOT)))

        self.assertEqual(
            offenders,
            [],
            msg="Iris-only viewport capture must not hard-reference Embeddium internals: "
            + ", ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
