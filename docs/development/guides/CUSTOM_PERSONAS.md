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
    challenge_patterns: Dict     # Challenge behavior configuration
    challenge_focus: List[str]   # Domain-specific challenge areas

class CustomPersona:
    """Base class for strategic personas"""

    def __init__(self, definition: PersonaDefinition):
        self.definition = definition
        self.challenge_framework = StrategicChallengeFramework()

    def analyze_context(self, input_text: str) -> float:
        """Return confidence score for handling this context"""

    def enhance_response(self, base_response: str) -> str:
        """Apply persona personality and expertise"""

    def select_frameworks(self, context: str) -> List[str]:
        """Choose relevant strategic frameworks"""

    def should_challenge(self, user_input: str) -> bool:
        """Determine if persona should challenge user assumptions"""
        return self.challenge_framework.should_challenge(user_input, self.definition.name)

    def generate_challenge_questions(self, user_input: str) -> List[str]:
        """Generate domain-specific challenge questions"""
        return self.challenge_framework.generate_persona_challenges(
            user_input, self.definition.name, self.definition.challenge_focus
        )
```

### **Persona Registration**
```python
# .claudedirector/config/persona_registry.py
from claudedirector.personas.custom_persona import CustomPersona

# Register new persona with challenge framework integration
persona_registry.register(
    name="sofia",
    class_ref=VendorStrategyPersona,
    activation_keywords=["vendor", "partnership", "procurement", "supplier"],
    domain_expertise=["vendor_management", "strategic_partnerships"],
    mcp_servers=["sequential", "context7"],
    frameworks=["Vendor Selection Framework", "Partnership Strategy"],
    challenge_patterns={
        "assumption_test": ["vendor", "partnership", "obviously", "clearly"],
        "root_cause_probe": ["problem", "issue", "challenge", "need"],
        "evidence_demand": ["best", "should", "must", "always"],
        "alternative_exploration": ["solution", "approach", "strategy"]
    },
    challenge_focus=["vendor_assumptions", "partnership_validation", "procurement_evidence"]
)
```

---

## 📋 **Development Guidelines**

### **Persona Design Principles**
- **Domain Expertise**: Clear specialization area with specific knowledge
- **Challenge Integration**: Define domain-specific challenge patterns and focus areas
- **Evidence Requirements**: Specify what evidence the persona demands for validation
- **Professional Tone**: Maintain collaborative but firm challenge approach
- **Assumption Testing**: Identify key assumptions the persona should challenge in their domain
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
