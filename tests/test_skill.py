from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "omakase"
SKILL = SKILL_ROOT / "SKILL.md"
METADATA = SKILL_ROOT / "agents" / "openai.yaml"
PROFILE_TEMPLATE = SKILL_ROOT / "assets" / "omakase.local.example.yml"
LOCAL_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class OmakaseSkillStructureTest(unittest.TestCase):
    def test_metadata_is_loadable_and_complete(self):
        _, frontmatter, _ = SKILL.read_text().split("---", 2)
        skill_metadata = yaml.safe_load(frontmatter)
        agent_metadata = yaml.safe_load(METADATA.read_text())

        self.assertEqual(skill_metadata["name"], "omakase")
        self.assertTrue(skill_metadata["description"].strip())
        interface = agent_metadata["interface"]
        for field in ("display_name", "short_description", "default_prompt"):
            with self.subTest(field=field):
                self.assertIsInstance(interface[field], str)
                self.assertTrue(interface[field].strip())

    def test_entrypoint_routes_to_every_support_resource(self):
        linked_files = {
            (SKILL_ROOT / target.split("#", 1)[0]).resolve()
            for target in LOCAL_LINK.findall(SKILL.read_text())
            if "://" not in target and not target.startswith(("#", "mailto:"))
        }
        support_files = [
            path
            for directory in ("assets", "references", "scripts")
            for path in (SKILL_ROOT / directory).iterdir()
            if path.is_file()
        ]

        for path in support_files:
            relative_path = path.relative_to(SKILL_ROOT).as_posix()
            with self.subTest(path=relative_path):
                self.assertIn(path.resolve(), linked_files)

    def test_local_markdown_links_resolve(self):
        markdown_files = ROOT.rglob("*.md")

        for document in markdown_files:
            for target in LOCAL_LINK.findall(document.read_text()):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                path_text = target.split("#", 1)[0]
                resolved = (document.parent / path_text).resolve()
                with self.subTest(document=document, target=target):
                    self.assertTrue(resolved.exists())

    def test_reference_documents_have_titles(self):
        for document in (SKILL_ROOT / "references").glob("*.md"):
            first_line = document.read_text().splitlines()[0]
            with self.subTest(document=document):
                self.assertTrue(first_line.startswith("# "))

    def test_profile_template_has_supported_schema(self):
        profile = yaml.safe_load(PROFILE_TEMPLATE.read_text())

        self.assertEqual(profile["version"], 1)
        self.assertEqual(
            set(profile),
            {"version", "bootstrap", "validation", "worktree", "ci", "publication"},
        )
        self.assertIsInstance(profile["bootstrap"]["steps"], list)
        self.assertIsInstance(profile["validation"]["quick"], list)
        self.assertIsInstance(profile["validation"]["full"], list)
        self.assertIsInstance(profile["worktree"]["required_local_files"], list)
        self.assertIsInstance(profile["worktree"]["notes"], list)

        steps = (
            profile["bootstrap"]["steps"]
            + profile["validation"]["quick"]
            + profile["validation"]["full"]
        )
        for step in steps:
            with self.subTest(step=step):
                self.assertEqual(set(step), {"runtime", "run", "env", "needs"})
                self.assertIsInstance(step["env"], dict)
                self.assertIsInstance(step["needs"], list)


if __name__ == "__main__":
    unittest.main()
