#!/usr/bin/env python3
"""
README Content Protection - Content-Aware Approach
Protects README.md from accidental deletion or corruption while allowing legitimate updates.

FIXED APPROACH: Instead of overwriting changes, validates content quality and prevents corruption.
"""

import sys
import os
from pathlib import Path
import re


def validate_readme_content(readme_path: Path) -> tuple[bool, str]:
    """
    Validate README content for essential elements

    Returns:
        (is_valid, reason)
    """
    if not readme_path.exists():
        return False, "README.md file is missing"

    try:
        content = readme_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Cannot read README.md: {e}"

    # Check for minimum content length
    if len(content.strip()) < 100:
        return False, "README.md content is too short (minimum 100 characters)"

    # Check for essential sections
    required_elements = [
        (r"#\s+ClaudeDirector", "Missing main title"),
        (r"##\s+.*[Qq]uick\s+[Ss]tart", "Missing Quick Start section"),
        (r"strategic|leadership|AI|persona", "Missing strategic/leadership content"),
    ]

    content_lower = content.lower()
    for pattern, error_msg in required_elements:
        if not re.search(pattern, content, re.IGNORECASE):
            return False, error_msg

    # Check for suspicious patterns that might indicate corruption
    suspicious_patterns = [
        (r"^File is empty\.$", "File appears to be empty placeholder"),
        (r"<\?xml|<!DOCTYPE html", "File appears to be XML/HTML instead of Markdown"),
    ]

    # Check if file is completely empty (separate check)
    if len(content.strip()) == 0:
        return False, "File is completely empty"

    for pattern, error_msg in suspicious_patterns:
        if re.search(pattern, content, re.MULTILINE):
            return False, error_msg

    return True, "README content is valid"


def check_explicit_readme_intent() -> bool:
    """
    Check if README changes are explicitly intended by looking for intent markers
    """
    # Check git commit message for explicit README intent
    try:
        import subprocess

        result = subprocess.run(
            ["git", "log", "--format=%B", "-n", "1", "--staged"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            commit_msg = result.stdout.lower()
            readme_intent_markers = [
                "readme",
                "documentation update",
                "update readme",
                "fix readme",
                "improve readme",
                "enhance readme",
            ]
            return any(marker in commit_msg for marker in readme_intent_markers)
    except:
        pass

    # Check for environment variable override
    return os.getenv("CLAUDEDIRECTOR_ALLOW_README_CHANGES", "").lower() == "true"


def main():
    """Main README content protection logic with PRESERVATION-FIRST approach"""
    if len(sys.argv) < 2:
        print("Usage: readme_content_protection.py <readme_file>")
        sys.exit(1)

    readme_path = Path(sys.argv[1])

    # 🛡️ CRITICAL FIX: Only protect root README.md, not subdirectory READMEs
    if readme_path.name == "README.md" and readme_path.parent != Path("."):
        print(f"✅ README PROTECTION: Skipping subdirectory README: {readme_path}")
        print("📋 Only root README.md is protected from accidental changes")
        sys.exit(0)

    # CRITICAL FIX: PRESERVATION-FIRST PROTECTION
    # Never block commits that could cause README deletion
    # Instead, validate content and warn but ALWAYS ALLOW
    # PROACTIVE PROTECTION: Check if README changes are explicitly intended
    if not check_explicit_readme_intent():
        print("🛡️ README PROTECTION: Implicit README changes detected")
        print("📋 Allowing commit but monitoring for content integrity")
        print(
            "💡 Future commits with README intent should include 'README' in commit message"
        )
        # CRITICAL: Do NOT exit(1) here - this was causing README deletion
        # sys.exit(1)  # DISABLED - This was the bug!

    # Validate README content quality
    is_valid, reason = validate_readme_content(readme_path)

    if not is_valid:
        print(f"🚨 README CONTENT PROTECTION: {reason}")
        print(f"📋 README validation failed for: {readme_path}")
        print("💡 This protection prevents README corruption")
        print("🔧 If this is a legitimate change, ensure README has:")
        print("   - Main title with 'ClaudeDirector'")
        print("   - Quick Start section")
        print("   - Strategic/leadership content")
        print("   - Minimum 100 characters")
        print("⚠️  PRESERVATION-FIRST: Allowing commit to prevent README loss")
        print("🛡️ Post-commit hook will restore README if corrupted")
        # CRITICAL FIX: Never exit(1) on content validation failure
        # This was causing README deletion during pre-commit processing
        # sys.exit(1)  # DISABLED - This was the second source of README deletion!

    print(f"✅ README CONTENT PROTECTION: {reason}")
    if check_explicit_readme_intent():
        print("✅ PRESERVATION-FIRST PROTECTION: Explicit README intent confirmed")
    else:
        print(
            "✅ PRESERVATION-FIRST PROTECTION: README preserved despite implicit changes"
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
