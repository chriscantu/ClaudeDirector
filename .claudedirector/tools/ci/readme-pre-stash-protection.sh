#!/bin/bash
# README.md Pre-Stash Protection System
# Prevents README.md from being lost during pre-commit stash operations
# CRITICAL: This must run BEFORE any other hooks that might trigger stashing

echo "🛡️ README.md PRE-STASH PROTECTION - Active"

# Create a backup of README.md before any stash operations
if [ -f "README.md" ]; then
    # Create backup with timestamp for debugging
    BACKUP_FILE=".claudedirector/backups/readme-backup-$(date +%Y%m%d-%H%M%S).md"
    mkdir -p "$(dirname "$BACKUP_FILE")"
    cp "README.md" "$BACKUP_FILE"

    # Create working backup that protection script can use
    cp "README.md" ".claudedirector/README.md.prestash.backup"

    echo "✅ README.md backup created: $BACKUP_FILE"
    echo "✅ Working backup created for stash protection"
else
    echo "⚠️  WARNING: README.md not found - cannot create pre-stash backup"

    # Try to restore from previous backup if available
    if [ -f ".claudedirector/README.md.prestash.backup" ]; then
        echo "🔧 Restoring README.md from previous backup..."
        cp ".claudedirector/README.md.prestash.backup" "README.md"
        git add "README.md"
        echo "✅ README.md restored from backup"
    else
        echo "❌ No backup available - README.md protection may trigger restoration"
    fi
fi

# Ensure README.md is properly staged to prevent stash issues
if [ -f "README.md" ]; then
    # Check if README.md has unstaged changes
    if git diff --name-only | grep -q "^README.md$"; then
        echo "🔧 README.md has unstaged changes - staging to prevent stash issues"
        git add "README.md"
        echo "✅ README.md staged to prevent stash conflicts"
    fi

    # Double-check that README.md is not being deleted
    if git diff --cached --name-status | grep -q "^D.*README.md$"; then
        echo "🚨 BLOCKED: README.md deletion detected in staged changes!"
        echo "Restoring README.md from backup..."

        if [ -f ".claudedirector/README.md.prestash.backup" ]; then
            cp ".claudedirector/README.md.prestash.backup" "README.md"
            git add "README.md"
            echo "✅ README.md restored and re-staged"
        else
            echo "❌ Cannot restore README.md - no backup available"
            exit 1
        fi
    fi
fi

echo "✅ README.md pre-stash protection complete"
exit 0
