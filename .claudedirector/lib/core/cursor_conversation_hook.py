#!/usr/bin/env python3
"""
Cursor Conversation Hook
Automatic conversation capture integration for ClaudeDirector
"""

import re
from datetime import datetime
from typing import Dict, List, Any

from ..personas.conversation_manager import ConversationManager


class CursorConversationHook:
    """
    Automatic conversation capture for Cursor integration
    Captures strategic conversations in real-time without manual intervention
    """

    def __init__(self, auto_start: bool = True):
        """Initialize conversation hook with automatic session management"""
        self.conversation_manager = ConversationManager()
        self.auto_start = auto_start
        self.session_active = False
        self.persona_pattern = re.compile(r"🎯|📊|🎨|💼|🏗️|📈|💰|🤝|⚖️|🔒")
        self.strategic_keywords = [
            "platform",
            "strategy",
            "stakeholder",
            "executive",
            "investment",
            "framework",
            "architecture",
            "organization",
            "leadership",
            "culture",
        ]

    def capture_conversation_turn(
        self, user_input: str, assistant_response: str
    ) -> bool:
        """
        Automatically capture conversation turn if strategic content is detected

        Args:
            user_input: User's message
            assistant_response: Assistant's full response

        Returns:
            True if conversation was captured
        """
        try:
            # Detect if this is a strategic conversation
            if not self._is_strategic_conversation(user_input, assistant_response):
                return False

            # Auto-start session if needed
            if not self.session_active and self.auto_start:
                self._start_strategic_session()

            # Extract personas from response
            personas_activated = self._extract_personas(assistant_response)

            # Generate metadata
            metadata = self._generate_conversation_metadata(
                user_input, assistant_response
            )

            # Capture the turn
            self.conversation_manager.capture_conversation_turn(
                user_input=user_input,
                assistant_response=assistant_response,
                personas_activated=personas_activated,
                context_metadata=metadata,
            )

            print(
                f"💾 Strategic conversation captured ({len(personas_activated)} personas)"
            )
            return True

        except Exception as e:
            print(f"⚠️ Conversation capture failed: {e}")
            return False

    def _is_strategic_conversation(
        self, user_input: str, assistant_response: str
    ) -> bool:
        """Detect if conversation contains strategic content"""
        combined_text = f"{user_input} {assistant_response}".lower()

        # Check for persona headers
        if self.persona_pattern.search(assistant_response):
            return True

        # Check for strategic keywords
        strategic_matches = sum(
            1 for keyword in self.strategic_keywords if keyword in combined_text
        )

        # Require at least 2 strategic keywords for capture
        return strategic_matches >= 2

    def _extract_personas(self, assistant_response: str) -> List[str]:
        """Extract activated personas from response"""
        personas = []

        # Pattern matches for persona headers
        persona_patterns = {
            "🎯.*Diego.*Engineering Leadership": "diego",
            "📊.*Camille.*Strategic Technology": "camille",
            "🎨.*Rachel.*Design Systems Strategy": "rachel",
            "💼.*Alvaro.*Platform Investment": "alvaro",
            "🏗️.*Martin.*Platform Architecture": "martin",
            "📈.*Marcus.*Platform Adoption": "marcus",
            "💰.*David.*Financial Planning": "david",
            "🤝.*Sofia.*Vendor Strategy": "sofia",
            "⚖️.*Elena.*Compliance Strategy": "elena",
        }

        for pattern, persona in persona_patterns.items():
            if re.search(pattern, assistant_response):
                personas.append(persona)

        return personas

    def _generate_conversation_metadata(
        self, user_input: str, assistant_response: str
    ) -> Dict[str, Any]:
        """Generate metadata for conversation context"""
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "capture_method": "automatic",
            "conversation_type": self._classify_conversation_type(user_input),
            "strategic_complexity": self._estimate_complexity(assistant_response),
            "framework_detected": self._detect_frameworks(assistant_response),
            "cursor_integration": True,
        }

        return metadata

    def _classify_conversation_type(self, user_input: str) -> str:
        """Classify the type of strategic conversation"""
        text = user_input.lower()

        if any(word in text for word in ["budget", "roi", "investment", "cost"]):
            return "financial_strategy"
        elif any(
            word in text for word in ["stakeholder", "executive", "vp", "meeting"]
        ):
            return "stakeholder_engagement"
        elif any(word in text for word in ["architecture", "platform", "technical"]):
            return "technical_strategy"
        elif any(word in text for word in ["team", "organization", "culture"]):
            return "organizational_strategy"
        else:
            return "general_strategic"

    def _estimate_complexity(self, assistant_response: str) -> float:
        """Estimate conversation complexity score"""
        complexity_indicators = [
            "framework",
            "methodology",
            "analysis",
            "assessment",
            "strategic",
            "systematic",
            "comprehensive",
        ]

        text = assistant_response.lower()
        matches = sum(1 for indicator in complexity_indicators if indicator in text)

        # Response length factor
        length_factor = min(len(assistant_response) / 1000, 1.0)

        return min((matches * 0.2) + length_factor, 1.0)

    def _detect_frameworks(self, assistant_response: str) -> List[str]:
        """Detect strategic frameworks mentioned in response"""
        frameworks = []

        framework_patterns = [
            "Team Topologies",
            "Capital Allocation",
            "Crucial Conversations",
            "Strategic Framework",
            "WRAP Framework",
            "Systems Thinking",
            "Accelerate Performance",
            "Platform Strategy",
        ]

        for framework in framework_patterns:
            if framework.lower() in assistant_response.lower():
                frameworks.append(framework)

        return frameworks

    def _start_strategic_session(self) -> None:
        """Start a new strategic session"""
        try:
            session_id = self.conversation_manager.start_conversation_session(
                "strategic"
            )
            self.session_active = True
            print(f"🚀 Strategic session auto-started: {session_id[:8]}...")
        except Exception as e:
            print(f"⚠️ Session auto-start failed: {e}")

    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        if self.session_active:
            return self.conversation_manager.get_session_status()
        else:
            return {"status": "no_active_session", "auto_start": self.auto_start}

    def end_session(self) -> bool:
        """End current session"""
        if self.session_active:
            success = self.conversation_manager.end_conversation_session()
            self.session_active = False
            return success
        return True


# Global conversation hook instance for automatic integration
_conversation_hook = None


def get_conversation_hook() -> CursorConversationHook:
    """Get global conversation hook instance"""
    global _conversation_hook
    if _conversation_hook is None:
        _conversation_hook = CursorConversationHook()
    return _conversation_hook


def auto_capture_conversation(user_input: str, assistant_response: str) -> bool:
    """
    Convenience function for automatic conversation capture

    Args:
        user_input: User's message
        assistant_response: Assistant's response

    Returns:
        True if conversation was captured
    """
    hook = get_conversation_hook()
    return hook.capture_conversation_turn(user_input, assistant_response)


if __name__ == "__main__":
    # Test the conversation hook
    hook = CursorConversationHook()

    # Test strategic conversation detection
    test_user = "Camille, what was our last conversation on platform culture?"
    test_response = """📊 Camille | Strategic Technology

    Looking at our strategic frameworks, platform culture discussions typically focus on...
    """

    captured = hook.capture_conversation_turn(test_user, test_response)
    print(f"Test capture result: {captured}")

    status = hook.get_session_status()
    print(f"Session status: {status}")
