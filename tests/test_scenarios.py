from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "evals" / "scenarios.md"
SCENARIO_ID = re.compile(r"OMK-[A-Z]+-[0-9]{3}")
AREAS = {
    "bootstrap",
    "conventions",
    "isolation",
    "planning",
    "profile",
    "publication",
    "triggering",
    "validation",
    "visual",
}


class ScenarioCatalogTest(unittest.TestCase):
    def setUp(self):
        self.text = SCENARIOS.read_text()
        _, frontmatter, body = self.text.split("---", 2)
        self.metadata = yaml.safe_load(frontmatter)
        body_lines = body.splitlines()
        table_start = next(
            index for index, line in enumerate(body_lines) if line.strip().startswith("|")
        )
        self.table_lines = []
        for line in body_lines[table_start:]:
            if not line.strip():
                break
            self.table_lines.append(line)
        self.rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in self.table_lines[2:]
        ]

    def test_catalog_is_explicitly_manual(self):
        self.assertEqual(
            self.metadata,
            {"kind": "behavioral-reference", "automated": False},
        )

    def test_scenarios_have_unique_stable_ids_and_known_areas(self):
        header = [
            cell.strip()
            for cell in self.table_lines[0].strip().strip("|").split("|")
        ]
        self.assertEqual(header, ["ID", "Area", "Prompt or situation", "Expected behavior"])
        self.assertRegex(
            self.table_lines[1].strip(), r"^\|(?:\s*:?-{3,}:?\s*\|){4}$"
        )
        self.assertTrue(self.rows)
        ids = [row[0] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({row[1] for row in self.rows}, AREAS)

        for line, row in zip(self.table_lines[2:], self.rows):
            with self.subTest(row=row):
                self.assertTrue(line.strip().startswith("|"))
                self.assertTrue(line.strip().endswith("|"))
                self.assertEqual(len(row), 4)
                self.assertIsNotNone(SCENARIO_ID.fullmatch(row[0]))
                self.assertIn(row[1], AREAS)
                self.assertTrue(row[2])
                self.assertTrue(row[3])


if __name__ == "__main__":
    unittest.main()
