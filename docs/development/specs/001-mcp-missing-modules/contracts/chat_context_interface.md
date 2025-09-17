# Interface Contract: ChatContextManager
# Spec-Kit Compliance: Detailed interface specification for implementation clarity

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, field
import time

# ============================================================================
# INTERFACE CONTRACTS - ChatContextManager Module
# ============================================================================


class ContextType(Enum):
    """Context types supported by ChatContextManager"""

    CHAT_SESSION = "chat_session"
    STRATEGIC_CONTEXT = "strategic_context"
    PERSONA_CONTEXT = "persona_context"
    MCP_ENHANCED = "mcp_enhanced"
    FRAMEWORK_CONTEXT = "framework_context"
    STAKEHOLDER_CONTEXT = "stakeholder_context"


@dataclass
class ChatContext:
    """Context structure for chat management operations"""

    context_type: ContextType
    session_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Context lifecycle
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None

    # Context relationships
    parent_context_id: Optional[str] = None
    child_context_ids: List[str] = field(default_factory=list)


@dataclass
class ContextOperation:
    """Operation structure for context management requests"""

    operation_type: str  # create, read, update, delete, merge
    context_id: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = None
    operation_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextResponse:
    """Standardized response for all context operations"""

    success: bool
    context: Optional[ChatContext] = None
    contexts: Optional[List[ChatContext]] = None
    error_message: Optional[str] = None
    operation_metadata: Dict[str, Any] = field(default_factory=dict)

    # Response metrics
    processing_time_ms: Optional[float] = None
    context_count: Optional[int] = None
    cache_hit: bool = False


class ChatContextInterface(ABC):
    """
    Abstract interface for ChatContextManager

    Defines the contract that ChatContextManager must implement
    to ensure consistent behavior and testability.
    """

    @abstractmethod
    def create_chat_context(
        self,
        context_type: ContextType,
        session_id: Optional[str] = None,
        initial_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> ContextResponse:
        """
        Create a new chat context

        Args:
            context_type: Type of context to create
            session_id: Optional existing session ID, generates new if None
            initial_data: Optional initial context data
            **kwargs: Additional context creation parameters

        Returns:
            ContextResponse with created context or error details
        """
        pass

    @abstractmethod
    def get_chat_context(self, context_id: str) -> ContextResponse:
        """
        Retrieve a specific chat context by ID

        Args:
            context_id: Unique context identifier

        Returns:
            ContextResponse with context data or error details
        """
        pass

    @abstractmethod
    def get_enhanced_context(
        self, session_id: str, context_types: Optional[List[ContextType]] = None
    ) -> ContextResponse:
        """
        Retrieve enhanced context using existing context engine

        Args:
            session_id: Session identifier
            context_types: Optional filter for specific context types

        Returns:
            ContextResponse with assembled enhanced context
        """
        pass

    @abstractmethod
    def update_chat_context(
        self,
        context_id: str,
        updates: Dict[str, Any],
        merge_strategy: str = "deep_merge",
    ) -> ContextResponse:
        """
        Update existing chat context

        Args:
            context_id: Context identifier to update
            updates: Data to update in context
            merge_strategy: How to merge updates (replace, shallow_merge, deep_merge)

        Returns:
            ContextResponse with updated context or error details
        """
        pass

    @abstractmethod
    def delete_chat_context(self, context_id: str) -> ContextResponse:
        """
        Delete a chat context

        Args:
            context_id: Context identifier to delete

        Returns:
            ContextResponse indicating deletion success/failure
        """
        pass

    @abstractmethod
    def list_session_contexts(
        self, session_id: str, context_types: Optional[List[ContextType]] = None
    ) -> ContextResponse:
        """
        List all contexts for a session

        Args:
            session_id: Session identifier
            context_types: Optional filter for specific context types

        Returns:
            ContextResponse with list of contexts
        """
        pass


# ============================================================================
# INTEGRATION MAPPING SPECIFICATIONS
# ============================================================================


class ExistingInfrastructureMapping:
    """
    Specification for how ChatContextManager integrates with existing infrastructure

    BLOAT_PREVENTION_SYSTEM.md Compliance: Zero duplication through adapter pattern
    """

    # ConversationManager Integration
    CONVERSATION_MANAGER_METHODS = {
        "start_conversation_session": {
            "maps_to": "create_chat_context",
            "parameter_mapping": {
                "session_id": "Generated or provided session_id",
                "context": "Converted to ChatContext.data",
            },
            "return_mapping": {"session_id": "ChatContext.session_id"},
        },
        "capture_conversation_turn": {
            "maps_to": "update_chat_context",
            "parameter_mapping": {
                "session_id": "ChatContext.session_id",
                "user_input": "ChatContext.data['conversation_turns'][-1]['user_input']",
                "response": "ChatContext.data['conversation_turns'][-1]['response']",
                "persona_used": "ChatContext.metadata['persona_used']",
                "context": "Merged into ChatContext.data",
            },
        },
    }

    # SessionManager Integration (from ai_intelligence/framework_detector.py)
    SESSION_MANAGER_METHODS = {
        "start_session": {
            "maps_to": "create_chat_context with FRAMEWORK_CONTEXT type",
            "parameter_mapping": {
                "session_type": "Converted to ContextType enum",
            },
            "return_mapping": {"session_id": "ChatContext.session_id"},
        },
        "get_session_context": {
            "maps_to": "get_chat_context",
            "parameter_mapping": {"current_session_id": "context_id parameter"},
            "return_mapping": {"ConversationContext": "Converted to ChatContext"},
        },
        "update_context": {
            "maps_to": "update_chat_context",
            "parameter_mapping": {"**kwargs": "Converted to updates Dict[str, Any]"},
        },
    }

    # AdvancedContextEngine Integration
    ADVANCED_CONTEXT_ENGINE_METHODS = {
        "conversation_layer": {
            "usage": "Retrieved via get_enhanced_context for STRATEGIC_CONTEXT",
            "integration": "ChatContext.data['conversation_layer_data']",
        },
        "strategic_layer": {
            "usage": "Retrieved via get_enhanced_context for STRATEGIC_CONTEXT",
            "integration": "ChatContext.data['strategic_layer_data']",
        },
        "stakeholder_layer": {
            "usage": "Retrieved via get_enhanced_context for STAKEHOLDER_CONTEXT",
            "integration": "ChatContext.data['stakeholder_layer_data']",
        },
        "learning_layer": {
            "usage": "Retrieved via get_enhanced_context for persona learning",
            "integration": "ChatContext.data['learning_layer_data']",
        },
        "organizational_layer": {
            "usage": "Retrieved via get_enhanced_context for org context",
            "integration": "ChatContext.data['organizational_layer_data']",
        },
    }

    # Configuration Integration
    CONFIG_MAPPING = {
        "conversation_manager_config": {
            "session_timeout": "config.get('session_timeout_seconds', 3600)",
            "max_context_size": "config.get('max_context_size', 10000)",
        },
        "session_manager_config": {
            "default_session_type": "config.get('default_session_type', 'strategic')"
        },
        "advanced_context_engine_config": {
            "conversation": "config.get('conversation', {})",
            "strategic": "config.get('strategic', {})",
            "stakeholder": "config.get('stakeholder', {})",
            "learning": "config.get('learning', {})",
            "organizational": "config.get('organizational', {})",
        },
    }


# ============================================================================
# ERROR HANDLING & GRACEFUL DEGRADATION
# ============================================================================


class GracefulDegradationStrategy:
    """
    Specification for handling failures in existing infrastructure

    Ensures ChatContextManager remains functional even if dependencies fail
    """

    FALLBACK_BEHAVIORS = {
        "ConversationManager_unavailable": {
            "strategy": "Direct session management with simplified context",
            "limitations": "No persona tracking or conversation turn capture",
            "user_notification": "Conversation management limited - persona features unavailable",
        },
        "SessionManager_unavailable": {
            "strategy": "Generate UUIDs for session management",
            "limitations": "No framework detection or conversation memory",
            "user_notification": "Framework detection unavailable",
        },
        "AdvancedContextEngine_unavailable": {
            "strategy": "Basic context storage without multi-layer intelligence",
            "limitations": "No strategic/stakeholder/learning layer integration",
            "user_notification": "Enhanced context features unavailable",
        },
    }

    ERROR_RECOVERY = {
        "import_failures": "Conditional imports with None fallbacks",
        "initialization_failures": "Partial initialization with reduced context types",
        "runtime_failures": "Context isolation - failures don't cascade across contexts",
    }


# ============================================================================
# CONTEXT LIFECYCLE MANAGEMENT
# ============================================================================


class ContextLifecycleSpecification:
    """Specification for context lifecycle management"""

    LIFECYCLE_STAGES = {
        "creation": {
            "triggers": ["create_chat_context", "session start", "persona activation"],
            "actions": [
                "assign unique ID",
                "set timestamps",
                "initialize data structure",
            ],
            "validations": [
                "context_type valid",
                "session_id format",
                "data structure valid",
            ],
        },
        "active": {
            "triggers": [
                "context updates",
                "data retrieval",
                "enhanced context assembly",
            ],
            "actions": ["update timestamps", "merge data", "maintain relationships"],
            "validations": ["context exists", "not expired", "data integrity"],
        },
        "expiration": {
            "triggers": ["timeout reached", "session ended", "explicit deletion"],
            "actions": ["cleanup data", "notify dependents", "update relationships"],
            "validations": ["safe to delete", "no active dependencies"],
        },
    }

    CONTEXT_RELATIONSHIPS = {
        "parent_child": "Strategic context can have multiple chat session children",
        "sibling": "Multiple persona contexts can exist for same session",
        "dependency": "MCP enhanced contexts depend on base chat contexts",
    }


# ============================================================================
# PERFORMANCE SPECIFICATIONS
# ============================================================================


class PerformanceRequirements:
    """Performance targets and monitoring specifications"""

    RESPONSE_TIME_TARGETS = {
        "create_chat_context": "< 50ms for simple contexts",
        "get_chat_context": "< 25ms for cached contexts",
        "get_enhanced_context": "< 200ms with full multi-layer assembly",
        "update_chat_context": "< 75ms for typical updates",
        "delete_chat_context": "< 25ms with cleanup",
    }

    MEMORY_USAGE_TARGETS = {
        "context_overhead": "< 1KB per basic context",
        "enhanced_context_overhead": "< 10KB per enhanced context",
        "total_context_cache": "< 50MB across all active sessions",
    }

    CONCURRENCY_TARGETS = {
        "concurrent_contexts": "1000+ active contexts without performance degradation",
        "context_updates_per_second": "100+ updates without blocking",
        "context_retrieval_rate": "500+ retrievals per second",
    }
