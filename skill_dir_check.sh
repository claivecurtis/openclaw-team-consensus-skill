#!/bin/bash

# Universal skill directory check script
# Uses environment variables for customization

WORKSPACE=${WORKSPACE:?"WORKSPACE env required (e.g., \$HOME/.openclaw/workspace)"}
SKILLS_DIR=$WORKSPACE/skills
DATE=$(date +%Y-%m-%d)
LOG_FILE=$WORKSPACE/memory/$DATE.md

# Required envs (examples below)
: "${SKILLS_LIST:?SKILLS_LIST env required (space-separated skill names)}"
SKILLS=($SKILLS_LIST)

echo "=== Skill Dir Check ($DATE) ===" >> $LOG_FILE
echo "WORKSPACE: $WORKSPACE" >> $LOG_FILE
echo "REPO_OWNER: $REPO_OWNER" >> $LOG_FILE
echo "SKILLS: ${SKILLS[*]}" >> $LOG_FILE
echo "Started at $(date)" >> $LOG_FILE

for SKILL in "${SKILLS[@]}"; do
    DIR=$SKILLS_DIR/$SKILL
    if [ ! -d "$DIR" ]; then
        echo "Cloning $SKILL" >> $LOG_FILE
: "${REPO_OWNER:?REPO_OWNER env required (e.g., claivecurtis or yourusername)}"
        git clone https://github.com/$REPO_OWNER/$SKILL $DIR >> $LOG_FILE 2>&1
    else
        echo "Pulling $SKILL" >> $LOG_FILE
        cd $DIR && git fetch origin && git merge origin/main --ff-only >> $LOG_FILE 2>&1 || echo "Pull failed for $SKILL" >> $LOG_FILE
    fi
done

echo "Skill dir check completed at $(date)" >> $LOG_FILE