# Plan: Fix Broken Unit Tests

## Overview
3-phase plan to fix all broken unit tests and enable comprehensive pre-commit coverage.

## Phases

### **Phase 1: Fix Collection Errors (P0)** ⏱️ 1-2 hours
**Objective**: Fix all 5 import errors blocking test collection

**Tasks**:
- See `tasks/task-001-fix-collection-errors.md`

**Deliverables**:
- All unit tests can be collected (0 ImportError)
- Baseline pass/fail count established

---

### **Phase 2: Categorize Failing Tests (P1)** ⏱️ 4-6 hours
**Objective**: Audit and categorize all failing unit tests

**Tasks**:
- See `tasks/task-002-categorize-failing-tests.md`

**Deliverables**:
- Complete audit report (zombie vs outdated vs bugs)
- Zombie tests deleted
- Outdated tests fixed or issues filed

---

### **Phase 3: Enable All-Unit-Tests Hook (P1)** ⏱️ 1 hour
**Objective**: Enable comprehensive pre-commit test coverage

**Tasks**:
- See `tasks/task-003-enable-all-tests-hook.md`

**Deliverables**:
- `all-unit-tests` pre-commit hook enabled
- CI enhanced to run all unit tests

---

## Timeline
- **Phase 1**: Immediate (blocks all other work)
- **Phase 2**: After Phase 1 complete
- **Phase 3**: After Phase 2 complete

## Total Effort
**Estimated**: 6-9 hours
**Priority**: P0 (critical infrastructure)
