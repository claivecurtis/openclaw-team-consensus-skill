# ROADMAP.md - API Reference for Team Consensus Skill

## Configuration API

The skill uses a JSON configuration file `config.json` with the following options:

- `num_reviewers`: Number of reviewer sub-agents (integer, 1-5)
- `enable_discussion`: Enable discussion synthesis phase (boolean)
- `voting_threshold`: Minimum approval ratio for consensus (float, 0.0-1.0)
- `max_reviewers`: Maximum number of reviewers (integer, default 5)
- `timeout_minutes`: Timeout for sub-agent responses (integer, >=1)
- `max_iterations`: Maximum review iterations (integer, >=1)
- `status_update_interval`: Interval in minutes for status updates (integer, >=1)
- `composition`: Dictionary of agent types and counts (e.g., {"code-agent": 2})
- `auto_select_team`: Enable automatic team selection (boolean)
- `enable_agent_reconfig`: Allow reconfiguring agents (boolean)
- `test_mode`: Simulate workflow without real spawns (boolean)

## Usage API

To use the skill, invoke with task description, and it will spawn reviewers, collect feedback, apply changes, and vote for consensus.

## Future Roadmap

- Integrate with more agent types from AGENTS.md
- Add advanced validation for all config options
- Implement visual UI for configuration and progress tracking
- Support hierarchical spawning for large teams
- Add export features for feedback and decisions
- Improve error handling and recovery