"""
📚 Framework Attribution Test Suite - Critical User Journey 5/5

BUSINESS CRITICAL PATH: Complete strategic framework intelligence and attribution
FAILURE IMPACT: Framework intelligence lost, strategic guidance becomes generic

This modular test suite provides comprehensive framework attribution protection:

🔧 Modules:
- test_framework_detection.py: Framework detection accuracy and performance (4 tests)
- test_framework_attribution.py: Attribution formatting and transparency (5 tests) 
- test_framework_coordination.py: Multi-framework coordination and prioritization (4 tests)
- test_framework_recommendations.py: Proactive recommendations and analytics (4 tests)

📊 Coverage:
- 17 total test cases across 4 focused modules
- ~300 lines per module (vs 1,215 lines monolithic)
- Complete framework intelligence lifecycle protection
- Performance optimized (<8 seconds total execution)

🛡️ Business Protection:
- Framework detection accuracy and reliability
- Transparent attribution and audit trail compliance
- Multi-framework coordination and prioritization
- Proactive framework recommendations and usage analytics
- Complete strategic intelligence differentiation preserved

PRIORITY: P0 HIGH - Strategic framework intelligence protection
"""

__version__ = "1.0.0"
__author__ = "ClaudeDirector Framework Attribution Team"

# Test module exports for easy importing
from .test_framework_detection import TestFrameworkDetection
from .test_framework_attribution import TestFrameworkAttribution  
from .test_framework_coordination import TestFrameworkCoordination
from .test_framework_recommendations import TestFrameworkRecommendations

__all__ = [
    "TestFrameworkDetection",
    "TestFrameworkAttribution", 
    "TestFrameworkCoordination",
    "TestFrameworkRecommendations",
]
