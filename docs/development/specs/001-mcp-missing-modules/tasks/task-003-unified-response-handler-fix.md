# Task 003: Unified Response Handler Import Fix

## Task Overview
**ID**: TASK-003
**Component**: Import path correction for `unified_response_handler`
**Priority**: P0 (Critical import failure)
**Estimated Effort**: 30 minutes

## Context7 Pattern Applied
**Pattern**: **Import Path Correction** + **Dependency Resolution**
**Rationale**: Fix incorrect import path that's causing module loading failures

## BLOAT_PREVENTION_SYSTEM.md Compliance

### ✅ Root Cause Analysis
**EXISTING FUNCTIONALITY CONFIRMED**:
```python
# CURRENT LOCATION: .claudedirector/lib/performance/__init__.py
# Lines 188-201: Unified Response functionality (consolidated from unified_response_handler.py)
"UnifiedResponseHandler",
"UnifiedResponse",
"ResponseStatus",
"ResponseType",
"get_unified_response_handler",
"get_unified_manager",
"create_mcp_response",
"create_persona_response",
"create_fallback_response",
```

**PROBLEM**: Code trying to import from non-existent `lib.performance.unified_response_handler`
**SOLUTION**: Update imports to use consolidated `lib.performance` module

## Implementation Strategy

### Step 1: Identify Incorrect Import References
```bash
# Search for problematic imports
grep -r "lib.performance.unified_response_handler" .claudedirector/lib/
```

### Step 2: Correct Import Statements
```python
# INCORRECT (causing failures):
from lib.performance.unified_response_handler import (
    create_fallback_response,
    UnifiedResponse,
    ResponseStatus,
)

# CORRECT (existing consolidated module):
from lib.performance import (
    create_fallback_response,
    UnifiedResponse,
    ResponseStatus,
)
```

### Step 3: Validate Existing Functionality
**NO NEW CODE NEEDED** - functionality already exists in consolidated form:
- `UnifiedResponse` dataclass ✅
- `ResponseStatus` enum ✅
- `create_fallback_response()` function ✅
- `create_mcp_response()` function ✅
- `create_persona_response()` function ✅

## Files Requiring Import Updates

### Confirmed Files with Incorrect Imports:
1. `.claudedirector/lib/core/lightweight_fallback.py` (Line 14)
   ```python
   # CURRENT (Line 14):
   from ..performance.unified_response_handler import (

   # FIX TO:
   from ..performance import (
   ```

### Potential Additional Files:
- Any MCP modules created with incorrect import paths
- Any test files referencing the old path

## Acceptance Criteria
- [ ] All imports of `lib.performance.unified_response_handler` updated to `lib.performance`
- [ ] No import errors when loading MCP modules
- [ ] All existing functionality preserved (no behavior changes)
- [ ] All P0 tests continue passing
- [ ] Zero new code added (pure import path fix)

## Dependencies
- `lib/performance/__init__.py` (existing consolidated module)
- No new dependencies required

## Testing Strategy
- Import validation tests
- P0 regression protection
- Module loading verification

## Risk Assessment
**MINIMAL RISK**: Pure import path correction
- No functionality changes
- No new code
- Existing consolidated module already tested
- Simple find-and-replace operation

## Success Metrics
- ✅ Zero import failures
- ✅ All existing functionality preserved
- ✅ No code duplication introduced
- ✅ BLOAT_PREVENTION_SYSTEM.md compliant (uses existing consolidated module)
