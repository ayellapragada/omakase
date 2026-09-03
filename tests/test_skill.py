from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "omakase"
SKILL = SKILL_ROOT / "SKILL.md"
METADATA = SKILL_ROOT / "agents" / "openai.yaml"
PROJECT_GUIDANCE = SKILL_ROOT / "references" / "project-guidance.md"
REPOSITORY_CONVENTIONS = (
    SKILL_ROOT / "references" / "repository-conventions.md"
)
PROFILE_TEMPLATE = SKILL_ROOT / "assets" / "omakase.local.example.yml"
PROFILE_RESOLVER = SKILL_ROOT / "scripts" / "profile_path.py"


class OmakaseSkillContractTest(unittest.TestCase):
    def assert_contains_all(self, text, fragments):
        for fragment in fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_frontmatter_has_discriminating_trigger(self):
        _, frontmatter, _ = SKILL.read_text().split("---", 2)
        data = yaml.safe_load(frontmatter)

        self.assertEqual(data["name"], "omakase")
        self.assert_contains_all(
            data["description"],
            ("intended to land", "one-off scripts", "read-only", "diagnosis-only"),
        )

    def test_entrypoint_is_concise_and_routes_to_focused_references(self):
        text = SKILL.read_text()

        self.assertLessEqual(len(text.split()), 1600)
        self.assert_contains_all(
            text,
            (
                "references/project-guidance.md",
                "references/repository-conventions.md",
                "assets/omakase.local.example.yml",
                "scripts/profile_path.py",
            ),
        )

    def test_entrypoint_preserves_delivery_contract(self):
        text = SKILL.read_text()

        self.assert_contains_all(
            text,
            (
                "Superpowers",
                "GitHub",
                "Grim",
                "Lean review",
                "model and reasoning effort",
                "attention request",
                "<primary-checkout>/.worktrees/<task-slug>",
                "does not require a second approval",
                "scheduled follow-up",
                "CI failures",
                "review feedback",
                "Completion",
            ),
        )

    def test_profile_resources_and_metadata_are_present(self):
        metadata = METADATA.read_text()
        guidance = PROJECT_GUIDANCE.read_text()

        self.assert_contains_all(metadata, ('display_name: "Omakase"', "default_prompt:"))
        self.assertIn("# Personal project profile", guidance)
        self.assertTrue(PROFILE_TEMPLATE.is_file())
        self.assertTrue(PROFILE_RESOLVER.is_file())

    def test_profile_template_selects_runtime_per_step(self):
        profile = yaml.safe_load(PROFILE_TEMPLATE.read_text())

        self.assertNotIn("runtime", profile)
        self.assertEqual(profile["bootstrap"]["steps"], [{"runtime": None, "run": None}])
        self.assertEqual(profile["validation"]["quick"], [{"runtime": None, "run": None}])

    def test_operational_mechanics_live_in_project_guidance(self):
        skill = SKILL.read_text()
        guidance = PROJECT_GUIDANCE.read_text()
        operational_details = (
            "package-manager cache and log directories",
            "localhost sockets, browser processes, external services, or network access",
            "mutation of one dependency tree as an exclusive operation",
        )

        for detail in operational_details:
            with self.subTest(detail=detail):
                self.assertNotIn(detail, skill)
                self.assertIn(detail, guidance)

        self.assert_contains_all(
            guidance,
            (
                "failure and retry boundaries",
                "clean deterministic install or bootstrap command",
                "ignored generated artifacts",
                "Stable harness constraint",
                "one-off sandbox denial",
            ),
        )

    def test_repository_conventions_remain_artifact_specific(self):
        guidance = REPOSITORY_CONVENTIONS.read_text()

        self.assert_contains_all(
            guidance,
            (
                "Explicit policy",
                "Recent accepted examples",
                "Branch names",
                "Commit subjects",
                "Pull-request titles",
                "Pull-request bodies",
                "Review replies",
                "required platform prefix",
                "read the created or updated artifact back",
            ),
        )


if __name__ == "__main__":
    unittest.main()
