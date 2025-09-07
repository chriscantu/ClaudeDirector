"""
TS-4: Workflow Optimizer Component

🏗️ Martin | Platform Architecture - Strategic Workflow Optimization

This component provides intelligent workflow optimization suggestions and efficiency
tracking for ClaudeDirector's enhanced strategic analysis capabilities.

Follows SOLID principles:
- Single Responsibility: Workflow optimization only
- Open/Closed: Extensible through composition and strategy patterns
- Liskov Substitution: Implements consistent optimization interfaces
- Interface Segregation: Focused optimization interfaces
- Dependency Inversion: Depends on abstractions for analysis

TS-4 Capabilities:
- Development workflow optimization and efficiency tracking
- Strategic workflow pattern recognition and improvement suggestions
- Productivity measurement and bottleneck identification
- Integration with code-strategic mapping for context-aware optimizations
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# TS-4: Strategic analysis integration
try:
    from .code_strategic_mapper import CodeStrategicMapper, StrategicRecommendation
    from ..context_engineering.workspace_integration import (
        TS4StrategicInsight,
        TS4WorkflowMetrics,
    )

    TS4_STRATEGIC_ANALYSIS_AVAILABLE = True
except ImportError:
    TS4_STRATEGIC_ANALYSIS_AVAILABLE = False

    # Lightweight fallback for graceful degradation
    class StrategicRecommendation:
        def __init__(self, **kwargs):
            pass

    class TS4StrategicInsight:
        def __init__(self, **kwargs):
            pass

    class TS4WorkflowMetrics:
        def __init__(self, **kwargs):
            pass


logger = logging.getLogger(__name__)


class OptimizationType(Enum):
    """Types of workflow optimizations"""

    EFFICIENCY = "efficiency"
    STRATEGIC_ALIGNMENT = "strategic_alignment"
    BOTTLENECK_REMOVAL = "bottleneck_removal"
    FRAMEWORK_APPLICATION = "framework_application"
    AUTOMATION_OPPORTUNITY = "automation_opportunity"
    COLLABORATION_IMPROVEMENT = "collaboration_improvement"


class WorkflowStage(Enum):
    """Workflow stages for optimization targeting"""

    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    OPTIMIZATION = "optimization"


@dataclass
class WorkflowOptimization:
    """Individual workflow optimization recommendation"""

    optimization_id: str
    optimization_type: OptimizationType
    title: str
    description: str
    impact_level: str  # 'high', 'medium', 'low'
    effort_required: str  # 'high', 'medium', 'low'
    estimated_time_savings: float  # hours per week
    strategic_frameworks: List[str]
    implementation_steps: List[str]
    success_metrics: List[str]
    target_workflow_stage: WorkflowStage
    confidence_score: float  # 0-1
    created_at: datetime


@dataclass
class WorkflowEfficiencyMetrics:
    """Comprehensive workflow efficiency metrics"""

    overall_efficiency_score: float  # 0-1
    productivity_trend: str  # 'improving', 'stable', 'declining'
    bottleneck_count: int
    optimization_opportunities: int
    framework_utilization_rate: float  # 0-1
    automation_potential: float  # 0-1
    collaboration_effectiveness: float  # 0-1
    strategic_alignment_score: float  # 0-1
    time_savings_potential: float  # hours per week
    last_calculated: datetime


@dataclass
class WorkflowPattern:
    """Detected workflow pattern for optimization"""

    pattern_id: str
    pattern_type: str
    frequency: int
    efficiency_impact: float  # -1 to 1 (negative = inefficient)
    description: str
    optimization_suggestions: List[str]
    detected_at: datetime


class WorkflowOptimizer:
    """
    TS-4: Intelligent workflow optimization engine

    Provides strategic workflow analysis, optimization recommendations,
    and efficiency tracking with integration to ClaudeDirector's
    strategic analysis capabilities.

    Follows SOLID principles:
    - Single Responsibility: Workflow optimization only
    - Open/Closed: Extensible optimization strategies
    - Liskov Substitution: Consistent optimization interfaces
    - Interface Segregation: Focused optimization methods
    - Dependency Inversion: Uses strategic analysis abstractions
    """

    def __init__(self, workspace_path: Optional[str] = None):
        """Initialize workflow optimizer with optional workspace integration"""
        self.logger = logging.getLogger(__name__ + ".WorkflowOptimizer")
        self.workspace_path = Path(workspace_path) if workspace_path else None

        # TS-4: Strategic analysis integration
        if TS4_STRATEGIC_ANALYSIS_AVAILABLE:
            self.strategic_mapper = CodeStrategicMapper()
            self.ts4_enabled = True
            self.logger.info(
                "TS-4 strategic analysis enabled for workflow optimization"
            )
        else:
            self.strategic_mapper = None
            self.ts4_enabled = False
            self.logger.info(
                "TS-4 strategic analysis not available - using basic optimization"
            )

        # Optimization tracking
        self.optimizations: Dict[str, WorkflowOptimization] = {}
        self.efficiency_history: List[WorkflowEfficiencyMetrics] = []
        self.detected_patterns: Dict[str, WorkflowPattern] = {}

        # Performance metrics
        self.analysis_cache: Dict[str, Any] = {}
        self.cache_ttl = 3600  # 1 hour

        self.logger.info(
            f"WorkflowOptimizer initialized with workspace: {workspace_path}"
        )

    def analyze_workflow_efficiency(
        self,
        workflow_data: Dict[str, Any],
        strategic_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowEfficiencyMetrics:
        """
        Analyze workflow efficiency and generate comprehensive metrics

        Args:
            workflow_data: Data about current workflow (files, activities, etc.)
            strategic_context: Optional strategic context for enhanced analysis

        Returns:
            Comprehensive efficiency metrics with optimization opportunities
        """
        start_time = time.time()

        try:
            # Calculate base efficiency metrics
            base_metrics = self._calculate_base_efficiency(workflow_data)

            # Enhanced analysis with TS-4 strategic context
            if self.ts4_enabled and strategic_context:
                enhanced_metrics = self._enhance_with_strategic_analysis(
                    base_metrics, workflow_data, strategic_context
                )
            else:
                enhanced_metrics = base_metrics

            # Detect workflow patterns
            patterns = self._detect_workflow_patterns(workflow_data)
            self._update_pattern_cache(patterns)

            # Calculate optimization opportunities
            optimization_count = len(
                self._identify_optimization_opportunities(enhanced_metrics, patterns)
            )

            # Create comprehensive metrics
            efficiency_metrics = WorkflowEfficiencyMetrics(
                overall_efficiency_score=enhanced_metrics.get("efficiency_score", 0.5),
                productivity_trend=self._calculate_productivity_trend(),
                bottleneck_count=len(self._identify_bottlenecks(workflow_data)),
                optimization_opportunities=optimization_count,
                framework_utilization_rate=enhanced_metrics.get(
                    "framework_utilization", 0.0
                ),
                automation_potential=self._assess_automation_potential(workflow_data),
                collaboration_effectiveness=self._assess_collaboration_effectiveness(
                    workflow_data
                ),
                strategic_alignment_score=enhanced_metrics.get(
                    "strategic_alignment", 0.5
                ),
                time_savings_potential=self._calculate_time_savings_potential(patterns),
                last_calculated=datetime.now(),
            )

            # Store in history for trend analysis
            self.efficiency_history.append(efficiency_metrics)
            if len(self.efficiency_history) > 50:  # Keep last 50 measurements
                self.efficiency_history.pop(0)

            analysis_time = time.time() - start_time
            self.logger.info(
                f"Workflow efficiency analysis completed in {analysis_time:.2f}s"
            )

            return efficiency_metrics

        except Exception as e:
            self.logger.error(f"Workflow efficiency analysis failed: {e}")
            # Return default metrics on failure
            return WorkflowEfficiencyMetrics(
                overall_efficiency_score=0.5,
                productivity_trend="stable",
                bottleneck_count=0,
                optimization_opportunities=0,
                framework_utilization_rate=0.0,
                automation_potential=0.0,
                collaboration_effectiveness=0.5,
                strategic_alignment_score=0.5,
                time_savings_potential=0.0,
                last_calculated=datetime.now(),
            )

    def generate_optimization_recommendations(
        self,
        efficiency_metrics: WorkflowEfficiencyMetrics,
        workflow_data: Dict[str, Any],
        priority_focus: Optional[str] = None,
    ) -> List[WorkflowOptimization]:
        """
        Generate prioritized workflow optimization recommendations

        Args:
            efficiency_metrics: Current efficiency metrics
            workflow_data: Workflow context data
            priority_focus: Optional focus area ('efficiency', 'strategic', 'collaboration')

        Returns:
            List of prioritized optimization recommendations
        """
        try:
            optimizations = []

            # Identify optimization opportunities
            opportunities = self._identify_optimization_opportunities(
                asdict(efficiency_metrics), self.detected_patterns
            )

            # Generate specific optimizations for each opportunity
            for opportunity in opportunities:
                optimization = self._create_optimization_recommendation(
                    opportunity, workflow_data, efficiency_metrics
                )
                if optimization:
                    optimizations.append(optimization)

            # Add strategic framework-based optimizations if available
            if self.ts4_enabled and self.strategic_mapper:
                strategic_optimizations = self._generate_strategic_optimizations(
                    workflow_data, efficiency_metrics
                )
                optimizations.extend(strategic_optimizations)

            # Prioritize optimizations
            prioritized = self._prioritize_optimizations(optimizations, priority_focus)

            # Store optimizations for tracking
            for opt in prioritized:
                self.optimizations[opt.optimization_id] = opt

            self.logger.info(f"Generated {len(prioritized)} workflow optimizations")
            return prioritized

        except Exception as e:
            self.logger.error(f"Optimization generation failed: {e}")
            return []

    def track_optimization_implementation(
        self,
        optimization_id: str,
        implementation_status: str,
        results: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Track the implementation and results of an optimization

        Args:
            optimization_id: ID of the optimization being tracked
            implementation_status: Status ('implemented', 'in_progress', 'abandoned')
            results: Optional results data (time_saved, efficiency_gain, etc.)

        Returns:
            True if tracking was successful
        """
        try:
            if optimization_id not in self.optimizations:
                self.logger.warning(f"Unknown optimization ID: {optimization_id}")
                return False

            optimization = self.optimizations[optimization_id]

            # Update optimization with implementation data
            # (In a full implementation, this would update a database)
            self.logger.info(
                f"Tracked optimization {optimization_id}: {implementation_status}"
            )

            if results:
                self.logger.info(f"Optimization results: {results}")

            return True

        except Exception as e:
            self.logger.error(f"Optimization tracking failed: {e}")
            return False

    def get_workflow_insights_summary(self) -> Dict[str, Any]:
        """Get comprehensive workflow insights summary"""
        try:
            latest_metrics = (
                self.efficiency_history[-1] if self.efficiency_history else None
            )

            return {
                "current_efficiency": (
                    latest_metrics.overall_efficiency_score if latest_metrics else 0.5
                ),
                "productivity_trend": (
                    latest_metrics.productivity_trend if latest_metrics else "stable"
                ),
                "total_optimizations": len(self.optimizations),
                "active_patterns": len(self.detected_patterns),
                "time_savings_potential": (
                    latest_metrics.time_savings_potential if latest_metrics else 0.0
                ),
                "bottleneck_count": (
                    latest_metrics.bottleneck_count if latest_metrics else 0
                ),
                "framework_utilization": (
                    latest_metrics.framework_utilization_rate if latest_metrics else 0.0
                ),
                "ts4_enabled": self.ts4_enabled,
                "analysis_history_size": len(self.efficiency_history),
                "last_analysis": (
                    latest_metrics.last_calculated.isoformat()
                    if latest_metrics
                    else None
                ),
            }

        except Exception as e:
            self.logger.error(f"Insights summary generation failed: {e}")
            return {"error": str(e)}

    # Private helper methods (following DRY principle)

    def _calculate_base_efficiency(
        self, workflow_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate base efficiency metrics from workflow data"""
        # Simplified efficiency calculation
        file_count = len(workflow_data.get("files", []))
        activity_count = len(workflow_data.get("activities", []))

        # Basic efficiency heuristics
        efficiency_score = min((activity_count / max(file_count, 1)) / 10, 1.0)

        return {
            "efficiency_score": efficiency_score,
            "framework_utilization": 0.0,  # Will be enhanced by strategic analysis
            "strategic_alignment": 0.5,  # Default neutral alignment
        }

    def _enhance_with_strategic_analysis(
        self,
        base_metrics: Dict[str, float],
        workflow_data: Dict[str, Any],
        strategic_context: Dict[str, Any],
    ) -> Dict[str, float]:
        """Enhance metrics with TS-4 strategic analysis"""
        if not self.strategic_mapper:
            return base_metrics

        try:
            # Use strategic context to enhance metrics
            enhanced_metrics = base_metrics.copy()

            # Framework utilization from strategic context
            if "frameworks" in strategic_context:
                framework_count = len(strategic_context["frameworks"])
                enhanced_metrics["framework_utilization"] = min(
                    framework_count / 5, 1.0
                )

            # Strategic alignment from context
            if "strategic_alignment" in strategic_context:
                enhanced_metrics["strategic_alignment"] = strategic_context[
                    "strategic_alignment"
                ]

            # Efficiency boost from strategic analysis
            if enhanced_metrics["framework_utilization"] > 0.5:
                enhanced_metrics[
                    "efficiency_score"
                ] *= 1.2  # 20% boost for good framework usage

            return enhanced_metrics

        except Exception as e:
            self.logger.warning(f"Strategic enhancement failed: {e}")
            return base_metrics

    def _detect_workflow_patterns(
        self, workflow_data: Dict[str, Any]
    ) -> List[WorkflowPattern]:
        """Detect workflow patterns for optimization"""
        patterns = []

        try:
            # Pattern: Repetitive file operations
            files = workflow_data.get("files", [])
            if len(files) > 10:
                patterns.append(
                    WorkflowPattern(
                        pattern_id=f"repetitive_files_{int(time.time())}",
                        pattern_type="repetitive_operations",
                        frequency=len(files),
                        efficiency_impact=-0.3,  # Negative impact
                        description=f"High number of file operations ({len(files)}) detected",
                        optimization_suggestions=[
                            "Consider batch processing",
                            "Automate repetitive tasks",
                        ],
                        detected_at=datetime.now(),
                    )
                )

            # Pattern: Strategic framework usage
            activities = workflow_data.get("activities", [])
            framework_activities = [
                a for a in activities if "framework" in str(a).lower()
            ]
            if framework_activities:
                patterns.append(
                    WorkflowPattern(
                        pattern_id=f"framework_usage_{int(time.time())}",
                        pattern_type="strategic_framework",
                        frequency=len(framework_activities),
                        efficiency_impact=0.4,  # Positive impact
                        description=f"Strategic framework usage detected ({len(framework_activities)} activities)",
                        optimization_suggestions=[
                            "Expand framework application",
                            "Document framework patterns",
                        ],
                        detected_at=datetime.now(),
                    )
                )

        except Exception as e:
            self.logger.warning(f"Pattern detection failed: {e}")

        return patterns

    def _update_pattern_cache(self, patterns: List[WorkflowPattern]):
        """Update the pattern cache with new patterns"""
        for pattern in patterns:
            self.detected_patterns[pattern.pattern_id] = pattern

        # Keep only recent patterns (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.detected_patterns = {
            pid: pattern
            for pid, pattern in self.detected_patterns.items()
            if pattern.detected_at > cutoff_time
        }

    def _calculate_productivity_trend(self) -> str:
        """Calculate productivity trend from efficiency history"""
        if len(self.efficiency_history) < 2:
            return "stable"

        recent_scores = [
            m.overall_efficiency_score for m in self.efficiency_history[-5:]
        ]

        if len(recent_scores) >= 2:
            trend = recent_scores[-1] - recent_scores[0]
            if trend > 0.1:
                return "improving"
            elif trend < -0.1:
                return "declining"

        return "stable"

    def _identify_bottlenecks(self, workflow_data: Dict[str, Any]) -> List[str]:
        """Identify workflow bottlenecks"""
        bottlenecks = []

        # Simple bottleneck detection heuristics
        files = workflow_data.get("files", [])
        activities = workflow_data.get("activities", [])

        if len(files) > 20:
            bottlenecks.append("High file count may indicate inefficient organization")

        if len(activities) > 50:
            bottlenecks.append("High activity count may indicate process inefficiency")

        return bottlenecks

    def _identify_optimization_opportunities(
        self, metrics: Dict[str, Any], patterns: Dict[str, WorkflowPattern]
    ) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities"""
        opportunities = []

        # Low efficiency opportunity
        if metrics.get("overall_efficiency_score", 0.5) < 0.6:
            opportunities.append(
                {
                    "type": OptimizationType.EFFICIENCY,
                    "description": "Overall workflow efficiency below optimal threshold",
                    "impact": "high",
                    "effort": "medium",
                }
            )

        # Framework utilization opportunity
        if metrics.get("framework_utilization_rate", 0.0) < 0.5:
            opportunities.append(
                {
                    "type": OptimizationType.FRAMEWORK_APPLICATION,
                    "description": "Low strategic framework utilization detected",
                    "impact": "medium",
                    "effort": "low",
                }
            )

        # Pattern-based opportunities
        for pattern in patterns.values():
            if pattern.efficiency_impact < -0.2:  # Negative impact patterns
                opportunities.append(
                    {
                        "type": OptimizationType.BOTTLENECK_REMOVAL,
                        "description": pattern.description,
                        "impact": "medium",
                        "effort": "medium",
                        "pattern_suggestions": pattern.optimization_suggestions,
                    }
                )

        return opportunities

    def _assess_automation_potential(self, workflow_data: Dict[str, Any]) -> float:
        """Assess automation potential (0-1)"""
        # Simple heuristic: repetitive activities indicate automation potential
        activities = workflow_data.get("activities", [])

        if not activities:
            return 0.0

        # Count repetitive patterns (simplified)
        activity_counts = {}
        for activity in activities:
            activity_str = str(activity).lower()
            activity_counts[activity_str] = activity_counts.get(activity_str, 0) + 1

        repetitive_activities = sum(
            1 for count in activity_counts.values() if count > 2
        )
        automation_potential = min(repetitive_activities / len(activities), 1.0)

        return automation_potential

    def _assess_collaboration_effectiveness(
        self, workflow_data: Dict[str, Any]
    ) -> float:
        """Assess collaboration effectiveness (0-1)"""
        # Simplified assessment based on workflow data
        # In a real implementation, this would analyze communication patterns,
        # shared resources, coordination efficiency, etc.

        files = workflow_data.get("files", [])
        activities = workflow_data.get("activities", [])

        # Heuristic: balanced file-to-activity ratio indicates good collaboration
        if not files or not activities:
            return 0.5  # Neutral score

        ratio = len(activities) / len(files)
        # Optimal ratio is around 2-5 activities per file
        if 2 <= ratio <= 5:
            return 0.8
        elif 1 <= ratio <= 7:
            return 0.6
        else:
            return 0.4

    def _calculate_time_savings_potential(
        self, patterns: Dict[str, WorkflowPattern]
    ) -> float:
        """Calculate potential time savings from optimization (hours per week)"""
        total_savings = 0.0

        for pattern in patterns.values():
            if pattern.efficiency_impact < 0:  # Inefficient patterns
                # Estimate savings based on pattern frequency and impact
                savings = (
                    abs(pattern.efficiency_impact) * pattern.frequency * 0.1
                )  # hours
                total_savings += savings

        return min(total_savings, 20.0)  # Cap at 20 hours per week

    def _create_optimization_recommendation(
        self,
        opportunity: Dict[str, Any],
        workflow_data: Dict[str, Any],
        efficiency_metrics: WorkflowEfficiencyMetrics,
    ) -> Optional[WorkflowOptimization]:
        """Create a specific optimization recommendation"""
        try:
            optimization_id = f"opt_{opportunity['type'].value}_{int(time.time())}"

            # Generate implementation steps based on opportunity type
            implementation_steps = self._generate_implementation_steps(opportunity)
            success_metrics = self._generate_success_metrics(opportunity)

            return WorkflowOptimization(
                optimization_id=optimization_id,
                optimization_type=opportunity["type"],
                title=f"Optimize {opportunity['type'].value.replace('_', ' ').title()}",
                description=opportunity["description"],
                impact_level=opportunity.get("impact", "medium"),
                effort_required=opportunity.get("effort", "medium"),
                estimated_time_savings=self._estimate_time_savings(opportunity),
                strategic_frameworks=self._suggest_frameworks(opportunity),
                implementation_steps=implementation_steps,
                success_metrics=success_metrics,
                target_workflow_stage=WorkflowStage.OPTIMIZATION,
                confidence_score=0.7,  # Default confidence
                created_at=datetime.now(),
            )

        except Exception as e:
            self.logger.error(f"Optimization creation failed: {e}")
            return None

    def _generate_strategic_optimizations(
        self,
        workflow_data: Dict[str, Any],
        efficiency_metrics: WorkflowEfficiencyMetrics,
    ) -> List[WorkflowOptimization]:
        """Generate optimizations using TS-4 strategic analysis"""
        if not self.strategic_mapper:
            return []

        optimizations = []

        try:
            # Use strategic mapper to analyze workflow for optimization opportunities
            workflow_summary = f"Workflow efficiency: {efficiency_metrics.overall_efficiency_score:.2f}, "
            workflow_summary += f"Bottlenecks: {efficiency_metrics.bottleneck_count}, "
            workflow_summary += f"Framework utilization: {efficiency_metrics.framework_utilization_rate:.2f}"

            strategic_context = self.strategic_mapper.analyze_strategic_context(
                workflow_summary, {"context_type": "workflow_optimization"}
            )

            if strategic_context and strategic_context.recommended_frameworks:
                # Create framework-based optimization
                optimization = WorkflowOptimization(
                    optimization_id=f"strategic_framework_{int(time.time())}",
                    optimization_type=OptimizationType.FRAMEWORK_APPLICATION,
                    title="Apply Strategic Frameworks",
                    description=f"Implement {', '.join(strategic_context.recommended_frameworks[:2])} for improved workflow",
                    impact_level="high",
                    effort_required="medium",
                    estimated_time_savings=2.0,  # 2 hours per week
                    strategic_frameworks=strategic_context.recommended_frameworks,
                    implementation_steps=[
                        f"Study {strategic_context.recommended_frameworks[0]} framework",
                        "Identify workflow application points",
                        "Implement framework patterns",
                        "Measure improvement",
                    ],
                    success_metrics=[
                        "Framework utilization > 70%",
                        "Efficiency score improvement",
                    ],
                    target_workflow_stage=WorkflowStage.PLANNING,
                    confidence_score=0.8,
                    created_at=datetime.now(),
                )
                optimizations.append(optimization)

        except Exception as e:
            self.logger.warning(f"Strategic optimization generation failed: {e}")

        return optimizations

    def _prioritize_optimizations(
        self,
        optimizations: List[WorkflowOptimization],
        priority_focus: Optional[str] = None,
    ) -> List[WorkflowOptimization]:
        """Prioritize optimizations based on impact, effort, and focus"""

        def priority_score(opt: WorkflowOptimization) -> float:
            # Base score from impact and effort
            impact_scores = {"high": 1.0, "medium": 0.6, "low": 0.3}
            effort_scores = {
                "low": 1.0,
                "medium": 0.7,
                "high": 0.4,
            }  # Lower effort = higher score

            score = impact_scores.get(opt.impact_level, 0.5) * effort_scores.get(
                opt.effort_required, 0.5
            )

            # Boost score based on priority focus
            if priority_focus:
                if (
                    priority_focus == "efficiency"
                    and opt.optimization_type == OptimizationType.EFFICIENCY
                ):
                    score *= 1.5
                elif (
                    priority_focus == "strategic"
                    and opt.optimization_type == OptimizationType.FRAMEWORK_APPLICATION
                ):
                    score *= 1.5
                elif (
                    priority_focus == "collaboration"
                    and opt.optimization_type
                    == OptimizationType.COLLABORATION_IMPROVEMENT
                ):
                    score *= 1.5

            # Factor in confidence and time savings
            score *= opt.confidence_score
            score += min(opt.estimated_time_savings / 10, 0.5)  # Bonus for time savings

            return score

        return sorted(optimizations, key=priority_score, reverse=True)

    def _generate_implementation_steps(self, opportunity: Dict[str, Any]) -> List[str]:
        """Generate implementation steps for an optimization opportunity"""
        opt_type = opportunity["type"]

        if opt_type == OptimizationType.EFFICIENCY:
            return [
                "Analyze current workflow bottlenecks",
                "Identify automation opportunities",
                "Implement process improvements",
                "Measure efficiency gains",
            ]
        elif opt_type == OptimizationType.FRAMEWORK_APPLICATION:
            return [
                "Select appropriate strategic framework",
                "Map framework to current workflow",
                "Train team on framework application",
                "Monitor framework effectiveness",
            ]
        elif opt_type == OptimizationType.BOTTLENECK_REMOVAL:
            return [
                "Identify specific bottleneck causes",
                "Design bottleneck elimination strategy",
                "Implement process changes",
                "Validate bottleneck resolution",
            ]
        else:
            return [
                "Analyze optimization opportunity",
                "Design improvement strategy",
                "Implement changes",
                "Measure results",
            ]

    def _generate_success_metrics(self, opportunity: Dict[str, Any]) -> List[str]:
        """Generate success metrics for an optimization opportunity"""
        opt_type = opportunity["type"]

        if opt_type == OptimizationType.EFFICIENCY:
            return [
                "Overall efficiency score > 0.8",
                "Productivity trend = improving",
                "Time savings > 2 hours/week",
            ]
        elif opt_type == OptimizationType.FRAMEWORK_APPLICATION:
            return [
                "Framework utilization rate > 0.7",
                "Strategic alignment score > 0.8",
                "Decision quality improvement",
            ]
        elif opt_type == OptimizationType.BOTTLENECK_REMOVAL:
            return [
                "Bottleneck count reduction > 50%",
                "Process completion time reduction",
                "Team satisfaction improvement",
            ]
        else:
            return [
                "Measurable improvement in target area",
                "Positive team feedback",
                "Sustained improvement over 4 weeks",
            ]

    def _estimate_time_savings(self, opportunity: Dict[str, Any]) -> float:
        """Estimate time savings for an optimization opportunity"""
        impact_savings = {"high": 4.0, "medium": 2.0, "low": 1.0}
        return impact_savings.get(opportunity.get("impact", "medium"), 2.0)

    def _suggest_frameworks(self, opportunity: Dict[str, Any]) -> List[str]:
        """Suggest relevant strategic frameworks for an optimization"""
        opt_type = opportunity["type"]

        framework_mapping = {
            OptimizationType.EFFICIENCY: ["Lean", "Kaizen", "Six Sigma"],
            OptimizationType.STRATEGIC_ALIGNMENT: [
                "OKR",
                "Balanced Scorecard",
                "Strategy Map",
            ],
            OptimizationType.BOTTLENECK_REMOVAL: [
                "Theory of Constraints",
                "Lean",
                "Agile",
            ],
            OptimizationType.FRAMEWORK_APPLICATION: [
                "Team Topologies",
                "SOLID Principles",
                "DRY",
            ],
            OptimizationType.COLLABORATION_IMPROVEMENT: [
                "Scrum",
                "Kanban",
                "Team Topologies",
            ],
            OptimizationType.AUTOMATION_OPPORTUNITY: [
                "DevOps",
                "CI/CD",
                "Infrastructure as Code",
            ],
        }

        return framework_mapping.get(opt_type, ["General Process Improvement"])


# Factory function for easy instantiation
def create_workflow_optimizer(
    workspace_path: Optional[str] = None,
) -> WorkflowOptimizer:
    """
    Factory function to create a WorkflowOptimizer instance

    Args:
        workspace_path: Optional path to workspace for file-based analysis

    Returns:
        Configured WorkflowOptimizer instance
    """
    return WorkflowOptimizer(workspace_path=workspace_path)
