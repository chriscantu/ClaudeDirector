# Framework Integration Development Guide

**Integrating strategic frameworks and methodologies into ClaudeDirector.**

---

## 📚 **Framework Integration**

### **Framework Definition Structure**
```python
# .claudedirector/lib/claudedirector/frameworks/custom_framework.py
from dataclasses import dataclass
from typing import List, Dict, Pattern

@dataclass
class FrameworkDefinition:
    """Strategic framework configuration"""

    name: str                    # e.g., "Team Topologies"
    category: str               # e.g., "Organizational Design"
    description: str            # Framework purpose
    detection_patterns: List[Pattern]  # Text patterns for detection
    confidence_threshold: float # Minimum confidence for attribution
    personas: List[str]         # Personas that use this framework

class FrameworkDetector:
    """Framework detection and attribution"""

    def detect_usage(self, text: str) -> List[FrameworkMatch]:
        """Detect framework usage in text"""

    def calculate_confidence(self, matches: List[str]) -> float:
        """Calculate detection confidence score"""

    def generate_attribution(self, framework: str, confidence: float) -> str:
        """Create framework attribution text"""
```

### **Framework Registration**
```yaml
# .claudedirector/config/frameworks.yaml
frameworks:
  team_topologies:
    name: "Team Topologies"
    category: "Organizational Design"
    description: "Team structure and cognitive load management"
    patterns:
      - "team topologies"
      - "cognitive load"
      - "stream-aligned team"
      - "platform team"
    confidence_threshold: 0.7
    personas: ["diego", "camille"]

  good_strategy_bad_strategy:
    name: "Good Strategy Bad Strategy"
    category: "Strategic Planning"
    description: "Strategy kernel and fluff detection"
    patterns:
      - "strategy kernel"
      - "good strategy"
      - "strategic coherence"
    confidence_threshold: 0.8
    personas: ["camille", "alvaro"]
```

---

## 📋 **Integration Guidelines**

### **Framework Selection Criteria**
- **Strategic Relevance**: Applicable to engineering leadership contexts
- **Proven Methodology**: Established track record in industry
- **Clear Application**: Specific use cases and implementation guidance
- **Measurable Impact**: Quantifiable benefits and outcomes

### **Detection Accuracy**
- **Pattern Matching**: Comprehensive keyword and phrase detection
- **Context Awareness**: Consider surrounding text for relevance
- **Confidence Scoring**: Accurate probability assessment
- **False Positive Prevention**: Avoid incorrect attributions

---

*Part of the [ClaudeDirector Development Guide](../DEVELOPMENT_GUIDE.md) suite.*
