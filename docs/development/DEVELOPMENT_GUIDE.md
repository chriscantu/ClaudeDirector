# ClaudeDirector Development Guide

**Comprehensive guide for extending and customizing ClaudeDirector's strategic AI architecture.**

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

## 🔧 **MCP Integration Development**

### **Basic MCP Client Implementation**
```python
# .claudedirector/lib/claudedirector/mcp/client_manager.py
import asyncio
from typing import Optional, Dict, Any

class MCPClient:
    """MCP protocol client for server communication"""

    def __init__(self):
        self.connections: Dict[str, MCPConnection] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}

    async def connect_server(self, server_config: dict) -> bool:
        """Establish connection to MCP server"""
        try:
            connection = MCPConnection(server_config)
            await connection.initialize()
            self.connections[server_config['name']] = connection
            return True
        except Exception as e:
            print(f"❌ Failed to connect to {server_config['name']}: {e}")
            return False

    async def call_capability(self, server: str, capability: str, params: dict) -> dict:
        """Call specific capability on MCP server"""
        if server not in self.connections:
            raise ConnectionError(f"Server {server} not connected")

        connection = self.connections[server]
        return await connection.call_capability(capability, params)
```

### **MCP Server Configuration**
```yaml
# .claudedirector/config/mcp_servers.yaml
servers:
  sequential:
    command: "npx"
    args: ["-y", "@sequential/mcp-server"]
    connection_type: "stdio"
    capabilities: ["systematic_analysis", "business_strategy"]
    timeout: 8

  context7:
    command: "python"
    args: ["-m", "context7.server"]
    connection_type: "stdio"
    capabilities: ["pattern_access", "methodology_lookup"]
    timeout: 8
    fallback:
      transport: "http"
      url: "https://api.context7.ai/mcp"
```

## 🎭 **Custom Persona Development**

### **Creating New Personas**
```python
# .claudedirector/lib/claudedirector/personas/custom_persona.py
from .base_persona import BasePersona

class CustomPersona(BasePersona):
    """Custom persona for specific domain expertise"""

    def __init__(self):
        super().__init__(
            name="custom",
            header="🔧 Custom | Domain Expertise",
            domain="domain_specialization",
            personality_traits={
                "communication_style": "direct and analytical",
                "decision_approach": "data-driven with practical focus",
                "interaction_pattern": "structured problem-solving"
            }
        )

    def enhance_response(self, response: str, context: dict) -> str:
        """Apply custom persona personality and expertise"""
        enhanced = self.add_personality_markers(response)
        enhanced = self.apply_domain_expertise(enhanced, context)
        return enhanced

    def get_framework_preferences(self) -> List[str]:
        """Return preferred strategic frameworks for this persona"""
        return ["Custom Framework", "Domain-Specific Methodology"]
```

### **Registering Custom Personas**
```python
# .claudedirector/config/custom_personas.py
from claudedirector.personas.custom_persona import CustomPersona

# Register custom persona
CUSTOM_PERSONAS = {
    "custom": CustomPersona(),
}

# Integration with persona manager
def register_custom_personas(persona_manager):
    for name, persona in CUSTOM_PERSONAS.items():
        persona_manager.register_persona(name, persona)
```

## 📚 **Framework Integration**

### **Adding Strategic Frameworks**
```python
# .claudedirector/frameworks/custom_framework.py
class CustomFramework:
    """Custom strategic framework implementation"""

    def __init__(self):
        self.name = "Custom Strategic Framework"
        self.confidence_threshold = 0.7
        self.detection_patterns = [
            r"strategic.*planning",
            r"custom.*methodology",
            r"domain.*analysis"
        ]

    def detect_usage(self, response: str) -> float:
        """Detect framework usage and return confidence score"""
        confidence = 0.0
        for pattern in self.detection_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                confidence += 0.3
        return min(confidence, 1.0)

    def generate_attribution(self) -> str:
        """Generate framework attribution text"""
        return f"""📚 Strategic Framework: {self.name} detected
---
**Framework Attribution**: This analysis applies {self.name} methodology,
adapted through domain expertise."""
```

### **Framework Registration**
```yaml
# .claudedirector/config/frameworks.yaml
custom_frameworks:
  - name: "Custom Strategic Framework"
    module: "claudedirector.frameworks.custom_framework"
    class: "CustomFramework"
    enabled: true
    priority: 1
```

## 🔒 **Testing & Quality Assurance**

### **Test Suite Structure**
```
📁 .claudedirector/tests/
├── 📁 unit/                 # Unit tests
│   ├── test_personas.py     # Persona functionality
│   ├── test_transparency.py # Transparency system
│   └── test_frameworks.py   # Framework detection
├── 📁 integration/          # Integration tests
│   ├── test_mcp_integration.py  # MCP server integration
│   └── test_cursor_integration.py  # Cursor conversation flow
├── 📁 regression/           # Regression tests
│   └── test_mcp_transparency_p0.py  # P0 feature protection
└── run_mcp_transparency_tests.py  # Unified test runner
```

### **Writing Tests for Custom Components**
```python
# .claudedirector/tests/unit/test_custom_persona.py
import unittest
from claudedirector.personas.custom_persona import CustomPersona

class TestCustomPersona(unittest.TestCase):

    def setUp(self):
        self.persona = CustomPersona()

    def test_persona_initialization(self):
        """Test persona initializes correctly"""
        self.assertEqual(self.persona.name, "custom")
        self.assertIn("🔧 Custom", self.persona.header)

    def test_response_enhancement(self):
        """Test persona enhances responses correctly"""
        response = "Here is strategic guidance."
        context = {"complexity": "high"}

        enhanced = self.persona.enhance_response(response, context)

        self.assertIn(self.persona.header, enhanced)
        self.assertGreater(len(enhanced), len(response))

    def test_framework_preferences(self):
        """Test persona framework preferences"""
        frameworks = self.persona.get_framework_preferences()
        self.assertIsInstance(frameworks, list)
        self.assertGreater(len(frameworks), 0)

if __name__ == "__main__":
    unittest.main()
```

### **Running Test Suites**
```bash
# Run all tests
python3 .claudedirector/tests/run_mcp_transparency_tests.py

# Run specific test suites
python3 -m pytest .claudedirector/tests/unit/ -v
python3 -m pytest .claudedirector/tests/integration/ -v

# Run with coverage
python3 -m pytest .claudedirector/tests/ --cov=claudedirector --cov-report=html
```

## 📊 **Performance Optimization**

### **Response Time Optimization**
```python
# .claudedirector/lib/claudedirector/performance/optimizer.py
class ResponseOptimizer:
    """Optimize response generation performance"""

    def __init__(self):
        self.cache = LRUCache(maxsize=1000)
        self.complexity_cache = {}

    def optimize_persona_selection(self, context: str) -> str:
        """Cache persona selection for similar contexts"""
        context_hash = hash(context)
        if context_hash in self.cache:
            return self.cache[context_hash]

        persona = self.select_persona_uncached(context)
        self.cache[context_hash] = persona
        return persona

    def optimize_framework_detection(self, response: str) -> List[Framework]:
        """Batch framework detection for efficiency"""
        if len(response) < 100:  # Skip detection for short responses
            return []

        return self.detect_frameworks_full(response)
```

### **Memory Management**
```python
# .claudedirector/lib/claudedirector/core/memory_manager.py
class MemoryManager:
    """Manage conversation memory and context efficiently"""

    def __init__(self, max_context_length: int = 10000):
        self.max_context_length = max_context_length
        self.context_buffer = deque(maxlen=100)

    def add_conversation_turn(self, user_input: str, response: str):
        """Add conversation turn with automatic truncation"""
        turn = ConversationTurn(user_input, response, timestamp=time.time())
        self.context_buffer.append(turn)

        # Truncate if context too long
        total_length = sum(len(turn.combined_text) for turn in self.context_buffer)
        while total_length > self.max_context_length and len(self.context_buffer) > 1:
            removed = self.context_buffer.popleft()
            total_length -= len(removed.combined_text)
```

## 🚀 **Deployment & Production**

### **Environment Configuration**
```bash
# Production environment variables
export CLAUDEDIRECTOR_ENV=production
export LOG_LEVEL=info
export MCP_TIMEOUT=5
export CACHE_TTL=3600

# Performance tuning
export MAX_CONCURRENT_MCP=3
export COMPLEXITY_THRESHOLD=4
export TRANSPARENCY_CACHE_SIZE=1000
```

### **Production Monitoring**
```python
# .claudedirector/lib/claudedirector/monitoring/health_check.py
class HealthMonitor:
    """Monitor system health and performance"""

    def check_mcp_servers(self) -> Dict[str, bool]:
        """Check MCP server connectivity"""
        results = {}
        for server_name in self.mcp_client.connections:
            results[server_name] = self.mcp_client.health_check(server_name)
        return results

    def check_performance_metrics(self) -> Dict[str, float]:
        """Check response time and resource usage"""
        return {
            "avg_response_time": self.get_avg_response_time(),
            "memory_usage": self.get_memory_usage(),
            "cache_hit_rate": self.get_cache_hit_rate()
        }
```

## 📋 **Development Workflow**

### **Contributing Guidelines**
1. **Fork and branch**: Create feature branches for all changes
2. **Test first**: Write tests before implementing features
3. **Documentation**: Update documentation for all changes
4. **Quality gates**: All tests must pass before merging
5. **AI cleanup**: Use the AI cleanup enforcement hook

### **Code Quality Standards**
```bash
# Pre-commit hooks ensure quality
git commit -m "Your changes"  # Runs automatically:
# - Whitespace cleanup
# - Security scanning
# - Test validation (NO SKIPPING)
# - AI cleanup enforcement
# - SOLID principle validation
```

---

**🎯 Ready to extend ClaudeDirector with custom strategic capabilities!**
