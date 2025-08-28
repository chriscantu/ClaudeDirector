"""
Context Analyzer for Strategic Intelligence

Analyzes strategic context to determine situation complexity and classification
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import logging


class ContextComplexity(Enum):
    """Strategic context complexity levels"""

    SIMPLE = "simple"  # Single domain, clear objectives
    MODERATE = "moderate"  # Multiple domains, some ambiguity
    COMPLEX = "complex"  # Cross-functional, high ambiguity
    ENTERPRISE = "enterprise"  # Multi-stakeholder, high stakes


class SituationalContext(Enum):
    """Types of strategic situations requiring different approaches"""

    CRISIS_RESPONSE = "crisis_response"
    STRATEGIC_PLANNING = "strategic_planning"
    TEAM_COORDINATION = "team_coordination"
    STAKEHOLDER_ALIGNMENT = "stakeholder_alignment"
    TECHNICAL_DECISION = "technical_decision"
    EXECUTIVE_COMMUNICATION = "executive_communication"
    PROCESS_OPTIMIZATION = "process_optimization"
    ORGANIZATIONAL_CHANGE = "organizational_change"


class ContextAnalyzer:
    """Analyzes strategic context to determine situation and complexity"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def analyze_query_characteristics(self, query: str) -> Dict[str, Any]:
        """Analyze query characteristics for context classification"""
        query_lower = query.lower()

        # Domain indicators
        domain_indicators = {
            "technical": ["architecture", "system", "code", "technical", "engineering"],
            "strategic": ["strategy", "planning", "roadmap", "vision", "goals"],
            "organizational": ["team", "people", "culture", "process", "organization"],
            "stakeholder": [
                "stakeholder",
                "communication",
                "alignment",
                "relationship",
            ],
            "executive": ["board", "vp", "executive", "leadership", "senior"],
        }

        domain_scores = {}
        for domain, indicators in domain_indicators.items():
            score = sum(1 for indicator in indicators if indicator in query_lower)
            domain_scores[domain] = score / len(indicators)

        # Complexity indicators
        complexity_indicators = {
            "multiple_teams": ["teams", "cross-functional", "multiple", "across"],
            "high_stakes": ["critical", "urgent", "important", "executive"],
            "ambiguity": ["unclear", "ambiguous", "complex", "challenging"],
            "scale": ["large", "enterprise", "organization-wide", "global"],
        }

        complexity_scores = {}
        for indicator_type, indicators in complexity_indicators.items():
            score = sum(1 for indicator in indicators if indicator in query_lower)
            complexity_scores[indicator_type] = score > 0

        # Urgency indicators
        urgency_indicators = ["urgent", "immediate", "asap", "quickly", "soon"]
        urgency_score = sum(
            1 for indicator in urgency_indicators if indicator in query_lower
        )

        return {
            "query_length": len(query.split()),
            "domain_scores": domain_scores,
            "complexity_indicators": complexity_scores,
            "urgency_score": urgency_score,
            "primary_domain": (
                max(domain_scores.items(), key=lambda x: x[1])[0]
                if domain_scores
                else "strategic"
            ),
            "estimated_complexity": sum(complexity_scores.values())
            / len(complexity_scores),
        }

    def classify_situational_context(
        self, query: str, query_analysis: Dict[str, Any], layer_context: Dict[str, Any]
    ) -> SituationalContext:
        """Classify the situational context based on analysis"""

        query_lower = query.lower()
        primary_domain = query_analysis["primary_domain"]

        # Crisis indicators
        crisis_keywords = [
            "crisis",
            "urgent",
            "emergency",
            "critical",
            "failure",
            "down",
            "broken",
        ]
        if any(keyword in query_lower for keyword in crisis_keywords):
            return SituationalContext.CRISIS_RESPONSE

        # Executive communication indicators
        exec_keywords = ["present", "board", "vp", "executive", "leadership", "senior"]
        if any(keyword in query_lower for keyword in exec_keywords):
            return SituationalContext.EXECUTIVE_COMMUNICATION

        # Technical decision indicators
        tech_keywords = ["architecture", "technical", "code", "system", "engineering"]
        if primary_domain == "technical" or any(
            keyword in query_lower for keyword in tech_keywords
        ):
            return SituationalContext.TECHNICAL_DECISION

        # Team coordination indicators
        team_keywords = ["team", "coordination", "collaboration", "work together"]
        if any(keyword in query_lower for keyword in team_keywords):
            return SituationalContext.TEAM_COORDINATION

        # Stakeholder alignment indicators
        stakeholder_keywords = [
            "stakeholder",
            "alignment",
            "communication",
            "agreement",
        ]
        if any(keyword in query_lower for keyword in stakeholder_keywords):
            return SituationalContext.STAKEHOLDER_ALIGNMENT

        # Process optimization indicators
        process_keywords = ["process", "optimize", "improve", "efficiency", "workflow"]
        if any(keyword in query_lower for keyword in process_keywords):
            return SituationalContext.PROCESS_OPTIMIZATION

        # Organizational change indicators
        change_keywords = ["change", "transform", "restructure", "reorganize", "scale"]
        if any(keyword in query_lower for keyword in change_keywords):
            return SituationalContext.ORGANIZATIONAL_CHANGE

        # Default to strategic planning
        return SituationalContext.STRATEGIC_PLANNING

    def assess_context_complexity(
        self,
        query_analysis: Dict[str, Any],
        layer_context: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]],
    ) -> ContextComplexity:
        """Assess the complexity level of the strategic context"""

        complexity_score = 0

        # Query complexity
        if query_analysis["query_length"] > 20:
            complexity_score += 1

        # Multiple domain involvement
        domain_count = sum(
            1 for score in query_analysis["domain_scores"].values() if score > 0.3
        )
        if domain_count > 2:
            complexity_score += 1

        # Complexity indicators from query analysis
        complexity_indicators = query_analysis.get("complexity_indicators", {})
        complexity_score += sum(complexity_indicators.values())

        # Stakeholder complexity
        stakeholder_context = layer_context.get("stakeholder", {})
        if stakeholder_context.get("stakeholder_count", 0) > 3:
            complexity_score += 1

        # Strategic context complexity
        strategic_context = layer_context.get("strategic", {})
        if strategic_context.get("active_initiatives", 0) > 2:
            complexity_score += 1

        # Map score to complexity level
        if complexity_score >= 4:
            return ContextComplexity.ENTERPRISE
        elif complexity_score >= 3:
            return ContextComplexity.COMPLEX
        elif complexity_score >= 2:
            return ContextComplexity.MODERATE
        else:
            return ContextComplexity.SIMPLE

    def identify_involved_stakeholders(
        self, layer_context: Dict[str, Any], query_analysis: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Identify stakeholders involved in the strategic context"""

        stakeholder_context = layer_context.get("stakeholder", {})
        primary_domain = query_analysis["primary_domain"]

        # Default stakeholder mapping based on domain
        domain_stakeholders = {
            "technical": ["tech_lead", "senior_engineers", "engineering_manager"],
            "strategic": ["engineering_director", "product_manager", "executive_team"],
            "organizational": ["engineering_manager", "hr_partner", "team_leads"],
            "stakeholder": ["product_manager", "design_lead", "business_stakeholders"],
            "executive": ["vp_engineering", "cto", "executive_team"],
        }

        primary_stakeholders = domain_stakeholders.get(
            primary_domain, ["engineering_manager"]
        )

        # Add stakeholders from context
        context_stakeholders = stakeholder_context.get("active_stakeholders", [])
        primary_stakeholders.extend(context_stakeholders)

        # Remove duplicates and organize
        primary_stakeholders = list(set(primary_stakeholders))

        return {
            "primary": primary_stakeholders[:3],  # Top 3 primary
            "secondary": primary_stakeholders[3:],  # Rest as secondary
            "total_count": len(primary_stakeholders),
        }

    def assess_time_sensitivity(
        self,
        query: str,
        layer_context: Dict[str, Any],
        situational_context: SituationalContext,
    ) -> str:
        """Assess time sensitivity of the strategic context"""

        query_lower = query.lower()

        # Immediate indicators
        immediate_keywords = ["urgent", "asap", "immediately", "emergency", "critical"]
        if any(keyword in query_lower for keyword in immediate_keywords):
            return "immediate"

        # Short-term indicators
        short_term_keywords = [
            "soon",
            "quickly",
            "next week",
            "this sprint",
            "short term",
        ]
        if any(keyword in query_lower for keyword in short_term_keywords):
            return "short_term"

        # Long-term indicators
        long_term_keywords = [
            "roadmap",
            "vision",
            "long term",
            "next year",
            "strategic",
        ]
        if any(keyword in query_lower for keyword in long_term_keywords):
            return "long_term"

        # Situational defaults
        if situational_context == SituationalContext.CRISIS_RESPONSE:
            return "immediate"
        elif situational_context in [
            SituationalContext.TEAM_COORDINATION,
            SituationalContext.STAKEHOLDER_ALIGNMENT,
        ]:
            return "short_term"
        elif situational_context in [
            SituationalContext.STRATEGIC_PLANNING,
            SituationalContext.ORGANIZATIONAL_CHANGE,
        ]:
            return "long_term"

        return "short_term"  # Default

    def summarize_layer_context(self, layer_context: Dict[str, Any]) -> Dict[str, str]:
        """Summarize layer context for strategic analysis"""
        summary = {}

        for layer_name, layer_data in layer_context.items():
            if layer_data:
                # Extract key insights from each layer
                if layer_name == "strategic":
                    summary[layer_name] = (
                        f"Active initiatives: {layer_data.get('active_initiatives', 0)}"
                    )
                elif layer_name == "stakeholder":
                    summary[layer_name] = (
                        f"Stakeholders: {layer_data.get('stakeholder_count', 0)}"
                    )
                elif layer_name == "organizational":
                    summary[layer_name] = (
                        f"Structure: {layer_data.get('structure_type', 'unknown')}"
                    )
                else:
                    summary[layer_name] = f"Data available: {len(layer_data)} fields"
            else:
                summary[layer_name] = "No data available"

        return summary
