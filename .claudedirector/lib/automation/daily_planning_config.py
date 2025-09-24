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

    # ✅ Command Constants (Context7 Pattern: Centralized Command Management)
    CMD_START: str = "/daily-plan start"
    CMD_STATUS: str = "/daily-plan status"
    CMD_REVIEW: str = "/daily-plan review"
    CMD_HELP: str = "/daily-plan help"

    # ✅ Session State Constants
    STATE_COLLECTING: str = "collecting_priorities"
    SESSION_KEY_STATE: str = "state"
    SESSION_KEY_PRIORITIES: str = "priorities"
    SESSION_KEY_STARTED: str = "started_at"
    SESSION_KEY_USER_ID: str = "user_id"
    SESSION_STATE_STARTED: str = "started"

    # ✅ Completion Keywords
    COMPLETION_WORDS: List[str] = None

    # ✅ User Messages (Context7 Pattern: Centralized Message Management)
    MSG_SESSION_STARTED: str = (
        "🎯 Daily Planning Session Started!\n\nWhat are your top 3-5 priorities for today? Please enter them one at a time."
    )
    MSG_UNKNOWN_COMMAND: str = (
        "Unknown daily planning command. Use '/daily-plan help' for available commands."
    )
    MSG_NO_SESSION: str = (
        "No active planning session. Use '/daily-plan start' to begin."
    )
    MSG_NO_PRIORITIES: str = (
        "Please add at least one priority before completing your plan."
    )
    MSG_PRIORITY_ADDED: str = (
        "✅ Priority {count} added: {priority}\n\nAdd another priority or type 'done' to complete your plan."
    )
    MSG_PLAN_CREATED: str = (
        "✅ Daily plan created with {count} priorities:\n{priorities_list}\n\n{result_message}"
    )
    MSG_SESSION_ERROR: str = (
        "Session state error. Use '/daily-plan start' to begin a new session."
    )

    # ✅ Error Messages (Context7 Pattern: Centralized Error Management)
    ERROR_FEATURE_UNAVAILABLE: str = (
        "Sorry, the daily planning feature is not available."
    )
    ERROR_DAILY_PLANNING_UNAVAILABLE: str = "Daily planning feature not available"
    ERROR_COMMAND_PROCESSING: str = "Error processing daily planning command: {error}"

    # ✅ Follow-up Suggestions
    SUGGESTIONS_SUCCESS: List[str] = None

    # ✅ Help Text (Context7 Pattern: Centralized Documentation)
    HELP_TEXT: str = """🎯 Daily Planning Commands

Available Commands:
  /daily-plan start  - Start interactive daily planning session
  /daily-plan status - Check today's progress
  /daily-plan review - Review and complete today's plan
  /daily-plan help   - Show this help message

Interactive Planning:
1. Use '/daily-plan start' to begin
2. Enter your priorities one at a time
3. Type 'done' when finished
4. Your plan will be created with strategic alignment analysis

Strategic Focus:
- L0 Initiatives: Required organizational work (70% recommended)
- L1 Initiatives: Strategic competitive advantage (30% recommended)
- Documentation focus: Planning captures priorities, doesn't execute them"""

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

        if self.COMPLETION_WORDS is None:
            self.COMPLETION_WORDS = ["done", "finish", "complete"]

        if self.SUGGESTIONS_SUCCESS is None:
            self.SUGGESTIONS_SUCCESS = [
                "/daily-plan start - Start daily planning session",
                "/daily-plan status - Check today's progress",
                "/daily-plan review - Review and complete plan",
                "/daily-plan help - Show help",
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
    def get_command_constants(cls) -> Dict[str, str]:
        """✅ Centralized command constants access"""
        return {
            "start": cls._constants.CMD_START,
            "status": cls._constants.CMD_STATUS,
            "review": cls._constants.CMD_REVIEW,
            "help": cls._constants.CMD_HELP,
        }

    @classmethod
    def get_session_data(cls, user_id: str) -> Dict[str, Any]:
        """✅ Centralized session initialization data"""
        from datetime import datetime

        return {
            cls._constants.SESSION_KEY_STATE: cls._constants.STATE_COLLECTING,
            cls._constants.SESSION_KEY_PRIORITIES: [],
            cls._constants.SESSION_KEY_STARTED: datetime.now().isoformat(),
        }

    @classmethod
    def format_priority_added_message(cls, count: int, priority: str) -> str:
        """✅ Centralized priority added message formatting"""
        return cls._constants.MSG_PRIORITY_ADDED.format(count=count, priority=priority)

    @classmethod
    def format_plan_created_message(
        cls, count: int, priorities: List[str], result_message: str
    ) -> str:
        """✅ Centralized plan created message formatting"""
        priorities_list = "\n".join(f"{i+1}. {p}" for i, p in enumerate(priorities))
        return cls._constants.MSG_PLAN_CREATED.format(
            count=count, priorities_list=priorities_list, result_message=result_message
        )

    @classmethod
    def format_error_message(cls, error: str) -> str:
        """✅ Centralized error message formatting"""
        return cls._constants.ERROR_COMMAND_PROCESSING.format(error=error)

    @classmethod
    def get_follow_up_suggestions(cls) -> List[str]:
        """✅ Centralized follow-up suggestions"""
        return cls._constants.SUGGESTIONS_SUCCESS.copy()

    @classmethod
    def is_completion_word(cls, word: str) -> bool:
        """✅ Centralized completion word checking"""
        return word.lower() in cls._constants.COMPLETION_WORDS

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
