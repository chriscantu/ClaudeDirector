#!/bin/bash
# Auto-backup script for leadership-workspace
BACKUP_DIR=".claudedirector/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
cp -r leadership-workspace "$BACKUP_DIR/workspace-backup-$TIMESTAMP"
# Keep only last 5 backups
ls -t "$BACKUP_DIR"/workspace-backup-* | tail -n +6 | xargs rm -rf 2>/dev/null || true
echo "Workspace backed up to $BACKUP_DIR/workspace-backup-$TIMESTAMP"
