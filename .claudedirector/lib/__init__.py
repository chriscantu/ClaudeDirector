"""
ClaudeDirector - Strategic Leadership AI Framework
Version: 1.2.1

Strategic AI directors with complete transparency for engineering leadership.
Automatically adapts to VP/CTO/Director/Manager/Staff Engineer contexts.

Core Components:
- Intelligent Personas: Diego, Camille, Rachel, Alvaro, Martin + 5 more
- Strategic Frameworks: 25+ proven methodologies (Team Topologies, etc.)
- Complete Transparency: Real-time AI enhancement disclosure
- MCP Integration: Advanced analysis with transparent activation
- Persistent Memory: Context preservation across sessions

Usage:
  # Import from flattened structure
  from core.enhanced_framework_manager import EnhancedFrameworkManager
  from core.auto_conversation_integration import auto_capture_conversation

For Cursor integration, ClaudeDirector activates automatically.
For CLI usage: ./claudedirector --help
"""

__version__ = "1.2.1"
__author__ = "ClaudeDirector Team"

# Make library importable as 'claudedirector' module
import sys
from pathlib import Path

# Ensure the lib directory is the package root
lib_dir = Path(__file__).parent
if str(lib_dir) not in sys.path:
    sys.path.insert(0, str(lib_dir))

# Core framework components - using direct imports from flattened structure
try:
    __all__ = ['EnhancedFrameworkManager', 'auto_capture_conversation']
except ImportError:
    # Graceful degradation if components not available
    __all__ = []
