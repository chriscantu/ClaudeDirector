#!/usr/bin/env python3
"""
Framework Pattern Definitions for ClaudeDirector
Centralized framework patterns - eliminates hard-coded strings in framework detection
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class FrameworkDefinition:
    """Structured framework definition with patterns and metadata"""

    name: str
    patterns: List[str]
    type: str
    confidence_weight: float = 0.9


class FrameworkPatternRegistry:
    """Centralized registry of all strategic framework patterns"""

    def __init__(self):
        self._frameworks = self._initialize_frameworks()

    def _initialize_frameworks(self) -> Dict[str, FrameworkDefinition]:
        """Initialize all framework definitions"""
        return {
            # Strategic Frameworks
            "OGSM Strategic Framework": FrameworkDefinition(
                name="OGSM Strategic Framework",
                patterns=[
                    "ogsm",
                    "ogsm strategic framework",
                    "ogsm framework",
                    "objectives goals strategies measures",
                    "ogsm analysis",
                    "ogsm planning",
                    "ogsm strategic planning",
                ],
                type="strategic",
                confidence_weight=0.9,
            ),
            "Blue Ocean Strategy": FrameworkDefinition(
                name="Blue Ocean Strategy",
                patterns=[
                    "blue ocean strategy",
                    "blue ocean",
                    "uncontested market space",
                    "uncontested market spaces",
                    "value innovation",
                    "strategy canvas",
                    "four actions framework",
                    "blue ocean approach",
                ],
                type="strategic",
                confidence_weight=0.9,
            ),
            "Design Thinking": FrameworkDefinition(
                name="Design Thinking",
                patterns=[
                    "design thinking",
                    "design thinking process",
                    "design thinking methodology",
                    "empathize define ideate prototype test",
                    "human-centered design",
                    "design thinking framework",
                    "empathize",
                    "ideate",
                    "prototype",
                ],
                type="innovation",
                confidence_weight=0.9,
            ),
            "Porter's Five Forces": FrameworkDefinition(
                name="Porter's Five Forces",
                patterns=[
                    "porter's five forces",
                    "five forces analysis",
                    "competitive forces",
                    "porter five forces",
                    "threat of new entrants",
                    "bargaining power of suppliers",
                    "bargaining power of buyers",
                    "threat of substitute products",
                    "competitive rivalry",
                    "competitive intensity",
                    "industry structure analysis",
                    "industry attractiveness",
                    "competitive landscape analysis",
                    "market position analysis",
                    "competitive dynamics",
                    "industry forces",
                    "porter analysis",
                    "porter framework",
                    "porter model",
                    "five forces model",
                    "industry analysis",
                    "competitive environment analysis",
                    "market structure analysis",
                ],
                type="strategic",
                confidence_weight=0.95,
            ),
            "Jobs-to-be-Done": FrameworkDefinition(
                name="Jobs-to-be-Done",
                patterns=[
                    "jobs to be done",
                    "jobs-to-be-done",
                    "jtbd",
                    "customer jobs",
                    "job stories",
                    "when I",
                    "I want to",
                    "so I can",
                ],
                type="innovation",
                confidence_weight=0.9,
            ),
            "Lean Startup": FrameworkDefinition(
                name="Lean Startup",
                patterns=[
                    "lean startup",
                    "minimum viable product",
                    "mvp",
                    "build measure learn",
                    "build-measure-learn",
                    "validated learning",
                    "lean methodology",
                    "lean approach",
                    "lean principles",
                    "lean development",
                    "lean startup methodology",
                    "lean startup principles",
                    "lean startup approach",
                    "lean startup framework",
                    "lean startup process",
                    "lean startup cycle",
                    "lean startup loop",
                    "pivot",
                    "persevere",
                    "innovation accounting",
                    "actionable metrics",
                    "vanity metrics",
                    "cohort analysis",
                    "split testing",
                ],
                type="innovation",
                confidence_weight=0.92,
            ),
            "SWOT Analysis": FrameworkDefinition(
                name="SWOT Analysis",
                patterns=[
                    "swot analysis",
                    "swot",
                    "strengths weaknesses opportunities threats",
                    "strengths and weaknesses",
                    "opportunities and threats",
                ],
                type="strategic",
                confidence_weight=0.9,
            ),
            "Kotter's 8-Step Change Model": FrameworkDefinition(
                name="Kotter's 8-Step Change Model",
                patterns=[
                    "kotter",
                    "kotter's 8-step",
                    "8-step change",
                    "eight-step change",
                    "kotter change model",
                    "sense of urgency",
                    "guiding coalition",
                ],
                type="organizational",
                confidence_weight=0.9,
            ),
            "ADKAR Framework": FrameworkDefinition(
                name="ADKAR Framework",
                patterns=[
                    "adkar",
                    "awareness desire knowledge ability reinforcement",
                    "adkar framework",
                    "adkar model",
                    "change management",
                    "individual change",
                ],
                type="organizational",
                confidence_weight=0.9,
            ),
            # Team and Leadership Frameworks
            "Team Topologies": FrameworkDefinition(
                name="Team Topologies",
                patterns=[
                    "team topologies",
                    "Team Topologies",
                    "team structure",
                    "cognitive load",
                    "stream-aligned team",
                    "enabling team",
                    "complicated subsystem team",
                    "platform team",
                    "team interaction patterns",
                ],
                type="organizational",
                confidence_weight=0.95,
            ),
            "WRAP Framework": FrameworkDefinition(
                name="WRAP Framework",
                patterns=[
                    "wrap framework",
                    "WRAP framework",
                    "Apply the WRAP framework",
                    "apply the wrap framework",
                    "widen your options",
                    "reality-test your assumptions",
                    "attain distance before deciding",
                    "prepare to be wrong",
                ],
                type="decision-making",
                confidence_weight=0.95,
            ),
            "Good Strategy Bad Strategy": FrameworkDefinition(
                name="Good Strategy Bad Strategy",
                patterns=[
                    "strategy kernel",
                    "clear kernel",
                    "Our strategy needs a clear kernel",
                    "our strategy needs a clear kernel",
                    "diagnosis challenge guiding policy",
                    "good strategy bad strategy",
                    "Good Strategy Bad Strategy",
                    "rumelt framework",
                    "strategic kernel",
                    "coherent actions",
                ],
                type="strategic",
                confidence_weight=0.95,
            ),
            "Crucial Conversations": FrameworkDefinition(
                name="Crucial Conversations",
                patterns=[
                    "crucial conversations",
                    "Crucial Conversations",
                    "difficult conversations",
                    "high-stakes conversations",
                    "make it safe",
                    "start with heart",
                    "learn to look",
                    "speak persuasively",
                    "explore others' paths",
                    "move to action",
                    "crucial conversation skills",
                    "dialogue skills",
                    "pool of shared meaning",
                    "silence or violence",
                ],
                type="communication",
                confidence_weight=0.9,
            ),
            "Thinking in Systems": FrameworkDefinition(
                name="Thinking in Systems",
                patterns=[
                    "systems thinking",
                    "thinking in systems",
                    "system dynamics",
                    "leverage points",
                    "mental models",
                    "systems perspective",
                ],
                type="strategic",
                confidence_weight=0.85,
            ),
            # Design and UX Frameworks
            "Design System Scaling": FrameworkDefinition(
                name="Design System Scaling",
                patterns=[
                    "design system",
                    "design systems",
                    "component library",
                    "design tokens",
                    "design system scaling",
                ],
                type="design",
                confidence_weight=0.85,
            ),
            # Business Frameworks
            "Business Model Canvas": FrameworkDefinition(
                name="Business Model Canvas",
                patterns=[
                    "business model canvas",
                    "value proposition",
                    "customer segments",
                    "key partnerships",
                    "key activities",
                    "key resources",
                ],
                type="business",
                confidence_weight=0.9,
            ),
            "Competitive Analysis": FrameworkDefinition(
                name="Competitive Analysis",
                patterns=[
                    "competitive analysis",
                    "competitor analysis",
                    "competitive landscape",
                    "competitive positioning",
                    "competitive advantage",
                    "competitive intelligence",
                ],
                type="strategic",
                confidence_weight=0.85,
            ),
            # Platform and Technical Frameworks
            "Capital Allocation Framework": FrameworkDefinition(
                name="Capital Allocation Framework",
                patterns=[
                    "capital allocation",
                    "resource allocation",
                    "investment prioritization",
                    "platform investment",
                    "resource prioritization",
                    "investment framework",
                    "capital allocation framework",
                    "investment allocation",
                    "resource allocation framework",
                    "budget allocation",
                    "funding allocation",
                    "capacity allocation",
                    "engineering capacity",
                    "platform vs feature",
                    "investment strategy",
                    "resource strategy",
                    "engineering investment",
                    "technical investment",
                    "platform strategy investment",
                    "engineering resource allocation",
                ],
                type="strategic",
                confidence_weight=0.92,
            ),
            "Technical Strategy Framework": FrameworkDefinition(
                name="Technical Strategy Framework",
                patterns=[
                    "technical strategy",
                    "technology strategy",
                    "technical roadmap",
                    "architecture strategy",
                    "platform strategy",
                    "engineering strategy",
                    "technical vision",
                    "technology roadmap",
                    "architecture roadmap",
                    "platform roadmap",
                    "technical direction",
                    "technology direction",
                    "engineering direction",
                ],
                type="technical",
                confidence_weight=0.9,
            ),
            "Strategic Platform Assessment": FrameworkDefinition(
                name="Strategic Platform Assessment",
                patterns=[
                    "platform assessment",
                    "platform evaluation",
                    "platform maturity",
                    "platform health",
                    "platform strategy assessment",
                    "platform readiness",
                    "platform capability assessment",
                    "platform investment assessment",
                    "platform value assessment",
                    "platform ROI assessment",
                    "platform effectiveness",
                    "platform performance assessment",
                    "platform adoption assessment",
                ],
                type="technical",
                confidence_weight=0.9,
            ),
        }

    def get_framework_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Get framework patterns in legacy format for backward compatibility"""
        patterns = {}
        for name, definition in self._frameworks.items():
            patterns[name] = {
                "patterns": definition.patterns,
                "type": definition.type,
                "confidence_weight": definition.confidence_weight,
            }
        return patterns

    def get_framework_definition(self, name: str) -> FrameworkDefinition:
        """Get specific framework definition"""
        return self._frameworks.get(name)

    def get_all_frameworks(self) -> Dict[str, FrameworkDefinition]:
        """Get all framework definitions"""
        return self._frameworks.copy()

    def get_frameworks_by_type(
        self, framework_type: str
    ) -> Dict[str, FrameworkDefinition]:
        """Get frameworks filtered by type"""
        return {
            name: definition
            for name, definition in self._frameworks.items()
            if definition.type == framework_type
        }


# Global registry instance
FRAMEWORK_REGISTRY = FrameworkPatternRegistry()
