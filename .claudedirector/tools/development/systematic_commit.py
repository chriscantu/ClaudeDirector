#!/usr/bin/env python3
"""
Systematic Commit Helper

Wrapper script that ensures complete commits by running systematic validation
and auto-fixing common issues before committing.

Usage:
    python .claudedirector/tools/development/systematic_commit.py "commit message"
"""

import sys
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python systematic_commit.py 'commit message'")
        sys.exit(1)

    commit_message = sys.argv[1]

    # Run systematic validation with auto-fix
    print("🔍 Running systematic commit validation...")
    result = subprocess.run(
        ["python", ".claudedirector/tools/development/systematic_commit_checker.py"]
    )

    if result.returncode != 0:
        print("❌ Systematic validation failed - commit aborted")
        sys.exit(1)

    # If validation passes, commit
    print("✅ Validation passed - proceeding with commit...")
    commit_result = subprocess.run(["git", "commit", "-m", commit_message])

    if commit_result.returncode == 0:
        print("🎉 Systematic commit completed successfully!")
    else:
        print("❌ Commit failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
