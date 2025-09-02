"""
Stakeholder Intelligence Unified Module - Phase 3A.3.4 SOLID Coordinator/Facade
Transformed from monolithic implementation to SOLID-compliant component coordinator

Author: Martin | Platform Architecture with Sequential7 methodology  
"""

import sys
import time
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Phase 3A.3.1: Extract type definitions for SOLID compliance
from .stakeholder_intelligence_types import (
    StakeholderRole,
    CommunicationStyle,
    InfluenceLevel,
    StakeholderProfile,
)

# Phase 3A.3.4: Import SOLID-compliant components
from .stakeholder_components import (
    StakeholderRepository,
    StakeholderDetectionEngine,
    ContentProcessor,
    RelationshipAnalyzer,
)

# Add project root to path for legacy imports during transition
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

# Enhanced imports for Phase 9 integration + Phase 2 Migration
try:
    from ..core.config import get_config

    # Phase 2 Migration: Prefer UnifiedDatabaseCoordinator
    try:
        from ..core.unified_database import (
            get_unified_database_coordinator as get_database_manager,
        )
        print("📊 Phase 2: Using UnifiedDatabaseCoordinator for stakeholder intelligence")
    except ImportError:
        from ..core.database import get_database_manager
        print("📊 Phase 2: Fallback to legacy DatabaseManager for stakeholder intelligence")

    from ..core.exceptions import AIDetectionError, DatabaseError
    from ..performance.cache_manager import get_cache_manager
    from ..performance.memory_optimizer import get_memory_optimizer
    from ..performance.response_optimizer import get_response_optimizer
except ImportError:
    # Graceful fallback for migration period
    logging.warning("Phase 9 migration: Using legacy imports for stakeholder intelligence")

    class MinimalConfig:
        def __init__(self):
            self.database_path = str(PROJECT_ROOT / "data" / "strategic_memory.db")
            self.workspace_dir = str(PROJECT_ROOT / "leadership-workspace")

        @property
        def workspace_path_obj(self):
            return Path(self.workspace_dir)

    def get_config():
        return MinimalConfig()

    class AIDetectionError(Exception):
        def __init__(self, message, detection_type=None):
            super().__init__(message)
            self.detection_type = detection_type

    class DatabaseError(Exception):
        pass


class StakeholderIntelligenceUnified:
    """
    Unified Stakeholder Intelligence System - Phase 3A.3.4 SOLID Coordinator/Facade
    
    Transformed from monolithic architecture to SOLID-compliant coordinator pattern.
    Uses composition of specialized components following Single Responsibility Principle.

    Components:
    - StakeholderRepository: Data persistence and CRUD operations  
    - StakeholderDetectionEngine: AI-powered stakeholder detection
    - ContentProcessor: Content analysis and workspace processing
    - RelationshipAnalyzer: Relationship intelligence and interaction analysis

    Features:
    - SOLID-compliant architecture with clear separation of concerns
    - Component-based design for maintainability and testability
    - Complete backward compatibility during migration
    - Enterprise-grade performance with caching and optimization
    """

    def __init__(
        self, config: Optional[Dict[str, Any]] = None, enable_performance: bool = True
    ):
        """Initialize unified stakeholder intelligence system with SOLID components"""
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)
        self.enable_performance = enable_performance

        # Storage configuration
        self.max_stakeholders = getattr(self.config, "max_stakeholders", 500)
        self.interaction_retention_days = getattr(
            self.config, "interaction_retention", 365
        )

        # Initialize performance components (Phase 8 integration)
        cache_manager = None
        if self.enable_performance:
            try:
                cache_manager = get_cache_manager()
                self.memory_optimizer = get_memory_optimizer()
                self.response_optimizer = get_response_optimizer()
                self.logger.info(
                    "🏗️ Phase 3A.3.4: SOLID-compliant stakeholder intelligence with performance optimization"
                )
            except Exception as e:
                self.logger.warning(f"Performance optimization unavailable: {e}")
                self.enable_performance = False

        # Phase 3A.3.4: Initialize SOLID-compliant components
        self.repository = StakeholderRepository(
            cache_manager=cache_manager,
            enable_performance=self.enable_performance,
            max_stakeholders=self.max_stakeholders,
        )
        
        self.detection_engine = StakeholderDetectionEngine(
            cache_manager=cache_manager,
            enable_performance=self.enable_performance,
        )
        
        self.content_processor = ContentProcessor(
            detection_engine=self.detection_engine,
            repository=self.repository,
            enable_performance=self.enable_performance,
        )
        
        self.relationship_analyzer = RelationshipAnalyzer(
            repository=self.repository,
            cache_manager=cache_manager,
            enable_performance=self.enable_performance,
            interaction_retention_days=self.interaction_retention_days,
        )

        # Legacy compatibility layer for migration period
        self._init_legacy_compatibility()

        print("✅ Phase 3A.3.4: StakeholderIntelligenceUnified initialized with SOLID component architecture")

    def _init_legacy_compatibility(self) -> None:
        """Initialize legacy compatibility during migration"""
        pass

    def _migrate_legacy_stakeholder_data(self) -> None:
        """Migrate stakeholder data from legacy systems during Phase 9"""
        pass

    # === CORE STAKEHOLDER MANAGEMENT (SOLID Component Delegation) ===

    def add_stakeholder(
        self,
        stakeholder_data: Dict[str, Any],
        source: str = "manual",
        confidence: float = 1.0,
    ) -> bool:
        """Add or update stakeholder profile - Phase 3A.3.4: Delegates to StakeholderRepository component"""
        return self.repository.add_stakeholder(stakeholder_data, source, confidence)

    def get_stakeholder(self, stakeholder_id: str) -> Optional[StakeholderProfile]:
        """Get stakeholder profile by ID - Phase 3A.3.4: Delegates to StakeholderRepository component"""
        return self.repository.get_stakeholder(stakeholder_id)

    def list_stakeholders(
        self, filter_by: Optional[Dict[str, Any]] = None, include_metadata: bool = False
    ) -> List[Dict[str, Any]]:
        """List stakeholders with optional filtering - Phase 3A.3.4: Delegates to StakeholderRepository component"""
        return self.repository.list_stakeholders(filter_by, include_metadata)

    # === INTERACTION TRACKING (SOLID Component Delegation) ===

    def record_interaction(
        self, 
        stakeholder_id: str, 
        interaction_type: str,
        context: Dict[str, Any],
        outcome: Optional[str] = None,
    ) -> bool:
        """Record stakeholder interaction - Phase 3A.3.4: Delegates to RelationshipAnalyzer component"""
        return self.relationship_analyzer.record_interaction(stakeholder_id, interaction_type, context, outcome)

    def get_relationship_context(
        self, query: str, limit: int = 5
    ) -> Dict[str, Any]:
        """Get relationship context for strategic queries - Phase 3A.3.4: Delegates to RelationshipAnalyzer component"""
        return self.relationship_analyzer.get_relationship_context(query, limit)

    # === AI DETECTION CAPABILITIES (SOLID Component Delegation) ===

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """AI-powered stakeholder detection - Phase 3A.3.4: Delegates to StakeholderDetectionEngine component"""
        return self.detection_engine.detect_stakeholders_in_content(content, context)

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any], auto_create: bool = True
    ) -> Dict[str, Any]:
        """Process content for stakeholders - Phase 3A.3.4: Delegates to ContentProcessor component"""
        return self.content_processor.process_content_for_stakeholders(content, context, auto_create)

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process workspace for stakeholders - Phase 3A.3.4: Delegates to ContentProcessor component"""
        return self.content_processor.process_workspace_for_stakeholders(workspace_path)

    # === SYSTEM METRICS AND STATISTICS ===

    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics from all components"""
        stats = {
            "repository_stats": self.repository.get_repository_stats(),
            "interaction_stats": self.relationship_analyzer.get_interaction_stats(),
            "processing_stats": self.content_processor.get_processing_stats(),
            "detection_patterns": self.detection_engine.get_detection_patterns(),
            "system_config": {
                "max_stakeholders": self.max_stakeholders,
                "interaction_retention_days": self.interaction_retention_days,
                "performance_enabled": self.enable_performance,
            },
        }
        return stats

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        return {
            "stakeholder_count": self.repository.get_stakeholder_count(),
            "interaction_count": len(self.relationship_analyzer.interactions),
            "performance_enabled": self.enable_performance,
        }


# === LEGACY COMPATIBILITY FUNCTIONS ===

def detect_stakeholders(content: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    engine = StakeholderDetectionEngine()
    return engine.detect_stakeholders_in_content(content, context)


def get_stakeholder_intelligence():
    """Factory function to get stakeholder intelligence instance"""
    return StakeholderIntelligenceUnified()


# === LEGACY COMPATIBILITY WRAPPER CLASSES ===
# These are imported from stakeholder_components/ but also need to be available at this module level

class StakeholderLayerMemory:
    """Legacy compatibility wrapper for context_engineering/stakeholder_layer.py"""

    def __init__(self, config=None, enable_performance: bool = True):
        # Initialize with proper lazy loading to prevent circular imports
        def _init():
            return StakeholderIntelligenceUnified(config, enable_performance)
        self._unified = _init()

    def get_relationship_context(self, query: str) -> Dict[str, Any]:
        return self._unified.get_relationship_context(query)

    def get_memory_usage(self) -> Dict[str, Any]:
        return self._unified.get_memory_usage()


class StakeholderIntelligence:
    """Legacy compatibility wrapper for intelligence/stakeholder.py"""

    def __init__(
        self,
        config=None,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
    ):
        def _init():
            return StakeholderIntelligenceUnified(config, enable_performance)
        self._unified = _init()

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        return self._unified.detect_stakeholders_in_content(content, context)

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._unified.process_content_for_stakeholders(content, context)

    def list_stakeholders(
        self, filter_by: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self._unified.list_stakeholders(filter_by)

    def add_stakeholder(
        self, stakeholder_key: str, display_name: str, **kwargs
    ) -> bool:
        stakeholder_data = {"name": display_name, **kwargs}
        return self._unified.add_stakeholder(stakeholder_data)

    def get_stakeholder(self, stakeholder_key: str) -> Optional[Dict[str, Any]]:
        profile = self._unified.get_stakeholder(stakeholder_key)
        return profile.to_dict() if profile else None

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        return self._unified.process_workspace_for_stakeholders(workspace_path)

    def get_system_stats(self) -> Dict[str, Any]:
        return self._unified.get_system_stats()
