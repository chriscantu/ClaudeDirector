# Task 004: Factory Integration Implementation

## Task Overview
**ID**: TASK-004
**Component**: Factory functions for MCP module creation
**Priority**: P1 (Clean architecture completion)
**Estimated Effort**: 1 hour

## Context7 Pattern Applied
**Pattern**: **Factory Pattern** + **Dependency Injection**
**Rationale**: Provide clean factory interface for MCP module instantiation following SOLID principles

## BLOAT_PREVENTION_SYSTEM.md Compliance

### ✅ Existing Factory Pattern Analysis
**REUSE EXISTING (DRY Compliance)**:
```python
# EXISTING: .claudedirector/lib/performance/__init__.py
def get_unified_manager():
    """Legacy compatibility - return performance monitor"""

# EXISTING: Multiple factory functions already implemented
def create_mcp_response(content: str, **kwargs) -> UnifiedResponse
def create_persona_response(content: str, **kwargs) -> UnifiedResponse
def create_fallback_response(content: str, **kwargs) -> UnifiedResponse
```

### 🚫 PREVENT DUPLICATION
**DO NOT CREATE**:
- New factory base classes (use existing patterns)
- New dependency injection framework (use simple factory functions)
- New configuration management (use existing config patterns)

## Implementation Strategy

### Step 1: Simple Factory Functions
```python
# .claudedirector/lib/mcp/conversational_data_manager.py
def create_conversational_data_manager(config: Optional[Dict[str, Any]] = None) -> ConversationalDataManager:
    """
    Factory function for ConversationalDataManager creation

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured ConversationalDataManager instance
    """
    return ConversationalDataManager(config)

# .claudedirector/lib/mcp/chat_context_manager.py
def create_chat_context_manager(config: Optional[Dict[str, Any]] = None) -> ChatContextManager:
    """
    Factory function for ChatContextManager creation

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured ChatContextManager instance
    """
    return ChatContextManager(config)
```

### Step 2: Update Module __init__.py
```python
# .claudedirector/lib/mcp/__init__.py
from .conversational_data_manager import (
    ConversationalDataManager,
    ConversationalQuery,
    DataResponse,
    QueryType,
    create_conversational_data_manager,  # Factory function
)

from .chat_context_manager import (
    ChatContextManager,
    ChatContext,
    ContextType,
    create_chat_context_manager,  # Factory function
)

__all__ = [
    # Classes
    "ConversationalDataManager",
    "ChatContextManager",
    "ConversationalQuery",
    "DataResponse",
    "ChatContext",
    # Enums
    "QueryType",
    "ContextType",
    # Factory functions
    "create_conversational_data_manager",
    "create_chat_context_manager",
]
```

### Step 3: Configuration Pattern Consistency
```python
# Follow existing configuration patterns from lib/performance/
DEFAULT_MCP_CONFIG = {
    "enable_caching": True,
    "enable_performance_monitoring": True,
    "session_timeout_seconds": 3600,
    "max_context_size": 10000,
}

def create_conversational_data_manager(config: Optional[Dict[str, Any]] = None) -> ConversationalDataManager:
    """Factory with default configuration merge"""
    merged_config = {**DEFAULT_MCP_CONFIG, **(config or {})}
    return ConversationalDataManager(merged_config)
```

## Acceptance Criteria
- [ ] Factory functions follow existing patterns from `lib/performance`
- [ ] Clean instantiation interface: `create_conversational_data_manager()`
- [ ] Configuration merging with sensible defaults
- [ ] Export factory functions in module `__init__.py`
- [ ] Zero code duplication with existing factory patterns
- [ ] All P0 tests continue passing

## Dependencies
- Task 001: ConversationalDataManager implementation
- Task 002: ChatContextManager implementation
- Existing configuration patterns from `lib/performance`

## Testing Strategy
- Factory function unit tests
- Configuration merging tests
- Default behavior validation
- Import tests for factory functions

## Risk Assessment
**MINIMAL RISK**: Simple factory pattern implementation
- Follows existing proven patterns
- No complex dependency injection
- Straightforward configuration handling
- Standard factory function approach

## Success Metrics
- ✅ Clean factory interface available
- ✅ Consistent with existing project patterns
- ✅ Zero duplication with existing factory logic
- ✅ SOLID principles compliance (Factory Pattern)
