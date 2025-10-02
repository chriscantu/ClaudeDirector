# Task 005: Category C - Error Test Fixes (Blocking Execution)

## Task Overview
**ID**: TASK-005
**Priority**: P1 (HIGH)
**Estimated Effort**: 6-8 hours
**Phase**: 2C (Category C - Error Tests)
**Depends On**: TASK-004 (Category B) ✅

## Objective
Fix the **29 error tests** that are blocking test execution. These tests fail during the collection or setup phase, preventing pytest from even running them.

## Current Status
**Status**: ⏳ **PENDING** (waiting for Category B completion)

**Starting Point** (after Category B completion):
- **250+ passing tests** (82%+ pass rate)
- **<5 failing tests**
- **29 error tests** (blocking execution)
- **23 skipped tests**

**Target**:
- **280+ passing tests** (92%+ pass rate)
- **0 error tests** (all tests collectable and executable)
- **Enable all-unit-tests pre-commit hook**

---

## Problem Statement

We have **29 tests with ERROR status** that prevent pytest from executing them. These are more serious than failures because they block the test runner.

### **Error Categories**

#### **C1: Import Errors** (~15 tests)
Tests that fail during import due to:
- Missing dependencies
- Circular imports
- Module not found errors

**Example**:
```python
# ERROR during collection
ImportError: cannot import name 'OldClass' from 'lib.core.module'
```

#### **C2: Fixture Errors** (~8 tests)
Tests that fail during fixture setup:
- Fixture not found
- Fixture initialization fails
- Fixture dependency issues

**Example**:
```python
# ERROR during setup
fixture 'deprecated_fixture' not found
```

#### **C3: Parametrization Errors** (~4 tests)
Tests with invalid parametrize decorators:
- Invalid parameter format
- Missing parameter values
- Type mismatches

**Example**:
```python
# ERROR during collection
@pytest.mark.parametrize("input,expected", [...])  # Missing values
```

#### **C4: Class/Module Errors** (~2 tests)
Tests with class or module-level issues:
- Invalid test class structure
- Module-level exceptions
- Invalid test discovery

---

## Approach

### **Phase 1: Error Analysis** (1-2 hours)
1. **Collect all error messages**: `pytest --tb=short -v 2>&1 | grep ERROR`
2. **Categorize each error** into C1, C2, C3, or C4
3. **Identify root causes**: Missing code, config issues, or test design problems
4. **Create fix plan**: Prioritize by severity and impact

### **Phase 2: Systematic Error Fixes** (4-5 hours)

#### **C1: Import Error Fixes** (2 hours)
1. **Identify missing imports**: Check if modules exist in production
2. **Fix circular imports**: Refactor import structure if needed
3. **Update absolute imports**: Ensure correct import paths
4. **Delete obsolete tests**: If code no longer exists

#### **C2: Fixture Error Fixes** (1-2 hours)
1. **Review fixture definitions**: Check `conftest.py` files
2. **Fix fixture dependencies**: Update fixture chains
3. **Replace deprecated fixtures**: Use current fixture patterns
4. **Update fixture scopes**: Ensure correct scope (function/module/session)

#### **C3: Parametrization Fixes** (30 minutes)
1. **Fix parameter formats**: Ensure valid pytest syntax
2. **Add missing values**: Complete parameter lists
3. **Fix type mismatches**: Ensure parameter types are correct

#### **C4: Class/Module Fixes** (30 minutes)
1. **Fix test class structure**: Ensure proper inheritance
2. **Fix module-level issues**: Remove blocking exceptions
3. **Update test discovery**: Ensure tests are discoverable

### **Phase 3: Validation & Hook Enablement** (1-2 hours)
1. **Run full test suite**: Verify 280+ passing (92%+ pass rate)
2. **Verify 0 errors**: `pytest --collect-only` should show no errors
3. **Run P0 tests**: Ensure 42/42 still passing
4. **Enable all-unit-tests hook**: Uncomment in `.pre-commit-config.yaml`
5. **Test hook**: `pre-commit run all-unit-tests --all-files`

---

## Success Criteria

- [ ] **0 error tests** (down from 29)
- [ ] **Pass rate ≥92%** (280+ tests passing out of 305)
- [ ] **42/42 P0 tests passing** (maintain P0 integrity)
- [ ] **all-unit-tests hook enabled** in `.pre-commit-config.yaml`
- [ ] **Hook passes**: `pre-commit run all-unit-tests --all-files`
- [ ] **CATEGORY-C-COMPLETION.md** created with detailed report

---

## Deliverables

1. **Fixed test files** (estimated 10-15 files modified)
2. **Updated `.pre-commit-config.yaml`** - Enable all-unit-tests hook
3. **CATEGORY-C-COMPLETION.md** - Detailed completion report
4. **Updated task-002-categorize-failing-tests.md** - Mark Category C complete
5. **Updated task-003-enable-all-tests-hook.md** - Mark as complete
6. **Commit and push** to PR (feature/fix-unit-tests-categories-bc)

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Error tests are unfixable** | MEDIUM | Document as known issues; skip in hook |
| **New errors introduced** | HIGH | Run `pytest --collect-only` after each fix |
| **Hook blocks commits** | CRITICAL | Test hook thoroughly before enabling |
| **Time overrun (>8 hours)** | LOW | Focus on fixable errors; document blockers |

---

## Architecture Compliance

- ✅ **DRY**: Reuse existing fixtures and test utilities
- ✅ **SOLID-SRP**: Each test validates one specific behavior
- ✅ **PROJECT_STRUCTURE**: All tests remain in `.claudedirector/tests/unit/`
- ✅ **BLOAT_PREVENTION**: Delete any tests that are permanently broken

---

## Final Validation Steps

After Category C completion, the unit test suite should be:

1. **✅ 280+ tests passing** (92%+ pass rate)
2. **✅ 0 error tests** (all collectable)
3. **✅ <5 failing tests** (documented and tracked)
4. **✅ 42/42 P0 tests passing** (100% P0 integrity)
5. **✅ all-unit-tests hook enabled** (enforces test quality)

---

## Next Steps (After Completion)

1. **Merge PR**: Complete unit test fix initiative
2. **Monitor**: Ensure hook doesn't block legitimate work
3. **Iterate**: Fix remaining <5 failures in follow-up PRs
4. **Celebrate**: Unit test suite is now robust and comprehensive! 🎉

---

**Status**: ⏳ **PENDING** - Waiting for Category B completion
**Next Action**: Begin after Task 004 (Category B) is complete
