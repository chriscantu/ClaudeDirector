#!/usr/bin/env python3
"""
Fix Import Paths Script
Systematically updates all 'from lib.*' imports to 'from lib.*' pattern
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path: Path) -> bool:
    """Fix imports in a single file. Returns True if changes were made."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Pattern to match: from lib.* import
        pattern = r'from claudedirector\.([^\s]+) import'
        replacement = r'from lib.\1 import'

        content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed imports in: {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Fix all import paths in the .claudedirector directory"""
    base_dir = Path(__file__).parent.parent.parent
    claudedirector_dir = base_dir / ".claudedirector"

    print("🔧 Fixing import paths from 'claudedirector.*' to 'lib.*'")
    print("=" * 60)

    # Find all Python files with problematic imports
    files_to_fix = []
    for py_file in claudedirector_dir.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(r'from claudedirector\.', content):
                    files_to_fix.append(py_file)
        except:
            continue

    print(f"📊 Found {len(files_to_fix)} files with problematic imports")
    print()

    # Fix each file
    fixed_count = 0
    for file_path in files_to_fix:
        if fix_imports_in_file(file_path):
            fixed_count += 1

    print()
    print("=" * 60)
    print(f"🎉 Import path fixing complete!")
    print(f"📊 Files processed: {len(files_to_fix)}")
    print(f"✅ Files fixed: {fixed_count}")
    print(f"⏭️  Files unchanged: {len(files_to_fix) - fixed_count}")

if __name__ == "__main__":
    main()
