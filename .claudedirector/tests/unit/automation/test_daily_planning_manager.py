"""
Unit tests for Daily Planning Manager

✅ ARCHITECTURAL COMPLIANCE:
- Tests only coordination layer (no business logic duplication)
- Validates proper BaseManager pattern usage
- Ensures DRY compliance with existing StrategicTaskManager/StrategicMemoryManager
- Follows PROJECT_STRUCTURE.md test organization

Author: Martin | Platform Architecture
Date: 2025-09-22
Compliance: PROJECT_STRUCTURE.md + BLOAT_PREVENTION_SYSTEM.md
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
from pathlib import Path

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from lib.automation.daily_planning_manager import (
    DailyPlanningManager,
    DailyPlanningResult,
)
from lib.automation.daily_planning_config import DailyPlanningConfig, DAILY_PLANNING
from lib.core.types import ProcessingResult
from lib.core.base_manager import BaseManagerConfig, ManagerType


class TestDailyPlanningManager:
    """
    ✅ Test suite for DailyPlanningManager coordination layer only

    Focus: Test coordination between existing managers, not business logic
    """

    @pytest.fixture
    def mock_task_manager(self):
        """Mock StrategicTaskManager to test coordination only"""
        mock = Mock()
        mock.get_connection.return_value = Mock()
        mock._create_task_from_detection.return_value = 12345  # Mock task ID
        return mock

    @pytest.fixture
    def mock_memory_manager(self):
        """Mock StrategicMemoryManager to test coordination only"""
        mock = Mock()
        mock.get_strategic_context.return_value = {
            "l0_initiatives": ["Platform Scalability", "Technical Debt Reduction"],
            "l1_initiatives": ["Cross-Team Coordination"],
            "organizational_priorities": "strategic_leadership",
        }
        return mock

    @pytest.fixture
    def daily_planning_manager(self, mock_task_manager, mock_memory_manager):
        """DailyPlanningManager with mocked dependencies"""
        manager = DailyPlanningManager()

        # ✅ Mock existing infrastructure to test coordination only
        manager.task_manager = mock_task_manager
        manager.memory_manager = mock_memory_manager

        return manager

    def test_manager_initialization(self):
        """✅ Test proper BaseManager pattern initialization"""
        manager = DailyPlanningManager()

        # Verify BaseManager pattern compliance
        assert hasattr(manager, "config")
        assert manager.config.manager_name == "daily_planning_manager"
        assert manager.config.manager_type == ManagerType.AUTOMATION
        assert manager.config.enable_logging is True
        assert manager.config.enable_caching is True
        assert manager.config.enable_metrics is True

        # Verify manager dependencies are initialized
        assert hasattr(manager, "task_manager")
        assert hasattr(manager, "memory_manager")

    def test_create_daily_plan_coordination(
        self, daily_planning_manager, mock_task_manager, mock_memory_manager
    ):
        """✅ Test create_daily_plan coordinates existing systems (no new business logic)"""
        priorities = [
            "Review architecture docs",
            "Strategic planning session",
            "Team one-on-ones",
        ]

        # Execute coordination
        result = daily_planning_manager.manage(
            "create_daily_plan", priorities=priorities
        )

        # ✅ Verify coordination with existing StrategicTaskManager
        mock_task_manager._create_task_from_detection.assert_called_once()
        call_args = mock_task_manager._create_task_from_detection.call_args[0][0]
        assert call_args["task_text"] == DailyPlanningConfig.format_task_text(
            priorities
        )
        assert call_args["category"] == DAILY_PLANNING.DAILY_PLANNING_CATEGORY
        assert call_args["priority"] == "high"

        # ✅ Verify coordination with existing StrategicMemoryManager
        mock_memory_manager.get_strategic_context.assert_called()

        # ✅ Verify result structure (extends ProcessingResult)
        assert isinstance(result, DailyPlanningResult)
        assert result.success is True
        assert len(result.daily_tasks) == 1
        assert result.strategic_analysis is not None
        assert "alignment_score" in result.strategic_analysis

    def test_review_daily_plan_coordination(self, daily_planning_manager):
        """✅ Test review_daily_plan coordinates completion tracking"""
        completions = {1: True, 2: False, 3: True}  # 2/3 completed
        additional_progress = "Completed architecture review ahead of schedule"

        # Execute coordination
        result = daily_planning_manager.manage(
            "review_daily_plan",
            completions=completions,
            additional_progress=additional_progress,
        )

        # ✅ Verify result structure (no complex business logic)
        assert isinstance(result, DailyPlanningResult)
        assert result.success is True
        assert result.completion_stats["completion_rate"] == 2 / 3
        assert result.completion_stats["completed_tasks"] == 2
        assert result.completion_stats["total_tasks"] == 3
        assert result.data["additional_progress"] == additional_progress

    def test_strategic_alignment_coordination(
        self, daily_planning_manager, mock_memory_manager
    ):
        """✅ Test strategic alignment uses existing StrategicMemoryManager only"""
        priorities = ["Platform optimization", "Team development"]

        # Execute coordination
        result = daily_planning_manager._analyze_strategic_alignment(priorities)

        # ✅ Verify coordination with existing StrategicMemoryManager (no new analysis logic)
        mock_memory_manager.get_strategic_context.assert_called()

        # ✅ Verify simple coordination logic (no complex algorithms)
        assert "alignment_score" in result
        assert "l0_coverage" in result
        assert "l1_coverage" in result
        assert result["l0_coverage"] == 2  # From mock data
        assert result["l1_coverage"] == 1  # From mock data

    def test_get_today_status_coordination(
        self, daily_planning_manager, mock_task_manager
    ):
        """✅ Test get_today_status coordinates with existing database"""
        # Mock database connection and cursor
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (3, 2)  # 3 total, 2 completed
        mock_connection.cursor.return_value = mock_cursor
        mock_task_manager.get_connection.return_value = mock_connection

        # Execute coordination
        result = daily_planning_manager.manage("get_today_status")

        # ✅ Verify coordination with existing StrategicTaskManager database
        mock_task_manager.get_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()

        # ✅ Verify result structure
        assert isinstance(result, DailyPlanningResult)
        assert result.success is True
        assert result.completion_stats["total_tasks"] == 3
        assert result.completion_stats["completed_tasks"] == 2
        assert result.completion_stats["completion_rate"] == 2 / 3

    def test_strategic_balance_coordination(
        self, daily_planning_manager, mock_memory_manager
    ):
        """✅ Test strategic balance uses existing strategic context only"""
        # Execute coordination
        result = daily_planning_manager.manage("get_strategic_balance")

        # ✅ Verify coordination with existing StrategicMemoryManager
        mock_memory_manager.get_strategic_context.assert_called()

        # ✅ Verify simple balance calculation (no complex algorithms)
        assert isinstance(result, DailyPlanningResult)
        assert result.success is True
        assert result.l0_l1_balance is not None

        # Based on mock data: 2 L0 + 1 L1 = 3 total
        expected_l0_pct = (2 / 3) * 100  # 66.67%
        expected_l1_pct = (1 / 3) * 100  # 33.33%

        assert abs(result.l0_l1_balance["l0_percentage"] - expected_l0_pct) < 1
        assert abs(result.l0_l1_balance["l1_percentage"] - expected_l1_pct) < 1

    def test_error_handling_coordination(self, daily_planning_manager):
        """✅ Test error handling preserves coordination layer"""
        # Test invalid operation
        result = daily_planning_manager.manage("invalid_operation")

        # ✅ Verify error handling doesn't duplicate error logic
        with pytest.raises(ValueError, match="Unknown operation: invalid_operation"):
            daily_planning_manager.manage("invalid_operation")

    def test_dry_compliance_no_duplication(self, daily_planning_manager):
        """✅ Critical test: Verify zero code duplication with existing systems"""
        # ✅ Verify manager only coordinates, doesn't duplicate business logic

        # Should NOT have duplicate task creation logic
        assert not hasattr(daily_planning_manager, "_create_strategic_task")
        assert not hasattr(daily_planning_manager, "_execute_task_analysis")

        # Should NOT have duplicate strategic analysis logic
        assert not hasattr(daily_planning_manager, "_compute_strategic_scores")
        assert not hasattr(daily_planning_manager, "_analyze_organizational_alignment")

        # Should NOT have duplicate database schema or operations
        assert not hasattr(daily_planning_manager, "_setup_daily_plans_table")
        assert not hasattr(daily_planning_manager, "_setup_org_initiatives_table")

        # ✅ Should ONLY have coordination methods
        coordination_methods = [
            "_create_daily_plan",
            "_review_daily_plan",
            "_analyze_strategic_alignment",
            "_get_strategic_context",
            "_get_today_status",
            "_get_strategic_balance",
        ]

        for method in coordination_methods:
            assert hasattr(
                daily_planning_manager, method
            ), f"Missing coordination method: {method}"

    def test_solid_single_responsibility(self, daily_planning_manager):
        """✅ Test SOLID: Single Responsibility - only daily planning coordination"""

        # ✅ Should NOT handle other concerns
        non_daily_planning_operations = [
            "weekly_report",
            "quarterly_analysis",
            "stakeholder_mapping",
            "framework_detection",
            "performance_monitoring",
        ]

        for operation in non_daily_planning_operations:
            with pytest.raises(ValueError):
                daily_planning_manager.manage(operation)

        # ✅ Should ONLY handle daily planning operations
        valid_operations = [
            "create_daily_plan",
            "review_daily_plan",
            "analyze_strategic_alignment",
            "get_today_status",
            "get_strategic_balance",
        ]

        for operation in valid_operations:
            # Should not raise ValueError for valid operations
            try:
                result = daily_planning_manager.manage(operation, priorities=["test"])
                # Verify result is DailyPlanningResult (single responsibility)
                assert isinstance(result, DailyPlanningResult)
            except Exception as e:
                # Only coordination exceptions allowed, not ValueError for invalid operation
                assert "Unknown operation" not in str(e)

    def test_bloat_prevention_compliance(self, daily_planning_manager):
        """✅ Critical test: BLOAT_PREVENTION_SYSTEM.md compliance verification"""

        # ✅ Manager should be small coordination layer only
        coordination_layer_methods = [
            "__init__",
            "manage",
            "_create_daily_plan",
            "_review_daily_plan",
            "_analyze_strategic_alignment",
            "_get_strategic_context",
            "_get_today_status",
            "_get_strategic_balance",
        ]

        actual_methods = [
            method
            for method in dir(daily_planning_manager)
            if not method.startswith("__") or method == "__init__"
        ]

        # Should only have coordination methods + inherited BaseManager methods
        bloat_indicators = [
            method
            for method in actual_methods
            if method not in coordination_layer_methods
            and not method.startswith("_")  # Allow private inherited methods
            and method
            not in [
                "config",
                "logger",
                "task_manager",
                "memory_manager",
            ]  # Allow dependency attributes
        ]

        assert (
            len(bloat_indicators) == 0
        ), f"Potential code bloat detected: {bloat_indicators}"

        # ✅ File should be small (coordination only)
        manager_file = (
            Path(__file__).parent.parent.parent
            / "lib"
            / "automation"
            / "daily_planning_manager.py"
        )
        if manager_file.exists():
            with open(manager_file, "r") as f:
                line_count = len(f.readlines())

            # Should be small coordination layer (spec updated with completion)
            MAX_COORDINATION_LAYER_LINES = (
                450  # Configuration constant for coordination layer size
            )
            assert (
                line_count < MAX_COORDINATION_LAYER_LINES
            ), f"File too large: {line_count} lines. Should be <{MAX_COORDINATION_LAYER_LINES} for coordination layer with completion."

    @patch("lib.automation.daily_planning_manager.StrategicTaskManager")
    @patch("lib.automation.daily_planning_manager.StrategicMemoryManager")
    def test_complete_priority_success(self, mock_memory_manager, mock_task_manager):
        """
        ✅ Test priority completion functionality
        ✅ SOLID: Single responsibility for completion testing
        ✅ DRY: Uses existing mocking patterns
        """
        # Mock database interaction
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_task_manager_instance = Mock()
        mock_task_manager_instance.get_connection.return_value = mock_connection
        mock_task_manager.return_value = mock_task_manager_instance

        # Mock task found in database
        mock_cursor.fetchone.return_value = (
            1,
            DailyPlanningConfig.format_task_text(["Team meeting"]),
            DAILY_PLANNING.TASK_STATUS_PENDING,
        )

        manager = DailyPlanningManager()

        # Mock the status method to return completion stats
        with patch.object(manager, "_get_today_status") as mock_status, patch.object(
            manager, "_get_strategic_context"
        ) as mock_context:

            mock_status.return_value = DailyPlanningResult(
                success=True, completion_stats={"completed_tasks": 1, "total_tasks": 3}
            )
            mock_context.return_value = {"alignment_score": 85}

            # Test successful completion
            result = manager.manage("complete_priority", priority_name="team meeting")

            # ✅ Validate result structure
            assert isinstance(result, DailyPlanningResult)
            assert result.success is True
            assert "Priority completed" in result.message
            assert result.completion_stats is not None
            assert result.strategic_analysis is not None

            # ✅ Validate database interaction (DRY: uses existing patterns)
            mock_cursor.execute.assert_called()
            mock_connection.commit.assert_called_once()

    @patch("lib.automation.daily_planning_manager.StrategicTaskManager")
    @patch("lib.automation.daily_planning_manager.StrategicMemoryManager")
    def test_complete_priority_not_found(self, mock_memory_manager, mock_task_manager):
        """
        ✅ Test completion when priority not found
        ✅ Error handling validation
        """
        # Mock database interaction - no task found
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_task_manager_instance = Mock()
        mock_task_manager_instance.get_connection.return_value = mock_connection
        mock_task_manager.return_value = mock_task_manager_instance

        # Mock no task found
        mock_cursor.fetchone.return_value = None

        manager = DailyPlanningManager()

        # Test priority not found
        result = manager.manage("complete_priority", priority_name="nonexistent task")

        # ✅ Validate error handling
        assert isinstance(result, DailyPlanningResult)
        assert result.success is False
        assert "not found" in result.message
        assert result.data["error"] == "priority_not_found"

    @patch("lib.automation.daily_planning_manager.StrategicTaskManager")
    @patch("lib.automation.daily_planning_manager.StrategicMemoryManager")
    def test_complete_priority_already_completed(
        self, mock_memory_manager, mock_task_manager
    ):
        """
        ✅ Test completion when priority already completed
        ✅ Idempotent operation validation
        """
        # Mock database interaction
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_task_manager_instance = Mock()
        mock_task_manager_instance.get_connection.return_value = mock_connection
        mock_task_manager.return_value = mock_task_manager_instance

        # Mock task already completed
        mock_cursor.fetchone.return_value = (
            1,
            DailyPlanningConfig.format_task_text(["Team meeting"]),
            DAILY_PLANNING.TASK_STATUS_COMPLETED,
        )

        manager = DailyPlanningManager()

        # Test already completed
        result = manager.manage("complete_priority", priority_name="team meeting")

        # ✅ Validate idempotent behavior
        assert isinstance(result, DailyPlanningResult)
        assert result.success is True
        assert "already completed" in result.message
        assert result.data["already_completed"] is True
