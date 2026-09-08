import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "omakase" / "scripts" / "profile_path.py"


class ProfilePathTest(unittest.TestCase):
    def git(self, *args, cwd):
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )

    def resolve(self, repo):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_resolves_one_profile_in_primary_checkout_from_every_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            primary = root / "project"
            linked = root / "project-feature"
            primary.mkdir()
            self.git("init", "-b", "main", cwd=primary)
            self.git("config", "user.email", "test@example.com", cwd=primary)
            self.git("config", "user.name", "Omakase Test", cwd=primary)
            (primary / "README.md").write_text("test\n")
            self.git("add", "README.md", cwd=primary)
            self.git("commit", "-m", "Initial commit", cwd=primary)
            self.git("worktree", "add", "-b", "feature", str(linked), cwd=primary)

            expected = primary.resolve() / ".omakase.local.yml"
            for repo in (primary, linked):
                with self.subTest(repo=repo):
                    result = self.resolve(repo)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(Path(result.stdout.strip()), expected)

    def test_reports_a_clear_error_outside_git(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.resolve(directory)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not inside a Git repository", result.stderr)

    def test_rejects_a_bare_repository_without_a_working_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            bare = Path(directory) / "project.git"
            self.git("init", "--bare", str(bare), cwd=directory)

            result = self.resolve(bare)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("bare repository has no working tree", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_reports_a_clear_error_when_git_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--repo", directory],
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PATH": ""},
            )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("git executable is unavailable", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
