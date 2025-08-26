#!/usr/bin/env python3
"""
Environment Validation Script for CI/Local Alignment
Ensures CI and local development environments are properly aligned
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_python_version():
    """Validate Python version meets requirements"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")

    if version.major != 3 or version.minor < 11:
        print(
            f"❌ Python {version.major}.{version.minor} not supported. Requires Python >=3.11"
        )
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor} supported")
        return True


def check_critical_dependencies():
    """Check that critical dependencies are installed"""
    # Map package names to import names
    critical_deps = {
        "yaml": "PyYAML",
        "pydantic": "pydantic",
        "click": "click",
        "requests": "requests",
        "structlog": "structlog",
        "pytest": "pytest",
    }

    failed_deps = []

    for import_name, package_name in critical_deps.items():
        try:
            importlib.import_module(import_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            print(f"❌ {package_name} not found")
            failed_deps.append(package_name)

    # Special check for mcp-use (may not be importable the same way)
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import mcp_use"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ mcp-use installed")
        else:
            print("❌ mcp-use not found")
            failed_deps.append("mcp-use")
    except Exception:
        print("❌ mcp-use not found")
        failed_deps.append("mcp-use")

    return len(failed_deps) == 0


def check_test_structure():
    """Validate test structure matches expected organization"""
    project_root = Path(__file__).parent.parent.parent

    critical_paths = [
        ".claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py",
        ".claudedirector/tests/regression/p0_blocking/test_setup_feature.py",
        ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml",
    ]

    all_exist = True
    for path in critical_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"✅ {path} exists")
        else:
            print(f"❌ {path} missing")
            all_exist = False

    return all_exist


def main():
    """Run all validation checks"""
    print("🔍 Environment Validation Starting...")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Critical Dependencies", check_critical_dependencies),
        ("Test Structure", check_test_structure),
    ]

    results = []
    for check_name, check_func in checks:
        print(f"\n📋 Checking: {check_name}")
        print("-" * 30)
        result = check_func()
        results.append(result)

    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)

    if all(results):
        print("🎉 ALL CHECKS PASSED - Environment Ready")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED - Environment Issues Detected")
        sys.exit(1)


if __name__ == "__main__":
    main()
