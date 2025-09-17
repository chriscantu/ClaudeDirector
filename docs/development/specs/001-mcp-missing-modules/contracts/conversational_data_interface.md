# Interface Contract: ConversationalDataManager
# Spec-Kit Compliance: Detailed interface specification for implementation clarity

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, field

# ============================================================================
# INTERFACE CONTRACTS - ConversationalDataManager Module
# ============================================================================


class QueryType(Enum):
    """Query types supported by ConversationalDataManager"""

    CONVERSATION_HISTORY = "conversation_history"
    STRATEGIC_CONTEXT = "strategic_context"
    SESSION_DATA = "session_data"
    TOPIC_SEARCH = "topic_search"
    FRAMEWORK_USAGE = "framework_usage"


@dataclass
class ConversationalQuery:
    """Query structure for conversational data requests"""

    query_type: QueryType
    session_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    # Query-specific parameters
    limit: Optional[int] = None
    offset: Optional[int] = None
    time_range: Optional[Dict[str, Any]] = None
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataResponse:
    """Standardized response structure for all data operations"""

    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    query_metadata: Dict[str, Any] = field(default_factory=dict)

    # Response metrics
    processing_time_ms: Optional[float] = None
    result_count: Optional[int] = None
    has_more_results: bool = False


class ConversationalDataInterface(ABC):
    """
    Abstract interface for ConversationalDataManager

    Defines the contract that ConversationalDataManager must implement
    to ensure consistent behavior and testability.
    """

    @abstractmethod
    def query_conversation_data(self, query: ConversationalQuery) -> DataResponse:
        """
        Execute a conversational data query

        Args:
            query: ConversationalQuery with type, session_id, and parameters

        Returns:
            DataResponse with success status, data, and metadata
        """
        pass

    @abstractmethod
    def store_conversation_turn(
        self,
        session_id: str,
        user_input: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DataResponse:
        """
        Store a conversation turn for future retrieval

        Args:
            session_id: Unique session identifier
            user_input: User's input message
            assistant_response: Assistant's response
            metadata: Optional metadata (personas, frameworks, etc.)

        Returns:
            DataResponse indicating storage success/failure
        """
        pass

    @abstractmethod
    def get_session_context(self, session_id: str) -> DataResponse:
        """
        Retrieve comprehensive context for a session

        Args:
            session_id: Unique session identifier

        Returns:
            DataResponse with session context data
        """
        pass

    @abstractmethod
    def search_conversations(
        self, search_term: str, session_id: Optional[str] = None, limit: int = 10
    ) -> DataResponse:
        """
        Search conversations by content or metadata

        Args:
            search_term: Text to search for
            session_id: Optional session filter
            limit: Maximum results to return

        Returns:
            DataResponse with matching conversations
        """
        pass


# ============================================================================
# INTEGRATION MAPPING SPECIFICATIONS
# ============================================================================


class ExistingInfrastructureMapping:
    """
    Specification for how ConversationalDataManager integrates with existing infrastructure

    BLOAT_PREVENTION_SYSTEM.md Compliance: Zero duplication through facade pattern
    """

    # ConversationLayerMemory Integration
    CONVERSATION_LAYER_METHODS = {
        "store_conversation_context": {
            "maps_to": "store_conversation_turn",
            "parameter_mapping": {
                "session_data": "Constructed from session_id, user_input, assistant_response",
                "session_data.query": "user_input",
                "session_data.response": "assistant_response",
                "session_data.session_id": "session_id",
                "session_data.timestamp": "time.time()",
            },
        },
        "retrieve_relevant_context": {
            "maps_to": "query_conversation_data + get_session_context",
            "parameter_mapping": {
                "current_query": "ConversationalQuery.parameters['search_term']",
                "session_id": "ConversationalQuery.session_id",
            },
        },
    }

    # StrategicMemoryManager Integration
    STRATEGIC_MEMORY_METHODS = {
        "ensure_db_exists": {
            "usage": "Called during ConversationalDataManager.__init__()",
            "error_handling": "Graceful degradation if database unavailable",
        },
        "current_session_id": {
            "usage": "Retrieved for session context operations",
            "fallback": "Generate temporary session ID if None",
        },
    }

    # Configuration Integration
    CONFIG_MAPPING = {
        "conversation_layer_config": {
            "retention_days": "config.get('retention_days', 90)",
            "max_conversations_per_session": "config.get('max_conversations', 1000)",
        },
        "strategic_memory_config": {
            "db_path": "config.get('db_path', None)",
            "enable_performance": "config.get('enable_performance', True)",
            "session_backup_interval": "config.get('session_backup_interval', 300)",
        },
    }


# ============================================================================
# ERROR HANDLING & GRACEFUL DEGRADATION
# ============================================================================


class GracefulDegradationStrategy:
    """
    Specification for handling failures in existing infrastructure

    Ensures ConversationalDataManager remains functional even if dependencies fail
    """

    FALLBACK_BEHAVIORS = {
        "ConversationLayerMemory_unavailable": {
            "strategy": "In-memory conversation storage",
            "limitations": "No persistence across restarts",
            "user_notification": "Limited conversation history - persistence unavailable",
        },
        "StrategicMemoryManager_unavailable": {
            "strategy": "Session-only memory",
            "limitations": "No cross-session strategic context",
            "user_notification": "Strategic context limited to current session",
        },
        "Database_connection_failed": {
            "strategy": "Memory-only operation",
            "limitations": "No data persistence",
            "user_notification": "Operating in memory-only mode",
        },
    }

    ERROR_RECOVERY = {
        "import_failures": "Try-except blocks with specific fallback imports",
        "initialization_failures": "Partial initialization with reduced functionality",
        "runtime_failures": "Circuit breaker pattern with automatic retry",
    }


# ============================================================================
# PERFORMANCE SPECIFICATIONS
# ============================================================================


class PerformanceRequirements:
    """Performance targets and monitoring specifications"""

    RESPONSE_TIME_TARGETS = {
        "query_conversation_data": "< 100ms for typical queries",
        "store_conversation_turn": "< 50ms for single turn",
        "get_session_context": "< 200ms with full context assembly",
        "search_conversations": "< 300ms for text search",
    }

    MEMORY_USAGE_TARGETS = {
        "max_memory_per_session": "< 10MB",
        "conversation_cache_size": "< 100MB total",
        "graceful_degradation_overhead": "< 5MB additional",
    }

    SCALABILITY_TARGETS = {
        "concurrent_sessions": "100+ without performance degradation",
        "conversation_history_size": "10,000+ turns per session",
        "search_index_size": "1M+ conversation turns",
    }
