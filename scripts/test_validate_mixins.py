#!/usr/bin/env python3
import os
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_mixins.sh"


class ValidateMixinsPortabilityTest(unittest.TestCase):
    def test_validator_does_not_require_jq(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            resources_dir = project_dir / "src" / "main" / "resources"
            libs_dir = project_dir / "build" / "libs"
            resources_dir.mkdir(parents=True)
            libs_dir.mkdir(parents=True)

            (resources_dir / "client.test.mixins.json").write_text(
                """
{
  "required": true,
  "package": "me.example.mixin",
  "client": [
    "test.MixinExample"
  ]
}
""".strip()
                + "\n",
                encoding="utf-8",
            )

            with zipfile.ZipFile(libs_dir / "test.jar", "w") as jar_file:
                jar_file.writestr("me/example/mixin/test/MixinExample.class", b"")

            temp_bin = project_dir / "bin"
            temp_bin.mkdir()
            for command in ("bash", "basename", "cut", "dirname", "du", "find", "grep", "head", "jar", "python3"):
                resolved = shutil.which(command)
                self.assertIsNotNone(resolved, f"required command missing for test: {command}")
                os.symlink(resolved, temp_bin / command)

            env = os.environ.copy()
            env["PATH"] = str(temp_bin)

            result = subprocess.run(
                [str(temp_bin / "bash"), str(VALIDATOR)],
                cwd=project_dir,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"validator should succeed without jq\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("ALL CHECKS PASSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
