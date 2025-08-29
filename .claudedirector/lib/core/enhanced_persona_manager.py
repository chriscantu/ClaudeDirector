"""
Enhanced Persona Manager
Integrates MCP capabilities with existing persona system for enhanced strategic analysis.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Import with fallback for consolidated integration
try:
    from ..integration.unified_bridge import MCPUseClient
except ImportError:
    try:
        from integration.unified_bridge import MCPUseClient
    except ImportError:
        # Fallback minimal class for testing
        class MCPUseClient:
            def __init__(self, *args, **kwargs):
                self.is_available = False
from .complexity_analyzer import (
    AnalysisComplexityDetector as ComplexityAnalyzer,
    ComplexityAnalysis,
)

logger = logging.getLogger(__name__)


class EnhancementStatus(Enum):
    """Status of enhancement attempt"""

    SUCCESS = "success"
    FALLBACK = "fallback"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class EnhancedResponse:
    """Response from enhanced persona system"""

    content: str
    persona: str
    enhancement_status: EnhancementStatus
    processing_time: float
    mcp_server_used: Optional[str] = None
    complexity_score: float = 0.0
    transparency_message: Optional[str] = None
    fallback_reason: Optional[str] = None


class TransparencyManager:
    """Manages transparent communication about external system access"""

    def __init__(self):
        self.messages = {
            "accessing_framework": "I'm accessing our strategic analysis framework to provide you with enhanced guidance...",
            "framework_enhanced": "I've enhanced this analysis using our strategic framework methodologies.",
            "framework_unavailable": "The strategic analysis framework is temporarily unavailable, so I'll provide guidance based on my core knowledge.",
            "framework_timeout": "The analysis is taking longer than expected. Let me provide you with immediate guidance while the enhanced framework loads.",
            "framework_error": "External strategic frameworks are temporarily unavailable. I'll help you with standard analysis methods.",
            "performance_note": "This enhanced analysis may take a moment as I access specialized frameworks.",
        }

    def get_access_message(self, persona: str, server: str) -> str:
        """Get message for accessing external framework"""
        return self.messages["accessing_framework"]

    def get_enhanced_message(
        self, persona: str, server: str, processing_time: float
    ) -> str:
        """Get message indicating enhanced response"""
        return self.messages["framework_enhanced"]

    def get_fallback_message(self, reason: str) -> str:
        """Get message for fallback scenario"""
        if "timeout" in reason.lower():
            return self.messages["framework_timeout"]
        elif "unavailable" in reason.lower():
            return self.messages["framework_unavailable"]
        else:
            return self.messages["framework_error"]

    def get_performance_note(self) -> str:
        """Get performance expectation message"""
        return self.messages["performance_note"]


class EnhancedPersonaManager:
    """
    Enhanced persona manager that integrates MCP capabilities with existing personas
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize enhanced persona manager

        Args:
            config_path: Path to MCP server configuration
        """
        self.mcp_client = MCPUseClient(config_path)
        self.complexity_analyzer = ComplexityAnalyzer(self.mcp_client.config)
        self.transparency_manager = TransparencyManager()
        self.is_initialized = False

        # Persona-specific settings
        self.persona_configs = {
            "diego": {
                "primary_server": "sequential",
                "capabilities": ["systematic_analysis", "organizational_scaling"],
                "enhancement_threshold": 0.7,
                "timeout": 8,
            },
            "martin": {
                "primary_server": "context7",
                "capabilities": ["architecture_patterns", "technical_frameworks"],
                "enhancement_threshold": 0.6,
                "timeout": 8,
            },
            "rachel": {
                "primary_server": "context7",
                "capabilities": [
                    "design_system_methodology",
                    "cross_team_coordination",
                ],
                "enhancement_threshold": 0.6,
                "timeout": 8,
            },
            "alvaro": {
                "primary_server": "sequential",
                "capabilities": ["business_strategy", "competitive_analysis"],
                "enhancement_threshold": 0.7,
                "timeout": 8,
            },
            "camille": {
                "primary_server": "sequential",
                "capabilities": ["technology_leadership", "organizational_scaling"],
                "enhancement_threshold": 0.7,
                "timeout": 8,
            },
        }

    async def initialize(self) -> bool:
        """
        Initialize MCP connections

        Returns:
            True if initialization successful, False if graceful degradation
        """
        try:
            if not self.mcp_client.is_available:
                logger.info("MCP client unavailable - operating in standard mode")
                self.is_initialized = True
                return True

            connection_status = await self.mcp_client.initialize_connections()

            if connection_status.success_rate > 0:
                logger.info(
                    f"Enhanced persona manager initialized: {connection_status.available_servers} servers available"
                )
                self.is_initialized = True
                return True
            else:
                logger.warning("No MCP servers available - operating in standard mode")
                self.is_initialized = True
                return True

        except Exception as e:
            logger.error(f"Error initializing enhanced persona manager: {e}")
            self.is_initialized = True  # Graceful degradation
            return True

    async def get_enhanced_response(
        self, persona: str, user_input: str, context: Optional[Dict[str, Any]] = None
    ) -> EnhancedResponse:
        """
        Get enhanced response for specified persona

        Args:
            persona: Persona name (diego, martin, rachel, alvaro, camille)
            user_input: User's input/question
            context: Optional conversation context

        Returns:
            EnhancedResponse with content and metadata
        """
        start_time = time.time()

        # Ensure initialized
        if not self.is_initialized:
            await self.initialize()

        # Analyze complexity to determine if enhancement is needed
        complexity_analysis = self.complexity_analyzer.analyze_input_complexity(
            user_input, {"current_persona": persona}
        )

        # Check if enhancement should be attempted
        if not self._should_enhance(persona, complexity_analysis):
            # Return standard response
            standard_response = await self._get_standard_response(
                persona, user_input, context
            )
            processing_time = time.time() - start_time

            return EnhancedResponse(
                content=standard_response,
                persona=persona,
                enhancement_status=EnhancementStatus.FALLBACK,
                processing_time=processing_time,
                complexity_score=complexity_analysis.confidence,
                fallback_reason="Complexity below enhancement threshold",
            )

        # Attempt enhanced response
        return await self._get_enhanced_response(
            persona, user_input, complexity_analysis, context, start_time
        )

    def _should_enhance(
        self, persona: str, complexity_analysis: ComplexityAnalysis
    ) -> bool:
        """
        Determine if enhancement should be attempted

        Args:
            persona: Persona name
            complexity_analysis: Complexity analysis result

        Returns:
            True if enhancement should be attempted
        """
        if not self.mcp_client.is_available:
            return False

        persona_config = self.persona_configs.get(persona, {})
        threshold = persona_config.get("enhancement_threshold", 0.6)

        # Check if complexity meets threshold
        if complexity_analysis.confidence < threshold:
            return False

        # Check if recommended enhancement matches persona capabilities
        if complexity_analysis.recommended_enhancement:
            capabilities = persona_config.get("capabilities", [])
            enhancement_type = complexity_analysis.recommended_enhancement

            # Map enhancement types to capabilities
            enhancement_mapping = {
                "systematic_analysis": [
                    "systematic_analysis",
                    "organizational_scaling",
                ],
                "architecture_patterns": [
                    "architecture_patterns",
                    "technical_frameworks",
                ],
                "design_system_methodology": [
                    "design_system_methodology",
                    "cross_team_coordination",
                ],
                "business_strategy": ["business_strategy", "competitive_analysis"],
                "technology_leadership": [
                    "technology_leadership",
                    "organizational_scaling",
                ],
            }

            required_capabilities = enhancement_mapping.get(enhancement_type, [])
            if any(cap in capabilities for cap in required_capabilities):
                return True

        return False

    async def _get_enhanced_response(
        self,
        persona: str,
        user_input: str,
        complexity_analysis: ComplexityAnalysis,
        context: Optional[Dict[str, Any]],
        start_time: float,
    ) -> EnhancedResponse:
        """
        Get enhanced response using MCP integration

        Args:
            persona: Persona name
            user_input: User input
            complexity_analysis: Complexity analysis
            context: Conversation context
            start_time: Start time for processing measurement

        Returns:
            EnhancedResponse with enhanced content
        """
        persona_config = self.persona_configs.get(persona, {})
        primary_server = persona_config.get("primary_server", "sequential")
        timeout = persona_config.get("timeout", 8)

        try:
            # Check if server is available
            if not self.mcp_client.is_server_available(primary_server):
                return await self._handle_fallback(
                    persona,
                    user_input,
                    context,
                    start_time,
                    f"Server {primary_server} not available",
                )

            # Prepare analysis query
            analysis_query = self._prepare_analysis_query(
                persona, user_input, complexity_analysis, context
            )

            # Execute MCP analysis
            mcp_response = await self.mcp_client.execute_analysis(
                primary_server, analysis_query, timeout
            )

            if not mcp_response.success:
                return await self._handle_fallback(
                    persona,
                    user_input,
                    context,
                    start_time,
                    mcp_response.error_message or "MCP analysis failed",
                )

            # Blend MCP response with persona characteristics
            enhanced_content = await self._blend_response(
                persona, user_input, mcp_response.content, context
            )

            processing_time = time.time() - start_time

            # Generate transparency message
            transparency_message = self.transparency_manager.get_enhanced_message(
                persona, primary_server, processing_time
            )

            return EnhancedResponse(
                content=enhanced_content,
                persona=persona,
                enhancement_status=EnhancementStatus.SUCCESS,
                processing_time=processing_time,
                mcp_server_used=primary_server,
                complexity_score=complexity_analysis.confidence,
                transparency_message=transparency_message,
            )

        except asyncio.TimeoutError:
            return await self._handle_fallback(
                persona,
                user_input,
                context,
                start_time,
                f"Timeout after {timeout} seconds",
            )
        except Exception as e:
            logger.error(f"Error in enhanced response for {persona}: {e}")
            return await self._handle_fallback(
                persona, user_input, context, start_time, str(e)
            )

    async def _handle_fallback(
        self,
        persona: str,
        user_input: str,
        context: Optional[Dict[str, Any]],
        start_time: float,
        reason: str,
    ) -> EnhancedResponse:
        """
        Handle fallback to standard response

        Args:
            persona: Persona name
            user_input: User input
            context: Conversation context
            start_time: Start time
            reason: Reason for fallback

        Returns:
            EnhancedResponse with standard content and fallback status
        """
        standard_response = await self._get_standard_response(
            persona, user_input, context
        )
        processing_time = time.time() - start_time

        fallback_message = self.transparency_manager.get_fallback_message(reason)

        return EnhancedResponse(
            content=standard_response,
            persona=persona,
            enhancement_status=EnhancementStatus.FALLBACK,
            processing_time=processing_time,
            complexity_score=0.0,
            transparency_message=fallback_message,
            fallback_reason=reason,
        )

    def _prepare_analysis_query(
        self,
        persona: str,
        user_input: str,
        complexity_analysis: ComplexityAnalysis,
        context: Optional[Dict[str, Any]],
    ) -> str:
        """
        Prepare analysis query for MCP server

        Args:
            persona: Persona name
            user_input: User input
            complexity_analysis: Complexity analysis
            context: Conversation context

        Returns:
            Formatted query for MCP server
        """
        # Persona-specific query preparation with enhanced context
        if persona == "diego":
            query_prefix = "Analyze this organizational strategy challenge using systematic frameworks:"
        elif persona == "martin":
            if (
                "architecture" in user_input.lower()
                or "technical" in user_input.lower()
            ):
                query_prefix = (
                    "Find relevant architectural patterns and technical frameworks for:"
                )
            else:
                query_prefix = "Analyze this technical challenge using proven architectural patterns:"
        elif persona == "rachel":
            if "design" in user_input.lower() or "system" in user_input.lower():
                query_prefix = "Find design system methodologies and cross-team coordination patterns for:"
            else:
                query_prefix = (
                    "Analyze this design challenge using scaling methodologies:"
                )
        elif persona == "alvaro":
            if "business" in user_input.lower() or "strategy" in user_input.lower():
                query_prefix = "Analyze this business strategy challenge using competitive analysis frameworks:"
            elif "financial" in user_input.lower() or "roi" in user_input.lower():
                query_prefix = (
                    "Apply financial modeling and ROI analysis frameworks to:"
                )
            else:
                query_prefix = (
                    "Analyze this business challenge using strategic frameworks:"
                )
        elif persona == "camille":
            if (
                "technology" in user_input.lower()
                and "leadership" in user_input.lower()
            ):
                query_prefix = "Analyze this technology leadership challenge using organizational scaling frameworks:"
            else:
                query_prefix = "Analyze this organizational challenge using executive decision frameworks:"
        else:
            query_prefix = "Analyze this strategic challenge:"

        # Include complexity triggers for context
        triggers_context = ""
        if complexity_analysis.triggers:
            triggers_context = f" [Context: {', '.join(complexity_analysis.triggers)}]"

        # Add persona-specific context hints
        persona_context = ""
        if persona == "martin":
            persona_context = (
                " [Focus: Technical architecture, scalability patterns, system design]"
            )
        elif persona == "rachel":
            persona_context = (
                " [Focus: Design systems, cross-team coordination, UX methodology]"
            )
        elif persona == "alvaro":
            persona_context = (
                " [Focus: Business strategy, competitive analysis, financial modeling]"
            )

        return f"{query_prefix} {user_input}{triggers_context}{persona_context}"

    async def _blend_response(
        self,
        persona: str,
        user_input: str,
        mcp_content: str,
        context: Optional[Dict[str, Any]],
    ) -> str:
        """
        Blend MCP response with persona characteristics

        Args:
            persona: Persona name
            user_input: Original user input
            mcp_content: Content from MCP server
            context: Conversation context

        Returns:
            Blended response maintaining persona authenticity
        """
        # Persona-specific response blending with enhanced MCP context
        persona_styles = {
            "diego": {
                "intro": "Looking at this systematically,",
                "framework_intro": "Based on proven organizational frameworks,",
                "pattern_intro": "Using systematic analysis methodologies,",
                "style": "collaborative and systematic",
            },
            "martin": {
                "intro": "From an architectural perspective,",
                "framework_intro": "Drawing on established technical patterns,",
                "pattern_intro": "Based on proven architectural patterns,",
                "style": "analytical and practical",
            },
            "rachel": {
                "intro": "Considering the design system approach,",
                "framework_intro": "Using collaborative design methodologies,",
                "pattern_intro": "Drawing on design system scaling patterns,",
                "style": "inclusive and facilitative",
            },
            "alvaro": {
                "intro": "From a business strategy standpoint,",
                "framework_intro": "Applying competitive analysis frameworks,",
                "pattern_intro": "Using business strategy methodologies,",
                "style": "strategic and business-focused",
            },
            "camille": {
                "intro": "Taking a technology leadership view,",
                "framework_intro": "Using organizational scaling methodologies,",
                "pattern_intro": "Based on executive decision frameworks,",
                "style": "executive and strategic",
            },
        }

        persona_style = persona_styles.get(persona, persona_styles["diego"])

        # Enhanced response blending based on content type and persona
        if mcp_content and mcp_content.strip():
            # Determine the type of enhancement based on content patterns
            content_lower = mcp_content.lower()

            if any(
                pattern in content_lower
                for pattern in ["pattern", "architecture", "design"]
            ):
                intro = persona_style["pattern_intro"]
            elif any(
                framework in content_lower
                for framework in ["framework", "methodology", "approach"]
            ):
                intro = persona_style["framework_intro"]
            else:
                intro = persona_style["framework_intro"]

            # Clean and format the MCP content
            clean_content = mcp_content.strip()

            # Ensure proper sentence structure
            if not clean_content.endswith("."):
                clean_content += "."

            blended_response = f"{intro} {clean_content}"

            # Add persona-specific contextual closure if needed
            if persona == "martin" and len(clean_content) > 100:
                blended_response += (
                    " This approach provides a solid technical foundation."
                )
            elif persona == "rachel" and len(clean_content) > 100:
                blended_response += (
                    " This ensures we can scale effectively across teams."
                )
            elif persona == "alvaro" and len(clean_content) > 100:
                blended_response += " This positions us strategically in the market."
        else:
            # Fallback if MCP content is empty - persona-specific responses
            if persona == "martin":
                blended_response = f"{persona_style['intro']} let me analyze the technical architecture implications."
            elif persona == "rachel":
                blended_response = f"{persona_style['intro']} let's collaborate on this design challenge."
            elif persona == "alvaro":
                blended_response = f"{persona_style['intro']} let me provide strategic business analysis."
            else:
                blended_response = f"{persona_style['intro']} let me help you work through this challenge."

        return blended_response

    async def _get_standard_response(
        self, persona: str, user_input: str, context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Get standard response without MCP enhancement

        Args:
            persona: Persona name
            user_input: User input
            context: Conversation context

        Returns:
            Standard persona response
        """
        # Enhanced standard responses with persona-specific context awareness
        input_preview = user_input[:50] + "..." if len(user_input) > 50 else user_input

        if persona == "diego":
            if any(
                keyword in user_input.lower()
                for keyword in ["team", "organization", "scaling", "structure"]
            ):
                return f"I'll help you approach this organizational challenge systematically. For '{input_preview}', let's break this down into coordinated steps that consider team dynamics and scaling principles."
            else:
                return f"I'll help you approach this systematically. For '{input_preview}', let's break this down into coordinated steps."

        elif persona == "martin":
            if any(
                keyword in user_input.lower()
                for keyword in ["architecture", "technical", "system", "design"]
            ):
                return f"Let me analyze the technical architecture aspects. For '{input_preview}', I'll examine the patterns and scalability considerations."
            else:
                return f"Let me analyze this technically. For '{input_preview}', here's my architectural perspective."

        elif persona == "rachel":
            if any(
                keyword in user_input.lower()
                for keyword in ["design", "system", "user", "experience", "team"]
            ):
                return f"Let's collaborate on this design system challenge. For '{input_preview}', I'll facilitate an approach that considers cross-team coordination and user experience."
            else:
                return f"Let's collaborate on this design challenge. For '{input_preview}', I'll facilitate our approach."

        elif persona == "alvaro":
            if any(
                keyword in user_input.lower()
                for keyword in ["business", "strategy", "market", "competitive"]
            ):
                return f"From a business strategy perspective, '{input_preview}' requires strategic analysis of market positioning and competitive advantages."
            elif any(
                keyword in user_input.lower()
                for keyword in ["roi", "financial", "cost", "investment"]
            ):
                return f"Looking at the financial implications, '{input_preview}' needs ROI analysis and investment strategy consideration."
            else:
                return f"From a business strategy perspective, '{input_preview}' requires strategic analysis."

        elif persona == "camille":
            if any(
                keyword in user_input.lower()
                for keyword in ["technology", "leadership", "organizational"]
            ):
                return f"Taking a technology leadership view of '{input_preview}', let's consider the organizational scaling and executive decision implications."
            else:
                return f"Taking a technology leadership view of '{input_preview}', let's consider the organizational implications."

        else:
            return f"Let me help you with '{input_preview}'"

    async def cleanup(self) -> None:
        """Cleanup MCP connections"""
        if self.mcp_client:
            await self.mcp_client.cleanup_connections()

    def get_server_status(self) -> Dict[str, Any]:
        """Get current server status for monitoring"""
        if not self.mcp_client.is_available:
            return {"status": "unavailable", "reason": "mcp-use library not available"}

        available_servers = self.mcp_client.get_available_servers()

        return {
            "status": "available" if available_servers else "no_servers",
            "available_servers": available_servers,
            "total_personas": len(self.persona_configs),
            "enhanced_personas": [
                p
                for p in self.persona_configs.keys()
                if self.persona_configs[p]["primary_server"] in available_servers
            ],
        }
