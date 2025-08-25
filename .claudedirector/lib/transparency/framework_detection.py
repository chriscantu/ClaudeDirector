"""
Strategic Framework Detection Middleware
Identifies and attributes strategic frameworks used in ClaudeDirector responses
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class FrameworkUsage:
    """Represents usage of a strategic framework"""

    framework_name: str
    confidence_score: float
    matched_patterns: List[str]
    framework_type: str  # 'strategic', 'architectural', 'business', etc.


class FrameworkDetectionMiddleware:
    """Middleware to detect and attribute strategic frameworks used in responses"""

    def __init__(self):
        # Strategic framework patterns with confidence weights
        self.framework_patterns = {
            # Common Strategic Frameworks (High Priority)
            "OGSM Strategic Framework": {
                "patterns": [
                    "ogsm",
                    "ogsm strategic framework",
                    "ogsm framework",
                    "objectives goals strategies measures",
                    "ogsm analysis",
                    "ogsm planning",
                    "ogsm strategic planning",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
            "Blue Ocean Strategy": {
                "patterns": [
                    "blue ocean strategy",
                    "blue ocean",
                    "uncontested market space",
                    "uncontested market spaces",
                    "value innovation",
                    "strategy canvas",
                    "four actions framework",
                    "blue ocean approach",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
            "Design Thinking": {
                "patterns": [
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
                "type": "innovation",
                "confidence_weight": 0.9,
            },
            "Porter's Five Forces": {
                "patterns": [
                    "porter's five forces",
                    "five forces analysis",
                    "competitive forces",
                    "porter five forces",
                    "competitive analysis framework",
                    "industry analysis",
                    "porter's five forces analysis",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
            "BCG Matrix": {
                "patterns": [
                    "bcg matrix",
                    "boston consulting group matrix",
                    "stars cash cows dogs question marks",
                    "bcg growth share matrix",
                    "portfolio analysis",
                    "question mark products",
                    "cash cows",
                    "stars",
                ],
                "type": "strategic",
                "confidence_weight": 0.8,
            },
            "Jobs-to-be-Done": {
                "patterns": [
                    "jobs-to-be-done",
                    "jobs to be done",
                    "jtbd framework",
                    "customer jobs",
                    "jobs-to-be-done framework",
                    "job story",
                ],
                "type": "innovation",
                "confidence_weight": 0.8,
            },
            "Lean Startup": {
                "patterns": [
                    "lean startup",
                    "lean startup methodology",
                    "minimum viable product",
                    "mvp development",
                    "build measure learn",
                    "validated learning",
                    "mvp",
                ],
                "type": "innovation",
                "confidence_weight": 0.8,
            },
            "OKRs": {
                "patterns": [
                    "okr",
                    "okrs",
                    "objectives and key results",
                    "objective key results",
                    "okr framework",
                    "quarterly objectives",
                ],
                "type": "strategic",
                "confidence_weight": 0.8,
            },
            "SWOT Analysis": {
                "patterns": [
                    "swot analysis",
                    "swot framework",
                    "strengths weaknesses opportunities threats",
                    "swot matrix",
                    "internal external analysis",
                ],
                "type": "strategic",
                "confidence_weight": 0.8,
            },
            "Kotter's 8-Step Change Model": {
                "patterns": [
                    "kotter's 8-step",
                    "kotter 8 step",
                    "8-step change model",
                    "kotter change model",
                    "create urgency",
                    "guiding coalition",
                ],
                "type": "change_management",
                "confidence_weight": 0.8,
            },
            "ADKAR Framework": {
                "patterns": [
                    "adkar",
                    "adkar framework",
                    "awareness desire knowledge ability reinforcement",
                    "adkar change model",
                ],
                "type": "change_management",
                "confidence_weight": 0.8,
            },
            # Specialized ClaudeDirector Frameworks
            "Sequential": {
                "patterns": [
                    "sequential server",
                    "systematic analysis",
                    "strategic framework analysis",
                    "systematic strategic analysis",
                    "sequential methodology",
                    "strategic analysis framework",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
            "Context7": {
                "patterns": [
                    "context7 server",
                    "proven patterns",
                    "architectural patterns",
                    "design system methodology",
                    "established architectural patterns",
                    "context7 framework",
                    "proven architectural methodologies",
                ],
                "type": "architectural_patterns",
                "confidence_weight": 0.9,
            },
            "Magic": {
                "patterns": [
                    "magic server",
                    "diagram generation",
                    "visualization",
                    "business visualization",
                    "presentation creation",
                    "magic implementation",
                ],
                "type": "implementation",
                "confidence_weight": 0.8,
            },
            "Team Topologies": {
                "patterns": [
                    "team topologies",
                    "Team Topologies",
                    "team structure",
                    "conway's law",
                    "cognitive load",
                    "team topology patterns",
                    "stream-aligned teams",
                    "platform teams",
                    "complicated subsystem teams",
                ],
                "type": "organizational",
                "confidence_weight": 0.8,
            },
            "WRAP Framework": {
                "patterns": [
                    "wrap framework",
                    "WRAP framework",
                    "Apply the WRAP framework",
                    "apply the wrap framework",
                    "wrap analysis",
                    "wrap decision",
                    "widen your options",
                    "reality-test",
                    "attain distance",
                    "prepare to be wrong",
                ],
                "type": "decision",
                "confidence_weight": 0.8,
            },
            "Good Strategy Bad Strategy": {
                "patterns": [
                    "strategy kernel",
                    "clear kernel",
                    "Our strategy needs a clear kernel",
                    "our strategy needs a clear kernel",
                    "strategic analysis",
                    "good strategy bad strategy",
                    "Good Strategy Bad Strategy",
                    "rumelt framework",
                    "diagnosis",
                    "guiding policy",
                    "coherent action",
                ],
                "type": "strategic",
                "confidence_weight": 0.7,
            },
            "Crucial Conversations": {
                "patterns": [
                    "crucial conversations",
                    "difficult conversations",
                    "crucial conversation framework",
                    "start with heart",
                    "learn to look",
                    "make it safe",
                    "state your path",
                ],
                "type": "communication",
                "confidence_weight": 0.7,
            },
            "Accelerate": {
                "patterns": [
                    "accelerate framework",
                    "elite performance",
                    "deployment frequency",
                    "lead time",
                    "change failure rate",
                    "recovery time",
                    "dora metrics",
                ],
                "type": "performance",
                "confidence_weight": 0.8,
            },
            "Thinking in Systems": {
                "patterns": [
                    "systems thinking",
                    "feedback loops",
                    "leverage points",
                    "system patterns",
                    "systems behavior",
                    "mental models",
                    "system structure",
                ],
                "type": "systems",
                "confidence_weight": 0.7,
            },
            "Design System Scaling": {
                "patterns": [
                    "design system scaling",
                    "federated governance",
                    "design system methodology",
                    "component adoption",
                    "design system maturity",
                    "cross-team design coordination",
                ],
                "type": "design",
                "confidence_weight": 0.8,
            },
            "Business Model Canvas": {
                "patterns": [
                    "business model canvas",
                    "value proposition",
                    "customer segments",
                    "revenue streams",
                    "key partnerships",
                    "business model framework",
                ],
                "type": "business",
                "confidence_weight": 0.8,
            },
            "Competitive Analysis": {
                "patterns": [
                    "competitive analysis",
                    "competitive positioning",
                    "market positioning",
                    "competitive intelligence",
                    "competitive advantage",
                    "market differentiation",
                ],
                "type": "business",
                "confidence_weight": 0.7,
            },
            # Missing Strategic Frameworks - Completing 25+ Framework Target
            "Capital Allocation Framework": {
                "patterns": [
                    "capital allocation",
                    "resource allocation",
                    "engineering budget",
                    "platform investment",
                    "feature vs platform",
                    "roi analysis",
                    "resource prioritization",
                    "investment strategy",
                    "budget planning",
                    "engineering resource investment",
                    "platform vs feature trade-offs",
                    "capital allocation framework",
                    "roi metrics",
                    "present.*platform.*investment",
                    "investment.*board",
                    "platform.*roi",
                    "board.*roi",
                    "investment.*metrics",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
            "Technical Strategy Framework": {
                "patterns": [
                    "technical strategy",
                    "technology roadmap",
                    "architecture decisions",
                    "technical debt",
                    "technology planning",
                    "technical strategy framework",
                    "architectural decisions",
                    "tech debt management",
                    "technology architecture",
                    "technical roadmap planning",
                    "engineering strategy",
                    "technology investment",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
            "Strategic Platform Assessment": {
                "patterns": [
                    "platform assessment",
                    "platform maturity",
                    "platform evaluation",
                    "platform health",
                    "platform adoption",
                    "platform effectiveness",
                    "strategic platform assessment",
                    "platform maturity model",
                    "platform investment evaluation",
                    "platform strategy assessment",
                    "five-phase platform evaluation",
                    "platform readiness assessment",
                ],
                "type": "strategic",
                "confidence_weight": 0.9,
            },
        }

        # Persona-specific attribution templates
        self.persona_attribution_templates = {
            "diego": "This analysis combines {frameworks} methodology, adapted through my organizational leadership experience.",
            "camille": "This strategic approach uses {frameworks} framework, positioned through my executive technology leadership perspective.",
            "rachel": "This recommendation follows {frameworks} methodology, customized through my cross-functional design experience.",
            "alvaro": "This analysis leverages {frameworks} framework, applied through my competitive business strategy experience.",
            "martin": "This approach uses {frameworks} patterns, adapted through my evolutionary architecture experience.",
        }

        # Minimum confidence threshold for framework attribution
        self.confidence_threshold = 0.6

    def detect_frameworks_used(self, response_content: str) -> List[FrameworkUsage]:
        """Detect strategic frameworks used in a response"""
        detected_frameworks = []

        # Normalize content for pattern matching
        content_lower = response_content.lower()

        for framework_name, framework_config in self.framework_patterns.items():
            patterns = framework_config["patterns"]
            framework_type = framework_config["type"]
            base_confidence = framework_config["confidence_weight"]

            matched_patterns = []
            confidence_score = 0.0

            # Check each pattern
            for pattern in patterns:
                pattern_lower = pattern.lower()

                # Count occurrences of this pattern
                pattern_count = content_lower.count(pattern_lower)

                if pattern_count > 0:
                    matched_patterns.append(pattern)
                    # Add confidence based on pattern occurrence
                    confidence_score += min(
                        pattern_count * 0.3, 0.8
                    )  # Cap per pattern at 0.8

            # Apply base confidence weight
            if matched_patterns:
                confidence_score = min(confidence_score * base_confidence, 1.0)

                # Only include if above threshold
                if confidence_score >= self.confidence_threshold:
                    detected_frameworks.append(
                        FrameworkUsage(
                            framework_name=framework_name,
                            confidence_score=confidence_score,
                            matched_patterns=matched_patterns,
                            framework_type=framework_type,
                        )
                    )

        # Sort by confidence score (highest first)
        detected_frameworks.sort(key=lambda f: f.confidence_score, reverse=True)

        return detected_frameworks

    def create_framework_attribution(
        self, persona: str, frameworks: List[FrameworkUsage]
    ) -> str:
        """Generate framework attribution text for a persona"""
        if not frameworks:
            return ""

        # Get framework names for high-confidence frameworks only
        high_confidence_frameworks = [
            f for f in frameworks if f.confidence_score >= 0.8
        ]

        if not high_confidence_frameworks:
            # Use top framework if no high-confidence ones
            high_confidence_frameworks = frameworks[:1]

        framework_names = [f.framework_name for f in high_confidence_frameworks]

        if len(framework_names) == 1:
            frameworks_text = framework_names[0]
        elif len(framework_names) == 2:
            frameworks_text = f"{framework_names[0]} and {framework_names[1]}"
        else:
            frameworks_text = (
                ", ".join(framework_names[:-1]) + f", and {framework_names[-1]}"
            )

        # Get persona-specific template
        template = self.persona_attribution_templates.get(
            persona, self.persona_attribution_templates["diego"]
        )

        return template.format(frameworks=frameworks_text)

    def add_framework_attribution(
        self, persona: str, response: str, frameworks: List[FrameworkUsage]
    ) -> str:
        """Add framework attribution to a response"""
        if not frameworks:
            return response

        attribution = self.create_framework_attribution(persona, frameworks)

        if attribution:
            return f"{response}\n\n---\n\n**Framework Attribution**: {attribution}"

        return response

    def get_framework_summary(self, frameworks: List[FrameworkUsage]) -> Dict[str, any]:
        """Get summary information about detected frameworks"""
        if not frameworks:
            return {
                "total_frameworks": 0,
                "framework_types": [],
                "highest_confidence": 0.0,
                "frameworks_used": [],
            }

        framework_types = list(set(f.framework_type for f in frameworks))
        frameworks_used = [f.framework_name for f in frameworks]
        highest_confidence = max(f.confidence_score for f in frameworks)

        return {
            "total_frameworks": len(frameworks),
            "framework_types": framework_types,
            "highest_confidence": highest_confidence,
            "frameworks_used": frameworks_used,
        }

    def create_framework_disclosure(self, frameworks: List[FrameworkUsage]) -> str:
        """Create a simple framework disclosure for transparency"""
        if not frameworks:
            return ""

        # Only show frameworks with confidence >= 0.7
        high_confidence = [f for f in frameworks if f.confidence_score >= 0.7]

        if not high_confidence:
            return ""

        framework_names = [f.framework_name for f in high_confidence]

        if len(framework_names) == 1:
            return f"📚 Strategic Framework: {framework_names[0]}"
        else:
            return f"📚 Strategic Frameworks: {', '.join(framework_names)}"
