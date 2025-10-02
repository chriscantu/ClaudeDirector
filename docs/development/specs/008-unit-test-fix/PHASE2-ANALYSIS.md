# Phase 2 Analysis: Categorize Failing Unit Tests

**Date**: October 1, 2025
**Analyst**: Martin | Platform Architecture
**Status**: 🚧 IN PROGRESS

---

## 🎯 **Executive Summary**

**Objective**: Categorize all 128 failing/error tests to determine root causes and fix strategies.

**Current Status**:
- **317 tests total**
- **166 passing** (52.4%)
- **99 failing** (31.2%)
- **29 errors** (9.1%)
- **23 skipped** (7.3%)

---

## 📊 **Error Pattern Analysis**

### **Primary Error Categories Identified**

#### **1. API Method Changes (Highest Priority)**
**Count**: ~20+ tests
**Pattern**: `AttributeError: 'X' object has no attribute 'Y'. Did you mean: 'Z'?`

**Examples**:
- `AnalysisComplexityDetector.analyze_complexity` → `analyze_input_complexity` (18 tests)
- `AnalysisComplexity.STRATEGIC` → Does not exist (enum changed)
- `ClaudeDirectorConfig.project_root` → Attribute removed (5 tests)
- `ClaudeDirectorConfig.stakeholder_auto_create_threshold` → Removed (2 tests)

**Root Cause**: API evolution without test updates (legitimate code changes, outdated tests)
**Fix Strategy**: Update test assertions to match current API

---

#### **2. Mock/Import Issues (Medium Priority)**
**Count**: ~10 tests
**Pattern**: `AttributeError: <module 'X'> does not have the attribute 'Y'`

**Examples**:
- `lib.core.generation.solid_template_engine.UnifiedFactory` does not exist (10 tests)
- Mock targets outdated or incorrect

**Root Cause**: Test mocking targets that were refactored/moved/renamed
**Fix Strategy**: Update mock import paths and targets

---

#### **3. Module Import Errors (Medium Priority)**
**Count**: ~11 tests
**Pattern**: `ModuleNotFoundError: No module named 'claudedirector'`

**Examples**:
- Tests trying to import `claudedirector` package (not `lib`)
- 11 occurrences of this exact error

**Root Cause**: Incorrect import paths (should be `lib.X` not `claudedirector.X`)
**Fix Strategy**: Update import statements to use correct paths

---

#### **4. Test Logic Errors (Lower Priority)**
**Count**: ~50+ tests
**Patterns**:
- Assertion failures
- Incorrect test expectations
- Business logic changes not reflected in tests

**Examples**:
- `test_personal_retrospective_agent.py`: 2 failures
- `test_decision_orchestrator.py`: 18 failures
- `test_solid_template_engine.py`: 10 failures
- `test_sdk_enhanced_manager.py`: 7 failures

**Root Cause**: Tests written for old implementation, code evolved
**Fix Strategy**: Case-by-case analysis and update

---

## 🏗️ **Categorization Strategy**

### **Category A: Quick Wins (Fix First)**
Tests failing due to simple API renames or import path issues.
**Estimated**: 40-50 tests
**Effort**: 1-2 hours
**Impact**: High (immediate pass rate improvement)

**Action Items**:
1. Fix `analyze_complexity` → `analyze_input_complexity` (18 tests)
2. Fix `claudedirector` → `lib` imports (11 tests)
3. Fix `UnifiedFactory` mock issues (10 tests)
4. Fix removed config attributes (7 tests)

---

### **Category B: Outdated Tests (Rewrite or Delete)**
Tests for features that have been significantly refactored.
**Estimated**: 30-40 tests
**Effort**: 3-4 hours
**Impact**: Medium (cleanup + accuracy)

**Action Items**:
1. Review `test_decision_orchestrator.py` (18 failures) - Likely outdated
2. Review `test_solid_template_engine.py` (10 failures) - API changed
3. Review `test_sdk_enhanced_manager.py` (7 failures) - Recent implementation
4. Review `test_personal_retrospective_agent.py` (2 failures) - Integration changed

---

### **Category C: Legitimate Bugs (Fix Code or Test)**
Tests failing due to actual bugs in implementation or test logic.
**Estimated**: 20-30 tests
**Effort**: 4-6 hours
**Impact**: High (quality improvement)

**Action Items**:
1. Analyze assertion failures case-by-case
2. Determine if code or test is incorrect
3. Fix appropriately with full validation

---

## 📋 **Detailed Test File Breakdown**

### **High-Impact Files (Fix First)**

#### **1. `test_complexity_analyzer.py`** - 18 failures
**Issue**: API method renamed
- `analyze_complexity` → `analyze_input_complexity`
- Missing attributes: `thresholds`, `_analyze_base_complexity`, etc.
- Enum values changed: `STRATEGIC` no longer exists

**Fix**: Update all method calls and assertions

---

#### **2. `test_decision_orchestrator.py`** - 18 failures
**Issue**: Likely complete API overhaul
**Tests**:
- test_orchestrator_initialization
- test_full_analysis_workflow_success
- test_complexity_determination
- test_framework_recommendations
- test_stakeholder_extraction
- And 13 more...

**Fix**: Review implementation, rewrite tests

---

#### **3. `test_solid_template_engine.py`** - 10 failures
**Issue**: Mock target `UnifiedFactory` does not exist
**Tests**:
- test_initialization_with_basic_engine_extension
- test_unified_factory_integration
- test_context7_mcp_integration_patterns
- And 7 more...

**Fix**: Find correct mock target or update implementation

---

#### **4. `test_config.py`** - 7 failures
**Issue**: Config attributes removed
- `project_root` (5 tests)
- `stakeholder_auto_create_threshold` (2 tests)

**Fix**: Update tests to use current config API

---

#### **5. `test_sdk_enhanced_manager.py`** - 7 failures
**Issue**: Recent implementation (PR #168), tests incomplete
**Tests**:
- test_permanent_error_categorization
- test_timeout_error_categorization
- test_sdk_error_stats_extension
- And 4 more...

**Fix**: Complete test implementation for new features

---

### **Medium-Impact Files**

#### **6. `test_personal_retrospective_agent.py`** - 2 failures
- test_help_command
- test_interactive_retrospective_flow

#### **7. `test_mcp_enhancements.py`** - 1 failure
- test_query_pattern_classification

#### **8. `test_task_002_analytics_enhancement.py`** - 2 failures
- test_empty_session_data_handling
- test_session_flow_coherence

#### **9. `test_weekly_reporter_mcp_integration.py`** - 4 failures
- test_factory_function
- test_completion_probability_with_mcp_enhancement
- test_completion_probability_with_mcp_fallback
- test_extends_existing_strategic_analyzer

#### **10. `test_ai_detection_core.py`** - 5 failures
- test_confidence_score_validation
- test_stakeholder_detection_threshold_logic
- test_task_detection_threshold_logic
- test_threshold_configuration_validation
- test_stakeholder_name_detection_patterns

#### **11. `test_structure_aware_placement_engine.py`** - 2 failures
- test_component_pattern_matching
- test_placement_result_structure

---

## 🎯 **Phase 2 Execution Plan**

### **Step 1: Quick API Fixes (Category A)**
**Target**: 40-50 tests passing
**Effort**: 1-2 hours

1. Fix `test_complexity_analyzer.py` (18 tests)
   - Replace `analyze_complexity` with `analyze_input_complexity`
   - Update attribute references
   - Fix enum values

2. Fix import path issues (11 tests)
   - Replace `claudedirector` with `lib` in imports

3. Fix `test_config.py` (7 tests)
   - Remove references to deleted config attributes
   - Update assertions

4. Fix mock issues in `test_solid_template_engine.py` (10 tests)
   - Find correct mock target for `UnifiedFactory`

---

### **Step 2: Outdated Test Review (Category B)**
**Target**: 30-40 tests fixed/deleted
**Effort**: 3-4 hours

1. Analyze `test_decision_orchestrator.py` (18 tests)
   - Determine if feature still exists
   - Rewrite or delete tests

2. Review recent implementations
   - `test_sdk_enhanced_manager.py` (7 tests)
   - Complete test coverage

3. Review integration tests
   - `test_weekly_reporter_mcp_integration.py` (4 tests)
   - `test_personal_retrospective_agent.py` (2 tests)

---

### **Step 3: Case-by-Case Analysis (Category C)**
**Target**: Remaining 20-30 tests
**Effort**: 4-6 hours

1. Detailed failure analysis for each remaining test
2. Determine if bug is in code or test
3. Fix appropriately
4. Add regression coverage

---

## 📊 **Success Metrics**

### **Phase 2 Goal**
- **Category A**: 90%+ pass rate (quick fixes)
- **Category B**: 80%+ pass rate (rewrites/deletes)
- **Category C**: 100% pass rate (deep fixes)

### **Overall Target**
- **317 tests**: 100% passing or intentionally skipped
- **0 collection errors**
- **0 import errors**
- **0 API mismatch errors**

---

## 🚀 **Next Steps**

1. ✅ **Complete this analysis** - Document all 128 failures
2. 🚧 **Execute Step 1** - Quick API fixes (Category A)
3. ⏭️ **Execute Step 2** - Outdated test review (Category B)
4. ⏭️ **Execute Step 3** - Case-by-case analysis (Category C)
5. ⏭️ **Final Validation** - Run complete test suite
6. ⏭️ **Enable CI Hook** - Activate `all-unit-tests` in pre-commit

---

**Status**: 🚧 **ANALYSIS IN PROGRESS**
**Next Action**: Execute Step 1 - Quick API Fixes
