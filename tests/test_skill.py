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
VISUAL_PRODUCT_WORK = SKILL_ROOT / "references" / "visual-product-work.md"
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
                "GitHub",
                "repository-approved integrations",
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

    def test_superpowers_is_optional_not_a_dependency(self):
        skill = SKILL.read_text()
        readme = (ROOT / "README.md").read_text()

        self.assert_contains_all(
            skill,
            (
                "Superpowers is optional",
                "does not depend on it",
                "explicitly requests it",
            ),
        )
        self.assertIn("optional", readme.lower())
        self.assertNotIn("superpowers:", skill)

    def test_core_delivery_workflows_are_owned_directly(self):
        text = SKILL.read_text()

        self.assert_contains_all(
            text,
            (
                "create an isolated worktree",
                "proportionate to the change",
                "Review the completed diff against the task",
                "independent review",
                "Inspect the diff and run applicable validation yourself",
            ),
        )

    def test_visual_product_work_is_routed_and_conditional(self):
        text = SKILL.read_text()

        self.assert_contains_all(
            text,
            (
                "references/visual-product-work.md",
                "materially affects the rendered product experience",
                "Do not activate it merely because a change has a frontend file",
            ),
        )
        self.assertTrue(VISUAL_PRODUCT_WORK.is_file())

    def test_visual_product_work_defines_pr_evidence(self):
        guidance = VISUAL_PRODUCT_WORK.read_text()

        self.assert_contains_all(
            guidance,
            (
                "rendered UI, layout, styling, interaction states, or product imagery",
                "Capture the meaningful baseline before implementation",
                "same state, data, viewport, and theme",
                "Consider image generation",
                "Do not generate imagery",
                "independent visual critique",
                "bounded",
                "## Screenshots",
                "descriptive alt text",
                "new surface",
                "temporary delivery artifacts",
                "Do not commit them solely",
                "--attach",
                "pull-request template",
                "Read the published body back",
                "not review-ready",
            ),
        )

    def test_defaults_to_publishing_a_pull_request(self):
        text = SKILL.read_text()

        self.assert_contains_all(
            text,
            (
                "Treat a project change intended to land as authorization to publish",
                "Do not present the branch-finishing options menu",
                "commit only task-related changes",
                "push the task branch",
                "create or update the pull request",
                "explicitly asks to keep the work local",
            ),
        )

    def test_pr_readiness_requires_more_than_green_checks(self):
        text = SKILL.read_text()

        self.assert_contains_all(
            text,
            (
                "current PR state",
                "draft status",
                "mergeability and merge-state",
                "review decision",
                "after changing its base branch",
                "required checks are green or intentionally skipped under repository policy",
                "no merge conflicts or policy blockers",
                "no requested changes or required reviews are outstanding",
                "Concrete blockers",
                "Report blockers",
            ),
        )

    def test_validation_is_proportional_to_change_risk(self):
        text = SKILL.read_text()

        self.assert_contains_all(
            text,
            (
                "Classify the completed diff before choosing validation",
                "documentation-only",
                "cannot affect runtime behavior",
                "skip runtime tests, builds, and CI waiting",
                "documentation-focused checks",
                "workflows, executable configuration, dependencies, schemas, migrations, generated files, or assets",
                "skip-CI convention",
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
        expected_step = {
            "runtime": None,
            "run": None,
            "env": {},
            "needs": [],
        }
        self.assertEqual(profile["bootstrap"]["steps"], [expected_step])
        self.assertEqual(profile["validation"]["quick"], [expected_step])

    def test_profile_steps_capture_execution_requirements_structurally(self):
        guidance = PROJECT_GUIDANCE.read_text()

        self.assert_contains_all(
            guidance,
            (
                "`env`",
                "`needs`",
                "Apply `env` before the first attempt",
                "Request the execution context named by `needs` before the first attempt",
                "Do not duplicate structured step requirements in `worktree.notes`",
            ),
        )

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
