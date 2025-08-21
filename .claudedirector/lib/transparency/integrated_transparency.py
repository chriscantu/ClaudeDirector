"""
Integrated Transparency System
Main integration point for MCP and framework transparency across ClaudeDirector personas
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time

from .mcp_transparency import MCPTransparencyMiddleware, MCPContext
from .framework_detection import FrameworkDetectionMiddleware, FrameworkUsage


@dataclass
class TransparencyContext:
    """Complete transparency context for a persona response"""
    mcp_context: MCPContext
    detected_frameworks: List[FrameworkUsage]
    processing_start_time: float
    persona: str

    def __init__(self, persona: str):
        self.mcp_context = MCPContext()
        self.detected_frameworks = []
        self.processing_start_time = time.time()
        self.persona = persona

    @property
    def total_processing_time(self) -> float:
        return time.time() - self.processing_start_time

    @property
    def has_enhancements(self) -> bool:
        return self.mcp_context.has_mcp_calls() or len(self.detected_frameworks) > 0


@dataclass
class MultiPersonaContext:
    """Context for multi-persona collaborative responses"""
    primary_persona: str
    consulting_personas: List[str]
    consultation_results: Dict[str, str]
    integration_mode: str = 'collaborative'  # 'sequential', 'collaborative', 'handoff'


@dataclass
class PersonaTransition:
    """Manages context handoff between personas"""
    from_persona: str
    to_persona: str
    context_summary: str
    handoff_reason: str

    def format_transition(self) -> str:
        return f"""🔄 Transitioning to {self.to_persona}

{self.to_persona}
**Context Received**: {self.context_summary}
Taking ownership of this {self.handoff_reason}..."""


class MultiPersonaResponseFormatter:
    """Formats multi-persona responses with clear UX patterns"""

    def __init__(self):
        # Persona header mappings
        self.persona_headers = {
            "diego": "🎯 Diego | Engineering Leadership",
            "camille": "📊 Camille | Strategic Technology",
            "rachel": "🎨 Rachel | Design Systems Strategy",
            "alvaro": "💼 Alvaro | Platform Investment Strategy",
            "sofia": "🤝 Sofia | Vendor Strategy",
            "elena": "⚖️ Elena | Compliance Strategy",
            "marcus": "📈 Marcus | Platform Adoption",
            "david": "💰 David | Financial Planning",
            "martin": "🏗️ Martin | Platform Architecture",
            "frontend": "💻 Frontend | UI Foundation Specialist",
            "backend": "🔧 Backend | Platform Services Specialist",
            "legal": "⚖️ Legal | International Compliance",
            "security": "🔒 Security | Platform Security Architecture",
            "data": "📊 Data | Analytics Strategy"
        }

    def _get_persona_header(self, persona: str) -> str:
        """Get standardized persona header"""
        return self.persona_headers.get(persona.lower(), f"🎯 {persona.title()}")

    def format_collaborative_response(self, primary_persona: str,
                                    consultant_responses: Dict[str, str],
                                    integration_summary: str) -> str:
        """Format collaborative multi-persona response (Rachel's Pattern 2)"""

        parts = [
            self._get_persona_header(primary_persona),
            "This requires cross-functional analysis.",
            "",
            "🤝 **Cross-Functional Analysis**"
        ]

        # Add consulting persona sections
        for persona, response in consultant_responses.items():
            if persona != 'integration':  # Skip integration summary
                parts.append(f"{self._get_persona_header(persona)}: {response}")

        parts.append("")

        # Primary persona integration
        parts.extend([
            self._get_persona_header(primary_persona),
            f"**Integrated Recommendation**: {integration_summary}"
        ])

        return "\n".join(parts)

    def format_sequential_consultation(self, primary_persona: str,
                                     consulting_persona: str,
                                     consultation_response: str,
                                     integration_response: str) -> str:
        """Format sequential persona consultation (Rachel's Pattern 1)"""

        primary_header = self._get_persona_header(primary_persona)
        consulting_header = self._get_persona_header(consulting_persona)
        consulting_name = consulting_persona.split('|')[0].strip() if '|' in consulting_persona else consulting_persona

        return f"""{primary_header}
Based on your challenge, let me consult with our specialist.

🔄 Consulting with {consulting_header}

{consulting_header}
{consultation_response}

🔄 Back to {primary_header}

{primary_header}
Building on {consulting_name}'s insights, {integration_response}"""

    def format_persona_handoff(self, transition: PersonaTransition, response: str) -> str:
        """Format persona handoff with context (Rachel's Pattern 3)"""

        from_header = self._get_persona_header(transition.from_persona)
        to_header = self._get_persona_header(transition.to_persona)

        return f"""{from_header}
This becomes primarily a {transition.handoff_reason}.

{transition.format_transition()}

{to_header}
{response}"""


class IntegratedTransparencySystem:
    """Unified transparency system for ClaudeDirector personas"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.mcp_middleware = MCPTransparencyMiddleware()
        self.framework_middleware = FrameworkDetectionMiddleware()
        self.multi_persona_formatter = MultiPersonaResponseFormatter()

        # Configuration options
        self.transparency_enabled = self.config.get('transparency_enabled', True)
        self.mcp_disclosure_enabled = self.config.get('mcp_disclosure_enabled', True)
        self.framework_attribution_enabled = self.config.get('framework_attribution_enabled', True)

        # Performance tracking
        self.performance_stats = {
            'total_requests': 0,
            'enhanced_requests': 0,
            'avg_transparency_overhead': 0.0,
            'mcp_calls_tracked': 0,
            'frameworks_detected': 0
        }

    def create_transparency_context(self, persona: str) -> TransparencyContext:
        """Create a new transparency context for a persona response"""
        return TransparencyContext(persona)

    def create_multi_persona_context(self, primary_persona: str, consulting_personas: List[str] = None,
                                   integration_mode: str = 'collaborative') -> MultiPersonaContext:
        """Create a new multi-persona context for collaborative responses"""
        return MultiPersonaContext(
            primary_persona=primary_persona,
            consulting_personas=consulting_personas or [],
            consultation_results={},
            integration_mode=integration_mode
        )

    def track_mcp_call(self, context: TransparencyContext, server_name: str,
                       capability: str, processing_time: float, success: bool = True,
                       error_message: Optional[str] = None):
        """Track an MCP call in the transparency context"""
        if self.mcp_disclosure_enabled:
            self.mcp_middleware.track_mcp_call(
                context.mcp_context, server_name, capability,
                processing_time, success, error_message
            )
            self.performance_stats['mcp_calls_tracked'] += 1

    def apply_transparency(self, context: TransparencyContext, response: str) -> str:
        """Apply full transparency treatment to a persona response"""
        if not self.transparency_enabled:
            return response

        transparency_start = time.time()

        # Track performance
        self.performance_stats['total_requests'] += 1

        # Detect frameworks used in the response
        if self.framework_attribution_enabled:
            context.detected_frameworks = self.framework_middleware.detect_frameworks_used(response)
            if context.detected_frameworks:
                self.performance_stats['frameworks_detected'] += len(context.detected_frameworks)

        enhanced_response = response

        # Apply MCP transparency
        if self.mcp_disclosure_enabled and context.mcp_context.has_mcp_calls():
            enhanced_response = self.mcp_middleware.wrap_persona_response(
                context.persona, enhanced_response, context.mcp_context
            )

        # Apply framework attribution
        if self.framework_attribution_enabled and context.detected_frameworks:
            enhanced_response = self.framework_middleware.add_framework_attribution(
                context.persona, enhanced_response, context.detected_frameworks
            )

        # Track performance overhead
        transparency_overhead = time.time() - transparency_start
        self._update_performance_stats(transparency_overhead, context.has_enhancements)

        return enhanced_response

    def create_transparency_summary(self, context: TransparencyContext) -> Dict[str, Any]:
        """Create a summary of transparency information for debugging/analytics"""
        return {
            'persona': context.persona,
            'processing_time': context.total_processing_time,
            'mcp_calls': len(context.mcp_context.mcp_calls),
            'mcp_servers_used': context.mcp_context.get_server_names(),
            'frameworks_detected': len(context.detected_frameworks),
            'framework_names': [f.framework_name for f in context.detected_frameworks],
            'has_mcp_failures': context.mcp_context.has_failures,
            'enhancement_applied': context.has_enhancements
        }

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the transparency system"""
        return {
            **self.performance_stats,
            'enhancement_rate': (
                self.performance_stats['enhanced_requests'] /
                max(self.performance_stats['total_requests'], 1)
            ) * 100
        }

    def apply_multi_persona_transparency(self, multi_context: MultiPersonaContext, response: str) -> str:
        """Apply transparency treatment to multi-persona responses"""
        if not self.transparency_enabled:
            return response

        # Determine the interaction pattern and apply appropriate formatting
        if multi_context.integration_mode == 'collaborative':
            return self._apply_collaborative_transparency(multi_context, response)
        elif multi_context.integration_mode == 'sequential':
            return self._apply_sequential_transparency(multi_context, response)
        elif multi_context.integration_mode == 'handoff':
            return self._apply_handoff_transparency(multi_context, response)
        else:
            # Fallback to standard single-persona transparency
            return response

    def _apply_collaborative_transparency(self, multi_context: MultiPersonaContext, response: str) -> str:
        """Apply transparency for collaborative multi-persona responses"""
        # Extract consultation results and integration summary from response
        consultant_responses = multi_context.consultation_results
        integration_summary = response

        # Phase 2: Apply multi-persona transparency enhancements
        enhanced_response = self.multi_persona_formatter.format_collaborative_response(
            multi_context.primary_persona,
            consultant_responses,
            integration_summary
        )

        # Add MCP transparency if consulting personas used MCP servers
        enhanced_response = self._apply_multi_persona_mcp_transparency(
            multi_context, enhanced_response
        )

        # Add framework attribution for multi-persona analysis
        enhanced_response = self._apply_multi_persona_framework_attribution(
            multi_context, enhanced_response
        )

        return enhanced_response

    def _apply_sequential_transparency(self, multi_context: MultiPersonaContext, response: str) -> str:
        """Apply transparency for sequential persona consultation"""
        if multi_context.consulting_personas:
            consulting_persona = multi_context.consulting_personas[0]
            consultation_response = multi_context.consultation_results.get(consulting_persona, "")

            # Phase 2: Apply multi-persona transparency enhancements
            enhanced_response = self.multi_persona_formatter.format_sequential_consultation(
                multi_context.primary_persona,
                consulting_persona,
                consultation_response,
                response
            )

            # Add MCP transparency for sequential consultation
            enhanced_response = self._apply_multi_persona_mcp_transparency(
                multi_context, enhanced_response
            )

            # Add framework attribution for sequential analysis
            enhanced_response = self._apply_multi_persona_framework_attribution(
                multi_context, enhanced_response
            )

            return enhanced_response

        return response

    def _apply_handoff_transparency(self, multi_context: MultiPersonaContext, response: str) -> str:
        """Apply transparency for persona handoff situations"""
        if multi_context.consulting_personas:
            # Create a transition object for the handoff
            transition = PersonaTransition(
                from_persona=multi_context.primary_persona,
                to_persona=multi_context.consulting_personas[0],
                context_summary="Strategic context transfer",
                handoff_reason="specialized domain expertise"
            )

            # Phase 2: Apply multi-persona transparency enhancements
            enhanced_response = self.multi_persona_formatter.format_persona_handoff(transition, response)

            # Add MCP transparency for handoff context
            enhanced_response = self._apply_multi_persona_mcp_transparency(
                multi_context, enhanced_response
            )

            # Add framework attribution for handoff analysis
            enhanced_response = self._apply_multi_persona_framework_attribution(
                multi_context, enhanced_response
            )

            return enhanced_response

        return response

    def wrap_multi_persona_response(self, multi_context: MultiPersonaContext, response: str,
                                   transparency_context: Optional[TransparencyContext] = None) -> str:
        """Complete multi-persona response wrapper with transparency integration"""
        enhanced_response = response

        # Apply multi-persona formatting first
        enhanced_response = self.apply_multi_persona_transparency(multi_context, enhanced_response)

        # If we have a transparency context, apply standard transparency enhancements
        if transparency_context and transparency_context.has_enhancements:
            # Apply MCP transparency if present
            if self.mcp_disclosure_enabled and transparency_context.mcp_context.has_mcp_calls():
                enhanced_response = self.mcp_middleware.wrap_persona_response(
                    multi_context.primary_persona, enhanced_response, transparency_context.mcp_context
                )

            # Apply framework attribution if present
            if self.framework_attribution_enabled and transparency_context.detected_frameworks:
                enhanced_response = self.framework_middleware.add_framework_attribution(
                    multi_context.primary_persona, enhanced_response, transparency_context.detected_frameworks
                )

        return enhanced_response

    def _apply_multi_persona_mcp_transparency(self, multi_context: MultiPersonaContext, response: str) -> str:
        """Apply MCP transparency for multi-persona interactions (Phase 2)"""
        if not self.mcp_disclosure_enabled:
            return response

        # Check if multi-persona context has associated MCP calls
        mcp_calls_summary = getattr(multi_context, 'mcp_calls_summary', None)
        if not mcp_calls_summary:
            return response

        # Add multi-persona MCP disclosure
        mcp_disclosure = self._format_multi_persona_mcp_disclosure(multi_context, mcp_calls_summary)
        if mcp_disclosure:
            return f"{response}\n\n{mcp_disclosure}"

        return response

    def _apply_multi_persona_framework_attribution(self, multi_context: MultiPersonaContext, response: str) -> str:
        """Apply framework attribution for multi-persona analysis (Phase 2)"""
        if not self.framework_attribution_enabled:
            return response

        # Check if multi-persona context has framework usage
        frameworks_used = getattr(multi_context, 'frameworks_used', None)
        if not frameworks_used:
            return response

        # Add multi-persona framework attribution
        framework_attribution = self._format_multi_persona_framework_attribution(
            multi_context, frameworks_used
        )
        if framework_attribution:
            return f"{response}\n\n{framework_attribution}"

        return response

    def _format_multi_persona_mcp_disclosure(self, multi_context: MultiPersonaContext,
                                           mcp_calls_summary: Dict[str, Any]) -> str:
        """Format MCP disclosure for multi-persona interactions"""
        if not mcp_calls_summary:
            return ""

        lines = ["🔧 **Multi-Persona MCP Enhancement**"]

        # Show which personas used which servers
        for persona, servers in mcp_calls_summary.items():
            if servers:
                persona_header = self.multi_persona_formatter._get_persona_header(persona)
                server_list = ", ".join(servers)
                lines.append(f"• {persona_header}: {server_list}")

        lines.append("---")
        lines.append("**Enhanced Analysis**: Cross-functional insights powered by strategic frameworks and collaborative intelligence.")

        return "\n".join(lines)

    def _format_multi_persona_framework_attribution(self, multi_context: MultiPersonaContext,
                                                  frameworks_used: Dict[str, List[str]]) -> str:
        """Format framework attribution for multi-persona analysis"""
        if not frameworks_used:
            return ""

        lines = ["📚 **Multi-Persona Framework Integration**"]

        # Show which personas used which frameworks
        for persona, frameworks in frameworks_used.items():
            if frameworks:
                persona_header = self.multi_persona_formatter._get_persona_header(persona)
                framework_list = ", ".join(frameworks)
                lines.append(f"• {persona_header}: {framework_list}")

        lines.append("---")
        lines.append("**Framework Attribution**: This cross-functional analysis combines proven strategic frameworks, adapted through collaborative expertise.")

        return "\n".join(lines)

    def coordinate_multi_persona_mcp_calls(self, transparency_contexts: Dict[str, TransparencyContext]) -> Dict[str, Any]:
        """Coordinate MCP calls across multiple personas (Phase 2)"""
        mcp_summary = {}

        for persona, context in transparency_contexts.items():
            if context.mcp_context.has_mcp_calls():
                servers_used = context.mcp_context.get_server_names()
                mcp_summary[persona] = servers_used

        return mcp_summary

    def coordinate_multi_persona_frameworks(self, transparency_contexts: Dict[str, TransparencyContext]) -> Dict[str, List[str]]:
        """Coordinate framework usage across multiple personas (Phase 2)"""
        framework_summary = {}

        for persona, context in transparency_contexts.items():
            if context.detected_frameworks:
                framework_names = [f.framework_name for f in context.detected_frameworks]
                framework_summary[persona] = framework_names

        return framework_summary

    def enhance_multi_persona_context(self, multi_context: MultiPersonaContext,
                                    transparency_contexts: Dict[str, TransparencyContext]) -> MultiPersonaContext:
        """Enhance multi-persona context with transparency information (Phase 2)"""
        # Add MCP calls summary
        multi_context.mcp_calls_summary = self.coordinate_multi_persona_mcp_calls(transparency_contexts)

        # Add frameworks used summary
        multi_context.frameworks_used = self.coordinate_multi_persona_frameworks(transparency_contexts)

        return multi_context

    def create_enhanced_multi_persona_response(self, primary_persona: str,
                                             consulting_personas: List[str],
                                             consultation_results: Dict[str, str],
                                             integration_response: str,
                                             transparency_contexts: Optional[Dict[str, TransparencyContext]] = None,
                                             integration_mode: str = 'collaborative') -> str:
        """Complete Phase 2 enhanced multi-persona response with full transparency (Convenience method)"""

        # Create multi-persona context
        multi_context = self.create_multi_persona_context(
            primary_persona, consulting_personas, integration_mode
        )
        multi_context.consultation_results = consultation_results

        # Enhance with transparency information if provided
        if transparency_contexts:
            multi_context = self.enhance_multi_persona_context(multi_context, transparency_contexts)

        # Apply complete transparency treatment
        return self.apply_multi_persona_transparency(multi_context, integration_response)

    def _update_performance_stats(self, transparency_overhead: float, has_enhancements: bool):
        """Update internal performance tracking"""
        # Update average overhead (exponential moving average)
        current_avg = self.performance_stats['avg_transparency_overhead']
        self.performance_stats['avg_transparency_overhead'] = (
            0.9 * current_avg + 0.1 * transparency_overhead
        )

        if has_enhancements:
            self.performance_stats['enhanced_requests'] += 1


class PersonaTransparencyDecorator:
    """Decorator class for adding transparency to persona responses"""

    def __init__(self, transparency_system: IntegratedTransparencySystem):
        self.transparency_system = transparency_system

    def __call__(self, persona_func):
        """Decorator that adds transparency to a persona response function"""
        async def wrapper(*args, **kwargs):
            # Extract persona name from function or kwargs
            persona = kwargs.get('persona', getattr(persona_func, 'persona_name', 'unknown'))

            # Create transparency context
            context = self.transparency_system.create_transparency_context(persona)

            # Add context to kwargs for the persona function to use
            kwargs['transparency_context'] = context

            # Call the original persona function
            response = await persona_func(*args, **kwargs)

            # Apply transparency enhancements
            enhanced_response = self.transparency_system.apply_transparency(context, response)

            return enhanced_response

        return wrapper


# Convenience function for easy integration
def transparent_persona_response(transparency_system: IntegratedTransparencySystem):
    """Decorator factory for transparent persona responses"""
    return PersonaTransparencyDecorator(transparency_system)


class TransparencyConfig:
    """Configuration management for transparency system"""

    DEFAULT_CONFIG = {
        'transparency_enabled': True,
        'mcp_disclosure_enabled': True,
        'framework_attribution_enabled': True,
        'performance_monitoring_enabled': True,
        'debug_mode': False
    }

    @classmethod
    def create_default(cls) -> Dict[str, Any]:
        """Create default transparency configuration"""
        return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def create_minimal(cls) -> Dict[str, Any]:
        """Create minimal transparency configuration"""
        return {
            'transparency_enabled': True,
            'mcp_disclosure_enabled': True,
            'framework_attribution_enabled': False,
            'performance_monitoring_enabled': False,
            'debug_mode': False
        }

    @classmethod
    def create_debug(cls) -> Dict[str, Any]:
        """Create debug transparency configuration with full logging"""
        config = cls.DEFAULT_CONFIG.copy()
        config['debug_mode'] = True
        return config


# Example usage integration
def create_transparency_system(config_type: str = "default") -> IntegratedTransparencySystem:
    """Factory function to create transparency system with predefined configs"""

    if config_type == "minimal":
        config = TransparencyConfig.create_minimal()
    elif config_type == "debug":
        config = TransparencyConfig.create_debug()
    else:
        config = TransparencyConfig.create_default()

    return IntegratedTransparencySystem(config)
