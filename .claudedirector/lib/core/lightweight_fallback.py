"""
Lightweight Fallback Pattern Implementation - Phase 12
OVERVIEW.md Architectural Innovation for graceful MCP server degradation
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FallbackMode(Enum):
    """Fallback operation modes"""

    FULL_HEAVYWEIGHT = "full"  # All MCP servers available
    LIGHTWEIGHT = "lightweight"  # Essential persona functionality only
    ESSENTIAL = "essential"  # Core system functionality only


@dataclass
class FallbackResponse:
    """Response from fallback system"""

    content: str
    mode: FallbackMode
    persona: str
    processing_time: float
    transparency_message: str
    fallback_reason: Optional[str] = None


class LightweightPersonaFallback:
    """
    PHASE 12: Lightweight fallback for persona functionality when MCP unavailable

    Implements OVERVIEW.md Lightweight Fallback Pattern:
    - Smart dependency detection before MCP instantiation
    - API compatibility maintained in lightweight mode
    - Essential persona functionality always available
    """

    def __init__(self):
        self.persona_essentials = self._initialize_persona_essentials()
        self.fallback_templates = self._initialize_fallback_templates()

    def _initialize_persona_essentials(self) -> Dict[str, Dict[str, Any]]:
        """Initialize essential persona characteristics for lightweight mode"""
        return {
            "diego": {
                "domain": "Engineering Leadership",
                "icon": "🎯",
                "essential_capabilities": [
                    "team_structure_guidance",
                    "organizational_coordination",
                    "strategic_planning_basics",
                ],
                "lightweight_personality": "Great to connect! Let me provide foundational strategic guidance...",
                "key_frameworks": [
                    "Team Topologies",
                    "Organizational Design",
                    "Strategic Planning",
                ],
            },
            "martin": {
                "domain": "Platform Architecture",
                "icon": "🏗️",
                "essential_capabilities": [
                    "architecture_principles",
                    "platform_design_basics",
                    "technical_decision_guidance",
                ],
                "lightweight_personality": "Let me help with architectural thinking using proven patterns...",
                "key_frameworks": [
                    "SOLID Principles",
                    "Evolutionary Architecture",
                    "Platform Strategy",
                ],
            },
            "rachel": {
                "domain": "Design Systems Strategy",
                "icon": "🎨",
                "essential_capabilities": [
                    "design_system_principles",
                    "user_experience_guidance",
                    "cross_team_design_coordination",
                ],
                "lightweight_personality": "I'll help with design system strategy using proven UX principles...",
                "key_frameworks": [
                    "Design System Maturity",
                    "User-Centered Design",
                    "Design Thinking",
                ],
            },
            "camille": {
                "domain": "Strategic Technology",
                "icon": "📊",
                "essential_capabilities": [
                    "technology_strategy",
                    "competitive_analysis_basics",
                    "executive_communication",
                ],
                "lightweight_personality": "Let me provide strategic technology guidance for your situation...",
                "key_frameworks": [
                    "Technology Strategy",
                    "Competitive Analysis",
                    "Strategic Planning",
                ],
            },
            "alvaro": {
                "domain": "Platform Investment Strategy",
                "icon": "💼",
                "essential_capabilities": [
                    "business_value_analysis",
                    "roi_calculation_basics",
                    "investment_prioritization",
                ],
                "lightweight_personality": "I'll help analyze the business value and investment considerations...",
                "key_frameworks": [
                    "Business Value Analysis",
                    "ROI Calculation",
                    "Investment Strategy",
                ],
            },
        }

    def _initialize_fallback_templates(self) -> Dict[str, str]:
        """Initialize fallback response templates"""
        return {
            "lightweight_mcp_disclosure": "⚡ **Lightweight Mode**: MCP servers temporarily unavailable - providing essential {persona} guidance",
            "essential_disclosure": "🔧 **Essential Mode**: Core strategic guidance available - enhanced features temporarily offline",
            "fallback_attribution": "📚 **Framework Reference**: Guidance based on {frameworks} principles",
        }

    async def generate_lightweight_response(
        self, persona: str, user_input: str, fallback_reason: str = "MCP unavailable"
    ) -> FallbackResponse:
        """
        Generate lightweight persona response without MCP enhancement

        Implements OVERVIEW.md pattern: Essential Features Always Available
        """
        start_time = time.time()

        persona_config = self.persona_essentials.get(
            persona, self.persona_essentials["martin"]
        )

        # Generate essential persona response
        response_content = self._generate_essential_guidance(persona_config, user_input)

        # Add persona header
        header = f"{persona_config['icon']} **{persona.title()} | {persona_config['domain']}** (Lightweight Mode)"

        # Add transparency disclosure
        transparency = self.fallback_templates["lightweight_mcp_disclosure"].format(
            persona=persona_config["domain"]
        )

        # Add framework attribution
        frameworks = ", ".join(
            persona_config["key_frameworks"][:2]
        )  # Show 2 key frameworks
        attribution = self.fallback_templates["fallback_attribution"].format(
            frameworks=frameworks
        )

        # Combine response
        full_response = (
            f"{header}\n\n{transparency}\n\n{response_content}\n\n{attribution}"
        )

        processing_time = time.time() - start_time

        return FallbackResponse(
            content=full_response,
            mode=FallbackMode.LIGHTWEIGHT,
            persona=persona,
            processing_time=processing_time,
            transparency_message=transparency,
            fallback_reason=fallback_reason,
        )

    def _generate_essential_guidance(
        self, persona_config: Dict[str, Any], user_input: str
    ) -> str:
        """Generate essential strategic guidance using persona's core capabilities"""

        # Start with persona's lightweight personality
        response_parts = [persona_config["lightweight_personality"]]

        # Add domain-specific guidance based on capabilities
        capabilities = persona_config["essential_capabilities"]

        if "strategic_planning" in " ".join(capabilities):
            response_parts.append(
                "\n**Strategic Approach:**\n"
                "1. **Clarify Objectives**: Define specific outcomes you want to achieve\n"
                "2. **Assess Current State**: Understand existing constraints and resources\n"
                "3. **Identify Key Actions**: Determine 2-3 critical next steps\n"
                "4. **Plan Implementation**: Create actionable timeline with accountability"
            )

        if "architecture" in " ".join(capabilities):
            response_parts.append(
                "\n**Architectural Thinking:**\n"
                "- **Start with Principles**: Apply SOLID principles and proven patterns\n"
                "- **Consider Evolution**: Design for change and incremental improvement\n"
                "- **Focus on Value**: Prioritize components that deliver immediate business value\n"
                "- **Document Decisions**: Capture rationale for future context"
            )

        if "design" in " ".join(capabilities):
            response_parts.append(
                "\n**Design System Strategy:**\n"
                "- **User-Centered Approach**: Start with user needs and workflows\n"
                "- **Component Thinking**: Build reusable, consistent design patterns\n"
                "- **Cross-Team Alignment**: Ensure design standards support all teams\n"
                "- **Iterative Improvement**: Continuously refine based on usage feedback"
            )

        if "business" in " ".join(capabilities):
            response_parts.append(
                "\n**Business Value Analysis:**\n"
                "- **Quantify Impact**: Measure outcomes in business metrics\n"
                "- **Consider Alternatives**: Evaluate multiple approaches\n"
                "- **Risk Assessment**: Identify and mitigate key risks\n"
                "- **Timeline Considerations**: Balance speed vs. quality trade-offs"
            )

        # Add general next steps
        response_parts.append(
            "\n**Immediate Next Steps:**\n"
            "1. **Validate Understanding**: Ensure we're aligned on the core challenge\n"
            "2. **Prioritize Actions**: Focus on highest-impact activities first\n"
            "3. **Gather Stakeholders**: Identify key people who need to be involved\n"
            "4. **Define Success**: Establish clear criteria for measuring progress\n\n"
            "*For enhanced strategic analysis with frameworks and detailed recommendations, "
            "MCP enhancement will be available once servers are restored.*"
        )

        return "\n".join(response_parts)

    async def generate_essential_response(
        self, persona: str, user_input: str
    ) -> FallbackResponse:
        """
        Generate essential system response when all enhancement unavailable

        Implements OVERVIEW.md pattern: Core functionality preserved
        """
        start_time = time.time()

        # Essential system response - minimal but functional
        essential_content = (
            f"**ClaudeDirector Strategic Guidance**\n\n"
            f"I'm experiencing temporary connectivity issues with enhanced AI capabilities, "
            f"but I can still provide essential strategic guidance.\n\n"
            f"**For your strategic question:**\n\n"
            f"1. **Immediate Actions**: Focus on the most critical 1-2 steps you can take today\n"
            f"2. **Stakeholder Engagement**: Identify who needs to be involved in decisions\n"
            f"3. **Risk Mitigation**: Consider potential obstacles and prepare contingencies\n"
            f"4. **Success Metrics**: Define how you'll measure progress and outcomes\n\n"
            f"**Next Steps:**\n"
            f"- Break down your challenge into specific, actionable components\n"
            f"- Prioritize actions based on impact and urgency\n"
            f"- Engage relevant stakeholders for input and alignment\n"
            f"- Plan regular checkpoints to assess progress\n\n"
            f"*Enhanced strategic analysis with personas, frameworks, and detailed "
            f"recommendations will be available once connectivity is restored.*"
        )

        transparency = self.fallback_templates["essential_disclosure"]
        full_response = f"{transparency}\n\n{essential_content}"

        processing_time = time.time() - start_time

        return FallbackResponse(
            content=full_response,
            mode=FallbackMode.ESSENTIAL,
            persona="system",
            processing_time=processing_time,
            transparency_message=transparency,
            fallback_reason="All enhancement systems unavailable",
        )


class MCPDependencyChecker:
    """
    Smart dependency detection for MCP server availability

    Implements OVERVIEW.md pattern: Intelligent dependency checking before instantiation
    """

    def __init__(self):
        self.health_cache = {}
        self.cache_ttl = 30  # 30 second cache for health checks
        self.timeout = 5  # 5 second timeout for health checks

    async def check_mcp_dependency(self, persona: str, mcp_client=None) -> bool:
        """
        Smart detection: OVERVIEW.md lightweight fallback pattern

        Returns True if MCP enhancement is available, False for fallback
        """
        try:
            # Check if MCP client exists and is configured
            if not mcp_client:
                logger.debug(f"MCP client unavailable for {persona}")
                return False

            # Check basic availability
            if not hasattr(mcp_client, "is_available") or not mcp_client.is_available:
                logger.debug(f"MCP client not available for {persona}")
                return False

            # Quick health check with caching
            cache_key = f"{persona}_health"
            current_time = time.time()

            if cache_key in self.health_cache:
                cached_time, cached_result = self.health_cache[cache_key]
                if current_time - cached_time < self.cache_ttl:
                    return cached_result

            # Perform health check with timeout
            health_result = await self._quick_health_check(persona, mcp_client)

            # Cache result
            self.health_cache[cache_key] = (current_time, health_result)

            return health_result

        except Exception as e:
            logger.warning(f"MCP dependency check failed for {persona}: {e}")
            return False

    async def _quick_health_check(self, persona: str, mcp_client) -> bool:
        """Perform quick health check on MCP client"""
        try:
            # Use asyncio.wait_for to enforce timeout
            health_task = asyncio.create_task(self._ping_mcp_client(mcp_client))
            result = await asyncio.wait_for(health_task, timeout=self.timeout)
            return result
        except asyncio.TimeoutError:
            logger.warning(f"MCP health check timeout for {persona}")
            return False
        except Exception as e:
            logger.warning(f"MCP health check error for {persona}: {e}")
            return False

    async def _ping_mcp_client(self, mcp_client) -> bool:
        """Minimal ping to test MCP client responsiveness"""
        try:
            # Try to access basic MCP client functionality
            if hasattr(mcp_client, "ping"):
                return await mcp_client.ping()
            elif hasattr(mcp_client, "health_check"):
                result = await mcp_client.health_check()
                return result.get("status") == "healthy"
            else:
                # Fallback: check if basic attributes exist
                return hasattr(mcp_client, "is_available") and mcp_client.is_available
        except Exception:
            return False

    def clear_health_cache(self):
        """Clear health check cache to force fresh checks"""
        self.health_cache.clear()


# Factory function for lightweight fallback pattern integration
def create_lightweight_fallback_system() -> (
    tuple[LightweightPersonaFallback, MCPDependencyChecker]
):
    """
    Factory function implementing OVERVIEW.md Lightweight Fallback Pattern

    Returns:
        Tuple of (persona_fallback, dependency_checker) for integration
    """
    persona_fallback = LightweightPersonaFallback()
    dependency_checker = MCPDependencyChecker()

    logger.info("Lightweight fallback system initialized - OVERVIEW.md pattern active")

    return persona_fallback, dependency_checker

