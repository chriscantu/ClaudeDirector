"""
Framework Selector for Context-Aware Intelligence

Selects optimal strategic frameworks based on situational context
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import logging
from .context_analyzer import ContextComplexity, SituationalContext


@dataclass
class ContextualFrameworkRecommendation:
    """Contextually optimized framework recommendation"""

    framework_name: str
    confidence_score: float  # 0.0 to 1.0
    relevance_score: float  # 0.0 to 1.0
    situational_fit: float  # 0.0 to 1.0

    # Context analysis
    context_complexity: ContextComplexity
    situational_context: SituationalContext
    stakeholder_involvement: List[str]
    time_sensitivity: str  # immediate, short_term, long_term

    # Application guidance
    key_focus_areas: List[str]
    adaptation_suggestions: List[str]
    success_metrics: List[str]

    # Performance metadata
    selection_timestamp: datetime
    analysis_duration_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "framework_name": self.framework_name,
            "confidence_score": self.confidence_score,
            "relevance_score": self.relevance_score,
            "situational_fit": self.situational_fit,
            "context_complexity": self.context_complexity.value,
            "situational_context": self.situational_context.value,
            "stakeholder_involvement": self.stakeholder_involvement,
            "time_sensitivity": self.time_sensitivity,
            "key_focus_areas": self.key_focus_areas,
            "adaptation_suggestions": self.adaptation_suggestions,
            "success_metrics": self.success_metrics,
            "selection_timestamp": self.selection_timestamp.isoformat(),
            "analysis_duration_ms": self.analysis_duration_ms,
        }


class FrameworkSelector:
    """Selects optimal strategic frameworks based on context analysis"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self._initialize_framework_mappings()

    def _initialize_framework_mappings(self):
        """Initialize framework situation and relevance mappings"""
        self.framework_situation_map = {
            SituationalContext.CRISIS_RESPONSE: [
                "Crucial Conversations",
                "WRAP Framework",
                "Team Topologies",
            ],
            SituationalContext.STRATEGIC_PLANNING: [
                "Good Strategy Bad Strategy",
                "Strategic Analysis Framework",
                "Capital Allocation Framework",
            ],
            SituationalContext.TEAM_COORDINATION: [
                "Team Topologies",
                "Scaling Up Excellence",
                "Organizational Design",
            ],
            SituationalContext.STAKEHOLDER_ALIGNMENT: [
                "Crucial Conversations",
                "Stakeholder Analysis",
                "Communication Strategy",
            ],
            SituationalContext.TECHNICAL_DECISION: [
                "Technical Strategy Framework",
                "ADR Patterns",
                "Evolutionary Architecture",
            ],
            SituationalContext.EXECUTIVE_COMMUNICATION: [
                "Strategic Analysis Framework",
                "Business Model Canvas",
                "Executive Communication",
            ],
        }

        self.framework_relevance = {
            "Team Topologies": {
                "domains": ["organizational", "technical"],
                "situations": [
                    SituationalContext.TEAM_COORDINATION,
                    SituationalContext.ORGANIZATIONAL_CHANGE,
                ],
            },
            "Good Strategy Bad Strategy": {
                "domains": ["strategic", "executive"],
                "situations": [
                    SituationalContext.STRATEGIC_PLANNING,
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                ],
            },
            "Crucial Conversations": {
                "domains": ["stakeholder", "organizational"],
                "situations": [
                    SituationalContext.STAKEHOLDER_ALIGNMENT,
                    SituationalContext.CRISIS_RESPONSE,
                ],
            },
            "Strategic Analysis Framework": {
                "domains": ["strategic", "executive"],
                "situations": [
                    SituationalContext.STRATEGIC_PLANNING,
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                ],
            },
        }

        self.framework_focus = {
            "Team Topologies": [
                "team_structure",
                "cognitive_load",
                "communication_patterns",
            ],
            "Good Strategy Bad Strategy": [
                "strategy_kernel",
                "strategic_objectives",
                "competitive_advantage",
            ],
            "Crucial Conversations": [
                "difficult_conversations",
                "stakeholder_alignment",
                "conflict_resolution",
            ],
            "Strategic Analysis Framework": [
                "situation_analysis",
                "strategic_options",
                "decision_criteria",
            ],
            "Capital Allocation Framework": [
                "resource_allocation",
                "investment_priorities",
                "roi_analysis",
            ],
        }

        self.framework_metrics = {
            "Team Topologies": [
                "Reduced cross-team dependencies",
                "Improved team autonomy scores",
                "Decreased cognitive load indicators",
            ],
            "Good Strategy Bad Strategy": [
                "Clear strategic objectives defined",
                "Stakeholder alignment on strategy",
                "Measurable strategic progress",
            ],
            "Crucial Conversations": [
                "Successful difficult conversation outcomes",
                "Improved stakeholder relationships",
                "Reduced conflict incidents",
            ],
            "Strategic Analysis Framework": [
                "Comprehensive situation analysis completed",
                "Strategic options identified and evaluated",
                "Clear decision criteria established",
            ],
        }

    def recommend_optimal_framework(
        self,
        context_analysis: Dict[str, Any],
        framework_detector_results: List[Dict] = None,
    ) -> ContextualFrameworkRecommendation:
        """Recommend optimal framework based on strategic context analysis"""

        situational_context = context_analysis["situational_context"]
        complexity_level = context_analysis["complexity_level"]
        stakeholder_analysis = context_analysis["stakeholder_analysis"]

        # Get situational framework candidates
        framework_candidates = self.framework_situation_map.get(
            situational_context, ["Strategic Analysis Framework"]
        )

        # Score frameworks based on context fit
        framework_scores = {}
        for framework in framework_candidates:
            score = self._calculate_framework_context_fit(
                framework, situational_context, complexity_level, stakeholder_analysis
            )
            framework_scores[framework] = score

        # Include detected frameworks with context scoring
        if framework_detector_results:
            for detection in framework_detector_results:
                framework_name = detection.get("framework_name", "")
                if framework_name and framework_name not in framework_scores:
                    base_score = detection.get("confidence", 0.5)
                    context_score = self._calculate_framework_context_fit(
                        framework_name,
                        situational_context,
                        complexity_level,
                        stakeholder_analysis,
                    )
                    framework_scores[framework_name] = (base_score + context_score) / 2

        # Select best framework
        if framework_scores:
            best_framework = max(framework_scores.items(), key=lambda x: x[1])
            framework_name, confidence_score = best_framework
        else:
            framework_name = "Strategic Analysis Framework"
            confidence_score = 0.7

        # Generate contextual recommendation
        return ContextualFrameworkRecommendation(
            framework_name=framework_name,
            confidence_score=confidence_score,
            relevance_score=self._calculate_relevance_score(
                framework_name, context_analysis
            ),
            situational_fit=self._calculate_situational_fit(
                framework_name, situational_context
            ),
            context_complexity=complexity_level,
            situational_context=situational_context,
            stakeholder_involvement=stakeholder_analysis.get("primary", []),
            time_sensitivity=context_analysis["time_sensitivity"],
            key_focus_areas=self._identify_framework_focus_areas(
                framework_name, context_analysis
            ),
            adaptation_suggestions=self._generate_framework_adaptations(
                framework_name, context_analysis
            ),
            success_metrics=self._define_framework_success_metrics(
                framework_name, situational_context
            ),
            selection_timestamp=datetime.now(),
            analysis_duration_ms=0.0,  # Will be set by caller
        )

    def _calculate_framework_context_fit(
        self,
        framework_name: str,
        situational_context: SituationalContext,
        complexity_level: ContextComplexity,
        stakeholder_analysis: Dict[str, Any],
    ) -> float:
        """Calculate how well a framework fits the context"""

        # Base score from situational mapping
        situational_frameworks = self.framework_situation_map.get(
            situational_context, []
        )
        if framework_name in situational_frameworks:
            base_score = 0.8
        else:
            base_score = 0.4

        # Complexity adjustment
        complexity_bonus = {
            ContextComplexity.SIMPLE: 0.0,
            ContextComplexity.MODERATE: 0.1,
            ContextComplexity.COMPLEX: 0.15,
            ContextComplexity.ENTERPRISE: 0.2,
        }.get(complexity_level, 0.0)

        # Stakeholder count adjustment
        stakeholder_count = stakeholder_analysis.get("total_count", 1)
        if stakeholder_count > 3:
            stakeholder_bonus = 0.1
        else:
            stakeholder_bonus = 0.0

        return min(1.0, base_score + complexity_bonus + stakeholder_bonus)

    def _calculate_relevance_score(
        self, framework_name: str, context_analysis: Dict[str, Any]
    ) -> float:
        """Calculate framework relevance to specific context"""

        framework_config = self.framework_relevance.get(framework_name, {})
        if not framework_config:
            return 0.5  # Default relevance

        # Domain match
        primary_domain = context_analysis.get("query_characteristics", {}).get(
            "primary_domain", "strategic"
        )
        relevant_domains = framework_config.get("domains", [])
        domain_match = 1.0 if primary_domain in relevant_domains else 0.3

        # Situation match
        situational_context = context_analysis.get("situational_context")
        relevant_situations = framework_config.get("situations", [])
        situation_match = 1.0 if situational_context in relevant_situations else 0.3

        return (domain_match + situation_match) / 2

    def _calculate_situational_fit(
        self, framework_name: str, situational_context: SituationalContext
    ) -> float:
        """Calculate how well framework fits the specific situation"""

        situational_frameworks = self.framework_situation_map.get(
            situational_context, []
        )
        if framework_name in situational_frameworks:
            # Get position in list (earlier = better fit)
            position = situational_frameworks.index(framework_name)
            return 1.0 - (position * 0.1)  # Decrease by 0.1 for each position

        return 0.5  # Default fit

    def _identify_framework_focus_areas(
        self, framework_name: str, context_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify key focus areas for framework application"""
        default_focus = ["strategic_analysis", "framework_application"]
        return self.framework_focus.get(framework_name, default_focus)

    def _generate_framework_adaptations(
        self, framework_name: str, context_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate framework adaptation suggestions"""

        complexity_level = context_analysis.get(
            "complexity_level", ContextComplexity.MODERATE
        )
        time_sensitivity = context_analysis.get("time_sensitivity", "short_term")

        adaptations = []

        # Complexity-based adaptations
        if complexity_level == ContextComplexity.ENTERPRISE:
            adaptations.append(
                "Scale framework application across multiple stakeholder groups"
            )
            adaptations.append(
                "Include executive communication and change management elements"
            )
        elif complexity_level == ContextComplexity.SIMPLE:
            adaptations.append(
                "Simplify framework application for focused team context"
            )

        # Time-sensitive adaptations
        if time_sensitivity == "immediate":
            adaptations.append("Focus on immediate actionable elements of framework")
            adaptations.append("Defer comprehensive analysis for rapid decision making")
        elif time_sensitivity == "long_term":
            adaptations.append(
                "Include comprehensive strategic analysis and planning phases"
            )

        # Framework-specific adaptations
        if framework_name == "Team Topologies":
            adaptations.append(
                "Assess current team cognitive load and communication patterns"
            )
        elif framework_name == "Good Strategy Bad Strategy":
            adaptations.append("Develop clear strategy kernel with specific objectives")

        return adaptations or ["Apply framework systematically with context awareness"]

    def _define_framework_success_metrics(
        self, framework_name: str, situational_context: SituationalContext
    ) -> List[str]:
        """Define success metrics for framework application"""

        # Framework-specific metrics
        metrics = self.framework_metrics.get(
            framework_name, ["Framework application success"]
        )

        # Situational metrics
        situational_metrics = {
            SituationalContext.CRISIS_RESPONSE: [
                "Crisis resolution time",
                "Stakeholder confidence restoration",
            ],
            SituationalContext.TEAM_COORDINATION: [
                "Team collaboration effectiveness",
                "Communication frequency",
            ],
            SituationalContext.EXECUTIVE_COMMUNICATION: [
                "Executive understanding",
                "Decision clarity",
            ],
        }

        metrics.extend(situational_metrics.get(situational_context, []))
        return list(set(metrics))  # Remove duplicates
