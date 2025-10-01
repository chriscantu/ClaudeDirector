# Task 001: Fix Unit Test Collection Errors

## Task Overview
**ID**: TASK-001
**Priority**: P0 (CRITICAL)
**Estimated Effort**: 1-2 hours
**Phase**: 1

## Problem Statement
5 unit tests have collection errors (ImportError), blocking all unit test execution:
1. `test_prompt_cache_optimizer.py` - Cannot import `performance_config`
2. `test_complexity_analyzer.py` - Import failure
3. `test_mcp_use_client.py` - Import failure
4. `test_persona_activation_engine.py` - Import failure
5. `test_template_commands.py` - Import failure

## Root Cause
Configuration file `performance_config.py` was moved from `lib/config/` to `config/` in PR #168, but some imports were not updated to reflect the new canonical location.

## Solution Strategy
1. **Audit all 5 tests** for specific import errors
2. **Update import paths** to use absolute imports from `.claudedirector.config`
3. **Add fallback imports** for test isolation (if needed)
4. **Verify collection** - all tests should collect successfully

## Deliverables
- [ ] All 5 tests can be collected (0 ImportError)
- [ ] Import paths use canonical config location
- [ ] All tests run (pass or fail reported, not blocked)
- [ ] Baseline test status documented

## Acceptance Criteria
- [x] `pytest .claudedirector/tests/unit/ --collect-only` runs without errors
- [ ] All unit tests can be executed
- [ ] No import errors
- [ ] Baseline pass/fail count established

## Architecture Compliance
- ✅ **PROJECT_STRUCTURE.md**: Use canonical config location (`.claudedirector/config/`)
- ✅ **DRY**: No duplicate configuration files
- ✅ **BLOAT_PREVENTION**: No new code, just import path fixes

## Implementation Notes
**Files to Update**:
1. `.claudedirector/tests/unit/performance/test_prompt_cache_optimizer.py`
2. `.claudedirector/tests/unit/test_complexity_analyzer.py`
3. `.claudedirector/tests/unit/test_mcp_use_client.py`
4. `.claudedirector/tests/unit/test_persona_activation_engine.py`
5. `.claudedirector/tests/unit/test_template_commands.py`

**Expected Fix Pattern**:
```python
# OLD (broken after PR #168):
from lib.config.performance_config import get_prompt_caching_config

# NEW (canonical location):
from claudedirector.config.performance_config import get_prompt_caching_config
```

---

**Status**: 🚧 IN PROGRESS
**Next Step**: Audit import errors for all 5 tests
