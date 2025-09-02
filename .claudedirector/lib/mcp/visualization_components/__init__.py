#!/usr/bin/env python3
"""
Executive Visualization Components
Phase 3A.2: SOLID Compliance Decomposition

🏗️ Martin | Platform Architecture - Component architecture design
🎨 Rachel | Design Systems Strategy - Visualization component patterns
🤖 Berny | AI/ML Engineering - Modular design principles

Decomposed visualization components from executive_visualization_server.py
following Single Responsibility Principle and clean architecture patterns.
"""

from .persona_template_manager import PersonaTemplateManager

__all__ = [
    "PersonaTemplateManager",
]
