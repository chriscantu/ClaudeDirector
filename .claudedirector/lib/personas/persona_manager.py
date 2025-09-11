#!/usr/bin/env python3
"""
🎯 PERSONA MANAGER - SOLID Compliance Decomposition

Single Responsibility: Persona selection, activation, and behavior management only.
Part of unified_persona_engine.py decomposition (1,514 → ~400 lines each).

Author: Martin | Platform Architecture
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

try:
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
except ImportError:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType


class PersonaType(Enum):
    """Strategic persona types for ClaudeDirector"""

    DIEGO = "diego"  # Engineering Leadership
    CAMILLE = "camille"  # Strategic Technology
    RACHEL = "rachel"  # Design Systems Strategy
    ALVARO = "alvaro"  # Platform Investment Strategy
    MARTIN = "martin"  # Platform Architecture
    MARCUS = "marcus"  # Platform Adoption
    DAVID = "david"  # Financial Planning
    SOFIA = "sofia"  # Vendor Strategy
    ELENA = "elena"  # Compliance Strategy


@dataclass
class PersonaBehavior:
    """Persona behavior configuration"""

    persona_type: PersonaType
    challenge_intensity: float = 0.7
    framework_focus: List[str] = None
    response_style: str = "strategic"
    transparency_level: str = "high"


class PersonaManager(BaseManager):
    """
    🎯 SINGLE RESPONSIBILITY: Persona management only

    Manages persona selection, activation, and behavior configuration.
    No longer handles challenges, responses, or conversations.
    """

    def __init__(self, config: Optional[BaseManagerConfig] = None):
        """Initialize persona manager with focused responsibility"""
        if config is None:
            config = BaseManagerConfig(
                manager_name="persona_manager",
                manager_type=ManagerType.PERSONA,
                enable_caching=True,
                enable_metrics=True,
            )

        super().__init__(config)
        self.active_personas: Dict[str, PersonaBehavior] = {}
        self.persona_cache = {}

        self.logger.info("PersonaManager initialized - focused responsibility")

    def manage(self) -> Dict[str, Any]:
        """Required BaseManager abstract method implementation"""
        return {
            "status": "active",
            "active_personas": len(self.active_personas),
            "available_personas": len(list(PersonaType)),
            "responsibility": "persona_management_only",
        }

    def activate_persona(
        self, persona_type: PersonaType, context: Dict[str, Any] = None
    ) -> PersonaBehavior:
        """Activate a specific persona with behavior configuration"""
        try:
            behavior = PersonaBehavior(
                persona_type=persona_type,
                challenge_intensity=(
                    context.get("challenge_intensity", 0.7) if context else 0.7
                ),
                framework_focus=context.get("frameworks", []) if context else [],
                response_style=context.get("style", "strategic"),
                transparency_level=context.get("transparency", "high"),
            )

            self.active_personas[persona_type.value] = behavior
            self.logger.info(f"Activated persona: {persona_type.value}")

            return behavior

        except Exception as e:
            self.logger.error(f"Persona activation failed: {e}")
            return self._get_fallback_behavior(persona_type)

    def get_active_persona(self, persona_id: str) -> Optional[PersonaBehavior]:
        """Get currently active persona behavior"""
        return self.active_personas.get(persona_id)

    def list_available_personas(self) -> List[PersonaType]:
        """List all available persona types"""
        return list(PersonaType)

    def deactivate_persona(self, persona_id: str) -> bool:
        """Deactivate a specific persona"""
        if persona_id in self.active_personas:
            del self.active_personas[persona_id]
            self.logger.info(f"Deactivated persona: {persona_id}")
            return True
        return False

    def _get_fallback_behavior(self, persona_type: PersonaType) -> PersonaBehavior:
        """Provide fallback behavior for error cases"""
        return PersonaBehavior(
            persona_type=persona_type,
            challenge_intensity=0.5,
            framework_focus=["strategic_thinking"],
            response_style="balanced",
            transparency_level="medium",
        )

    def get_persona_metrics(self) -> Dict[str, Any]:
        """Get persona usage metrics"""
        return {
            "active_personas": len(self.active_personas),
            "available_personas": len(list(PersonaType)),
            "cache_size": len(self.persona_cache),
        }
