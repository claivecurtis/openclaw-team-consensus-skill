#!/bin/bash

# Universal skill directory check script
# Uses environment variables for customization

WORKSPACE=${WORKSPACE:-$HOME/.openclaw/workspace}
SKILLS_DIR=$WORKSPACE/skills
DATE=$(date +%Y-%m-%d)
LOG_FILE=$WORKSPACE/memory/$DATE.md

# Default skills to check; can be overridden by SKILLS_LIST env var
DEFAULT_SKILLS=("openclaw-team-consensus-skill" "openclaw-proxmox-api-skill" "teamspeak")
SKILLS=(${SKILLS_LIST:-"${DEFAULT_SKILLS[@]}"})

echo "Skill dir check started at $(date)" >> $LOG_FILE

for SKILL in "${SKILLS[@]}"; do
    DIR=$SKILLS_DIR/$SKILL
    if [ ! -d "$DIR" ]; then
        echo "Cloning $SKILL" >> $LOG_FILE
# Set REPO_OWNER env var (e.g., claivecurtis) or per-skill via custom logic
        REPO_OWNER=${REPO_OWNER:-claivecurtis}
        git clone https://github.com/$REPO_OWNER/$SKILL $DIR >> $LOG_FILE 2>&1
    else
        echo "Pulling $SKILL" >> $LOG_FILE
        cd $DIR && git fetch origin && git merge origin/main --ff-only >> $LOG_FILE 2>&1 || echo "Pull failed for $SKILL" >> $LOG_FILE
    fi
done

echo "Skill dir check completed at $(date)" >> $LOG_FILE