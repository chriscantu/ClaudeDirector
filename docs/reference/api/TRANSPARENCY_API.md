# Transparency System API

**Real-time AI enhancement disclosure and framework attribution system.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 🔍 **Transparency System API**

### **MCP Transparency Middleware**
```python
# .claudedirector/lib/claudedirector/transparency/mcp_transparency.py
class MCPTransparencyMiddleware:
    """Real-time disclosure of MCP server usage"""

    def __init__(self):
        self.active_disclosures = {}

    def start_disclosure(self, persona: str, server: str, capability: str) -> str:
        """Generate real-time MCP usage disclosure"""
        disclosure_id = self._generate_disclosure_id()

        disclosure_text = f"""🔧 Accessing MCP Server: {server} ({capability})
*{self._get_processing_message(server, capability)}...*"""

        self.active_disclosures[disclosure_id] = {
            'persona': persona,
            'server': server,
            'capability': capability,
            'timestamp': datetime.now()
        }

        return disclosure_text

    def complete_disclosure(self, disclosure_id: str, success: bool) -> str:
        """Complete MCP disclosure with results"""
        if disclosure_id not in self.active_disclosures:
            return ""

        disclosure = self.active_disclosures[disclosure_id]

        if success:
            return f"✅ Enhanced analysis complete using {disclosure['server']}"
        else:
            return f"⚠️ Enhancement unavailable, providing standard {disclosure['persona']} guidance"
```

### **Framework Attribution Engine**
```python
# .claudedirector/lib/claudedirector/transparency/framework_attribution.py
class FrameworkAttributionEngine:
    """Automatic detection and attribution of strategic frameworks"""

    def __init__(self):
        self.framework_patterns = self._load_framework_patterns()
        self.confidence_threshold = 0.7

    def detect_frameworks(self, response_text: str, persona: str) -> List[FrameworkAttribution]:
        """Detect strategic frameworks used in response"""
        attributions = []

        for framework_name, patterns in self.framework_patterns.items():
            confidence = self._calculate_confidence(response_text, patterns)

            if confidence >= self.confidence_threshold:
                attribution = FrameworkAttribution(
                    framework_name=framework_name,
                    confidence=confidence,
                    persona=persona,
                    evidence=self._extract_evidence(response_text, patterns)
                )
                attributions.append(attribution)

        return sorted(attributions, key=lambda x: x.confidence, reverse=True)

    def generate_attribution_text(self, attributions: List[FrameworkAttribution]) -> str:
        """Generate framework attribution disclosure"""
        if not attributions:
            return ""

        primary = attributions[0]
        return f"""📚 Strategic Framework: {primary.framework_name} detected
---
**Framework Attribution**: This analysis applies {primary.framework_name} methodology,
adapted through my {primary.persona} experience."""

    def _calculate_confidence(self, text: str, patterns: Dict) -> float:
        """Calculate framework detection confidence"""
        # Implementation details...
        pass
```

---

**🎯 The transparency system ensures complete visibility into AI enhancements and strategic framework usage.**
