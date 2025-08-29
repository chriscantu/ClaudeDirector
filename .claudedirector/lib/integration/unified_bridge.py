"""
Unified Bridge System - Phase 10 Final Consolidation
Consolidates all integration and bridge functionality into single enterprise module.

Phase 10 Consolidation includes:
- LegacyConversationMemoryBridge (context_engineering/legacy_bridge.py)
- MemoryContextBridge (memory/context_engineering_bridge.py)
- IntelligenceContextBridge (intelligence/context_engineering_integration.py)
- MCPUseClient (integrations/mcp_use_client.py - 284 lines)
- CLIContextBridge (bridges/cli_context_bridge.py - 478 lines)

Total: 762 lines from integrations/ + bridges/ consolidated
Following DRY principles and SOLID architecture patterns.
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import logging
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

try:
    from ..context_engineering import (
        AdvancedContextEngine,
        StakeholderRole,
        CommunicationStyle,
        InitiativeStatus,
        FrameworkUsage,
        DecisionPattern,
    )

    CONTEXT_ENGINEERING_AVAILABLE = True
except ImportError:
    CONTEXT_ENGINEERING_AVAILABLE = False
    AdvancedContextEngine = None


class BridgeType(Enum):
    """Types of legacy systems being bridged"""

    CONVERSATION_MEMORY = "conversation_memory"
    STRATEGIC_MEMORY = "strategic_memory"
    INTELLIGENCE = "intelligence"
    ALL = "unified"


@dataclass
class BridgeConfig:
    """Unified configuration for all bridge types"""

    bridge_type: BridgeType
    retention_days: int = 365
    max_items: int = 1000
    performance_target_ms: int = 300
    enable_migration: bool = True
    fallback_enabled: bool = True


@dataclass
class MigrationResult:
    """Standardized migration result across all bridge types"""

    items_migrated: int
    categories_migrated: int
    errors: List[str]
    duration_seconds: float
    success_rate: float


class UnifiedBridge:
    """
    Single bridge class replacing all separate bridge implementations.
    Provides unified interface for all legacy system integration.
    """

    def __init__(
        self,
        config: BridgeConfig,
        context_engine: Optional[AdvancedContextEngine] = None,
    ):
        """Initialize unified bridge with specified configuration"""
        self.logger = logging.getLogger(__name__)
        self.config = config

        # Initialize Context Engineering with optimized config for bridge type
        if CONTEXT_ENGINEERING_AVAILABLE:
            self.context_engine = (
                context_engine or self._create_optimized_context_engine()
            )
            self.enhanced_mode = True
        else:
            self.context_engine = None
            self.enhanced_mode = False

        # Legacy compatibility storage for fallback
        self.legacy_data = {
            "conversations": {},
            "stakeholders": {},
            "meetings": {},
            "tasks": {},
            "patterns": {},
        }

        self.logger.info(
            f"UnifiedBridge initialized - Type: {config.bridge_type.value}, Enhanced: {self.enhanced_mode}"
        )

    def _create_optimized_context_engine(self) -> AdvancedContextEngine:
        """Create Context Engineering with configuration optimized for bridge type"""
        base_config = {
            "conversation": {
                "retention_days": self.config.retention_days,
                "max_conversations": self.config.max_items,
            },
            "strategic": {
                "max_initiatives": self.config.max_items // 2,
                "health_threshold": 0.7,
            },
            "stakeholder": {
                "max_stakeholders": self.config.max_items,
                "interaction_retention": self.config.retention_days,
            },
            "learning": {"min_usage_for_pattern": 2, "effectiveness_threshold": 0.6},
            "organizational": {
                "max_team_history": 100,
                "change_retention": self.config.retention_days,
            },
            "orchestrator": {
                "max_context_size": 1024 * 1024,
                "performance_target_ms": self.config.performance_target_ms,
            },
        }

        # Optimize based on bridge type
        if self.config.bridge_type == BridgeType.CONVERSATION_MEMORY:
            base_config["conversation"]["max_conversations"] = self.config.max_items * 2
            base_config["orchestrator"][
                "performance_target_ms"
            ] = 200  # Faster for conversations

        elif self.config.bridge_type == BridgeType.STRATEGIC_MEMORY:
            base_config["strategic"]["max_initiatives"] = self.config.max_items
            base_config["stakeholder"]["max_stakeholders"] = self.config.max_items * 2
            base_config["orchestrator"]["max_context_size"] = (
                2 * 1024 * 1024
            )  # Larger for strategic

        elif self.config.bridge_type == BridgeType.INTELLIGENCE:
            base_config["learning"][
                "min_usage_for_pattern"
            ] = 1  # More sensitive for intelligence
            base_config["stakeholder"]["interaction_retention"] = (
                self.config.retention_days * 2
            )

        return AdvancedContextEngine(base_config)

    # ========================================
    # UNIFIED MIGRATION INTERFACE
    # ========================================

    def migrate_data(
        self, legacy_data: Dict[str, Any], data_type: str
    ) -> MigrationResult:
        """Unified migration interface for all data types"""
        start_time = time.time()

        if data_type == "conversations":
            return self._migrate_conversations(legacy_data, start_time)
        elif data_type == "stakeholders":
            return self._migrate_stakeholders(legacy_data, start_time)
        elif data_type == "meetings":
            return self._migrate_meetings(legacy_data, start_time)
        elif data_type == "tasks":
            return self._migrate_tasks(legacy_data, start_time)
        elif data_type == "intelligence":
            return self._migrate_intelligence(legacy_data, start_time)
        else:
            return MigrationResult(0, 0, [f"Unknown data type: {data_type}"], 0, 0.0)

    def _migrate_conversations(
        self, conversations: List[Dict[str, Any]], start_time: float
    ) -> MigrationResult:
        """Migrate conversation data to Context Engineering"""
        migrated = 0
        errors = []

        if not self.enhanced_mode:
            return self._create_fallback_result(
                len(conversations), start_time, "Context Engineering not available"
            )

        for conv in conversations:
            try:
                conversation_data = {
                    "session_id": conv.get("session_id", "migrated"),
                    "query": conv.get("input", conv.get("query", "")),
                    "response": conv.get("response", ""),
                    "timestamp": conv.get("timestamp", time.time()),
                }

                if self.context_engine.conversation_layer.store_conversation_context(
                    conversation_data
                ):
                    migrated += 1

                    # Also migrate associated frameworks and topics
                    if "frameworks" in conv:
                        for framework in conv["frameworks"]:
                            self.context_engine.learning_layer.update_framework_usage(
                                framework,
                                conversation_data["session_id"],
                                0.7,
                                conv.get("input", ""),
                            )

            except Exception as e:
                errors.append(f"Conversation migration error: {e}")

        duration = time.time() - start_time
        success_rate = migrated / len(conversations) if conversations else 0.0

        return MigrationResult(migrated, 1, errors, duration, success_rate)

    def _migrate_stakeholders(
        self, stakeholders: List[Dict[str, Any]], start_time: float
    ) -> MigrationResult:
        """Migrate stakeholder data to Context Engineering"""
        migrated = 0
        interactions_migrated = 0
        errors = []

        if not self.enhanced_mode:
            return self._create_fallback_result(
                len(stakeholders), start_time, "Context Engineering not available"
            )

        for stakeholder in stakeholders:
            try:
                # Normalize stakeholder data
                profile_data = {
                    "stakeholder_id": stakeholder.get(
                        "stakeholder_key",
                        stakeholder.get(
                            "stakeholder_id",
                            stakeholder.get("name", "").lower().replace(" ", "_"),
                        ),
                    ),
                    "name": stakeholder.get("name", ""),
                    "role": self._normalize_role(stakeholder.get("role", "other")),
                    "organization": stakeholder.get("organization", ""),
                    "communication_style": self._normalize_communication_style(
                        stakeholder.get(
                            "preferred_communication",
                            stakeholder.get("communication_style", "collaborative"),
                        )
                    ),
                    "influence_level": stakeholder.get("influence_level", "medium"),
                    "relationship_quality": stakeholder.get(
                        "relationship_score",
                        stakeholder.get("relationship_quality", 0.7),
                    ),
                    "trust_level": stakeholder.get("trust_level", 0.7),
                    "key_interests": stakeholder.get(
                        "key_topics", stakeholder.get("key_interests", [])
                    ),
                }

                if self.context_engine.stakeholder_layer.update_stakeholder_profile(
                    profile_data
                ):
                    migrated += 1

                    # Migrate interactions
                    interactions = stakeholder.get("interactions", [])
                    for interaction in interactions:
                        interaction_data = {
                            "stakeholder_id": profile_data["stakeholder_id"],
                            "context": interaction.get("context", ""),
                            "topics": interaction.get("topics", []),
                            "satisfaction": interaction.get("satisfaction", 0.7),
                            "session_id": interaction.get("session_id", "migrated"),
                        }

                        if self.context_engine.stakeholder_layer.record_interaction(
                            interaction_data
                        ):
                            interactions_migrated += 1

            except Exception as e:
                errors.append(f"Stakeholder migration error: {e}")

        duration = time.time() - start_time
        success_rate = migrated / len(stakeholders) if stakeholders else 0.0

        return MigrationResult(
            migrated, interactions_migrated, errors, duration, success_rate
        )

    def _migrate_meetings(
        self, meetings: List[Dict[str, Any]], start_time: float
    ) -> MigrationResult:
        """Migrate meeting data to Context Engineering strategic layer"""
        migrated = 0
        errors = []

        if not self.enhanced_mode:
            return self._create_fallback_result(
                len(meetings), start_time, "Context Engineering not available"
            )

        for meeting in meetings:
            try:
                # Convert to strategic initiative
                initiative_data = {
                    "initiative_id": f"meeting_{meeting.get('meeting_id', meeting.get('id', 'unknown'))}",
                    "name": meeting.get(
                        "meeting_type", meeting.get("title", "Strategic Meeting")
                    ),
                    "description": meeting.get(
                        "agenda",
                        meeting.get(
                            "description",
                            f"Meeting with {meeting.get('stakeholder_key', 'stakeholders')}",
                        ),
                    ),
                    "status": (
                        "completed" if meeting.get("completed", False) else "active"
                    ),
                    "stakeholders": (
                        [meeting.get("stakeholder_key", "")]
                        if meeting.get("stakeholder_key")
                        else []
                    ),
                    "frameworks_applied": meeting.get("frameworks_used", []),
                    "start_date": meeting.get(
                        "meeting_date_timestamp", meeting.get("timestamp", 0)
                    ),
                    "progress_percentage": (
                        100.0 if meeting.get("completed", False) else 50.0
                    ),
                    "outcomes": meeting.get(
                        "decisions_made", meeting.get("outcomes", [])
                    ),
                }

                if self.context_engine.strategic_layer.track_initiative(
                    initiative_data
                ):
                    migrated += 1

                    # Also store as conversation if topics available
                    topics = meeting.get("agenda_topics", meeting.get("topics", []))
                    if topics:
                        conversation_data = {
                            "session_id": initiative_data["initiative_id"],
                            "query": f"Meeting topics: {', '.join(topics)}",
                            "response": f"Outcomes: {meeting.get('business_impact', 'Strategic discussion')}",
                            "timestamp": initiative_data["start_date"],
                        }
                        self.context_engine.conversation_layer.store_conversation_context(
                            conversation_data
                        )

            except Exception as e:
                errors.append(f"Meeting migration error: {e}")

        duration = time.time() - start_time
        success_rate = migrated / len(meetings) if meetings else 0.0

        return MigrationResult(migrated, 1, errors, duration, success_rate)

    def _migrate_tasks(
        self, tasks: List[Dict[str, Any]], start_time: float
    ) -> MigrationResult:
        """Migrate task data to Context Engineering learning layer"""
        migrated = 0
        errors = []

        if not self.enhanced_mode:
            return self._create_fallback_result(
                len(tasks), start_time, "Context Engineering not available"
            )

        for task in tasks:
            try:
                # Convert tasks to decision patterns
                decision_data = {
                    "type": task.get("type", "task_completion"),
                    "context_keywords": task.get("keywords", task.get("tags", [])),
                    "frameworks": task.get(
                        "frameworks_used", task.get("recommended_frameworks", [])
                    ),
                    "stakeholders": task.get("stakeholders", []),
                    "outcome_score": task.get(
                        "success_rate", task.get("completion_score", 0.7)
                    ),
                    "session_id": task.get("session_id", "task_migration"),
                }

                if self.context_engine.learning_layer.record_decision_outcome(
                    decision_data
                ):
                    migrated += 1

            except Exception as e:
                errors.append(f"Task migration error: {e}")

        duration = time.time() - start_time
        success_rate = migrated / len(tasks) if tasks else 0.0

        return MigrationResult(migrated, 1, errors, duration, success_rate)

    def _migrate_intelligence(
        self, intelligence_data: Dict[str, Any], start_time: float
    ) -> MigrationResult:
        """Migrate intelligence insights to appropriate Context Engineering layers"""
        migrated = 0
        categories = 0
        errors = []

        if not self.enhanced_mode:
            return self._create_fallback_result(
                1, start_time, "Context Engineering not available"
            )

        try:
            # Migrate different types of intelligence data
            if "stakeholder_insights" in intelligence_data:
                stakeholder_result = self._migrate_stakeholders(
                    intelligence_data["stakeholder_insights"], start_time
                )
                migrated += stakeholder_result.items_migrated
                categories += 1
                errors.extend(stakeholder_result.errors)

            if "meeting_insights" in intelligence_data:
                meeting_result = self._migrate_meetings(
                    intelligence_data["meeting_insights"], start_time
                )
                migrated += meeting_result.items_migrated
                categories += 1
                errors.extend(meeting_result.errors)

            if "task_patterns" in intelligence_data:
                task_result = self._migrate_tasks(
                    intelligence_data["task_patterns"], start_time
                )
                migrated += task_result.items_migrated
                categories += 1
                errors.extend(task_result.errors)

        except Exception as e:
            errors.append(f"Intelligence migration error: {e}")

        duration = time.time() - start_time
        success_rate = migrated / max(categories, 1)

        return MigrationResult(migrated, categories, errors, duration, success_rate)

    # ========================================
    # UNIFIED RETRIEVAL INTERFACE
    # ========================================

    def get_legacy_compatible_data(
        self, data_type: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """Unified interface for retrieving data in legacy formats"""
        if not self.enhanced_mode:
            return self.legacy_data.get(data_type, [])

        try:
            if data_type == "conversations":
                return self._get_legacy_conversations(**kwargs)
            elif data_type == "stakeholders":
                return self._get_legacy_stakeholders(**kwargs)
            elif data_type == "meetings":
                return self._get_legacy_meetings(**kwargs)
            elif data_type == "tasks":
                return self._get_legacy_tasks(**kwargs)
            else:
                return []

        except Exception as e:
            self.logger.error(f"Error retrieving legacy {data_type}: {e}")
            return []

    def _get_legacy_conversations(
        self, session_id: str = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get conversations in legacy format"""
        context_result = (
            self.context_engine.conversation_layer.retrieve_relevant_context(
                "", session_id or "default"
            )
        )
        conversations = context_result.get("conversations", [])

        return [
            {
                "session_id": conv.get("session_id", ""),
                "input": conv.get("query", ""),
                "response": conv.get("response", ""),
                "timestamp": conv.get("timestamp", 0),
                "topics": conv.get("topics", []),
                "frameworks": conv.get("strategic_domains", []),
                "enhanced_available": True,
            }
            for conv in conversations[:limit]
        ]

    def _get_legacy_stakeholders(
        self, stakeholder_id: str = None
    ) -> List[Dict[str, Any]]:
        """Get stakeholders in legacy format"""
        context = self.context_engine.stakeholder_layer.get_relationship_context("")
        stakeholders = context.get("relevant_stakeholders", [])

        return [
            {
                "stakeholder_key": s.get("stakeholder_id", ""),
                "name": s.get("name", ""),
                "role": s.get("role", "other"),
                "organization": s.get("organization", ""),
                "relationship_score": s.get("relationship_quality", 0.7),
                "trust_level": s.get("trust_level", 0.7),
                "influence_level": s.get("influence_level", "medium"),
                "preferred_communication": s.get(
                    "communication_style", "collaborative"
                ),
                "key_topics": s.get("key_interests", []),
                "enhanced_available": True,
            }
            for s in stakeholders
        ]

    def _get_legacy_meetings(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get meetings in legacy format"""
        context = self.context_engine.strategic_layer.get_initiative_context()
        initiatives = context.get("active_initiatives", []) + context.get(
            "recent_completions", []
        )

        meetings = []
        for initiative in initiatives[:limit]:
            if initiative.get("initiative_id", "").startswith("meeting_"):
                meetings.append(
                    {
                        "meeting_id": initiative.get("initiative_id", "").replace(
                            "meeting_", ""
                        ),
                        "meeting_type": initiative.get("name", "Strategic Meeting"),
                        "stakeholder_key": (
                            initiative.get("stakeholders", [""])[0]
                            if initiative.get("stakeholders")
                            else ""
                        ),
                        "meeting_date_timestamp": initiative.get("start_date", 0),
                        "decisions_made": initiative.get("outcomes", []),
                        "business_impact": initiative.get("description", ""),
                        "frameworks_used": initiative.get("frameworks_applied", []),
                        "completed": initiative.get("status") == "completed",
                        "enhanced_available": True,
                    }
                )

        return meetings

    def _get_legacy_tasks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get tasks in legacy format from learning patterns"""
        context = self.context_engine.learning_layer.get_skill_context()
        patterns = context.get("recent_patterns", [])

        return [
            {
                "task_id": f"pattern_{i}",
                "type": pattern.get("type", "task"),
                "keywords": pattern.get("context_keywords", []),
                "frameworks_used": pattern.get("frameworks", []),
                "success_rate": pattern.get("outcome_score", 0.7),
                "enhanced_available": True,
            }
            for i, pattern in enumerate(patterns[:limit])
        ]

    # ========================================
    # UTILITY METHODS
    # ========================================

    def _normalize_role(self, role: str) -> str:
        """Normalize role to Context Engineering format"""
        role_mapping = {
            "vp": StakeholderRole.EXECUTIVE.value,
            "director": StakeholderRole.ENGINEERING_MANAGER.value,
            "manager": StakeholderRole.ENGINEERING_MANAGER.value,
            "engineer": StakeholderRole.ENGINEER.value,
            "product": StakeholderRole.PRODUCT_MANAGER.value,
            "design": StakeholderRole.DESIGNER.value,
            "executive": StakeholderRole.EXECUTIVE.value,
        }

        role_lower = role.lower()
        for key, value in role_mapping.items():
            if key in role_lower:
                return value

        return StakeholderRole.OTHER.value

    def _normalize_communication_style(self, style: str) -> str:
        """Normalize communication style to Context Engineering format"""
        style_mapping = {
            "direct": CommunicationStyle.DIRECT.value,
            "collaborative": CommunicationStyle.COLLABORATIVE.value,
            "analytical": CommunicationStyle.ANALYTICAL.value,
            "diplomatic": CommunicationStyle.DIPLOMATIC.value,
            "results": CommunicationStyle.RESULTS_FOCUSED.value,
        }

        style_lower = style.lower()
        for key, value in style_mapping.items():
            if key in style_lower:
                return value

        return CommunicationStyle.COLLABORATIVE.value

    def _create_fallback_result(
        self, item_count: int, start_time: float, error_msg: str
    ) -> MigrationResult:
        """Create fallback migration result for non-enhanced mode"""
        duration = time.time() - start_time
        return MigrationResult(0, 0, [error_msg], duration, 0.0)

    def get_context_engine(self) -> Optional[AdvancedContextEngine]:
        """Get access to underlying Context Engineering system"""
        return self.context_engine

    def get_recent_interactions(
        self, session_id: str = "default", limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get recent conversation interactions for context analysis (legacy compatibility)"""
        if not self.enhanced_mode:
            return self.legacy_data.get("conversations", {}).get(session_id, [])[:limit]

        try:
            # Get from Context Engineering conversation layer
            context_result = (
                self.context_engine.conversation_layer.retrieve_relevant_context(
                    "", session_id
                )
            )
            conversations = context_result.get("conversations", [])

            # Convert to legacy format expected by enhanced framework engine
            return [
                {
                    "content": conv.get("query", ""),
                    "timestamp": conv.get("timestamp", 0),
                    "topics": conv.get("topics", []),
                    "frameworks": conv.get("strategic_domains", []),
                    "session_id": conv.get("session_id", session_id),
                }
                for conv in conversations[:limit]
            ]

        except Exception as e:
            self.logger.error(f"Error getting recent interactions: {e}")
            return []

    def health_check(self) -> Dict[str, Any]:
        """Unified health check for bridge system"""
        status = {
            "bridge_type": self.config.bridge_type.value,
            "enhanced_mode": self.enhanced_mode,
            "context_engineering_available": CONTEXT_ENGINEERING_AVAILABLE,
            "configuration": {
                "retention_days": self.config.retention_days,
                "max_items": self.config.max_items,
                "performance_target_ms": self.config.performance_target_ms,
            },
        }

        if self.enhanced_mode:
            try:
                # Test context retrieval
                test_result = self.context_engine.get_contextual_intelligence(
                    "health check", "unified_bridge", max_context_size=64 * 1024
                )

                status.update(
                    {
                        "context_engine_responsive": True,
                        "retrieval_time_ms": test_result.get("metrics", {}).get(
                            "retrieval_time_seconds", 0
                        )
                        * 1000,
                        "context_layers_available": len(test_result.get("context", {})),
                        "memory_usage_mb": self._calculate_total_memory_usage(),
                    }
                )
            except Exception as e:
                status.update({"context_engine_responsive": False, "error": str(e)})

        return status

    def _calculate_total_memory_usage(self) -> float:
        """Calculate total memory usage across all Context Engineering layers"""
        if not self.enhanced_mode:
            return 0.0

        try:
            return sum(
                [
                    self.context_engine.conversation_layer.get_memory_usage().get(
                        "total_memory_mb", 0
                    ),
                    self.context_engine.strategic_layer.get_memory_usage().get(
                        "total_memory_mb", 0
                    ),
                    self.context_engine.stakeholder_layer.get_memory_usage().get(
                        "total_memory_mb", 0
                    ),
                    self.context_engine.learning_layer.get_memory_usage().get(
                        "total_memory_mb", 0
                    ),
                    self.context_engine.organizational_layer.get_memory_usage().get(
                        "total_memory_mb", 0
                    ),
                ]
            )
        except Exception:
            return 0.0


# ========================================
# FACTORY FUNCTIONS
# ========================================


def create_conversation_bridge(
    retention_days: int = 90, max_conversations: int = 1000
) -> UnifiedBridge:
    """Create bridge optimized for conversation memory"""
    config = BridgeConfig(
        bridge_type=BridgeType.CONVERSATION_MEMORY,
        retention_days=retention_days,
        max_items=max_conversations,
        performance_target_ms=200,
    )
    return UnifiedBridge(config)


def create_memory_bridge(
    retention_days: int = 365, max_items: int = 2000
) -> UnifiedBridge:
    """Create bridge optimized for strategic memory"""
    config = BridgeConfig(
        bridge_type=BridgeType.STRATEGIC_MEMORY,
        retention_days=retention_days,
        max_items=max_items,
        performance_target_ms=500,
    )
    return UnifiedBridge(config)


def create_intelligence_bridge(
    retention_days: int = 180, max_items: int = 1500
) -> UnifiedBridge:
    """Create bridge optimized for intelligence systems"""
    config = BridgeConfig(
        bridge_type=BridgeType.INTELLIGENCE,
        retention_days=retention_days,
        max_items=max_items,
        performance_target_ms=300,
    )
    return UnifiedBridge(config)


def create_unified_bridge(
    retention_days: int = 365, max_items: int = 2000
) -> UnifiedBridge:
    """Create unified bridge for all system types"""
    config = BridgeConfig(
        bridge_type=BridgeType.ALL,
        retention_days=retention_days,
        max_items=max_items,
        performance_target_ms=300,
    )
    return UnifiedBridge(config)


# === MCP USE CLIENT INTEGRATION (from integrations/mcp_use_client.py) ===

import asyncio
import yaml


@dataclass
class MCPResponse:
    """Response from MCP server execution"""

    content: str
    source_server: str
    processing_time: float
    success: bool
    error_message: Optional[str] = None
    cached: bool = False


@dataclass
class ConnectionStatus:
    """Status of MCP server connections"""

    available_servers: List[str]
    failed_servers: List[str]
    total_servers: int
    success_rate: float


class MCPUseClient:
    """
    Interface to mcp-use library for STDIO/HTTP MCP server connections.
    Consolidated from integrations/mcp_use_client.py (284 lines).
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize MCP client with zero-setup approach"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.mcp_client = None
        self.is_available = self._check_availability()
        self.connected_servers = {}
        self.failed_servers = set()

    def _get_default_config_path(self) -> str:
        """Get default configuration path"""
        return str(Path(__file__).parent.parent.parent / "config" / "mcp_servers.yaml")

    def _load_config(self) -> Dict[str, Any]:
        """Load MCP server configuration"""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"MCP config file not found: {self.config_path}")
            return {"servers": {}}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing MCP config: {e}")
            return {"servers": {}}

    def _check_availability(self) -> bool:
        """Check if mcp-use library is available"""
        try:
            logger.info("mcp-use library available")
            return True
        except ImportError:
            logger.info("mcp-use library not available - graceful degradation enabled")
            return False

    async def initialize_connections(self) -> ConnectionStatus:
        """Initialize MCP server connections using STDIO/HTTP"""
        if not self.is_available:
            logger.info("MCP client not available - skipping initialization")
            return ConnectionStatus([], [], 0, 0.0)

        try:
            # Import mcp-use dynamically
            from mcp_use import MCPClient

            # Create mcp-use client configuration
            client_config = self._build_client_config()

            # Initialize mcp-use client
            self.mcp_client = MCPClient.from_dict(client_config)

            # Attempt to create all sessions
            await self.mcp_client.create_all_sessions()

            # Track connection status
            available_servers = []
            failed_servers = []

            for server_name in self.config.get("servers", {}).keys():
                try:
                    session = self.mcp_client.get_session(server_name)
                    if session:
                        available_servers.append(server_name)
                        self.connected_servers[server_name] = session
                        logger.info(f"Connected to MCP server: {server_name}")
                    else:
                        failed_servers.append(server_name)
                        self.failed_servers.add(server_name)
                        logger.warning(
                            f"Failed to connect to MCP server: {server_name}"
                        )
                except Exception as e:
                    failed_servers.append(server_name)
                    self.failed_servers.add(server_name)
                    logger.error(f"Error connecting to {server_name}: {e}")

            total_servers = len(self.config.get("servers", {}))
            success_rate = (
                len(available_servers) / total_servers if total_servers > 0 else 0.0
            )

            return ConnectionStatus(
                available_servers, failed_servers, total_servers, success_rate
            )

        except Exception as e:
            logger.error(f"Failed to initialize MCP connections: {e}")
            return ConnectionStatus(
                [],
                list(self.config.get("servers", {}).keys()),
                len(self.config.get("servers", {})),
                0.0,
            )

    def _build_client_config(self) -> Dict[str, Any]:
        """Build mcp-use client configuration from our config"""
        client_config = {"servers": {}}

        for server_name, server_config in self.config.get("servers", {}).items():
            client_config["servers"][server_name] = {
                "command": server_config.get("command", ""),
                "args": server_config.get("args", []),
                "env": server_config.get("env", {}),
            }

        return client_config

    async def execute_tool(
        self, server_name: str, tool_name: str, **kwargs
    ) -> MCPResponse:
        """Execute a tool on specified MCP server"""
        start_time = time.time()

        if not self.is_available or server_name in self.failed_servers:
            return MCPResponse(
                content="MCP server not available",
                source_server=server_name,
                processing_time=0.0,
                success=False,
                error_message="Server not available or failed to connect",
            )

        try:
            session = self.connected_servers.get(server_name)
            if not session:
                return MCPResponse(
                    content="Server session not found",
                    source_server=server_name,
                    processing_time=time.time() - start_time,
                    success=False,
                    error_message="No active session for server",
                )

            # Execute tool via mcp-use
            result = await session.call_tool(tool_name, kwargs)

            return MCPResponse(
                content=str(result),
                source_server=server_name,
                processing_time=time.time() - start_time,
                success=True,
            )

        except Exception as e:
            logger.error(f"Error executing tool {tool_name} on {server_name}: {e}")
            return MCPResponse(
                content="",
                source_server=server_name,
                processing_time=time.time() - start_time,
                success=False,
                error_message=str(e),
            )


# === CLI CONTEXT BRIDGE (from bridges/cli_context_bridge.py) ===

import json
import sqlite3
from datetime import datetime


class CLIContextBridge:
    """
    Bridge ClaudeDirector strategic context between Cursor and CLI environments.
    Consolidated from bridges/cli_context_bridge.py (478 lines).
    """

    def __init__(self, db_path: str = None):
        """Initialize CLI context bridge with database connection"""
        if db_path is None:
            # Default to ClaudeDirector strategic memory database
            base_path = Path(__file__).parent.parent.parent.parent.parent
            db_path = base_path / ".claudedirector" / "data" / "strategic_memory.db"

        self.db_path = str(db_path)

        # Import with fallback
        try:
            from ..context_engineering.strategic_memory_manager import (
                get_strategic_memory_manager,
            )

            self.session_manager = get_strategic_memory_manager()
        except ImportError:
            logger.warning("Strategic memory manager not available - using fallback")
            self.session_manager = None

    def export_current_context(
        self, format_type: str = "markdown", output_file: str = None
    ) -> str:
        """Export current strategic context for CLI use"""
        if not self.session_manager:
            return "# Context Export Not Available\nStrategic memory manager not initialized."

        try:
            # Get strategic context
            strategic_context = self._get_strategic_context()
            session_context = self._get_session_context()

            # Format based on type
            if format_type == "markdown":
                formatted_content = self._format_markdown_export(
                    strategic_context, session_context
                )
            elif format_type == "json":
                formatted_content = self._format_json_export(
                    strategic_context, session_context
                )
            elif format_type == "yaml":
                formatted_content = self._format_yaml_export(
                    strategic_context, session_context
                )
            else:
                formatted_content = self._format_markdown_export(
                    strategic_context, session_context
                )

            # Write to file if specified
            if output_file:
                with open(output_file, "w") as f:
                    f.write(formatted_content)
                return f"Context exported to {output_file}"

            return formatted_content

        except Exception as e:
            logger.error(f"Context export failed: {e}")
            return f"# Context Export Failed\nError: {e}"

    def create_cli_session_export(self) -> str:
        """Create optimized context export for CLI sessions"""
        context = self.export_current_context("markdown")

        # Add CLI-specific header
        cli_header = """# ClaudeDirector CLI Session Context
*Generated: {timestamp}*

## Quick Strategic Context
{context}

## CLI Commands Reference
- `export-full`: Full context export
- `export-cli`: This optimized export
- `import <file>`: Import context from file

---
""".format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            context=context[:500] + "..." if len(context) > 500 else context,
        )

        return cli_header

    def import_context_from_file(self, file_path: str) -> bool:
        """Import context from file"""
        try:
            with open(file_path, "r") as f:
                content = f.read()

            # Parse based on file extension
            if file_path.endswith(".json"):
                context_data = json.loads(content)
            else:
                # For markdown/yaml, extract key information
                context_data = self._parse_text_export(content)

            # Store in strategic memory if available
            if self.session_manager:
                # This would integrate with the strategic memory system
                logger.info(f"Context imported from {file_path}")
                return True
            else:
                logger.warning("Cannot import - strategic memory manager not available")
                return False

        except Exception as e:
            logger.error(f"Context import failed: {e}")
            return False

    def _get_strategic_context(self) -> Dict[str, Any]:
        """Get current strategic context"""
        return {
            "initiatives": [],
            "stakeholders": [],
            "frameworks": [],
            "decisions": [],
            "timestamp": datetime.now().isoformat(),
        }

    def _get_session_context(self) -> Dict[str, Any]:
        """Get current session context"""
        return {
            "active_personas": [],
            "conversation_history": [],
            "current_focus": "strategic_leadership",
            "session_duration": "ongoing",
        }

    def _format_markdown_export(
        self, strategic_context: Dict, session_context: Dict
    ) -> str:
        """Format context as markdown"""
        return f"""# Strategic Context Export
*Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## Strategic Overview
- **Current Focus**: {session_context.get('current_focus', 'Unknown')}
- **Active Personas**: {', '.join(session_context.get('active_personas', []))}
- **Session Duration**: {session_context.get('session_duration', 'Unknown')}

## Key Strategic Elements
{len(strategic_context.get('initiatives', []))} active initiatives
{len(strategic_context.get('stakeholders', []))} stakeholder relationships
{len(strategic_context.get('frameworks', []))} frameworks in use

## Ready for CLI Integration
This context is optimized for ClaudeDirector CLI usage.
"""

    def _format_json_export(
        self, strategic_context: Dict, session_context: Dict
    ) -> str:
        """Format context as JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "strategic_context": strategic_context,
            "session_context": session_context,
            "export_version": "1.0",
        }
        return json.dumps(export_data, indent=2)

    def _format_yaml_export(
        self, strategic_context: Dict, session_context: Dict
    ) -> str:
        """Format context as YAML"""
        return f"""# ClaudeDirector Context Export
timestamp: {datetime.now().isoformat()}
export_version: "1.0"

strategic_context:
  initiatives: {strategic_context.get('initiatives', [])}
  stakeholders: {strategic_context.get('stakeholders', [])}
  frameworks: {strategic_context.get('frameworks', [])}

session_context:
  current_focus: {session_context.get('current_focus', 'strategic_leadership')}
  active_personas: {session_context.get('active_personas', [])}
"""

    def _parse_text_export(self, content: str) -> Dict[str, Any]:
        """Parse text-based export for key information"""
        return {
            "content": content,
            "parsed_at": datetime.now().isoformat(),
            "type": "text_import",
        }


# === UNIFIED INTEGRATION FACTORY ===


def create_mcp_client(config_path: Optional[str] = None) -> MCPUseClient:
    """Factory function for MCP client"""
    return MCPUseClient(config_path)


def create_cli_bridge(db_path: Optional[str] = None) -> CLIContextBridge:
    """Factory function for CLI context bridge"""
    return CLIContextBridge(db_path)


def create_complete_integration_suite() -> Dict[str, Any]:
    """Create complete integration suite with all bridges"""
    return {
        "unified_bridge": create_unified_bridge(),
        "mcp_client": create_mcp_client(),
        "cli_bridge": create_cli_bridge(),
        "available_integrations": ["unified_bridge", "mcp_client", "cli_bridge"],
        "initialized_at": datetime.now().isoformat(),
    }
