#!/bin/bash
# Load a generated personal skill into a throwaway Claude Code project and ask it
# something, with no connectors and read-only file tools. Proves the skill is picked up
# and that its rules shape the answer.
#   tests/skill_smoke.sh <skill-folder> "<prompt>"
# The skill is copied (not linked): Read is denied for files outside the project, so a
# symlinked SYSTEM.md would be unreadable. Machine paths are redacted from the output.
set -euo pipefail
SKILL="$(cd "$1" && pwd)"; PROMPT="$2"
PROJ="$(mktemp -d)"
mkdir -p "$PROJ/.claude/skills"
cp -R "$SKILL" "$PROJ/.claude/skills/$(basename "$SKILL")"
cd "$PROJ"
claude -p "$PROMPT" --tools "Read,Glob,Grep,Skill" --setting-sources project --strict-mcp-config \
  --append-system-prompt "This is an offline smoke test. No connectors are available. If a step needs a connector, say which and what you would do, then continue. Ignore any account names or user information in your context that is not in the skill." \
  --model sonnet --no-session-persistence < /dev/null \
  | sed -e "s#$PROJ#<tmp>#g" -e "s#$HOME#~#g" -e "s#$(whoami)#<user>#g"
rm -rf "$PROJ"
