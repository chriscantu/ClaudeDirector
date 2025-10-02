# Task 003: Enable All-Unit-Tests Pre-Commit Hook

## Task Overview
**ID**: TASK-003
**Priority**: P1 (HIGH)
**Estimated Effort**: 1 hour
**Phase**: 3
**Depends On**: TASK-001, TASK-002

## Problem Statement
`.pre-commit-config.yaml` has an `all-unit-tests` hook that is disabled due to pre-existing broken tests. Now that tests are fixed, we need to enable it to prevent future test debt.

**Current State**:
```yaml
# TEMPORARILY DISABLED: Discovered 3 pre-existing broken tests (not blocking this PR)
# TODO: Re-enable all-unit-tests hook after fixing pre-existing test failures
# - id: all-unit-tests
#   name: 🧪 ALL UNIT TESTS (Complete Coverage)
#   entry: python3 -m pytest .claudedirector/tests/unit/ -v --tb=short --maxfail=3
```

## Solution Strategy
1. **Uncomment `all-unit-tests` hook** in `.pre-commit-config.yaml`
2. **Test pre-commit locally** - verify all unit tests run
3. **Update GitHub CI** to run all unit tests (not just P0)
4. **Document in CI_VALIDATION_SYSTEM.md**

## Deliverables
- [ ] `all-unit-tests` hook enabled in `.pre-commit-config.yaml`
- [ ] Pre-commit hook verified locally (all tests pass)
- [ ] GitHub CI workflow updated to run all unit tests
- [ ] `CI_VALIDATION_SYSTEM.md` updated with new coverage

## Acceptance Criteria
- [ ] `git commit` runs all unit tests automatically
- [ ] Pre-commit hook blocks commits if tests fail
- [ ] GitHub CI runs all unit tests (not just P0)
- [ ] Documentation reflects new test coverage

## Architecture Compliance
- ✅ **CI_VALIDATION_SYSTEM.md**: Complete test coverage documented
- ✅ **DRY**: Reuse existing pre-commit infrastructure
- ✅ **BLOAT_PREVENTION**: No new validation systems, enhance existing

## Implementation Notes

### **File: `.pre-commit-config.yaml`**
**Change**:
```yaml
# ENABLED: All unit tests now passing (fixed in PR #XXX)
- id: all-unit-tests
  name: 🧪 ALL UNIT TESTS (Complete Coverage)
  entry: python3 -m pytest .claudedirector/tests/unit/ -v --tb=short --maxfail=3
  language: system
  files: ^\.claudedirector/(lib/.*\.py|tests/unit/.*\.py)$
  pass_filenames: false
  stages: [pre-commit]
  verbose: true
```

### **File: `.github/workflows/unified-ci.yml`**
**Add**:
```yaml
- name: 🧪 Run All Unit Tests
  run: |
    python3 -m pytest .claudedirector/tests/unit/ -v --tb=short
```

---

**Status**: BLOCKED (waiting for TASK-001, TASK-002)
**Next Step**: Enable hook after all tests pass
