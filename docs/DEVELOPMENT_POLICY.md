# ClaudeDirector Development Policy

**Mandatory development standards and architectural policies for all ClaudeDirector contributions.**

---

## 🛡️ **Policy Enforcement**

This document establishes **mandatory** development standards that are **automatically enforced** through pre-commit hooks and CI validation. All contributions must comply with these policies.

### **Enforcement Mechanisms**
- ✅ **Pre-commit Hooks**: Automatic validation before commits
- ✅ **CI Pipeline**: Comprehensive validation before merge
- ✅ **PR Reviews**: Manual verification of policy compliance
- ✅ **Automated Rejection**: Non-compliant changes are automatically blocked

---

## 📋 **Mandatory Development Standards**

### **1. Documentation Standards**
#### **File Size Limits** (ENFORCED)
- **Documentation Files**: 500 lines per `.md` file (aligned with code standards)
- **Python Files**: 500 lines per `.py` file (existing standard)
- **Automatic Check**: Pre-commit hooks validate all files
- **Violation Action**: Commit blocked until files are split
- **Exception Process**: Must be approved by architecture review

#### **Documentation Structure** (ENFORCED)
- **Single Responsibility**: Each file covers one focused topic
- **Clear Navigation**: Index files link to focused sub-documents
- **Consistent Format**: Follow established templates and patterns
- **Cross-References**: Maintain links between related documents

### **2. Code Quality Standards**
#### **Testing Requirements** (ENFORCED)
- **P0 Test Coverage**: All critical features must have P0 tests
- **Test Execution**: All tests must pass before commit/merge
- **No Test Skipping**: P0 tests cannot be skipped or disabled
- **Coverage Minimum**: 80% code coverage for new code

#### **Code Style** (ENFORCED)
- **Black Formatting**: All Python code must pass Black formatting
- **Type Hints**: All public functions must have type annotations
- **Docstrings**: All public APIs must have comprehensive documentation
- **Import Standards**: Follow established import path conventions

### **3. Architecture Compliance**
#### **Component Structure** (ENFORCED)
- **Layered Architecture**: Follow established architectural layers
- **Separation of Concerns**: Clear boundaries between components
- **Interface Contracts**: Maintain stable public APIs
- **Dependency Management**: No circular dependencies allowed

#### **Integration Standards** (ENFORCED)
- **MCP Protocol**: All external integrations use MCP standard
- **Transparency Requirements**: All AI enhancements must be disclosed
- **Security Compliance**: All integrations pass security validation
- **Performance SLAs**: Response times within documented limits

### **4. Git Workflow Standards**
#### **Branch Management** (ENFORCED)
- **Feature Branches**: All changes via feature branches from main
- **Naming Convention**: Follow `feature/`, `fix/`, `docs/` prefixes
- **Single Purpose**: One feature/fix per branch
- **Clean History**: Squash commits before merge

#### **Commit Standards** (ENFORCED)
- **Conventional Commits**: Follow `type(scope): description` format
- **Descriptive Messages**: Clear explanation of changes and impact
- **Atomic Commits**: Each commit represents complete, working change
- **No Force Push**: Protect shared branch history

---

## 🔧 **Automated Enforcement**

### **Pre-commit Hook Validation**
```yaml
# .pre-commit-config.yaml enforcement rules
repos:
  - repo: local
    hooks:
      - id: documentation-size-limit
        name: Documentation Size Limit (200 lines)
        entry: python .claudedirector/tools/policy/check_doc_size.py
        language: system
        files: '\.md$'

      - id: architecture-compliance
        name: Architecture Compliance Check
        entry: python .claudedirector/tools/policy/check_architecture.py
        language: system
        files: '\.py$'

      - id: p0-test-protection
        name: P0 Test Protection
        entry: python .claudedirector/tools/policy/check_p0_tests.py
        language: system
        files: 'test.*\.py$'
```

### **CI Pipeline Enforcement**
```yaml
# .github/workflows/policy-enforcement.yml
name: Development Policy Enforcement
on: [push, pull_request]
jobs:
  policy-validation:
    runs-on: ubuntu-latest
    steps:
      - name: Documentation Standards Check
        run: python .claudedirector/tools/policy/validate_docs.py

      - name: Architecture Compliance Check
        run: python .claudedirector/tools/policy/validate_architecture.py

      - name: Code Quality Standards Check
        run: python .claudedirector/tools/policy/validate_code_quality.py
```

---

## 📊 **Policy Metrics & Monitoring**

### **Compliance Tracking**
- **Documentation Health**: File size distribution and compliance rate
- **Test Coverage**: P0 test coverage and execution success rate
- **Architecture Violations**: Component coupling and dependency analysis
- **Code Quality**: Formatting, typing, and documentation compliance

### **Violation Reporting**
- **Real-time Feedback**: Immediate feedback during development
- **Trend Analysis**: Track compliance improvements over time
- **Exception Tracking**: Monitor and review policy exceptions
- **Team Metrics**: Individual and team compliance scorecards

---

## 🚨 **Policy Violations**

### **Automatic Rejection Criteria**
- **Documentation > 200 lines**: Commit blocked until split
- **P0 Test Failures**: Merge blocked until tests pass
- **Architecture Violations**: Component coupling exceeds limits
- **Security Violations**: Sensitive data or security issues detected

### **Exception Process**
1. **Technical Justification**: Document why exception is necessary
2. **Architecture Review**: Review by senior technical leadership
3. **Time-bound Approval**: Exception valid for specific timeframe
4. **Remediation Plan**: Plan to address exception in future

---

## 📚 **Reference Documentation**

### **Development Guides** (MANDATORY READING)
- **[Core Architecture](development/guides/CORE_ARCHITECTURE.md)**: System architecture principles
- **[Development Workflow](development/guides/DEVELOPMENT_WORKFLOW.md)**: Git workflow and processes
- **[Testing & QA](development/guides/TESTING_QA.md)**: Testing standards and requirements
- **[Performance Optimization](development/guides/PERFORMANCE_OPTIMIZATION.md)**: Performance requirements

### **Architecture Documentation** (MANDATORY COMPLIANCE)
- **[System Overview](architecture/OVERVIEW.md)**: High-level architecture
- **[Component Patterns](architecture/patterns/)**: Architectural patterns library
- **[API Standards](reference/API_REFERENCE.md)**: API design and documentation standards

---

## ✅ **Policy Acknowledgment**

**By contributing to ClaudeDirector, all developers acknowledge:**

1. **Standards Compliance**: All contributions must meet documented standards
2. **Automatic Enforcement**: Policy violations will be automatically rejected
3. **Continuous Improvement**: Standards evolve based on project needs
4. **Team Responsibility**: All team members enforce and maintain standards

---

*This policy is automatically enforced and regularly updated to maintain ClaudeDirector's architectural integrity and development quality.*
