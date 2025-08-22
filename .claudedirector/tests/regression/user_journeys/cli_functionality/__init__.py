"""
🔧 CLI Functionality Test Suite - Critical User Journey 3/5

BUSINESS CRITICAL PATH: Complete command-line interface reliability for daily workflows
FAILURE IMPACT: Users lose access to core ClaudeDirector functionality via CLI

This modular test suite provides comprehensive CLI protection:

🔧 Modules:
- test_cli_core_operations.py: Core CLI functionality and essential workflows (7 tests)
- test_cli_error_handling.py: Error handling, resilience, and edge cases (8 tests)

📊 Coverage:
- 15 total test cases across 2 focused modules
- ~300 lines per module (vs 603 lines monolithic)
- Complete CLI user experience protection
- Robust error handling and resilience validation

🛡️ Business Protection:
- CLI script existence and executability
- Core command discovery and help system
- Configuration management workflows
- Chat interface integration
- Strategic persona activation via CLI
- Comprehensive error handling and user feedback
- End-to-end workflow validation
- Resilience to missing dependencies and corrupted configs
- Interrupt handling and resource constraints
- Concurrent execution safety

PRIORITY: P0 HIGH - Daily user workflow cannot fail
"""

__version__ = "1.0.0"
__author__ = "ClaudeDirector CLI Team"

# Test module exports for easy importing
from .test_cli_core_operations import TestCLICoreOperations
from .test_cli_error_handling import TestCLIErrorHandling

__all__ = [
    "TestCLICoreOperations",
    "TestCLIErrorHandling",
]
