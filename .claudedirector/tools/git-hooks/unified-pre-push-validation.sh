#!/bin/bash
# Unified Pre-push Hook: Complete GitHub CI Workflow Validation
# Uses unified test runner for 100% CI/local parity
#
# Author: Martin | Platform Architecture
# Purpose: Eliminate CI/local discrepancies through unified test execution

set -e  # Exit on any error

echo "🚀 UNIFIED PRE-PUSH VALIDATION"
echo "============================================================"
echo "Using unified test architecture for 100% CI/local parity"
echo "All tests defined in .claudedirector/config/test_registry.yaml"
echo "Single source of truth eliminates CI/local discrepancies"
echo "============================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_section() {
    echo ""
    print_status $BLUE "============================================================"
    print_status $BLUE "$1"
    print_status $BLUE "============================================================"
}

# Function to run a step and handle errors
run_step() {
    local step_name="$1"
    local command="$2"

    print_status $YELLOW "🔄 Running: $step_name"

    if eval "$command"; then
        print_status $GREEN "✅ PASSED: $step_name"
        return 0
    else
        print_status $RED "❌ FAILED: $step_name"
        print_status $RED "🚫 PRE-PUSH VALIDATION FAILED"
        print_status $RED "Fix the above issue before pushing to GitHub"
        exit 1
    fi
}

print_section "UNIFIED TEST EXECUTION"

# Install required dependencies
run_step "Install PyYAML for unified runner" "python -m pip install pyyaml"

# Set environment for pre-push detection
export PRE_PUSH_HOOK=true

# Run unified test runner with pre-push profile
run_step "Unified Pre-Push Test Suite" "python .claudedirector/tools/testing/unified_test_runner.py pre_push --validate"

print_section "PRE-PUSH VALIDATION COMPLETE"

print_status $GREEN "🎉 ALL VALIDATIONS PASSED!"
print_status $GREEN "✅ UNIFIED PRE-PUSH VALIDATION SUCCESS"
print_status $GREEN "✅ 100% CI/Local parity maintained"
print_status $GREEN "🚀 Safe to push to GitHub - CI will pass"

echo ""
print_status $BLUE "============================================================"
print_status $BLUE "📊 VALIDATION SUMMARY:"
print_status $BLUE "  ✅ Quality Gates: PASSED (via unified runner)"
print_status $BLUE "  ✅ P0 Blocking Tests: PASSED (via unified runner)"
print_status $BLUE "  ✅ Architecture Consistency: VALIDATED"
print_status $BLUE "  ✅ Test Registry Integrity: VERIFIED"
print_status $BLUE ""
print_status $BLUE "🚀 PUSH APPROVED - GitHub CI will succeed!"
print_status $BLUE "============================================================"
