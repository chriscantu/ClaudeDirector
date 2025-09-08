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

# PHASE 8.4: Import consolidated response functionality
try:
    from .unified_data_performance_manager import (
        create_persona_response,
        create_fallback_response,
        UnifiedResponse,
        ResponseStatus,
    )
except ImportError:
    # Fallback for testing environments
    def create_persona_response(*args, **kwargs):
        return {"status": "success", "content": kwargs.get("content", "")}

    def create_fallback_response(*args, **kwargs):
        return {"status": "fallback", "content": kwargs.get("content", "")}

    class UnifiedResponse:
        def __init__(self, *args, **kwargs):
            pass

    class ResponseStatus:
        SUCCESS = "success"

    class EnhancedResponse:
        def __init__(self, content="", status="success", **kwargs):
            self.content = content
            self.status = status
            for k, v in kwargs.items():
                setattr(self, k, v)


# PHASE 8.4: BaseManager consolidation imports
from .base_manager import BaseManager, BaseManagerConfig, ManagerType

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
from .visual_template_manager import VisualTemplateManager

try:
    from .lightweight_fallback import (
        create_lightweight_fallback_system,
        FallbackMode,
        FallbackResponse,
    )
except ImportError:
    # Fallback for testing environments
    def create_lightweight_fallback_system():
        return None, None

    class FallbackMode:
        GRACEFUL = "graceful"

    class FallbackResponse:
        def __init__(self, *args, **kwargs):
            pass


# PHASE 8.4: Remove manual logger - will use BaseManager.logger


class EnhancementStatus(Enum):
    """Status of enhancement attempt"""

    SUCCESS = "success"
    FALLBACK = "fallback"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    ERROR = "error"


# TS-4: EnhancedResponse class ELIMINATED - replaced with UnifiedResponse
# This eliminates 30+ lines of duplicate response handling logic
# All EnhancedResponse functionality now handled by create_persona_response() from unified_response_handler


# PHASE 8.4: TransparencyManager ELIMINATED - functionality consolidated into EnhancedPersonaManager
# This eliminates ~35 lines of duplicate class infrastructure


class EnhancedPersonaManager(BaseManager):
    """
    Enhanced persona manager that integrates MCP capabilities with existing personas
    PHASE 12: Always-on MCP enhancement with direct persona → server routing
    PHASE 8.4: Consolidated with BaseManager to eliminate infrastructure duplication
    """

    # PHASE 12: Direct persona → MCP server mapping for always-on enhancement
    PERSONA_SERVER_MAPPING = {
        "diego": "sequential",  # systematic_analysis
        "martin": "context7",  # architecture_patterns
        "rachel": "context7",  # design_methodology
        "camille": "sequential",  # strategic_technology
        "alvaro": "sequential",  # business_strategy
        "sofia": "sequential",  # vendor_strategy
        "elena": "context7",  # compliance_strategy
        "marcus": "context7",  # platform_adoption
        "david": "sequential",  # financial_planning
        "berny": "sequential",  # ai_ml_strategy
        "delbert": "sequential",  # data_strategy
        "security": "context7",  # security_architecture
        "data": "sequential",  # analytics_strategy
    }

    def __init__(self, config: Optional[BaseManagerConfig] = None):
        """
        Initialize enhanced persona manager with BaseManager infrastructure

        Args:
            config: BaseManager configuration
        """
        # PHASE 8.4: BaseManager initialization eliminates duplicate infrastructure
        if config is None:
            config = BaseManagerConfig(
                manager_name="enhanced_persona_manager",
                manager_type=ManagerType.PERFORMANCE,
                enable_metrics=True,
                enable_caching=True,
                enable_logging=True,
                custom_config={"config_path": None},
            )

        super().__init__(config)

        # Initialize persona-specific components
        config_path = self.config.custom_config.get("config_path")
        self.mcp_client = MCPUseClient(config_path)
        self.complexity_analyzer = ComplexityAnalyzer(self.mcp_client.config)

        # PHASE 8.4: Consolidate TransparencyManager functionality into this class
        self.transparency_messages = {
            "accessing_framework": "I'm accessing our strategic analysis framework to provide you with enhanced guidance...",
            "framework_enhanced": "I've enhanced this analysis using our strategic framework methodologies.",
            "framework_unavailable": "The strategic analysis framework is temporarily unavailable, so I'll provide guidance based on my core knowledge.",
            "framework_timeout": "The analysis is taking longer than expected. Let me provide you with immediate guidance while the enhanced framework loads.",
            "framework_error": "External strategic frameworks are temporarily unavailable. I'll help you with standard analysis methods.",
            "performance_note": "This enhanced analysis may take a moment as I access specialized frameworks.",
        }

        # PHASE 12: Visual template manager for Magic MCP integration
        self.visual_template_manager = VisualTemplateManager()
        # PHASE 12: Lightweight fallback pattern for graceful degradation
        self.persona_fallback, self.dependency_checker = (
            create_lightweight_fallback_system()
        )
        self.is_initialized = False

        # PHASE 8.4: MASSIVE CONSOLIDATION - Integrate conversation management
        # This eliminates the need for separate integrated_conversation_manager.py (657 lines)
        self.current_session_id = None
        self.conversation_buffer = []
        self.backup_interval = 300  # 5 minutes
        self.last_backup_time = None
        self.auto_backup_enabled = True

        # Initialize conversation components
        try:
            from context_engineering.strategic_memory_manager import (
                get_strategic_memory_manager,
            )

            self.session_manager = get_strategic_memory_manager()
        except ImportError:
            self.session_manager = None

        try:
            from ..integration.unified_bridge import CLIContextBridge

            db_path = self.config.custom_config.get("db_path")
            if not db_path:
                from pathlib import Path

                base_path = Path(__file__).parent.parent.parent.parent.parent
                db_path = str(base_path / "data" / "strategic_memory.db")
            self.cli_bridge = CLIContextBridge(db_path)
        except ImportError:
            self.cli_bridge = None

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Delegates to persona management operations
        """
        if operation == "get_enhanced_response":
            return await self.get_enhanced_response(*args, **kwargs)
        elif operation == "initialize":
            return await self.initialize()
        elif operation == "get_transparency_message":
            return self._get_transparency_message(*args, **kwargs)
        elif operation == "check_dependencies":
            return self.dependency_checker.check_all()
        # PHASE 8.4: CONSOLIDATED conversation operations (replaces integrated_conversation_manager.py)
        elif operation == "start_session":
            return self.start_conversation_session(*args, **kwargs)
        elif operation == "end_session":
            return self.end_conversation_session(*args, **kwargs)
        elif operation == "capture_turn":
            return self.capture_conversation_turn(*args, **kwargs)
        elif operation == "backup_context":
            return self.backup_conversation_context(*args, **kwargs)
        elif operation == "get_session_status":
            return self.get_session_status(*args, **kwargs)
        elif operation == "export_cli":
            return self.export_for_cli(*args, **kwargs)
        else:
            self.logger.warning(f"Unknown operation: {operation}")
            return None

    def _get_transparency_message(self, message_type: str, **kwargs) -> str:
        """
        PHASE 8.4: Consolidated transparency message functionality
        Replaces separate TransparencyManager class
        """
        if message_type == "access":
            return self.transparency_messages["accessing_framework"]
        elif message_type == "enhanced":
            return self.transparency_messages["framework_enhanced"]
        elif message_type == "fallback":
            reason = kwargs.get("reason", "")
            if "timeout" in reason.lower():
                return self.transparency_messages["framework_timeout"]
            elif "unavailable" in reason.lower():
                return self.transparency_messages["framework_unavailable"]
            else:
                return self.transparency_messages["framework_error"]
        elif message_type == "performance":
            return self.transparency_messages["performance_note"]
        else:
            return "AI enhancement processing..."

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
                self.self.logger.info(
                    "MCP client unavailable - operating in standard mode"
                )
                self.is_initialized = True
                return True

            connection_status = await self.mcp_client.initialize_connections()

            if connection_status.success_rate > 0:
                self.logger.info(
                    f"Enhanced persona manager initialized: {connection_status.available_servers} servers available"
                )
                self.is_initialized = True
                return True
            else:
                self.logger.warning(
                    "No MCP servers available - operating in standard mode"
                )
                self.is_initialized = True
                return True

        except Exception as e:
            self.logger.error(f"Error initializing enhanced persona manager: {e}")
            self.is_initialized = True  # Graceful degradation
            return True

    async def get_enhanced_response(
        self, persona: str, user_input: str, context: Optional[Dict[str, Any]] = None
    ) -> UnifiedResponse:
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

        # PHASE 12: Always-on enhancement with lightweight fallback pattern
        # Implements OVERVIEW.md Lightweight Fallback Pattern
        try:
            # 🔍 Dependency Check (OVERVIEW.md pattern)
            mcp_available = await self.dependency_checker.check_mcp_dependency(
                persona, self.mcp_client
            )

            if mcp_available:
                # 💪 Heavyweight Module - Full MCP Enhancement
                return await self._get_enhanced_response(
                    persona, user_input, complexity_analysis, context, start_time
                )
            else:
                # 🪶 Lightweight Fallback - Essential Features
                fallback_response = (
                    await self.persona_fallback.generate_lightweight_response(
                        persona, user_input, "MCP servers temporarily unavailable"
                    )
                )

                return await create_fallback_response(
                    content=fallback_response.content,
                    reason=fallback_response.fallback_reason,
                    persona=persona,
                    metadata={
                        "enhancement_status": EnhancementStatus.FALLBACK.value,
                        "complexity_score": complexity_analysis.confidence,
                        "original_processing_time": fallback_response.processing_time,
                    },
                )

        except Exception as e:
            # ⚡ Essential Features Always Available
            self.logger.warning(f"Enhancement system failure for {persona}: {e}")
            essential_response = (
                await self.persona_fallback.generate_essential_response(
                    persona, user_input
                )
            )

            return await create_fallback_response(
                content=essential_response.content,
                reason=f"System error: {str(e)}",
                persona=persona,
                status=ResponseStatus.ERROR,
                metadata={
                    "enhancement_status": EnhancementStatus.ERROR.value,
                    "complexity_score": 0.0,
                    "original_processing_time": essential_response.processing_time,
                },
            )

    def _should_enhance(
        self, persona: str, complexity_analysis: ComplexityAnalysis
    ) -> bool:
        """
        PHASE 12: Always-on MCP enhancement - removed complexity thresholds

        Always returns True when MCP client is available for guaranteed 100% enhancement rate.
        No more complexity threshold detection or conditional enhancement logic.

        Args:
            persona: Persona name
            complexity_analysis: ComplexityAnalysis (kept for API compatibility)

        Returns:
            True if MCP client is available (always-on enhancement)
        """
        # Phase 12: Always-on enhancement - only check MCP availability
        return self.mcp_client.is_available

    def get_mcp_server_for_persona(self, persona: str) -> str:
        """
        PHASE 12: Get primary MCP server for persona (always-on routing)

        Args:
            persona: Persona name

        Returns:
            MCP server name for this persona
        """
        return self.PERSONA_SERVER_MAPPING.get(
            persona, "sequential"
        )  # Default to sequential

    def is_visual_request(self, user_input: str) -> bool:
        """
        PHASE 12: Check if user input requests visual enhancement

        Args:
            user_input: User's request

        Returns:
            True if request should route to Magic MCP for visual enhancement
        """
        return self.visual_template_manager.detect_visual_request(user_input)

    def get_visual_enhancement_context(
        self, persona: str, user_input: str
    ) -> Dict[str, Any]:
        """
        PHASE 12: Get Magic MCP visual enhancement context for persona

        Args:
            persona: Persona name
            user_input: User's visual request

        Returns:
            Context dictionary for Magic MCP visual enhancement
        """
        return self.visual_template_manager.get_magic_mcp_enhancement_context(
            persona, user_input
        )

    async def _get_enhanced_response(
        self,
        persona: str,
        user_input: str,
        complexity_analysis: ComplexityAnalysis,
        context: Optional[Dict[str, Any]],
        start_time: float,
    ) -> UnifiedResponse:
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
            transparency_message = self._get_transparency_message("enhanced")

            return await create_persona_response(
                content=enhanced_content,
                persona=persona,
                status=ResponseStatus.SUCCESS,
                mcp_server_used=primary_server,
                transparency_message=transparency_message,
                metadata={
                    "enhancement_status": EnhancementStatus.SUCCESS.value,
                    "complexity_score": complexity_analysis.confidence,
                    "original_processing_time": processing_time,
                },
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
            self.logger.error(f"Error in enhanced response for {persona}: {e}")
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
    ) -> UnifiedResponse:
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

        fallback_message = self._get_transparency_message("fallback", reason=reason)

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

    # PHASE 8.4: MASSIVE CONSOLIDATION - Conversation management methods
    # This eliminates the need for integrated_conversation_manager.py (657 lines ELIMINATED)

    def start_conversation_session(self, session_type: str = "strategic") -> str:
        """Start new conversation session with context tracking"""
        if not self.session_manager:
            self.logger.warning(
                "Session manager not available - operating without session tracking"
            )
            return "no-session-manager"

        self.current_session_id = self.session_manager.start_session(session_type)
        self.conversation_buffer = []
        from datetime import datetime

        self.last_backup_time = datetime.now()

        self.logger.info(
            f"Strategic session started (ID: {self.current_session_id[:8] if self.current_session_id else 'unknown'}...)"
        )
        return self.current_session_id or "fallback-session"

    def capture_conversation_turn(
        self,
        user_input: str,
        assistant_response: str,
        personas_activated: List[str] = None,
        context_metadata: Dict[str, Any] = None,
    ) -> None:
        """Capture conversation turn for context preservation"""
        if not self.current_session_id:
            self.start_conversation_session()

        from datetime import datetime

        turn_data = {
            "timestamp": datetime.now(),
            "user_input": user_input,
            "assistant_response": assistant_response,
            "personas_activated": personas_activated or [],
            "context_metadata": context_metadata or {},
        }

        self.conversation_buffer.append(turn_data)

        # Auto-backup if needed
        if self.auto_backup_enabled and self.last_backup_time:
            time_since_backup = datetime.now() - self.last_backup_time
            if time_since_backup.total_seconds() > self.backup_interval:
                self.backup_conversation_context()

    def backup_conversation_context(self) -> None:
        """Backup current conversation context to strategic memory"""
        if not self.session_manager or not self.current_session_id:
            return

        try:
            self.session_manager.update_session_context(
                self.current_session_id,
                {"conversation_buffer": self.conversation_buffer},
            )
            from datetime import datetime

            self.last_backup_time = datetime.now()
            self.logger.info("Conversation context backed up")
        except Exception as e:
            self.logger.warning(f"Failed to backup conversation context: {e}")

    def end_conversation_session(self) -> None:
        """End current conversation session"""
        if self.current_session_id and self.session_manager:
            try:
                self.backup_conversation_context()
                self.session_manager.end_session(self.current_session_id)
                self.logger.info(f"Session {self.current_session_id[:8]}... ended")
            except Exception as e:
                self.logger.warning(f"Error ending session: {e}")

        self.current_session_id = None
        self.conversation_buffer = []

    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        return {
            "session_id": self.current_session_id,
            "active": bool(self.current_session_id),
            "conversation_turns": len(self.conversation_buffer),
            "last_backup": self.last_backup_time,
            "auto_backup_enabled": self.auto_backup_enabled,
        }

    def export_for_cli(self, filename: Optional[str] = None) -> str:
        """Export conversation for CLI integration"""
        if not self.conversation_buffer:
            return "No conversation data to export"

        from datetime import datetime

        export_content = f"# Strategic Session Export\n\n"
        export_content += f"Session ID: {self.current_session_id}\n"
        export_content += f"Export Time: {datetime.now()}\n\n"

        for i, turn in enumerate(self.conversation_buffer, 1):
            export_content += f"## Turn {i}\n\n"
            export_content += f"**User:** {turn['user_input']}\n\n"
            export_content += f"**Assistant:** {turn['assistant_response']}\n\n"
            if turn["personas_activated"]:
                export_content += (
                    f"**Personas:** {', '.join(turn['personas_activated'])}\n\n"
                )

        if filename and self.cli_bridge:
            try:
                self.cli_bridge.export_content(filename, export_content)
                self.logger.info(f"Conversation exported to {filename}")
            except Exception as e:
                self.logger.warning(f"Failed to export to file: {e}")

        return export_content


# PHASE 8.4: MASSIVE CONSOLIDATION - Factory functions for both managers
def create_enhanced_persona_manager(
    config_path: Optional[str] = None,
) -> EnhancedPersonaManager:
    """Factory function for creating EnhancedPersonaManager with conversation capabilities"""
    config = BaseManagerConfig(
        manager_name="enhanced_persona_manager",
        manager_type=ManagerType.PERFORMANCE,
        enable_metrics=True,
        enable_caching=True,
        enable_logging=True,
        custom_config={"config_path": config_path, "db_path": None},
    )
    return EnhancedPersonaManager(config)


# Legacy compatibility aliases for integrated_conversation_manager.py (ELIMINATED)
def create_integrated_conversation_manager(
    db_path: Optional[str] = None,
) -> EnhancedPersonaManager:
    """Legacy compatibility - now returns EnhancedPersonaManager with conversation capabilities"""
    config = BaseManagerConfig(
        manager_name="integrated_conversation_manager",
        manager_type=ManagerType.PERFORMANCE,
        enable_metrics=True,
        enable_caching=True,
        enable_logging=True,
        custom_config={"config_path": None, "db_path": db_path},
    )
    return EnhancedPersonaManager(config)


# Alias for backward compatibility
IntegratedConversationManager = EnhancedPersonaManager
