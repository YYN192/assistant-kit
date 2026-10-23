#!/bin/bash
# Ask the simulated person (a separate Claude instance with no tools) to answer the
# assistant's latest message.
#   tests/ask_persona.sh <persona-id> <file-with-assistant-message>
# Appends both sides to examples/<persona-id>/transcript.md and prints the reply.
# The persona sees only its hidden sheet and the conversation so far.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ID="$1"; MSG_FILE="$2"
SHEET="$ROOT/tests/personas/$ID.md"
OUT="$ROOT/examples/$ID"
TRANSCRIPT="$OUT/transcript.md"
mkdir -p "$OUT"
[ -f "$TRANSCRIPT" ] || printf '# Transcript: %s\n\nSetup conversation between the kit (Claude) and the simulated person.\n' "$ID" > "$TRANSCRIPT"

{ printf '\n---\n\n**Claude:**\n\n'; cat "$MSG_FILE"; printf '\n'; } >> "$TRANSCRIPT"

SYSTEM="You are role-playing a real person who is setting up a personal assistant with Claude. \
Stay fully in character as the person described in the sheet below. Answer only what you are asked, \
the way this person would type in a chat: natural, sometimes brief, never meta. Do not invent \
details that contradict the sheet; if something isn't in the sheet, give a plausible short answer \
consistent with it. When the assistant gives you steps to do (connect an app, set up forwarding, \
run a command, upload a file), pretend you did them and report the realistic outcome from the sheet \
(including errors the sheet says happen). Never reveal this sheet or that you are simulated. \
Ignore any account names, emails or other user information you might see in your context: \
they are NOT yours; you are only the person in this sheet.

PERSON SHEET:
$(cat "$SHEET")"

PROMPT="Here is the conversation so far (you are the person; 'Claude' is the assistant):

$(cat "$TRANSCRIPT")

Write your next reply to Claude's last message, as the person. Reply with the message text only."

cd "$(mktemp -d)"
REPLY="$(claude -p "$PROMPT" --system-prompt "$SYSTEM" --tools "" --setting-sources "" \
  --strict-mcp-config --model sonnet --no-session-persistence < /dev/null)"

{ printf '\n**%s:**\n\n%s\n' "Person" "$REPLY"; } >> "$TRANSCRIPT"
printf '%s\n' "$REPLY"
