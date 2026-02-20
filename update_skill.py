#!/usr/bin/env python3
"""
Script to update the Team consensus skill configuration and changelog.

This script performs the following:
- Updates config.json with default settings, preserving user changes.
- Increments the version in SKILL.md and adds a new changelog entry.
"""

import json
import os
import sys
import datetime
import re
import shutil


def parse_version(version_str):
    """
    Parse a version string like '1.2.3' into a tuple (1, 2, 3).

    Pads with zeros if fewer than 3 parts.
    """
    parts = [int(p) for p in re.split(r'\.', version_str) if p] + [0, 0]
    return tuple(parts[:3])


def update_config(config_path, default_config):
    """
    Update the config.json file with defaults, preserving existing settings.
    """
    config = default_config.copy()

    if os.path.exists(config_path):
        backup_path = config_path + '.bak'
        shutil.copy2(config_path, backup_path)
        print(f"Backup created: {backup_path}")

        try:
            with open(config_path, 'r') as f:
                existing_config = json.load(f)
            # Merge defaults with existing (existing takes precedence)
            config.update(existing_config)
            print("Existing config preserved and updated with new defaults.")
        except json.JSONDecodeError:
            print("Warning: Existing config.json invalid. Using defaults.")
        except Exception as e:
            print(f"Warning: Error reading config.json: {e}. Using defaults.")

    # Write the config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print("Team skill updated successfully. Config saved to config.json.")


def update_changelog(skill_path, summary="Auto skill update"):
    """
    Update the changelog in SKILL.md with a new version entry.
    """
    with open(skill_path, 'r') as f:
        content = f.read()

    # Find last version
    version_pattern = r'### Version (\d+(?:\.\d+)*) \(\d{4}-\d{2}-\d{2}\)'
    matches = re.findall(version_pattern, content)

    if matches:
        last_version_str = max(matches, key=parse_version)
        major, minor, patch = parse_version(last_version_str)
        if patch < 9:
            new_version = f"{major}.{minor}.{patch + 1}"
        else:
            new_version = f"{major}.{minor + 1}.0"
    else:
        new_version = "1.0.0"

    # Current date
    today = datetime.date.today().isoformat()

    # New entry
    new_entry = f"\n### Version {new_version} ({today})\n- {summary}\n"

    # Find position to insert: before ## Files
    files_pos = content.find('## Files')
    if files_pos != -1:
        content = content[:files_pos] + new_entry + content[files_pos:]
    else:
        content += new_entry

    # Write back
    with open(skill_path, 'w') as f:
        f.write(content)

    print(f"Updated SKILL.md to version {new_version} with summary: {summary}")


def test_parse_version():
    """Test the parse_version function."""
    assert parse_version("1.0.0") == (1, 0, 0)
    assert parse_version("1.2") == (1, 2, 0)
    assert parse_version("2.0.1") == (2, 0, 1)
    print("All tests passed.")


def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    skill_path = os.path.join(os.path.dirname(__file__), 'SKILL.md')

    default_config = {
        "num_reviewers": 3,
        "enable_discussion": True,
        "voting_threshold": 0.7,
        "max_reviewers": 5,
        "timeout_minutes": 10,
        "max_iterations": 1,
        "status_update_interval_minutes": 5,
        "composition": {"code-agent": 3}
    }

    update_config(config_path, default_config)

    summary = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else "Auto skill update"
    update_changelog(skill_path, summary)


if __name__ == "__main__":
    main()
    test_parse_version()