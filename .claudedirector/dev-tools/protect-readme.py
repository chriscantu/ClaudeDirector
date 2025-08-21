#!/usr/bin/env python3
"""
README.md Protection Script
Prevents accidental deletion of README.md from main branch
"""

import subprocess
import sys
from pathlib import Path


def check_readme_exists():
    """Check if README.md exists in the repository root"""
    readme_path = Path("README.md")
    return readme_path.exists()


def restore_readme():
    """Restore README.md from git history if it's missing"""
    try:
        # Try to restore from the most recent commit that had it
        result = subprocess.run(
            ["git", "log", "--oneline", "--", "README.md"],
            capture_output=True,
            text=True,
            check=True,
        )

        if result.stdout.strip():
            # Get the most recent commit that modified README.md
            latest_commit = result.stdout.strip().split("\n")[0].split()[0]

            # Restore README.md from that commit
            subprocess.run(
                ["git", "checkout", latest_commit, "--", "README.md"], check=True
            )

            # Stage and commit the restoration
            subprocess.run(["git", "add", "README.md"], check=True)
            subprocess.run(
                [
                    "git",
                    "commit",
                    "--no-verify",
                    "-m",
                    "🚨 AUTO-RESTORE: README.md protection system\n\nREADME.md was missing and has been automatically restored.\nThis file is critical for project discovery and must remain on main branch.",
                ],
                check=True,
            )

            print("✅ README.md automatically restored and committed")
            return True
        else:
            print("❌ No README.md found in git history")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to restore README.md: {e}")
        return False


def main():
    """Main protection check"""
    if not check_readme_exists():
        print("🚨 CRITICAL: README.md is missing from main branch!")
        print("📝 Attempting automatic restoration...")

        if restore_readme():
            print("✅ README.md protection system successful")
            return 0
        else:
            print("❌ README.md protection system failed")
            print("⚠️  Manual intervention required!")
            return 1
    else:
        print("✅ README.md protection check passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
