#!/usr/bin/env python3
"""
NET CODE REDUCTION ENFORCER
============================

CRITICAL PREVENTION SYSTEM: Ensures DRY initiatives actually reduce code.

This tool prevents the "infrastructure-first" trap that led to 4,000 line
additions in a DRY initiative. It enforces the "ELIMINATION-FIRST" methodology.

Author: Martin | Platform Architecture
"""

import subprocess
import sys
import os
from pathlib import Path


def get_git_diff_stats():
    """Get actual line additions/deletions from git diff"""
    try:
        # Get diff stats against main branch
        result = subprocess.run(
            ["git", "diff", "--stat", "main...HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        if not result.stdout.strip():
            # No changes yet
            return 0, 0, []

        lines = result.stdout.strip().split("\n")
        summary_line = lines[-1]  # Last line has summary

        # Parse summary like "20 files changed, 1217 insertions(+), 598 deletions(-)"
        additions = 0
        deletions = 0

        if "insertion" in summary_line:
            parts = summary_line.split(", ")
            for part in parts:
                if "insertion" in part:
                    additions = int(part.split()[0])
                elif "deletion" in part:
                    deletions = int(part.split()[0])

        return additions, deletions, lines[:-1]  # Return file list without summary

    except subprocess.CalledProcessError:
        # Probably no commits yet, or not in git repo
        return 0, 0, []


def analyze_file_changes(file_lines):
    """Analyze which files are causing additions"""
    problematic_files = []

    for line in file_lines:
        if not line.strip():
            continue

        # Parse lines like " .claudedirector/lib/core/base_processor.py | 329 +++++++++++++++++++"
        parts = line.split("|")
        if len(parts) != 2:
            continue

        filename = parts[0].strip()
        changes = parts[1].strip()

        # Count additions (+ symbols)
        additions = changes.count("+")
        deletions = changes.count("-")

        if additions > deletions:
            problematic_files.append(
                {
                    "file": filename,
                    "net_addition": additions - deletions,
                    "additions": additions,
                    "deletions": deletions,
                }
            )

    return problematic_files


def main():
    """Enforce net code reduction for DRY initiatives"""
    print("🛡️ NET CODE REDUCTION ENFORCER")
    print("=" * 50)
    print("PREVENTION: Ensures DRY initiatives actually reduce code")
    print()

    additions, deletions, file_lines = get_git_diff_stats()

    if additions == 0 and deletions == 0:
        print("✅ No changes detected - validation passed")
        return 0

    net_change = additions - deletions

    print(f"📊 CHANGE ANALYSIS:")
    print(f"   Additions: {additions:,} lines")
    print(f"   Deletions: {deletions:,} lines")
    print(f"   Net Change: {net_change:+,} lines")
    print()

    if net_change <= 0:
        print(f"✅ NET REDUCTION ACHIEVED: {abs(net_change):,} lines eliminated")
        print("🎉 DRY initiative validation PASSED")
        return 0

    # Net addition detected - this is the problem we're preventing
    print(f"🚨 NET ADDITION DETECTED: {net_change:,} lines added")
    print("❌ DRY initiative validation FAILED")
    print()

    # Analyze problematic files
    problematic_files = analyze_file_changes(file_lines)

    if problematic_files:
        print("🔍 FILES CAUSING NET ADDITIONS:")
        for file_info in sorted(
            problematic_files, key=lambda x: x["net_addition"], reverse=True
        )[:10]:
            print(
                f"   {file_info['file']}: +{file_info['net_addition']} lines "
                f"({file_info['additions']} additions, {file_info['deletions']} deletions)"
            )
        print()

    print("🛡️ ENFORCEMENT RULES VIOLATED:")
    print("   1. DRY initiatives MUST result in net code reduction")
    print("   2. Infrastructure additions must eliminate 3x their size")
    print("   3. No 'add infrastructure now, eliminate later' commits")
    print()

    print("💡 REQUIRED ACTIONS:")
    print("   1. Delete duplicate code BEFORE adding infrastructure")
    print("   2. Each new file must eliminate 3x its own line count")
    print("   3. Focus on elimination, not consolidation")
    print()

    print("🚨 COMMIT BLOCKED - Fix net additions before proceeding")
    return 1


if __name__ == "__main__":
    sys.exit(main())
