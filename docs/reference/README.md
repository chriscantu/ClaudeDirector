# ClaudeDirector API Reference

## Overview
Complete API reference documentation for ClaudeDirector - the industry's first completely transparent AI strategic leadership framework.

## Documentation Structure

### **[API Reference](API_REFERENCE.md)**
Complete API documentation index with quick start examples and integration guides.

### **[API Documentation](api/)**
Detailed API documentation for all system components:
- **Transparency System** - AI enhancement disclosure and framework attribution
- **Persona System** - Strategic persona management and coordination
- **MCP Integration** - MCP server management and capability invocation
- **Framework Detection** - Strategic framework analysis and recommendation
- **Performance Monitoring** - System performance tracking and metrics
- **Configuration Management** - System configuration and user preferences

### **[Library Overview](lib-overview.md)**
Python package structure, installation, and usage documentation.

### **[P0 Features Architecture](p0-features.md)**
Architecture documentation for P0 (business-critical) features and capabilities.

## Quick Start

```python
from lib.core.enhanced_persona_manager import EnhancedPersonaManager

# Initialize persona system
persona_manager = EnhancedPersonaManager()

# Get strategic guidance
response = await persona_manager.get_enhanced_response(
    persona="diego",  # Engineering Leadership
    user_input="How should we scale our platform architecture?"
)
```

## Integration Status
✅ **Production Ready**: All core features validated with P0 test coverage
✅ **Cursor Compatible**: Seamless integration with Cursor IDE workflows
✅ **Enterprise Grade**: Complete transparency and audit capabilities

For detailed implementation guides, see the [API Reference](API_REFERENCE.md) and individual module documentation.
