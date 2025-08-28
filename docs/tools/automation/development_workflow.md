# ClaudeDirector Development Workflow

## 🎯 **GOAL: Prevent Future 48K Line Commits**

### **Commit Size Guidelines**

#### **Standard Commits (Preferred)**
- **Target**: < 200 lines changed
- **Maximum**: 500 lines (requires justification)
- **Focus**: Single feature or logical unit

#### **Large Commits (Exceptional)**
- **Threshold**: > 500 lines
- **Requirement**: Explicit approval in commit message
- **Process**: Break into smaller commits when possible

### **Feature Branch Strategy**

#### **Branch Naming**
```bash
feature/descriptive-feature-name
fix/specific-bug-description
cleanup/targeted-area
docs/documentation-update
```

#### **Branch Lifecycle**
1. **Create**: `git checkout -b feature/my-feature`
2. **Develop**: Regular commits < 500 lines
3. **Test**: All P0 tests must pass
4. **Review**: Create PR with CI validation
5. **Merge**: Squash merge to main

### **CI-First Development**

#### **Pre-Commit Validation**
```bash
# Required before every commit
.claudedirector/tools/testing/mandatory_test_validator.py

# Recommended before push
.claudedirector/tools/cleanup/automated_cleanup.py
```

#### **Local CI Simulation**
```bash
# Run full CI pipeline locally
python3 .claudedirector/tools/ci/local-ci-runner.py

# Quick smoke test
python3 .claudedirector/tools/testing/smoke_tests.py
```

### **P0 Feature Protection**

#### **Mandatory P0 Tests**
- **MCP Transparency**: Real-time disclosure
- **Conversation Tracking**: Persistent memory
- **Quality Targets**: 85% conversation quality
- **First-Run Wizard**: Zero-setup experience
- **Cursor Integration**: Live conversation flow

#### **P0 Test Enforcement**
```bash
# All P0 tests MUST pass before commit
# No exceptions, no skipping allowed
# Automated via pre-commit hooks
```

### **Package Management**

#### **Library Structure**
```
.claudedirector/lib/
├── core/           # Essential functionality
├── transparency/   # MCP and framework disclosure
├── memory/         # Conversation persistence
├── intelligence/   # Stakeholder and meeting AI
└── p0_features/    # Mission-critical features
```

#### **Import Validation**
```bash
# CI validates package can be installed
pip install -e ./.claudedirector/lib

# Core modules must be importable
from claudedirector.core import integrated_conversation_manager
```

### **Cleanup Automation**

#### **Automated Cleanup (Pre-Commit)**
- Remove Python cache files
- Fix placeholder code patterns
- Consolidate excessive documentation
- Validate package structure

#### **Manual Cleanup (Weekly)**
```bash
# Run comprehensive cleanup
.claudedirector/tools/cleanup/automated_cleanup.py

# Review and archive old branches
git branch -d $(git branch --merged | grep -v main)
```

### **Documentation Standards**

#### **File Size Limits**
- **README files**: < 200 lines (focus on essentials)
- **Implementation docs**: < 300 lines (break into sections)
- **API documentation**: Generated from code comments

#### **Required Documentation**
- **Feature PRs**: Include user impact and testing notes
- **Architecture changes**: Update ARCHITECTURE.md
- **Breaking changes**: Migration guide required

### **Quality Gates**

#### **Commit-Level Gates**
- [ ] P0 tests pass
- [ ] No placeholder code
- [ ] Documentation updated
- [ ] Security scan clean

#### **PR-Level Gates**
- [ ] Full CI pipeline passes
- [ ] Code review approved
- [ ] Package installation validated
- [ ] Performance benchmarks met

#### **Release-Level Gates**
- [ ] All integration tests pass
- [ ] Documentation is current
- [ ] Security audit complete
- [ ] Deployment smoke tests pass

### **Emergency Procedures**

#### **Hotfix Process**
1. **Create hotfix branch** from main
2. **Minimal change** to fix critical issue
3. **Skip some hooks** if P0 tests pass: `git commit --no-verify`
4. **Immediate PR** with fast-track review
5. **Post-fix cleanup** in follow-up PR

#### **Rollback Process**
```bash
# If large commit causes issues
git revert <commit-hash>

# If entire feature needs removal
git revert -m 1 <merge-commit>
```

---

## **📊 Success Metrics**

### **Velocity Targets**
- **Average commit size**: < 300 lines
- **Feature branch duration**: < 1 week
- **CI pass rate**: > 95%
- **Hotfix frequency**: < 1 per month

### **Quality Targets**
- **P0 test failures**: 0 tolerance
- **Security violations**: 0 tolerance
- **Documentation debt**: < 5 outdated files
- **Technical debt**: Weekly review and cleanup
