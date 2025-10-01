# Task 002: Categorize Failing Unit Tests

## Task Overview
**ID**: TASK-002
**Priority**: P1 (HIGH)
**Estimated Effort**: 4-6 hours
**Phase**: 2
**Depends On**: TASK-001

## Problem Statement
79 unit tests are failing (from audit), but we don't know why:
- **Zombie tests**: Testing deleted/non-existent code → DELETE
- **Outdated tests**: API changed, test not updated → FIX
- **Bugs**: Legitimate code issues → FIX or FILE ISSUE

**Current State**:
- ✅ 3 zombie tests already deleted in PR #168
- ✅ 2 dead code files removed in PR #168
- ❌ 79 failures remain (status unknown)

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
- [ ] Complete audit report (all 79 failures categorized)
- [ ] Zombie tests deleted
- [ ] Outdated tests fixed
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
