# Sequential Thinking Enforcement Policy

## MANDATORY ENFORCEMENT POLICY

**🚨 ZERO TOLERANCE**: Sequential Thinking methodology must be applied to ALL development and analysis activities in ClaudeDirector.

### Policy Requirements:
- All technical decisions must use the 6-step Sequential Thinking methodology
- All code changes must demonstrate systematic analysis
- All architectural decisions must include Sequential Thinking documentation
- All P0 tests must validate Sequential Thinking compliance
- **ALL SPECIFICATIONS MUST USE SPEC-KIT FORMAT** (as per SPEC_KIT_ANALYSIS.md)
- All development artifacts must follow PROJECT_STRUCTURE.md placement
- All code must adhere to SOLID and DRY principles with BLOAT_PREVENTION_SYSTEM.md integration

## ZERO EXCEPTIONS RULE

**No commits are allowed without Sequential Thinking compliance**. This includes:
- Code changes without systematic analysis
- Architecture modifications without Sequential Thinking documentation
- Feature implementations without the 6-step methodology
- Bug fixes that don't demonstrate root cause analysis
- **Specifications not using spec-kit format**
- Files placed outside PROJECT_STRUCTURE.md requirements
- Code violating SOLID or DRY principles
- Development without BLOAT_PREVENTION_SYSTEM.md integration

### 6-Step Sequential Thinking Methodology:
1. **Problem Definition**: Clear articulation of the issue
2. **Root Cause Analysis**: Systematic investigation of underlying causes
3. **Solution Architecture**: Comprehensive solution design
4. **Implementation Strategy**: Detailed execution plan
5. **Strategic Enhancement**: Business impact and optimization
6. **Success Metrics**: Measurable validation criteria

## ENFORCEMENT MECHANISMS

### Pre-Commit Validation:
- P0 tests validate Sequential Thinking compliance
- Architectural compliance checks enforce methodology usage
- Code bloat prevention ensures systematic approach

### CI/CD Integration:
- All pull requests must pass Sequential Thinking P0 tests
- CI pipeline validates methodology application
- Automated enforcement prevents non-compliant merges

### Documentation Requirements:
- All Python files must include Sequential Thinking methodology references
- Technical decisions must document the 6-step process
- Architecture changes must demonstrate systematic analysis

## NON-COMPLIANCE CONSEQUENCES

### Immediate Actions:
- **Commit Blocking**: Non-compliant commits are automatically blocked
- **Pull Request Rejection**: PRs without Sequential Thinking compliance are rejected
- **CI Failure**: Automated validation prevents deployment

### Quality Impact:
- Development becomes ad-hoc without systematic approach
- Technical debt increases due to unsystematic decisions
- Solution quality decreases without proper analysis
- Strategic value is compromised by reactive development

### Business Impact:
- Engineering productivity degrades
- Solution quality decreases
- Strategic decision support becomes unreliable
- Competitive advantage is lost through unsystematic development

---

**Enforcement Owner**: Martin | Platform Architecture
**Last Updated**: September 10, 2025
**Policy Version**: 1.0
**Compliance Requirement**: 100% (Zero Tolerance)
