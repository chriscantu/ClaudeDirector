#!/bin/bash
# README.md Protection Hook
# Prevents deletion and ensures restoration of README.md

echo "🛡️ README.md PROTECTION SYSTEM - Active"

# Prioritize restoration from pre-stash backup first
if [ -f ".claudedirector/README.md.prestash.backup" ]; then
    echo "⚡ Fast restoration: Found pre-stash backup"
    cp ".claudedirector/README.md.prestash.backup" "README.md"
    echo "✅ README.md restored from pre-stash backup"
    git add README.md
    echo "✅ README.md re-staged for commit"
    echo "✅ README.md protection complete (via pre-stash backup)"
    exit 0
fi

# Check if README.md exists
if [ ! -f "README.md" ]; then
    echo "🚨 CRITICAL: README.md is missing!"

    # Try to restore from git
    if git show HEAD:README.md > README.md 2>/dev/null; then
        echo "✅ README.md restored from git HEAD"
        git add README.md
        echo "✅ README.md re-staged for commit"
    else
        echo "❌ Cannot restore README.md from git"
        echo "🚨 COMMIT BLOCKED: README.md must exist"
        exit 1
    fi
else
    echo "✅ README.md exists"
fi

# Ensure README.md is always staged
git add README.md 2>/dev/null || true

echo "✅ README.md protection complete"
exit 0
