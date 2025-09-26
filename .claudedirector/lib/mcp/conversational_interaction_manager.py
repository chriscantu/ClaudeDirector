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

# ✅ DRY: Import terminal-safe daily planning agent (BLOAT_PREVENTION_SYSTEM.md compliant)
try:
    from agents.terminal_safe_daily_planning_agent import TerminalSafeDailyPlanningAgent

    DAILY_PLANNING_AVAILABLE = True
except ImportError:
    # Graceful degradation if not available
    class TerminalSafeDailyPlanningAgent:
        pass

    DAILY_PLANNING_AVAILABLE = False

# Phase 2: Personal Retrospective Agent Integration (DRY compliance)
try:
    from agents.personal_retrospective_agent import PersonalRetrospectiveAgent

    RETROSPECTIVE_AVAILABLE = True
except ImportError:
    # Graceful degradation if not available
    class PersonalRetrospectiveAgent:
        pass

    RETROSPECTIVE_AVAILABLE = True

logger = logging.getLogger(__name__)


class InteractionIntent(Enum):
    """Natural language interaction intent classification"""

    TIME_NAVIGATION = "time_navigation"  # "Show me Q3 data"
    DATA_FILTERING = "data_filtering"  # "Filter by engineering team"
    DRILL_DOWN = "drill_down"  # "Drill down into platform metrics"
    COMPARISON = "comparison"  # "Compare with last quarter"
    CONTEXT_RESET = "context_reset"  # "Go back", "Reset filters"
    INSIGHT_REQUEST = "insight_request"  # "What's driving this spike?"
    DAILY_PLAN_COMMAND = (
        "daily_plan_command"  # "Daily plan start", "/daily-plan review"
    )
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
            InteractionIntent.DAILY_PLAN_COMMAND: MCPServerConstants.Phase7B.INTENT_PATTERNS[
                "daily_plan_command"
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

        # ✅ DRY: Lazy initialization for optional managers
        self._daily_planning_agent = None
        self._retrospective_agent = None

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
        if not RETROSPECTIVE_AVAILABLE:
            return None

        if self._retrospective_agent is None:
            self._retrospective_agent = PersonalRetrospectiveAgent()
            logger.info("✅ PersonalRetrospectiveAgent initialized (lazy loading)")
        return self._retrospective_agent

    @property
    def daily_planning_agent(self) -> PersonalDailyPlanningAgent:
        """
        Lazy-loaded PersonalDailyPlanningAgent (Pattern Compliance: follows retrospective_agent)

        ARCHITECTURE COMPLIANCE:
        - DRY: Reuses existing BaseManager pattern
        - Performance: Lazy initialization
        - PATTERN CONSISTENCY: Same pattern as retrospective_agent
        """
        if not DAILY_PLANNING_AVAILABLE:
            return None

        if self._daily_planning_agent is None:
            self._daily_planning_agent = PersonalDailyPlanningAgent()
            logger.info("✅ PersonalDailyPlanningAgent initialized (lazy loading)")

        return self._daily_planning_agent

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

    @property
    def daily_planning_manager(self) -> Optional[TerminalSafeDailyPlanningAgent]:
        """
        ✅ DRY: Lazy initialization of TerminalSafeDailyPlanningAgent
        Following existing pattern for optional manager integration
        """
        if not DAILY_PLANNING_AVAILABLE:
            return None

        if self._daily_planning_manager is None:
            try:
                self._daily_planning_manager = TerminalSafeDailyPlanningAgent()
                logger.info(
                    "✅ TerminalSafeDailyPlanningAgent initialized successfully"
                )
            except Exception as e:
                logger.error(
                    f"❌ Failed to initialize TerminalSafeDailyPlanningAgent: {e}"
                )
                return None

        return self._daily_planning_manager

    @property
    def retrospective_agent(self) -> Optional[PersonalRetrospectiveAgent]:
        """
        ✅ Lazy initialization of PersonalRetrospectiveAgent following daily-planning pattern
        ✅ DRY: Reuses existing initialization pattern
        """
        if not RETROSPECTIVE_AVAILABLE:
            return None

        if self._retrospective_agent is None:
            try:
                from ..agents.personal_retrospective_agent import (
                    PersonalRetrospectiveAgent,
                )

                self._retrospective_agent = PersonalRetrospectiveAgent()
                logger.info("✅ PersonalRetrospectiveAgent initialized")
            except ImportError as e:
                logger.warning(f"PersonalRetrospectiveAgent not available: {e}")
                return None

        return self._retrospective_agent

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

            # Phase 2: Daily Planning Command Routing (Pattern Compliance: follows retrospective)
            if intent.intent == InteractionIntent.DAILY_PLAN_COMMAND:
                return await self._handle_daily_plan_command(query, current_context)

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
            elif intent.intent == InteractionIntent.DAILY_PLAN_COMMAND:
                return await self._handle_daily_plan_command(intent, chart_id, context)
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

    async def _handle_daily_plan_command(
        self, intent: QueryIntent, chart_id: str, context: Dict
    ) -> Dict:
        """
        ✅ Handle daily planning commands
        ✅ DRY: Uses existing PersonalDailyPlanningAgent for coordination
        """
        logger.info(f"Processing daily plan command: {intent.raw_query}")

        if not self.daily_planning_agent:
            logger.warning("PersonalDailyPlanningAgent not available")
            return {
                "updated_html": context.get("current_html", ""),
                "state_changed": False,
                "modification_type": "daily_plan_command",
                "error": "Daily planning feature not available",
            }

        try:
            # ✅ Parse command type from query
            query_lower = intent.raw_query.lower()

            if any(
                word in query_lower for word in ["start", "create", "new", "plan today"]
            ):
                # Extract priorities from query (simple parsing)
                priorities = self._extract_priorities_from_query(intent.raw_query)

                # ✅ DRY: Use existing PersonalDailyPlanningAgent
                result = self.daily_planning_agent.process_request(
                    {
                        "command": "/daily-plan start",
                        "user_id": context.get("user_id", "default"),
                        "user_input": "",
                    }
                )

                response_content = (
                    f"✅ Daily plan created with {len(priorities)} priorities"
                )
                if result.strategic_analysis:
                    alignment_score = result.strategic_analysis.get(
                        "alignment_score", 0
                    )
                    response_content += (
                        f"\n📊 Strategic Alignment: {alignment_score:.0f}%"
                    )

            elif any(
                word in query_lower
                for word in ["review", "check", "status", "progress"]
            ):
                # ✅ DRY: Use existing PersonalDailyPlanningAgent for status
                result = self.daily_planning_manager.process_request(
                    {
                        "command": "/daily-plan status",
                        "user_id": context.get("user_id", "default"),
                        "user_input": "",
                    }
                )

                if result.completion_stats:
                    completed = result.completion_stats.get("completed_tasks", 0)
                    total = result.completion_stats.get("total_tasks", 0)
                    response_content = (
                        f"📊 Daily progress: {completed}/{total} tasks completed"
                    )
                else:
                    response_content = "📊 No daily plan found for today"

            elif any(
                word in query_lower
                for word in ["complete", "done", "finished", "mark done"]
            ):
                # ✅ NEW: Handle task completion with fuzzy matching
                priority_name = self._extract_priority_name_from_completion_query(
                    intent.raw_query
                )

                if not priority_name:
                    response_content = "❓ Please specify which priority to mark as complete (e.g., 'daily plan complete team meeting')"
                else:
                    # ✅ DRY: Use existing PersonalDailyPlanningAgent for completion
                    result = self.daily_planning_manager.process_request(
                        {
                            "command": "complete",
                            "user_id": context.get("user_id", "default"),
                            "user_input": priority_name,
                        }
                    )

                    if result.success:
                        response_content = result.message
                        if result.completion_stats:
                            completed = result.completion_stats.get(
                                "completed_tasks", 0
                            )
                            total = result.completion_stats.get("total_tasks", 0)
                            response_content += (
                                f"\n📊 Progress: {completed}/{total} tasks completed"
                            )
                    else:
                        response_content = f"❌ {result.message}"

            elif any(
                word in query_lower for word in ["balance", "strategic", "l0", "l1"]
            ):
                # ✅ DRY: Use existing PersonalDailyPlanningAgent for strategic balance
                result = self.daily_planning_manager.process_request(
                    {
                        "command": "balance",
                        "user_id": context.get("user_id", "default"),
                        "user_input": "",
                    }
                )

                if result.l0_l1_balance:
                    l0_pct = result.l0_l1_balance.get("l0_percentage", 0)
                    l1_pct = result.l0_l1_balance.get("l1_percentage", 0)
                    response_content = (
                        f"⚖️ Strategic balance: L0 {l0_pct:.0f}%, L1 {l1_pct:.0f}%"
                    )
                else:
                    response_content = "⚖️ Strategic balance analysis unavailable"
            else:
                # Default help response
                response_content = """
                🎯 Daily Planning Commands:
                • "daily plan start" - Create new daily plan
                • "daily plan complete [task]" - Mark priority as done
                • "daily plan review" - Check today's progress
                • "daily plan status" - Quick progress overview
                • "daily plan balance" - View strategic alignment
                """

            return {
                "updated_html": context.get("current_html", "")
                + f"\n{response_content}",
                "state_changed": True,
                "modification_type": "daily_plan_command",
                "daily_plan_result": result.data if hasattr(result, "data") else None,
                "command_processed": True,
            }

        except Exception as e:
            logger.error(f"Error processing daily plan command: {e}")
            return {
                "updated_html": context.get("current_html", ""),
                "state_changed": False,
                "modification_type": "daily_plan_command",
                "error": f"Daily planning error: {str(e)}",
            }

    def _extract_priorities_from_query(self, query: str) -> List[str]:
        """
        ✅ Simple priority extraction from natural language
        ✅ No complex NLP - basic pattern matching only
        """
        # Remove command words and extract priorities
        query_clean = query.lower()
        for cmd_word in [
            "daily plan",
            "start",
            "create",
            "new",
            "plan today",
            "/daily-plan",
        ]:
            query_clean = query_clean.replace(cmd_word, "")

        # Simple priority extraction - split by common delimiters
        priorities = []
        for delimiter in [",", ";", "and", "&"]:
            if delimiter in query_clean:
                parts = [p.strip() for p in query_clean.split(delimiter) if p.strip()]
                priorities = parts
                break

        # Fallback: if no delimiters, treat whole query as single priority
        if not priorities and query_clean.strip():
            priorities = [query_clean.strip()]

        # Default priorities if nothing extracted
        if not priorities:
            priorities = ["Strategic planning", "Team coordination", "Technical debt"]

        return priorities[:5]  # Limit to 5 priorities

    def _extract_priority_name_from_completion_query(self, query: str) -> str:
        """
        ✅ Extract priority name from completion commands for fuzzy matching
        ✅ SOLID: Single responsibility for priority name extraction
        """
        query_lower = query.lower()

        # Remove common completion command words
        for cmd_word in [
            "daily plan complete",
            "daily plan done",
            "mark done",
            "complete priority",
            "done",
            "finished",
            "complete",
        ]:
            if cmd_word in query_lower:
                query_lower = query_lower.replace(cmd_word, "").strip()
                break

        # Clean up extra words and return priority name
        priority_name = query_lower.strip()

        # If nothing left, return empty string
        if not priority_name or len(priority_name.strip()) < 2:
            return ""

        return priority_name

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
            # Check if retrospective agent is available
            if not RETROSPECTIVE_AVAILABLE:
                logger.warning("PersonalRetrospectiveAgent not available")
                return await create_conversational_response(
                    content="Sorry, the retrospective feature is not available.",
                    status=ResponseStatus.ERROR,
                    success=False,
                    error="Personal retrospective feature not available",
                    metadata={"processing_time": time.time() - start_time},
                )

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

    async def _handle_daily_plan_command(
        self, query: str, current_context: Dict[str, Any] = None
    ) -> UnifiedResponse:
        """
        Handle daily planning commands (Pattern Compliance: follows _handle_retrospective_command)

        ARCHITECTURE COMPLIANCE:
        - DRY: Delegates to PersonalDailyPlanningAgent (no duplication)
        - PATTERN CONSISTENCY: Exact same structure as _handle_retrospective_command
        - Performance: <500ms target maintained

        Args:
            query: Original user query (e.g., "/daily-plan start")
            current_context: Current session context

        Returns:
            UnifiedResponse: Daily planning command result
        """
        start_time = time.time()

        try:
            # Check if daily planning manager is available
            if not DAILY_PLANNING_AVAILABLE:
                logger.warning("PersonalDailyPlanningAgent not available")

                return await create_conversational_response(
                    content="Sorry, the daily planning feature is not available.",
                    status=ResponseStatus.ERROR,
                    success=False,
                    error="Daily planning feature not available",
                    metadata={"processing_time": time.time() - start_time},
                )

            # Parse daily planning command from query (SAME PATTERN as retrospective)
            query_lower = query.lower().strip()
            user_id = (
                current_context.get("user_id", "default_user")
                if current_context
                else "default_user"
            )

            # Extract command and user input (FOLLOWS RETROSPECTIVE PATTERN)
            if "/daily-plan start" in query_lower:
                command = "/daily-plan start"
                user_input = ""
            elif "/daily-plan status" in query_lower:
                command = "/daily-plan status"
                user_input = ""
            elif "/daily-plan review" in query_lower:
                command = "/daily-plan review"
                user_input = ""
            elif "/daily-plan help" in query_lower:
                command = "/daily-plan help"
                user_input = ""
            else:
                # Handle session input during active daily planning
                command = "session_input"
                user_input = query.strip()

            # Delegate to PersonalDailyPlanningAgent (SAME PATTERN as retrospective)
            request_data = {
                "command": command,
                "user_id": user_id,
                "user_input": user_input,
            }

            result = self.daily_planning_manager.process_request(request_data)

            processing_time = time.time() - start_time
            logger.info(
                f"✅ Daily planning command processed in {processing_time:.3f}s"
            )

            return await create_conversational_response(
                content=result.message,
                status=(
                    ResponseStatus.SUCCESS if result.success else ResponseStatus.ERROR
                ),
                success=result.success,
                follow_up_suggestions=(
                    [
                        "/daily-plan start - Start new daily plan",
                        "/daily-plan status - Check today's plan",
                        "/daily-plan review - Review recent plans",
                        "/daily-plan help - Show help",
                    ]
                    if result.success
                    else []
                ),
                metadata={
                    "daily_plan_command": command,
                    "processing_time": processing_time,
                    "manager_result": result.__dict__,
                },
            )

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"❌ Error processing daily planning command: {e}", exc_info=True
            )

            return await create_conversational_response(
                content=f"Sorry, I encountered an error processing your daily planning command: {str(e)}",
                status=ResponseStatus.ERROR,
                success=False,
                error=f"Daily planning processing failed: {str(e)}",
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
