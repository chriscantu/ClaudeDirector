"""
Enhanced Transparency Engine
Full integration of ClaudeDirector transparency system with 25+ framework detection
"""

import sys
import time
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import full transparency system
try:
    from transparency.integrated_transparency import IntegratedTransparencySystem
    from transparency.framework_detection import FrameworkDetectionMiddleware
    from transparency.mcp_transparency import MCPTransparencyMiddleware
    HAS_FULL_TRANSPARENCY = True
except ImportError:
    HAS_FULL_TRANSPARENCY = False

# Import integration bridge as fallback
integration_path = Path(__file__).parent.parent.parent.parent / "integration-protection"
sys.path.insert(0, str(integration_path))

try:
    from cursor_transparency_bridge import CursorTransparencyBridge
    HAS_BRIDGE = True
except ImportError:
    HAS_BRIDGE = False


class EnhancedTransparencyEngine:
    """
    Enhanced transparency engine combining full system with fallback bridge
    Provides 25+ framework detection, persona headers, and MCP transparency
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.performance_mode = self.config.get('performance_mode', 'standard')  # 'standard', 'fast', 'comprehensive'

        # Initialize systems in order of preference
        self.full_system = None
        self.framework_detector = None
        self.mcp_middleware = None
        self.bridge = None

        if HAS_FULL_TRANSPARENCY:
            try:
                self.full_system = IntegratedTransparencySystem(self.config)
                self.framework_detector = FrameworkDetectionMiddleware()
                self.mcp_middleware = MCPTransparencyMiddleware()
                self.mode = "full_system"
                print("✅ Enhanced transparency: Full system active (25+ frameworks)")
            except Exception as e:
                print(f"⚠️ Full transparency system failed to initialize: {e}")
                self.full_system = None

        if not self.full_system and HAS_BRIDGE:
            try:
                self.bridge = CursorTransparencyBridge()
                self.mode = "bridge_fallback"
                print("✅ Enhanced transparency: Bridge fallback active")
            except Exception as e:
                print(f"⚠️ Bridge fallback failed: {e}")
                self.bridge = None

        if not self.full_system and not self.bridge:
            self.mode = "disabled"
            print("❌ Enhanced transparency: No systems available")

        # Performance tracking
        self.performance_stats = {
            'total_requests': 0,
            'enhanced_requests': 0,
            'framework_detections': 0,
            'avg_processing_time': 0.0,
            'mode': self.mode
        }

    def enhance_response(self, response: str, user_input: str = "", metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Enhance a response with full transparency features

        Returns:
            Dict with enhanced_response, transparency_summary, frameworks_detected, processing_time
        """
        start_time = time.time()

        if self.mode == "disabled":
            return {
                'enhanced_response': response,
                'transparency_summary': {'transparency_applied': False, 'mode': 'disabled'},
                'frameworks_detected': [],
                'processing_time': 0.0
            }

        try:
            if self.mode == "full_system":
                return self._enhance_with_full_system(response, user_input, metadata, start_time)
            elif self.mode == "bridge_fallback":
                return self._enhance_with_bridge(response, user_input, metadata, start_time)
        except Exception as e:
            print(f"⚠️ Transparency enhancement error: {e}")
            return {
                'enhanced_response': response,  # Return original on error
                'transparency_summary': {'transparency_applied': False, 'error': str(e)},
                'frameworks_detected': [],
                'processing_time': time.time() - start_time
            }

    def _enhance_with_full_system(self, response: str, user_input: str, metadata: Optional[Dict], start_time: float) -> Dict[str, Any]:
        """Enhance using full transparency system"""

        # Detect persona from context
        persona = self._detect_persona_from_input(user_input)

        # Create transparency context
        context = self.full_system.create_transparency_context(persona)

        # Detect frameworks
        frameworks_detected = []
        if self.framework_detector:
            frameworks = self.framework_detector.detect_frameworks_used(response)
            frameworks_detected = [
                {
                    'name': f.framework_name,
                    'confidence': f.confidence_score,
                    'type': f.framework_type,
                    'patterns': f.matched_patterns
                }
                for f in frameworks
            ]
            context.detected_frameworks = frameworks

        # Apply transparency enhancements
        enhanced_response = self.full_system.apply_transparency(context, response)

        # Create summary
        transparency_summary = self.full_system.create_transparency_summary(context)
        transparency_summary.update({
            'mode': 'full_system',
            'persona_detected': persona,
            'frameworks_count': len(frameworks_detected)
        })

        processing_time = time.time() - start_time
        self._update_stats(processing_time, True, len(frameworks_detected))

        return {
            'enhanced_response': enhanced_response,
            'transparency_summary': transparency_summary,
            'frameworks_detected': frameworks_detected,
            'processing_time': processing_time
        }

    def _enhance_with_bridge(self, response: str, user_input: str, metadata: Optional[Dict], start_time: float) -> Dict[str, Any]:
        """Enhance using bridge fallback"""

        # Apply bridge transparency
        enhanced_response = self.bridge.apply_transparency_system(response, user_input)

        # Get summary
        transparency_summary = self.bridge.create_transparency_summary(enhanced_response, user_input)
        transparency_summary['mode'] = 'bridge_fallback'

        processing_time = time.time() - start_time
        self._update_stats(processing_time, transparency_summary.get('transparency_applied', False), 0)

        return {
            'enhanced_response': enhanced_response,
            'transparency_summary': transparency_summary,
            'frameworks_detected': [],  # Bridge doesn't do framework detection yet
            'processing_time': processing_time
        }

    def _detect_persona_from_input(self, user_input: str) -> str:
        """Detect appropriate persona from user input"""
        if self.bridge:
            return self.bridge.detect_persona_from_context(user_input)

        # Simple fallback detection
        input_lower = user_input.lower()
        if any(word in input_lower for word in ["architecture", "platform", "scalability", "technical"]):
            return "martin"
        elif any(word in input_lower for word in ["team", "leadership", "organization", "management"]):
            return "diego"
        elif any(word in input_lower for word in ["business", "roi", "investment", "value"]):
            return "alvaro"
        elif any(word in input_lower for word in ["design", "ux", "component", "ui"]):
            return "rachel"
        else:
            return "martin"  # Default

    def detect_frameworks_in_response(self, response: str) -> List[Dict[str, Any]]:
        """Detect frameworks used in a response"""
        if self.mode == "full_system" and self.framework_detector:
            frameworks = self.framework_detector.detect_frameworks_used(response)
            return [
                {
                    'name': f.framework_name,
                    'confidence': f.confidence_score,
                    'type': f.framework_type,
                    'patterns': f.matched_patterns
                }
                for f in frameworks
            ]
        return []

    def get_available_frameworks(self) -> List[str]:
        """Get list of available frameworks for detection"""
        if self.mode == "full_system" and self.framework_detector:
            return list(self.framework_detector.framework_patterns.keys())
        return []

    def add_persona_header(self, response: str, persona: str) -> str:
        """Add persona header to response"""
        if self.bridge:
            return self.bridge.add_persona_header(response, persona)

        # Fallback headers
        headers = {
            "martin": "🏗️ Martin | Platform Architecture",
            "diego": "🎯 Diego | Engineering Leadership",
            "alvaro": "💼 Alvaro | Platform Investment Strategy",
            "rachel": "🎨 Rachel | Design Systems Strategy",
            "camille": "📊 Camille | Strategic Technology"
        }

        header = headers.get(persona, headers["martin"])
        if not response.strip().startswith("🏗️") and not response.strip().startswith("🎯"):
            return f"{header}\n\n{response}"
        return response

    def _update_stats(self, processing_time: float, transparency_applied: bool, frameworks_detected: int):
        """Update performance statistics"""
        self.performance_stats['total_requests'] += 1

        if transparency_applied:
            self.performance_stats['enhanced_requests'] += 1

        if frameworks_detected > 0:
            self.performance_stats['framework_detections'] += frameworks_detected

        # Update average processing time
        current_avg = self.performance_stats['avg_processing_time']
        self.performance_stats['avg_processing_time'] = (
            0.9 * current_avg + 0.1 * processing_time
        )

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        total = self.performance_stats['total_requests']
        enhanced = self.performance_stats['enhanced_requests']

        return {
            **self.performance_stats,
            'enhancement_rate': (enhanced / max(total, 1)) * 100,
            'available_frameworks': len(self.get_available_frameworks()),
            'system_status': {
                'full_system_available': HAS_FULL_TRANSPARENCY,
                'bridge_available': HAS_BRIDGE,
                'current_mode': self.mode
            }
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get detailed system status"""
        return {
            'mode': self.mode,
            'full_system_available': HAS_FULL_TRANSPARENCY,
            'bridge_available': HAS_BRIDGE,
            'frameworks_available': len(self.get_available_frameworks()),
            'performance_mode': self.performance_mode,
            'transparency_enabled': self.mode != "disabled"
        }


# Global engine instance
_transparency_engine = None

def get_transparency_engine(config: Optional[Dict] = None) -> EnhancedTransparencyEngine:
    """Get or create global transparency engine"""
    global _transparency_engine
    if _transparency_engine is None:
        _transparency_engine = EnhancedTransparencyEngine(config)
    return _transparency_engine


def enhance_response_transparency(response: str, user_input: str = "", metadata: Optional[Dict] = None) -> str:
    """Convenience function to enhance a response with transparency"""
    engine = get_transparency_engine()
    result = engine.enhance_response(response, user_input, metadata)
    return result['enhanced_response']


def get_framework_detection_summary(response: str) -> List[Dict[str, Any]]:
    """Get framework detection summary for a response"""
    engine = get_transparency_engine()
    return engine.detect_frameworks_in_response(response)


# Example usage and testing
if __name__ == "__main__":
    print("🚀 Testing Enhanced Transparency Engine")
    print("=" * 50)

    engine = EnhancedTransparencyEngine()

    # Test framework detection capabilities
    print(f"📚 Available frameworks: {len(engine.get_available_frameworks())}")
    print(f"🔧 System mode: {engine.mode}")

    # Test cases
    test_cases = [
        {
            "input": "How should we implement Team Topologies in our architecture?",
            "response": "Based on Team Topologies principles, we should organize teams around cognitive load and Conway's Law. Stream-aligned teams work best for feature development.",
            "expected_frameworks": ["Team Topologies"]
        },
        {
            "input": "What's our strategic platform investment approach?",
            "response": "Using OGSM strategic framework, we need objectives, goals, strategies, and measures for platform ROI analysis.",
            "expected_frameworks": ["OGSM Strategic Framework"]
        },
        {
            "input": "Design thinking approach to user experience?",
            "response": "Design thinking methodology involves empathize, define, ideate, prototype, and test phases for human-centered design.",
            "expected_frameworks": ["Design Thinking"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['input'][:40]}...")

        result = engine.enhance_response(
            test_case['response'],
            test_case['input']
        )

        print(f"   Mode: {result['transparency_summary'].get('mode', 'unknown')}")
        print(f"   Persona: {result['transparency_summary'].get('persona_detected', 'unknown')}")
        print(f"   Frameworks: {len(result['frameworks_detected'])}")

        if result['frameworks_detected']:
            for framework in result['frameworks_detected']:
                print(f"     - {framework['name']} ({framework['confidence']:.2f})")

        print(f"   Processing: {result['processing_time']*1000:.2f}ms")

        # Check if expected frameworks were detected
        detected_names = [f['name'] for f in result['frameworks_detected']]
        for expected in test_case['expected_frameworks']:
            if expected in detected_names:
                print(f"     ✅ Expected framework '{expected}' detected")
            else:
                print(f"     ⚠️ Expected framework '{expected}' not detected")

    # Performance summary
    stats = engine.get_performance_stats()
    print(f"\n📊 Performance Summary:")
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Enhanced: {stats['enhanced_requests']} ({stats['enhancement_rate']:.1f}%)")
    print(f"   Framework detections: {stats['framework_detections']}")
    print(f"   Avg processing: {stats['avg_processing_time']*1000:.2f}ms")
    print(f"   Available frameworks: {stats['available_frameworks']}")
    print(f"   System mode: {stats['system_status']['current_mode']}")
