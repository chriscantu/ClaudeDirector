"""
Response Middleware for ClaudeDirector Transparency Integration
Ensures all responses include persona headers and framework detection
"""

import sys
import time
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import transparency bridge
integration_path = Path(__file__).parent.parent.parent.parent / "integration-protection"
sys.path.insert(0, str(integration_path))

try:
    from cursor_transparency_bridge import (
        ensure_transparency_compliance,
        get_transparency_summary,
    )

    TRANSPARENCY_AVAILABLE = True
except ImportError:
    TRANSPARENCY_AVAILABLE = False
    print("⚠️ Transparency bridge not available")


class ResponseTransparencyMiddleware:
    """Middleware to apply transparency features to all responses"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = self.config.get("transparency_enabled", True)
        self.performance_stats = {
            "total_responses": 0,
            "enhanced_responses": 0,
            "avg_processing_time": 0.0,
            "total_processing_time": 0.0,
        }

    def process_response(
        self, response: str, user_input: str = "", metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process a response through the transparency system

        Returns:
            Dict containing enhanced_response, transparency_summary, and processing_stats
        """
        start_time = time.time()

        if not self.enabled or not TRANSPARENCY_AVAILABLE:
            return {
                "enhanced_response": response,
                "transparency_summary": {"transparency_applied": False},
                "processing_time": 0.0,
            }

        try:
            # Apply transparency compliance
            enhanced_response = ensure_transparency_compliance(response, user_input)

            # Get transparency summary
            transparency_summary = get_transparency_summary(
                enhanced_response, user_input
            )

            # Calculate processing time
            processing_time = time.time() - start_time

            # Update performance stats
            self._update_stats(
                processing_time, transparency_summary.get("transparency_applied", False)
            )

            return {
                "enhanced_response": enhanced_response,
                "transparency_summary": transparency_summary,
                "processing_time": processing_time,
                "middleware_applied": True,
            }

        except Exception as e:
            # Graceful fallback on error
            print(f"⚠️ Transparency middleware error: {e}")
            return {
                "enhanced_response": response,  # Return original response
                "transparency_summary": {
                    "transparency_applied": False,
                    "error": str(e),
                },
                "processing_time": time.time() - start_time,
                "middleware_applied": False,
            }

    def _update_stats(self, processing_time: float, transparency_applied: bool):
        """Update internal performance statistics"""
        self.performance_stats["total_responses"] += 1
        self.performance_stats["total_processing_time"] += processing_time

        if transparency_applied:
            self.performance_stats["enhanced_responses"] += 1

        # Update average (exponential moving average for efficiency)
        current_avg = self.performance_stats["avg_processing_time"]
        self.performance_stats["avg_processing_time"] = (
            0.9 * current_avg + 0.1 * processing_time
        )

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for monitoring"""
        total = self.performance_stats["total_responses"]
        enhanced = self.performance_stats["enhanced_responses"]

        return {
            **self.performance_stats,
            "enhancement_rate": (enhanced / max(total, 1)) * 100,
            "enabled": self.enabled,
            "transparency_available": TRANSPARENCY_AVAILABLE,
        }

    def reset_stats(self):
        """Reset performance statistics"""
        self.performance_stats = {
            "total_responses": 0,
            "enhanced_responses": 0,
            "avg_processing_time": 0.0,
            "total_processing_time": 0.0,
        }


# Global middleware instance
_transparency_middleware = None


def get_transparency_middleware(
    config: Optional[Dict] = None,
) -> ResponseTransparencyMiddleware:
    """Get or create global transparency middleware instance"""
    global _transparency_middleware
    if _transparency_middleware is None:
        _transparency_middleware = ResponseTransparencyMiddleware(config)
    return _transparency_middleware


def apply_response_transparency(
    response: str, user_input: str = "", metadata: Optional[Dict] = None
) -> str:
    """
    Convenience function to apply transparency to a response
    Returns the enhanced response string
    """
    middleware = get_transparency_middleware()
    result = middleware.process_response(response, user_input, metadata)
    return result["enhanced_response"]


def get_response_transparency_summary(
    response: str, user_input: str = ""
) -> Dict[str, Any]:
    """
    Get transparency summary for a response
    """
    middleware = get_transparency_middleware()
    result = middleware.process_response(response, user_input)
    return result["transparency_summary"]


# Integration hook for conversation capture
def enhance_conversation_turn(
    user_input: str,
    assistant_response: str,
    personas_activated: Optional[List[str]] = None,
    metadata: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Enhance a conversation turn with transparency features

    Returns enhanced turn data for capture
    """
    middleware = get_transparency_middleware()
    result = middleware.process_response(assistant_response, user_input, metadata)

    # Create enhanced turn data
    enhanced_turn = {
        "user_input": user_input,
        "assistant_response": result["enhanced_response"],
        "personas_activated": personas_activated or [],
        "metadata": metadata or {},
        "transparency_summary": result["transparency_summary"],
        "processing_time": result["processing_time"],
    }

    return enhanced_turn


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Response Transparency Middleware")
    print("=" * 50)

    # Test cases
    test_cases = [
        {
            "input": "How should we architect our platform for scale?",
            "response": "Here's a systematic approach to platform architecture...",
            "expected_persona": "martin",
        },
        {
            "input": "What's our team coordination strategy?",
            "response": "Team structure depends on several factors...",
            "expected_persona": "diego",
        },
        {
            "input": "Platform investment ROI analysis",
            "response": "Business value requires careful analysis...",
            "expected_persona": "alvaro",
        },
    ]

    middleware = ResponseTransparencyMiddleware()

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['input'][:40]}...")

        result = middleware.process_response(test_case["response"], test_case["input"])

        print(
            f"   Persona: {result['transparency_summary'].get('persona_detected', 'unknown')}"
        )
        print(
            f"   Header: {'✅' if result['transparency_summary'].get('has_persona_header') else '❌'}"
        )
        print(f"   Time: {result['processing_time']*1000:.2f}ms")
        print(
            f"   Applied: {'✅' if result['transparency_summary'].get('transparency_applied') else '❌'}"
        )

    # Performance stats
    stats = middleware.get_performance_stats()
    print(f"\n📊 Performance Stats:")
    print(f"   Total responses: {stats['total_responses']}")
    print(
        f"   Enhanced: {stats['enhanced_responses']} ({stats['enhancement_rate']:.1f}%)"
    )
    print(f"   Avg time: {stats['avg_processing_time']*1000:.2f}ms")
    print(f"   Enabled: {stats['enabled']}")
    print(f"   Available: {stats['transparency_available']}")
