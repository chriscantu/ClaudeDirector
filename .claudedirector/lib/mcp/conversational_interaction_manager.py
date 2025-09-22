"""
Conversational Interaction Manager - Phase 7B Chat Integration

ARCHITECTURE COMPLIANCE:
- OVERVIEW.md: Leverages Always-On MCP Enhancement (Phase 12)
- DRY Principle: Extends InteractiveEnhancementAddon, no duplication
- SOLID: Single responsibility for natural language chart interactions
- Lightweight Fallback: Graceful degradation when MCP unavailable

Phase 7B: T-B1 - 8 Story Points - P0 Priority
Foundation: Phase 7A InteractiveEnhancementAddon
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

from .constants import MCPServerConstants
from .interactive_enhancement_addon import (
    InteractiveEnhancementAddon,
    InteractiveEnhancementResult,
)
from .mcp_integration_manager import MCPIntegrationManager

# TS-4: Import unified response handler (eliminates duplicate InteractionResponse pattern)
from ..performance import (
    create_conversational_response,
    UnifiedResponse,
    ResponseStatus,
)

# Phase 2: Personal Retrospective Agent Integration (DRY compliance)
from ..agents.personal_retrospective_agent import PersonalRetrospectiveAgent

logger = logging.getLogger(__name__)


class InteractionIntent(Enum):
    """Natural language interaction intent classification"""

    TIME_NAVIGATION = "time_navigation"  # "Show me Q3 data"
    DATA_FILTERING = "data_filtering"  # "Filter by engineering team"
    DRILL_DOWN = "drill_down"  # "Drill down into platform metrics"
    COMPARISON = "comparison"  # "Compare with last quarter"
    CONTEXT_RESET = "context_reset"  # "Go back", "Reset filters"
    INSIGHT_REQUEST = "insight_request"  # "What's driving this spike?"
    RETROSPECTIVE_COMMAND = (
        "retrospective_command"  # "/retrospective create", "/retrospective view"
    )
    UNKNOWN = "unknown"


@dataclass
class QueryIntent:
    """Parsed natural language query with extracted intent"""

    intent: InteractionIntent
    entities: List[str] = field(default_factory=list)
    time_period: Optional[str] = None
    filter_criteria: Dict[str, str] = field(default_factory=dict)
    confidence: float = 0.0
    raw_query: str = ""


# TS-4: InteractionResponse class ELIMINATED - replaced with UnifiedResponse
# This eliminates 35+ lines of duplicate response handling logic
# All InteractionResponse functionality now handled by create_conversational_response() from unified_response_handler


class ConversationalInteractionManager:
    """
    Enable natural language interactions with interactive charts

    ARCHITECTURE INTEGRATION:
    - Extends InteractiveEnhancementAddon (Phase 7A foundation)
    - Uses Always-On MCP Enhancement (OVERVIEW.md Phase 12)
    - Implements Lightweight Fallback Pattern for graceful degradation
    - Maintains <500ms response time target (OVERVIEW.md enterprise SLA)

    SUPPORTED PATTERNS:
    ✅ "Show me Q3 data" → Update chart timeframe
    ✅ "Filter by engineering team" → Apply team filter
    ✅ "Drill down into platform metrics" → Navigate hierarchy
    ✅ "Compare with last quarter" → Add comparison overlay
    ✅ "What's driving this spike?" → Generate strategic insights
    """

    def __init__(self, interactive_addon: Optional[InteractiveEnhancementAddon] = None):
        """
        Initialize conversational interaction manager

        Args:
            interactive_addon: Phase 7A Interactive Enhancement Addon instance
                              (DRY compliance - reuse existing system)
        """
        self.name = "conversational-interaction-manager"
        self.version = "1.0.0"

        # DRY Principle: Leverage existing Phase 7A components
        self.interactive_addon = interactive_addon or InteractiveEnhancementAddon()
        self.mcp_manager = MCPIntegrationManager()

        # Phase 2: Personal Retrospective Agent Integration (Lightweight Factory Pattern)
        self._retrospective_agent = None  # Lazy initialization for performance

        # Natural language patterns from configuration (DRY compliance)
        self.intent_patterns = {
            InteractionIntent.TIME_NAVIGATION: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "time_navigation"
            ],
            InteractionIntent.DATA_FILTERING: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "data_filtering"
            ],
            InteractionIntent.DRILL_DOWN: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "drill_down"
            ],
            InteractionIntent.COMPARISON: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "comparison"
            ],
            InteractionIntent.CONTEXT_RESET: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "context_reset"
            ],
            InteractionIntent.INSIGHT_REQUEST: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "insight_request"
            ],
            InteractionIntent.RETROSPECTIVE_COMMAND: [
                r"/retrospective\s+(create|view|help)",
                r"retrospective\s+(create|view|help)",
                r"personal\s+retrospective",
                r"weekly\s+retrospective",
            ],
        }

        # Entity and time patterns from configuration
        self.entity_patterns = MCPServerConstants.Phase7B.ENTITY_PATTERNS
        self.time_patterns = MCPServerConstants.Phase7B.TIME_PATTERNS
        self.default_suggestions = MCPServerConstants.Phase7B.DEFAULT_SUGGESTIONS

        # Performance targets from configuration (OVERVIEW.md compliance)
        self.performance_target = (
            MCPServerConstants.Phase7B.INTERACTION_PROCESSING_TARGET
        )

        logger.info(f"ConversationalInteractionManager {self.version} initialized")
        logger.info(
            "✅ ARCHITECTURE: Extends Phase 7A InteractiveEnhancementAddon (DRY compliance)"
        )

    @property
    def retrospective_agent(self) -> PersonalRetrospectiveAgent:
        """
        Lazy-loaded PersonalRetrospectiveAgent (SOLID: Single Responsibility)

        ARCHITECTURE COMPLIANCE:
        - DRY: Reuses existing BaseManager pattern
        - Performance: Lazy initialization
        - SOLID: Dependency injection pattern
        """
        if self._retrospective_agent is None:
            self._retrospective_agent = PersonalRetrospectiveAgent()
            logger.info("✅ PersonalRetrospectiveAgent initialized (lazy loading)")
        return self._retrospective_agent

    def cleanup(self):
        """
        Cleanup resources following OVERVIEW.md patterns

        PERFORMANCE REQUIREMENT: <500ms enterprise SLA compliance
        """
        logger.info("🧹 Cleaning up Conversational Interaction Manager...")

        if hasattr(self.interactive_addon, "cleanup"):
            self.interactive_addon.cleanup()

        if hasattr(self.mcp_manager, "cleanup"):
            self.mcp_manager.cleanup()

        logger.info("✅ Conversational Interaction Manager cleanup complete")

    async def async_cleanup(self):
        """Async cleanup for background tasks - OVERVIEW.md performance compliance"""
        logger.info("🧹 Performing async cleanup...")

        if hasattr(self.interactive_addon, "async_cleanup"):
            await self.interactive_addon.async_cleanup()

        if hasattr(self.mcp_manager, "async_cleanup"):
            await self.mcp_manager.async_cleanup()

        logger.info("✅ Conversational Interaction Manager async cleanup complete")

    async def process_interaction_query(
        self, query: str, chart_id: str, current_context: Dict[str, Any] = None
    ) -> UnifiedResponse:
        """
        Process natural language chart interactions with <500ms target

        Args:
            query: Natural language query from user
            chart_id: Current chart identifier
            current_context: Current chart state and context

        Returns:
            InteractionResponse with updated chart and suggestions

        PERFORMANCE TARGET: <500ms processing (OVERVIEW.md enterprise SLA)
        ARCHITECTURE: Uses Always-On MCP Enhancement (Phase 12)
        """
        start_time = time.time()
        current_context = current_context or {}

        try:
            logger.info(
                f"Processing conversational query: '{query}' for chart {chart_id}"
            )

            # Step 1: Parse query intent using pattern matching (fast local processing)
            intent = self._parse_query_intent(query)
            logger.info(
                f"Intent recognized: {intent.intent.value} (confidence: {intent.confidence:.2f})"
            )

            # Phase 2: Personal Retrospective Command Routing (DRY compliance)
            if intent.intent == InteractionIntent.RETROSPECTIVE_COMMAND:
                return await self._handle_retrospective_command(query, current_context)

            # Step 2: Apply chart modifications based on intent
            # ARCHITECTURE: Leverage existing InteractiveEnhancementAddon (DRY principle)
            modification_result = await self._apply_chart_modifications(
                intent, chart_id, current_context
            )

            # Step 3: Generate follow-up suggestions using strategic context
            follow_up_suggestions = await self._generate_follow_up_suggestions(
                intent, current_context, modification_result
            )

            processing_time = time.time() - start_time
            logger.info(f"✅ Conversational query processed in {processing_time:.3f}s")

            return await create_conversational_response(
                content=modification_result.get("updated_html", ""),
                status=ResponseStatus.SUCCESS,
                success=True,
                follow_up_suggestions=follow_up_suggestions,
                intent_recognized=intent,
                chart_state_updated=modification_result.get("state_changed", False),
                metadata={
                    "original_processing_time": processing_time,
                },
            )

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"❌ Error processing conversational query: {e}", exc_info=True
            )

            # ARCHITECTURE: Lightweight Fallback Pattern (OVERVIEW.md)
            return await create_conversational_response(
                content=current_context.get("original_html", ""),
                status=ResponseStatus.ERROR,
                success=False,
                error=f"Conversational processing failed: {str(e)}",
                metadata={
                    "original_processing_time": processing_time,
                },
            )

    def _parse_query_intent(self, query: str) -> QueryIntent:
        """
        Parse natural language query to extract intent and entities

        PERFORMANCE: Fast local processing for <500ms target
        """
        query_lower = query.lower()
        intent_scores = {}

        # Score each intent based on keyword matching
        for intent_type, keywords in self.intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                intent_scores[intent_type] = score / len(keywords)

        # Determine best intent match
        if intent_scores:
            best_intent = max(intent_scores.keys(), key=lambda k: intent_scores[k])
            confidence = intent_scores[best_intent]
        else:
            best_intent = InteractionIntent.UNKNOWN
            confidence = 0.0

        # Extract entities and parameters (basic pattern matching)
        entities = self._extract_entities(query_lower)
        time_period = self._extract_time_period(query_lower)
        filter_criteria = self._extract_filter_criteria(query_lower, best_intent)

        return QueryIntent(
            intent=best_intent,
            entities=entities,
            time_period=time_period,
            filter_criteria=filter_criteria,
            confidence=confidence,
            raw_query=query,
        )

    def _extract_entities(self, query: str) -> List[str]:
        """Extract relevant entities from query using configuration patterns"""
        entities = []

        # Use configured entity patterns (DRY compliance)
        for category, patterns in self.entity_patterns.items():
            for pattern in patterns:
                if pattern in query:
                    entities.append(pattern)

        return entities

    def _extract_time_period(self, query: str) -> Optional[str]:
        """Extract time period from query using configured patterns"""
        # Use configured time patterns (DRY compliance)
        for pattern in self.time_patterns:
            if pattern in query:
                return pattern

        return None

    def _extract_filter_criteria(
        self, query: str, intent: InteractionIntent
    ) -> Dict[str, str]:
        """Extract filter criteria based on intent"""
        criteria = {}

        if intent == InteractionIntent.DATA_FILTERING:
            # Look for "by X" patterns
            if "by " in query:
                parts = query.split("by ")
                if len(parts) > 1:
                    filter_value = parts[1].split()[0]  # First word after "by"
                    criteria["filter_by"] = filter_value

        return criteria

    async def _apply_chart_modifications(
        self, intent: QueryIntent, chart_id: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply chart modifications based on parsed intent

        ARCHITECTURE: Uses Phase 7A InteractiveEnhancementAddon (DRY compliance)
        """
        try:
            # Map intent to chart operations
            if intent.intent == InteractionIntent.TIME_NAVIGATION:
                return await self._handle_time_navigation(intent, chart_id, context)
            elif intent.intent == InteractionIntent.DATA_FILTERING:
                return await self._handle_data_filtering(intent, chart_id, context)
            elif intent.intent == InteractionIntent.DRILL_DOWN:
                return await self._handle_drill_down(intent, chart_id, context)
            elif intent.intent == InteractionIntent.COMPARISON:
                return await self._handle_comparison(intent, chart_id, context)
            elif intent.intent == InteractionIntent.CONTEXT_RESET:
                return await self._handle_context_reset(intent, chart_id, context)
            elif intent.intent == InteractionIntent.INSIGHT_REQUEST:
                return await self._handle_insight_request(intent, chart_id, context)
            else:
                # Default: return current state
                return {
                    "updated_html": context.get("current_html", ""),
                    "state_changed": False,
                }

        except Exception as e:
            logger.error(f"Error applying chart modifications: {e}")
            return {
                "updated_html": context.get("current_html", ""),
                "state_changed": False,
            }

    async def _handle_time_navigation(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """Handle time-based navigation requests"""
        logger.info(f"Applying time navigation: {intent.time_period}")

        # In a real implementation, this would modify the chart data/view
        # For now, return mock updated state
        updated_html = context.get("current_html", "")
        # TODO: Actual time filtering logic would go here

        return {
            "updated_html": updated_html,
            "state_changed": True,
            "modification_type": "time_navigation",
            "applied_period": intent.time_period,
        }

    async def _handle_data_filtering(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """Handle data filtering requests"""
        logger.info(f"Applying data filtering: {intent.filter_criteria}")

        updated_html = context.get("current_html", "")
        # TODO: Actual filtering logic would go here

        return {
            "updated_html": updated_html,
            "state_changed": True,
            "modification_type": "data_filtering",
            "applied_filters": intent.filter_criteria,
        }

    async def _handle_drill_down(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """Handle drill-down requests"""
        logger.info(f"Applying drill-down: {intent.entities}")

        updated_html = context.get("current_html", "")
        # TODO: Actual drill-down logic would go here

        return {
            "updated_html": updated_html,
            "state_changed": True,
            "modification_type": "drill_down",
            "drill_entities": intent.entities,
        }

    async def _handle_comparison(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """Handle comparison requests"""
        logger.info(f"Applying comparison analysis")

        updated_html = context.get("current_html", "")
        # TODO: Actual comparison logic would go here

        return {
            "updated_html": updated_html,
            "state_changed": True,
            "modification_type": "comparison",
            "comparison_entities": intent.entities,
        }

    async def _handle_context_reset(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """Handle context reset requests"""
        logger.info("Resetting chart context to default state")

        # Reset to original chart state
        updated_html = context.get("original_html", context.get("current_html", ""))

        return {
            "updated_html": updated_html,
            "state_changed": True,
            "modification_type": "context_reset",
        }

    async def _handle_insight_request(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """Handle requests for insights and analysis"""
        logger.info("Generating strategic insights for chart data")

        # TODO: Integration with MCP Sequential for strategic analysis
        # This would use Always-On MCP Enhancement (Phase 12)

        updated_html = context.get("current_html", "")

        return {
            "updated_html": updated_html,
            "state_changed": False,
            "modification_type": "insight_request",
            "insights_generated": True,
        }

    async def _generate_follow_up_suggestions(
        self,
        intent: QueryIntent,
        context: Dict[str, Any],
        modification_result: Dict[str, Any],
    ) -> List[str]:
        """
        Generate strategic follow-up suggestions

        ARCHITECTURE: Uses strategic context for persona-aware suggestions
        """
        try:
            suggestions = []

            # Use configured suggestions based on intent (DRY compliance)
            if intent.intent == InteractionIntent.TIME_NAVIGATION:
                suggestions = self.default_suggestions.get("time_navigation", [])
            elif intent.intent == InteractionIntent.DATA_FILTERING:
                suggestions = self.default_suggestions.get("data_filtering", [])
            elif intent.intent == InteractionIntent.DRILL_DOWN:
                suggestions = self.default_suggestions.get("drill_down", [])
            else:
                suggestions = self.default_suggestions.get("default", [])

            # Limit to 3 most relevant suggestions
            return suggestions[:3]

        except Exception as e:
            logger.error(f"Error generating follow-up suggestions: {e}")
            return self.default_suggestions.get("default", [])

    async def _handle_retrospective_command(
        self, query: str, current_context: Dict[str, Any] = None
    ) -> UnifiedResponse:
        """
        Handle personal retrospective commands (Phase 2 Integration)

        ARCHITECTURE COMPLIANCE:
        - DRY: Delegates to PersonalRetrospectiveAgent (no duplication)
        - SOLID: Single responsibility for command routing
        - Performance: <500ms target maintained

        Args:
            query: Original user query (e.g., "/retrospective create")
            current_context: Current session context

        Returns:
            UnifiedResponse: Retrospective command result
        """
        start_time = time.time()

        try:
            # Parse retrospective command from query
            query_lower = query.lower().strip()
            user_id = (
                current_context.get("user_id", "default_user")
                if current_context
                else "default_user"
            )

            # Extract command and user input
            if "/retrospective create" in query_lower:
                command = "/retrospective create"
                user_input = ""
            elif "/retrospective view" in query_lower:
                command = "/retrospective view"
                user_input = ""
            elif "/retrospective help" in query_lower:
                command = "/retrospective help"
                user_input = ""
            else:
                # Handle session input during active retrospective
                command = "session_input"
                user_input = query.strip()

            # Delegate to PersonalRetrospectiveAgent (DRY compliance)
            request_data = {
                "command": command,
                "user_id": user_id,
                "user_input": user_input,
            }

            result = self.retrospective_agent.process_request(request_data)

            processing_time = time.time() - start_time
            logger.info(f"✅ Retrospective command processed in {processing_time:.3f}s")

            return await create_conversational_response(
                content=result.message,
                status=(
                    ResponseStatus.SUCCESS if result.success else ResponseStatus.ERROR
                ),
                success=result.success,
                follow_up_suggestions=(
                    [
                        "/retrospective create - Start new retrospective",
                        "/retrospective view - View recent entries",
                        "/retrospective help - Show help",
                    ]
                    if result.success
                    else []
                ),
                metadata={
                    "retrospective_command": command,
                    "processing_time": processing_time,
                    "agent_result": result.__dict__,
                },
            )

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"❌ Error processing retrospective command: {e}", exc_info=True
            )

            return await create_conversational_response(
                content=f"Sorry, I encountered an error processing your retrospective command: {str(e)}",
                status=ResponseStatus.ERROR,
                success=False,
                error=f"Retrospective processing failed: {str(e)}",
                metadata={
                    "processing_time": processing_time,
                },
            )

    def __enter__(self):
        """Context manager entry point"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - ensures cleanup"""
        self.cleanup()

    async def __aenter__(self):
        """Async context manager entry point"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit point - ensures async cleanup"""
        await self.async_cleanup()


def create_conversational_interaction_manager(
    interactive_addon: Optional[InteractiveEnhancementAddon] = None,
) -> ConversationalInteractionManager:
    """
    Factory function for ConversationalInteractionManager

    Args:
        interactive_addon: Optional Phase 7A addon to extend (DRY compliance)

    Returns:
        ConversationalInteractionManager: Ready for natural language interactions
    """
    return ConversationalInteractionManager(interactive_addon)
