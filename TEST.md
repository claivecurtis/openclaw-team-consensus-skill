# TEST.md - Full Workflow Demo (Test Mode)

## Usage
Set `test_mode: true` in config or prompt to simulate full flow without subagents/cron/costs.

## Example: Code Review Task

**Input Task:** Review `def add(a, b): return a + b` for bugs/improvements.

### 1. Config (defaults)
- num_reviewers: 3
- enable_discussion: true
- auto_select_team: true

### 2. Auto-Analysis & Proposal
Keywords: code/Python → review-agent prio.
**Proposed:** `{"review-agent": 2, "general-agent": 1}`
Approved.

### 3. Mock Reviewers (no spawn)
- review-agent1 *(or equiv.): "Add types/docstring."
- review-agent2: "Solid, edge cases?"
- general-agent *(or equiv.): "Types + tests."

### 4. Discussion Synth
"Consensus: Type hints/docstring; no bugs."

### 5. Proposed Changes
```python
def add(a: int, b: int) -> int:
    """Add two ints."""
    return a + b
```

### 6. Mock Voters: Approve (3/3)

**Success!** Edit TEST.md for your task.