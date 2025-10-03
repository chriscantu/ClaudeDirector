# Plan: Fix Broken Unit Tests

## Overview
Comprehensive plan to fix all broken unit tests, address architectural violations, and enable comprehensive pre-commit coverage.

**Date**: October 2025
**Status**: Phase 1 & 2 Complete, Phase 3 In Progress (Option A - Architectural Cleanup)

---

## 🚨 **Critical Architectural Findings** (October 3, 2025)

**Pre-Implementation Review Identified 3 Major Violations**:

1. **❌ VIOLATION: Legacy Test Organization** - 8 root-level tests in wrong directories per PROJECT_STRUCTURE.md
2. **❌ VIOLATION: Task-Specific Test Files** - 2 ephemeral task files mixed with permanent tests
3. **❌ VIOLATION: No Shared Test Fixtures** - Zero conftest.py files (DRY violation)

**Decision: Option A - Architectural Cleanup First**
- **Rationale**: Fixing tests without addressing root organizational issues perpetuates technical debt
- **Impact**: Better foundation, clean patterns for future development
- **Status**: Phase 1 Complete (shared fixtures infrastructure)

---

## Phases

### **Phase 1: Fix Collection Errors (P0)** ⏱️ 1-2 hours
**Objective**: Fix all 5 import errors blocking test collection

**Tasks**:
- See `tasks/task-001-fix-collection-errors.md`

**Deliverables**:
- All unit tests can be collected (0 ImportError)
- Baseline pass/fail count established

---

### **Phase 2: Categorize & Fix Failing Tests (P1)** ⏱️ 4-6 hours  ✅ **COMPLETE**
**Objective**: Audit, categorize, and fix failing unit tests

**Status**: Category A Complete (27 tests fixed)
- ✅ Collection errors fixed (5 → 0)
- ✅ Zombie tests deleted (3 files + dead code)
- ✅ Import path fixes (42 mock patches + 7 imports)
- ✅ API rewrites (test_complexity_analyzer.py, test_decision_orchestrator.py, test_solid_template_engine.py)
- ✅ Pass rate improved: 52% → 59% (182/317 passing)

**Tasks**:
- See `tasks/task-002-categorize-failing-tests.md`
- See `tasks/task-004-category-b-moderate-fixes.md` (In Progress)
- See `tasks/task-005-category-c-error-fixes.md` (Pending)

---

### **Phase 2.5: Architectural Cleanup (Option A)** ⏱️ 2-3 hours ✅ **Phase 1 Complete**
**Objective**: Establish clean architectural foundation before continuing test fixes

**Completed**:
- ✅ **Phase 1.1**: Root conftest.py created (483 lines of shared fixtures)
- ✅ **Phase 1.2**: Component-specific conftest.py files (5 files, 1,305 lines)
- ✅ **Phase 1.3**: Architectural compliance documented
- ✅ **unittest.TestCase standard** documented in TESTING_ARCHITECTURE.md

**Remaining**:
- ⏳ **Phase 2**: Move 8 root-level tests to correct directories
- ⏳ **Phase 3**: Delete 2 ephemeral task test files
- ⏳ **Phase 4**: Validation & documentation

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
