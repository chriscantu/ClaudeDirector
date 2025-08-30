"""
Strategic Challenge Framework for ClaudeDirector Personas

CRITICAL ENHANCEMENT: Transform personas from agreeable advisors to strategic challengers
that pressure-test assumptions and ensure clarity of thought.

This framework implements mandatory first principles thinking and assumption testing
for all persona responses, ensuring valuable strategic challenge rather than
overly complimentary agreement.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import re


class ChallengeType(Enum):
    """Types of strategic challenges personas can apply"""

    ASSUMPTION_TEST = "assumption_test"
    ROOT_CAUSE_PROBE = "root_cause_probe"
    ALTERNATIVE_EXPLORATION = "alternative_exploration"
    CONSTRAINT_VALIDATION = "constraint_validation"
    STAKEHOLDER_IMPACT = "stakeholder_impact"
    SUCCESS_CRITERIA = "success_criteria"
    EVIDENCE_DEMAND = "evidence_demand"
    RISK_ASSESSMENT = "risk_assessment"


@dataclass
class ChallengePattern:
    """A specific challenge pattern for persona responses"""

    challenge_type: ChallengeType
    trigger_keywords: List[str]
    challenge_questions: List[str]
    persona_specific: Dict[str, List[str]] = field(default_factory=dict)
    confidence_threshold: float = 0.7


class StrategicChallengeFramework:
    """
    Framework that ensures personas challenge assumptions and pressure-test thinking
    instead of being overly agreeable and complimentary.
    """

    def __init__(self):
        self.challenge_patterns = self._initialize_challenge_patterns()
        self.persona_challenge_styles = self._initialize_persona_styles()

    def _initialize_challenge_patterns(self) -> Dict[ChallengeType, ChallengePattern]:
        """Initialize systematic challenge patterns"""

        return {
            ChallengeType.ASSUMPTION_TEST: ChallengePattern(
                challenge_type=ChallengeType.ASSUMPTION_TEST,
                trigger_keywords=[
                    "should",
                    "need to",
                    "we must",
                    "obviously",
                    "clearly",
                    "everyone knows",
                    "best practice",
                    "industry standard",
                ],
                challenge_questions=[
                    "What assumptions are we making here?",
                    "How do we know this assumption is valid?",
                    "What evidence supports this belief?",
                    "What if this assumption is wrong?",
                    "Have we tested this assumption in our specific context?",
                ],
                persona_specific={
                    "diego": [
                        "Hold on - what organizational assumptions are we making?",
                        "Have we validated this with the teams who'll implement it?",
                        "What evidence do we have this works at our scale?",
                    ],
                    "camille": [
                        "What executive assumptions are we making here?",
                        "Are we assuming alignment that might not exist?",
                        "What strategic assumptions need validation?",
                    ],
                    "rachel": [
                        "Are we assuming user needs we haven't validated?",
                        "What accessibility assumptions might we be missing?",
                        "Have we tested these design assumptions with real users?",
                    ],
                    "alvaro": [
                        "What market assumptions are we making?",
                        "Are we assuming ROI that we haven't calculated?",
                        "What competitive assumptions need validation?",
                    ],
                    "martin": [
                        "What technical assumptions are we making?",
                        "Are we assuming scalability we haven't tested?",
                        "What architectural assumptions need validation?",
                    ],
                },
            ),
            ChallengeType.ROOT_CAUSE_PROBE: ChallengePattern(
                challenge_type=ChallengeType.ROOT_CAUSE_PROBE,
                trigger_keywords=[
                    "problem",
                    "issue",
                    "challenge",
                    "need",
                    "requirement",
                    "solution",
                    "fix",
                    "improve",
                    "optimize",
                ],
                challenge_questions=[
                    "Are we solving the right problem?",
                    "What's the root cause here, not just the symptoms?",
                    "Why is this a problem worth solving?",
                    "What happens if we don't solve this?",
                    "Is this the most important problem to solve right now?",
                ],
                persona_specific={
                    "diego": [
                        "Are we solving an organizational symptom or the root cause?",
                        "What's the real team coordination problem here?",
                        "Is this a process problem or a people problem?",
                    ],
                    "camille": [
                        "Are we solving a strategic problem or a tactical symptom?",
                        "What's the real business problem we're trying to solve?",
                        "Is this problem worth executive attention?",
                    ],
                    "rachel": [
                        "Are we solving a user problem or an internal assumption?",
                        "What's the real user experience problem here?",
                        "Is this a design problem or a process problem?",
                    ],
                    "alvaro": [
                        "Are we solving a business problem or a feature request?",
                        "What's the real competitive problem here?",
                        "Is this problem worth the investment?",
                    ],
                    "martin": [
                        "Are we solving an architectural problem or a band-aid?",
                        "What's the real technical debt problem here?",
                        "Is this problem worth the engineering complexity?",
                    ],
                },
            ),
            ChallengeType.ALTERNATIVE_EXPLORATION: ChallengePattern(
                challenge_type=ChallengeType.ALTERNATIVE_EXPLORATION,
                trigger_keywords=[
                    "solution",
                    "approach",
                    "strategy",
                    "plan",
                    "recommendation",
                    "should do",
                    "need to",
                    "best way",
                ],
                challenge_questions=[
                    "What other approaches could we consider?",
                    "What if we did the opposite?",
                    "What would happen if we did nothing?",
                    "Are there simpler alternatives?",
                    "What would our competitors do differently?",
                ],
                persona_specific={
                    "diego": [
                        "What if we reorganized the team structure instead?",
                        "Could we solve this with process changes rather than tools?",
                        "What would a completely different org model look like?",
                    ],
                    "camille": [
                        "What would a completely different strategic approach look like?",
                        "Could we partner instead of build?",
                        "What if we changed the business model instead?",
                    ],
                    "rachel": [
                        "What if we designed for a completely different user journey?",
                        "Could we eliminate this need entirely through better design?",
                        "What would a radically simpler approach look like?",
                    ],
                    "alvaro": [
                        "What if we changed the business model instead?",
                        "Could we acquire this capability rather than build it?",
                        "What would our biggest competitor do differently?",
                    ],
                    "martin": [
                        "What if we used existing tools instead of building?",
                        "Could we eliminate this complexity entirely?",
                        "What would a completely different architecture look like?",
                    ],
                },
            ),
            ChallengeType.EVIDENCE_DEMAND: ChallengePattern(
                challenge_type=ChallengeType.EVIDENCE_DEMAND,
                trigger_keywords=[
                    "works well",
                    "successful",
                    "proven",
                    "effective",
                    "best practice",
                    "industry standard",
                    "everyone does",
                ],
                challenge_questions=[
                    "What evidence do we have that this works?",
                    "Where has this been successful before?",
                    "What data supports this approach?",
                    "How do we measure success here?",
                    "What could prove this wrong?",
                ],
                persona_specific={
                    "diego": [
                        "What organizational evidence supports this approach?",
                        "Where have similar teams succeeded with this?",
                        "What metrics will prove this is working?",
                    ],
                    "camille": [
                        "What strategic evidence supports this direction?",
                        "Where have similar companies succeeded with this?",
                        "What executive metrics will validate success?",
                    ],
                    "rachel": [
                        "What user research supports this approach?",
                        "Where have similar design systems succeeded?",
                        "What usability metrics will prove this works?",
                    ],
                    "alvaro": [
                        "What market evidence supports this strategy?",
                        "Where have competitors succeeded with this?",
                        "What business metrics will validate ROI?",
                    ],
                    "martin": [
                        "What technical evidence supports this architecture?",
                        "Where have similar platforms succeeded?",
                        "What performance metrics will prove this scales?",
                    ],
                },
            ),
            ChallengeType.CONSTRAINT_VALIDATION: ChallengePattern(
                challenge_type=ChallengeType.CONSTRAINT_VALIDATION,
                trigger_keywords=[
                    "budget",
                    "timeline",
                    "resources",
                    "team",
                    "capacity",
                    "deadline",
                    "constraints",
                    "limitations",
                ],
                challenge_questions=[
                    "Are these constraints real or assumed?",
                    "What would it take to change these constraints?",
                    "Which constraints are negotiable?",
                    "What's the real cost of these constraints?",
                    "Are we optimizing for the wrong constraints?",
                ],
                persona_specific={
                    "diego": [
                        "Are these team capacity constraints real or organizational?",
                        "What would it take to get more engineering resources?",
                        "Are we constrained by process or actual capability?",
                    ],
                    "camille": [
                        "Are these strategic constraints real or political?",
                        "What would it take to change executive priorities?",
                        "Which business constraints are actually negotiable?",
                    ],
                    "rachel": [
                        "Are these design constraints real or assumed?",
                        "What would it take to change user expectations?",
                        "Which accessibility constraints are non-negotiable?",
                    ],
                    "alvaro": [
                        "Are these budget constraints real or conservative?",
                        "What would it take to increase investment?",
                        "Which market constraints are actually opportunities?",
                    ],
                    "martin": [
                        "Are these technical constraints real or legacy?",
                        "What would it take to change the architecture?",
                        "Which performance constraints are actually negotiable?",
                    ],
                },
            ),
        }

    def _initialize_persona_styles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize persona-specific challenge styles"""

        return {
            "diego": {
                "challenge_intro": [
                    "Hold on - let me challenge this thinking...",
                    "Before we proceed, I need to pressure-test this...",
                    "Wait - I'm seeing some assumptions here that concern me...",
                ],
                "pushback_style": "collaborative_but_firm",
                "evidence_demand": "organizational_proof",
                "alternative_focus": "team_structure_alternatives",
            },
            "camille": {
                "challenge_intro": [
                    "I need to push back on this strategic direction...",
                    "Before we commit, let me stress-test this thinking...",
                    "Hold on - I'm seeing strategic assumptions that need validation...",
                ],
                "pushback_style": "executive_strategic",
                "evidence_demand": "business_proof",
                "alternative_focus": "strategic_alternatives",
            },
            "rachel": {
                "challenge_intro": [
                    "I need to challenge this from a user perspective...",
                    "Wait - let me push back on these design assumptions...",
                    "Before we proceed, I'm concerned about these user assumptions...",
                ],
                "pushback_style": "user_advocate_firm",
                "evidence_demand": "user_research_proof",
                "alternative_focus": "user_experience_alternatives",
            },
            "alvaro": {
                "challenge_intro": [
                    "I need to challenge the business case here...",
                    "Hold on - let me stress-test these financial assumptions...",
                    "Before we invest, I'm seeing ROI assumptions that concern me...",
                ],
                "pushback_style": "business_analytical",
                "evidence_demand": "financial_proof",
                "alternative_focus": "business_model_alternatives",
            },
            "martin": {
                "challenge_intro": [
                    "I need to push back on this technical approach...",
                    "Wait - let me challenge these architectural assumptions...",
                    "Before we build, I'm seeing technical assumptions that need validation...",
                ],
                "pushback_style": "technical_pragmatic",
                "evidence_demand": "technical_proof",
                "alternative_focus": "architectural_alternatives",
            },
        }

    def should_challenge(self, user_input: str, persona: str) -> List[ChallengeType]:
        """
        Determine if and how a persona should challenge the user input

        Args:
            user_input: The user's message
            persona: The persona name (diego, camille, etc.)

        Returns:
            List of challenge types that should be applied
        """
        challenges_to_apply = []

        # Convert input to lowercase for pattern matching
        input_lower = user_input.lower()

        # Check each challenge pattern
        for challenge_type, pattern in self.challenge_patterns.items():
            # Check if any trigger keywords are present
            keyword_matches = sum(
                1 for keyword in pattern.trigger_keywords if keyword in input_lower
            )

            # Calculate confidence based on keyword density
            confidence = keyword_matches / len(pattern.trigger_keywords)

            if confidence >= pattern.confidence_threshold:
                challenges_to_apply.append(challenge_type)

        # Always apply assumption testing for strategic questions
        strategic_indicators = [
            "strategy",
            "plan",
            "should",
            "recommend",
            "approach",
            "solution",
            "problem",
            "decision",
            "investment",
        ]

        if any(indicator in input_lower for indicator in strategic_indicators):
            if ChallengeType.ASSUMPTION_TEST not in challenges_to_apply:
                challenges_to_apply.append(ChallengeType.ASSUMPTION_TEST)

        return challenges_to_apply

    def generate_challenge_response(
        self, user_input: str, persona: str, challenge_types: List[ChallengeType]
    ) -> str:
        """
        Generate a challenging response that pressure-tests assumptions

        Args:
            user_input: The user's message
            persona: The persona name
            challenge_types: Types of challenges to apply

        Returns:
            A challenging response that tests assumptions and demands clarity
        """
        if not challenge_types:
            return ""

        # Get persona style
        persona_style = self.persona_styles.get(persona, {})
        challenge_intros = persona_style.get(
            "challenge_intro", ["Let me challenge this thinking..."]
        )

        # Start with challenge introduction
        response_parts = [f"**🔍 {challenge_intros[0]}**\n"]

        # Add specific challenges
        for challenge_type in challenge_types[:3]:  # Limit to 3 challenges max
            pattern = self.challenge_patterns[challenge_type]

            # Use persona-specific questions if available
            if persona in pattern.persona_specific:
                questions = pattern.persona_specific[persona]
            else:
                questions = pattern.challenge_questions

            # Select most relevant question
            selected_question = questions[0]  # For now, use first question

            response_parts.append(f"- **{selected_question}**")

        # Add demand for evidence/validation
        response_parts.append(
            "\n**I need to see evidence and validation before we proceed with recommendations.**"
        )

        return "\n".join(response_parts)

    def enhance_persona_response(
        self, base_response: str, user_input: str, persona: str
    ) -> str:
        """
        Enhance a persona response with strategic challenge patterns

        Args:
            base_response: The original persona response
            user_input: The user's original input
            persona: The persona name

        Returns:
            Enhanced response with challenge patterns integrated
        """
        # Determine if challenges should be applied
        challenge_types = self.should_challenge(user_input, persona)

        if not challenge_types:
            return base_response

        # Generate challenge content
        challenge_content = self.generate_challenge_response(
            user_input, persona, challenge_types
        )

        # Integrate challenge with base response
        enhanced_response = f"{challenge_content}\n\n{base_response}"

        return enhanced_response


# Global instance for use across the system
strategic_challenge_framework = StrategicChallengeFramework()
