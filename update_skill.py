#!/usr/bin/env python3

import json
import os
import sys
import datetime
import re

# Update Team skill config and changelog

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
skill_path = os.path.join(os.path.dirname(__file__), 'SKILL.md')

config = {
    "num_reviewers": 3,
    "enable_discussion": True,
    "voting_threshold": 0.7,
    "max_reviewers": 5,
    "timeout_minutes": 10,
    "max_iterations": 1,
    "status_update_interval_minutes": 5,
    "composition": {"code-agent": 3}
}

# Check if config exists and preserve user changes if present
if os.path.exists(config_path):
    try:
        with open(config_path, 'r') as f:
            existing_config = json.load(f)
        # Merge existing with defaults, preferring existing
        config.update(existing_config)
        print("Existing config preserved and updated with new defaults.")
    except json.JSONDecodeError:
        print("Warning: Existing config.json is invalid. Overwriting with defaults.")
    except Exception as e:
        print(f"Warning: Error reading config.json: {e}. Overwriting with defaults.")

# Write the config
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("Team skill updated successfully. Config saved to config.json.")

# Update SKILL.md changelog
with open(skill_path, 'r') as f:
    content = f.read()

# Find last version
matches = re.findall(r'### Version (\d+\.\d+) \(\d{4}-\d{2}-\d{2}\)', content)
if matches:
    last_version = max(float(v) for v in matches)
    major = int(last_version)
    minor = int(round((last_version - major) * 10))
    new_minor = minor + 1
    new_version = f"{major}.{new_minor}"
else:
    new_version = "1.0"

# Current date
today = datetime.date.today().isoformat()

# Summary
if len(sys.argv) > 1:
    summary = ' '.join(sys.argv[1:])
else:
    summary = "Routine config update"

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
