"""
Analysis Complexity Detector for MCP Integration
Determines when systematic analysis would add value to persona responses.

Author: Martin (Principal Platform Architect)
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import structlog

# Configure logging
logger = structlog.get_logger(__name__)


class AnalysisComplexity(Enum):
    """Complexity levels for user input analysis"""

    SIMPLE = "simple"  # Basic questions, standard persona response sufficient
    MEDIUM = "medium"  # Some complexity, might benefit from light enhancement - configured via ClaudeDirectorConfig
    COMPLEX = "complex"  # High complexity, systematic analysis recommended
    SYSTEMATIC = "systematic"  # Explicitly requesting systematic approach


class EnhancementStrategy(Enum):
    """Strategies for enhancing persona responses"""

    NONE = "none"  # No enhancement needed
    LIGHT_FRAMEWORK = "light_framework"  # Light framework reference
    SYSTEMATIC_ANALYSIS = "systematic_analysis"  # Full systematic analysis
    VISUAL_ENHANCEMENT = "visual_enhancement"  # Add visual components
    MULTI_PERSPECTIVE = "multi_perspective"  # Multiple persona coordination


@dataclass
class ComplexityAnalysis:
    """Result of complexity analysis"""

    complexity: AnalysisComplexity
    confidence: float  # 0.0 - 1.0
    enhancement_strategy: EnhancementStrategy
    recommended_capabilities: List[str]
    trigger_keywords: List[str]
    reasoning: str
    persona_suitability: Dict[str, float]  # persona -> suitability score


class AnalysisComplexityDetector:
    """
    Detects input complexity and determines appropriate enhancement strategy.

    Uses pattern matching, keyword analysis, and contextual cues to determine
    when MCP server enhancement would add significant value.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

        # Complexity indicators - patterns that suggest need for systematic analysis
        self.complexity_patterns = {
            AnalysisComplexity.SYSTEMATIC: [
                # Explicit systematic requests
                r"systematic(ally)?",
                r"step[- ]by[- ]step",
                r"framework",
                r"methodology",
                r"structured approach",
                r"comprehensive analysis",
                r"thorough evaluation",
                # Planning and strategy patterns
                r"strategic plan",
                r"quarterly plan",
                r"annual plan",
                r"roadmap",
                r"assessment",
                # Decision-making patterns
                r"decision framework",
                r"evaluation criteria",
                r"trade[- ]?offs?",
                r"pros and cons",
                r"risk assessment",
            ],
            AnalysisComplexity.COMPLEX: [
                # Organizational complexity
                r"organizational?",
                r"team structure",
                r"restructur(e|ing)",
                r"scaling",
                r"cross[- ]team",
                r"stakeholder",
                r"alignment",
                # Strategic complexity
                r"strategy",
                r"vision",
                r"transformation",
                r"initiative",
                r"investment",
                r"prioriti[sz]ation",
                # Technical complexity
                r"architecture",
                r"platform",
                r"technical debt",
                r"migration",
                r"integration",
                r"system design",
                # Problem-solving complexity
                r"challenge",
                r"problem",
                r"issue",
                r"crisis",
                r"conflict",
                r"bottleneck",
            ],
            AnalysisComplexity.MEDIUM: [
                # Moderate complexity indicators
                r"how (do|should) (I|we)",
                r"what (is|are) the best",
                r"help me (with|understand)",
                r"advice",
                r"recommendation",
                r"guidance",
                r"approach",
                r"thoughts on",
                r"opinion",
            ],
        }

        # Domain-specific keywords that increase complexity
        self.domain_keywords = {
            "strategic": [
                "strategic",
                "strategy",
                "planning",
                "roadmap",
                "vision",
                "objectives",
                "goals",
                "priorities",
                "initiative",
            ],
            "organizational": [
                "team",
                "org",
                "organizational",
                "structure",
                "reporting",
                "hierarchy",
                "roles",
                "responsibilities",
                "culture",
            ],
            "technical": [
                "architecture",
                "platform",
                "system",
                "technical",
                "engineering",
                "infrastructure",
                "design",
                "implementation",
                "technology",
            ],
            "process": [
                "process",
                "workflow",
                "procedure",
                "methodology",
                "framework",
                "governance",
                "standards",
                "practices",
                "guidelines",
            ],
            "people": [
                "leadership",
                "management",
                "development",
                "career",
                "performance",
                "hiring",
                "onboarding",
                "mentoring",
                "coaching",
                "feedback",
            ],
        }

        # Persona capability mapping
        self.persona_capabilities = {
            "diego": {
                "domains": ["strategic", "organizational", "people"],
                "specialties": [
                    "team_scaling",
                    "cross_team_coordination",
                    "strategic_planning",
                ],
                "mcp_servers": ["sequential", "context7"],
            },
            "martin": {
                "domains": ["technical", "process"],
                "specialties": [
                    "architecture",
                    "technical_debt",
                    "evolutionary_design",
                ],
                "mcp_servers": ["context7"],
            },
            "rachel": {
                "domains": ["process", "organizational"],
                "specialties": [
                    "design_systems",
                    "cross_team_alignment",
                    "user_experience",
                ],
                "mcp_servers": ["context7", "magic"],
            },
            "camille": {
                "domains": ["strategic", "organizational", "people"],
                "specialties": [
                    "leadership",
                    "organizational_health",
                    "strategic_technology",
                ],
                "mcp_servers": ["sequential", "context7"],
            },
            "alvaro": {
                "domains": ["strategic", "process"],
                "specialties": [
                    "product_strategy",
                    "business_value",
                    "market_analysis",
                ],
                "mcp_servers": ["magic", "sequential"],
            },
        }

        # Visual enhancement triggers
        self.visual_triggers = [
            "diagram",
            "chart",
            "visual",
            "presentation",
            "slide",
            "graphic",
            "map",
            "flow",
            "process",
            "timeline",
            "roadmap",
            "dashboard",
        ]

        # Framework request triggers
        self.framework_triggers = [
            "framework",
            "methodology",
            "best practice",
            "pattern",
            "model",
            "approach",
            "standard",
            "guideline",
            "template",
            "checklist",
        ]

    def analyze_input_complexity(
        self, user_input: str, context: Optional[Dict] = None
    ) -> ComplexityAnalysis:
        """
        Analyze user input to determine complexity and enhancement needs.

        Args:
            user_input: The user's message/question
            context: Optional context (persona, conversation history, etc.)

        Returns:
            ComplexityAnalysis with recommendations
        """
        # Normalize input for analysis
        normalized_input = user_input.lower().strip()

        # Initialize analysis components
        complexity_scores = {level: 0.0 for level in AnalysisComplexity}
        trigger_keywords = []
        domain_scores = {domain: 0.0 for domain in self.domain_keywords}

        # Pattern matching for complexity levels
        for complexity_level, patterns in self.complexity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, normalized_input, re.IGNORECASE)
                if matches:
                    complexity_scores[complexity_level] += len(matches) * 0.3
                    # Ensure matches are strings (flatten any tuple results from regex groups)
                    string_matches = [
                        (
                            str(match)
                            if isinstance(match, str)
                            else (
                                str(match[0])
                                if isinstance(match, tuple)
                                else str(match)
                            )
                        )
                        for match in matches
                    ]
                    trigger_keywords.extend(string_matches)

        # Domain keyword analysis
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in normalized_input:
                    domain_scores[domain] += 0.2
                    trigger_keywords.append(keyword)

        # Length and structure analysis
        word_count = len(normalized_input.split())
        sentence_count = len([s for s in normalized_input.split(".") if s.strip()])

        # Longer, more structured inputs tend to be more complex
        if word_count > 50:
            complexity_scores[AnalysisComplexity.COMPLEX] += 0.2
        elif word_count > 20:
            complexity_scores[AnalysisComplexity.MEDIUM] += 0.2

        if sentence_count > 3:
            complexity_scores[AnalysisComplexity.COMPLEX] += 0.1

        # Question complexity analysis
        question_words = ["how", "why", "what", "when", "where", "which"]
        question_count = sum(1 for word in question_words if word in normalized_input)

        if question_count > 1:
            complexity_scores[AnalysisComplexity.COMPLEX] += 0.15

        # Determine final complexity level
        max_score = max(complexity_scores.values())
        primary_complexity = max(complexity_scores.items(), key=lambda x: x[1])[0]

        # Adjust for minimum thresholds
        if max_score < 0.3:
            primary_complexity = AnalysisComplexity.SIMPLE
            confidence = max_score / 0.3
        else:
            confidence = min(max_score, 1.0)

        # Determine enhancement strategy
        enhancement_strategy = self._determine_enhancement_strategy(
            primary_complexity, domain_scores, normalized_input
        )

        # Determine recommended capabilities
        recommended_capabilities = self._determine_capabilities(
            domain_scores, enhancement_strategy
        )

        # Calculate persona suitability
        persona_suitability = self._calculate_persona_suitability(
            domain_scores, recommended_capabilities, context
        )

        # Generate reasoning
        reasoning = self._generate_reasoning(
            primary_complexity, domain_scores, trigger_keywords, enhancement_strategy
        )

        return ComplexityAnalysis(
            complexity=primary_complexity,
            confidence=confidence,
            enhancement_strategy=enhancement_strategy,
            recommended_capabilities=recommended_capabilities,
            trigger_keywords=list(set(trigger_keywords)),
            reasoning=reasoning,
            persona_suitability=persona_suitability,
        )

    def _determine_enhancement_strategy(
        self,
        complexity: AnalysisComplexity,
        domain_scores: Dict[str, float],
        normalized_input: str,
    ) -> EnhancementStrategy:
        """Determine the appropriate enhancement strategy"""

        # Check for visual enhancement triggers
        if any(trigger in normalized_input for trigger in self.visual_triggers):
            return EnhancementStrategy.VISUAL_ENHANCEMENT

        # Check for explicit framework requests
        if any(trigger in normalized_input for trigger in self.framework_triggers):
            return EnhancementStrategy.LIGHT_FRAMEWORK

        # Determine by complexity level
        if complexity == AnalysisComplexity.SYSTEMATIC:
            return EnhancementStrategy.SYSTEMATIC_ANALYSIS
        elif complexity == AnalysisComplexity.COMPLEX:
            # High domain scores suggest systematic analysis would be valuable
            max_domain_score = max(domain_scores.values())
            if max_domain_score > 0.4:
                return EnhancementStrategy.SYSTEMATIC_ANALYSIS
            else:
                return EnhancementStrategy.LIGHT_FRAMEWORK
        elif complexity == AnalysisComplexity.MEDIUM:
            return EnhancementStrategy.LIGHT_FRAMEWORK
        else:
            return EnhancementStrategy.NONE

    def _determine_capabilities(
        self, domain_scores: Dict[str, float], strategy: EnhancementStrategy
    ) -> List[str]:
        """Determine what MCP server capabilities would be most valuable"""
        capabilities = []

        if strategy == EnhancementStrategy.NONE:
            return capabilities

        # Map domains to capabilities
        domain_capability_map = {
            "strategic": ["systematic_analysis", "strategic_planning"],
            "organizational": ["systematic_analysis", "leadership_frameworks"],
            "technical": ["pattern_access", "architectural_patterns"],
            "process": ["methodology_lookup", "best_practices"],
            "people": ["leadership_frameworks", "best_practices"],
        }

        # Add capabilities based on domain scores
        for domain, score in domain_scores.items():
            if score > 0.2:  # Threshold for relevance
                capabilities.extend(domain_capability_map.get(domain, []))

        # Add strategy-specific capabilities
        if strategy == EnhancementStrategy.VISUAL_ENHANCEMENT:
            capabilities.extend(["diagram_generation", "visual_storytelling"])
        elif strategy == EnhancementStrategy.SYSTEMATIC_ANALYSIS:
            capabilities.extend(["systematic_analysis", "framework_application"])

        return list(set(capabilities))  # Remove duplicates

    def _calculate_persona_suitability(
        self,
        domain_scores: Dict[str, float],
        capabilities: List[str],
        context: Optional[Dict] = None,
    ) -> Dict[str, float]:
        """Calculate how suitable each persona is for this analysis"""
        suitability = {}

        for persona, persona_info in self.persona_capabilities.items():
            score = 0.0

            # Domain alignment
            for domain in persona_info["domains"]:
                score += domain_scores.get(domain, 0.0) * 0.4

            # Capability alignment
            persona_specialties = persona_info.get("specialties", [])
            for capability in capabilities:
                if any(specialty in capability for specialty in persona_specialties):
                    score += 0.3

            # MCP server availability
            persona_servers = persona_info.get("mcp_servers", [])
            if persona_servers and capabilities:
                score += 0.2  # Bonus for having MCP integration

            # Current context (if this persona is already active)
            if context and context.get("current_persona") == persona:
                score += 0.1  # Small bonus for continuity

            suitability[persona] = min(score, 1.0)

        return suitability

    def _generate_reasoning(
        self,
        complexity: AnalysisComplexity,
        domain_scores: Dict[str, float],
        trigger_keywords: List[str],
        strategy: EnhancementStrategy,
    ) -> str:
        """Generate human-readable reasoning for the analysis"""

        reasoning_parts = []

        # Complexity reasoning
        if complexity == AnalysisComplexity.SYSTEMATIC:
            reasoning_parts.append("Input explicitly requests systematic analysis")
        elif complexity == AnalysisComplexity.COMPLEX:
            reasoning_parts.append(
                "Input shows high complexity requiring structured approach"
            )
        elif complexity == AnalysisComplexity.MEDIUM:
            reasoning_parts.append(
                "Input has moderate complexity that could benefit from enhancement"
            )
        else:
            reasoning_parts.append(
                "Input is straightforward and suitable for standard response"
            )

        # Domain reasoning
        significant_domains = [
            domain for domain, score in domain_scores.items() if score > 0.3
        ]
        if significant_domains:
            reasoning_parts.append(f"Primary domains: {', '.join(significant_domains)}")

        # Trigger keywords
        if trigger_keywords:
            # Ensure all keywords are strings (filter out any tuples)
            string_keywords = [
                str(kw) for kw in trigger_keywords if isinstance(kw, (str, tuple))
            ]
            if string_keywords:
                top_keywords = sorted(
                    set(string_keywords), key=string_keywords.count, reverse=True
                )[:3]
                reasoning_parts.append(f"Key triggers: {', '.join(top_keywords)}")

        # Strategy reasoning
        strategy_explanations = {
            EnhancementStrategy.SYSTEMATIC_ANALYSIS: "Systematic analysis recommended for comprehensive insight",
            EnhancementStrategy.LIGHT_FRAMEWORK: "Light framework reference would add value",
            EnhancementStrategy.VISUAL_ENHANCEMENT: "Visual components would enhance understanding",
            EnhancementStrategy.MULTI_PERSPECTIVE: "Multiple persona perspectives recommended",
            EnhancementStrategy.NONE: "Standard persona response sufficient",
        }

        reasoning_parts.append(strategy_explanations[strategy])

        return ". ".join(reasoning_parts)

    def should_enhance_with_mcp(
        self,
        analysis: ComplexityAnalysis,
        persona: str,
        thresholds: Optional[Dict[str, float]] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        PHASE 12: Always-on MCP enhancement - removed complexity thresholds

        Always returns True for guaranteed 100% enhancement rate.
        Returns persona's primary MCP server for direct routing.

        Args:
            analysis: ComplexityAnalysis (kept for API compatibility)
            persona: The target persona name
            thresholds: Ignored (kept for API compatibility)

        Returns:
            Tuple of (True, recommended_server) - always enhance
        """
        # PHASE 12: Always-on enhancement - import persona mapping from unified engine
        from ..personas.unified_persona_engine import UnifiedPersonaEngine

        # Get persona's primary MCP server
        recommended_server = UnifiedPersonaEngine.PERSONA_SERVER_MAPPING.get(
            persona, "sequential"
        )

        # Always enhance with persona's primary server
        return True, recommended_server

    def get_enhancement_context(self, analysis: ComplexityAnalysis) -> Dict[str, Any]:
        """
        Generate context information for MCP server requests.

        Args:
            analysis: The complexity analysis result

        Returns:
            Context dictionary for MCP requests
        """
        return {
            "complexity_level": analysis.complexity.value,
            "confidence": analysis.confidence,
            "strategy": analysis.enhancement_strategy.value,
            "domains": [
                domain
                for domain, score in zip(
                    self.domain_keywords.keys(),
                    [
                        analysis.persona_suitability.get(p, 0)
                        for p in self.persona_capabilities.keys()
                    ],
                )
                if score > 0.3
            ],
            "capabilities": analysis.recommended_capabilities,
            "keywords": analysis.trigger_keywords,
            "reasoning": analysis.reasoning,
        }
