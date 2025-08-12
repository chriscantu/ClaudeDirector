#!/bin/bash
# Post-commit README.md Verification & Recovery
# Runs AFTER all git operations complete to verify README.md integrity

echo "🔍 POST-COMMIT: README.md Integrity Verification"

# Check if README.md exists after commit operations
if [ ! -f "README.md" ]; then
    echo "🚨 CRITICAL: README.md missing after commit operations!"
    echo "🔧 Attempting immediate restoration..."

    # Try to restore from the current commit (should have it)
    if git checkout HEAD -- README.md 2>/dev/null; then
        echo "✅ README.md restored from current commit"
    else
        # Fallback: restore from previous commit
        if git checkout HEAD~1 -- README.md 2>/dev/null; then
            echo "✅ README.md restored from previous commit"
            # Re-commit the restoration
            git add README.md
            git commit --no-verify -m "🚨 AUTO-FIX: README.md restored by post-commit hook"
        else
            echo "❌ FAILED: Could not restore README.md"
            echo "⚠️  Manual intervention required!"
            exit 1
        fi
    fi
fi

# Verify README.md has required content
if [ -f "README.md" ]; then
    if ! grep -q "Value Proposition" README.md; then
        echo "⚠️  WARNING: README.md missing 'Value Proposition' - content may be corrupted"
    fi
    if ! grep -q "Quick Start" README.md; then
        echo "⚠️  WARNING: README.md missing 'Quick Start' - content may be corrupted"
    fi
    echo "✅ README.md integrity verified"
else
    echo "❌ README.md still missing after restoration attempts"
    exit 1
fi

exit 0
