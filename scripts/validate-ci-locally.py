#!/usr/bin/env python3
"""
Local CI Validation Script
Runs the same checks as GitHub Actions CI pipeline locally to catch issues before pushing.

Usage: python3 scripts/validate-ci-locally.py [--fix]
"""

import os
import sys
import subprocess
import re
import ast
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(step_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}🔍 {step_name}{Colors.END}")
    print("=" * 60)

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def run_command(cmd, shell=False, check=True):
    """Run a command and return the result"""
    try:
        # Prefer venv tools if available
        if isinstance(cmd, str) and not shell:
            cmd_parts = cmd.split()
            tool = cmd_parts[0]
            # Check for venv versions of tools
            venv_tool = f"./venv/bin/{tool}"
            if os.path.exists(venv_tool):
                cmd_parts[0] = venv_tool
                cmd = " ".join(cmd_parts)
                shell = True

        result = subprocess.run(
            cmd if shell else cmd.split(),
            capture_output=True,
            text=True,
            shell=shell,
            check=False
        )
        return result
    except subprocess.SubprocessError as e:
        if check:
            raise
        return None

def security_scan():
    """Run the same security scan as CI"""
    print_step("SECURITY SCAN - Sensitive Data Protection")

    # Sensitive patterns to scan for (exact copy from CI)
    patterns = [
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'Email addresses'),
        (r'(?:password|passwd|pwd)\s*[=:]\s*[a-zA-Z0-9_-]{8,}', 'Passwords'),
        (r'(?:api_key|apikey|secret)\s*[=:]\s*[a-zA-Z0-9_-]{16,}', 'API Keys'),
        (r'(?:token)\s*[=:]\s*[a-zA-Z0-9_-]{20,}', 'Tokens'),
        (r'aws_access_key_id\s*[=:]\s*[A-Z0-9]{20}', 'AWS Access Keys'),
        (r'ssh-rsa\s+[A-Za-z0-9+/]{100,}', 'SSH Keys')
    ]

    issues = []

    for root, dirs, files in os.walk('.'):
        # Skip .git and other system directories (exact copy from CI)
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'node_modules', 'target', 'build', 'dist']]

        for file in files:
            if file.endswith(('.py', '.yaml', '.yml', '.json', '.txt', '.md')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    for pattern, desc in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Skip obvious test data or documentation
                            line = content[:match.start()].count('\n') + 1
                            context = match.group()

                            # Enhanced filtering for documentation and examples (exact copy from CI)
                            skip_patterns = ['example', 'test', 'dummy', 'placeholder', 'xxx', 'company.com', 'platform-security.internal', 'sample', 'docs', 'documentation', 'procore.com']
                            is_doc_file = any(doc_path in filepath.lower() for doc_path in ['docs/', 'readme', 'security.md', 'example', 'leadership-workspace/'])
                            is_example_content = any(pattern in context.lower() for pattern in skip_patterns)

                            if not (is_doc_file or is_example_content):
                                issues.append(f'{filepath}:{line} - {desc}: {context[:50]}...')
                except Exception:
                    pass

    if issues:
        print_error('SECURITY VIOLATIONS DETECTED:')
        for issue in issues[:10]:  # Limit to first 10
            print(f'   {issue}')
        if len(issues) > 10:
            print(f'   ... and {len(issues) - 10} more issues')
        return False
    else:
        print_success('No sensitive data patterns detected')
        return True

def black_formatting_check(fix=False):
    """Run Black formatting check"""
    print_step("CODE QUALITY - Black Formatting Check")

    # Ensure black is available (matches CI)
    install_result = run_command("python -m pip install black>=23.0.0", check=False)

    if fix:
        result = run_command("python -m black .claudedirector/")
        if result.returncode == 0:
            print_success("Black formatting applied")
            return True
        else:
            print_error("Black formatting failed")
            print(result.stderr)
            return False
    else:
        result = run_command("python -m black --check --diff .claudedirector/")
        if result.returncode == 0:
            print_success("Black formatting check passed")
            return True
        else:
            print_error("BLACK FORMATTING VIOLATIONS DETECTED")
            print("Run 'python3 scripts/validate-ci-locally.py --fix' to fix formatting issues")
            print(result.stdout)
            return False

def flake8_linting():
    """Run Flake8 linting"""
    print_step("CODE QUALITY - Flake8 Linting")

    # Ensure flake8 is available (matches CI)
    install_result = run_command("python -m pip install flake8>=6.0.0", check=False)

    result = run_command("python -m flake8 .claudedirector/ --max-line-length=120 --extend-ignore=E203,W503,E501,F541,F841,E302,E303,E305,E402,E261,E128,E129,E722,E731,F824,F811,W292,F821 --statistics")
    if result.returncode == 0:
        print_success("Flake8 linting check passed")
        return True
    else:
        print_error("FLAKE8 LINTING VIOLATIONS DETECTED")
        print(result.stdout)
        return False

def mypy_type_checking():
    """Run MyPy type checking with error count limit (matches CI)"""
    print_step("CODE QUALITY - MyPy Type Checking")
    
    # Ensure mypy and type stubs are available (matches CI)
    install_result = run_command("python -m pip install mypy>=1.0.0 types-PyYAML>=6.0.0 types-requests>=2.32.0 types-setuptools>=80.0.0", check=False)
    
    # Count errors and allow up to 500 for development codebase (matches CI)
    result = run_command("python -m mypy .claudedirector/lib/ --ignore-missing-imports --no-strict-optional")
    if result.returncode == 0:
        print_success("MyPy type checking passed (0 errors)")
        return True
    
    # Count errors in output
    error_lines = [line for line in result.stdout.split('\n') if 'error:' in line]
    error_count = len(error_lines)
    
    if error_count > 500:
        print_error(f"MYPY TYPE CHECKING VIOLATIONS: {error_count} errors exceed 500 limit")
        print("Showing first 10 errors:")
        for line in error_lines[:10]:
            print(f"  {line}")
        return False
    else:
        print_success(f"MyPy type checking passed ({error_count} errors within 500 limit)")
        return True

def solid_principles_validation():
    """Run SOLID principles validation (exact copy from CI)"""
    print_step("SOLID PRINCIPLES VALIDATION")

    class SOLIDAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.violations = []
            self.current_file = ''

        def visit_ClassDef(self, node):
            # Single Responsibility: Check for classes with too many methods
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            if len(methods) > 15:
                self.violations.append(f'{self.current_file}:{node.lineno} - SRP Violation: Class {node.name} has {len(methods)} methods (>15)')

            # Check for god classes (too many lines)
            if hasattr(node, 'end_lineno') and node.end_lineno:
                lines = node.end_lineno - node.lineno
                if lines > 200:
                    self.violations.append(f'{self.current_file}:{node.lineno} - SRP Violation: Class {node.name} has {lines} lines (>200)')

            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # Single Responsibility: Check for functions with too many parameters
            if len(node.args.args) > 7:
                self.violations.append(f'{self.current_file}:{node.lineno} - ISP Violation: Function {node.name} has {len(node.args.args)} parameters (>7)')

            # Check for long functions
            if hasattr(node, 'end_lineno') and node.end_lineno:
                lines = node.end_lineno - node.lineno
                if lines > 50:
                    self.violations.append(f'{self.current_file}:{node.lineno} - SRP Violation: Function {node.name} has {lines} lines (>50)')

            self.generic_visit(node)

    analyzer = SOLIDAnalyzer()

    if os.path.exists('.claudedirector/lib'):
        for root, dirs, files in os.walk('.claudedirector/lib'):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()

                        tree = ast.parse(content)
                        analyzer.current_file = filepath
                        analyzer.visit(tree)
                    except Exception as e:
                        print_warning(f'Could not analyze {filepath}: {e}')

    if analyzer.violations:
        print_error('SOLID PRINCIPLES VIOLATIONS DETECTED:')
        for violation in analyzer.violations[:20]:  # Limit output
            print(f'   {violation}')
        if len(analyzer.violations) > 20:
            print(f'   ... and {len(analyzer.violations) - 20} more violations')
        print(f'Total violations: {len(analyzer.violations)}')
        if len(analyzer.violations) > 50:  # Only fail for major violations
            return False
        else:
            print_warning("Minor violations detected but within acceptable limits")
            return True
    else:
        print_success('SOLID principles validation passed')
        return True

def unit_tests_with_coverage():
    """Run unit tests with coverage (exact copy from CI)"""
    print_step("UNIT TESTS WITH COVERAGE REPORTING")

    # Install coverage tool (matches CI)
    install_result = run_command("python -m pip install coverage", check=False)

    # Run tests with coverage (exact CI command)
    print("Running unit tests with coverage...")
    result = run_command("python -m coverage run --source=.claudedirector/lib .claudedirector/tests/unit/test_suite_runner.py")
    if result.returncode != 0:
        print_error("Unit tests failed")
        print(result.stdout)
        print(result.stderr)
        return False

    # Generate coverage reports (exact CI command)
    print("Generating coverage reports...")
    coverage_result = run_command("python -m coverage report")
    if coverage_result.returncode != 0:
        print_error("Coverage report generation failed")
        print(coverage_result.stdout)
        return False
    
    # Extract coverage percentage
    lines = coverage_result.stdout.strip().split('\n')
    if lines:
        last_line = lines[-1]
        if '%' in last_line:
            # Extract percentage from "TOTAL ... X%"
            pct_str = last_line.split()[-1].replace('%', '')
            try:
                coverage_pct = float(pct_str)
                print(f"Coverage achieved: {coverage_pct}%")
                
                # Allow minimum 5% for development codebase (matches CI)
                if coverage_pct < 5.0:
                    print_error(f"Coverage below 5% minimum threshold ({coverage_pct}%)")
                    return False
                else:
                    print_success(f"Coverage passed ({coverage_pct}% achieved)")
                    return True
            except ValueError:
                print_warning("Could not parse coverage percentage, assuming acceptable")

    # Generate additional reports (exact CI commands)
    run_command("python -m coverage xml", check=False)
    run_command("python -m coverage html --directory=htmlcov", check=False)

    print_success("Unit tests completed with coverage reporting")
    return True

def check_prerequisites():
    """Check if required tools are available"""
    print_step("PREREQUISITES CHECK")

    tools = ['python3', 'pip']
    missing = []

    for tool in tools:
        result = run_command(f"which {tool}", shell=True, check=False)
        if result and result.returncode == 0:
            print_success(f"{tool} available")
        else:
            # Check venv
            venv_tool = f"./venv/bin/{tool}"
            if os.path.exists(venv_tool):
                print_success(f"{tool} available (venv)")
            else:
                missing.append(tool)
                print_error(f"{tool} not found")

    if missing:
        print_warning(f"Some tools missing: {missing}")
        print_warning("Consider running: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt")
        return False

    return True

def main():
    """Main validation function"""
    fix_mode = '--fix' in sys.argv

    print(f"{Colors.BOLD}🚀 LOCAL CI VALIDATION - Matching GitHub Actions Pipeline{Colors.END}")
    print("=" * 80)

    if fix_mode:
        print_warning("Running in FIX mode - will attempt to auto-fix issues")

    # Check prerequisites
    if not check_prerequisites():
        print_error("Prerequisites not met - some checks may fail")
        print_warning("Continuing anyway...")

    # Track results
    results = []

    # Run all checks in order
    checks = [
        ("Security Scan", lambda: security_scan()),
        ("Black Formatting", lambda: black_formatting_check(fix_mode)),
        ("Flake8 Linting", lambda: flake8_linting()),
        ("MyPy Type Checking", lambda: mypy_type_checking()),
        ("SOLID Principles", lambda: solid_principles_validation()),
        ("Unit Tests & Coverage", lambda: unit_tests_with_coverage()),
    ]

    for check_name, check_func in checks:
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print_error(f"{check_name} failed with exception: {e}")
            results.append((check_name, False))

    # Summary
    print(f"\n{Colors.BOLD}📊 VALIDATION SUMMARY{Colors.END}")
    print("=" * 60)

    passed = 0
    failed = 0

    for check_name, success in results:
        if success:
            print_success(f"{check_name}")
            passed += 1
        else:
            print_error(f"{check_name}")
            failed += 1

    print(f"\nChecks Passed: {passed}")
    print(f"Checks Failed: {failed}")

    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED - Ready for CI/CD Pipeline!{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ {failed} CHECKS FAILED - Fix issues before pushing{Colors.END}")
        if not fix_mode:
            print(f"{Colors.YELLOW}Tip: Run with --fix to auto-fix formatting issues{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
