#!/usr/bin/env python3
"""
Unified Validation CLI - Single Interface for All Validations

🏗️ Martin | Platform Architecture - Consolidated CLI Interface

CONSOLIDATION OBJECTIVE: Replace multiple validation CLIs with a single,
comprehensive interface that provides access to all validation modules.

REPLACES:
- Multiple bloat checker CLIs
- Multiple security scanner CLIs
- Multiple quality checker CLIs
- Multiple architecture validation CLIs

USAGE:
  python validate.py <path>                    # Validate with all modules
  python validate.py <path> --modules bloat   # Validate with specific module
  python validate.py <path> --fix             # Auto-fix issues where possible
  python validate.py <path> --report out.txt  # Save report to file
"""

import sys
import os
from pathlib import Path

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    from core.validation.unified_prevention_engine import (
        UnifiedPreventionEngine,
        BloatModule,
        P0Module,
        SecurityModule,
        QualityModule,
    )
except ImportError as e:
    print(f"❌ Could not import UnifiedPreventionEngine: {e}")
    print("🔧 Please ensure the unified prevention engine is properly installed")
    sys.exit(1)


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🛡️ Unified Validation System - Consolidated Code Quality Enforcement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate.py .                          # Validate current directory
  python validate.py myfile.py                  # Validate single file
  python validate.py . --modules bloat security # Run only bloat and security modules
  python validate.py . --report validation.txt  # Save report to file
  python validate.py . --quiet                  # Only show violations
        """,
    )

    parser.add_argument("path", help="File or directory to validate")
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursive directory validation (default: True)",
    )
    parser.add_argument(
        "--modules",
        nargs="*",
        choices=["bloat", "p0", "security", "quality"],
        help="Specific validation modules to run",
    )
    parser.add_argument("--report", "-o", help="Output report to file")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Only show violations, suppress info"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix issues where possible (TODO: future enhancement)",
    )

    args = parser.parse_args()

    if not args.quiet:
        print("🛡️ UNIFIED VALIDATION SYSTEM")
        print("=" * 60)
        print("📋 Consolidated code quality enforcement")
        print("🎯 DRY/SOLID compliant validation architecture")
        print("=" * 60)

    # Initialize engine with selected modules
    if args.modules:
        module_map = {
            "bloat": BloatModule(),
            "p0": P0Module(),
            "security": SecurityModule(),
            "quality": QualityModule(),
        }
        modules = [module_map[name] for name in args.modules]
        engine = UnifiedPreventionEngine(modules)

        if not args.quiet:
            print(f"🔍 Running modules: {', '.join(args.modules)}")
    else:
        engine = UnifiedPreventionEngine()
        if not args.quiet:
            print("🔍 Running all validation modules")

    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Path does not exist: {path}")
        return 1

    # Run validation
    if path.is_file():
        if not args.quiet:
            print(f"📁 Validating file: {path}")
        results = {str(path): engine.validate_file(path)}
    else:
        if not args.quiet:
            print(f"📁 Validating directory: {path}")
        results = engine.validate_directory(path, args.recursive)

    if not results:
        print("⚠️  No Python files found to validate")
        return 0

    # Handle JSON output
    if args.json:
        import json

        json_results = {}
        for file_path, file_results in results.items():
            json_results[file_path] = {}
            for module_name, result in file_results.items():
                json_results[file_path][module_name] = {
                    "violations": result.violations,
                    "warnings": result.warnings,
                    "execution_time_ms": result.execution_time_ms,
                    "success": result.success,
                }

        json_output = json.dumps(json_results, indent=2)
        if args.report:
            Path(args.report).write_text(json_output)
            print(f"📄 JSON report written to {args.report}")
        else:
            print(json_output)
        return 0

    # Generate and output report
    report = engine.generate_report(results)

    if args.report:
        Path(args.report).write_text(report)
        if not args.quiet:
            print(f"📄 Report written to {args.report}")

    if not args.quiet or any(
        len(result.violations) > 0
        for file_results in results.values()
        for result in file_results.values()
    ):
        print(report)

    # Return exit code based on violations
    total_violations = sum(
        len(result.violations)
        for file_results in results.values()
        for result in file_results.values()
    )

    if total_violations > 0:
        if not args.quiet:
            print(f"\n🚨 Validation completed with {total_violations} violations")
        return 1
    else:
        if not args.quiet:
            print("\n✅ All validations passed successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
