#!/bin/bash
"""
Regression Test Enforcement Hook

CRITICAL: This hook cannot be bypassed with --no-verify or any other mechanism.
Enforces mandatory regression tests before ANY commit reaches GitHub.

This hook is called from multiple points to ensure it cannot be circumvented:
1. Pre-commit hook (early detection)
2. Pre-push hook (final validation)
3. CI/CD pipeline (server-side validation)
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️ REGRESSION TEST ENFORCEMENT SYSTEM${NC}"
echo "============================================================"
echo -e "${YELLOW}MANDATORY: These tests protect against SOLID refactoring regressions${NC}"
echo -e "${RED}CANNOT BE BYPASSED: No --no-verify, no exceptions${NC}"
echo "============================================================"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Change to project root
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f ".claudedirector/tests/regression/run_complete_regression_suite.py" ]; then
    echo -e "${RED}❌ ERROR: Regression test suite not found${NC}"
    echo "Expected: .claudedirector/tests/regression/run_complete_regression_suite.py"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Run regression tests with timeout and detailed output
echo -e "${BLUE}🧪 EXECUTING MANDATORY REGRESSION TESTS...${NC}"
echo ""

if timeout 600 python .claudedirector/tests/regression/run_complete_regression_suite.py; then
    echo ""
    echo -e "${GREEN}✅ ALL REGRESSION TESTS PASSED${NC}"
    echo -e "${GREEN}🎯 COMMIT APPROVED - Safe to proceed${NC}"
    exit 0
else
    exit_code=$?
    echo ""
    echo -e "${RED}❌ REGRESSION TESTS FAILED${NC}"
    echo -e "${RED}🚫 COMMIT BLOCKED${NC}"
    echo ""
    echo -e "${YELLOW}📋 TROUBLESHOOTING STEPS:${NC}"
    echo "1. Run individual tests to identify issues:"
    echo "   python .claudedirector/tests/regression/test_configuration_integrity.py"
    echo "   python .claudedirector/tests/regression/test_framework_engine_regression.py"
    echo ""
    echo "2. Fix any failing tests before attempting to commit"
    echo ""
    echo "3. Re-run the complete test suite:"
    echo "   python .claudedirector/tests/regression/run_complete_regression_suite.py"
    echo ""
    echo -e "${RED}⚠️ IMPORTANT ENFORCEMENT NOTES:${NC}"
    echo -e "${RED}🚫 --no-verify will NOT bypass these tests${NC}"
    echo -e "${RED}🚫 These tests run in CI and will block deployment${NC}"
    echo -e "${RED}🚫 No exceptions - all regression tests must pass${NC}"
    echo ""
    exit $exit_code
fi
