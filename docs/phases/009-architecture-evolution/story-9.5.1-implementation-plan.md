# Story 9.5.1 Implementation Plan: Context Intelligence Consolidation

**Author**: Martin | Platform Architecture  
**Sequential Thinking Applied**: ✅ 6-Step Methodology
**Parent Spec**: story-9.5.1-context-intelligence-spec.md
**Estimated Duration**: 1-2 days
**Target**: 334 lines → 0 lines (100% consolidation)

## **🧠 Sequential Thinking Implementation Strategy**

### **Step 4: Implementation Strategy (Detailed)**

This plan systematically consolidates 334 lines of context intelligence code into the existing `lib/context_engineering/` architecture while maintaining P0 test integrity.

### **Step 5: Strategic Enhancement**

Apply proven consolidation patterns from Phase 9.5.1 (validation system) success:
- **Incremental Migration**: Move one component at a time
- **P0 Validation**: Test after each step  
- **Import Mapping**: Track all dependencies
- **Rollback Ready**: Git commits for each migration step

## **📋 Task Breakdown**

### **🔍 PHASE 1: Analysis and Baseline (4 hours)**

#### **Task 1.1: Context Intelligence Audit**
```bash
# Map all context intelligence files and dependencies
find .claudedirector/lib/strategic_intelligence -name "*context*" -type f
grep -r "context_intelligence" .claudedirector/lib/ --include="*.py"
grep -r "from.*strategic_intelligence" .claudedirector/ --include="*.py"
```

**Deliverable**: Complete dependency map of context intelligence usage

#### **Task 1.2: Context Engineering Assessment**  
```bash
# Analyze existing context_engineering capabilities
find .claudedirector/lib/context_engineering -name "*.py" -exec wc -l {} +
grep -r "class.*Context" .claudedirector/lib/context_engineering/
```

**Deliverable**: Capability matrix showing overlap and gaps

#### **Task 1.3: P0 Baseline Validation**
```bash
# Ensure clean P0 baseline before changes
python .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py
```

**Deliverable**: P0 test baseline (39/39 passing)

### **🔄 PHASE 2: Incremental Migration (8 hours)**

#### **Task 2.1: Context Bridge Elimination (2 hours)**
**Target**: `context_intelligence_bridge.py` (334 lines)

```python
# Step-by-step migration strategy:
# 1. Identify valuable logic vs. duplicate logic
# 2. Migrate valuable logic to context_engineering
# 3. Update imports to use context_engineering  
# 4. Delete context_intelligence_bridge.py
```

**Validation**: 
- P0 tests pass after each step
- No import errors
- Context functionality preserved

#### **Task 2.2: Mock Implementation Replacement (3 hours)**
**Target**: Replace all `mock_context_*.py` files

```python
# For each mock implementation:
# 1. Identify corresponding real context class
# 2. Update imports to use real implementation
# 3. Remove mock file
# 4. Test integration
```

**Validation**:
- All mocks replaced with real implementations
- Context behavior unchanged
- Performance maintained

#### **Task 2.3: Import Path Updates (2 hours)**
**Target**: All modules importing from `strategic_intelligence.context_*`

```bash
# Systematic import updates:
grep -r "from.*strategic_intelligence.*context" .claudedirector/ --include="*.py" -l | \
xargs sed -i 's/from.*strategic_intelligence.*context/from lib.context_engineering/g'
```

**Validation**:
- No broken imports
- All context operations functional
- P0 tests passing

#### **Task 2.4: Configuration Consolidation (1 hour)**
**Target**: Context configuration scattered across files

```python
# Consolidate context configurations:
# 1. Identify all context config locations
# 2. Migrate to unified context_engineering config
# 3. Update references
# 4. Remove duplicate configs
```

**Validation**:
- Single source of truth for context config
- All context operations use unified config
- No configuration drift

### **🧪 PHASE 3: Validation and Testing (4 hours)**

#### **Task 3.1: P0 Test Validation**
```bash
# Full P0 test suite validation
python .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py
```

**Success Criteria**: 39/39 P0 tests passing

#### **Task 3.2: Context-Specific Testing**
```bash
# Run context-specific tests
python -m pytest .claudedirector/tests/ -k "context" -v
```

**Success Criteria**: All context tests passing

#### **Task 3.3: Integration Testing**
```bash
# Test context integration across modules
python -c "from lib.context_engineering import *; print('Context integration successful')"
```

**Success Criteria**: No import errors, context operations functional

#### **Task 3.4: Performance Validation**
```bash
# Ensure no performance regression
python .claudedirector/tests/regression/business_critical/test_performance.py
```

**Success Criteria**: Performance P0 test passing

### **📋 PHASE 4: Documentation and Cleanup (2 hours)**

#### **Task 4.1: Architecture Documentation Update**
- Update `PROJECT_STRUCTURE.md` to reflect context consolidation
- Document context_engineering as single source of truth
- Remove references to strategic_intelligence context components

#### **Task 4.2: Import Documentation**
- Create context import guide for developers
- Document migration from old to new import paths
- Update any developer documentation

#### **Task 4.3: Consolidation Analysis**
- Document line reduction achieved (334 → 0)
- Update story-9.5.1 spec with completion status
- Add completion entry to phase9.5-consolidation-analysis.md

## **🎯 Success Metrics Tracking**

| Metric | Baseline | Target | Current | Status |
|--------|----------|---------|---------|---------|
| **Context Intelligence Lines** | 334 | 0 | 334 | 🔄 Pending |
| **Mock Implementations** | 5+ files | 0 | 5+ | 🔄 Pending |
| **Import Paths** | Fragmented | Unified | Fragmented | 🔄 Pending |
| **P0 Tests** | 39/39 | 39/39 | 39/39 | ✅ Baseline |
| **Context Engineering Integration** | 0% | 100% | 0% | 🔄 Pending |

## **🚨 Risk Mitigation**

### **Rollback Strategy**
```bash
# Each phase creates a rollback point
git checkout -b context-migration-phase-1
# ... perform Phase 1 tasks ...
git commit -m "Phase 1: Context intelligence audit complete"

git checkout -b context-migration-phase-2  
# ... perform Phase 2 tasks ...
git commit -m "Phase 2: Context migration complete"
```

### **P0 Test Monitoring**
- Run P0 tests after each major change
- Stop and rollback if any P0 test fails
- Document any P0 test modifications needed

### **Import Validation**
```python
# Validate imports after each change
python -c "
import sys
sys.path.append('.claudedirector')
try:
    from lib.context_engineering import *
    print('✅ Context engineering imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
```

## **📅 Execution Timeline**

### **Day 1 (8 hours)**
- **Morning (4h)**: Phase 1 - Analysis and Baseline
- **Afternoon (4h)**: Phase 2.1-2.2 - Bridge elimination and mock replacement

### **Day 2 (8 hours)**  
- **Morning (4h)**: Phase 2.3-2.4 - Import updates and configuration consolidation
- **Afternoon (4h)**: Phase 3 - Validation and testing + Phase 4 - Documentation

## **🔄 Next Steps After Completion**

1. **Update Phase 9.5 Status**: Mark Story 9.5.1 as completed
2. **Prepare Story 9.5.2**: Strategic Enhancement Migration
3. **Document Lessons Learned**: Update consolidation best practices
4. **Validate Overall Progress**: Check Phase 9.5 completion percentage

---

**Ready for Execution**: All prerequisites met, baseline established, systematic plan defined with Sequential Thinking methodology.
