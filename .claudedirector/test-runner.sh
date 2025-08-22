#!/bin/bash

# ClaudeDirector Test Runner
# Comprehensive testing script for MCP integration with quality gates

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TESTS_DIR="$SCRIPT_DIR/tests"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Test categories
run_unit_tests() {
    log_info "Running unit tests..."

    if [ -d "$TESTS_DIR/unit" ]; then
        cd "$PROJECT_ROOT"

        # Set PYTHONPATH to include our modules
        export PYTHONPATH="$SCRIPT_DIR/lib:$PYTHONPATH"

        # Run unit tests with coverage
        python -m pytest "$TESTS_DIR/unit" -v --tb=short --cov="$SCRIPT_DIR/lib" --cov-report=term-missing --cov-fail-under=90

        if [ $? -eq 0 ]; then
            log_success "Unit tests passed"
        else
            log_error "Unit tests failed"
            return 1
        fi
    else
        log_warning "Unit tests directory not found"
    fi
}

run_regression_tests() {
    log_info "Running regression tests..."

    if [ -d "$TESTS_DIR/regression" ]; then
        cd "$PROJECT_ROOT"
        export PYTHONPATH="$SCRIPT_DIR/lib:$PYTHONPATH"

        python -m pytest "$TESTS_DIR/regression" -v --tb=short

        if [ $? -eq 0 ]; then
            log_success "Regression tests passed"
        else
            log_error "Regression tests failed"
            return 1
        fi
    else
        log_warning "Regression tests directory not found"
    fi
}

run_policy_tests() {
    log_info "Running policy validation tests..."

    if [ -d "$TESTS_DIR/policy" ]; then
        cd "$PROJECT_ROOT"
        export PYTHONPATH="$SCRIPT_DIR/lib:$PYTHONPATH"

        python -m pytest "$TESTS_DIR/policy" -v --tb=short

        if [ $? -eq 0 ]; then
            log_success "Policy validation passed"
        else
            log_error "Policy validation failed"
            return 1
        fi
    else
        log_warning "Policy tests directory not found"
    fi
}

run_integration_tests() {
    log_info "Running integration tests..."

    if [ -d "$TESTS_DIR/integration" ]; then
        cd "$PROJECT_ROOT"
        export PYTHONPATH="$SCRIPT_DIR/lib:$PYTHONPATH"

        python -m pytest "$TESTS_DIR/integration" -v --tb=short

        if [ $? -eq 0 ]; then
            log_success "Integration tests passed"
        else
            log_error "Integration tests failed"
            return 1
        fi
    else
        log_warning "Integration tests directory not found"
    fi
}

run_performance_tests() {
    log_info "Running performance tests..."

    if [ -d "$TESTS_DIR/performance" ]; then
        cd "$PROJECT_ROOT"
        export PYTHONPATH="$SCRIPT_DIR/lib:$PYTHONPATH"

        python -m pytest "$TESTS_DIR/performance" -v --tb=short

        if [ $? -eq 0 ]; then
            log_success "Performance tests passed"
        else
            log_error "Performance tests failed"
            return 1
        fi
    else
        log_warning "Performance tests directory not found"
    fi
}

# Quality Gates
regression_gate() {
    log_info "=== REGRESSION GATE ==="

    run_regression_tests
    if [ $? -ne 0 ]; then
        log_error "REGRESSION GATE FAILED"
        return 1
    fi

    log_success "REGRESSION GATE PASSED"
    return 0
}

policy_gate() {
    log_info "=== POLICY GATE ==="

    run_policy_tests
    if [ $? -ne 0 ]; then
        log_error "POLICY GATE FAILED"
        return 1
    fi

    log_success "POLICY GATE PASSED"
    return 0
}

performance_gate() {
    log_info "=== PERFORMANCE GATE ==="

    run_performance_tests
    if [ $? -ne 0 ]; then
        log_error "PERFORMANCE GATE FAILED"
        return 1
    fi

    log_success "PERFORMANCE GATE PASSED"
    return 0
}

# Comprehensive test suites
run_sprint1_validation() {
    log_info "=== SPRINT 1 VALIDATION ==="

    # Foundation tests
    run_unit_tests || return 1

    # Quality gates
    regression_gate || return 1
    policy_gate || return 1

    log_success "SPRINT 1 VALIDATION PASSED"
}

run_sprint2_validation() {
    log_info "=== SPRINT 2 VALIDATION ==="

    # All previous tests
    run_sprint1_validation || return 1

    # Enhanced functionality tests
    run_integration_tests || return 1
    performance_gate || return 1

    log_success "SPRINT 2 VALIDATION PASSED"
}

run_comprehensive_validation() {
    log_info "=== COMPREHENSIVE VALIDATION ==="

    # All test categories
    run_unit_tests || return 1
    run_integration_tests || return 1
    run_regression_tests || return 1
    run_policy_tests || return 1
    run_performance_tests || return 1

    log_success "COMPREHENSIVE VALIDATION PASSED"
}

# Individual test execution based on arguments
case "$1" in
    --unit)
        run_unit_tests
        ;;
    --regression)
        run_regression_tests
        ;;
    --policy)
        run_policy_tests
        ;;
    --integration)
        run_integration_tests
        ;;
    --performance)
        run_performance_tests
        ;;
    --sprint1)
        run_sprint1_validation
        ;;
    --sprint2)
        run_sprint2_validation
        ;;
    --comprehensive)
        run_comprehensive_validation
        ;;
    --regression-gate)
        regression_gate
        ;;
    --policy-gate)
        policy_gate
        ;;
    --performance-gate)
        performance_gate
        ;;
    *)
        echo "Usage: $0 [--unit|--regression|--policy|--integration|--performance|--sprint1|--sprint2|--comprehensive|--regression-gate|--policy-gate|--performance-gate]"
        echo ""
        echo "Test Categories:"
        echo "  --unit           Run unit tests with coverage"
        echo "  --regression     Run regression tests"
        echo "  --policy         Run policy validation tests"
        echo "  --integration    Run integration tests"
        echo "  --performance    Run performance tests"
        echo ""
        echo "Quality Gates:"
        echo "  --regression-gate  Execute regression quality gate"
        echo "  --policy-gate      Execute policy quality gate"
        echo "  --performance-gate Execute performance quality gate"
        echo ""
        echo "Sprint Validation:"
        echo "  --sprint1        Run Sprint 1 validation suite"
        echo "  --sprint2        Run Sprint 2 validation suite"
        echo "  --comprehensive  Run all tests and quality gates"
        echo ""
        exit 1
        ;;
esac
