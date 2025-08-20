# ClaudeDirector API Reference

**Complete API documentation for ClaudeDirector's strategic AI architecture.**

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

    def detect_and_attribute(self, response: str, persona: str) -> str:
        """Detect frameworks and generate attribution"""
        detected_frameworks = self._detect_frameworks(response)

        if not detected_frameworks:
            return ""

        attribution = self._generate_attribution(detected_frameworks, persona)
        return attribution

    def _detect_frameworks(self, response: str) -> List[Framework]:
        """Pattern matching for framework detection"""
        detected = []

        for framework in self.framework_patterns:
            confidence = self._calculate_confidence(response, framework)
            if confidence > 0.7:
                detected.append({
                    'framework': framework,
                    'confidence': confidence
                })

        return detected

    def _generate_attribution(self,
                            frameworks: List[Framework],
                            persona: str) -> str:
        """Generate framework attribution text"""
        if len(frameworks) == 1:
            return f"""📚 Strategic Framework: {frameworks[0]['framework']['name']} detected
---
**Framework Attribution**: This analysis applies {frameworks[0]['framework']['name']} methodology,
adapted through my {persona} experience."""
        else:
            framework_list = "\n".join([
                f"• {fw['framework']['name']}" for fw in frameworks
            ])
            return f"""📚 Multiple Strategic Frameworks detected:
{framework_list}
---
**Framework Attribution**: This analysis integrates multiple strategic methodologies."""
```

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

## 🔧 **MCP Integration API**

### **MCP Client Manager**
```python
# .claudedirector/lib/claudedirector/mcp/client_manager.py
class MCPClientManager:
    """Manage MCP server connections and capabilities"""

    def __init__(self):
        self.clients = {}
        self.server_configs = self._load_server_configs()
        self.circuit_breakers = {}

    async def initialize_servers(self) -> Dict[str, bool]:
        """Initialize all configured MCP servers"""
        results = {}

        for server_name, config in self.server_configs.items():
            try:
                client = MCPClient(config)
                await client.connect()
                self.clients[server_name] = client
                self.circuit_breakers[server_name] = CircuitBreaker()
                results[server_name] = True
            except Exception as e:
                print(f"❌ Failed to initialize {server_name}: {e}")
                results[server_name] = False

        return results

    async def call_capability(self,
                            server: str,
                            capability: str,
                            params: dict,
                            timeout: float = 5.0) -> dict:
        """Call specific capability on MCP server with circuit breaker"""
        if server not in self.clients:
            raise ServerNotAvailableError(f"Server {server} not available")

        circuit_breaker = self.circuit_breakers[server]

        if circuit_breaker.is_open:
            raise CircuitBreakerOpenError(f"Circuit breaker open for {server}")

        try:
            async with asyncio.timeout(timeout):
                result = await self.clients[server].call_capability(capability, params)
                circuit_breaker.record_success()
                return result
        except Exception as e:
            circuit_breaker.record_failure()
            raise MCPCallError(f"Failed to call {capability} on {server}: {e}")

    def get_server_capabilities(self, server: str) -> List[str]:
        """Get available capabilities for specific server"""
        if server not in self.server_configs:
            return []

        return self.server_configs[server].get('capabilities', [])

    def health_check(self, server: str) -> bool:
        """Check health of specific MCP server"""
        if server not in self.clients:
            return False

        try:
            return self.clients[server].is_healthy()
        except Exception:
            return False
```

### **MCP Client Implementation**
```python
# .claudedirector/lib/claudedirector/mcp/mcp_client.py
class MCPClient:
    """Individual MCP server client"""

    def __init__(self, config: dict):
        self.config = config
        self.connection = None
        self.capabilities = config.get('capabilities', [])

    async def connect(self):
        """Establish connection to MCP server"""
        transport_type = self.config.get('transport', 'stdio')

        if transport_type == 'stdio':
            self.connection = await self._create_stdio_connection()
        elif transport_type == 'http':
            self.connection = await self._create_http_connection()
        else:
            raise UnsupportedTransportError(f"Transport {transport_type} not supported")

    async def call_capability(self, capability: str, params: dict) -> dict:
        """Call specific capability with parameters"""
        if capability not in self.capabilities:
            raise CapabilityNotSupportedError(f"Capability {capability} not supported")

        request = {
            'method': capability,
            'params': params,
            'id': self._generate_request_id()
        }

        response = await self.connection.send_request(request)
        return response

    def is_healthy(self) -> bool:
        """Check if connection is healthy"""
        if not self.connection:
            return False

        return self.connection.is_alive()

    async def _create_stdio_connection(self):
        """Create stdio transport connection"""
        # Implementation for stdio transport
        pass

    async def _create_http_connection(self):
        """Create HTTP transport connection"""
        # Implementation for HTTP transport
        pass
```

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

## 🔄 **Conversation Management API**

### **Conversation Manager**
```python
# .claudedirector/lib/claudedirector/core/conversation_manager.py
class ConversationManager:
    """Manage conversation state and context"""

    def __init__(self):
        self.current_session = None
        self.context_buffer = deque(maxlen=50)
        self.persona_history = []

    def start_conversation(self, user_id: str = None) -> ConversationSession:
        """Start new conversation session"""
        self.current_session = ConversationSession(
            id=self._generate_session_id(),
            user_id=user_id,
            started_at=datetime.now()
        )
        return self.current_session

    def add_interaction(self,
                       user_input: str,
                       response: str,
                       persona: str,
                       mcp_servers_used: List[str] = None,
                       frameworks_detected: List[str] = None) -> ConversationTurn:
        """Add conversation turn with metadata"""
        turn = ConversationTurn(
            user_input=user_input,
            response=response,
            persona=persona,
            mcp_servers_used=mcp_servers_used or [],
            frameworks_detected=frameworks_detected or [],
            timestamp=datetime.now()
        )

        self.context_buffer.append(turn)
        self.persona_history.append(persona)

        if self.current_session:
            self.current_session.add_turn(turn)

        return turn

    def get_context_summary(self, max_turns: int = 5) -> str:
        """Get summarized context from recent turns"""
        recent_turns = list(self.context_buffer)[-max_turns:]

        summary_parts = []
        for turn in recent_turns:
            summary_parts.append(f"User: {turn.user_input[:100]}...")
            summary_parts.append(f"{turn.persona}: {turn.response[:200]}...")

        return "\n".join(summary_parts)

    def get_persona_continuity(self) -> str:
        """Analyze persona usage patterns for continuity"""
        if len(self.persona_history) < 2:
            return "single_persona"

        if len(set(self.persona_history[-3:])) == 1:
            return "consistent_persona"
        elif len(set(self.persona_history[-3:])) > 2:
            return "multi_persona_collaboration"
        else:
            return "persona_transition"
```

## 📊 **Performance Monitoring API**

### **Performance Monitor**
```python
# .claudedirector/lib/claudedirector/monitoring/performance_monitor.py
class PerformanceMonitor:
    """Monitor system performance and resource usage"""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.thresholds = {
            'response_time': 2.0,  # seconds
            'mcp_timeout': 5.0,    # seconds
            'memory_usage': 0.8,   # 80% of available
        }

    def record_response_time(self, operation: str, duration: float):
        """Record response time for operation"""
        self.metrics[f"{operation}_response_time"].append({
            'duration': duration,
            'timestamp': time.time()
        })

        # Alert if threshold exceeded
        if duration > self.thresholds['response_time']:
            self._trigger_alert(f"Slow response: {operation} took {duration:.2f}s")

    def record_mcp_call(self, server: str, capability: str, duration: float, success: bool):
        """Record MCP server call metrics"""
        self.metrics[f"mcp_{server}_{capability}"].append({
            'duration': duration,
            'success': success,
            'timestamp': time.time()
        })

    def get_performance_summary(self) -> dict:
        """Get performance metrics summary"""
        summary = {}

        for metric_name, measurements in self.metrics.items():
            if not measurements:
                continue

            recent_measurements = [
                m for m in measurements
                if time.time() - m['timestamp'] < 3600  # Last hour
            ]

            if recent_measurements:
                durations = [m['duration'] for m in recent_measurements]
                summary[metric_name] = {
                    'count': len(recent_measurements),
                    'avg_duration': sum(durations) / len(durations),
                    'max_duration': max(durations),
                    'min_duration': min(durations)
                }

        return summary

    def check_health(self) -> Dict[str, bool]:
        """Check overall system health"""
        health_checks = {}

        # Check response times
        recent_responses = self._get_recent_metric('response_time')
        if recent_responses:
            avg_response = sum(recent_responses) / len(recent_responses)
            health_checks['response_time_healthy'] = avg_response < self.thresholds['response_time']

        # Check MCP server availability
        for server in ['sequential', 'context7', 'magic']:
            recent_calls = self._get_recent_metric(f'mcp_{server}')
            if recent_calls:
                success_rate = sum(1 for call in recent_calls if call.get('success', False)) / len(recent_calls)
                health_checks[f'{server}_healthy'] = success_rate > 0.8

        return health_checks
```

## 🛠️ **Configuration API**

### **Configuration Manager**
```python
# .claudedirector/lib/claudedirector/config/config_manager.py
class ConfigurationManager:
    """Manage ClaudeDirector configuration"""

    def __init__(self, config_path: str = ".claudedirector/config"):
        self.config_path = Path(config_path)
        self.config = self._load_configuration()

    def _load_configuration(self) -> dict:
        """Load configuration from files"""
        config = {}

        # Load base configuration
        base_config_file = self.config_path / "default_config.yaml"
        if base_config_file.exists():
            with open(base_config_file) as f:
                config.update(yaml.safe_load(f))

        # Load user configuration (overrides)
        user_config_file = self.config_path / "user_config.yaml"
        if user_config_file.exists():
            with open(user_config_file) as f:
                user_config = yaml.safe_load(f)
                config = self._merge_configs(config, user_config)

        return config

    def get(self, key: str, default=None):
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value):
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config_section = self.config

        for k in keys[:-1]:
            if k not in config_section:
                config_section[k] = {}
            config_section = config_section[k]

        config_section[keys[-1]] = value

    def save_user_config(self):
        """Save user configuration to file"""
        user_config_file = self.config_path / "user_config.yaml"
        with open(user_config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
```

---

**🎯 Complete API reference for extending ClaudeDirector's strategic AI architecture.**
