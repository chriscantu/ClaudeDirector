# Spec: Fix Broken Unit Tests

## Executive Summary
**Status**: 🚨 **CRITICAL** - 5 unit tests with collection errors, blocking CI enhancement
**Objective**: Fix all broken unit tests to enable comprehensive pre-commit coverage
**Target**: 100% unit test collection success, 0 import errors

## Problem Statement
PR #168 identified systemic unit test failures when attempting to run all unit tests (not just P0):
- **5 collection errors** (import failures)
- **79 failing unit tests** (pre-existing, from audit)
- **3 zombie tests deleted** (tested non-existent code)
- **2 dead code files removed** (never imported, broken)

**Current CI Gap**: GitHub CI only runs P0 tests, allowing non-P0 failures to accumulate undetected.

**Business Impact**:
- ❌ Cannot enable `all-unit-tests` pre-commit hook
- ❌ False confidence in test coverage (122 passing ≠ all tests)
- ❌ Technical debt accumulation in test suite
- ❌ Import errors indicate architectural issues

## Root Cause Analysis

### **Issue 1: Import Path Errors (5 tests)**
**Affected Tests**:
1. `test_prompt_cache_optimizer.py` - Cannot import `performance_config` from `lib.config`
2. `test_complexity_analyzer.py` - Import failure (TBD)
3. `test_mcp_use_client.py` - Import failure (TBD)
4. `test_persona_activation_engine.py` - Import failure (TBD)
5. `test_template_commands.py` - Import failure (TBD)

**Root Cause**: Configuration file moved from `lib/config/` to `config/` in PR #168, but imports not updated.

### **Issue 2: Failing Unit Tests (79 tests)**
**Status**: Requires audit to determine:
- Zombie tests (testing deleted code)
- Outdated tests (API changed, test not updated)
- Legitimate failures (code bugs)

## Success Criteria
- [x] All 5 collection errors resolved
- [ ] Import paths corrected for moved configuration files
- [ ] All unit tests can be collected (no ImportError)
- [ ] Failing tests categorized (zombie vs outdated vs bugs)
- [ ] `all-unit-tests` pre-commit hook enabled
- [ ] CI enhanced to run all unit tests (not just P0)

## Architecture Compliance

### **BLOAT_PREVENTION_SYSTEM.md**
- ✅ Delete zombie tests (already done: 3 deleted)
- ✅ Delete dead code (already done: `DailyPlanningManager`, `daily_planning_config.py`)
- ✅ No new test code duplication

### **PROJECT_STRUCTURE.md**
- ✅ Configuration in `.claudedirector/config/` (canonical location)
- ✅ Tests in `.claudedirector/tests/unit/`
- ✅ Update imports to absolute paths

### **SOLID Principles**
- ✅ Single Responsibility: Each test validates one unit
- ✅ Dependency Inversion: Tests depend on abstractions, not implementations

## Implementation Strategy

### **Phase 1: Fix Collection Errors (P0)**
**Priority**: CRITICAL - Blocks all unit test execution
**Effort**: 1-2 hours

**Tasks**:
1. Audit all 5 failing tests for import errors
2. Update import paths to use canonical config location
3. Verify all tests can be collected successfully
4. Run all unit tests to establish baseline pass/fail counts

### **Phase 2: Categorize Failing Tests (P1)**
**Priority**: HIGH - Required for CI enhancement
**Effort**: 4-6 hours

**Tasks**:
1. Run all unit tests, capture failures
2. Categorize each failure:
   - **Zombie**: Tests non-existent code → DELETE
   - **Outdated**: API changed, test not updated → FIX
   - **Bug**: Legitimate code issue → FIX or FILE ISSUE
3. Document findings in `plan.md`

### **Phase 3: Enable All-Unit-Tests Hook (P1)**
**Priority**: HIGH - Prevents future test debt
**Effort**: 1 hour

**Tasks**:
1. Uncomment `all-unit-tests` hook in `.pre-commit-config.yaml`
2. Verify pre-commit runs all unit tests successfully
3. Update CI to run all unit tests (not just P0)

## Definition of Done
- [ ] All 5 collection errors fixed
- [ ] All unit tests can be collected (0 import errors)
- [ ] Failing tests categorized and documented
- [ ] Zombie tests deleted
- [ ] `all-unit-tests` pre-commit hook enabled
- [ ] CI runs all unit tests
- [ ] PR approved and merged

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|-----------|
| More zombie tests discovered | HIGH | Delete systematically, follow BLOAT_PREVENTION |
| Legitimate bugs found | MEDIUM | File issues for non-critical bugs, fix P0 bugs immediately |
| Performance impact (long test runs) | LOW | Optimize with parallel execution, caching |

---

**Created**: October 1, 2025
**Author**: Martin (Platform Architecture)
**Status**: DRAFT - Awaiting implementation
