# Custom Persona Development Guide

**Creating and integrating custom strategic leadership personas in ClaudeDirector.**

---

## 🎭 **Custom Persona Development**

### **Persona Definition Structure**
```python
# .claudedirector/lib/claudedirector/personas/custom_persona.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PersonaDefinition:
    """Strategic persona configuration"""

    name: str                    # e.g., "Sofia"
    emoji: str                   # e.g., "🤝"
    domain: str                  # e.g., "Vendor Strategy"
    expertise: List[str]         # Core competencies
    personality_traits: Dict     # Communication style
    mcp_preferences: Dict        # Preferred enhancement servers
    framework_affinity: List[str] # Strategic frameworks

class CustomPersona:
    """Base class for strategic personas"""

    def __init__(self, definition: PersonaDefinition):
        self.definition = definition

    def analyze_context(self, input_text: str) -> float:
        """Return confidence score for handling this context"""

    def enhance_response(self, base_response: str) -> str:
        """Apply persona personality and expertise"""

    def select_frameworks(self, context: str) -> List[str]:
        """Choose relevant strategic frameworks"""
```

### **Persona Registration**
```python
# .claudedirector/config/persona_registry.py
from claudedirector.personas.custom_persona import CustomPersona

# Register new persona
persona_registry.register(
    name="sofia",
    class_ref=VendorStrategyPersona,
    activation_keywords=["vendor", "partnership", "procurement", "supplier"],
    domain_expertise=["vendor_management", "strategic_partnerships"],
    mcp_servers=["sequential", "context7"],
    frameworks=["Vendor Selection Framework", "Partnership Strategy"]
)
```

---

## 📋 **Development Guidelines**

### **Persona Design Principles**
- **Domain Expertise**: Clear specialization area with specific knowledge
- **Authentic Personality**: Consistent communication style and approach
- **Strategic Focus**: Business and organizational leadership orientation
- **Framework Integration**: Natural use of relevant strategic methodologies

### **Implementation Requirements**
- **Context Analysis**: Ability to assess relevance to domain
- **Response Enhancement**: Apply personality and expertise to responses
- **Framework Selection**: Choose appropriate strategic frameworks
- **MCP Integration**: Leverage external analytical capabilities

### **Quality Standards**
- **Consistency**: Maintain personality across all interactions
- **Expertise Depth**: Demonstrate genuine domain knowledge
- **Strategic Value**: Provide actionable business insights
- **Transparency**: Clear attribution of AI enhancements

---

*Part of the [ClaudeDirector Development Guide](../DEVELOPMENT_GUIDE.md) suite.*
