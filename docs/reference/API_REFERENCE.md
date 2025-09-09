# API Reference

**API documentation for ClaudeDirector.**

---

## 📚 **API Documentation Index**

### **Core System APIs**

#### **🔍 [Transparency System API](api/TRANSPARENCY_API.md)**
AI enhancement disclosure and framework attribution.
- MCP Transparency Middleware
- Framework Attribution Engine

#### **🎭 [Persona System API](api/PERSONA_SYSTEM_API.md)**
Persona selection, management, and coordination.
- Persona Manager
- Base Persona Class

#### **🔧 [MCP Integration API](api/MCP_INTEGRATION_API.md)**
MCP server management and capability invocation.
- MCP Client Manager
- MCP Client Implementation

### **Intelligence & Analysis APIs**

#### **📚 [Framework Detection API](api/FRAMEWORK_DETECTION_API.md)**
Detection and attribution of strategic frameworks.
- Framework Detector
- Pattern Recognition Engine

#### **🔄 [Conversation Management API](api/CONVERSATION_API.md)**
Conversation context management and persistence.
- Conversation Manager
- Context Persistence

### **System Management APIs**

#### **📊 [Performance Monitoring API](api/PERFORMANCE_API.md)**
Performance tracking and metrics.
- Performance Monitor
- Metrics Collection

#### **🛠️ [Configuration API](api/CONFIGURATION_API.md)**
System configuration management and user preferences.
- Configuration Manager
- User Settings

---

## 🚀 **Quick Start**

### **Basic Usage**
```python
from lib.core.enhanced_persona_manager import EnhancedPersonaManager
from lib.transparency.mcp_transparency import MCPTransparencyMiddleware

# Initialize core components
persona_manager = EnhancedPersonaManager()
transparency = MCPTransparencyMiddleware()

# Get enhanced strategic response
response = await persona_manager.get_enhanced_response(
    persona="diego",
    user_input="How should we scale our platform architecture?"
)
```

### **Advanced Integration**
```python
from lib.mcp.client_manager import MCPClientManager
from lib.frameworks.framework_detector import FrameworkDetector

# Initialize MCP integration
mcp_manager = MCPClientManager()
await mcp_manager.initialize_servers()

# Detect strategic frameworks
detector = FrameworkDetector()
frameworks = detector.detect_frameworks(response_text, "diego")
```

---

## 📖 **Additional Resources**

- **[Architecture Overview](../architecture/OVERVIEW.md)** - System design and components
- **[Development Guide](../development/DEVELOPMENT_GUIDE.md)** - Setup and development workflow
- **[Strategic Frameworks](../frameworks/FRAMEWORKS_INDEX.md)** - Available framework methodologies

---

**🎯 Complete API reference for transparent AI strategic leadership at enterprise scale.**
