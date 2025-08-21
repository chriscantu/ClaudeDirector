"""
Enhanced Persona Manager with Embedded Framework Integration
Integrates embedded framework capabilities with the existing persona activation system.

This manager coordinates between:
- Dynamic Persona Activation Engine (existing)
- Embedded Framework Engine (new)
- Persona Enhancement Engine (new)

Author: Martin (Principal Platform Architect)
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import structlog

from .persona_activation_engine import (
    ContextAnalysisEngine,
    PersonaSelectionEngine,
    ConversationStateEngine,
    ContextResult,
    PersonaSelection
)
from .complexity_analyzer import AnalysisComplexityDetector
from .persona_enhancement_engine import PersonaEnhancementEngine, EnhancementResult
from .template_engine import TemplateDiscoveryEngine

# Configure logging
logger = structlog.get_logger(__name__)


class EnhancedPersonaManager:
    """
    Enhanced Persona Manager with Embedded Framework Integration

    Coordinates the complete persona activation and enhancement workflow:
    1. Context Analysis (existing)
    2. Persona Selection (existing)
    3. Embedded Framework Enhancement (new)
    4. Response Integration (new)
    5. State Management (existing)
    """

    def __init__(
        self,
        template_discovery: TemplateDiscoveryEngine,
        enhancement_config: Optional[Dict] = None
    ):
        """
        Initialize enhanced persona manager

        Args:
            template_discovery: Template discovery engine
            enhancement_config: Enhancement configuration overrides
        """
        self.template_discovery = template_discovery

        # Initialize existing persona system
        self.context_engine = ContextAnalysisEngine(template_discovery)
        self.persona_engine = PersonaSelectionEngine(template_discovery)
        self.state_engine = ConversationStateEngine()

        # Initialize embedded framework enhancement system
        self.complexity_detector = AnalysisComplexityDetector(enhancement_config or {})
        self.enhancement_engine = PersonaEnhancementEngine(
            self.complexity_detector,
            enhancement_config or {}
        )

        # Configuration
        self.enhancement_config = enhancement_config or {}
        self.enhancement_enabled = True  # Always enabled with embedded frameworks
        self.fallback_to_standard = True

        # Performance tracking
        self.enhancement_stats = {
            "total_requests": 0,
            "enhanced_requests": 0,
            "fallback_requests": 0,
            "average_enhancement_time": 0.0
        }

        logger.info(
            "embedded_framework_system_initialized",
            enabled=True,
            enhancement_config=bool(enhancement_config)
        )

    def process_user_input(
        self,
        user_input: str,
        conversation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user input through complete enhanced persona workflow

        Args:
            user_input: User's message or query
            conversation_context: Optional conversation history/context

        Returns:
            Complete response with persona activation and enhancement info
        """
        start_time = time.time()

        try:
            # Step 1: Analyze context (existing system)
            context_result = self.context_engine.analyze_context(user_input)

            # Step 2: Select persona (existing system)
            persona_selection = self.persona_engine.select_persona(context_result)

            # Step 3: Update conversation state (existing system)
            self.state_engine.update_state(persona_selection, context_result, user_input)

            # Step 4: Generate base persona response (simulated for now)
            base_response = self._generate_base_persona_response(
                persona_selection, user_input, conversation_context
            )

            # Step 5: Apply embedded framework enhancement if enabled
            enhancement_result = self._apply_embedded_enhancement(
                persona_selection.primary,
                user_input,
                base_response,
                conversation_context
            )

            # Step 6: Track statistics
            self._update_statistics(enhancement_result, start_time)

            # Step 7: Prepare final response
            final_response = self._prepare_final_response(
                context_result,
                persona_selection,
                base_response,
                enhancement_result,
                start_time
            )

            logger.info(
                "persona_workflow_completed",
                persona=persona_selection.primary,
                enhanced=enhancement_result.enhancement_applied,
                total_time_ms=int((time.time() - start_time) * 1000)
            )

            return final_response

        except Exception as e:
            logger.error(
                "persona_workflow_failed",
                error=str(e),
                user_input=user_input[:100]  # Truncate for logging
            )

            # Return fallback response
            return self._create_fallback_response(user_input, str(e))

    def _generate_base_persona_response(
        self,
        persona_selection: PersonaSelection,
        user_input: str,
        conversation_context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate base persona response (simulated for integration)

        In a real implementation, this would call the actual persona
        response generation system (e.g., Claude with persona context).
        """

        # Simulate different persona response styles
        persona_responses = {
            "diego": f"Great question! Let me work through this from a strategic platform perspective. {self._get_diego_response_style()}",
            "martin": f"Let me think about this architecturally. {self._get_martin_response_style()}",
            "rachel": f"From a user experience standpoint, {self._get_rachel_response_style()}",
            "alvaro": f"Looking at this from a product strategy perspective, {self._get_alvaro_response_style()}",
            "camille": f"As we think about organizational strategy, {self._get_camille_response_style()}"
        }

        base_template = persona_responses.get(
            persona_selection.primary,
            "Let me help you think through this challenge..."
        )

        # Add context-specific elements
        if "mobile" in user_input.lower() or "ios" in user_input.lower():
            base_template += " Given the mobile platform context, we need to consider native performance, app store considerations, and cross-platform strategy."
        elif "product" in user_input.lower() or "feature" in user_input.lower():
            base_template += " From a product perspective, we should focus on user value, business impact, and strategic alignment."
        elif "architecture" in user_input.lower() or "technical" in user_input.lower():
            base_template += " From an architectural standpoint, we need to consider scalability, maintainability, and evolutionary design principles."

        return base_template

    def _get_diego_response_style(self) -> str:
        """Get Diego's characteristic response style"""
        return "I'm excited to explore this challenge with you. Let's break this down systematically while keeping the human element front and center."

    def _get_martin_response_style(self) -> str:
        """Get Martin's characteristic response style"""
        return "There are some interesting patterns here that remind me of similar challenges I've seen. Let's consider the trade-offs carefully."

    def _get_rachel_response_style(self) -> str:
        """Get Rachel's characteristic response style"""
        return "I love how this impacts the user experience. Let's think about this holistically - both for end users and the teams building it."

    def _get_alvaro_response_style(self) -> str:
        """Get Alvaro's characteristic response style"""
        return "let's get real about the business impact here. What's the ROI story we're telling stakeholders?"

    def _get_camille_response_style(self) -> str:
        """Get Camille's characteristic response style"""
        return "let's be honest about what we're dealing with here. The people problem is usually harder than the technical problem."

    def _apply_embedded_enhancement(
        self,
        persona_name: str,
        user_input: str,
        base_response: str,
        conversation_context: Optional[Dict[str, Any]]
    ) -> EnhancementResult:
        """Apply embedded framework enhancement if appropriate"""

        if not self.enhancement_enabled or not self.enhancement_engine:
            return EnhancementResult(
                enhanced_response=base_response,
                enhancement_applied=False,
                framework_used=None,
                analysis_data=None,
                processing_time_ms=0,
                fallback_reason="Enhancement system not available"
            )

        try:
            # Apply embedded framework enhancement
            enhancement_result = self.enhancement_engine.enhance_response(
                persona_name,
                user_input,
                base_response,
                conversation_context
            )

            return enhancement_result

        except Exception as e:
            logger.error(
                "embedded_framework_enhancement_error",
                persona=persona_name,
                error=str(e)
            )

            # Return fallback with base response
            return EnhancementResult(
                enhanced_response=base_response,
                enhancement_applied=False,
                framework_used=None,
                analysis_data=None,
                processing_time_ms=0,
                fallback_reason=f"Enhancement error: {str(e)}"
            )

    def _update_statistics(self, enhancement_result: EnhancementResult, start_time: float) -> None:
        """Update performance and usage statistics"""

        self.enhancement_stats["total_requests"] += 1

        if enhancement_result.enhancement_applied:
            self.enhancement_stats["enhanced_requests"] += 1
        else:
            self.enhancement_stats["fallback_requests"] += 1

        # Update average enhancement time
        total_time = (time.time() - start_time) * 1000
        current_avg = self.enhancement_stats["average_enhancement_time"]
        total_requests = self.enhancement_stats["total_requests"]

        self.enhancement_stats["average_enhancement_time"] = (
            (current_avg * (total_requests - 1) + total_time) / total_requests
        )

    def _prepare_final_response(
        self,
        context_result: ContextResult,
        persona_selection: PersonaSelection,
        base_response: str,
        enhancement_result: EnhancementResult,
        start_time: float
    ) -> Dict[str, Any]:
        """Prepare the final response with all metadata"""

        total_processing_time = int((time.time() - start_time) * 1000)

        return {
            # Core response
            "response": enhancement_result.enhanced_response,
            "persona": persona_selection.primary,
            "template_id": persona_selection.template_id,

            # Context analysis
            "context": context_result.to_dict(),

            # Persona selection
            "persona_selection": persona_selection.to_dict(),

            # Enhancement information
            "enhancement": {
                "applied": enhancement_result.enhancement_applied,
                "framework_used": enhancement_result.framework_used,
                "analysis_data": enhancement_result.analysis_data,
                "processing_time_ms": enhancement_result.processing_time_ms,
                "fallback_reason": enhancement_result.fallback_reason
            },

            # Performance metrics
            "performance": {
                "total_processing_time_ms": total_processing_time,
                "context_analysis_time_ms": context_result.analysis_time_ms,
                "persona_selection_time_ms": persona_selection.selection_time_ms,
                "enhancement_time_ms": enhancement_result.processing_time_ms
            },

            # System state
            "conversation_state": self.state_engine.get_current_state(),

            # System capabilities
            "capabilities": {
                "enhancement_enabled": self.enhancement_enabled,
                "enhanced_personas": ["diego", "martin", "rachel", "camille", "alvaro"] if self.enhancement_enabled else [],
                "available_templates": [t.template_id for t in self.template_discovery.list_templates()]
            }
        }

    def _create_fallback_response(self, user_input: str, error_message: str) -> Dict[str, Any]:
        """Create fallback response when main workflow fails"""

        return {
            "response": "I understand you're looking for strategic guidance. Let me help you think through this challenge. While I'm experiencing some technical difficulties with my enhanced analysis capabilities, I can still provide thoughtful strategic advice.",
            "persona": "camille",  # Global fallback
            "template_id": "fallback",
            "context": {"confidence": 0.0, "fallback": True},
            "persona_selection": {"method": "emergency_fallback"},
            "enhancement": {"applied": False, "fallback_reason": f"System error: {error_message}"},
            "performance": {"total_processing_time_ms": 0},
            "conversation_state": self.state_engine.get_current_state(),
            "capabilities": {"enhancement_enabled": False, "error": error_message}
        }

    # Public interface methods

    def get_current_state(self) -> Dict[str, Any]:
        """Get current conversation state"""
        return self.state_engine.get_current_state()

    def get_activation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent persona activation history"""
        return self.state_engine.get_activation_history(limit)

    def get_enhancement_statistics(self) -> Dict[str, Any]:
        """Get MCP enhancement usage statistics"""
        return {
            **self.enhancement_stats,
            "enhancement_rate": (
                self.enhancement_stats["enhanced_requests"] /
                max(self.enhancement_stats["total_requests"], 1)
            ),
            "enhancement_enabled": self.enhancement_enabled
        }

    async def get_mcp_server_status(self) -> Dict[str, Any]:
        """Get status of MCP servers"""
        if not self.mcp_client:
            return {"available": False, "reason": "MCP client not initialized"}

        try:
            return await self.mcp_client.get_connection_status()
        except Exception as e:
            return {"available": False, "error": str(e)}

    def reset_conversation(self) -> None:
        """Reset conversation state for new session"""
        self.state_engine.reset_session()

        # Reset enhancement statistics
        self.enhancement_stats = {
            "total_requests": 0,
            "enhanced_requests": 0,
            "fallback_requests": 0,
            "average_enhancement_time": 0.0
        }

        logger.info("conversation_reset", enhancement_enabled=self.enhancement_enabled)

    async def close(self) -> None:
        """Clean up resources"""
        if self.mcp_client:
            await self.mcp_client.close()

        logger.info("enhanced_persona_manager_closed")


# Utility functions for easy integration

async def create_enhanced_persona_manager(
    template_config_path: str,
    mcp_config_path: Optional[str] = None,
    enhancement_config: Optional[Dict] = None
) -> EnhancedPersonaManager:
    """
    Create enhanced persona manager with all components

    Args:
        template_config_path: Path to director templates configuration
        mcp_config_path: Optional path to MCP server configuration
        enhancement_config: Optional enhancement configuration overrides

    Returns:
        Fully initialized EnhancedPersonaManager
    """

    # Create template discovery engine
    template_discovery = TemplateDiscoveryEngine(template_config_path)

    # Create enhanced persona manager
    manager = EnhancedPersonaManager(
        template_discovery,
        mcp_config_path,
        enhancement_config
    )

    # Wait for MCP initialization if config provided
    if mcp_config_path:
        # Give MCP system time to initialize
        await asyncio.sleep(0.1)

    return manager


def create_demo_enhanced_manager(enable_mcp: bool = True) -> EnhancedPersonaManager:
    """
    Create enhanced persona manager for demos/testing

    Args:
        enable_mcp: Whether to enable MCP enhancement (mock for demos)

    Returns:
        EnhancedPersonaManager configured for demonstration
    """

    # Create mock template discovery for demo
    from .template_engine import TemplateDiscoveryEngine
    template_discovery = TemplateDiscoveryEngine(".claudedirector/config/director_templates.yaml")

    # Create manager without MCP for now (would need mock servers for full demo)
    manager = EnhancedPersonaManager(template_discovery)

    if enable_mcp:
        # In a real demo, this would initialize with mock MCP servers
        logger.info("demo_manager_created", mcp_mock_enabled=enable_mcp)

    return manager
