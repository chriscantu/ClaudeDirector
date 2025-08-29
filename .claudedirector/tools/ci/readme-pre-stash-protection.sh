#!/bin/bash
# README.md Pre-Stash Protection Hook
# Creates a backup of README.md before git stash operations

echo "🛡️ README.md PRE-STASH PROTECTION - Active"

# Create a temporary backup of README.md
if [ -f "README.md" ]; then
    cp "README.md" ".claudedirector/README.md.prestash.backup"
    echo "✅ README.md backup created: .claudedirector/README.md.prestash.backup"
    git add README.md # Ensure README.md is always staged
else
    echo "⚠️ README.md not found, no pre-stash backup created."
fi

echo "✅ README.md pre-stash protection complete"
exit 0
