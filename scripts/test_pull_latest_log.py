#!/usr/bin/env python3
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "pull_latest_log.sh"


class PullLatestLogTest(unittest.TestCase):
    def test_copies_source_log_to_default_repo_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_repo = Path(tmp)
            source_log = temp_repo / "source-latest.log"
            source_text = "[10:00:00] [main/INFO]: hello from prism\n"
            source_log.write_text(source_text, encoding="utf-8")

            result = subprocess.run(
                ["bash", str(SCRIPT_PATH)],
                cwd=temp_repo,
                env={
                    **os.environ,
                    "VOXY_PULL_LATEST_LOG_SOURCE": str(source_log),
                },
                capture_output=True,
                text=True,
                check=False,
            )

            snapshot_path = temp_repo / ".tmp" / "logs" / "latest-1.21.1.log"
            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertTrue(snapshot_path.is_file(), "expected repo-local latest.log snapshot to exist")
            self.assertEqual(snapshot_path.read_text(encoding="utf-8"), source_text)
            self.assertIn(str(snapshot_path), result.stdout)


if __name__ == "__main__":
    unittest.main()
