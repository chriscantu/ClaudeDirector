"""
Daily Planning Configuration Constants

✅ BLOAT_PREVENTION_SYSTEM.md Compliance - Centralized Constants
✅ DRY Principle Implementation - Single Source of Truth
✅ Martin | Platform Architecture - Hard-Coded Values Elimination

Author: Martin | Platform Architecture
Date: 2025-09-23
Purpose: Eliminate all hard-coded values from Daily Planning system
Compliance: BLOAT_PREVENTION_SYSTEM.md + DRY principles
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class DailyPlanningConstants:
    """
    ✅ Centralized configuration for all Daily Planning hard-coded values
    ✅ SOLID: Single responsibility for configuration management
    ✅ DRY: Eliminates duplication across multiple files
    """

    # ✅ Strategic Alignment Configuration
    ALIGNMENT_SCORE_MULTIPLIER: int = 20
    MAX_ALIGNMENT_SCORE: int = 100
    MIN_ALIGNMENT_SCORE: int = 0

    # ✅ Priority Management Configuration
    MAX_DAILY_PRIORITIES: int = 5
    MIN_PRIORITY_NAME_LENGTH: int = 2
    DEFAULT_COMPLETED_COUNT: int = 0

    # ✅ Database/Category Constants
    DAILY_PLANNING_CATEGORY: str = "daily_planning"
    TASK_TEXT_PREFIX: str = "Daily Plan"
    TASK_STATUS_COMPLETED: str = "completed"
    TASK_STATUS_PENDING: str = "pending"

    # ✅ SQL Query Constants
    DAILY_PLANNING_CATEGORY_FILTER: str = "AND category = 'daily_planning'"

    # ✅ Default Fallback Strategic Context
    DEFAULT_L0_INITIATIVES: List[str] = None
    DEFAULT_L1_INITIATIVES: List[str] = None
    DEFAULT_ORGANIZATIONAL_PRIORITY: str = "strategic_leadership"

    # ✅ Default Priority Templates
    DEFAULT_PRIORITIES: List[str] = None

    # ✅ Task Text Formatting
    TASK_TEXT_SEPARATOR: str = "; "
    STRATEGIC_ALIGNMENT_FORMAT: str = " (Strategic alignment: {}%)"

    def __post_init__(self):
        """Initialize list fields to avoid mutable defaults"""
        if self.DEFAULT_L0_INITIATIVES is None:
            self.DEFAULT_L0_INITIATIVES = [
                "Platform Scalability",
                "Technical Debt Reduction",
                "Team Development",
            ]

        if self.DEFAULT_L1_INITIATIVES is None:
            self.DEFAULT_L1_INITIATIVES = [
                "Cross-Team Coordination",
                "Engineering Process Innovation",
            ]

        if self.DEFAULT_PRIORITIES is None:
            self.DEFAULT_PRIORITIES = [
                "Review daily tasks",
                "Strategic planning",
                "Team coordination",
            ]


class DailyPlanningConfig:
    """
    ✅ Configuration service for Daily Planning system
    ✅ Provides centralized access to all configuration values
    ✅ Implements business logic for configuration-based calculations
    """

    # ✅ Singleton pattern for configuration constants
    _constants = DailyPlanningConstants()

    @classmethod
    def get_constants(cls) -> DailyPlanningConstants:
        """✅ Access to configuration constants"""
        return cls._constants

    @classmethod
    def calculate_alignment_score(cls, priorities_count: int) -> int:
        """
        ✅ Centralized alignment scoring algorithm
        ✅ Replaces hard-coded: min(len(priorities) * 20, 100)
        """
        score = priorities_count * cls._constants.ALIGNMENT_SCORE_MULTIPLIER
        return min(score, cls._constants.MAX_ALIGNMENT_SCORE)

    @classmethod
    def get_default_strategic_context(cls) -> Dict:
        """
        ✅ Centralized default strategic context
        ✅ Replaces hard-coded L0/L1 initiative lists
        """
        return {
            "l0_initiatives": cls._constants.DEFAULT_L0_INITIATIVES.copy(),
            "l1_initiatives": cls._constants.DEFAULT_L1_INITIATIVES.copy(),
            "organizational_priorities": cls._constants.DEFAULT_ORGANIZATIONAL_PRIORITY,
        }

    @classmethod
    def format_task_text(cls, priorities: List[str]) -> str:
        """
        ✅ Centralized task text formatting
        ✅ Replaces hard-coded: f"Daily Plan: {'; '.join(priorities)}"
        """
        priorities_text = cls._constants.TASK_TEXT_SEPARATOR.join(priorities)
        return f"{cls._constants.TASK_TEXT_PREFIX}: {priorities_text}"

    @classmethod
    def limit_priorities(cls, priorities: List[str]) -> List[str]:
        """
        ✅ Centralized priority limiting
        ✅ Replaces hard-coded: priorities[:5]
        """
        return priorities[: cls._constants.MAX_DAILY_PRIORITIES]

    @classmethod
    def get_default_priorities(cls) -> List[str]:
        """
        ✅ Centralized default priority templates
        ✅ Replaces hard-coded default priority lists
        """
        return cls._constants.DEFAULT_PRIORITIES.copy()

    @classmethod
    def is_valid_priority_name(cls, priority_name: str) -> bool:
        """
        ✅ Centralized priority name validation
        ✅ Replaces hard-coded: len(priority_name) < 2
        """
        return (
            priority_name
            and len(priority_name.strip()) >= cls._constants.MIN_PRIORITY_NAME_LENGTH
        )

    @classmethod
    def format_strategic_alignment_message(cls, alignment_score: int) -> str:
        """
        ✅ Centralized strategic alignment message formatting
        ✅ Replaces hard-coded: f" (Strategic alignment: {alignment_score}%)"
        """
        return cls._constants.STRATEGIC_ALIGNMENT_FORMAT.format(alignment_score)

    @classmethod
    def get_completion_stats_template(cls, planned_count: int) -> Dict:
        """
        ✅ Centralized completion stats template
        ✅ Replaces hard-coded: {"planned": len(priorities), "completed": 0}
        """
        return {
            "planned": planned_count,
            "completed": cls._constants.DEFAULT_COMPLETED_COUNT,
        }


# ✅ Module-level convenience access
DAILY_PLANNING = DailyPlanningConfig.get_constants()
