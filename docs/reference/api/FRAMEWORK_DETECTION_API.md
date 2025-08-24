# Framework Detection API

**Automatic detection and attribution of strategic frameworks in AI responses.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 📚 **Framework Detection API**

### **Framework Detector**
```python
# .claudedirector/lib/claudedirector/frameworks/framework_detector.py
class FrameworkDetector:
    """Automatic strategic framework identification"""

    def __init__(self):
        self.frameworks = self._load_frameworks()
        self.confidence_threshold = 0.7

    def detect_frameworks(self, response: str) -> List[FrameworkMatch]:
        """Identify applied strategic methodologies"""
        matches = []

        for framework in self.frameworks:
            confidence = self._calculate_confidence(response, framework)

            if confidence >= self.confidence_threshold:
                matches.append(FrameworkMatch(
                    framework=framework,
                    confidence=confidence,
                    matched_patterns=self._get_matched_patterns(response, framework)
                ))

        # Sort by confidence (highest first)
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches

    def _calculate_confidence(self, response: str, framework: Framework) -> float:
        """Calculate framework application confidence"""
        total_patterns = len(framework.patterns)
        matched_patterns = 0

        for pattern in framework.patterns:
            if re.search(pattern.regex, response, re.IGNORECASE):
                matched_patterns += pattern.weight

        return min(matched_patterns / total_patterns, 1.0)

    def generate_attribution(self, frameworks: List[FrameworkMatch]) -> str:
        """Create framework attribution display"""
        if not frameworks:
            return ""

        if len(frameworks) == 1:
            framework = frameworks[0].framework
            return f"""📚 Strategic Framework: {framework.name} detected
---
**Framework Attribution**: This analysis applies {framework.name} methodology,
adapted through domain expertise."""
        else:
            framework_list = "\n".join([
                f"• {match.framework.name} (confidence: {match.confidence:.1%})"
                for match in frameworks[:3]  # Show top 3
            ])
            return f"""📚 Multiple Strategic Frameworks detected:
{framework_list}
---
**Framework Attribution**: This analysis integrates multiple strategic methodologies."""
```
