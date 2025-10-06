# Task 004: Category B - Moderate Complexity Test Fixes

## Task Overview
**ID**: TASK-004
**Priority**: P2 (MEDIUM)
**Estimated Effort**: 8-12 hours
**Phase**: 2B (Category B - Moderate Complexity)
**Depends On**: TASK-002 (Category A) ✅

## Objective
Fix the remaining **71 failing unit tests** that require moderate complexity fixes. These tests have correct imports but fail due to:
- Outdated API usage
- Changed method signatures
- Mock/fixture issues
- Assertion mismatches

## Current Status
**Status**: 🔄 **IN PROGRESS**

**Starting Point** (after Category A completion):
- **182 passing tests** (60% pass rate)
- **71 failing tests** (moderate complexity)
- **29 error tests** (will be addressed in Task 005)
- **23 skipped tests**

**Target**:
- **250+ passing tests** (82%+ pass rate)
- **<5 failing tests**
- **Address all moderate complexity issues**

---

## Problem Statement

After Category A import path fixes, we still have **71 failing tests** that require more substantial refactoring:

### **Failure Categories**

#### **B1: Outdated API Usage** (~30 tests)
Tests using old method signatures or deprecated APIs that need updates to match current production code.

**Example**:
```python
# Test expects old API
result = analyzer.analyze(complexity="COMPLEX")

# Production now uses
result = analyzer.analyze(complexity_threshold="medium")
```

#### **B2: Mock/Fixture Issues** (~20 tests)
Tests with mocks that don't match current implementation or fixtures that no longer align with production data structures.

**Example**:
```python
# Mock doesn't match actual method signature
mock_engine.process.return_value = {"status": "ok"}

# Actual implementation returns
UnifiedResponse(success=True, data={...})
```

#### **B3: Assertion Mismatches** (~15 tests)
Tests with assertions that are too strict or don't account for current business logic.

**Example**:
```python
# Test expects exact match
assert result.complexity == "COMPLEX"

# Production now returns
assert result.complexity == "MEDIUM"  # Updated threshold logic
```

#### **B4: Integration Test Issues** (~6 tests)
Tests that require multiple components to be mocked/configured correctly.

---

## Approach

### **Phase 0: Pre-Implementation Architecture Validation** (30 minutes)
**Purpose**: Ensure compliance with TESTING_ARCHITECTURE.md and BLOAT_PREVENTION_SYSTEM.md

1. **Validate test architecture consistency**:
   ```python
   from .claudedirector.tests.p0_enforcement.run_mandatory_p0_tests import P0TestEnforcer
   enforcer = P0TestEnforcer()

   # Ensure test architecture is consistent
   if not enforcer.validate_test_files_exist():
       raise ArchitectureViolation("Test file structure inconsistent")
   ```

2. **Scan for test utility duplication**:
   ```bash
   # Check existing test utilities (BLOAT_PREVENTION compliance)
   python .claudedirector/tools/architecture/bloat_prevention_system.py .claudedirector/tests/

   # Inventory existing fixtures in conftest.py
   grep -r "^def \|^class " .claudedirector/tests/conftest.py
   ```

3. **Document reusable components**:
   - List existing test utilities to reuse
   - Identify gaps where new utilities are needed
   - Justify any new utility creation

4. **Validate PROJECT_STRUCTURE compliance**:
   - Confirm all tests in `.claudedirector/tests/unit/`
   - Check no tests in wrong directories
   - Verify test naming conventions

### **Phase 1: Triage & Analysis** (2 hours)
1. **Validate test architecture** using P0TestEnforcer (REQUIRED)
2. **Run full test suite** and capture detailed failure output
3. **Categorize each failure** into B1, B2, B3, or B4
4. **Identify common patterns** (e.g., all tests in one file use old API)
5. **Prioritize by impact** (fix files with most failures first)

### **Phase 2: Systematic Fixes** (6-8 hours)
Fix tests systematically by category:

#### **B1: API Updates** (3 hours)
1. Identify production API changes (grep for method signatures)
2. Update test calls to match current API
3. Verify test logic still validates correct behavior

#### **B2: Mock Updates** (2-3 hours)
1. **FIRST: Check existing mock patterns** in conftest.py (DRY compliance)
2. **REUSE existing mocks** where possible
3. Review production implementations for new mocks needed
4. Update mocks to match current signatures
5. Update return values to match UnifiedResponse patterns
6. **Document new mocks** and justify why existing ones don't work

#### **B3: Assertion Updates** (1-2 hours)
1. Review business logic changes
2. Update assertions to match current expected behavior
3. Document why assertions changed (in test docstrings)

#### **B4: Integration Fixes** (1-2 hours)
1. Fix component interaction issues
2. Update test fixtures to match current data structures
3. Ensure proper cleanup/teardown

### **Phase 3: Validation & Integration** (2-3 hours)
**Purpose**: Unified test runner integration and environment parity validation

1. **Run unified test suite** (REQUIRED - TESTING_ARCHITECTURE.md compliance):
   ```python
   # Use unified test runner (not manual pytest)
   python .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py --unit-tests
   ```

2. **Verify pass rate**: Confirm 250+ passing (82%+ pass rate)

3. **Validate environment parity**:
   - Local results match expected CI behavior
   - Test discovery is consistent
   - No "works locally, fails in CI" risks

4. **Run bloat prevention validation**:
   ```bash
   python .claudedirector/tools/architecture/bloat_prevention_system.py .claudedirector/tests/
   ```

5. **P0 test validation** (42/42 must pass):
   ```bash
   python .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py
   ```

6. **Update P0 registry** (if needed):
   - Add unit test suite integrity to `p0_test_definitions.yaml`
   - Document pass rate requirements

7. **Review changes**: Ensure no test logic was lost

8. **Documentation**: Update CATEGORY-B-COMPLETION.md with:
   - Test architecture validation results
   - Bloat prevention scan results
   - Environment parity confirmation
   - Unified runner integration status

---

## Success Criteria

- [ ] **Pass rate ≥82%** (250+ tests passing out of 305)
- [ ] **Failing tests <5** (down from 71)
- [ ] **42/42 P0 tests passing** (maintain P0 integrity)
- [ ] **All Category B tests fixed or documented**
- [ ] **Zero architectural violations**
- [ ] **CATEGORY-B-COMPLETION.md** created with detailed report

---

## Deliverables

1. **Fixed test files** (estimated 15-20 files modified)
2. **CATEGORY-B-COMPLETION.md** - Detailed completion report
3. **Updated task-002-categorize-failing-tests.md** - Mark Category B complete
4. **Commit and push** to PR (feature/fix-unit-tests-categories-bc)

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Test logic lost during fix** | HIGH | Review each test carefully; preserve original intent in docstrings |
| **New failures introduced** | MEDIUM | Run full test suite after each batch of fixes |
| **P0 tests broken** | CRITICAL | Run P0 tests after every commit |
| **Time overrun (>12 hours)** | LOW | Focus on high-impact files first; document remaining work |

---

## Architecture Compliance

### **TESTING_ARCHITECTURE.md Compliance** (ENFORCED)
- ✅ **Phase 0**: Validate test architecture consistency using P0TestEnforcer
- ✅ **Phase 3**: Use unified test runner (not manual pytest) for environment parity
- ✅ **Integration**: Update p0_test_definitions.yaml if needed
- ✅ **Unified Runner**: All validation uses `run_mandatory_p0_tests.py`

### **BLOAT_PREVENTION_SYSTEM.md Compliance** (ENFORCED)
- ✅ **Phase 0**: Scan existing test utilities before creating new ones
- ✅ **Phase 2**: Reuse existing fixtures and mocks from conftest.py
- ✅ **Phase 3**: Run bloat prevention validation before commit
- ✅ **Documentation**: Track all reused vs new utilities

### **Core Principles**
- ✅ **DRY**: Reuse existing test utilities and fixtures (validated in Phase 0)
- ✅ **SOLID-SRP**: Each test validates one specific behavior
- ✅ **PROJECT_STRUCTURE**: All tests remain in `.claudedirector/tests/unit/`
- ✅ **Environment Parity**: Local === CI execution (validated in Phase 3)

---

## Next Steps (After Completion)

1. **Task 005**: Category C - Fix 29 error tests (blocking execution)
2. **Task 003**: Enable all-unit-tests pre-commit hook
3. **Merge PR**: Complete unit test fix initiative

---

**Status**: 🔄 **READY TO START** - Category A foundation complete
**Next Action**: Begin Phase 1 - Triage & Analysis
