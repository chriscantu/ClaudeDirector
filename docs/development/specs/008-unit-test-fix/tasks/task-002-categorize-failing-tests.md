# Task 002: Categorize Failing Unit Tests

## Task Overview
**ID**: TASK-002
**Priority**: P1 (HIGH)
**Estimated Effort**: 4-6 hours
**Phase**: 2 (Category A: COMPLETED, Categories B/C: PENDING)
**Depends On**: TASK-001 ✅

## Completion Status (Category A)
**Status**: ✅ **CATEGORY A COMPLETED** (October 2, 2025)

**Category A Results** (Import Path Quick Wins):
- **49 import path issues fixed** across 9 test files
- **16 tests now passing** (was 166, now 182)
- **28 fewer failures** (was 99, now 71)
- **Pass rate improvement**: 54% → 60% (+6%)
- **Time Taken**: 45 minutes (as estimated)

See: `CATEGORY-A-COMPLETION.md` for detailed report.

**Remaining Work**:
- **Category B**: 71 failing tests (moderate complexity)
- **Category C**: 29 error tests (blocking execution)

---

## Problem Statement
71 unit tests are still failing, but we don't know why:
- **Zombie tests**: Testing deleted/non-existent code → DELETE
- **Outdated tests**: API changed, test not updated → FIX
- **Bugs**: Legitimate code issues → FIX or FILE ISSUE

**Current State** (as of PR #169):
- ✅ **Category A COMPLETE**: 49 import path fixes (16 tests fixed)
- ✅ 3 zombie tests deleted in PR #168
- ✅ 2 dead code files removed in PR #168
- ❌ **71 failures remain** (Category B - moderate complexity)
- ❌ **29 errors remain** (Category C - blocking execution)

## Solution Strategy
1. **Run all unit tests** after TASK-001 fixes
2. **Categorize each failure** using triage criteria
3. **Delete zombie tests** (follow BLOAT_PREVENTION)
4. **Fix outdated tests** (update to current API)
5. **File issues for bugs** (non-critical bugs)

## Triage Criteria

### **Zombie Test** → DELETE
- Tests import non-existent modules
- Tests reference deleted classes/functions
- Tests validate removed features
- **Action**: DELETE test file, document in PR

### **Outdated Test** → FIX
- Tests fail due to API signature changes
- Tests use deprecated patterns
- Tests have incorrect assertions (API behavior changed)
- **Action**: Update test to match current API

### **Bug** → FIX or FILE ISSUE
- Tests fail due to code bugs
- Tests expose architectural issues
- **Action**: Fix P0 bugs immediately, file issues for others

## Deliverables
- [x] **Category A (Quick Wins)**: Import path fixes ✅ **COMPLETED**
- [ ] Category B (Moderate): Complex integration tests (71 failures)
- [ ] Category C (Errors): Blocking ERROR tests (29 errors)
- [ ] Bug issues filed (if non-critical)
- [ ] Updated `.pre-commit-config.yaml` with new baseline

## Acceptance Criteria
- [ ] All 79 failures triaged and categorized
- [ ] Zombie tests removed from codebase
- [ ] Outdated tests updated to pass
- [ ] No more than 10 failures remain (legitimate bugs)
- [ ] Issues filed for all remaining bugs

## Architecture Compliance
- ✅ **BLOAT_PREVENTION**: Delete zombie tests, no unnecessary code
- ✅ **DRY**: Fix tests using current abstractions
- ✅ **SOLID**: Tests validate single units with clear responsibilities

---

**Status**: BLOCKED (waiting for TASK-001)
**Next Step**: Run full unit test suite after TASK-001 complete
