# Claw Team Skill 🗡️

Spawn **multi-agent team** for consensus on reviews/tasks/code/PRs.

**GH**: [claivecurtis/openclaw-team-consensus-skill](https://github.com/claivecurtis/openclaw-team-consensus-skill)

## Quick Start

Prompt: \"Use Team skill to review [code/PR/task]\"

**Auto**:
- Config (reviewers 3, timeout 5min).
- Status cron (5min).
- Spawn mixed agents (code-heavy).
- Feedback/discuss/vote/consensus.
- Lead fixes/actions.

## Features

- **Async/parallel**: Push-based, robust timeouts/cleanup.
- **Agents**: code-agent/grok (configurable).
- **Consensus**: Vote threshold, partial OK.
- **Export**: Logs/metrics Markdown.
- **Robust**: Kill crons/subs, no orphans/duplicates.

**Full docs**: [SKILL.md](SKILL.md)

**Contribute**: CONTRIBUTING.mdInstalled. Lint: OK. Formatted.
