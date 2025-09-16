#!/usr/bin/env python3
"""
Conversation Hooks - Platform Integration
Conversation Persistence System Recovery

Authors: Martin | Platform Architecture + Diego | Engineering Leadership
Story: Phase B.2 - Platform Integration Hooks
Priority: P0 - BLOCKING (Platform integration)

This module provides integration hooks for capturing conversations from
different platforms (Cursor IDE and Claude.ai) and routing them to the
conversation persistence bridge.

Key Features:
- Cursor IDE integration via environment detection
- Claude.ai integration via manual trigger patterns
- Automatic session management
- Error handling and fallback mechanisms

CRITICAL: Follows PROJECT_STRUCTURE.md core/ patterns and BLOAT_PREVENTION_SYSTEM.md
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

# Import the conversation bridge (avoid duplication)
try:
    from .conversation_persistence_bridge import (
        get_conversation_bridge,
        ConversationPlatform,
    )
except ImportError:
    # Fallback for testing
    get_conversation_bridge = None
    ConversationPlatform = None


class CursorIntegrationHook:
    """
    Integration hook for Cursor IDE conversations.

    Detects Cursor environment and automatically captures strategic conversations.
    """

    def __init__(self):
        self.logger = logger.bind(component="CursorIntegrationHook")
        self.session_id = self._generate_session_id()
        self.conversation_count = 0

    def _generate_session_id(self) -> str:
        """Generate session ID based on Cursor context"""
        # Use workspace path + timestamp for session ID
        workspace = os.environ.get("CURSOR_WORKSPACE", os.getcwd())
        timestamp = int(time.time())
        return f"cursor_{Path(workspace).name}_{timestamp}"

    def is_cursor_environment(self) -> bool:
        """Detect if running in Cursor IDE environment"""
        cursor_indicators = [
            os.environ.get("CURSOR_WORKSPACE"),
            os.environ.get("CURSOR_SESSION"),
            os.path.exists(".cursor") if os.path.exists(".") else False,
            "cursor" in os.environ.get("EDITOR", "").lower(),
        ]
        return any(cursor_indicators)

    def capture_from_cursor_session(
        self,
        user_message: str,
        ai_response: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Capture conversation from Cursor IDE session"""
        if not get_conversation_bridge:
            self.logger.warning("Conversation bridge not available")
            return False

        try:
            bridge = get_conversation_bridge()

            # Add Cursor-specific context
            platform_hints = {
                "cursor": True,
                "ide": True,
                "workspace": os.environ.get("CURSOR_WORKSPACE", os.getcwd()),
                "session_count": self.conversation_count,
            }

            if context:
                platform_hints.update(context)

            success = bridge.capture_conversation(
                user_input=user_message,
                ai_response=ai_response,
                session_id=self.session_id,
                platform_hints=platform_hints,
            )

            if success:
                self.conversation_count += 1
                self.logger.debug(
                    f"Cursor conversation captured",
                    session_id=self.session_id,
                    count=self.conversation_count,
                )

            return success

        except Exception as e:
            self.logger.error(f"Failed to capture Cursor conversation: {e}")
            return False


class ClaudeIntegrationHook:
    """
    Integration hook for Claude.ai conversations.

    Provides manual trigger mechanisms and automatic detection patterns.
    """

    def __init__(self):
        self.logger = logger.bind(component="ClaudeIntegrationHook")
        self.session_id = self._generate_session_id()
        self.conversation_count = 0

    def _generate_session_id(self) -> str:
        """Generate session ID for Claude.ai"""
        timestamp = int(time.time())
        return f"claude_web_{timestamp}"

    def is_claude_environment(self) -> bool:
        """Detect if running in Claude.ai environment (limited detection)"""
        # Claude.ai detection is limited - mainly for documentation
        claude_indicators = [
            "claude" in sys.argv[0].lower() if sys.argv else False,
            os.environ.get("CLAUDE_SESSION"),
        ]
        return any(claude_indicators)

    def capture_from_claude_session(
        self,
        user_message: str,
        ai_response: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Capture conversation from Claude.ai session"""
        if not get_conversation_bridge:
            self.logger.warning("Conversation bridge not available")
            return False

        try:
            bridge = get_conversation_bridge()

            # Add Claude-specific context
            platform_hints = {
                "claude": True,
                "web": True,
                "session_count": self.conversation_count,
            }

            if context:
                platform_hints.update(context)

            success = bridge.capture_conversation(
                user_input=user_message,
                ai_response=ai_response,
                session_id=self.session_id,
                platform_hints=platform_hints,
            )

            if success:
                self.conversation_count += 1
                self.logger.debug(
                    f"Claude conversation captured",
                    session_id=self.session_id,
                    count=self.conversation_count,
                )

            return success

        except Exception as e:
            self.logger.error(f"Failed to capture Claude conversation: {e}")
            return False

    def manual_capture_trigger(self, conversation_data: Dict[str, Any]) -> bool:
        """Manual trigger for capturing Claude.ai conversations"""
        try:
            user_message = conversation_data.get("user_input", "")
            ai_response = conversation_data.get("ai_response", "")

            if not user_message or not ai_response:
                self.logger.warning("Incomplete conversation data for manual capture")
                return False

            return self.capture_from_claude_session(
                user_message, ai_response, conversation_data.get("context", {})
            )

        except Exception as e:
            self.logger.error(f"Manual capture trigger failed: {e}")
            return False


class ConversationHookManager:
    """
    Manager for all conversation hooks and platform integrations.

    Provides unified interface for conversation capture across platforms.
    """

    def __init__(self):
        self.logger = logger.bind(component="ConversationHookManager")
        self.cursor_hook = CursorIntegrationHook()
        self.claude_hook = ClaudeIntegrationHook()
        self.active_platform = self._detect_active_platform()

        self.logger.info(
            f"ConversationHookManager initialized for platform: {self.active_platform}"
        )

    def _detect_active_platform(self) -> str:
        """Detect the currently active platform"""
        if self.cursor_hook.is_cursor_environment():
            return "cursor"
        elif self.claude_hook.is_claude_environment():
            return "claude"
        else:
            return "unknown"

    def capture_conversation(
        self,
        user_input: str,
        ai_response: str,
        platform_override: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Capture conversation using appropriate platform hook.

        Args:
            user_input: User's input message
            ai_response: AI assistant's response
            platform_override: Override platform detection
            context: Additional context information

        Returns:
            True if conversation was captured successfully
        """
        platform = platform_override or self.active_platform

        try:
            if platform == "cursor":
                return self.cursor_hook.capture_from_cursor_session(
                    user_input, ai_response, context
                )
            elif platform == "claude":
                return self.claude_hook.capture_from_claude_session(
                    user_input, ai_response, context
                )
            else:
                # Try both platforms as fallback
                cursor_success = self.cursor_hook.capture_from_cursor_session(
                    user_input, ai_response, context
                )
                claude_success = self.claude_hook.capture_from_claude_session(
                    user_input, ai_response, context
                )
                return cursor_success or claude_success

        except Exception as e:
            self.logger.error(f"Failed to capture conversation: {e}")
            return False

    def get_session_info(self) -> Dict[str, Any]:
        """Get information about active sessions"""
        return {
            "active_platform": self.active_platform,
            "cursor_session": {
                "session_id": self.cursor_hook.session_id,
                "conversation_count": self.cursor_hook.conversation_count,
                "environment_detected": self.cursor_hook.is_cursor_environment(),
            },
            "claude_session": {
                "session_id": self.claude_hook.session_id,
                "conversation_count": self.claude_hook.conversation_count,
                "environment_detected": self.claude_hook.is_claude_environment(),
            },
        }


# Global hook manager instance
_hook_manager: Optional[ConversationHookManager] = None


def get_hook_manager() -> ConversationHookManager:
    """Get singleton conversation hook manager"""
    global _hook_manager
    if _hook_manager is None:
        _hook_manager = ConversationHookManager()
    return _hook_manager


def auto_capture_conversation(
    user_input: str, ai_response: str, context: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Automatic conversation capture with platform detection.

    This is the main entry point for automatic conversation capture.
    """
    try:
        manager = get_hook_manager()
        return manager.capture_conversation(user_input, ai_response, context=context)
    except Exception as e:
        logger.error(f"Auto capture failed: {e}")
        return False


def manual_capture_conversation(
    user_input: str,
    ai_response: str,
    platform: str = "claude",
    context: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Manual conversation capture for specific platform.

    Useful for Claude.ai integration where automatic detection is limited.
    """
    try:
        manager = get_hook_manager()
        return manager.capture_conversation(
            user_input, ai_response, platform_override=platform, context=context
        )
    except Exception as e:
        logger.error(f"Manual capture failed: {e}")
        return False


if __name__ == "__main__":
    # Test the conversation hooks
    manager = ConversationHookManager()

    # Test conversation capture
    test_user_input = "What's the best approach for implementing microservices?"
    test_ai_response = """🏗️ Martin | Platform Architecture

    Great question about microservices architecture! Let me break down the key considerations...

    I recommend starting with a modular monolith approach and gradually extracting services..."""

    success = manager.capture_conversation(test_user_input, test_ai_response)

    if success:
        print("✅ Test conversation hook worked successfully")
        session_info = manager.get_session_info()
        print(f"📊 Session info: {json.dumps(session_info, indent=2)}")
    else:
        print("❌ Test conversation hook failed")
