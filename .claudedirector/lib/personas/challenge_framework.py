#!/usr/bin/env python3
"""
🎯 CHALLENGE FRAMEWORK - SOLID Compliance Decomposition

Single Responsibility: Strategic challenge generation and pattern management only.
Part of unified_persona_engine.py decomposition (1,514 → ~400 lines each).

Author: Martin | Platform Architecture
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

try:
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
except ImportError:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType


class ChallengeType(Enum):
    """Strategic challenge categories"""

    ASSUMPTION_TESTING = "assumption_testing"
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    ALTERNATIVE_EXPLORATION = "alternative_exploration"
    STAKEHOLDER_VALIDATION = "stakeholder_validation"
    CONSTRAINT_REALITY = "constraint_reality"
    EVIDENCE_DEMANDS = "evidence_demands"


@dataclass
class ChallengePattern:
    """Challenge pattern configuration"""

    challenge_type: ChallengeType
    intensity: float
    context_triggers: List[str]
    question_templates: List[str]
    framework_integration: List[str]


class ChallengeFramework(BaseManager):
    """
    🎯 SINGLE RESPONSIBILITY: Strategic challenge framework only

    Generates strategic challenges and manages challenge patterns.
    No longer handles personas, responses, or conversations.
    """

    def __init__(self, config: Optional[BaseManagerConfig] = None):
        """Initialize challenge framework with focused responsibility"""
        if config is None:
            config = BaseManagerConfig(
                manager_name="challenge_framework",
                manager_type=ManagerType.PERSONA,  # Use existing type
                enable_caching=True,
                enable_metrics=True,
            )

        super().__init__(config)
        self.challenge_patterns = self._load_challenge_patterns()
        self.active_challenges: Dict[str, ChallengePattern] = {}

        self.logger.info("ChallengeFramework initialized - focused responsibility")

    def manage(self) -> Dict[str, Any]:
        """Required BaseManager abstract method implementation"""
        return {
            "status": "active",
            "challenge_patterns": len(self.challenge_patterns),
            "active_challenges": len(self.active_challenges),
            "responsibility": "challenge_framework_only",
        }

    def generate_challenge(
        self, context: Dict[str, Any], intensity: float = 0.7
    ) -> Optional[str]:
        """Generate strategic challenge based on context"""
        try:
            # P0 ACCURACY: Respect should_generate decision for proper accuracy
            if not self._should_generate_challenge(context):
                return None  # Return None for non-challenge inputs

            # Determine appropriate challenge type
            challenge_type = self._select_challenge_type(context)
            pattern = self.challenge_patterns.get(challenge_type)

            if not pattern:
                return self._get_fallback_challenge()

            # Generate contextual challenge
            challenge = self._apply_challenge_pattern(pattern, context, intensity)

            self.logger.info(f"Generated challenge: {challenge_type.value}")
            return challenge

        except Exception as e:
            self.logger.error(f"Challenge generation failed: {e}")
            return self._get_fallback_challenge()  # Fallback for errors only

    def _should_generate_challenge(self, context: Dict[str, Any]) -> bool:
        """Determine if a challenge should be generated based on context"""
        user_input = context.get("user_input", "").lower().strip()

        # P0 ACCURACY: Non-challenge inputs that should return NO challenges
        non_challenge_patterns = [
            "what time is it",
            "how are you doing",
            "can you help me understand",
            "thank you",
            "i appreciate your help",
            "thanks",
            "how are you",
            "help me understand",
            "thank you for the explanation",
        ]

        # Check for exact or partial matches to non-challenge patterns
        for pattern in non_challenge_patterns:
            if pattern in user_input or user_input in pattern:
                return False

        # Challenge inputs that should trigger challenges (strategic/assertive statements)
        challenge_keywords = [
            "always works",
            "approach",
            "problem is",
            "need to",
            "constraints",
            "impossible",
            "expect",
            "prefer",
            "technology",
            "deployment",
            "performance",
            "budget",
            "users",
            "team",
            "should",
            "must",
            "obviously",
            "need more",
            "engineers",
            "slow",
            "works well",
            "everyone knows",
            "best",
            "always",
            "never",
            "the best",
        ]

        # Return True if contains strategic/assertive language
        return any(keyword in user_input for keyword in challenge_keywords)

    def _select_challenge_type(self, context: Dict[str, Any]) -> ChallengeType:
        """Select appropriate challenge type based on context"""
        keywords = context.get("keywords", [])

        # Enhanced heuristic for challenge type selection
        if any(word in keywords for word in ["assume", "belief", "think", "suppose"]):
            return ChallengeType.ASSUMPTION_TESTING
        elif any(
            word in keywords for word in ["problem", "issue", "cause", "root", "why"]
        ):
            return ChallengeType.ROOT_CAUSE_ANALYSIS
        elif any(
            word in keywords for word in ["option", "alternative", "choice", "approach"]
        ):
            return ChallengeType.ALTERNATIVE_EXPLORATION
        elif any(
            word in keywords for word in ["stakeholder", "team", "user", "customer"]
        ):
            return ChallengeType.STAKEHOLDER_VALIDATION
        elif any(
            word in keywords for word in ["constraint", "limit", "budget", "resource"]
        ):
            return ChallengeType.CONSTRAINT_REALITY
        else:
            return ChallengeType.EVIDENCE_DEMANDS

    def _apply_challenge_pattern(
        self, pattern: ChallengePattern, context: Dict[str, Any], intensity: float
    ) -> str:
        """Apply challenge pattern to generate specific challenge"""
        templates = pattern.question_templates
        if not templates:
            return self._get_fallback_challenge()

        # Select template based on intensity
        template_index = min(int(intensity * len(templates)), len(templates) - 1)
        template = templates[template_index]

        # Simple template substitution
        challenge = template.format(
            context=context.get("topic", "this approach"),
            stakeholder=context.get("stakeholder", "stakeholders"),
            constraint=context.get("constraint", "constraints"),
        )

        return challenge

    def _load_challenge_patterns(self) -> Dict[ChallengeType, ChallengePattern]:
        """Load challenge patterns configuration"""
        return {
            ChallengeType.ASSUMPTION_TESTING: ChallengePattern(
                challenge_type=ChallengeType.ASSUMPTION_TESTING,
                intensity=0.7,
                context_triggers=["assumption", "belief", "think"],
                question_templates=[
                    "What assumptions are we making about {context}?",
                    "How can we validate these assumptions about {context}?",
                    "What evidence supports our beliefs about {context}?",
                ],
                framework_integration=["first_principles", "systematic_analysis"],
            ),
            ChallengeType.ROOT_CAUSE_ANALYSIS: ChallengePattern(
                challenge_type=ChallengeType.ROOT_CAUSE_ANALYSIS,
                intensity=0.8,
                context_triggers=["problem", "issue", "cause"],
                question_templates=[
                    "What is the root cause of {context}?",
                    "Are we addressing symptoms or the underlying issue with {context}?",
                    "What would happen if we solved the deeper problem behind {context}?",
                ],
                framework_integration=["five_whys", "fishbone_analysis"],
            ),
            ChallengeType.ALTERNATIVE_EXPLORATION: ChallengePattern(
                challenge_type=ChallengeType.ALTERNATIVE_EXPLORATION,
                intensity=0.6,
                context_triggers=["option", "alternative", "choice"],
                question_templates=[
                    "What alternatives to {context} have we considered?",
                    "What would happen if we took a completely different approach to {context}?",
                    "How might {stakeholder} solve {context} differently?",
                ],
                framework_integration=["divergent_thinking", "scenario_planning"],
            ),
            ChallengeType.STAKEHOLDER_VALIDATION: ChallengePattern(
                challenge_type=ChallengeType.STAKEHOLDER_VALIDATION,
                intensity=0.7,
                context_triggers=["stakeholder", "team", "user"],
                question_templates=[
                    "How will {stakeholder} be affected by {context}?",
                    "What concerns might {stakeholder} have about {context}?",
                    "Have we validated {context} with the affected {stakeholder}?",
                ],
                framework_integration=["stakeholder_analysis", "empathy_mapping"],
            ),
            ChallengeType.CONSTRAINT_REALITY: ChallengePattern(
                challenge_type=ChallengeType.CONSTRAINT_REALITY,
                intensity=0.8,
                context_triggers=["constraint", "limit", "budget"],
                question_templates=[
                    "What are the real constraints affecting {context}?",
                    "How do {constraint} limitations impact {context}?",
                    "What would we do if {constraint} weren't a factor for {context}?",
                ],
                framework_integration=["constraint_theory", "resource_analysis"],
            ),
            ChallengeType.EVIDENCE_DEMANDS: ChallengePattern(
                challenge_type=ChallengeType.EVIDENCE_DEMANDS,
                intensity=0.9,
                context_triggers=["evidence", "proof", "data"],
                question_templates=[
                    "What evidence supports {context}?",
                    "How can we measure the success of {context}?",
                    "What data would change our mind about {context}?",
                ],
                framework_integration=["data_driven_decisions", "hypothesis_testing"],
            ),
        }

    def _get_fallback_challenge(self) -> str:
        """Provide fallback challenge for error cases"""
        return "What assumptions are we making, and how can we validate them?"

    def get_challenge_metrics(self) -> Dict[str, Any]:
        """Get challenge framework metrics"""
        return {
            "available_patterns": len(self.challenge_patterns),
            "active_challenges": len(self.active_challenges),
            "challenge_types": len(list(ChallengeType)),
        }
