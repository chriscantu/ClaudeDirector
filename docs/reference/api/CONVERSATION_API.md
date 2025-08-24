# Conversation Management API

**Strategic conversation context management and persistence.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 🔄 **Conversation Management API**

### **Conversation Manager**
```python
# .claudedirector/lib/claudedirector/core/conversation_manager.py
class ConversationManager:
    """Manage conversation state and context"""

    def __init__(self):
        self.current_session = None
        self.context_buffer = deque(maxlen=50)
        self.persona_history = []

    def start_conversation(self, user_id: str = None) -> ConversationSession:
        """Start new conversation session"""
        self.current_session = ConversationSession(
            id=self._generate_session_id(),
            user_id=user_id,
            started_at=datetime.now()
        )
        return self.current_session

    def add_interaction(self,
                       user_input: str,
                       response: str,
                       persona: str,
                       mcp_servers_used: List[str] = None,
                       frameworks_detected: List[str] = None) -> ConversationTurn:
        """Add conversation turn with metadata"""
        turn = ConversationTurn(
            user_input=user_input,
            response=response,
            persona=persona,
            mcp_servers_used=mcp_servers_used or [],
            frameworks_detected=frameworks_detected or [],
            timestamp=datetime.now()
        )

        self.context_buffer.append(turn)
        self.persona_history.append(persona)

        if self.current_session:
            self.current_session.add_turn(turn)

        return turn

    def get_context_summary(self, max_turns: int = 5) -> str:
        """Get summarized context from recent turns"""
        recent_turns = list(self.context_buffer)[-max_turns:]

        summary_parts = []
        for turn in recent_turns:
            summary_parts.append(f"User: {turn.user_input[:100]}...")
            summary_parts.append(f"{turn.persona}: {turn.response[:200]}...")

        return "\n".join(summary_parts)

    def get_persona_continuity(self) -> str:
        """Analyze persona usage patterns for continuity"""
        if len(self.persona_history) < 2:
            return "single_persona"

        if len(set(self.persona_history[-3:])) == 1:
            return "consistent_persona"
        elif len(set(self.persona_history[-3:])) > 2:
            return "multi_persona_collaboration"
        else:
            return "persona_transition"
```
