# Development Workflow Guide

**Development processes, workflows, and best practices for ClaudeDirector contributors.**

---

## 📋 **Development Workflow**

### **Git Workflow**
```bash
# Feature development workflow
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: descriptive commit message"

# Push and create PR
git push -u origin feature/your-feature-name
gh pr create --title "Feature Title" --body "Description"
```

### **Branch Naming Conventions**
- **Features**: `feature/description-of-feature`
- **Bug Fixes**: `fix/description-of-fix`
- **Documentation**: `docs/description-of-changes`
- **Performance**: `perf/description-of-optimization`
- **Refactoring**: `refactor/description-of-changes`

### **Commit Message Format**
```
type(scope): description

feat(personas): add vendor strategy persona
fix(mcp): resolve connection timeout issues
docs(api): update MCP integration documentation
perf(cache): optimize framework detection caching
test(p0): add persona selection accuracy tests
```

### **Code Review Process**
1. **Self Review**: Review your own changes before requesting review
2. **Automated Checks**: Ensure all CI checks pass
3. **Peer Review**: At least one reviewer approval required
4. **Testing**: Verify all tests pass and coverage requirements met
5. **Documentation**: Update relevant documentation

---

## 📋 **Development Standards**

### **Code Quality**
- **Type Hints**: Use Python type hints for all function signatures
- **Documentation**: Comprehensive docstrings for all public APIs
- **Error Handling**: Graceful error handling with appropriate logging
- **Performance**: Consider performance implications of all changes

### **Testing Requirements**
- **P0 Coverage**: All critical features must have P0 tests
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Performance Tests**: Validate response time requirements

### **Documentation Standards**
- **API Documentation**: Complete API reference for all public interfaces
- **Architecture Documentation**: Update architecture docs for structural changes
- **User Documentation**: Update user guides for feature changes
- **Development Documentation**: Update development guides for process changes

---

*Part of the [ClaudeDirector Development Guide](../DEVELOPMENT_GUIDE.md) suite.*
