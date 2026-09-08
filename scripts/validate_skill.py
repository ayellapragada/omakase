#!/usr/bin/env python3
"""Validate the portable structure of a Codex skill directory."""

from pathlib import Path
import re
import sys

import yaml


ALLOWED_FRONTMATTER_KEYS = {
    "allowed-tools",
    "description",
    "license",
    "metadata",
    "name",
}


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    skill_file = skill_path / "SKILL.md"
    if not skill_file.is_file():
        return False, "SKILL.md not found"

    content = skill_file.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid or missing YAML frontmatter"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return False, f"Invalid YAML in frontmatter: {error}"

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"
    unexpected_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        names = ", ".join(sorted(unexpected_keys))
        return False, f"Unexpected frontmatter key(s): {names}"
    for required_key in ("name", "description"):
        if required_key not in frontmatter:
            return False, f"Missing '{required_key}' in frontmatter"

    name = frontmatter["name"]
    if not isinstance(name, str):
        return False, "Skill name must be a string"
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        return False, "Skill name must be hyphen-case"
    if len(name) > 64:
        return False, "Skill name must be 64 characters or fewer"

    description = frontmatter["description"]
    if not isinstance(description, str):
        return False, "Skill description must be a string"
    if description.startswith("[TODO:"):
        return False, "Skill description contains an unfinished TODO"
    if "<" in description or ">" in description:
        return False, "Skill description cannot contain angle brackets"
    if len(description) > 1024:
        return False, "Skill description must be 1024 characters or fewer"

    fence_marker = None
    fence_length = 0
    for line in content[match.end() :].splitlines():
        fence = re.match(
            r"^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$", line
        )
        if fence:
            marker = fence.group(1)
            if fence_marker is None:
                fence_marker = marker[0]
                fence_length = len(marker)
            elif (
                marker[0] == fence_marker
                and len(marker) >= fence_length
                and not fence.group(2).strip()
            ):
                fence_marker = None
                fence_length = 0
            continue
        if fence_marker is None and re.fullmatch(r" {0,3}\[TODO:[^\n]*\][ \t]*", line):
            return False, "Skill instructions contain an unfinished TODO"

    return True, "Skill is valid!"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_skill.py <skill-directory>")
        return 2

    valid, message = validate_skill(Path(sys.argv[1]))
    print(message)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
