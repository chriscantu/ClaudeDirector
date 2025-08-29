"""
Real MCP Server Integration for ClaudeDirector Transparency System
Integrates our transparency system with the actual ClaudeDirector MCP infrastructure
"""

import time
from typing import Dict, Any, Optional, List
import structlog

from .integrated_transparency import IntegratedTransparencySystem, TransparencyContext
from .persona_integration import TransparentPersonaManager, MCPIntegrationHelper
try:
    from ..integration.unified_bridge import MCPUseClient, MCPResponse
except ImportError:
    # Fallback classes for testing
    class MCPUseClient:
        def __init__(self, *args, **kwargs):
            self.is_available = False

    class MCPResponse:
        def __init__(self, *args, **kwargs):
            self.success = False

logger = structlog.get_logger(__name__)


class RealMCPIntegrationHelper(MCPIntegrationHelper):
    """Enhanced MCP Integration Helper that uses real ClaudeDirector MCP servers"""

    def __init__(
        self,
        transparency_context: TransparencyContext,
        persona_manager: TransparentPersonaManager,
        mcp_client: MCPUseClient,
    ):
        super().__init__(transparency_context, persona_manager)
        self.mcp_client = mcp_client
        self.server_mapping = self._build_server_mapping()

    def _build_server_mapping(self) -> Dict[str, List[str]]:
        """Build mapping of persona capabilities to MCP servers"""
        mapping = {
            "diego": ["sequential"],  # Strategic analysis and systematic frameworks
            "camille": [
                "sequential",
                "context7",
            ],  # Executive strategy and innovation patterns
            "rachel": [
                "context7",
                "magic",
            ],  # Design systems and organizational patterns
            "alvaro": [
                "sequential",
                "context7",
            ],  # Business strategy and competitive analysis
            "martin": [
                "context7",
                "magic",
            ],  # Architecture patterns and technical visualization
        }
        return mapping

    async def call_mcp_server(
        self, server_name: str, capability: str, **call_kwargs
    ) -> Any:
        """
        Make an actual MCP server call with automatic transparency tracking

        Args:
            server_name: Name of the MCP server (sequential, context7, magic)
            capability: Capability being called
            **call_kwargs: Arguments for the MCP call

        Returns:
            Result from MCP server call
        """
        start_time = time.time()

        try:
            # Check if server is available
            if not self.mcp_client.is_server_available(server_name):
                processing_time = time.time() - start_time

                # Track failed call
                self.persona_manager.track_mcp_call(
                    self.transparency_context,
                    server_name,
                    capability,
                    processing_time,
                    success=False,
                    error_message=f"Server {server_name} not available",
                )

                # Return fallback response
                return {
                    "server": server_name,
                    "capability": capability,
                    "result": f"Server {server_name} temporarily unavailable",
                    "fallback": True,
                    "kwargs": call_kwargs,
                }

            # Build query from capability and kwargs
            query = self._build_query(capability, call_kwargs)

            # Execute MCP call
            response: MCPResponse = await self.mcp_client.execute_analysis(
                server_name, query, timeout=8
            )

            processing_time = time.time() - start_time

            if response.success:
                # Track successful call
                self.persona_manager.track_mcp_call(
                    self.transparency_context,
                    server_name,
                    capability,
                    processing_time,
                    success=True,
                )

                return {
                    "server": server_name,
                    "capability": capability,
                    "result": response.content,
                    "processing_time": response.processing_time,
                    "kwargs": call_kwargs,
                }
            else:
                # Track failed call
                self.persona_manager.track_mcp_call(
                    self.transparency_context,
                    server_name,
                    capability,
                    processing_time,
                    success=False,
                    error_message=response.error_message,
                )

                raise Exception(f"MCP server error: {response.error_message}")

        except Exception as e:
            processing_time = time.time() - start_time

            # Track failed call
            self.persona_manager.track_mcp_call(
                self.transparency_context,
                server_name,
                capability,
                processing_time,
                success=False,
                error_message=str(e),
            )

            logger.error(
                "mcp_server_call_failed",
                server=server_name,
                capability=capability,
                error=str(e),
            )
            raise e

    def _build_query(self, capability: str, kwargs: Dict[str, Any]) -> str:
        """Build MCP query from capability and arguments"""

        base_query = kwargs.get("query", kwargs.get("prompt", ""))

        # Add capability-specific context
        if capability == "systematic_analysis":
            query = f"Please provide systematic analysis for: {base_query}"
        elif capability == "framework_application":
            framework = kwargs.get("framework", "strategic framework")
            query = f"Apply {framework} to analyze: {base_query}"
        elif capability == "pattern_access":
            pattern_type = kwargs.get("pattern_type", "business pattern")
            query = f"Access {pattern_type} patterns for: {base_query}"
        elif capability == "architecture_patterns":
            query = f"Provide architecture pattern guidance for: {base_query}"
        elif capability == "business_visualization":
            viz_type = kwargs.get("visualization_type", "business diagram")
            query = f"Create {viz_type} visualization for: {base_query}"
        elif capability == "competitive_intel":
            market = kwargs.get("market", "current market")
            query = f"Analyze competitive intelligence in {market} for: {base_query}"
        else:
            # Generic capability query
            query = f"Execute {capability} for: {base_query}"

        return query

    async def call_persona_appropriate_servers(
        self, persona: str, capability: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Call MCP servers appropriate for the given persona and capability

        Args:
            persona: Name of the persona (diego, camille, rachel, alvaro, martin)
            capability: Capability needed
            **kwargs: Arguments for the MCP calls

        Returns:
            List of results from appropriate MCP servers
        """
        appropriate_servers = self.server_mapping.get(persona, [])
        results = []

        for server in appropriate_servers:
            # Check if server has the required capability
            server_capabilities = self.mcp_client.get_server_capabilities(server)

            if capability in server_capabilities:
                try:
                    result = await self.call_mcp_server(server, capability, **kwargs)
                    results.append(result)
                except Exception as e:
                    logger.warning(f"Failed to call {server} for {capability}: {e}")
                    continue

        return results


class EnhancedTransparentPersonaManager(TransparentPersonaManager):
    """
    Enhanced Transparent Persona Manager integrated with real ClaudeDirector MCP infrastructure
    """

    def __init__(
        self,
        transparency_system: IntegratedTransparencySystem,
        mcp_client: MCPUseClient,
    ):
        super().__init__(transparency_system)
        self.mcp_client = mcp_client

        # Register enhanced persona handlers that use real MCP servers
        self._setup_mcp_enhanced_personas()

    def _setup_mcp_enhanced_personas(self):
        """Setup enhanced persona handlers that use real MCP servers"""

        # Diego - Strategic Leadership with Sequential server
        self.register_persona("diego", self._diego_mcp_handler)

        # Camille - Innovation & Technology with Sequential + Context7
        self.register_persona("camille", self._camille_mcp_handler)

        # Rachel - Change Management with Context7 + Magic
        self.register_persona("rachel", self._rachel_mcp_handler)

        # Alvaro - Technical Excellence with Sequential + Context7
        self.register_persona("alvaro", self._alvaro_mcp_handler)

        # Martin - Business Development with Context7 + Magic
        self.register_persona("martin", self._martin_mcp_handler)

    async def _diego_mcp_handler(self, query: str, **kwargs) -> str:
        """Diego - Strategic Leadership with real MCP server integration"""
        transparency_context = kwargs.get("transparency_context")
        mcp_helper = RealMCPIntegrationHelper(
            transparency_context, self, self.mcp_client
        )

        try:
            # Use Sequential server for systematic strategic analysis
            results = await mcp_helper.call_persona_appropriate_servers(
                "diego", "systematic_analysis", query=query
            )

            # Build enhanced response
            base_response = f"""**Strategic Analysis - Diego**

I'm excited to explore this challenge with you. Let me break this down systematically while keeping the human element front and center.

**Strategic Framework Application:**"""

            if results:
                # Incorporate MCP analysis
                mcp_analysis = results[0].get("result", "Analysis completed")
                base_response += f"""

{mcp_analysis}

**Strategic Recommendations:**
1. Market positioning using Porter's Five Forces analysis
2. Resource allocation through BCG Matrix evaluation
3. Risk mitigation via scenario planning methodologies

This analysis leverages advanced strategic intelligence capabilities to ensure comprehensive coverage."""
            else:
                # Fallback when MCP servers unavailable
                base_response += """

Based on systematic strategic analysis principles:

1. **Objective Assessment**: What are we really trying to achieve here?
2. **Market Dynamics**: Understanding competitive forces and positioning
3. **Resource Optimization**: Ensuring sustainable value creation
4. **Risk Management**: Building resilience into our strategic approach

While my enhanced strategic analysis systems are temporarily unavailable, I'm drawing on proven strategic frameworks to provide comprehensive guidance."""

            return base_response.strip()

        except Exception as e:
            logger.error("diego_mcp_handler_error", error=str(e))
            return self._fallback_response("diego", query, str(e))

    async def _camille_mcp_handler(self, query: str, **kwargs) -> str:
        """Camille - Innovation & Technology with MCP integration"""
        transparency_context = kwargs.get("transparency_context")
        mcp_helper = RealMCPIntegrationHelper(
            transparency_context, self, self.mcp_client
        )

        try:
            # Use Sequential for strategic analysis + Context7 for innovation patterns
            strategic_results = await mcp_helper.call_mcp_server(
                "sequential",
                "framework_application",
                query=query,
                framework="innovation framework",
            )

            pattern_results = await mcp_helper.call_mcp_server(
                "context7",
                "pattern_access",
                query=query,
                pattern_type="innovation pattern",
            )

            base_response = f"""**Innovation Analysis - Camille**

As we think about organizational strategy, let's be honest about what we're dealing with here. The people problem is usually harder than the technical problem.

**Innovation Framework Application:**"""

            if strategic_results or pattern_results:
                if strategic_results and strategic_results.get("result"):
                    base_response += f"""

**Strategic Innovation Analysis:**
{strategic_results['result']}"""

                if pattern_results and pattern_results.get("result"):
                    base_response += f"""

**Innovation Pattern Insights:**
{pattern_results['result']}"""

                base_response += """

**Recommended Innovation Approach:**
- Design Thinking methodology for user-centric solutions
- Lean Startup principles for rapid validation
- Technology integration opportunities for competitive advantage

This analysis leverages advanced innovation intelligence and proven organizational patterns."""
            else:
                base_response += """

**Innovation Strategy Focus:**
1. **User-Centered Design**: What problems are we really solving?
2. **Technology Integration**: How can we leverage emerging capabilities?
3. **Organizational Alignment**: Building innovation culture and processes
4. **Market Validation**: Testing assumptions before scaling

While my enhanced innovation analysis systems are temporarily offline, I'm applying proven innovation frameworks and organizational transformation patterns."""

            return base_response.strip()

        except Exception as e:
            logger.error("camille_mcp_handler_error", error=str(e))
            return self._fallback_response("camille", query, str(e))

    async def _rachel_mcp_handler(self, query: str, **kwargs) -> str:
        """Rachel - Change Management with Context7 and Magic integration"""
        transparency_context = kwargs.get("transparency_context")
        mcp_helper = RealMCPIntegrationHelper(
            transparency_context, self, self.mcp_client
        )

        try:
            # Use Context7 for organizational patterns + Magic for visualizations
            org_results = await mcp_helper.call_mcp_server(
                "context7",
                "pattern_access",
                query=query,
                pattern_type="organizational pattern",
            )

            # Try to get visualization support
            viz_results = None
            if self.mcp_client.is_server_available("magic"):
                viz_results = await mcp_helper.call_mcp_server(
                    "magic",
                    "business_visualization",
                    query=query,
                    visualization_type="change roadmap",
                )

            base_response = f"""**Change Management Analysis - Rachel**

I love how this impacts the user experience. Let's think about this holistically - both for end users and the teams building it.

**Organizational Change Assessment:**"""

            if org_results and org_results.get("result"):
                base_response += f"""

**Organizational Pattern Analysis:**
{org_results['result']}

**Change Management Framework:**
- Kotter's 8-Step Change Model application
- ADKAR framework for individual change readiness
- Design system scaling methodology for organizational alignment"""

                if viz_results and viz_results.get("result"):
                    base_response += f"""

**Change Visualization:**
{viz_results['result']}"""

                base_response += """

This analysis incorporates advanced organizational intelligence and proven change management patterns."""
            else:
                base_response += """

**Change Management Focus:**
1. **Stakeholder Alignment**: Who needs to be engaged and how?
2. **Communication Strategy**: Clear, consistent messaging across all levels
3. **Training & Support**: Building capability and confidence
4. **Measurement & Feedback**: Tracking progress and adjusting approach

**ADKAR Assessment:**
- **Awareness**: Is everyone clear on the need for change?
- **Desire**: Do stakeholders want to participate and support?
- **Knowledge**: Do people know how to change?
- **Ability**: Can they implement required skills and behaviors?
- **Reinforcement**: Are we sustaining the change long-term?

While my enhanced organizational analysis systems are temporarily unavailable, I'm applying proven change management frameworks."""

            return base_response.strip()

        except Exception as e:
            logger.error("rachel_mcp_handler_error", error=str(e))
            return self._fallback_response("rachel", query, str(e))

    async def _alvaro_mcp_handler(self, query: str, **kwargs) -> str:
        """Alvaro - Technical Excellence with Sequential and Context7 integration"""
        transparency_context = kwargs.get("transparency_context")
        mcp_helper = RealMCPIntegrationHelper(
            transparency_context, self, self.mcp_client
        )

        try:
            # Use Sequential for business analysis + Context7 for technical patterns
            business_results = await mcp_helper.call_mcp_server(
                "sequential", "business_strategy", query=query
            )

            tech_results = await mcp_helper.call_mcp_server(
                "context7", "architecture_patterns", query=query
            )

            base_response = f"""**Technical Excellence Analysis - Alvaro**

Let's get real about the business impact here. What's the ROI story we're telling stakeholders?

**Business-Technical Alignment:**"""

            if business_results or tech_results:
                if business_results and business_results.get("result"):
                    base_response += f"""

**Business Impact Analysis:**
{business_results['result']}"""

                if tech_results and tech_results.get("result"):
                    base_response += f"""

**Technical Architecture Patterns:**
{tech_results['result']}"""

                base_response += """

**Technical Excellence Recommendations:**
- Architecture patterns that support business scalability
- Performance metrics aligned with business outcomes
- Technical debt management with clear ROI justification

This analysis leverages comprehensive business intelligence and proven architectural patterns."""
            else:
                base_response += """

**Technical Excellence Framework:**
1. **Business Value Alignment**: How does technical work drive business outcomes?
2. **Scalability & Performance**: Building for sustainable growth
3. **Architecture Quality**: Maintainable, testable, deployable systems
4. **Team Productivity**: Developer experience and delivery velocity

**Key Technical Considerations:**
- Code quality metrics and technical debt tracking
- Performance benchmarking against business requirements
- Security posture assessment and compliance
- DevOps pipeline optimization for faster delivery

While my enhanced business intelligence and architecture pattern systems are temporarily offline, I'm applying proven technical excellence frameworks."""

            return base_response.strip()

        except Exception as e:
            logger.error("alvaro_mcp_handler_error", error=str(e))
            return self._fallback_response("alvaro", query, str(e))

    async def _martin_mcp_handler(self, query: str, **kwargs) -> str:
        """Martin - Business Development with Context7 and Magic integration"""
        transparency_context = kwargs.get("transparency_context")
        mcp_helper = RealMCPIntegrationHelper(
            transparency_context, self, self.mcp_client
        )

        try:
            # Use Context7 for architectural patterns + Magic for business visualizations
            arch_results = await mcp_helper.call_mcp_server(
                "context7", "architecture_patterns", query=query
            )

            viz_results = None
            if self.mcp_client.is_server_available("magic"):
                viz_results = await mcp_helper.call_mcp_server(
                    "magic",
                    "business_visualization",
                    query=query,
                    visualization_type="business architecture",
                )

            base_response = f"""**Business Development Analysis - Martin**

Let me think about this architecturally. There are some interesting patterns here that remind me of similar challenges I've seen. Let's consider the trade-offs carefully.

**Architectural Business Strategy:**"""

            if arch_results or viz_results:
                if arch_results and arch_results.get("result"):
                    base_response += f"""

**Architecture Pattern Analysis:**
{arch_results['result']}"""

                if viz_results and viz_results.get("result"):
                    base_response += f"""

**Business Architecture Visualization:**
{viz_results['result']}"""

                base_response += """

**Strategic Architecture Recommendations:**
- Evolutionary architecture principles for business adaptability
- Platform thinking for scalable business model innovation
- Technology roadmap alignment with business strategy

This analysis incorporates proven architectural methodologies and business visualization capabilities."""
            else:
                base_response += """

**Business Architecture Framework:**
1. **Platform Strategy**: Building scalable business and technical foundations
2. **Evolutionary Design**: Adapting architecture as business needs evolve
3. **Integration Patterns**: Connecting systems, teams, and business processes
4. **Risk Management**: Technical and business risk assessment and mitigation

**Key Business Considerations:**
- Technology investment ROI and business value realization
- Competitive differentiation through architectural advantages
- Partnership and ecosystem integration opportunities
- Market timing and technical readiness assessment

While my enhanced architectural pattern and business visualization systems are temporarily unavailable, I'm applying proven platform and evolutionary architecture principles."""

            return base_response.strip()

        except Exception as e:
            logger.error("martin_mcp_handler_error", error=str(e))
            return self._fallback_response("martin", query, str(e))

    def _fallback_response(self, persona: str, query: str, error: str) -> str:
        """Generate fallback response when MCP integration fails"""

        persona_styles = {
            "diego": "I'm excited to help you think through this strategic challenge. While my enhanced analysis capabilities are temporarily offline, I can still provide strategic guidance based on proven frameworks.",
            "camille": "Let's approach this innovation challenge systematically. Although my enhanced innovation intelligence is temporarily unavailable, I'll apply organizational strategy principles to help.",
            "rachel": "This is an interesting user experience challenge. While my design system analysis capabilities are offline, I can still provide change management guidance based on proven methodologies.",
            "alvaro": "Let's focus on the business impact here. Even though my enhanced business intelligence systems are temporarily down, I can provide technical analysis based on proven patterns.",
            "martin": "Let me think about this from an architectural perspective. While my pattern analysis systems are temporarily offline, I can apply evolutionary architecture principles to help.",
        }

        return persona_styles.get(
            persona,
            "I understand your question and will provide the best guidance I can with my standard capabilities.",
        )


# Factory function for easy integration
async def create_mcp_integrated_transparency_manager(
    transparency_config: str = "default", mcp_config_path: Optional[str] = None
) -> EnhancedTransparentPersonaManager:
    """
    Create a transparency manager integrated with real ClaudeDirector MCP servers

    Args:
        transparency_config: Transparency configuration type
        mcp_config_path: Path to MCP server configuration

    Returns:
        EnhancedTransparentPersonaManager with real MCP integration
    """
    from .integrated_transparency import create_transparency_system

    # Create transparency system
    transparency_system = create_transparency_system(transparency_config)

    # Initialize MCP client
    mcp_client = MCPUseClient(mcp_config_path)

    # Initialize MCP connections
    connection_status = await mcp_client.initialize_connections()

    logger.info(
        "mcp_integration_initialized",
        available_servers=connection_status.available_servers,
        success_rate=connection_status.success_rate,
    )

    # Create enhanced transparent persona manager
    manager = EnhancedTransparentPersonaManager(transparency_system, mcp_client)

    return manager


# Utility function for connecting to existing ClaudeDirector enhanced persona manager
def integrate_transparency_with_existing_manager(
    existing_manager, transparency_config: str = "default"
) -> TransparentPersonaManager:
    """
    Integrate transparency with an existing ClaudeDirector enhanced persona manager

    Args:
        existing_manager: Existing EnhancedPersonaManager instance
        transparency_config: Transparency configuration type

    Returns:
        TransparentPersonaManager wrapping the existing manager
    """
    from .persona_integration import PersonaIntegrationFactory

    # Wrap existing manager with transparency
    transparent_manager = PersonaIntegrationFactory.wrap_existing_manager(
        existing_manager, transparency_config
    )

    logger.info(
        "transparency_integrated_with_existing_manager",
        manager_type=type(existing_manager).__name__,
        transparency_config=transparency_config,
    )

    return transparent_manager
