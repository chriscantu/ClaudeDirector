"""
Persona Chat Integration

Bridge between persona framework and P2.1 Executive Communication.
Enables natural language interaction with executive reporting and alerts.
"""

from .chat_interface import PersonaChatInterface
from .conversation_formatters import ConversationFormatter
from .persona_bridge import PersonaP2Bridge

__version__ = "2.1.0"
__author__ = "ClaudeDirector Team"

__all__ = [
    "PersonaChatInterface",
    "ConversationFormatter",
    "PersonaP2Bridge"
]
