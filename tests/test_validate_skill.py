from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skill.py"
SKILL = ROOT / "skills" / "omakase"


class ValidateSkillTest(unittest.TestCase):
    def validate_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory)
            (skill / "SKILL.md").write_text(text)
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(skill)],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_accepts_the_repository_skill(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(SKILL)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "Skill is valid!")

    def test_rejects_unexpected_frontmatter_keys(self):
        result = self.validate_text(
            "---\nname: example\ndescription: Example skill\nunexpected: true\n---\n"
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Unexpected frontmatter key", result.stdout)

    def test_rejects_an_invalid_skill_name(self):
        result = self.validate_text(
            "---\nname: Invalid Name\ndescription: Example skill\n---\n"
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("hyphen-case", result.stdout)

    def test_rejects_an_unfinished_todo(self):
        result = self.validate_text(
            "---\nname: example\ndescription: Example skill\n---\n\n"
            "[TODO: finish these instructions]\n"
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("unfinished TODO", result.stdout)

    def test_allows_todo_examples_inside_list_indented_fences(self):
        result = self.validate_text(
            "---\nname: example\ndescription: Example skill\n---\n\n"
            "-   ```text\n"
            "  [TODO: example placeholder]\n"
            "    ```\n"
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_invalid_descriptions(self):
        descriptions = (
            ("[not, text]", "must be a string"),
            ('"[TODO: describe this skill]"', "unfinished TODO"),
            ('"Use <placeholder>"', "angle brackets"),
            ('"' + ("x" * 1025) + '"', "1024 characters or fewer"),
        )
        for description, expected_message in descriptions:
            with self.subTest(expected_message=expected_message):
                result = self.validate_text(
                    f"---\nname: example\ndescription: {description}\n---\n"
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected_message, result.stdout)


if __name__ == "__main__":
    unittest.main()
