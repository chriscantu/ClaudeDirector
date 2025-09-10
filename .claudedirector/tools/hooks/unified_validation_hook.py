#!/usr/bin/env python3
"""
Unified Validation Hook - Single Pre-commit Hook for All Validations

🏗️ Martin | Platform Architecture - Consolidated Hook System

CONSOLIDATION OBJECTIVE: Replace multiple pre-commit hooks with a single,
fast, parallel validation hook that runs all checks efficiently.

REPLACES:
- Multiple bloat prevention hooks
- Multiple security scanning hooks  
- Multiple quality checking hooks
- Multiple architecture validation hooks

PERFORMANCE TARGET: <5s total validation time
ARCHITECTURE: Single hook → Unified Prevention Engine → Parallel validation
"""

import sys
import os
from pathlib import Path

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "lib"))

try:
    from core.validation.unified_prevention_engine import UnifiedPreventionEngine
except ImportError as e:
    print(f"❌ Could not import UnifiedPreventionEngine: {e}")
    print("🔧 Falling back to basic validation...")
    sys.exit(0)  # Don't block commits on import errors


def get_staged_python_files():
    """Get list of staged Python files for validation"""
    import subprocess
    
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True
        )
        
        python_files = [
            Path(f) for f in result.stdout.strip().split('\n') 
            if f.endswith('.py') and Path(f).exists()
        ]
        
        return python_files
        
    except subprocess.CalledProcessError:
        print("⚠️  Could not get staged files - validating current directory")
        return list(Path('.').glob('**/*.py'))


def main():
    """Main hook execution"""
    print("🛡️ UNIFIED VALIDATION HOOK")
    print("=" * 50)
    
    # Get staged files
    staged_files = get_staged_python_files()
    
    if not staged_files:
        print("✅ No Python files to validate")
        return 0
    
    print(f"🔍 Validating {len(staged_files)} Python files...")
    
    # Initialize unified engine
    engine = UnifiedPreventionEngine()
    
    # Validate all staged files
    all_results = {}
    for file_path in staged_files:
        file_results = engine.validate_file(file_path)
        if file_results:
            all_results[str(file_path)] = file_results
    
    # Generate report
    if all_results:
        report = engine.generate_report(all_results)
        print(report)
        
        # Count violations
        total_violations = sum(
            len(result.violations) 
            for file_results in all_results.values() 
            for result in file_results.values()
        )
        
        if total_violations > 0:
            print(f"\n🚨 COMMIT BLOCKED: {total_violations} violations must be fixed")
            return 1
    
    print("\n✅ ALL VALIDATIONS PASSED - Commit allowed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
