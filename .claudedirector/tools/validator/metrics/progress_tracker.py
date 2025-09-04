#!/usr/bin/env python3
"""
Validator Progress Tracking and Metrics

🎯 STRATEGIC OBJECTIVE: Real-time progress tracking and comprehensive metrics
for the validator-driven code elimination system.

Provides detailed analytics on elimination progress, code reduction metrics,
and system health monitoring during the validation process.

Author: Rachel | Design Systems Strategy + Diego | Engineering Leadership
Team: Validator-Driven Elimination System (Week 1)
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class EliminationMetrics:
    """Metrics for a single elimination operation"""

    operation_id: str
    timestamp: datetime
    pattern_type: str
    files_affected: List[str]
    lines_before: int
    lines_after: int
    lines_eliminated: int
    reduction_percentage: float
    execution_time_ms: int
    p0_test_results: Dict[str, bool]
    risk_level: str
    success: bool
    error_message: Optional[str] = None


@dataclass
class SessionMetrics:
    """Metrics for an entire validation session"""

    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    total_operations: int
    successful_operations: int
    failed_operations: int
    total_lines_eliminated: int
    total_files_affected: int
    average_reduction_percentage: float
    total_execution_time_ms: int
    p0_test_pass_rate: float
    operations: List[EliminationMetrics]


@dataclass
class CumulativeMetrics:
    """Cumulative metrics across all sessions"""

    total_sessions: int
    total_operations: int
    total_lines_eliminated: int
    total_files_processed: int
    overall_success_rate: float
    average_session_duration_ms: int
    top_elimination_patterns: List[Dict[str, Any]]
    performance_trends: Dict[str, List[float]]


class ProgressTracker:
    """
    📊 VALIDATOR PROGRESS TRACKING SYSTEM

    Comprehensive tracking and analytics for validator-driven elimination:
    - Real-time progress monitoring
    - Detailed elimination metrics
    - Performance trend analysis
    - Success rate tracking
    - Risk assessment analytics
    """

    def __init__(self, metrics_dir: str = None):
        self.metrics_dir = (
            Path(metrics_dir)
            if metrics_dir
            else Path(".claudedirector/tools/validator/metrics/data")
        )
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        self.current_session: Optional[SessionMetrics] = None
        self.session_start_time: Optional[datetime] = None

        # Load historical metrics
        self.cumulative_metrics = self._load_cumulative_metrics()

    def start_session(self, session_id: str = None) -> str:
        """
        Start a new validation session

        Args:
            session_id: Optional custom session ID

        Returns:
            Session ID for tracking
        """
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.session_start_time = datetime.now()
        self.current_session = SessionMetrics(
            session_id=session_id,
            start_time=self.session_start_time,
            end_time=None,
            total_operations=0,
            successful_operations=0,
            failed_operations=0,
            total_lines_eliminated=0,
            total_files_affected=0,
            average_reduction_percentage=0.0,
            total_execution_time_ms=0,
            p0_test_pass_rate=0.0,
            operations=[],
        )

        logger.info(f"📊 Started validation session: {session_id}")
        return session_id

    def track_elimination(
        self,
        operation_id: str,
        pattern_type: str,
        files_affected: List[str],
        lines_before: int,
        lines_after: int,
        execution_time_ms: int,
        p0_test_results: Dict[str, bool],
        risk_level: str,
        success: bool,
        error_message: str = None,
    ) -> EliminationMetrics:
        """
        Track a single elimination operation

        Args:
            operation_id: Unique operation identifier
            pattern_type: Type of pattern eliminated
            files_affected: List of files modified
            lines_before: Line count before elimination
            lines_after: Line count after elimination
            execution_time_ms: Operation execution time
            p0_test_results: P0 test results
            risk_level: Risk level of operation
            success: Whether operation succeeded
            error_message: Error message if failed

        Returns:
            EliminationMetrics object
        """
        if not self.current_session:
            raise ValueError("No active session - call start_session() first")

        lines_eliminated = lines_before - lines_after
        reduction_percentage = (
            (lines_eliminated / lines_before * 100) if lines_before > 0 else 0.0
        )

        metrics = EliminationMetrics(
            operation_id=operation_id,
            timestamp=datetime.now(),
            pattern_type=pattern_type,
            files_affected=files_affected,
            lines_before=lines_before,
            lines_after=lines_after,
            lines_eliminated=lines_eliminated,
            reduction_percentage=reduction_percentage,
            execution_time_ms=execution_time_ms,
            p0_test_results=p0_test_results,
            risk_level=risk_level,
            success=success,
            error_message=error_message,
        )

        # Update session metrics
        self.current_session.operations.append(metrics)
        self.current_session.total_operations += 1

        if success:
            self.current_session.successful_operations += 1
            self.current_session.total_lines_eliminated += lines_eliminated

            # Update files affected (unique count)
            all_files = set()
            for op in self.current_session.operations:
                all_files.update(op.files_affected)
            self.current_session.total_files_affected = len(all_files)
        else:
            self.current_session.failed_operations += 1

        self.current_session.total_execution_time_ms += execution_time_ms

        # Recalculate averages
        self._update_session_averages()

        logger.info(
            f"📈 Tracked elimination: {operation_id} "
            f"({lines_eliminated} lines, {reduction_percentage:.1f}% reduction)"
        )

        return metrics

    def end_session(self) -> SessionMetrics:
        """
        End the current validation session

        Returns:
            Final session metrics
        """
        if not self.current_session:
            raise ValueError("No active session to end")

        self.current_session.end_time = datetime.now()

        # Save session metrics
        self._save_session_metrics(self.current_session)

        # Update cumulative metrics
        self._update_cumulative_metrics(self.current_session)

        logger.info(f"📊 Ended validation session: {self.current_session.session_id}")
        logger.info(f"   Total Operations: {self.current_session.total_operations}")
        logger.info(
            f"   Lines Eliminated: {self.current_session.total_lines_eliminated}"
        )
        logger.info(f"   Success Rate: {self._calculate_success_rate():.1%}")

        session = self.current_session
        self.current_session = None

        return session

    def get_real_time_progress(self) -> Dict[str, Any]:
        """
        Get real-time progress information

        Returns:
            Dictionary with current progress metrics
        """
        if not self.current_session:
            return {"status": "no_active_session"}

        elapsed_time = datetime.now() - self.current_session.start_time

        return {
            "session_id": self.current_session.session_id,
            "elapsed_time_ms": int(elapsed_time.total_seconds() * 1000),
            "total_operations": self.current_session.total_operations,
            "successful_operations": self.current_session.successful_operations,
            "failed_operations": self.current_session.failed_operations,
            "total_lines_eliminated": self.current_session.total_lines_eliminated,
            "total_files_affected": self.current_session.total_files_affected,
            "current_success_rate": self._calculate_success_rate(),
            "average_reduction_percentage": self.current_session.average_reduction_percentage,
            "p0_test_pass_rate": self.current_session.p0_test_pass_rate,
            "operations_per_minute": self._calculate_operations_per_minute(),
            "estimated_completion_time": self._estimate_completion_time(),
        }

    def get_pattern_analytics(self) -> Dict[str, Any]:
        """
        Get analytics on elimination patterns

        Returns:
            Pattern-based analytics
        """
        if not self.current_session or not self.current_session.operations:
            return {"status": "no_data"}

        pattern_stats = defaultdict(
            lambda: {
                "count": 0,
                "total_lines_eliminated": 0,
                "total_execution_time": 0,
                "success_count": 0,
                "average_reduction": 0.0,
                "risk_levels": defaultdict(int),
            }
        )

        for op in self.current_session.operations:
            stats = pattern_stats[op.pattern_type]
            stats["count"] += 1

            if op.success:
                stats["total_lines_eliminated"] += op.lines_eliminated
                stats["success_count"] += 1

            stats["total_execution_time"] += op.execution_time_ms
            stats["risk_levels"][op.risk_level] += 1

        # Calculate averages
        for pattern_type, stats in pattern_stats.items():
            if stats["count"] > 0:
                stats["average_execution_time"] = (
                    stats["total_execution_time"] / stats["count"]
                )
                stats["success_rate"] = stats["success_count"] / stats["count"]

            if stats["success_count"] > 0:
                stats["average_lines_per_operation"] = (
                    stats["total_lines_eliminated"] / stats["success_count"]
                )

        return dict(pattern_stats)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance-focused metrics

        Returns:
            Performance analytics
        """
        if not self.current_session:
            return {"status": "no_active_session"}

        operations = self.current_session.operations
        if not operations:
            return {"status": "no_operations"}

        execution_times = [op.execution_time_ms for op in operations]
        reduction_percentages = [
            op.reduction_percentage for op in operations if op.success
        ]

        return {
            "total_operations": len(operations),
            "average_execution_time_ms": sum(execution_times) / len(execution_times),
            "min_execution_time_ms": min(execution_times),
            "max_execution_time_ms": max(execution_times),
            "average_reduction_percentage": (
                sum(reduction_percentages) / len(reduction_percentages)
                if reduction_percentages
                else 0
            ),
            "total_processing_time_ms": sum(execution_times),
            "operations_per_second": (
                len(operations) / (sum(execution_times) / 1000)
                if sum(execution_times) > 0
                else 0
            ),
            "efficiency_score": self._calculate_efficiency_score(),
        }

    def generate_session_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive session report

        Returns:
            Detailed session report
        """
        if not self.current_session:
            return {"error": "No active session"}

        return {
            "session_summary": {
                "session_id": self.current_session.session_id,
                "duration_ms": int(
                    (datetime.now() - self.current_session.start_time).total_seconds()
                    * 1000
                ),
                "total_operations": self.current_session.total_operations,
                "success_rate": self._calculate_success_rate(),
                "total_lines_eliminated": self.current_session.total_lines_eliminated,
                "files_affected": self.current_session.total_files_affected,
            },
            "real_time_progress": self.get_real_time_progress(),
            "pattern_analytics": self.get_pattern_analytics(),
            "performance_metrics": self.get_performance_metrics(),
            "risk_analysis": self._get_risk_analysis(),
            "recommendations": self._generate_recommendations(),
        }

    def _update_session_averages(self):
        """Update session-level average calculations"""
        if not self.current_session.operations:
            return

        successful_ops = [op for op in self.current_session.operations if op.success]

        if successful_ops:
            total_reduction = sum(op.reduction_percentage for op in successful_ops)
            self.current_session.average_reduction_percentage = total_reduction / len(
                successful_ops
            )

        # Calculate P0 test pass rate
        all_p0_results = []
        for op in self.current_session.operations:
            all_p0_results.extend(op.p0_test_results.values())

        if all_p0_results:
            self.current_session.p0_test_pass_rate = sum(all_p0_results) / len(
                all_p0_results
            )

    def _calculate_success_rate(self) -> float:
        """Calculate current session success rate"""
        if not self.current_session or self.current_session.total_operations == 0:
            return 0.0
        return (
            self.current_session.successful_operations
            / self.current_session.total_operations
        )

    def _calculate_operations_per_minute(self) -> float:
        """Calculate operations per minute rate"""
        if not self.current_session:
            return 0.0

        elapsed = datetime.now() - self.current_session.start_time
        minutes = elapsed.total_seconds() / 60

        return self.current_session.total_operations / minutes if minutes > 0 else 0.0

    def _estimate_completion_time(self) -> Optional[str]:
        """Estimate completion time based on current progress"""
        # Placeholder for completion time estimation logic
        return None

    def _calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score (0-100)"""
        if not self.current_session or not self.current_session.operations:
            return 0.0

        # Combine success rate, reduction efficiency, and speed
        success_rate = self._calculate_success_rate()
        avg_reduction = self.current_session.average_reduction_percentage / 100

        # Simple efficiency calculation (can be enhanced)
        efficiency = (
            success_rate * 0.4
            + avg_reduction * 0.4
            + min(self.current_session.p0_test_pass_rate, 1.0) * 0.2
        ) * 100

        return efficiency

    def _get_risk_analysis(self) -> Dict[str, Any]:
        """Analyze risk distribution in current session"""
        if not self.current_session:
            return {}

        risk_counts = defaultdict(int)
        risk_success_rates = defaultdict(lambda: {"total": 0, "successful": 0})

        for op in self.current_session.operations:
            risk_counts[op.risk_level] += 1
            risk_success_rates[op.risk_level]["total"] += 1
            if op.success:
                risk_success_rates[op.risk_level]["successful"] += 1

        risk_analysis = {}
        for risk_level in ["LOW", "MEDIUM", "HIGH"]:
            total = risk_success_rates[risk_level]["total"]
            successful = risk_success_rates[risk_level]["successful"]

            risk_analysis[risk_level] = {
                "count": risk_counts[risk_level],
                "success_rate": successful / total if total > 0 else 0.0,
            }

        return risk_analysis

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on current metrics"""
        recommendations = []

        if not self.current_session:
            return recommendations

        success_rate = self._calculate_success_rate()

        if success_rate < 0.8:
            recommendations.append(
                "Consider focusing on lower-risk elimination patterns to improve success rate"
            )

        if self.current_session.p0_test_pass_rate < 0.95:
            recommendations.append(
                "P0 test pass rate is below target - review test stability"
            )

        if self.current_session.average_reduction_percentage < 10:
            recommendations.append(
                "Average code reduction is low - consider targeting larger duplicate patterns"
            )

        return recommendations

    def _save_session_metrics(self, session: SessionMetrics):
        """Save session metrics to disk"""
        session_file = self.metrics_dir / f"{session.session_id}.json"

        # Convert to serializable format
        session_dict = asdict(session)
        session_dict["start_time"] = session.start_time.isoformat()
        if session.end_time:
            session_dict["end_time"] = session.end_time.isoformat()

        # Convert operation timestamps
        for op_dict in session_dict["operations"]:
            op_dict["timestamp"] = (
                datetime.fromisoformat(op_dict["timestamp"]).isoformat()
                if isinstance(op_dict["timestamp"], str)
                else op_dict["timestamp"].isoformat()
            )

        try:
            with open(session_file, "w") as f:
                json.dump(session_dict, f, indent=2)
            logger.debug(f"💾 Saved session metrics: {session_file}")
        except Exception as e:
            logger.error(f"❌ Failed to save session metrics: {e}")

    def _load_cumulative_metrics(self) -> CumulativeMetrics:
        """Load cumulative metrics from historical data"""
        # Placeholder - would load from historical session files
        return CumulativeMetrics(
            total_sessions=0,
            total_operations=0,
            total_lines_eliminated=0,
            total_files_processed=0,
            overall_success_rate=0.0,
            average_session_duration_ms=0,
            top_elimination_patterns=[],
            performance_trends={},
        )

    def _update_cumulative_metrics(self, session: SessionMetrics):
        """Update cumulative metrics with completed session"""
        # Placeholder - would update cumulative statistics
        pass


if __name__ == "__main__":
    # Example usage
    tracker = ProgressTracker()

    # Start a session
    session_id = tracker.start_session()

    # Track some eliminations
    tracker.track_elimination(
        operation_id="elim_001",
        pattern_type="initialization_pattern",
        files_affected=["file1.py", "file2.py"],
        lines_before=100,
        lines_after=80,
        execution_time_ms=1500,
        p0_test_results={"test1": True, "test2": True},
        risk_level="LOW",
        success=True,
    )

    # Get progress report
    report = tracker.generate_session_report()
    print("📊 VALIDATOR PROGRESS REPORT:")
    print(f"   Session ID: {report['session_summary']['session_id']}")
    print(f"   Operations: {report['session_summary']['total_operations']}")
    print(f"   Success Rate: {report['session_summary']['success_rate']:.1%}")
    print(f"   Lines Eliminated: {report['session_summary']['total_lines_eliminated']}")

    # End session
    final_metrics = tracker.end_session()
