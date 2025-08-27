"""
Organizational Learning Engine - Context Engineering Phase 3.1

Implements organizational pattern learning, cultural analysis, and change impact tracking
following ClaudeDirector's unified architecture patterns.

Author: Martin | Platform Architecture
Status: Phase 3.1 Implementation
Integration: Context Engineering Primary System
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib

# Context Engineering integration
# Removed circular import - AdvancedContextEngine imports this module
from .analytics_engine import AnalyticsEngine

logger = logging.getLogger(__name__)


@dataclass
class OrganizationalChange:
    """Track organizational changes and their strategic impacts"""

    change_id: str
    change_type: str  # 'structural', 'cultural', 'strategic', 'technological'
    impact_areas: List[str]
    stakeholders_affected: List[str]
    implementation_timeline: Dict[str, datetime]
    success_metrics: Dict[str, float]
    outcome_assessment: Optional[str] = None
    lessons_learned: List[str] = None
    confidence_score: float = 0.0

    def __post_init__(self):
        if self.lessons_learned is None:
            self.lessons_learned = []


@dataclass
class CulturalDimension:
    """Organizational culture dimension analysis"""

    dimension_name: str  # 'power_distance', 'uncertainty_avoidance', etc.
    score: float  # 0.0 to 1.0
    confidence: float
    evidence_sources: List[str]
    trend_direction: str  # 'increasing', 'stable', 'decreasing'
    framework_adjustments: Dict[str, float]
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class OrganizationalPattern:
    """Identified organizational success/failure patterns"""

    pattern_id: str
    pattern_type: str  # 'success', 'failure', 'risk'
    pattern_description: str
    contexts: List[str]
    frequency: float
    impact_score: float
    recommendations: List[str]
    confidence: float
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class OrganizationalChangeTracker:
    """Track and analyze organizational changes and their impacts"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.OrganizationalChangeTracker")

        # Performance targets per OVERVIEW.md
        self.max_analysis_time = self.config.get("max_analysis_time", 3.0)  # <3s target
        self.confidence_threshold = self.config.get("confidence_threshold", 0.8)

        # Change tracking storage
        self.changes: Dict[str, OrganizationalChange] = {}
        self.change_patterns: Dict[str, List[str]] = {}

    def track_organizational_change(
        self,
        change_type: str,
        description: str,
        stakeholders: List[str],
        expected_impact: Dict[str, Any],
    ) -> OrganizationalChange:
        """Track a new organizational change with impact prediction"""

        start_time = datetime.now()

        change_id = self._generate_change_id(change_type, description)

        # Analyze impact areas based on description and stakeholders
        impact_areas = self._analyze_impact_areas(description, stakeholders)

        # Create timeline based on change type
        timeline = self._create_implementation_timeline(change_type)

        # Initialize success metrics
        success_metrics = self._initialize_success_metrics(change_type, expected_impact)

        change = OrganizationalChange(
            change_id=change_id,
            change_type=change_type,
            impact_areas=impact_areas,
            stakeholders_affected=stakeholders,
            implementation_timeline=timeline,
            success_metrics=success_metrics,
            confidence_score=self._calculate_change_confidence(
                change_type, impact_areas
            ),
        )

        self.changes[change_id] = change

        # Performance check per OVERVIEW.md
        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed > self.max_analysis_time:
            self.logger.warning(
                f"Change tracking exceeded {self.max_analysis_time}s: {elapsed:.2f}s"
            )

        self.logger.info(f"Organizational change tracked: {change_id} ({change_type})")
        return change

    def assess_change_impact(
        self, change_id: str, actual_outcomes: Dict[str, Any]
    ) -> float:
        """Assess the actual impact of an organizational change"""

        if change_id not in self.changes:
            raise ValueError(f"Change {change_id} not found")

        change = self.changes[change_id]

        # Calculate success score based on actual vs expected outcomes
        success_score = self._calculate_success_score(
            change.success_metrics, actual_outcomes
        )

        # Extract lessons learned
        lessons = self._extract_lessons_learned(change, actual_outcomes, success_score)

        # Update change record
        change.outcome_assessment = f"Success Score: {success_score:.2f}"
        change.lessons_learned = lessons

        # Update organizational patterns
        self._update_organizational_patterns(change, success_score, lessons)

        self.logger.info(
            f"Change impact assessed: {change_id} (score: {success_score:.2f})"
        )
        return success_score

    def get_change_predictions(self, context: str) -> List[Dict[str, Any]]:
        """Predict potential organizational changes based on context"""

        predictions = []

        # Analyze context for change indicators
        change_indicators = self._detect_change_indicators(context)

        for indicator in change_indicators:
            # Find similar historical patterns
            similar_patterns = self._find_similar_patterns(indicator)

            # Generate prediction
            prediction = {
                "change_type": indicator["type"],
                "probability": indicator["confidence"],
                "predicted_impact": indicator["impact_areas"],
                "similar_patterns": similar_patterns,
                "recommendations": self._generate_change_recommendations(indicator),
            }
            predictions.append(prediction)

        return predictions

    def _generate_change_id(self, change_type: str, description: str) -> str:
        """Generate unique change ID"""
        content = f"{change_type}:{description}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _analyze_impact_areas(
        self, description: str, stakeholders: List[str]
    ) -> List[str]:
        """Analyze potential impact areas from change description"""

        impact_areas = set()

        # Keyword-based impact detection
        description_lower = description.lower()

        if any(
            word in description_lower for word in ["team", "structure", "org", "report"]
        ):
            impact_areas.add("organizational_structure")

        if any(
            word in description_lower for word in ["process", "workflow", "procedure"]
        ):
            impact_areas.add("operational_processes")

        if any(word in description_lower for word in ["culture", "value", "behavior"]):
            impact_areas.add("organizational_culture")

        if any(word in description_lower for word in ["technology", "system", "tool"]):
            impact_areas.add("technological_infrastructure")

        if any(word in description_lower for word in ["strategy", "goal", "objective"]):
            impact_areas.add("strategic_direction")

        # Stakeholder-based impact
        if len(stakeholders) > 10:
            impact_areas.add("cross_functional_coordination")

        return list(impact_areas) if impact_areas else ["general_organizational"]

    def _create_implementation_timeline(self, change_type: str) -> Dict[str, datetime]:
        """Create implementation timeline based on change type"""

        now = datetime.now()

        # Timeline patterns by change type
        timelines = {
            "structural": {
                "planning_start": now,
                "communication": now + timedelta(weeks=1),
                "implementation": now + timedelta(weeks=4),
                "stabilization": now + timedelta(weeks=12),
            },
            "cultural": {
                "planning_start": now,
                "pilot_program": now + timedelta(weeks=2),
                "rollout": now + timedelta(weeks=8),
                "evaluation": now + timedelta(weeks=26),
            },
            "strategic": {
                "planning_start": now,
                "stakeholder_alignment": now + timedelta(weeks=2),
                "execution": now + timedelta(weeks=6),
                "review": now + timedelta(weeks=13),
            },
            "technological": {
                "planning_start": now,
                "development": now + timedelta(weeks=3),
                "deployment": now + timedelta(weeks=8),
                "adoption": now + timedelta(weeks=16),
            },
        }

        return timelines.get(change_type, timelines["strategic"])

    def _initialize_success_metrics(
        self, change_type: str, expected_impact: Dict[str, Any]
    ) -> Dict[str, float]:
        """Initialize success metrics for change tracking"""

        base_metrics = {
            "stakeholder_satisfaction": 0.0,
            "implementation_speed": 0.0,
            "outcome_quality": 0.0,
            "risk_mitigation": 0.0,
        }

        # Add change-type specific metrics
        if change_type == "structural":
            base_metrics.update({"coordination_efficiency": 0.0, "role_clarity": 0.0})
        elif change_type == "cultural":
            base_metrics.update({"cultural_alignment": 0.0, "behavior_adoption": 0.0})
        elif change_type == "technological":
            base_metrics.update(
                {"system_adoption": 0.0, "performance_improvement": 0.0}
            )

        return base_metrics

    def _calculate_change_confidence(
        self, change_type: str, impact_areas: List[str]
    ) -> float:
        """Calculate confidence score for change prediction"""

        # Base confidence by change type
        base_confidence = {
            "structural": 0.8,
            "cultural": 0.6,
            "strategic": 0.7,
            "technological": 0.8,
        }.get(change_type, 0.7)

        # Adjust based on impact complexity
        complexity_penalty = min(len(impact_areas) * 0.05, 0.2)

        return max(0.1, base_confidence - complexity_penalty)

    def _calculate_success_score(
        self, expected_metrics: Dict[str, float], actual_outcomes: Dict[str, Any]
    ) -> float:
        """Calculate change success score based on outcomes"""

        scores = []

        for metric, expected_value in expected_metrics.items():
            if metric in actual_outcomes:
                actual_value = actual_outcomes[metric]
                if isinstance(actual_value, (int, float)):
                    # Calculate relative success (0.0 to 1.0)
                    if expected_value > 0:
                        score = min(1.0, actual_value / expected_value)
                    else:
                        score = 1.0 if actual_value >= 0 else 0.0
                    scores.append(score)

        return sum(scores) / len(scores) if scores else 0.5

    def _extract_lessons_learned(
        self,
        change: OrganizationalChange,
        outcomes: Dict[str, Any],
        success_score: float,
    ) -> List[str]:
        """Extract lessons learned from change implementation"""

        lessons = []

        if success_score >= 0.8:
            lessons.append(
                f"High success in {change.change_type} change - replicate approach"
            )
            lessons.append("Strong stakeholder alignment contributed to success")
        elif success_score >= 0.6:
            lessons.append(
                f"Moderate success in {change.change_type} change - identify improvement areas"
            )
        else:
            lessons.append(
                f"Challenges in {change.change_type} change - review approach"
            )
            lessons.append("Consider additional stakeholder support in future changes")

        # Timeline-based lessons
        if (
            "implementation_speed" in outcomes
            and outcomes["implementation_speed"] < 0.7
        ):
            lessons.append("Timeline management needs improvement for future changes")

        return lessons

    def _update_organizational_patterns(
        self, change: OrganizationalChange, success_score: float, lessons: List[str]
    ):
        """Update organizational patterns based on change outcomes"""

        pattern_type = (
            "success"
            if success_score >= 0.7
            else "failure" if success_score < 0.5 else "mixed"
        )

        pattern_key = f"{change.change_type}_{pattern_type}"

        if pattern_key not in self.change_patterns:
            self.change_patterns[pattern_key] = []

        self.change_patterns[pattern_key].extend(lessons)

    def _detect_change_indicators(self, context: str) -> List[Dict[str, Any]]:
        """Detect potential change indicators from context"""

        indicators = []
        context_lower = context.lower()

        # Structural change indicators
        if any(
            word in context_lower
            for word in ["reorganize", "restructure", "team change"]
        ):
            indicators.append(
                {
                    "type": "structural",
                    "confidence": 0.8,
                    "impact_areas": [
                        "organizational_structure",
                        "cross_functional_coordination",
                    ],
                }
            )

        # Cultural change indicators
        if any(word in context_lower for word in ["culture", "values", "behavior"]):
            indicators.append(
                {
                    "type": "cultural",
                    "confidence": 0.7,
                    "impact_areas": ["organizational_culture", "behavioral_patterns"],
                }
            )

        # Strategic change indicators
        if any(word in context_lower for word in ["strategy", "direction", "goals"]):
            indicators.append(
                {
                    "type": "strategic",
                    "confidence": 0.8,
                    "impact_areas": ["strategic_direction", "goal_alignment"],
                }
            )

        return indicators

    def _find_similar_patterns(self, indicator: Dict[str, Any]) -> List[str]:
        """Find similar historical patterns"""

        change_type = indicator["type"]
        similar_patterns = []

        for pattern_key, lessons in self.change_patterns.items():
            if change_type in pattern_key:
                similar_patterns.extend(lessons[:2])  # Top 2 lessons

        return similar_patterns

    def _generate_change_recommendations(self, indicator: Dict[str, Any]) -> List[str]:
        """Generate recommendations for predicted change"""

        change_type = indicator["type"]

        recommendations = {
            "structural": [
                "Ensure clear communication of new structure to all stakeholders",
                "Plan for 3-month transition period with regular check-ins",
                "Identify and address coordination challenges early",
            ],
            "cultural": [
                "Start with pilot groups to test cultural initiatives",
                "Provide clear examples and role models for desired behaviors",
                "Plan for 6+ month timeline for meaningful cultural change",
            ],
            "strategic": [
                "Align all stakeholders on strategic vision before implementation",
                "Break down strategy into concrete, measurable objectives",
                "Establish regular review and adjustment cycles",
            ],
            "technological": [
                "Conduct thorough impact assessment before deployment",
                "Plan comprehensive training and support programs",
                "Implement gradual rollout with feedback loops",
            ],
        }

        return recommendations.get(
            change_type, ["Conduct thorough planning and stakeholder analysis"]
        )


class CulturalContextAnalyzer:
    """Analyze organizational culture and adapt framework applicability"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.CulturalContextAnalyzer")

        # Cultural dimensions tracking
        self.cultural_dimensions: Dict[str, CulturalDimension] = {}
        self.framework_adjustments: Dict[str, Dict[str, float]] = {}

        # Performance targets
        self.max_analysis_time = self.config.get(
            "max_analysis_time", 1.0
        )  # Real-time target

    def analyze_cultural_context(
        self, context: str, stakeholder_data: Dict[str, Any]
    ) -> Dict[str, CulturalDimension]:
        """Analyze cultural context from conversation and stakeholder data"""

        start_time = datetime.now()

        # Detect cultural indicators
        cultural_indicators = self._detect_cultural_indicators(
            context, stakeholder_data
        )

        # Update cultural dimensions
        for dimension_name, score_data in cultural_indicators.items():
            self._update_cultural_dimension(dimension_name, score_data)

        # Performance check
        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed > self.max_analysis_time:
            self.logger.warning(
                f"Cultural analysis exceeded {self.max_analysis_time}s: {elapsed:.2f}s"
            )

        return self.cultural_dimensions

    def adapt_framework_recommendations(
        self, framework_name: str, cultural_context: Dict[str, CulturalDimension]
    ) -> float:
        """Adapt framework applicability based on cultural context"""

        if not cultural_context:
            return 1.0  # No adjustment if no cultural data

        # Framework-specific cultural adjustments
        adjustments = self._get_framework_cultural_adjustments(framework_name)

        total_adjustment = 1.0

        for dimension_name, dimension in cultural_context.items():
            if dimension_name in adjustments:
                adjustment_factor = adjustments[dimension_name]

                # Apply adjustment based on dimension score
                if dimension.score > 0.7:  # High dimension score
                    total_adjustment *= 1.0 + adjustment_factor * 0.3
                elif dimension.score < 0.3:  # Low dimension score
                    total_adjustment *= 1.0 - adjustment_factor * 0.3

        # Ensure adjustment stays within reasonable bounds
        return max(0.3, min(1.7, total_adjustment))

    def _detect_cultural_indicators(
        self, context: str, stakeholder_data: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Detect cultural dimension indicators from context"""

        indicators = {}
        context_lower = context.lower()

        # Power Distance indicators
        if any(
            word in context_lower
            for word in ["hierarchy", "approval", "authority", "executive"]
        ):
            indicators["power_distance"] = {
                "score": 0.7,
                "confidence": 0.6,
                "evidence": ["hierarchical language detected"],
            }

        # Uncertainty Avoidance indicators
        if any(
            word in context_lower
            for word in ["risk", "procedure", "process", "standard"]
        ):
            indicators["uncertainty_avoidance"] = {
                "score": 0.6,
                "confidence": 0.5,
                "evidence": ["process-oriented language detected"],
            }

        # Individualism vs Collectivism
        if any(
            word in context_lower
            for word in ["team", "collaboration", "together", "collective"]
        ):
            indicators["collectivism"] = {
                "score": 0.7,
                "confidence": 0.6,
                "evidence": ["collaborative language detected"],
            }
        elif any(
            word in context_lower
            for word in ["individual", "personal", "own", "independent"]
        ):
            indicators["individualism"] = {
                "score": 0.7,
                "confidence": 0.6,
                "evidence": ["individualistic language detected"],
            }

        return indicators

    def _update_cultural_dimension(
        self, dimension_name: str, score_data: Dict[str, Any]
    ):
        """Update or create cultural dimension"""

        if dimension_name in self.cultural_dimensions:
            # Update existing dimension
            dimension = self.cultural_dimensions[dimension_name]

            # Weighted average with existing score
            new_score = dimension.score * 0.7 + score_data["score"] * 0.3
            new_confidence = max(dimension.confidence, score_data["confidence"])

            dimension.score = new_score
            dimension.confidence = new_confidence
            dimension.evidence_sources.extend(score_data.get("evidence", []))
            dimension.last_updated = datetime.now()

            # Determine trend
            score_change = score_data["score"] - dimension.score
            if score_change > 0.1:
                dimension.trend_direction = "increasing"
            elif score_change < -0.1:
                dimension.trend_direction = "decreasing"
            else:
                dimension.trend_direction = "stable"
        else:
            # Create new dimension
            self.cultural_dimensions[dimension_name] = CulturalDimension(
                dimension_name=dimension_name,
                score=score_data["score"],
                confidence=score_data["confidence"],
                evidence_sources=score_data.get("evidence", []),
                trend_direction="stable",
                framework_adjustments={},
            )

    def _get_framework_cultural_adjustments(
        self, framework_name: str
    ) -> Dict[str, float]:
        """Get framework-specific cultural adjustments"""

        # Framework cultural sensitivity mappings
        framework_adjustments = {
            "team_topologies": {
                "power_distance": -0.3,  # Less effective in high power distance cultures
                "collectivism": 0.4,  # More effective in collectivist cultures
                "uncertainty_avoidance": -0.2,
            },
            "wrap_framework": {
                "uncertainty_avoidance": 0.3,  # More effective with structured decision making
                "individualism": 0.2,
                "power_distance": 0.1,
            },
            "crucial_conversations": {
                "power_distance": -0.4,  # Challenging in hierarchical cultures
                "individualism": 0.3,
                "uncertainty_avoidance": -0.2,
            },
            "capital_allocation": {
                "uncertainty_avoidance": 0.2,
                "power_distance": 0.1,
                "long_term_orientation": 0.3,
            },
        }

        return framework_adjustments.get(framework_name, {})


class OrganizationalLearningEngine:
    """
    Main orchestration for Phase 3.1 organizational learning capabilities

    Integrates with Context Engineering system following OVERVIEW.md architecture:
    - Built on AnalyticsEngine foundation from Phase 2.2
    - Follows unified bridge pattern
    - Maintains <3s performance targets
    - Provides complete audit trails
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.OrganizationalLearningEngine")

        # Initialize sub-components
        self.change_tracker = OrganizationalChangeTracker(
            self.config.get("change_tracking", {})
        )
        self.cultural_analyzer = CulturalContextAnalyzer(
            self.config.get("cultural_analysis", {})
        )

        # Performance targets per OVERVIEW.md
        self.max_response_time = self.config.get("max_response_time", 3.0)
        self.transparency_enabled = self.config.get("transparency_enabled", True)

        # Integration with existing Context Engineering
        self.analytics_engine: Optional[AnalyticsEngine] = None

        self.logger.info("OrganizationalLearningEngine initialized for Phase 3.1")

    def set_analytics_integration(self, analytics_engine: AnalyticsEngine):
        """Integrate with Phase 2.2 AnalyticsEngine"""
        self.analytics_engine = analytics_engine
        self.logger.info("Analytics Engine integration established")

    def analyze_organizational_context(
        self,
        context: str,
        stakeholder_data: Dict[str, Any],
        strategic_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Comprehensive organizational context analysis

        Returns organizational insights including:
        - Change predictions and recommendations
        - Cultural context analysis
        - Framework adaptation suggestions
        - Organizational patterns
        """

        start_time = datetime.now()

        try:
            # Cultural analysis (real-time target)
            cultural_dimensions = self.cultural_analyzer.analyze_cultural_context(
                context, stakeholder_data
            )

            # Change prediction analysis
            change_predictions = self.change_tracker.get_change_predictions(context)

            # Framework adaptation recommendations
            framework_adaptations = self._generate_framework_adaptations(
                cultural_dimensions, strategic_context
            )

            # Organizational pattern insights
            pattern_insights = self._extract_pattern_insights(
                context, cultural_dimensions, change_predictions
            )

            # Compile results
            results = {
                "cultural_dimensions": {
                    name: asdict(dimension)
                    for name, dimension in cultural_dimensions.items()
                },
                "change_predictions": change_predictions,
                "framework_adaptations": framework_adaptations,
                "pattern_insights": pattern_insights,
                "analysis_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "confidence": self._calculate_overall_confidence(
                        cultural_dimensions, change_predictions
                    ),
                    "performance_time": (datetime.now() - start_time).total_seconds(),
                },
            }

            # Performance check per OVERVIEW.md
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > self.max_response_time:
                self.logger.warning(
                    f"Organizational analysis exceeded {self.max_response_time}s: {elapsed:.2f}s"
                )

            # Transparency logging per OVERVIEW.md principles
            if self.transparency_enabled:
                self.logger.info(
                    f"Organizational analysis completed: {len(change_predictions)} predictions, {len(cultural_dimensions)} cultural dimensions"
                )

            return results

        except Exception as e:
            self.logger.error(f"Organizational analysis failed: {e}")
            return {
                "error": str(e),
                "fallback_recommendations": self._get_fallback_recommendations(),
            }

    def track_organizational_change(
        self,
        change_description: str,
        change_type: str,
        stakeholders: List[str],
        expected_outcomes: Dict[str, Any],
    ) -> str:
        """Track a new organizational change"""

        change = self.change_tracker.track_organizational_change(
            change_type=change_type,
            description=change_description,
            stakeholders=stakeholders,
            expected_impact=expected_outcomes,
        )

        return change.change_id

    def assess_change_outcome(
        self, change_id: str, actual_outcomes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess the outcome of an organizational change"""

        success_score = self.change_tracker.assess_change_impact(
            change_id, actual_outcomes
        )

        return {
            "change_id": change_id,
            "success_score": success_score,
            "assessment_timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_outcome_recommendations(success_score),
        }

    def get_cultural_framework_adaptation(self, framework_name: str) -> float:
        """Get cultural adaptation factor for a specific framework"""

        return self.cultural_analyzer.adapt_framework_recommendations(
            framework_name, self.cultural_analyzer.cultural_dimensions
        )

    def _generate_framework_adaptations(
        self,
        cultural_dimensions: Dict[str, CulturalDimension],
        strategic_context: Dict[str, Any],
    ) -> Dict[str, float]:
        """Generate framework adaptation recommendations"""

        adaptations = {}

        # Common frameworks to evaluate
        frameworks = [
            "team_topologies",
            "wrap_framework",
            "crucial_conversations",
            "capital_allocation",
            "accelerate",
            "platform_strategy",
        ]

        for framework in frameworks:
            adaptation_factor = self.cultural_analyzer.adapt_framework_recommendations(
                framework, cultural_dimensions
            )
            adaptations[framework] = adaptation_factor

        return adaptations

    def _extract_pattern_insights(
        self,
        context: str,
        cultural_dimensions: Dict[str, CulturalDimension],
        change_predictions: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Extract organizational pattern insights"""

        insights = []

        # Cultural pattern insights
        for dimension_name, dimension in cultural_dimensions.items():
            if dimension.confidence > 0.6:
                insight = {
                    "type": "cultural_pattern",
                    "pattern": f"Strong {dimension_name} tendency",
                    "confidence": dimension.confidence,
                    "implications": self._get_cultural_implications(
                        dimension_name, dimension.score
                    ),
                    "trend": dimension.trend_direction,
                }
                insights.append(insight)

        # Change pattern insights
        if change_predictions:
            high_probability_changes = [
                pred for pred in change_predictions if pred.get("probability", 0) > 0.7
            ]

            if high_probability_changes:
                insight = {
                    "type": "change_pattern",
                    "pattern": f"High probability of {len(high_probability_changes)} organizational changes",
                    "confidence": max(
                        pred.get("probability", 0) for pred in high_probability_changes
                    ),
                    "implications": [
                        "Proactive change management needed",
                        "Stakeholder communication critical",
                    ],
                    "affected_areas": list(
                        set(
                            area
                            for pred in high_probability_changes
                            for area in pred.get("predicted_impact", [])
                        )
                    ),
                }
                insights.append(insight)

        return insights

    def _calculate_overall_confidence(
        self,
        cultural_dimensions: Dict[str, CulturalDimension],
        change_predictions: List[Dict[str, Any]],
    ) -> float:
        """Calculate overall confidence score for organizational analysis"""

        confidences = []

        # Cultural confidence
        for dimension in cultural_dimensions.values():
            confidences.append(dimension.confidence)

        # Change prediction confidence
        for prediction in change_predictions:
            confidences.append(prediction.get("probability", 0.5))

        return sum(confidences) / len(confidences) if confidences else 0.5

    def _get_cultural_implications(
        self, dimension_name: str, score: float
    ) -> List[str]:
        """Get implications for cultural dimension scores"""

        implications_map = {
            "power_distance": {
                "high": [
                    "Top-down decision making preferred",
                    "Formal approval processes important",
                ],
                "low": [
                    "Collaborative decision making effective",
                    "Flat organizational structures work well",
                ],
            },
            "uncertainty_avoidance": {
                "high": [
                    "Structured approaches preferred",
                    "Clear procedures and standards needed",
                ],
                "low": [
                    "Flexible, adaptive approaches work well",
                    "Innovation and experimentation valued",
                ],
            },
            "individualism": {
                "high": [
                    "Individual recognition important",
                    "Personal accountability emphasized",
                ],
                "low": [
                    "Team recognition preferred",
                    "Collective responsibility valued",
                ],
            },
            "collectivism": {
                "high": ["Group harmony important", "Consensus building critical"],
                "low": [
                    "Individual initiative valued",
                    "Direct communication acceptable",
                ],
            },
        }

        level = "high" if score > 0.6 else "low"
        return implications_map.get(dimension_name, {}).get(
            level, ["Context-specific approach recommended"]
        )

    def _generate_outcome_recommendations(self, success_score: float) -> List[str]:
        """Generate recommendations based on change outcome assessment"""

        if success_score >= 0.8:
            return [
                "Excellent change outcome - document and replicate approach",
                "Share success patterns with other teams",
                "Consider scaling successful practices",
            ]
        elif success_score >= 0.6:
            return [
                "Good change outcome with room for improvement",
                "Analyze what worked well and enhance for future changes",
                "Address any remaining stakeholder concerns",
            ]
        else:
            return [
                "Change outcome below expectations - comprehensive review needed",
                "Conduct stakeholder feedback sessions",
                "Develop improvement plan for future organizational changes",
                "Consider additional support or resources",
            ]

    def _get_fallback_recommendations(self) -> List[str]:
        """Provide fallback recommendations when analysis fails"""

        return [
            "Conduct stakeholder analysis to understand organizational dynamics",
            "Assess current cultural patterns and change readiness",
            "Develop communication plan for any organizational changes",
            "Establish feedback mechanisms for continuous improvement",
        ]
