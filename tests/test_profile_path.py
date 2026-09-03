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


if __name__ == "__main__":
    unittest.main()
