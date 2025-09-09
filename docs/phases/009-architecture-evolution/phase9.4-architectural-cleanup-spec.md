# Phase 9.4: Architectural Cleanup Specification

**Status**: DRAFT
**Priority**: CRITICAL
**Sequential Thinking Phase**: Problem Definition Complete
**Estimated Effort**: 2-3 days
**Author**: Martin | Platform Architecture

## **🎯 Objective**

Resolve architectural violations identified in Phase 9.3 analysis where business logic is inappropriately placed in `.claudedirector/tools/` instead of `.claudedirector/lib/` per @PROJECT_STRUCTURE.md.

## **📋 Problem Statement**

**Root Issue**: 63 files in `.claudedirector/tools/` contain substantial business logic that should be in `.claudedirector/lib/` according to architectural principles.

**Specific Violations**:
1. **P0EnforcementSuite** - Core P0 validation business logic (tools/architecture/)
2. **MCPBloatAnalyzer** - 1,221 lines of analysis business logic (tools/architecture/)
3. **EnhancedSecurityScanner** - Security validation business logic (tools/quality/)
4. **MeetingIntelligenceManager** - Business intelligence logic (tools/automation/)
5. **WeeklyReportGenerator** - Core reporting functionality (tools/automation/)

## **🏗️ Architecture Principle Violation**

**@PROJECT_STRUCTURE.md states**:
- **`.claudedirector/lib/`** - Core System Library (business logic)
- **`.claudedirector/tools/`** - Development & Operations Tools (utilities only)

**Current State**: Tools directory contains business logic
**Target State**: Clean separation - tools contain only CLI interfaces and hooks

## **📊 Impact Assessment**

**Benefits**:
- ✅ Architectural compliance with @PROJECT_STRUCTURE.md
- ✅ Improved code organization and discoverability
- ✅ Better separation of concerns
- ✅ Enhanced testability of business logic

**Risks**:
- ⚠️ Import path changes may require updates
- ⚠️ CLI tools need refactoring to use lib/ classes
- ⚠️ Hook scripts need import adjustments

## **🎯 User Stories**

### **Story 9.4.1: Business Logic Migration**
**As a** platform architect
**I want** all business logic moved from tools/ to lib/
**So that** the architecture complies with PROJECT_STRUCTURE.md

**Acceptance Criteria**:
- [ ] All analysis engines moved to `.claudedirector/lib/core/analysis/`
- [ ] All business managers moved to `.claudedirector/lib/automation/`
- [ ] All security logic moved to `.claudedirector/lib/security/`
- [ ] Tools directory contains only CLI interfaces and hooks
- [ ] All imports updated and functional
- [ ] All P0 tests continue passing

### **Story 9.4.2: Tool Interface Refactoring**
**As a** developer using CLI tools
**I want** tools to provide clean interfaces to lib/ business logic
**So that** functionality is preserved while architecture is correct

**Acceptance Criteria**:
- [ ] CLI tools are lightweight interfaces only
- [ ] Business logic accessible via proper lib/ imports
- [ ] All existing functionality preserved
- [ ] Performance maintained or improved

## **🔧 Implementation Plan**

### **Phase 1: Analysis Engine Migration**
1. Move `MCPBloatAnalyzer` → `.claudedirector/lib/core/analysis/bloat_analyzer.py`
2. Move `P0EnforcementSuite` → `.claudedirector/lib/core/validation/p0_enforcer.py`
3. Update tool interfaces to use lib/ classes

### **Phase 2: Business Logic Migration**
1. Move security scanners → `.claudedirector/lib/security/`
2. Move automation managers → `.claudedirector/lib/automation/`
3. Move quality checkers → `.claudedirector/lib/quality/`

### **Phase 3: Interface Cleanup**
1. Refactor tools to be lightweight CLI interfaces
2. Update all import statements
3. Verify all hooks and scripts functional

### **Phase 4: Validation**
1. Run all P0 tests (must maintain 39/39 passing)
2. Verify architectural compliance
3. Test all CLI tools functionality

## **📈 Success Metrics**

- **Architectural Compliance**: 100% compliance with @PROJECT_STRUCTURE.md
- **P0 Test Integrity**: Maintain 39/39 passing tests
- **Functionality Preservation**: All existing features work identically
- **Import Cleanliness**: All imports follow proper lib/ → tools/ direction
- **Code Organization**: Business logic clearly separated from utilities

## **🔄 Dependencies**

**Prerequisites**:
- Phase 9.3 merged (provides stable baseline)
- All P0 tests passing
- No active development conflicts

**Blockers**: None identified

## **⚠️ Risk Mitigation**

1. **Import Breakage**: Create comprehensive import mapping before migration
2. **Functionality Loss**: Maintain 100% backward compatibility during transition
3. **Test Failures**: Run P0 tests after each migration step
4. **CLI Disruption**: Ensure all CLI interfaces remain functional

---

**Next Phase**: Phase 9.5 - Bloat System Consolidation (reduce 63 tool files)
