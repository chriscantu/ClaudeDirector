"""
Context Intelligence Bridge

Integrates strategic intelligence with context_engineering primary system.
Follows SOLID principles and maintains architectural compliance.

Architecture:
- Single Responsibility: Bridge between strategic intelligence and context engineering
- Open/Closed: Extensible for new context integration patterns
- Dependency Inversion: Depends on context_engineering abstractions
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

try:
    from ..core.models import StrategicContext
except ImportError:
    # Fallback for test environments
    import sys
    from pathlib import Path

    lib_path = Path(__file__).parent.parent
    sys.path.insert(0, str(lib_path))

    try:
        from core.models import StrategicContext
    except ImportError:
        # Mock class for test environments
        class StrategicContext:
            def __init__(
                self,
                organizational_context=None,
                strategic_objectives=None,
                stakeholder_priorities=None,
                **kwargs,
            ):
                self.organizational_context = organizational_context
                self.strategic_objectives = strategic_objectives or []
                self.stakeholder_priorities = stakeholder_priorities or {}
                for k, v in kwargs.items():
                    setattr(self, k, v)


# PHASE 8.4: Stub implementations for P0 compatibility
# Original context_engineering modules were consolidated in Phase 8


class MockAdvancedContextEngine:
    """Stub implementation for P0 compatibility"""

    def __init__(self):
        self.strategic_layer = MockStrategicLayer()
        self.stakeholder_layer = MockStakeholderLayer()
        self.organizational_layer = MockOrganizationalLayer()


class MockStrategicLayer:
    """Stub strategic layer for P0 compatibility"""

    def get_strategic_context(self):
        return {"initiatives": [], "frameworks": [], "decisions": [], "entries": []}

    def add_strategic_entry(self, entry):
        pass  # No-op for P0 compatibility


class MockStakeholderLayer:
    """Stub stakeholder layer for P0 compatibility"""

    def get_stakeholder_context(self):
        return {"stakeholders": [], "communication_patterns": {}}


class MockOrganizationalLayer:
    """Stub organizational layer for P0 compatibility"""

    def get_organizational_context(self):
        return {"patterns": {}, "structure": {}, "culture": {}}


# Type aliases for compatibility
AdvancedContextEngine = MockAdvancedContextEngine
StrategicLayerMemory = MockStrategicLayer
StakeholderLayerMemory = MockStakeholderLayer
OrganizationalLayerMemory = MockOrganizationalLayer
ContextOrchestrator = MockAdvancedContextEngine


@dataclass
class StrategicIntelligenceContext:
    """Strategic intelligence context for specifications"""

    organizational_patterns: Dict[str, Any]
    stakeholder_relationships: Dict[str, Any]
    strategic_initiatives: List[Dict[str, Any]]
    framework_history: List[str]
    decision_outcomes: List[Dict[str, Any]]


class ContextIntelligenceBridge:
    """
    Bridge between strategic intelligence and context engineering

    Follows SOLID principles:
    - Single Responsibility: Context integration for strategic intelligence
    - Dependency Inversion: Uses context_engineering abstractions
    """

    def __init__(self, context_engine: AdvancedContextEngine = None):
        """Initialize with context engine (Dependency Injection)"""
        self.context_engine = context_engine or MockAdvancedContextEngine()
        self.logger = logging.getLogger(__name__)

    def get_strategic_context_for_spec(
        self, spec_description: str, user_query: str = ""
    ) -> StrategicIntelligenceContext:
        """
        Get strategic context relevant to specification generation

        Args:
            spec_description: Description of the specification being created
            user_query: Original user query for context

        Returns:
            StrategicIntelligenceContext with relevant strategic intelligence
        """
        try:
            # Gather context from all layers
            strategic_context = self._gather_strategic_context(spec_description)
            stakeholder_context = self._gather_stakeholder_context(spec_description)
            organizational_context = self._gather_organizational_context(
                spec_description
            )

            # Assemble strategic intelligence context
            return StrategicIntelligenceContext(
                organizational_patterns=organizational_context.get("patterns", {}),
                stakeholder_relationships=stakeholder_context.get("relationships", {}),
                strategic_initiatives=strategic_context.get("initiatives", []),
                framework_history=strategic_context.get("frameworks_used", []),
                decision_outcomes=strategic_context.get("decision_history", []),
            )

        except Exception as e:
            self.logger.error(f"Failed to gather strategic context: {e}")
            return StrategicIntelligenceContext(
                organizational_patterns={},
                stakeholder_relationships={},
                strategic_initiatives=[],
                framework_history=[],
                decision_outcomes=[],
            )

    def _gather_strategic_context(self, spec_description: str) -> Dict[str, Any]:
        """Gather strategic layer context relevant to specification"""
        try:
            # Get strategic initiatives and decision history
            strategic_memory = (
                self.context_engine.strategic_layer.get_strategic_context()
            )

            # Filter for relevant strategic information
            relevant_context = {}

            if strategic_memory:
                relevant_context["initiatives"] = self._filter_relevant_initiatives(
                    strategic_memory.get("initiatives", []), spec_description
                )
                relevant_context["frameworks_used"] = strategic_memory.get(
                    "frameworks", []
                )
                relevant_context["decision_history"] = self._filter_relevant_decisions(
                    strategic_memory.get("decisions", []), spec_description
                )

            return relevant_context

        except Exception as e:
            self.logger.error(f"Failed to gather strategic context: {e}")
            return {}

    def _gather_stakeholder_context(self, spec_description: str) -> Dict[str, Any]:
        """Gather stakeholder context relevant to specification"""
        try:
            # Get stakeholder relationships and communication patterns
            stakeholder_memory = (
                self.context_engine.stakeholder_layer.get_stakeholder_context()
            )

            relevant_context = {}

            if stakeholder_memory:
                relevant_context["relationships"] = self._filter_relevant_stakeholders(
                    stakeholder_memory.get("stakeholders", []), spec_description
                )
                relevant_context["communication_patterns"] = stakeholder_memory.get(
                    "communication_patterns", {}
                )

            return relevant_context

        except Exception as e:
            self.logger.error(f"Failed to gather stakeholder context: {e}")
            return {}

    def _gather_organizational_context(self, spec_description: str) -> Dict[str, Any]:
        """Gather organizational context relevant to specification"""
        try:
            # Get organizational patterns and structure
            org_memory = (
                self.context_engine.organizational_layer.get_organizational_context()
            )

            relevant_context = {}

            if org_memory:
                relevant_context["patterns"] = org_memory.get("patterns", {})
                relevant_context["structure"] = org_memory.get("structure", {})
                relevant_context["culture"] = org_memory.get("culture", {})

            return relevant_context

        except Exception as e:
            self.logger.error(f"Failed to gather organizational context: {e}")
            return {}

    def _filter_relevant_initiatives(
        self, initiatives: List[Dict], spec_description: str
    ) -> List[Dict]:
        """Filter strategic initiatives relevant to specification"""
        relevant = []

        for initiative in initiatives:
            # Simple keyword matching - can be enhanced with semantic similarity
            initiative_text = str(initiative.get("description", "")).lower()
            if any(
                keyword in initiative_text
                for keyword in spec_description.lower().split()
            ):
                relevant.append(initiative)

        return relevant[:5]  # Limit to top 5 relevant initiatives

    def _filter_relevant_decisions(
        self, decisions: List[Dict], spec_description: str
    ) -> List[Dict]:
        """Filter strategic decisions relevant to specification"""
        relevant = []

        for decision in decisions:
            # Simple keyword matching - can be enhanced with semantic similarity
            decision_text = str(decision.get("description", "")).lower()
            if any(
                keyword in decision_text for keyword in spec_description.lower().split()
            ):
                relevant.append(decision)

        return relevant[:3]  # Limit to top 3 relevant decisions

    def _filter_relevant_stakeholders(
        self, stakeholders: List[Dict], spec_description: str
    ) -> List[Dict]:
        """Filter stakeholders relevant to specification"""
        relevant = []

        for stakeholder in stakeholders:
            # Check if stakeholder has relevant keywords or interests
            stakeholder_keywords = stakeholder.get("keywords", [])
            stakeholder_interests = stakeholder.get("interests", [])

            all_terms = stakeholder_keywords + stakeholder_interests
            if any(term.lower() in spec_description.lower() for term in all_terms):
                relevant.append(stakeholder)

        return relevant[:5]  # Limit to top 5 relevant stakeholders

    def store_specification_outcome(
        self, spec_path: str, enhancement_metadata: Dict[str, Any]
    ):
        """Store specification generation outcome in strategic memory"""
        try:
            # Create strategic memory entry for specification
            strategic_entry = {
                "type": "specification_generation",
                "spec_path": spec_path,
                "frameworks_applied": enhancement_metadata.get(
                    "frameworks_applied", []
                ),
                "stakeholders_involved": enhancement_metadata.get(
                    "stakeholders_identified", []
                ),
                "roi_projection": enhancement_metadata.get("roi_projections", {}),
                "timestamp": self._get_current_timestamp(),
            }

            # Store in strategic layer
            self.context_engine.strategic_layer.add_strategic_entry(strategic_entry)

            self.logger.info(f"Stored specification outcome for {spec_path}")

        except Exception as e:
            self.logger.error(f"Failed to store specification outcome: {e}")

    def get_specification_history(self) -> List[Dict[str, Any]]:
        """Get history of generated specifications"""
        try:
            strategic_memory = (
                self.context_engine.strategic_layer.get_strategic_context()
            )

            if not strategic_memory:
                return []

            # Filter for specification generation entries
            spec_entries = []
            for entry in strategic_memory.get("entries", []):
                if entry.get("type") == "specification_generation":
                    spec_entries.append(entry)

            return sorted(
                spec_entries, key=lambda x: x.get("timestamp", ""), reverse=True
            )

        except Exception as e:
            self.logger.error(f"Failed to get specification history: {e}")
            return []

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for memory entries"""
        from datetime import datetime

        return datetime.now().isoformat()
