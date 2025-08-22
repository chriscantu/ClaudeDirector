"""
🧠 Memory & Context Persistence Test Suite - Critical User Journey 4/5

BUSINESS CRITICAL PATH: Complete strategic memory and context preservation
FAILURE IMPACT: Strategic context lost, relationships reset, initiative tracking broken

This modular test suite provides comprehensive memory and context protection:

🔧 Modules:
- test_user_configuration.py: User config and preferences persistence (5 tests)
- test_strategic_context.py: Conversation history and initiative tracking (5 tests)
- test_stakeholder_intelligence.py: Relationship and organizational intelligence (4 tests)
- test_memory_performance.py: Performance optimization and lifecycle (5 tests)

📊 Coverage:
- 19 total test cases across 4 focused modules
- ~275 lines per module (vs 1,099 lines monolithic)
- Complete memory and context lifecycle protection
- Performance optimized (<10 seconds total execution)

🛡️ Business Protection:
- User configuration persistence across sessions
- Strategic conversation context preservation
- Stakeholder relationship intelligence tracking
- Memory performance under load (500+ conversations)
- Cross-session continuity and context handoff
- Multi-user isolation and security
- Complete strategic continuity preserved

PRIORITY: P0 BLOCKING - Strategic memory and context preservation
"""

__version__ = "1.0.0"
__author__ = "ClaudeDirector Memory & Context Team"

# Test module exports for easy importing
from .test_user_configuration import TestUserConfiguration
from .test_strategic_context import TestStrategicContext
from .test_stakeholder_intelligence import TestStakeholderIntelligence
from .test_memory_performance import TestMemoryPerformance

__all__ = [
    "TestUserConfiguration",
    "TestStrategicContext", 
    "TestStakeholderIntelligence",
    "TestMemoryPerformance",
]
