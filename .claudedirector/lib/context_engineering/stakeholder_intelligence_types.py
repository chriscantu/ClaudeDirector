#!/usr/bin/env python3
"""
Stakeholder Intelligence Type Definitions
Phase 3A.3.1: Type Extraction for SOLID Compliance

🏗️ Martin | Platform Architecture - SOLID Single Responsibility Principle
🤝 Diego | Engineering Leadership - Stakeholder relationship intelligence
🤖 Berny | AI/ML Engineering - Type safety and data integrity

Extracted from stakeholder_intelligence_unified.py for enhanced maintainability
and adherence to Single Responsibility Principle.
"""

import time
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum


class StakeholderRole(Enum):
    """Enhanced stakeholder role classification for enterprise contexts"""

    EXECUTIVE = "executive"
    VP_ENGINEERING = "vp_engineering"
    CTO = "cto"
    ENGINEERING_DIRECTOR = "engineering_director"
    ENGINEERING_MANAGER = "engineering_manager"
    STAFF_ENGINEER = "staff_engineer"
    PRINCIPAL_ENGINEER = "principal_engineer"
    PRODUCT_MANAGER = "product_manager"
    DESIGNER = "designer"
    ENGINEER = "engineer"
    VENDOR = "vendor"
    CUSTOMER = "customer"
    BOARD_MEMBER = "board_member"
    OTHER = "other"


class CommunicationStyle(Enum):
    """Communication style preferences for strategic alignment"""

    DIRECT = "direct"
    COLLABORATIVE = "collaborative"
    ANALYTICAL = "analytical"
    DIPLOMATIC = "diplomatic"
    RESULTS_FOCUSED = "results_focused"
    EXECUTIVE_BRIEF = "executive_brief"
    TECHNICAL_DETAIL = "technical_detail"


class InfluenceLevel(Enum):
    """Stakeholder influence classification"""

    CRITICAL = "critical"  # Board level, CEO, key VPs
    HIGH = "high"  # VPs, Directors, key decision makers
    MEDIUM = "medium"  # Managers, Staff engineers, key contributors
    LOW = "low"  # Individual contributors, vendors


@dataclass
class StakeholderProfile:
    """Comprehensive stakeholder profile with enterprise intelligence

    Centralized data model for all stakeholder information and metrics.
    Provides consistent structure for stakeholder profiles across
    the entire stakeholder intelligence system.
    """

    stakeholder_id: str
    name: str
    role: StakeholderRole
    organization: str
    communication_style: CommunicationStyle
    influence_level: InfluenceLevel

    # Enhanced intelligence fields
    collaboration_patterns: List[str]
    preferred_frameworks: List[str]
    conflict_triggers: List[str]
    success_patterns: List[str]
    decision_making_style: str
    key_interests: List[str]
    platform_position: str  # supporter, neutral, opponent, unknown

    # Relationship metrics
    interaction_frequency: float
    last_interaction: float
    relationship_quality: float  # 0.0 to 1.0
    trust_level: float  # 0.0 to 1.0

    # Detection and validation
    detection_confidence: float  # AI detection confidence
    validated: bool  # Human validated profile
    auto_created: bool  # Created by AI vs manual

    # Metadata
    created_timestamp: float
    updated_timestamp: float
    source_files: List[str]  # Files where detected

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with enum serialization"""
        data = asdict(self)
        # Convert enums to values
        data["role"] = self.role.value
        data["communication_style"] = self.communication_style.value
        data["influence_level"] = self.influence_level.value
        return data


# Version information
__version__ = "3.0.0"  # Phase 3A.3.1 - Type Extraction
__api_version__ = "1.0"
__last_updated__ = "2025-12-02"

# Public API exports
__all__ = [
    # Enums
    "StakeholderRole",
    "CommunicationStyle",
    "InfluenceLevel",
    # Data Classes
    "StakeholderProfile",
    # Version Info
    "__version__",
    "__api_version__",
]
