# Persona System API

**Strategic persona selection, management, and multi-persona coordination.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 🎭 **Persona System API**

### **Persona Manager**
```python
# .claudedirector/lib/claudedirector/core/persona_manager.py
class PersonaManager:
    """Strategic persona selection and management"""

    def __init__(self):
        self.personas = self._load_personas()
        self.context_analyzer = ContextAnalyzer()

    def select_persona(self, context: str) -> Persona:
        """Auto-select optimal persona based on context"""
        analysis = self.context_analyzer.analyze(context)

        # Weight factors for persona selection
        weights = {
            'leadership_keywords': 0.3,
            'technical_complexity': 0.25,
            'stakeholder_focus': 0.2,
            'organizational_scope': 0.15,
            'domain_specificity': 0.1
        }

        best_persona = None
        highest_score = 0

        for persona in self.personas.values():
            score = self._calculate_persona_score(analysis, persona, weights)
            if score > highest_score:
                highest_score = score
                best_persona = persona

        return best_persona

    def enhance_response(self, persona: Persona, response: str) -> str:
        """Apply persona personality and expertise"""
        enhanced = response

        # Add persona header
        enhanced = f"{persona.header}\n\n{enhanced}"

        # Apply personality traits
        enhanced = self._apply_personality_traits(enhanced, persona)

        # Add domain expertise
        enhanced = self._add_domain_expertise(enhanced, persona)

        return enhanced

    def coordinate_multi_persona(self, personas: List[Persona]) -> str:
        """Handle cross-functional collaboration"""
        coordination_header = "🤝 **Cross-Functional Analysis**\n"

        for persona in personas:
            coordination_header += f"{persona.header}: [Specific expertise contribution]\n"

        return coordination_header
```

### **Base Persona Class**
```python
# .claudedirector/lib/claudedirector/personas/base_persona.py
class BasePersona:
    """Base class for all strategic personas"""

    def __init__(self, name: str, header: str, domain: str, personality_traits: dict):
        self.name = name
        self.header = header
        self.domain = domain
        self.personality_traits = personality_traits
        self.framework_preferences = []

    def enhance_response(self, response: str, context: dict) -> str:
        """Apply persona-specific enhancements to response"""
        raise NotImplementedError("Subclasses must implement enhance_response")

    def get_framework_preferences(self) -> List[str]:
        """Return preferred strategic frameworks for this persona"""
        return self.framework_preferences

    def apply_personality_markers(self, response: str) -> str:
        """Apply personality-specific language patterns"""
        # Apply communication style
        if self.personality_traits.get('communication_style') == 'direct':
            response = self._apply_direct_communication(response)
        elif self.personality_traits.get('communication_style') == 'collaborative':
            response = self._apply_collaborative_communication(response)

        return response

    def _apply_direct_communication(self, response: str) -> str:
        """Apply direct communication patterns"""
        # Add decisive language markers
        return response

    def _apply_collaborative_communication(self, response: str) -> str:
        """Apply collaborative communication patterns"""
        # Add inclusive language markers
        return response
```

---

**🎯 The persona system provides role-based strategic AI with authentic personality and domain expertise.**
