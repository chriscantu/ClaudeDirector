#!/usr/bin/env python3
"""
Executive Visualization Type Definitions
Phase 3A.2.1: Type Extraction for SOLID Compliance

🏗️ Martin | Platform Architecture - SOLID Single Responsibility Principle
🎨 Rachel | Design Systems Strategy - Executive visualization data models
🤖 Berny | AI/ML Engineering - Type safety and data integrity

Extracted from executive_visualization_server.py for enhanced maintainability
and adherence to Single Responsibility Principle.
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class VisualizationResult:
    """Result of executive visualization generation

    Centralized data model for all executive visualization outcomes.
    Provides consistent structure for visualization results across
    the entire executive visualization system.
    """

    success: bool
    html_output: str
    chart_type: str
    persona: str
    generation_time: float
    file_size_bytes: int
    interactive_elements: List[str]
    error: Optional[str] = None
    timestamp: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Initialize timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = time.time()
