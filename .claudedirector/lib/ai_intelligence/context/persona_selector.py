"""
Persona Selector for Context-Aware Intelligence

Selects optimal personas based on strategic context analysis
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from .context_analyzer import ContextComplexity, SituationalContext


@dataclass
class PersonaActivationRecommendation:
    """Optimal persona selection based on context"""

    recommended_persona: str
    activation_confidence: float  # 0.0 to 1.0
    context_alignment: float  # 0.0 to 1.0

    # Context factors
    domain_expertise_match: float
    stakeholder_preference_match: float
    communication_style_match: float

    # Coordination guidance
    supporting_personas: List[str]
    collaboration_strategy: str
    escalation_path: Optional[str]

    # Performance tracking
    selection_reasoning: List[str]
    alternative_personas: List[Dict[str, float]]


class PersonaSelector:
    """Selects optimal personas based on context analysis"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self._initialize_persona_mappings()

    def _initialize_persona_mappings(self):
        """Initialize persona expertise and preference mappings"""
        self.persona_expertise = {
            "diego": {
                "domains": [
                    "engineering_leadership",
                    "platform_strategy",
                    "team_coordination",
                ],
                "situations": [
                    SituationalContext.TEAM_COORDINATION,
                    SituationalContext.STRATEGIC_PLANNING,
                ],
                "complexity_preference": [
                    ContextComplexity.COMPLEX,
                    ContextComplexity.ENTERPRISE,
                ],
                "communication_style": "direct_strategic",
            },
            "camille": {
                "domains": [
                    "strategic_technology",
                    "organizational_scaling",
                    "executive_advisory",
                ],
                "situations": [
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                    SituationalContext.STRATEGIC_PLANNING,
                ],
                "complexity_preference": [
                    ContextComplexity.ENTERPRISE,
                    ContextComplexity.COMPLEX,
                ],
                "communication_style": "executive_strategic",
            },
            "rachel": {
                "domains": [
                    "design_systems",
                    "ux_leadership",
                    "cross_functional_alignment",
                ],
                "situations": [
                    SituationalContext.STAKEHOLDER_ALIGNMENT,
                    SituationalContext.PROCESS_OPTIMIZATION,
                ],
                "complexity_preference": [
                    ContextComplexity.MODERATE,
                    ContextComplexity.COMPLEX,
                ],
                "communication_style": "collaborative_design",
            },
            "alvaro": {
                "domains": [
                    "platform_investment",
                    "business_value",
                    "stakeholder_communication",
                ],
                "situations": [
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                    SituationalContext.STRATEGIC_PLANNING,
                ],
                "complexity_preference": [
                    ContextComplexity.ENTERPRISE,
                    ContextComplexity.COMPLEX,
                ],
                "communication_style": "business_strategic",
            },
            "martin": {
                "domains": [
                    "platform_architecture",
                    "technical_strategy",
                    "evolutionary_design",
                ],
                "situations": [
                    SituationalContext.TECHNICAL_DECISION,
                    SituationalContext.ORGANIZATIONAL_CHANGE,
                ],
                "complexity_preference": [
                    ContextComplexity.COMPLEX,
                    ContextComplexity.MODERATE,
                ],
                "communication_style": "technical_strategic",
            },
        }

    def recommend_optimal_persona(
        self, context_analysis: Dict[str, Any]
    ) -> PersonaActivationRecommendation:
        """Recommend optimal persona activation based on context analysis"""

        situational_context = context_analysis["situational_context"]
        complexity_level = context_analysis["complexity_level"]
        stakeholder_analysis = context_analysis["stakeholder_analysis"]

        # Score personas based on context fit
        persona_scores = {}
        persona_details = {}

        for persona_name, persona_config in self.persona_expertise.items():
            # Calculate domain expertise match
            domain_match = self._calculate_domain_expertise_match(
                persona_config, context_analysis
            )

            # Calculate situational context match
            situation_match = self._calculate_situational_match(
                persona_config, situational_context
            )

            # Calculate complexity preference match
            complexity_match = self._calculate_complexity_match(
                persona_config, complexity_level
            )

            # Calculate stakeholder preference match
            stakeholder_match = self._calculate_stakeholder_match(
                persona_config, stakeholder_analysis
            )

            # Calculate composite score
            composite_score = (
                domain_match * 0.3
                + situation_match * 0.3
                + complexity_match * 0.2
                + stakeholder_match * 0.2
            )

            persona_scores[persona_name] = composite_score
            persona_details[persona_name] = {
                "domain_match": domain_match,
                "situation_match": situation_match,
                "complexity_match": complexity_match,
                "stakeholder_match": stakeholder_match,
            }

        # Select best persona
        if persona_scores:
            best_persona = max(persona_scores.items(), key=lambda x: x[1])
            recommended_persona, activation_confidence = best_persona
        else:
            recommended_persona = "diego"  # Default to diego
            activation_confidence = 0.5

        # Calculate context alignment
        persona_detail = persona_details.get(recommended_persona, {})
        context_alignment = (
            persona_detail.get("domain_match", 0.5)
            + persona_detail.get("situation_match", 0.5)
        ) / 2

        # Identify supporting personas
        supporting_personas = [
            persona
            for persona, score in persona_scores.items()
            if persona != recommended_persona and score > 0.6
        ]

        # Generate collaboration strategy
        collaboration_strategy = self._generate_collaboration_strategy(
            recommended_persona, supporting_personas, context_analysis
        )

        # Generate selection reasoning
        selection_reasoning = self._generate_persona_reasoning(
            recommended_persona, persona_detail, context_analysis
        )

        # Prepare alternative personas
        alternative_personas = [
            {"persona": persona, "score": score}
            for persona, score in sorted(
                persona_scores.items(), key=lambda x: x[1], reverse=True
            )
            if persona != recommended_persona
        ][
            :3
        ]  # Top 3 alternatives

        return PersonaActivationRecommendation(
            recommended_persona=recommended_persona,
            activation_confidence=activation_confidence,
            context_alignment=context_alignment,
            domain_expertise_match=persona_detail.get("domain_match", 0.5),
            stakeholder_preference_match=persona_detail.get("stakeholder_match", 0.5),
            communication_style_match=persona_detail.get("situation_match", 0.5),
            supporting_personas=supporting_personas,
            collaboration_strategy=collaboration_strategy,
            escalation_path=self._determine_escalation_path(
                recommended_persona, complexity_level, stakeholder_analysis
            ),
            selection_reasoning=selection_reasoning,
            alternative_personas=alternative_personas,
        )

    def _calculate_domain_expertise_match(
        self, persona_config: Dict[str, Any], context_analysis: Dict[str, Any]
    ) -> float:
        """Calculate domain expertise match for persona"""

        primary_domain = context_analysis.get("query_characteristics", {}).get(
            "primary_domain", "strategic"
        )
        persona_domains = persona_config.get("domains", [])

        # Direct domain match
        if any(domain in primary_domain for domain in persona_domains):
            return 1.0

        # Partial domain match
        domain_keywords = {
            "engineering_leadership": ["technical", "organizational"],
            "strategic_technology": ["strategic", "technical"],
            "design_systems": ["technical", "stakeholder"],
            "platform_investment": ["strategic", "executive"],
            "platform_architecture": ["technical"],
        }

        for persona_domain in persona_domains:
            keywords = domain_keywords.get(persona_domain, [])
            if primary_domain in keywords:
                return 0.7

        return 0.3  # Default low match

    def _calculate_situational_match(
        self, persona_config: Dict[str, Any], situational_context: SituationalContext
    ) -> float:
        """Calculate situational context match for persona"""

        persona_situations = persona_config.get("situations", [])

        if situational_context in persona_situations:
            return 1.0

        # Related situation matching
        situation_groups = {
            "strategic": [
                SituationalContext.STRATEGIC_PLANNING,
                SituationalContext.EXECUTIVE_COMMUNICATION,
            ],
            "operational": [
                SituationalContext.TEAM_COORDINATION,
                SituationalContext.PROCESS_OPTIMIZATION,
            ],
            "interpersonal": [
                SituationalContext.STAKEHOLDER_ALIGNMENT,
                SituationalContext.CRISIS_RESPONSE,
            ],
        }

        for group_name, situations in situation_groups.items():
            if situational_context in situations:
                # Check if persona has any situations in this group
                if any(sit in persona_situations for sit in situations):
                    return 0.7

        return 0.3  # Default low match

    def _calculate_complexity_match(
        self, persona_config: Dict[str, Any], complexity_level: ContextComplexity
    ) -> float:
        """Calculate complexity preference match for persona"""

        persona_complexity_prefs = persona_config.get("complexity_preference", [])

        if complexity_level in persona_complexity_prefs:
            return 1.0

        # Adjacent complexity matching
        complexity_order = [
            ContextComplexity.SIMPLE,
            ContextComplexity.MODERATE,
            ContextComplexity.COMPLEX,
            ContextComplexity.ENTERPRISE,
        ]
        current_index = complexity_order.index(complexity_level)

        for pref in persona_complexity_prefs:
            pref_index = complexity_order.index(pref)
            if abs(current_index - pref_index) == 1:
                return 0.7

        return 0.5  # Default neutral match

    def _calculate_stakeholder_match(
        self, persona_config: Dict[str, Any], stakeholder_analysis: Dict[str, Any]
    ) -> float:
        """Calculate stakeholder preference match for persona"""

        stakeholder_count = stakeholder_analysis.get("total_count", 1)
        primary_stakeholders = stakeholder_analysis.get("primary", [])

        # High-level stakeholder indicators
        executive_stakeholders = ["vp_engineering", "cto", "executive_team"]
        has_executives = any(
            stakeholder in executive_stakeholders
            for stakeholder in primary_stakeholders
        )

        # Persona preferences for stakeholder types
        if (
            persona_config.get("communication_style") == "executive_strategic"
            and has_executives
        ):
            return 1.0
        elif (
            persona_config.get("communication_style") == "technical_strategic"
            and stakeholder_count <= 3
        ):
            return 0.9
        elif (
            persona_config.get("communication_style") == "collaborative_design"
            and stakeholder_count > 2
        ):
            return 0.8

        return 0.6  # Default reasonable match

    def _generate_collaboration_strategy(
        self,
        primary_persona: str,
        supporting_personas: List[str],
        context_analysis: Dict[str, Any],
    ) -> str:
        """Generate collaboration strategy for multiple personas"""

        if not supporting_personas:
            return f"Single persona approach with {primary_persona} leading strategic guidance"

        complexity_level = context_analysis.get(
            "complexity_level", ContextComplexity.MODERATE
        )

        if complexity_level == ContextComplexity.ENTERPRISE:
            return f"{primary_persona} leads with coordinated input from {', '.join(supporting_personas)} for comprehensive multi-domain analysis"
        elif len(supporting_personas) == 1:
            return f"{primary_persona} leads with {supporting_personas[0]} providing specialized domain expertise"
        else:
            return f"{primary_persona} coordinates strategic approach with {', '.join(supporting_personas[:2])} providing complementary perspectives"

    def _generate_persona_reasoning(
        self,
        persona_name: str,
        persona_detail: Dict[str, Any],
        context_analysis: Dict[str, Any],
    ) -> List[str]:
        """Generate reasoning for persona selection"""

        reasoning = []

        # Domain expertise reasoning
        domain_match = persona_detail.get("domain_match", 0)
        if domain_match > 0.8:
            reasoning.append(
                f"Strong domain expertise match ({domain_match:.1f}) for strategic context"
            )

        # Situational reasoning
        situation_match = persona_detail.get("situation_match", 0)
        if situation_match > 0.8:
            reasoning.append(
                f"Optimal situational context fit ({situation_match:.1f}) for current scenario"
            )

        # Complexity reasoning
        complexity_match = persona_detail.get("complexity_match", 0)
        if complexity_match > 0.8:
            reasoning.append(
                f"Appropriate complexity handling capability ({complexity_match:.1f})"
            )

        # Context-specific reasoning
        situational_context = context_analysis.get("situational_context")
        if situational_context == SituationalContext.EXECUTIVE_COMMUNICATION:
            reasoning.append(
                "Executive communication expertise required for stakeholder context"
            )
        elif situational_context == SituationalContext.TEAM_COORDINATION:
            reasoning.append(
                "Team coordination and organizational design expertise needed"
            )

        return reasoning or [f"Selected {persona_name} as default strategic persona"]

    def _determine_escalation_path(
        self,
        primary_persona: str,
        complexity_level: ContextComplexity,
        stakeholder_analysis: Dict[str, Any],
    ) -> Optional[str]:
        """Determine escalation path if needed"""

        # Executive escalation for high complexity or executive stakeholders
        executive_stakeholders = ["vp_engineering", "cto", "executive_team"]
        primary_stakeholders = stakeholder_analysis.get("primary", [])
        has_executives = any(
            stakeholder in executive_stakeholders
            for stakeholder in primary_stakeholders
        )

        if complexity_level == ContextComplexity.ENTERPRISE or has_executives:
            if primary_persona not in ["camille", "alvaro"]:
                return "Escalate to Camille or Alvaro for executive-level strategic guidance"

        # Cross-functional escalation for complex coordination
        if (
            complexity_level == ContextComplexity.COMPLEX
            and primary_persona == "martin"
        ):
            return "Consider Diego for organizational coordination if technical solution requires team changes"

        return None
