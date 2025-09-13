"""
🎯 BasicSOLIDTemplateEngine - Shared Foundation Component

🏗️ Martin | Platform Architecture - DRY Compliance Fix

ARCHITECTURAL COMPLIANCE:
✅ DRY: Single implementation shared across UnifiedFactory and SOLIDTemplateEngine
✅ SOLID: Single responsibility for basic SOLID template generation
✅ BLOAT_PREVENTION_SYSTEM.md: Eliminates 98% code duplication (CRITICAL violation fix)
✅ PROJECT_STRUCTURE.md: Placed in .claudedirector/lib/core/generation/

DUPLICATION ELIMINATION:
- BEFORE: BasicSOLIDTemplateEngine duplicated in 2 locations (98% similarity)
- AFTER: Single shared implementation, imported by both consumers
- IMPACT: Eliminates CRITICAL BLOAT_PREVENTION_SYSTEM.md violation

Author: Martin | Platform Architecture - Sequential Thinking DRY remediation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BasicSOLIDTemplateEngine:
    """
    Basic SOLID template engine - Phase 2 foundation

    Shared implementation to eliminate code duplication between:
    - UnifiedFactory (fallback template engine)
    - SOLIDTemplateEngine (basic engine foundation)

    DRY COMPLIANCE: Single source of truth for basic SOLID templates
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize basic SOLID template engine"""
        self.config = config or {}

        # Basic SOLID principle templates
        self.templates = {
            "single_responsibility": 'class {name}:\n    """Single responsibility class"""\n    pass',
            "open_closed": 'class {name}(ABC):\n    """Open for extension, closed for modification"""\n    @abstractmethod\n    def process(self): pass',
        }

        logger.debug(
            f"BasicSOLIDTemplateEngine initialized with {len(self.templates)} templates"
        )

    def generate_template(self, template_type: str, **kwargs) -> str:
        """
        Generate SOLID-compliant code template

        Args:
            template_type: Type of template to generate
            **kwargs: Template formatting parameters

        Returns:
            Generated template code or placeholder
        """
        if template_type in self.templates:
            try:
                return self.templates[template_type].format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing template parameter: {e}")
                return f"# SOLID template for {template_type} - missing parameter: {e}"

        return f"# SOLID template for {template_type} - to be implemented"

    def get_available_templates(self) -> list:
        """Get list of available template types"""
        return list(self.templates.keys())

    def has_template(self, template_type: str) -> bool:
        """Check if template type is available"""
        return template_type in self.templates
