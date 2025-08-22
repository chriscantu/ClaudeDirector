"""
Framework Selection Logic
Selects the most appropriate strategic framework based on user input and context.

Author: Martin (Principal Platform Architect)
Refactored from: embedded_framework_engine.py for better testability
"""

from typing import Dict, List, Any


class FrameworkSelector:
    """Selects the most appropriate framework based on input analysis"""

    def __init__(self, strategic_frameworks: Dict[str, Any]):
        """
        Initialize with strategic frameworks configuration

        Args:
            strategic_frameworks: Dictionary of available frameworks
        """
        self.strategic_frameworks = strategic_frameworks
        self._framework_keywords = self._initialize_framework_keywords()

    def select_framework(
        self, user_input: str, domain_focus: List[str]
    ) -> Dict[str, Any]:
        """
        Select the most appropriate framework based on input and domains

        Args:
            user_input: User's query or request
            domain_focus: List of domain areas to focus on

        Returns:
            Selected framework configuration
        """
        input_lower = user_input.lower()

        # Calculate framework scores
        framework_scores = self._calculate_framework_scores(input_lower, domain_focus)

        # Select framework with highest score
        best_framework_name = max(framework_scores, key=framework_scores.get)

        # Apply signal-based overrides
        best_framework_name = self._apply_signal_overrides(
            input_lower, best_framework_name, framework_scores
        )

        return self.strategic_frameworks[best_framework_name]

    def _calculate_framework_scores(
        self, input_lower: str, domain_focus: List[str]
    ) -> Dict[str, float]:
        """Calculate scores for each framework based on input and domain alignment"""
        framework_scores = {}

        for framework_name, framework in self.strategic_frameworks.items():
            score = 0.0

            # Domain alignment scoring
            framework_domains = framework.get("domains", [])
            domain_overlap = len(set(domain_focus) & set(framework_domains))
            score += domain_overlap * 0.4

            # Keyword matching scoring
            keywords = self._framework_keywords.get(framework_name, [])
            keyword_matches = sum(1 for keyword in keywords if keyword in input_lower)
            score += keyword_matches * 0.15

            framework_scores[framework_name] = score

        return framework_scores

    def _apply_signal_overrides(
        self,
        input_lower: str,
        best_framework_name: str,
        framework_scores: Dict[str, float],
    ) -> str:
        """Apply signal-based framework selection overrides"""
        decision_signals = [
            "decision",
            "decide",
            "choose",
            "options",
            "alternative",
            "should we",
            "best approach",
            "which option",
        ]
        strategy_signals = [
            "fluff",
            "bad strategy",
            "real strategy",
            "challenge",
            "obstacle",
            "strategic",
            "leverage",
        ]

        has_decision_signals = any(signal in input_lower for signal in decision_signals)
        has_strategy_signals = any(signal in input_lower for signal in strategy_signals)

        # Override framework selection for strong decision/strategy signals
        if (
            has_decision_signals
            and framework_scores.get("decisive_wrap_framework", 0) >= 0.1
        ):
            return "decisive_wrap_framework"
        elif (
            has_strategy_signals
            and framework_scores.get("rumelt_strategy_kernel", 0) >= 0.1
        ):
            return "rumelt_strategy_kernel"
        elif framework_scores[best_framework_name] < 0.3:
            # Check for specific patterns that should trigger Rumelt or WRAP
            if has_strategy_signals:
                return "rumelt_strategy_kernel"
            elif has_decision_signals:
                return "decisive_wrap_framework"
            else:
                return "strategic_platform_assessment"

        return best_framework_name

    def _initialize_framework_keywords(self) -> Dict[str, List[str]]:
        """Initialize framework keyword mappings for scoring"""
        return {
            "strategic_platform_assessment": [
                "platform",
                "strategy",
                "assessment",
                "stakeholder",
                "roadmap",
                "planning",
                "quarterly",
                "q4",
                "alignment",
            ],
            "organizational_transformation": [
                "transformation",
                "change",
                "organizational",
                "culture",
                "team",
                "scaling",
                "structure",
                "communication",
            ],
            "technical_strategy": [
                "technical",
                "architecture",
                "system",
                "infrastructure",
                "debt",
                "engineering",
                "platform",
                "design",
            ],
            "rumelt_strategy_kernel": [
                "strategy",
                "strategic",
                "kernel",
                "diagnosis",
                "policy",
                "coherent",
                "challenge",
                "obstacle",
                "leverage",
                "focus",
                "choice",
                "advantage",
                "bad strategy",
                "fluff",
                "good strategy",
            ],
            "decisive_wrap_framework": [
                "decision",
                "decide",
                "options",
                "choose",
                "assumptions",
                "reality",
                "distance",
                "wrong",
                "prepare",
                "wrap",
                "widen",
                "test",
                "attain",
                "alternatives",
                "evidence",
                "bias",
            ],
            "scaling_up_excellence": [
                "scaling",
                "scale up",
                "adoption",
                "spread",
                "rollout",
                "standardization",
                "consistency",
                "quality",
                "excellence",
                "practices",
                "teams",
                "organization",
                "across",
                "multiple",
                "buddhist",
                "catholic",
                "hot causes",
                "cool solutions",
                "connect",
                "cascade",
                "cut",
                "growth",
                "mindset",
                "footprint",
            ],
            "team_topologies": [
                "team structure",
                "organizational design",
                "team types",
                "conway's law",
                "cognitive load",
                "platform team",
                "enabling team",
                "stream-aligned",
                "complicated subsystem",
                "interaction modes",
                "collaboration",
                "facilitating",
                "x-as-a-service",
                "team boundaries",
                "team topology",
            ],
            "accelerate_performance": [
                "team performance",
                "dora metrics",
                "deployment frequency",
                "lead time",
                "psychological safety",
                "team composition",
                "high performing teams",
                "change failure rate",
                "recovery time",
                "continuous integration",
                "team capabilities",
                "performance metrics",
                "team culture",
            ],
            "crucial_conversations": [
                "stakeholder",
                "difficult conversation",
                "executive",
                "alignment",
                "conflict",
                "communication",
                "negotiation",
                "buy-in",
                "crucial conversation",
                "dialogue",
                "safety",
                "mutual purpose",
                "persuasive",
                "listening",
                "action",
            ],
            "capital_allocation": [
                "budget",
                "investment",
                "roi",
                "resource allocation",
                "prioritization",
                "cost",
                "value",
                "portfolio",
                "funding",
                "capital",
                "financial",
                "resource",
                "allocation",
                "optimization",
                "returns",
            ],
            "decision_framework": [
                "decision",
                "choose",
                "options",
                "evaluate",
                "criteria",
                "trade-off",
                "recommendation",
                "analysis",
            ],
        }
