#!/usr/bin/env python3
"""
Auto Conversation Integration
Automatic integration of conversation capture with ClaudeDirector responses
"""

import sys
from pathlib import Path

# Add current package to path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from .cursor_conversation_hook import auto_capture_conversation


class ConversationInterceptor:
    """
    Intercepts ClaudeDirector responses to automatically capture conversations
    """

    def __init__(self):
        self.capture_enabled = True
        self.last_user_input = None

    def set_user_input(self, user_input: str) -> None:
        """Store user input for the next response capture"""
        self.last_user_input = user_input

    def capture_response(self, assistant_response: str) -> bool:
        """
        Capture assistant response with stored user input

        Args:
            assistant_response: The full assistant response

        Returns:
            True if conversation was captured
        """
        if not self.capture_enabled or not self.last_user_input:
            return False

        try:
            # Attempt automatic capture
            captured = auto_capture_conversation(
                user_input=self.last_user_input, assistant_response=assistant_response
            )

            # Clear stored input after capture attempt
            self.last_user_input = None

            return captured

        except Exception as e:
            print(f"⚠️ Auto-capture error: {e}")
            return False


# Global interceptor instance
_interceptor = ConversationInterceptor()


def enable_auto_capture() -> None:
    """Enable automatic conversation capture"""
    _interceptor.capture_enabled = True
    print("✅ Automatic conversation capture enabled")


def disable_auto_capture() -> None:
    """Disable automatic conversation capture"""
    _interceptor.capture_enabled = False
    print("⏸️ Automatic conversation capture disabled")


def capture_user_input(user_input: str) -> None:
    """
    Capture user input for next response
    Call this before generating assistant response
    """
    _interceptor.set_user_input(user_input)


def capture_assistant_response(assistant_response: str) -> bool:
    """
    Capture assistant response with previously stored user input
    Call this after generating assistant response

    Returns:
        True if conversation was captured
    """
    return _interceptor.capture_response(assistant_response)


def get_capture_status() -> dict:
    """Get current capture status"""
    return {
        "enabled": _interceptor.capture_enabled,
        "has_pending_input": _interceptor.last_user_input is not None,
    }


# Auto-initialization when module is imported
if __name__ != "__main__":
    # Automatically enable capture when imported as module
    enable_auto_capture()


if __name__ == "__main__":
    # Test the auto-capture system
    print("🧪 Testing Auto Conversation Integration")
    print("=" * 45)

    # Test user input capture
    test_user_input = "Martin, let's implement the permanent fix for the db first"
    capture_user_input(test_user_input)
    print(f"📝 Captured user input: {test_user_input[:50]}...")

    # Test assistant response capture
    test_assistant_response = """🏗️ Martin | Platform Architecture

    You're absolutely right on both counts. Let's tackle the permanent conversation capture fix first, then address the nested directory structure which definitely looks like architectural redundancy.
    """

    captured = capture_assistant_response(test_assistant_response)
    print(f"💾 Response capture result: {captured}")

    # Check status
    status = get_capture_status()
    print(f"📊 Capture status: {status}")
