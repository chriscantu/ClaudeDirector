#!/bin/bash
# README.md Protection System - Enhanced Pre-commit Hook
# Prevents README.md deletion during git operations

echo "🛡️ README.md PROTECTION SYSTEM - Active"

# Check if README.md exists
if [ ! -f "README.md" ]; then
    echo "🚨 CRITICAL: README.md is missing!"
    echo "🔧 Attempting automatic restoration..."
    
    # Try to restore from git history
    if git checkout HEAD~1 -- README.md 2>/dev/null; then
        echo "✅ README.md restored from git history"
        git add README.md
    else
        echo "❌ Failed to restore README.md from git history"
        echo "⚠️  Manual intervention required"
        exit 1
    fi
fi

# Check if README.md is being deleted in this commit
if git diff --cached --name-status | grep -q "^D.*README.md$"; then
    echo "🚨 BLOCKED: Attempt to delete README.md detected!"
    echo "README.md is critical for project discovery and must not be deleted"
    echo "If you need to modify README.md, use 'git add README.md' instead"
    exit 1
fi

# Verify README.md has minimum required content
if [ -f "README.md" ]; then
    if ! grep -q "Value Proposition" README.md; then
        echo "⚠️  WARNING: README.md missing 'Value Proposition' section"
    fi
    if ! grep -q "Quick Start" README.md; then
        echo "⚠️  WARNING: README.md missing 'Quick Start' section"
    fi
fi

echo "✅ README.md protection check passed"
exit 0
