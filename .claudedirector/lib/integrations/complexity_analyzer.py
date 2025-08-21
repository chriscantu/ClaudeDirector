"""
Complexity Analysis Engine
Analyzes input complexity to determine when MCP enhancement would add value.
"""

import re
import logging
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ComplexityLevel(Enum):
    """Complexity levels for input analysis"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    STRATEGIC = "strategic"


@dataclass
class ComplexityAnalysis:
    """Result of complexity analysis"""
    level: ComplexityLevel
    confidence: float
    triggers: List[str]
    recommended_enhancement: Optional[str]
    persona_specific_score: float


class ComplexityAnalyzer:
    """Analyze input complexity to determine enhancement needs"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize complexity analyzer with keyword patterns and thresholds

        Args:
            config: Configuration dictionary with enhancement thresholds
        """
        self.config = config
        self.thresholds = config.get('enhancement_thresholds', {})

        # Core strategic keywords
        self.strategic_keywords = [
            "restructure", "organization", "teams", "strategy",
            "scaling", "architecture", "platform", "design system",
            "governance", "adoption", "coordination", "alignment",
            "framework", "methodology", "systematic", "process"
        ]

        # Business strategy keywords (Alvaro)
        self.business_strategy_keywords = [
            "competitive analysis", "market positioning", "business strategy",
            "ROI", "financial modeling", "investment decision",
            "product strategy", "go-to-market", "market fit",
            "business case", "competitive advantage", "strategic positioning",
            "revenue", "profit", "cost analysis", "market share"
        ]

        # Technology leadership keywords (Camille)
        self.technology_leadership_keywords = [
            "technology strategy", "organizational scaling", "strategic planning",
            "executive decision", "technology roadmap", "architecture governance",
            "team scaling", "organizational design", "technology leadership",
            "strategic technology", "platform strategy", "technical vision",
            "CTO", "executive", "board", "leadership team"
        ]

        # Engineering keywords (Diego, Martin, Rachel)
        self.engineering_keywords = [
            "microservices", "distributed systems", "performance",
            "scalability", "reliability", "observability",
            "DevOps", "CI/CD", "testing", "deployment",
            "database", "API", "infrastructure", "cloud"
        ]

        # Design system keywords (Rachel)
        self.design_system_keywords = [
            "design system", "component library", "design tokens",
            "style guide", "design patterns", "brand consistency",
            "user interface", "user experience", "accessibility",
            "design ops", "design tools", "figma", "sketch"
        ]

        # Complexity indicators
        self.complexity_indicators = [
            "how should we", "what's the best approach", "framework",
            "methodology", "best practices", "proven approach",
            "systematic", "strategic", "comprehensive", "enterprise",
            "scale", "complex", "multiple", "cross-team", "organization"
        ]

        # Question complexity patterns
        self.complex_question_patterns = [
            r"how (?:should|can|do) we (?:approach|handle|manage|implement)",
            r"what(?:'s| is) the best (?:way|approach|method|strategy)",
            r"(?:help|guide|advise) (?:me|us) (?:with|on|for)",
            r"(?:framework|methodology|process) for",
            r"(?:strategic|systematic|comprehensive) (?:approach|analysis|plan)"
        ]

    def analyze_complexity(self, input_text: str, persona: str) -> ComplexityAnalysis:
        """
        Analyze input complexity and determine enhancement needs

        Args:
            input_text: User input to analyze
            persona: Target persona (diego, martin, rachel, alvaro, camille)

        Returns:
            ComplexityAnalysis with enhancement recommendations
        """
        input_lower = input_text.lower()
        triggers = []
        total_score = 0.0

        # Base complexity scoring
        base_score = self._analyze_base_complexity(input_lower)
        total_score += base_score

        # Persona-specific scoring
        persona_score = self._analyze_persona_specific_complexity(input_lower, persona)
        total_score += persona_score

        # Pattern matching scoring
        pattern_score, pattern_triggers = self._analyze_pattern_complexity(input_text)
        total_score += pattern_score
        triggers.extend(pattern_triggers)

        # Question complexity scoring
        question_score, question_triggers = self._analyze_question_complexity(input_text)
        total_score += question_score
        triggers.extend(question_triggers)

        # Length and structure scoring
        structure_score = self._analyze_structure_complexity(input_text)
        total_score += structure_score

        # Normalize score (more aggressive scoring for strategic content)
        final_score = min(1.0, total_score / 3.0)  # Less conservative normalization

        # Determine complexity level
        complexity_level = self._determine_complexity_level(final_score)

        # Determine recommended enhancement
        recommended_enhancement = self._determine_recommended_enhancement(
            persona, final_score, triggers
        )

        logger.debug(f"Complexity analysis for {persona}: score={final_score:.2f}, level={complexity_level.value}")

        return ComplexityAnalysis(
            level=complexity_level,
            confidence=final_score,
            triggers=triggers,
            recommended_enhancement=recommended_enhancement,
            persona_specific_score=persona_score
        )

    def _analyze_base_complexity(self, input_text: str) -> float:
        """Analyze base complexity using strategic keywords"""
        score = 0.0

        # Strategic keyword matching
        for keyword in self.strategic_keywords:
            if keyword in input_text:
                score += 0.1

        # Complexity indicator matching
        for indicator in self.complexity_indicators:
            if indicator in input_text:
                score += 0.15

        return min(1.0, score)

    def _analyze_persona_specific_complexity(self, input_text: str, persona: str) -> float:
        """Analyze complexity specific to persona domain"""
        score = 0.0

        if persona == "alvaro":
            # Business strategy complexity
            for keyword in self.business_strategy_keywords:
                if keyword in input_text:
                    score += 0.2

        elif persona == "camille":
            # Technology leadership complexity
            for keyword in self.technology_leadership_keywords:
                if keyword in input_text:
                    score += 0.2

        elif persona in ["diego", "martin", "rachel"]:
            # Engineering complexity
            for keyword in self.engineering_keywords:
                if keyword in input_text:
                    score += 0.15

            # Diego gets additional scoring for organizational and strategic terms
            if persona == "diego":
                diego_specific = [
                    "organizational", "cross-team", "coordination", "restructuring",
                    "systematic", "teams", "delivery", "velocity", "alignment"
                ]
                for keyword in diego_specific:
                    if keyword in input_text:
                        score += 0.2

            if persona == "rachel":
                # Design system specific complexity
                for keyword in self.design_system_keywords:
                    if keyword in input_text:
                        score += 0.2

        return min(1.0, score)

    def _analyze_pattern_complexity(self, input_text: str) -> Tuple[float, List[str]]:
        """Analyze complexity using regex patterns"""
        score = 0.0
        triggers = []

        for pattern in self.complex_question_patterns:
            matches = re.findall(pattern, input_text, re.IGNORECASE)
            if matches:
                score += 0.3
                triggers.append(f"complex_question_pattern: {pattern}")

        return min(1.0, score), triggers

    def _analyze_question_complexity(self, input_text: str) -> Tuple[float, List[str]]:
        """Analyze question complexity and structure"""
        score = 0.0
        triggers = []

        # Multi-part questions
        question_markers = input_text.count('?')
        if question_markers > 1:
            score += 0.2
            triggers.append(f"multi_part_question: {question_markers} questions")

        # Conditional or comparative questions
        if any(word in input_text.lower() for word in ["versus", "vs", "compared to", "better than", "rather than"]):
            score += 0.2
            triggers.append("comparative_question")

        # Open-ended strategic questions
        if any(phrase in input_text.lower() for phrase in ["how should", "what should", "when should", "why should"]):
            score += 0.15
            triggers.append("strategic_question")

        return min(1.0, score), triggers

    def _analyze_structure_complexity(self, input_text: str) -> float:
        """Analyze structural complexity of input"""
        score = 0.0

        # Length-based complexity
        word_count = len(input_text.split())
        if word_count > 50:
            score += 0.2
        elif word_count > 25:
            score += 0.1

        # Sentence complexity
        sentence_count = input_text.count('.') + input_text.count('!') + input_text.count('?')
        if sentence_count > 3:
            score += 0.15

        # Technical terminology density
        technical_terms = ["system", "process", "implementation", "approach", "solution", "architecture", "framework"]
        technical_count = sum(1 for term in technical_terms if term in input_text.lower())
        if technical_count > 2:
            score += 0.1

        return min(1.0, score)

    def _determine_complexity_level(self, score: float) -> ComplexityLevel:
        """Determine complexity level from score"""
        if score >= 0.7:
            return ComplexityLevel.STRATEGIC
        elif score >= 0.5:
            return ComplexityLevel.COMPLEX
        elif score >= 0.3:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.SIMPLE

    def _determine_recommended_enhancement(self, persona: str, score: float, triggers: List[str]) -> Optional[str]:
        """Determine recommended enhancement type"""
        if score < 0.4:  # Conservative threshold (MODERATE level)
            return None

        # Persona-specific enhancement recommendations
        if persona == "diego":
            if score >= self.thresholds.get('systematic_analysis', 0.7):
                return "systematic_analysis"
        elif persona == "martin":
            if score >= self.thresholds.get('framework_lookup', 0.6):
                return "architecture_patterns"
        elif persona == "rachel":
            if score >= self.thresholds.get('framework_lookup', 0.6):
                return "design_system_methodology"
        elif persona == "alvaro":
            if score >= self.thresholds.get('business_strategy', 0.7):
                return "business_strategy"
        elif persona == "camille":
            if score >= self.thresholds.get('technology_leadership', 0.7):
                return "technology_leadership"

        return None

    def should_enhance(self, analysis: ComplexityAnalysis, persona: str) -> bool:
        """
        Determine if enhancement should be triggered

        Args:
            analysis: ComplexityAnalysis result
            persona: Target persona

        Returns:
            True if enhancement should be triggered
        """
        return analysis.recommended_enhancement is not None

    def select_enhancement_type(self, analysis: ComplexityAnalysis, persona: str) -> Optional[str]:
        """
        Select appropriate enhancement type based on analysis

        Args:
            analysis: ComplexityAnalysis result
            persona: Target persona

        Returns:
            Enhancement type string or None
        """
        return analysis.recommended_enhancement
