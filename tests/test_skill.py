from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "omakase" / "SKILL.md"
METADATA = ROOT / "skills" / "omakase" / "agents" / "openai.yaml"
PROJECT_GUIDANCE = (
    ROOT / "skills" / "omakase" / "references" / "project-guidance.md"
)
REPOSITORY_CONVENTIONS = (
    ROOT / "skills" / "omakase" / "references" / "repository-conventions.md"
)
PROFILE_TEMPLATE = (
    ROOT / "skills" / "omakase" / "assets" / "omakase.local.example.yml"
)
PROFILE_RESOLVER = ROOT / "skills" / "omakase" / "scripts" / "profile_path.py"


class OmakaseSkillContractTest(unittest.TestCase):
    def test_skill_encodes_the_conductor_contract(self):
        text = SKILL.read_text()

        required_fragments = (
            "name: omakase",
            "Hybrid trigger",
            "Do not trigger",
            "one-off",
            "diagnosis",
            "worktree",
            "Superpowers",
            "GitHub",
            "repository-approved integrations",
            "scheduled follow-up",
            "CI",
            "review feedback",
            "Attention policy",
            "Completion",
            "references/project-guidance.md",
            ".omakase.local.yml",
            "scripts/profile_path.py",
            "primary checkout",
            "durable and reproducible",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_skill_has_desktop_metadata_and_project_profile_resources(self):
        metadata = METADATA.read_text()
        guidance = PROJECT_GUIDANCE.read_text()

        self.assertIn('display_name: "Omakase"', metadata)
        self.assertIn("default_prompt:", metadata)
        self.assertIn("# Personal project profile", guidance)
        self.assertIn("globally ignored", guidance)
        self.assertIn("established repository entry points", guidance)
        self.assertTrue(PROFILE_TEMPLATE.is_file())
        self.assertTrue(PROFILE_RESOLVER.is_file())

    def test_profile_template_selects_runtime_per_bootstrap_step(self):
        profile = yaml.safe_load(PROFILE_TEMPLATE.read_text())

        self.assertNotIn("runtime", profile)
        self.assertEqual(
            profile["bootstrap"]["steps"],
            [{"runtime": None, "run": None}],
        )
        self.assertEqual(
            profile["validation"]["quick"],
            [{"runtime": None, "run": None}],
        )

    def test_skill_avoids_redundant_approval_and_serial_waits(self):
        text = SKILL.read_text()

        self.assertIn("does not require a second approval", text)
        self.assertIn("materially diverges", text)
        self.assertIn("continue non-dependent", text)
        self.assertIn("background baseline", text)

    def test_skill_defaults_to_a_lean_cost_aware_review_cycle(self):
        text = SKILL.read_text()
        metadata = METADATA.read_text()

        required_fragments = (
            "Lean review by default",
            "Implement directly in the main agent",
            "For every project change intended to land, request one independent review",
            "at most one scoped re-review, and only when material findings required fixes",
            "Do not invoke `superpowers:subagent-driven-development` merely because a plan can be split into tasks",
            "user requests an exhaustive workflow",
            "repository policy requires it",
            "scale and risk justify the additional model consumption",
            "For every subagent dispatch, set both the model and reasoning effort explicitly",
            "cheapest capable tier for mechanical work",
            "balanced mid-tier for implementation from prose or ordinary review",
            "most capable tier",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

        self.assertIn("lean review cycle", metadata)

    def test_skill_uses_predictable_worktrees_and_exclusive_bootstrap(self):
        text = SKILL.read_text()
        guidance = PROJECT_GUIDANCE.read_text()

        self.assertIn("<primary-checkout>/.worktrees/<task-slug>", text)
        self.assertIn("exclusive operation", text)
        self.assertIn("untrusted", guidance)
        self.assertIn("clean deterministic", guidance)

    def test_skill_avoids_predictable_bootstrap_retries(self):
        text = SKILL.read_text()
        guidance = PROJECT_GUIDANCE.read_text()

        required_skill_fragments = (
            "profile owns project setup and validation",
            "use only its environment-detection and workspace-isolation steps",
            "Do not execute the isolation workflow's generic project-setup or baseline-verification steps",
            "Before the first dependency-tree mutation",
            "cache and log directories are writable",
            "known to require unavailable sandbox network access",
            "one correctly configured attempt",
        )
        for fragment in required_skill_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

        required_guidance_fragments = (
            "failure and retry boundaries",
            "repository-supported phase-specific commands or flags",
            "Do not decompose a canonical entry point into invented shell setup",
            "resume at the failed profile step",
        )
        for fragment in required_guidance_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, guidance)

    def test_skill_preflights_expensive_validation_execution_context(self):
        text = SKILL.read_text()
        guidance = PROJECT_GUIDANCE.read_text()

        required_skill_fragments = (
            "Before each expensive validation command",
            "localhost sockets, browser processes, external services, or network access",
            "correct execution context on the first run",
        )
        for fragment in required_skill_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

        self.assertIn("Stable harness constraint", guidance)
        self.assertIn("worktree.notes", guidance)
        self.assertIn("one-off sandbox denial", guidance)
        self.assertIn("Do not encode transient outages, one-off sandbox failures", text)

    def test_full_validation_prepares_ignored_generated_artifacts(self):
        text = SKILL.read_text()
        guidance = PROJECT_GUIDANCE.read_text()

        self.assertIn("full validation as self-preparing", text)
        self.assertIn("ignored generated artifacts", guidance)
        self.assertIn("A clean Git status does not prove", guidance)

    def test_skill_discovers_and_preserves_repository_conventions(self):
        text = SKILL.read_text()
        guidance = REPOSITORY_CONVENTIONS.read_text()

        required_skill_fragments = (
            "references/repository-conventions.md",
            "before naming a branch or composing a commit or pull request",
            "artifact-specific",
            "Do not assume that a commit-message convention also applies to pull-request titles",
        )
        for fragment in required_skill_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

        required_guidance_fragments = (
            "# Repository conventions",
            "Explicit policy",
            "Recent accepted examples",
            "human-authored",
            "mixed or weak",
            "Branch names",
            "Commit subjects",
            "Pull-request titles",
            "Pull-request bodies",
            "Review replies",
            "required platform prefix",
            "read the created or updated artifact back",
        )
        for fragment in required_guidance_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, guidance)


if __name__ == "__main__":
    unittest.main()
