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
        self.challenge_framework = StrategicChallengeFramework()

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

    def enhance_response(self, persona: Persona, response: str, user_input: str = "") -> str:
        """Apply persona personality, expertise, and challenge patterns"""
        enhanced = response

        # Add persona header
        enhanced = f"{persona.header}\n\n{enhanced}"

        # Apply challenge framework if needed
        if user_input and self.challenge_framework.should_challenge(user_input, persona.name):
            challenge_content = self.challenge_framework.generate_challenge_response(
                user_input, persona.name
            )
            enhanced = f"{challenge_content}\n\n{enhanced}"

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

### **Strategic Challenge Framework**
```python
# .claudedirector/lib/personas/strategic_challenge_framework.py
class StrategicChallengeFramework:
    """Challenge pattern detection and generation for strategic personas"""

    def __init__(self):
        self.challenge_patterns = self._load_challenge_patterns()
        self.persona_configurations = self._load_persona_configs()

    def should_challenge(self, user_input: str, persona: str) -> bool:
        """Determine if persona should challenge user assumptions"""
        confidence_score = self._calculate_challenge_confidence(user_input, persona)
        threshold = self.persona_configurations[persona].get('challenge_threshold', 0.7)
        return confidence_score >= threshold

    def generate_challenge_response(self, user_input: str, persona: str) -> str:
        """Generate domain-specific challenge questions"""
        challenge_types = self._detect_challenge_types(user_input)
        persona_config = self.persona_configurations[persona]

        challenge_questions = []
        for challenge_type in challenge_types:
            questions = persona_config['challenge_questions'].get(challenge_type, [])
            if questions:
                challenge_questions.extend(questions[:2])  # Limit to 2 per type

        if challenge_questions:
            header = "🔍 **Let me challenge this thinking...**\n\n"
            questions_text = "\n".join(f"- **{q}**" for q in challenge_questions)
            footer = "\n\n**I need to see evidence and validation before we proceed with recommendations.**"
            return f"{header}{questions_text}{footer}"

        return ""

    def _detect_challenge_types(self, user_input: str) -> List[str]:
        """Detect which challenge patterns apply to user input"""
        detected_types = []

        for challenge_type, patterns in self.challenge_patterns.items():
            trigger_keywords = patterns.get('trigger_keywords', [])
            confidence_threshold = patterns.get('confidence_threshold', 0.7)

            # Calculate confidence based on keyword presence and context
            confidence = self._calculate_pattern_confidence(user_input, trigger_keywords)

            if confidence >= confidence_threshold:
                detected_types.append(challenge_type)

        return detected_types

    def _calculate_challenge_confidence(self, user_input: str, persona: str) -> float:
        """Calculate confidence score for challenging this input"""
        # Implementation details for confidence calculation
        # Based on assumption keywords, certainty language, domain relevance
        pass
```

---

**🎯 The persona system provides role-based strategic AI with authentic personality and domain expertise.**
