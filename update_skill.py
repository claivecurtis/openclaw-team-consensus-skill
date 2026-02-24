#!/usr/bin/env python3
"""
Script to update the Team consensus skill configuration and changelog.

This script performs the following:
- Updates config.json with default settings, preserving user changes.
- Increments the version in SKILL.md and adds a new changelog entry.
"""

# Update Team skill config and changelog with backups & semantic versioning

# Update Team skill config and changelog with backups & semantic versioning

import json
import os
import sys
import datetime
import re
import shutil

config_path = os.path.join(os.path.dirname(__file__), "config.json")
skill_path = os.path.join(os.path.dirname(__file__), "SKILL.md")

# Default config
config = {
    "num_reviewers": 3,
    "enable_discussion": True,
    "voting_threshold": 0.7,
    "max_reviewers": 5,
    "timeout_minutes": 10,
    "max_iterations": 1,
    "status_update_interval": 5,
    "composition": {"code-agent": 3},
}

def validate_config(c):
    if not isinstance(c.get("num_reviewers", 3), int) or not 1 <= c.get("num_reviewers", 3) <= c.get("max_reviewers", 5):
        raise ValueError("num_reviewers must be int 1-5")
    if not isinstance(c.get("voting_threshold", 0.7), float) or not 0 <= c.get("voting_threshold", 0.7) <= 1:
        raise ValueError("voting_threshold must be float 0-1")
    if not isinstance(c.get("timeout_minutes", 10), int) or c.get("timeout_minutes", 10) < 1:
        raise ValueError("timeout_minutes must be int >=1")
    if not isinstance(c.get("max_iterations", 1), int) or c.get("max_iterations", 1) < 1:
        raise ValueError("max_iterations must be int >=1")
    if not isinstance(c.get("status_update_interval", 5), int) or c.get("status_update_interval", 5) < 1:
        raise ValueError("status_update_interval must be int >=1")
    if "enable_discussion" in c and not isinstance(c["enable_discussion"], bool):
        raise ValueError("enable_discussion must be bool")

# Backup existing config if present
if os.path.exists(config_path):
    backup_path = config_path + ".bak"
    shutil.copy2(config_path, backup_path)
    print(f"Backup created: {backup_path}")

    try:
        with open(config_path, "r") as f:
            existing_config = json.load(f)
        # Merge defaults with existing (existing wins)
        config.update(existing_config)
        print("Existing config merged with defaults.")
        validate_config(config)
    except json.JSONDecodeError:
        print("Invalid config.json. Using backup/defaults.")
        validate_config(config)
    except Exception as e:
        print(f"Config read error: {e}. Using backup/defaults.")
        validate_config(config)

# Write updated config
with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print("Config saved: config.json")

# Update changelog in SKILL.md
with open(skill_path, "r") as f:
    content = f.read()

# Extract versions
version_pattern = r"### Version (\\d+(?:\\.\\d+)*) \\(\\d{{4}}-\\d{{2}}-\\d{{2}}\\)"
matches = re.findall(version_pattern, content)


def parse_version(v):
    """Parse v1.2 → (1,2,0), pad to major.minor.patch"""

    parts = [int(p) for p in v.split(".") if p.strip()]
    parts += [0] * (3 - len(parts))
    return tuple(parts[:3])


if matches:
    last_v_str = max(matches, key=parse_version)
    major, minor, patch = parse_version(last_v_str)
    # Increment patch; roll to minor if patch == 9 (rare)
    if patch < 9:
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        new_version = f"{major}.{minor + 1}.0"
else:
    new_version = "1.0.0"

today = datetime.date.today().isoformat()

# Summary from args or default
summary = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Auto skill update"

new_entry = f"\n### Version {new_version} ({today})\n- {summary}\n"

# Check for idempotency: if summary already in latest entry, skip
if matches:
    last_v_str = max(matches, key=parse_version)
    last_entry_pos = content.find(f"### Version {last_v_str}")
    next_entry_pos = content.find("### Version", last_entry_pos + 1)
    if next_entry_pos == -1:
        next_entry_pos = len(content)
    last_entry = content[last_entry_pos:next_entry_pos]
    if summary in last_entry:
        print("Summary already in latest changelog entry. Skipping changelog update.")
        new_entry = ""

# Insert before '## Files'
files_pos = content.find("## Files")
if files_pos != -1:
    if new_entry:
        content = content[:files_pos] + new_entry + content[files_pos:]
else:
    if new_entry:
        content += new_entry

with open(skill_path, "w") as f:
    f.write(content)

print(f"SKILL.md → v{new_version}: {summary}")
