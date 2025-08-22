"""
ClaudeDirector Memory Management Module

This module provides strategic memory and data persistence capabilities
for the ClaudeDirector AI framework.

Components:
- Memory Manager: Core memory operations and persistence
- Stakeholder Intelligence: AI-powered stakeholder detection and engagement
- Meeting Intelligence: Meeting analysis and strategic insights
- Architecture Health Monitor: Platform architecture monitoring
- Workspace Monitor: Development environment monitoring
"""

from .memory_manager import StrategicMemoryManager
from .optimized_db_manager import OptimizedSQLiteManager

__all__ = [
    "StrategicMemoryManager",
    "OptimizedSQLiteManager",
]
