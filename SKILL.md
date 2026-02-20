---\nname: team\ndescription: Spawn team of reviewer sub-agents for consensus on tasks/outputs/code. Use when: multi-agent review, validation, decision-making workflows.\n---\n\n# Team Skill

## Description

The Team skill allows an agent to spawn a team of reviewer sub-agents to achieve consensus on prompts or outputs. It features a configurable workflow including spawning reviewers, collecting feedback, optional discussion, applying changes, and voting for consensus.

## Features

- Configurable number of reviewers (default: 3, max: 5)
- Efficient asynchronous spawning and collection with timeouts (default: 10 minutes)
- Optional discussion synthesis or lightweight summarization
- Voting-based consensus with threshold and options for partial consensus
- Customizable review criteria and prompts
- Metrics logging for optimization
- Scalable for larger teams with caching and reuse
- Periodic status updates every 5 minutes during skill use via cron
- On-demand config confirmation before team formation
- Flexible team composition with mixed agent types
- Comprehensive change log for version history
- Proactive timeout handling: spawn runTimeoutSeconds=300 (5min), poll subagents list every 1min, steer/kill >timeout, fast models (grok-fast-reason low thinking), task chunk if long. Fails consensus early.
- Dynamic config overrides via runtime user input
- Proactive timeout monitoring with early warnings
- Metrics logging to team_metrics.json for review time and consensus rate
- Flexible composition with percentages/weights and separate voter composition
- Visual UI for config interfaces and progress dashboards using canvas tool
- Push-based notifications via message tool for real-time status
- Review criteria customization in initial prompts
- Iterative reviews with learning from failures
- Tool integration mode for reviewers (e.g., web_search, exec)
- Parallel workflows for large items
- Feedback export and archiving to Markdown files
- Scalability for large teams with hierarchical spawning
- Consensus alternatives like majority wins or expert override
- Agent specialization with roles and custom prompts
- Version control integration via exec for git-commits post-consensus

## Workflow Diagram

```
Start
  |
  v
Set up Cron for Status Updates (every 5 min)
  |
  v
Prompt All Config Options (with user confirmation)
  |
  v
Select Agent Composition (mix agent types, e.g., 2 code-agent, 1 other)
  |
  v
Spawn Reviewers --> Collect Feedback (push-based)
  |                    |
  |<-------------------+
  v
Discussion (if enabled) --> Synthesize Feedback
  |
  v
Apply Changes
  |
  v
Spawn Voters --> Vote on Changes
  |              |
  |<-------------+
  v
Consensus? (threshold met)
  |     |
  Yes   No --> Notify User / Iterate
  |
  v
Remove Cron
  |
  v
End
```
  v
End
```

## Workflow

1. **Set up Cron for Status Updates**: At the start of skill use, set up a cron job to send status updates every 5 minutes via periodic status messages. Use the complete job object: run `openclaw cron add --name "team-status-<session_id>" --every "5m" --message "Provide a status update on the ongoing Team skill process, including current progress, number of reviewers spawned, feedback collected, etc." --agent "<current_agent_id>" --announce --to "<channel_id>" --session "isolated" --timeout-seconds 30`. If the job object is invalid (e.g., missing name or message), retry with correct parameters.

2. **Prompt for All Configuration**: Present all config options on-demand (num_reviewers, enable_discussion, voting_threshold, status_update_interval, etc.) and require user confirmation before proceeding.

3. **Select Agent Composition**: Allow user to specify the composition of agent types for the team (e.g., 2 code-agent, 1 other-agent), using available agents from `agents_list` with their models from `session_status`. Validate that the total does not exceed max_reviewers and that agents are allowed.

4. **Spawning Reviewers**: The agent uses the `subagents` tool to spawn the specified number and types of reviewer sub-agents according to the composition. Each is tasked with reviewing the provided item according to the task description. If spawning fails, retry up to 2 times. If all retries fail, terminate the team skill activity, notify the user, and remove the cron job.

5. **Collecting Feedback**: Feedback is collected from each reviewer as they complete their task (push-based notifications via system messages). If a sub-agent fails to provide feedback within timeout, mark as failed and proceed with available feedback.

6. **Discussion**: If enabled, a discussion sub-agent is spawned to synthesize the collected feedback into a cohesive summary. If spawning fails, skip discussion and proceed with raw feedback.

7. **Changes**: The agent reviews the feedback/discussion and makes necessary changes to the item.

8. **Voting**: Voting sub-agents are spawned to vote on the changes. Consensus is reached if the voting threshold is met. If spawning fails, use available voters or default to approval.

9. **Remove Cron**: At the end of the process, remove the cron job using `openclaw cron rm --name "team-status-<session_id>"`. If removal fails, log the error but do not fail the process.

## Configuration

The skill uses a config.json file for default settings, but when invoked, dynamically presents all options on-demand and requires user confirmation before forming the team:

- num_reviewers: Number of reviewer sub-agents (default: 3, max: 5)
- enable_discussion: Enable discussion synthesis phase (default: true)
- voting_threshold: Minimum approval ratio for consensus (default: 0.7)
- timeout_minutes: Timeout for sub-agent responses (default: 5)
- max_iterations: Maximum review iterations if consensus fails (default: 1)
- status_update_interval: Interval in minutes for periodic status updates during skill use (default: 5)
- agent_composition: Dictionary specifying the number of each agent type (e.g., {"code-agent": 2, "other-agent": 1}) (default: {"code-agent": 3})

Users can provide personalized overrides during prompting to tailor the process.

## Setup Agent Efficiency Cron

To maintain optimal agent performance, set up a periodic cron job for agent efficiency review. This cron will spawn a Team skill session to review and update the AGENTS.md table with current efficiency metrics, best uses, and notes.

### Steps to Setup:
1. Use the `openclaw cron add` command to create a recurring job:
   - Name: "agent-efficiency-review"
   - Schedule: Weekly (e.g., every Sunday at 9 AM)
   - Payload: Run Team skill to review agents and update AGENTS.md table
   - Announce to primary channels

Example command:
```
openclaw cron add --name "agent-efficiency-review" --every "7d" --message "Use Team skill to review agent efficiency and update AGENTS.md table with summaries/best uses/cost-speed metrics." --agent "code-agent" --announce --to "primary-channels" --session "isolated" --timeout-seconds 600
```

This ensures the AGENTS.md table remains current with agent efficiency data.

## Sub-Agent Composition

When using the skill, the agent pulls the list of available agents using the `agents_list` tool and displays them with their default models (queried via `session_status`). The user can specify the composition by assigning numbers to each agent type, e.g., 2 code-agent, 1 other-agent. The total should not exceed max_reviewers.

Refer to AGENTS.md efficiency table for suggestions on best agents for consensus tasks.

### Example Agent Efficiency Table

| Agent/Skill       | Model/Alias          | Best For                          | Efficiency Notes                      |
|-------------------|----------------------|-----------------------------------|---------------------------------------|
| grok-fast-reason | xai/grok-4-1-fast   | General reasoning/chat           | Default: Fast, low tokens            |
| code-agent        | (coding specialist) | Code/shell/CLI tasks             | Code opt: Precise scripting/PRs      |
| gem3-flash        | google/gemini-1.5-flash | Quick/light tasks            | Flash speed, low cost                |
| grok-4-full       | xai/grok-4          | Heavy analysis/complex           | Full cap: High think, higher cost    |
| Team skill        | Multi-agent (workspace/skills/openclaw-team-consensus-skill) | Consensus/meetings/reviews | Low-conf/critical: Spawn agents (e.g., code + grok-4) |

## Usage

1. Run `python3 skills/Team/update_skill.py [optional summary]` to update the config and append a new version to the changelog.

2. To use the skill, the agent follows the workflow steps: sets up cron for status updates, prompts all config options with confirmation, allows specifying agent composition, spawns reviewers per composition, collects feedback, handles discussion/voting, and removes cron at end.

## Examples

**Sample Scenario: Reviewing a Code Snippet**

- User: "Use Team skill to review this Python function for bugs and improvements."
- Agent prompts all options: "Number of reviewers? [3]" → 3; "Enable discussion? [true]" → true; "Status update interval? [5]" → 5; "Agent composition? [code-agent:3]" → 2 code-agent, 1 other-agent; User confirms.
- Sets up cron for status every 5 min.
- Spawns 2 code-agent and 1 other-agent reviewers with task: "Review this function: def add(a, b): return a + b  # for bugs and suggestions."
- Collects feedback (e.g., "No bugs, but add type hints. Rating: 4/5")
- Spawns discussion: Synthesizes into "Minor improvements needed."
- Applies changes: Edits function to def add(a: int, b: int) -> int: return a + b
- Spawns voters: All approve → Consensus reached.
- Removes cron.

## Error Handling

- If `agents_list` returns no agents, fallback to the default 'code-agent'.
- If spawning sub-agents fails, retry up to 2 times. If all retries fail, terminate the team skill activity, notify the user of the failure, and remove the cron job to prevent orphaned jobs.
- If discussion or voting phases encounter errors (e.g., spawn failures), use available feedback or default to approval to maintain progress, but log the errors.
- For agent allowance issues, ensure agents are called with correct parameters and retry if they do not respond initially to confirm they work when called.
- Timeouts prevent hangs; partial consensus allows proceeding with majority changes.
- On any critical error after start (e.g., agent spawn failures), implement termination method: kill any spawned sub-agents, remove cron, and notify user.
- On any error after skill start (including agent spawn failures), immediately terminate team skill activity: remove the status update cron job, kill any active sub-agents, and notify the user of the error and termination.
- Ensure agent allowance: Before spawning, verify the agent is available via `agents_list`; if not, fallback to allowed agents or abort with notification.

## Change Log

### Version 1.1 (2026-02-18)
- Added workflow diagram for visual clarity.
- Enhanced features: max reviewers (5), timeouts (10 min), partial consensus.
- Expanded config: max_reviewers, timeout_minutes, max_iterations.
- Added examples section with sample scenario.
- Improved error handling: retries, fallbacks, timeouts.
- Updated config.json with new fields.

### Version 1.2 (2026-02-18)
- Added status updates every 5 minutes during skill use using cron for periodic status messages.
- Ensured on-demand presentation of all config options before forming the team, with user confirmation.
- Allowed selecting and mixing agent types for team composition (e.g., specify numbers per type like 2 code-agent, 1 other).
- Updated SKILL.md, config.json, and init_skill.py to support new features.
- Modified workflow to include cron setup/removal and agent composition selection.
- Updated documentation, examples, and configuration sections accordingly.
- Maintained change log for historical recording of updates.

### Version 1.3 (2026-02-18)
- Modified workflow to propose changes before voting; apply changes only after consensus is reached.
- Updated workflow diagram and steps to reflect proposal-then-vote-apply sequence.
- Ensured changes are not applied without final team approval.

### Version 1.4 (2026-02-18)
- Added proactive timeout handling: Query system agent timeout and fail consensus 1 minute early to prevent sub-agent kills.
- Updated workflow to include deadline monitoring during voting.
- Enhanced robustness against system-level timeouts.

### Version 1.5 (2026-02-18)
- Fixed cron setup documentation: Added complete job object example for status updates and removal command.
- Ensures agents can correctly configure periodic status messages without errors.

#### Cron Job Object Example

To set up the status update cron job, use the `cron.add` tool with the following parameters:

```json
{
  "name": "team-status-update",
  "schedule": {
    "kind": "cron",
    "expr": "*/5 * * * *",
    "tz": "America/New_York"
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "Team skill status update: Check progress on current team activities."
  },
  "deleteAfterRun": false
}
```

To remove the cron job after completion, use `cron.remove` with `jobId` of the created job.

### Version 1.6 (2026-02-18)
- Consolidated duplicate change log entries and corrected workflow diagram syntax.
- Improved config initialization with checks to preserve user changes and fallback logic for composition.
- Added composition validation, detailed cron setup/removal, and enhanced error handling with logging/notifications.
- Introduced dynamic config overrides, proactive timeout monitoring with early warnings, metrics logging to team_metrics.json.
- Added flexible composition/voting with percentages/weights, visual UI for configs/dashboards using canvas, push-based notifications via message.
- New features: Review criteria customization, iterative learning with >1 iterations, tool integration mode, parallel workflows, feedback export/archiving, scalability for large teams (hierarchical spawning), consensus alternatives (majority wins), agent specialization with roles, version control integration via exec.
- Updated features list, workflow steps, and documentation for all enhancements.

### Version 1.7 (2026-02-18)
- Resolved cron issue by specifying complete job object with all required parameters (name, schedule via --every, message, agent, announce, to, session, timeout-seconds) to prevent invalid job object errors.
- Implemented method to terminate team skill activity on errors after start, including agent spawn failures: retry spawns up to 2 times, if fail, kill spawned sub-agents, remove cron, notify user.
- Implemented fix to prevent agent allowance issues by validating agent availability before spawning and ensuring agents work when called via retries and parameter checks.
- Enhanced error handling: Added automatic termination of team skill activity on errors after start, including agent spawn failures—removes cron job, kills active sub-agents, and notifies user.
- Improved agent allowance fixes: Ensures agents work when called by verifying availability before spawning and providing fallbacks or aborts with notifications.


### Version 1.8 (2026-02-19)
- Test update to verify changelog appending

### Version 1.9 (2026-02-19)
- Implemented proper versioning and changelog management: Renamed init_skill.py to update_skill.py, added logic to auto-increment version, append new changelog entry with date and summary without altering previous entries. Updated SKILL.md to reference the new script. This fixes overwriting, same version numbers, and merging issues by enforcing append-only history.

### Version 2.0 (2026-02-19)
- Added best practices files: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, .github templates
- Preconfigured team composition from AGENTS.md table: Set default composition to code-agent heavy for consensus.
- Added skill prompt reconfig options: Introduced enable_agent_reconfig config option to allow reconfiguring agent efficiency during processes.
- Added public section 'Setup Agent Efficiency Cron': Describes setup of periodic cron for agent efficiency review, updating AGENTS.md table using Team skill.

### Version 2.1 (2026-02-19)
- Removed hardcoded agent compositions; default to generic code-agent only to avoid user-specific hardcodes.
- Updated agent efficiency cron to use generic code-agent instead of specific models.
- Added reference to AGENTS.md efficiency table for agent selection suggestions.
- Sanitized for general users by removing personalized agent references.
## Files

- SKILL.md: This documentation

- update_skill.py: Update script to manage config and changelog

- config.json: Configuration file

### Version 2.2 (2026-02-19)
- Robust cron/subagent cleanup: On end/error/timeout/abort, always `subagents action=list` + `kill` lingering; `cron action=list | grep 'team-status'` + `remove <id>` by ID/name pattern. Prevents orphans (e.g., Team skill abrupt end).