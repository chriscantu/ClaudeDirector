#!/usr/bin/env python3
"""
Auto Conversation Integration
Automatic integration of conversation capture with ClaudeDirector responses
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add current package to path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from .cursor_conversation_hook import auto_capture_conversation

# Phase C: Import existing verification systems (DRY compliance)
try:
    from ..context_engineering.conversation_layer import ConversationLayerMemory
    from ..context_engineering.clarity_analyzer import ConversationAnalyzer

    VERIFICATION_AVAILABLE = True
except ImportError:
    VERIFICATION_AVAILABLE = False


class ConversationInterceptor:
    """
    Intercepts ClaudeDirector responses to automatically capture conversations
    Phase C Enhancement: Real-time verification using existing systems (BLOAT_PREVENTION_SYSTEM.md compliant)
    """

    def __init__(self):
        self.capture_enabled = True
        self.last_user_input = None

        # Phase C: Initialize verification systems using existing infrastructure (DRY compliance)
        self.verification_enabled = VERIFICATION_AVAILABLE
        self.conversation_analyzer = (
            ConversationAnalyzer() if VERIFICATION_AVAILABLE else None
        )
        self.conversation_layer = (
            ConversationLayerMemory() if VERIFICATION_AVAILABLE else None
        )

        # Phase C: Capture statistics using existing patterns
        self.capture_stats = {
            "total_attempts": 0,
            "successful_captures": 0,
            "successful_verifications": 0,
            "average_latency_ms": 0.0,
            "last_capture_timestamp": None,
        }

    def set_user_input(self, user_input: str) -> None:
        """Store user input for the next response capture"""
        self.last_user_input = user_input

    def capture_response(self, assistant_response: str) -> bool:
        """
        Capture assistant response with stored user input
        Phase C Enhancement: Real-time verification with <100ms latency target

        Args:
            assistant_response: The full assistant response

        Returns:
            True if conversation was captured and verified
        """
        if not self.capture_enabled or not self.last_user_input:
            return False

        # Phase C: Track performance metrics
        start_time = time.time()
        self.capture_stats["total_attempts"] += 1

        try:
            # Attempt automatic capture
            captured = auto_capture_conversation(
                user_input=self.last_user_input, assistant_response=assistant_response
            )

            # Phase C: Real-time verification using existing systems (DRY compliance)
            verification_success = False
            if captured and self.verification_enabled:
                verification_success = self._verify_capture_success(
                    self.last_user_input, assistant_response
                )

                if verification_success:
                    self.capture_stats["successful_verifications"] += 1

            # Update statistics
            if captured:
                self.capture_stats["successful_captures"] += 1

            # Calculate latency
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            self._update_latency_stats(latency_ms)

            # Clear stored input after capture attempt
            self.last_user_input = None

            # Phase C: Return verification result if available, otherwise capture result
            return verification_success if self.verification_enabled else captured

        except Exception as e:
            print(f"⚠️ Auto-capture error: {e}")
            return False

    def _verify_capture_success(self, user_input: str, assistant_response: str) -> bool:
        """
        Phase C: Verify conversation capture using existing ConversationAnalyzer (DRY compliance)

        Args:
            user_input: Original user input
            assistant_response: Assistant response

        Returns:
            True if capture verification succeeds
        """
        if not self.verification_enabled:
            return True  # Skip verification if not available

        try:
            # Use existing ConversationAnalyzer for quality verification
            conversation_text = f"User: {user_input}\n\nAssistant: {assistant_response}"
            analysis = self.conversation_analyzer.analyze_conversation(
                conversation_text
            )

            # Verification criteria using existing metrics
            verification_criteria = {
                "min_word_count": 10,  # Reasonable conversation length
                "min_coherence_score": 0.3,  # Basic coherence threshold
                "strategic_content_present": len(analysis.strategic_themes) > 0
                or len(analysis.action_items) > 0,
            }

            # Check criteria
            word_count_ok = (
                analysis.word_count >= verification_criteria["min_word_count"]
            )
            coherence_ok = (
                analysis.coherence_score >= verification_criteria["min_coherence_score"]
            )
            strategic_ok = verification_criteria["strategic_content_present"]

            verification_success = word_count_ok and coherence_ok and strategic_ok

            # Store verification context using existing ConversationLayerMemory
            if verification_success and self.conversation_layer:
                verification_context = {
                    "verification_timestamp": time.time(),
                    "analysis_metrics": {
                        "word_count": analysis.word_count,
                        "coherence_score": analysis.coherence_score,
                        "strategic_themes_count": len(analysis.strategic_themes),
                        "action_items_count": len(analysis.action_items),
                    },
                    "verification_result": "success",
                }
                self.conversation_layer.store_conversation_context(verification_context)

            return verification_success

        except Exception as e:
            print(f"⚠️ Verification error: {e}")
            return False  # Fail safe - if verification fails, don't block capture

    def _update_latency_stats(self, latency_ms: float) -> None:
        """
        Phase C: Update latency statistics using existing patterns

        Args:
            latency_ms: Latency in milliseconds
        """
        current_avg = self.capture_stats["average_latency_ms"]
        total_attempts = self.capture_stats["total_attempts"]

        # Calculate running average
        if total_attempts == 1:
            self.capture_stats["average_latency_ms"] = latency_ms
        else:
            # Weighted average for performance tracking
            self.capture_stats["average_latency_ms"] = (
                current_avg * (total_attempts - 1) + latency_ms
            ) / total_attempts

        self.capture_stats["last_capture_timestamp"] = time.time()

    def get_capture_statistics(self) -> Dict[str, Any]:
        """
        Phase C: Get detailed capture statistics

        Returns:
            Dictionary with capture performance metrics
        """
        stats = self.capture_stats.copy()

        # Calculate success rates
        if stats["total_attempts"] > 0:
            stats["capture_success_rate"] = (
                stats["successful_captures"] / stats["total_attempts"]
            )
            stats["verification_success_rate"] = (
                stats["successful_verifications"] / stats["total_attempts"]
            )
        else:
            stats["capture_success_rate"] = 0.0
            stats["verification_success_rate"] = 0.0

        # Add verification availability status
        stats["verification_enabled"] = self.verification_enabled
        stats["meets_latency_target"] = (
            stats["average_latency_ms"] < 100.0
        )  # <100ms target

        return stats


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


def get_capture_statistics() -> Dict[str, Any]:
    """
    Phase C: Get detailed capture statistics and performance metrics

    Returns:
        Dictionary with capture performance metrics including verification results
    """
    return _interceptor.get_capture_statistics()


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
