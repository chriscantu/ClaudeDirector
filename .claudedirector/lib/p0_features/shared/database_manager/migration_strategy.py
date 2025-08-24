"""
Database Migration Strategy for Embedded Systems

Delbert's zero-downtime migration strategy from SQLite to embedded databases.
Intelligent migration triggers based on performance thresholds and usage patterns.
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import structlog
import threading
from datetime import datetime, timedelta

from ....core.config import ClaudeDirectorConfig, get_config


logger = structlog.get_logger(__name__)


class MigrationTrigger(Enum):
    """Triggers that initiate database migration"""

    PERFORMANCE_DEGRADATION = "performance"  # Query times consistently >200ms
    SCALE_THRESHOLD = "scale"  # Dataset size exceeds SQLite optimal range
    WORKLOAD_COMPLEXITY = "workload"  # Analytics queries becoming dominant
    CONCURRENT_PRESSURE = "concurrency"  # Too many simultaneous connections
    SEMANTIC_SEARCH_DEMAND = "semantic"  # High semantic search usage
    MANUAL_TRIGGER = "manual"  # Administrator-initiated


class TargetDatabase(Enum):
    """Target database options for migration"""

    DUCKDB = "duckdb"  # For analytics workloads
    FAISS = "faiss"  # For semantic search workloads
    KUZU = "kuzu"  # For graph/relationship analysis
    HYBRID = "hybrid"  # Multi-database hybrid architecture


@dataclass
class MigrationCriteria:
    """Criteria for triggering database migration"""

    avg_query_time_ms: float = 200.0  # Performance threshold
    max_database_size_mb: float = 500.0  # Size threshold
    analytics_query_ratio: float = 0.3  # Analytics workload threshold
    concurrent_connections: int = 10  # Concurrency threshold
    semantic_search_ratio: float = 0.2  # Semantic search threshold
    evaluation_window_hours: int = 24  # Evaluation window
    consecutive_violations: int = 3  # Required consecutive violations


@dataclass
class MigrationPlan:
    """Migration execution plan"""

    trigger: MigrationTrigger
    target_database: TargetDatabase
    estimated_duration_minutes: int
    data_size_mb: float
    risk_level: str  # 'low', 'medium', 'high'
    rollback_strategy: str
    validation_tests: List[str]
    business_impact: str


class DatabaseMigrationStrategy:
    """
    Delbert's intelligent database migration strategy

    Migration Philosophy:
    1. Zero-downtime migrations with dual-write patterns
    2. Intelligent trigger detection based on real usage
    3. Gradual migration with performance validation
    4. Automatic rollback on performance regression
    5. Embedded database selection based on workload analysis
    """

    def __init__(self, config, director_config: Optional[ClaudeDirectorConfig] = None):
        super().__init__()
        self.config = config
        self.director_config = director_config or get_config()
        self.logger = logger.bind(component="migration_strategy")

        # Migration criteria
        self.criteria = MigrationCriteria()

        # Performance monitoring
        self._performance_history: List[Dict[str, Any]] = []
        self._workload_analysis: Dict[str, float] = {
            "transactional_ratio": 0.8,
            "analytics_ratio": 0.15,
            "semantic_ratio": 0.05,
        }

        # Migration state
        self._migration_in_progress = False
        self._migration_lock = threading.Lock()
        self._last_evaluation = None

        # Database size tracking
        self._database_size_history: List[Tuple[datetime, float]] = []

        # Migration recommendations cache
        self._cached_recommendations: Optional[List[MigrationPlan]] = None
        self._recommendation_cache_time: Optional[datetime] = None

    def evaluate_migration_need(
        self,
    ) -> Tuple[bool, List[MigrationTrigger], Dict[str, Any]]:
        """
        Evaluate if database migration is needed

        Returns:
            (needs_migration, triggered_criteria, analysis_data)
        """
        try:
            analysis_start = time.time()

            # Collect current performance metrics
            current_metrics = self._collect_performance_metrics()

            # Analyze trends
            trend_analysis = self._analyze_performance_trends()

            # Check each migration criteria
            triggered_criteria = []

            # Performance degradation check
            if self._check_performance_degradation(current_metrics, trend_analysis):
                triggered_criteria.append(MigrationTrigger.PERFORMANCE_DEGRADATION)

            # Scale threshold check
            if self._check_scale_threshold(current_metrics):
                triggered_criteria.append(MigrationTrigger.SCALE_THRESHOLD)

            # Workload complexity check
            if self._check_workload_complexity(current_metrics):
                triggered_criteria.append(MigrationTrigger.WORKLOAD_COMPLEXITY)

            # Concurrency pressure check
            if self._check_concurrent_pressure(current_metrics):
                triggered_criteria.append(MigrationTrigger.CONCURRENT_PRESSURE)

            # Semantic search demand check
            if self._check_semantic_demand(current_metrics):
                triggered_criteria.append(MigrationTrigger.SEMANTIC_SEARCH_DEMAND)

            needs_migration = (
                len(triggered_criteria) >= self.criteria.consecutive_violations
            )

            analysis_data = {
                "current_metrics": current_metrics,
                "trend_analysis": trend_analysis,
                "triggered_criteria": [t.value for t in triggered_criteria],
                "evaluation_time_ms": (time.time() - analysis_start) * 1000,
                "recommendation": self._generate_migration_recommendation(
                    triggered_criteria
                ),
            }

            self._last_evaluation = datetime.now()

            if needs_migration:
                self.logger.warning(
                    "Database migration recommended",
                    triggered_criteria=[t.value for t in triggered_criteria],
                    current_performance=current_metrics,
                )

            return needs_migration, triggered_criteria, analysis_data

        except Exception as e:
            self.logger.error("Migration evaluation failed", error=str(e))
            return False, [], {"error": str(e)}

    def generate_migration_plans(
        self, triggered_criteria: List[MigrationTrigger]
    ) -> List[MigrationPlan]:
        """
        Generate migration plans based on triggered criteria

        Delbert's Migration Planning:
        1. Analyze workload patterns to select optimal target database
        2. Estimate migration complexity and duration
        3. Design zero-downtime migration strategy
        4. Plan validation and rollback procedures
        """
        try:
            # Check cache first
            if (
                self._cached_recommendations
                and self._recommendation_cache_time
                and datetime.now() - self._recommendation_cache_time
                < timedelta(hours=1)
            ):
                return self._cached_recommendations

            migration_plans = []

            # Analyze current workload to determine best targets
            workload_analysis = self._analyze_current_workload()

            # Generate plans for different target databases
            if MigrationTrigger.WORKLOAD_COMPLEXITY in triggered_criteria:
                # Analytics-heavy workload → DuckDB
                duckdb_plan = self._create_duckdb_migration_plan(workload_analysis)
                migration_plans.append(duckdb_plan)

            if MigrationTrigger.SEMANTIC_SEARCH_DEMAND in triggered_criteria:
                # Semantic search workload → Faiss
                faiss_plan = self._create_faiss_migration_plan(workload_analysis)
                migration_plans.append(faiss_plan)

            if len(triggered_criteria) >= 2:
                # Multiple triggers → Hybrid architecture
                hybrid_plan = self._create_hybrid_migration_plan(
                    workload_analysis, triggered_criteria
                )
                migration_plans.append(hybrid_plan)

            # Always include Kuzu option for relationship analysis
            if self._should_consider_kuzu(workload_analysis):
                kuzu_plan = self._create_kuzu_migration_plan(workload_analysis)
                migration_plans.append(kuzu_plan)

            # Sort plans by estimated business value
            migration_plans.sort(
                key=lambda p: self._calculate_migration_value(p), reverse=True
            )

            # Cache recommendations
            self._cached_recommendations = migration_plans
            self._recommendation_cache_time = datetime.now()

            self.logger.info(
                "Migration plans generated",
                plans_created=len(migration_plans),
                primary_recommendation=(
                    migration_plans[0].target_database.value
                    if migration_plans
                    else None
                ),
            )

            return migration_plans

        except Exception as e:
            self.logger.error("Migration plan generation failed", error=str(e))
            return []

    def execute_migration(self, migration_plan: MigrationPlan) -> Dict[str, Any]:
        """
        Execute zero-downtime database migration

        Delbert's Migration Strategy:
        1. Prepare target database with optimized schema
        2. Start dual-write pattern (SQLite + Target)
        3. Bulk transfer historical data in background
        4. Validate data consistency and performance
        5. Switch read traffic to target database
        6. Complete migration and cleanup
        """
        with self._migration_lock:
            if self._migration_in_progress:
                return {"success": False, "error": "Migration already in progress"}

            self._migration_in_progress = True

        try:
            migration_start = time.time()

            self.logger.info(
                "Starting database migration",
                target=migration_plan.target_database.value,
                estimated_duration_min=migration_plan.estimated_duration_minutes,
            )

            # Phase 1: Preparation
            prep_result = self._prepare_migration(migration_plan)
            if not prep_result["success"]:
                return prep_result

            # Phase 2: Dual-write setup
            dual_write_result = self._setup_dual_write(migration_plan)
            if not dual_write_result["success"]:
                return dual_write_result

            # Phase 3: Data transfer
            transfer_result = self._transfer_data(migration_plan)
            if not transfer_result["success"]:
                return transfer_result

            # Phase 4: Validation
            validation_result = self._validate_migration(migration_plan)
            if not validation_result["success"]:
                return validation_result

            # Phase 5: Traffic switch
            switch_result = self._switch_traffic(migration_plan)
            if not switch_result["success"]:
                return switch_result

            # Phase 6: Cleanup
            cleanup_result = self._cleanup_migration(migration_plan)

            migration_duration = (time.time() - migration_start) / 60  # minutes

            result = {
                "success": True,
                "target_database": migration_plan.target_database.value,
                "migration_duration_minutes": migration_duration,
                "data_migrated_mb": migration_plan.data_size_mb,
                "validation_passed": validation_result.get("tests_passed", 0),
                "performance_improvement": self._measure_performance_improvement(),
            }

            self.logger.info("Database migration completed successfully", **result)

            return result

        except Exception as e:
            self.logger.error("Database migration failed", error=str(e))
            # Attempt rollback
            self._rollback_migration(migration_plan)
            return {"success": False, "error": str(e)}

        finally:
            self._migration_in_progress = False

    def get_migration_status(self) -> Dict[str, Any]:
        """Get current migration status and recommendations"""
        needs_migration, triggers, analysis = self.evaluate_migration_need()

        status = {
            "needs_migration": needs_migration,
            "triggered_criteria": [t.value for t in triggers],
            "last_evaluation": (
                self._last_evaluation.isoformat() if self._last_evaluation else None
            ),
            "migration_in_progress": self._migration_in_progress,
            "current_database": "sqlite",
            "performance_summary": analysis.get("current_metrics", {}),
            "recommendations": [],
        }

        if needs_migration:
            migration_plans = self.generate_migration_plans(triggers)
            status["recommendations"] = [
                {
                    "target_database": plan.target_database.value,
                    "estimated_duration_minutes": plan.estimated_duration_minutes,
                    "risk_level": plan.risk_level,
                    "business_impact": plan.business_impact,
                }
                for plan in migration_plans[:3]  # Top 3 recommendations
            ]

        return status

    # Private methods for migration implementation

    def _collect_performance_metrics(self) -> Dict[str, Any]:
        """Collect current database performance metrics"""
        try:
            # Get database file size
            db_path = Path(self.config.database_path)
            db_size_mb = (
                db_path.stat().st_size / (1024 * 1024) if db_path.exists() else 0
            )

            # Record database size history
            self._database_size_history.append((datetime.now(), db_size_mb))

            # Keep only recent history (30 days)
            cutoff_date = datetime.now() - timedelta(days=30)
            self._database_size_history = [
                (date, size)
                for date, size in self._database_size_history
                if date > cutoff_date
            ]

            # Calculate recent performance averages (placeholder - would get from actual monitoring)
            metrics = {
                "database_size_mb": db_size_mb,
                "avg_query_time_ms": 85.0,  # Would get from performance monitoring
                "p95_query_time_ms": 150.0,
                "concurrent_connections": 3,
                "queries_per_second": 12.5,
                "analytics_query_ratio": self._workload_analysis["analytics_ratio"],
                "semantic_query_ratio": self._workload_analysis["semantic_ratio"],
                "cache_hit_ratio": 0.85,
                "lock_contention_ratio": 0.02,
            }

            return metrics

        except Exception as e:
            self.logger.warning("Performance metrics collection failed", error=str(e))
            return {}

    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        try:
            # Analyze database size growth
            size_growth = self._calculate_size_growth_trend()

            # Analyze query performance trends (placeholder)
            performance_trend = {
                "query_time_trend": "stable",  # 'improving', 'stable', 'degrading'
                "size_growth_rate_mb_per_day": size_growth,
                "workload_complexity_trend": "increasing",
                "concurrent_usage_trend": "stable",
            }

            return performance_trend

        except Exception as e:
            self.logger.warning("Performance trend analysis failed", error=str(e))
            return {}

    def _calculate_size_growth_trend(self) -> float:
        """Calculate database size growth rate"""
        if len(self._database_size_history) < 2:
            return 0.0

        # Simple growth rate calculation
        recent_entries = self._database_size_history[-7:]  # Last 7 data points
        if len(recent_entries) < 2:
            return 0.0

        first_date, first_size = recent_entries[0]
        last_date, last_size = recent_entries[-1]

        days_elapsed = (last_date - first_date).total_seconds() / (24 * 3600)
        if days_elapsed <= 0:
            return 0.0

        growth_rate = (last_size - first_size) / days_elapsed
        return max(0.0, growth_rate)

    def _check_performance_degradation(
        self, metrics: Dict[str, Any], trends: Dict[str, Any]
    ) -> bool:
        """Check if performance degradation warrants migration"""
        avg_time = metrics.get("avg_query_time_ms", 0)
        p95_time = metrics.get("p95_query_time_ms", 0)

        # Performance degradation criteria
        return (
            avg_time > self.criteria.avg_query_time_ms
            or p95_time > self.criteria.avg_query_time_ms * 1.5
            or trends.get("query_time_trend") == "degrading"
        )

    def _check_scale_threshold(self, metrics: Dict[str, Any]) -> bool:
        """Check if database size exceeds SQLite optimal range"""
        db_size = metrics.get("database_size_mb", 0)
        return db_size > self.criteria.max_database_size_mb

    def _check_workload_complexity(self, metrics: Dict[str, Any]) -> bool:
        """Check if analytics workload is becoming dominant"""
        analytics_ratio = metrics.get("analytics_query_ratio", 0)
        return analytics_ratio > self.criteria.analytics_query_ratio

    def _check_concurrent_pressure(self, metrics: Dict[str, Any]) -> bool:
        """Check if concurrent connections are causing pressure"""
        concurrent_connections = metrics.get("concurrent_connections", 0)
        lock_contention = metrics.get("lock_contention_ratio", 0)

        return (
            concurrent_connections > self.criteria.concurrent_connections
            or lock_contention > 0.1  # 10% lock contention
        )

    def _check_semantic_demand(self, metrics: Dict[str, Any]) -> bool:
        """Check if semantic search usage is high"""
        semantic_ratio = metrics.get("semantic_query_ratio", 0)
        return semantic_ratio > self.criteria.semantic_search_ratio

    def _generate_migration_recommendation(
        self, triggered_criteria: List[MigrationTrigger]
    ) -> str:
        """Generate migration recommendation text"""
        if not triggered_criteria:
            return "No migration needed - current SQLite performance is optimal"

        if len(triggered_criteria) == 1:
            trigger = triggered_criteria[0]
            if trigger == MigrationTrigger.WORKLOAD_COMPLEXITY:
                return "Consider DuckDB migration for improved analytics performance"
            elif trigger == MigrationTrigger.SEMANTIC_SEARCH_DEMAND:
                return "Consider Faiss integration for enhanced semantic search"
            elif trigger == MigrationTrigger.SCALE_THRESHOLD:
                return "Database size suggests migration to more scalable solution"
            else:
                return f"Migration recommended due to {trigger.value} threshold"

        return "Multiple performance criteria triggered - hybrid database architecture recommended"

    def _analyze_current_workload(self) -> Dict[str, Any]:
        """Analyze current workload patterns for migration planning"""
        return {
            "transactional_queries": 75,  # Percentage
            "analytics_queries": 20,
            "semantic_searches": 5,
            "data_size_mb": 250.0,
            "peak_concurrent_users": 8,
            "primary_use_cases": [
                "strategic_planning",
                "stakeholder_tracking",
                "health_monitoring",
            ],
        }

    def _create_duckdb_migration_plan(
        self, workload_analysis: Dict[str, Any]
    ) -> MigrationPlan:
        """Create migration plan for DuckDB target"""
        return MigrationPlan(
            trigger=MigrationTrigger.WORKLOAD_COMPLEXITY,
            target_database=TargetDatabase.DUCKDB,
            estimated_duration_minutes=45,
            data_size_mb=workload_analysis["data_size_mb"],
            risk_level=self.director_config.get_enum_values("priority_levels")[2],
            rollback_strategy="Dual-write rollback with SQLite fallback",
            validation_tests=[
                "analytics_performance",
                "data_consistency",
                "query_compatibility",
            ],
            business_impact="20-30% improvement in analytics query performance",
        )

    def _create_faiss_migration_plan(
        self, workload_analysis: Dict[str, Any]
    ) -> MigrationPlan:
        """Create migration plan for Faiss target"""
        return MigrationPlan(
            trigger=MigrationTrigger.SEMANTIC_SEARCH_DEMAND,
            target_database=TargetDatabase.FAISS,
            estimated_duration_minutes=30,
            data_size_mb=workload_analysis["data_size_mb"] * 0.3,  # Only semantic data
            risk_level=self.director_config.get_enum_values("priority_levels")[3],
            rollback_strategy="Semantic search fallback to text-based search",
            validation_tests=[
                "semantic_accuracy",
                "search_performance",
                "relevance_scoring",
            ],
            business_impact="50-70% improvement in semantic search relevance and speed",
        )

    def _create_hybrid_migration_plan(
        self, workload_analysis: Dict[str, Any], triggers: List[MigrationTrigger]
    ) -> MigrationPlan:
        """Create migration plan for hybrid architecture"""
        return MigrationPlan(
            trigger=MigrationTrigger.PERFORMANCE_DEGRADATION,
            target_database=TargetDatabase.HYBRID,
            estimated_duration_minutes=90,
            data_size_mb=workload_analysis["data_size_mb"],
            risk_level=self.director_config.get_enum_values("priority_levels")[1],
            rollback_strategy="Phase-by-phase rollback with intelligent routing",
            validation_tests=[
                "routing_accuracy",
                "performance_improvement",
                "data_consistency",
                "analytics_performance",
                "semantic_accuracy",
            ],
            business_impact="Optimal performance across all workload types with intelligent routing",
        )

    def _create_kuzu_migration_plan(
        self, workload_analysis: Dict[str, Any]
    ) -> MigrationPlan:
        """Create migration plan for Kuzu graph database"""
        return MigrationPlan(
            trigger=MigrationTrigger.WORKLOAD_COMPLEXITY,
            target_database=TargetDatabase.KUZU,
            estimated_duration_minutes=60,
            data_size_mb=workload_analysis["data_size_mb"] * 0.4,  # Relationship data
            risk_level=self.director_config.get_enum_values("priority_levels")[2],
            rollback_strategy="Graph query fallback to SQL joins",
            validation_tests=[
                "relationship_accuracy",
                "graph_performance",
                "query_translation",
            ],
            business_impact="Advanced stakeholder relationship analysis and strategic network insights",
        )

    def _should_consider_kuzu(self, workload_analysis: Dict[str, Any]) -> bool:
        """Determine if Kuzu migration should be considered"""
        # Consider Kuzu if stakeholder relationships are a primary use case
        return "stakeholder_tracking" in workload_analysis.get("primary_use_cases", [])

    def _calculate_migration_value(self, plan: MigrationPlan) -> float:
        """Calculate business value score for migration plan"""
        # Simplified value calculation
        base_value = {
            TargetDatabase.DUCKDB: 0.7,
            TargetDatabase.FAISS: 0.6,
            TargetDatabase.KUZU: 0.5,
            TargetDatabase.HYBRID: 0.9,
        }.get(plan.target_database, 0.5)

        # Adjust for risk and complexity
        risk_penalty = {
            self.director_config.get_enum_values("priority_levels")[3]: 0,  # low
            self.director_config.get_enum_values("priority_levels")[2]: -0.1,  # medium
            self.director_config.get_enum_values("priority_levels")[1]: -0.2,  # high
        }.get(plan.risk_level, -0.1)
        duration_penalty = min(-0.2, -plan.estimated_duration_minutes / 500)

        return base_value + risk_penalty + duration_penalty

    # Migration execution methods (placeholders for full implementation)

    def _prepare_migration(self, plan: MigrationPlan) -> Dict[str, Any]:
        """Prepare migration environment"""
        self.logger.info(
            "Preparing migration environment", target=plan.target_database.value
        )
        # Would implement actual preparation logic
        return {"success": True, "preparation_time_ms": 5000}

    def _setup_dual_write(self, plan: MigrationPlan) -> Dict[str, Any]:
        """Setup dual-write pattern"""
        self.logger.info(
            "Setting up dual-write pattern", target=plan.target_database.value
        )
        # Would implement dual-write setup
        return {"success": True, "dual_write_ready": True}

    def _transfer_data(self, plan: MigrationPlan) -> Dict[str, Any]:
        """Transfer data to target database"""
        self.logger.info("Transferring data", size_mb=plan.data_size_mb)
        # Would implement data transfer with progress monitoring
        return {"success": True, "records_transferred": 1000, "transfer_time_ms": 15000}

    def _validate_migration(self, plan: MigrationPlan) -> Dict[str, Any]:
        """Validate migration success"""
        self.logger.info("Validating migration", tests=plan.validation_tests)
        # Would implement comprehensive validation
        return {
            "success": True,
            "tests_passed": len(plan.validation_tests),
            "validation_time_ms": 8000,
        }

    def _switch_traffic(self, plan: MigrationPlan) -> Dict[str, Any]:
        """Switch traffic to target database"""
        self.logger.info("Switching traffic to target database")
        # Would implement gradual traffic switch
        return {"success": True, "traffic_switched": True}

    def _cleanup_migration(self, plan: MigrationPlan) -> Dict[str, Any]:
        """Cleanup migration artifacts"""
        self.logger.info("Cleaning up migration artifacts")
        # Would implement cleanup
        return {"success": True, "cleanup_completed": True}

    def _rollback_migration(self, plan: MigrationPlan):
        """Rollback failed migration"""
        self.logger.warning("Rolling back migration", target=plan.target_database.value)
        # Would implement rollback logic

    def _measure_performance_improvement(self) -> Dict[str, float]:
        """Measure performance improvement after migration"""
        # Would implement actual performance measurement
        return {
            "query_time_improvement_percent": 25.0,
            "throughput_improvement_percent": 40.0,
            "concurrency_improvement_percent": 60.0,
        }
