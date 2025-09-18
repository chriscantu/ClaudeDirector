# Task 002: Chat Context Manager Implementation

## Task Overview
**ID**: TASK-002
**Component**: `chat_context_manager.py`
**Priority**: P0 (MCP integration completion)
**Estimated Effort**: 2-3 hours

## Context7 Pattern Applied
**Pattern**: **Context Manager Pattern** + **Adapter Pattern**
**Rationale**: Provides MCP-specific context management while adapting existing persona conversation infrastructure

## BLOAT_PREVENTION_SYSTEM.md Compliance

### ✅ Existing Infrastructure Analysis
**REUSE EXISTING (DRY Compliance)**:
```python
# EXISTING: .claudedirector/lib/personas/conversation_manager.py
class ConversationManager(BaseManager):
    def start_conversation_session(session_id: str, context: Dict[str, Any]) -> str
    def capture_conversation_turn(...) -> bool

# EXISTING: .claudedirector/lib/ai_intelligence/framework_detector.py
class SessionManager:
    def start_session(session_type: str = "strategic") -> str
    def get_session_context() -> Optional[ConversationContext]
    def update_context(**kwargs) -> None

# EXISTING: .claudedirector/lib/context_engineering/advanced_context_engine.py
class AdvancedContextEngine:
    def __init__(config: Optional[Dict[str, Any]] = None)
    # Multi-layered strategic context with intelligent assembly
```

### 🚫 PREVENT DUPLICATION
**DO NOT CREATE**:
- New session management logic (use existing SessionManager)
- New conversation tracking (use ConversationManager)
- New context assembly (use AdvancedContextEngine)

## Implementation Strategy

### Step 1: Adapter Pattern Implementation
```python
# .claudedirector/lib/mcp/chat_context_manager.py
from ..personas.conversation_manager import ConversationManager
from ..ai_intelligence.framework_detector import SessionManager, ConversationContext
from ..context_engineering.advanced_context_engine import AdvancedContextEngine

class ChatContextManager:
    """MCP-specific adapter for existing context infrastructure"""
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # REUSE: Existing infrastructure (DRY compliance)
        self.conversation_manager = ConversationManager()
        self.session_manager = SessionManager()
        self.context_engine = AdvancedContextEngine(config)
```

### Step 2: MCP-Specific Context Types
```python
class ContextType(Enum):
    CHAT_SESSION = "chat_session"
    STRATEGIC_CONTEXT = "strategic_context"
    PERSONA_CONTEXT = "persona_context"
    MCP_ENHANCED = "mcp_enhanced"

@dataclass
class ChatContext:
    context_type: ContextType
    session_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### Step 3: Context Operations
```python
class ChatContextManager:
    def create_chat_context(self, context_type: ContextType, **kwargs) -> ChatContext:
        """Create new chat context using existing infrastructure"""
        session_id = self.session_manager.start_session("mcp_chat")
        # Delegate to existing conversation manager
        self.conversation_manager.start_conversation_session(session_id, kwargs)

    def get_enhanced_context(self, session_id: str) -> Optional[ChatContext]:
        """Retrieve enhanced context using existing context engine"""
        # Leverage AdvancedContextEngine's multi-layered context

    def update_chat_context(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update context using existing session management"""
        # Delegate to existing session manager
```

## Acceptance Criteria
- [ ] Import `from .chat_context_manager import ChatContextManager` succeeds
- [ ] Zero code duplication with existing context infrastructure
- [ ] Adapter pattern provides MCP-specific interface
- [ ] Integration with existing ConversationManager, SessionManager, AdvancedContextEngine
- [ ] All P0 tests continue passing
- [ ] BLOAT_PREVENTION_SYSTEM.md compliant (reuses existing patterns)

## Dependencies
- `lib/personas/conversation_manager.py` (existing)
- `lib/ai_intelligence/framework_detector.py` (existing SessionManager)
- `lib/context_engineering/advanced_context_engine.py` (existing)
- No new dependencies required

## Testing Strategy
- Unit tests for adapter interface
- Integration tests with existing context infrastructure
- Session lifecycle tests
- P0 regression protection

## Risk Assessment
**LOW RISK**: Adapter pattern with existing infrastructure reuse
- No new session logic
- Leverages proven context management systems
- Minimal new code surface area
