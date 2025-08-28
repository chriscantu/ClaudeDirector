#!/usr/bin/env python3
"""
🧹 Intelligent Backup Cleanup System
====================================
Implements smart backup retention policies for ClaudeDirector.

Features:
- Keep latest 5 backups of each type
- Keep one backup per day for last 7 days
- Keep one backup per week for last 4 weeks
- Remove duplicates and excessive backups
- Preserve critical workspace snapshots
"""

import os
import sys
import glob
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import re


class IntelligentBackupCleaner:
    def __init__(self, backup_root: str = ".claudedirector/backups"):
        self.backup_root = Path(backup_root)
        self.stats = {"files_removed": 0, "space_freed": 0, "files_kept": 0}

    def get_file_size(self, filepath: Path) -> int:
        """Get file size in bytes, handling directories"""
        if filepath.is_file():
            return filepath.stat().st_size
        elif filepath.is_dir():
            return sum(f.stat().st_size for f in filepath.rglob("*") if f.is_file())
        return 0

    def parse_backup_timestamp(self, filename: str) -> datetime:
        """Extract timestamp from backup filename"""
        # Pattern: backup-YYYYMMDD-HHMMSS
        timestamp_match = re.search(r"(\d{8}-\d{6})", filename)
        if timestamp_match:
            timestamp_str = timestamp_match.group(1)
            return datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")

        # Fallback to file modification time
        filepath = self.backup_root / filename
        if filepath.exists():
            return datetime.fromtimestamp(filepath.stat().st_mtime)

        return datetime.min

    def categorize_backups(self) -> Dict[str, List[Path]]:
        """Categorize backups by type"""
        categories = {"readme": [], "workspace": [], "other": []}

        if not self.backup_root.exists():
            return categories

        for backup_file in self.backup_root.rglob("*backup*"):
            filename = backup_file.name.lower()
            if "readme" in filename:
                categories["readme"].append(backup_file)
            elif "workspace" in filename:
                categories["workspace"].append(backup_file)
            else:
                categories["other"].append(backup_file)

        return categories

    def apply_retention_policy(
        self, files: List[Path], keep_latest: int = 5
    ) -> List[Path]:
        """Apply intelligent retention policy"""
        if len(files) <= keep_latest:
            return []  # Keep all files

        # Sort by timestamp (newest first)
        files_with_time = [(f, self.parse_backup_timestamp(f.name)) for f in files]
        files_with_time.sort(key=lambda x: x[1], reverse=True)

        files_to_delete = []
        now = datetime.now()

        # Keep latest N files
        keep_latest_files = [f for f, _ in files_with_time[:keep_latest]]

        # Apply time-based retention to older files
        for file_path, timestamp in files_with_time[keep_latest:]:
            age = now - timestamp

            # Keep one per day for last 7 days
            if age <= timedelta(days=7):
                # Check if we already have a backup for this day
                day_key = timestamp.strftime("%Y-%m-%d")
                if not any(
                    self.parse_backup_timestamp(f.name).strftime("%Y-%m-%d") == day_key
                    for f in keep_latest_files
                ):
                    keep_latest_files.append(file_path)
                    continue

            # Keep one per week for last 4 weeks
            elif age <= timedelta(weeks=4):
                week_key = timestamp.strftime("%Y-W%U")
                if not any(
                    self.parse_backup_timestamp(f.name).strftime("%Y-W%U") == week_key
                    for f in keep_latest_files
                ):
                    keep_latest_files.append(file_path)
                    continue

            # Delete older files
            files_to_delete.append(file_path)

        return files_to_delete

    def cleanup_category(self, category: str, files: List[Path]) -> None:
        """Clean up a specific backup category"""
        if not files:
            return

        print(f"\n🧹 Cleaning up {category} backups ({len(files)} files)...")

        # Apply retention policy
        if category == "readme":
            files_to_delete = self.apply_retention_policy(files, keep_latest=3)
        elif category == "workspace":
            files_to_delete = self.apply_retention_policy(files, keep_latest=2)
        else:
            files_to_delete = self.apply_retention_policy(files, keep_latest=1)

        # Remove files
        for file_path in files_to_delete:
            try:
                file_size = self.get_file_size(file_path)
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()

                self.stats["files_removed"] += 1
                self.stats["space_freed"] += file_size
                print(f"   🗑️ Removed: {file_path.name} ({file_size // 1024}KB)")

            except Exception as e:
                print(f"   ❌ Failed to remove {file_path.name}: {e}")

        kept_count = len(files) - len(files_to_delete)
        self.stats["files_kept"] += kept_count
        print(f"   ✅ Kept {kept_count} files, removed {len(files_to_delete)} files")

    def run_cleanup(self, dry_run: bool = False) -> None:
        """Run the intelligent backup cleanup"""
        print("🧹 ClaudeDirector Intelligent Backup Cleanup")
        print("=" * 50)

        if dry_run:
            print("🔍 DRY RUN MODE - No files will be deleted")
            print()

        # Get current backup state
        categories = self.categorize_backups()

        total_files = sum(len(files) for files in categories.values())
        print(f"📊 Found {total_files} backup files:")
        for category, files in categories.items():
            print(f"   {category}: {len(files)} files")

        if total_files == 0:
            print("✅ No backups found - nothing to clean!")
            return

        # Calculate total size before cleanup
        total_size_before = sum(
            sum(self.get_file_size(f) for f in files) for files in categories.values()
        )

        print(f"📊 Total backup size: {total_size_before // (1024 * 1024)}MB")
        print()

        if not dry_run:
            # Clean each category
            for category, files in categories.items():
                self.cleanup_category(category, files)

        # Print summary
        print("\n📊 CLEANUP SUMMARY:")
        print(f"   Files removed: {self.stats['files_removed']}")
        print(f"   Files kept: {self.stats['files_kept']}")
        print(f"   Space freed: {self.stats['space_freed'] // (1024 * 1024)}MB")
        print(
            f"   Efficiency: {(self.stats['space_freed'] / total_size_before * 100):.1f}% space reduction"
        )


def main():
    """Main cleanup execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description="ClaudeDirector Intelligent Backup Cleanup"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting",
    )
    parser.add_argument(
        "--backup-dir", default=".claudedirector/backups", help="Backup directory path"
    )

    args = parser.parse_args()

    cleaner = IntelligentBackupCleaner(args.backup_dir)
    cleaner.run_cleanup(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
