# ADR-016: Mandatory Architectural Discovery Process

**Status**: ACTIVE
**Date**: 2024-12-29
**Context**: Prevention of code duplication violations like TS-4 Enhanced Cursor Bridge incident

## Problem Statement

The TS-4 Enhanced Cursor Integration implementation created 1,200+ lines of duplicative code that violated DRY principles and existing architectural patterns. This occurred despite having:
- Documented BLOAT_PREVENTION_SYSTEM.md
- Pre-commit hooks for duplication detection
- Clear PROJECT_STRUCTURE.md guidelines
- Existing cursor integration components

**Root Cause**: Missing mandatory architectural discovery phase before implementation.

## Decision

**MANDATORY ARCHITECTURAL DISCOVERY PROCESS** must be followed for ALL new component implementations.

### Phase 1: Discovery (MANDATORY - NO EXCEPTIONS)

#### 1.1 Existing Component Analysis
```bash
# REQUIRED: Search for existing functionality
grep -r "cursor" .claudedirector/lib/
grep -r "integration" .claudedirector/lib/
grep -r "workspace" .claudedirector/lib/
```

#### 1.2 Architectural Pattern Analysis
```bash
# REQUIRED: Analyze existing patterns
find .claudedirector/lib -name "*integration*" -type f
find .claudedirector/lib -name "*cursor*" -type f
find .claudedirector/lib -name "*bridge*" -type f
```

#### 1.3 DRY Compliance Check
```bash
# REQUIRED: Run duplication analysis
python .claudedirector/tools/architecture/bloat_prevention_system.py --target-dir lib/
```

### Phase 2: Architectural Decision Record (MANDATORY)

#### 2.1 Create ADR Before Implementation
- **File**: `docs/architecture/ADR-XXX-[FEATURE-NAME].md`
- **Required Sections**:
  - Existing Component Analysis
  - Duplication Risk Assessment
  - Enhancement vs New Component Decision
  - Implementation Strategy
  - DRY Compliance Plan

#### 2.2 ADR Template
```markdown
# ADR-XXX: [Feature Name] Implementation Strategy

**Status**: PROPOSED
**Date**: [Date]
**Context**: [Feature requirements and scope]

## Existing Component Analysis
- [ ] Searched for existing functionality: [results]
- [ ] Identified related components: [list]
- [ ] Analyzed duplication risk: [assessment]

## Implementation Decision
- [ ] **ENHANCE EXISTING** components: [justification]
- [ ] **CREATE NEW** focused components: [justification]
- [ ] **HYBRID APPROACH**: [detailed plan]

## DRY Compliance Plan
- [ ] No functional duplication
- [ ] Single source of truth maintained
- [ ] Existing patterns leveraged
- [ ] Net code reduction achieved

## Implementation Strategy
[Detailed technical approach]

## Validation Criteria
- [ ] All P0 tests pass
- [ ] No duplication detected by bloat prevention system
- [ ] Performance targets met
- [ ] Architectural compliance verified
```

### Phase 3: Implementation Validation (AUTOMATED)

#### 3.1 Enhanced Pre-commit Hooks
```bash
# REQUIRED: Enhanced duplication detection
python .claudedirector/tools/architecture/enhanced_duplication_detector.py
```

#### 3.2 Cross-Directory Analysis
- Analyze similarity across ALL lib/ subdirectories
- Block commits with >75% functional similarity
- Require explicit ADR reference for new components

## Implementation

### Immediate Actions (This Sprint)

1. **Create Enhanced Duplication Detector**
   - Cross-directory similarity analysis
   - Function-level duplication detection
   - Integration with pre-commit hooks

2. **Update Pre-commit Configuration**
   - Add mandatory architectural discovery check
   - Require ADR reference for new files
   - Enhanced bloat prevention validation

3. **Create ADR Template and Process**
   - Standardized ADR template
   - Mandatory ADR creation workflow
   - Integration with GitHub PR templates

### Long-term Improvements

1. **IDE Integration**
   - VS Code/Cursor extension for architectural discovery
   - Real-time duplication warnings
   - Automated existing component suggestions

2. **CI/CD Enhancement**
   - Architectural compliance gates
   - Automated ADR validation
   - Cross-component impact analysis

## Consequences

### Positive
- **Prevents duplication violations** through systematic discovery
- **Enforces architectural thinking** before implementation
- **Maintains DRY principles** through mandatory analysis
- **Improves code quality** through structured decision-making

### Negative
- **Adds development overhead** (~30 minutes per new component)
- **Requires discipline** to follow process consistently
- **May slow initial development** for urgent features

### Mitigation
- **Automate discovery tools** to reduce manual effort
- **Create templates** to streamline ADR creation
- **Integrate with IDE** for seamless workflow
- **Emergency bypass process** for P0 critical fixes

## Compliance

This ADR is **MANDATORY** and **ENFORCED** through:
- Pre-commit hooks (blocks commits without ADR reference)
- CI/CD pipeline validation
- Code review requirements
- P0 test integration

**Violation of this process is considered a BLOCKING architectural issue.**

## References

- [BLOAT_PREVENTION_SYSTEM.md](BLOAT_PREVENTION_SYSTEM.md)
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- [CODE_ELIMINATION_POLICY.md](CODE_ELIMINATION_POLICY.md)
- [TS-4 Duplication Incident Analysis](../phases/TS4_DUPLICATION_INCIDENT_ANALYSIS.md)
