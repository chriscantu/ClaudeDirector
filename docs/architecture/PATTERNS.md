# Architectural Patterns

**Design patterns and architectural decisions for ClaudeDirector.**

---

## 📋 **Current Architecture Patterns**

### 🏗️ **Core System Patterns**

ClaudeDirector follows established architectural patterns documented in:
- **OVERVIEW.md**: High-level system architecture
- **COMPONENTS.md**: Detailed component specifications
- **PROJECT_STRUCTURE.md**: Mandatory project organization
- **DECISIONS.md**: Architectural decision records (ADRs)

### 🎯 **Key Architectural Principles**

1. **Single Source of Truth**: Each concern has ONE authoritative location
2. **Context Engineering First**: Primary system for strategic intelligence
3. **P0 Test Protection**: Business-critical functionality always protected
4. **User/System Separation**: Clear boundaries between user and system territory
5. **Security by Default**: All personal data protected from source control

### 📚 **Pattern References**

For specific implementation patterns, refer to:
- **Context Engineering**: `.claudedirector/lib/context_engineering/` - 8-layer memory architecture
- **AI Intelligence**: `.claudedirector/lib/ai_intelligence/` - MCP coordination and framework detection
- **Core Components**: `.claudedirector/lib/core/` - Foundational system patterns
- **Integration Layer**: `.claudedirector/lib/integration/` - Unified integration patterns

---

*For detailed pattern implementations, see the component documentation in the respective directories.*
