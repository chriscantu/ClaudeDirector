# Core Architecture Development Guide

**Understanding ClaudeDirector's core architecture for development and extension.**

---

## 🏗️ **Core Architecture**

### **Directory Structure**
```
📁 ClaudeDirector/
├── 📁 .claudedirector/           # Core framework (DO NOT MODIFY)
│   ├── 📁 lib/claudedirector/    # Python implementation
│   │   ├── 📁 core/              # Conversation engine
│   │   ├── 📁 personas/          # Strategic persona logic
│   │   ├── 📁 transparency/      # Transparency system
│   │   ├── 📁 mcp/              # MCP client infrastructure
│   │   └── 📁 frameworks/        # Framework detection
│   ├── 📁 framework/             # Framework definitions
│   ├── 📁 config/               # Configuration files
│   ├── 📁 tests/                # Test suites
│   └── 📁 integration-protection/ # Integration safeguards
├── 📁 docs/                     # Documentation
│   ├── 📁 setup/               # Installation guides
│   ├── 📁 development/         # Development guides
│   ├── 📁 architecture/        # Architecture documentation
│   └── 📁 reference/           # API reference
└── 📄 README.md                 # User documentation
```

### **Core Components**

#### **1. Persona System**
```python
# .claudedirector/lib/claudedirector/core/persona_manager.py
class PersonaManager:
    """Strategic persona selection and management"""

    def select_persona(self, context: str) -> Persona:
        """Auto-select optimal persona based on context"""

    def enhance_response(self, persona: Persona, response: str) -> str:
        """Apply persona personality and expertise"""

    def coordinate_multi_persona(self, personas: List[Persona]) -> str:
        """Handle cross-functional collaboration"""
```

#### **2. Transparency Engine**
```python
# .claudedirector/lib/claudedirector/transparency/integrated_transparency.py
class TransparencyEngine:
    """Real-time AI capability disclosure"""

    def disclose_mcp_usage(self, server: str, capability: str) -> str:
        """Show when MCP servers enhance responses"""

    def attribute_framework(self, framework: str, confidence: float) -> str:
        """Attribute strategic frameworks used"""

    def generate_audit_trail(self, session_data: dict) -> AuditTrail:
        """Create complete audit trail for governance"""
```

#### **3. Framework Detection**
```python
# .claudedirector/lib/claudedirector/frameworks/framework_detector.py
class FrameworkDetector:
    """Automatic strategic framework identification"""

    def detect_frameworks(self, response: str) -> List[Framework]:
        """Identify applied strategic methodologies"""

    def calculate_confidence(self, framework: Framework) -> float:
        """Calculate framework application confidence"""

    def generate_attribution(self, frameworks: List[Framework]) -> str:
        """Create framework attribution display"""
```

---

## 📋 **Architecture Principles**

### **Separation of Concerns**
- **Core Logic**: Business logic isolated from presentation
- **Transparency Layer**: Complete audit trail generation
- **Integration Layer**: External service communication
- **Configuration Layer**: User preferences and system settings

### **Extensibility Points**
- **Custom Personas**: Add new strategic leadership roles
- **Framework Integration**: Integrate additional strategic methodologies
- **MCP Servers**: Connect external analytical capabilities
- **Transparency Hooks**: Custom audit trail generation

---

*Part of the [ClaudeDirector Development Guide](../DEVELOPMENT_GUIDE.md) suite.*
