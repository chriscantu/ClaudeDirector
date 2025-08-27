"""
Strategic Framework Detection Middleware
Identifies and attributes strategic frameworks used in ClaudeDirector responses
SOLID Compliance: Uses centralized configuration instead of hard-coded strings
"""

from typing import List, Dict
from dataclasses import dataclass

# Import centralized configuration
try:
    from core.constants.framework_definitions import FRAMEWORK_REGISTRY
    from core.constants.constants import PERSONAS, TRANSPARENCY

    CENTRALIZED_CONFIG_AVAILABLE = True
except ImportError:
    # Graceful fallback for transition period
    CENTRALIZED_CONFIG_AVAILABLE = False


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
        # Use centralized configuration or fallback to legacy patterns
        if CENTRALIZED_CONFIG_AVAILABLE:
            self.framework_patterns = FRAMEWORK_REGISTRY.get_framework_patterns()
            self.confidence_threshold = 0.7  # From centralized config
        else:
            # Legacy fallback patterns for compatibility
            self.framework_patterns = self._get_legacy_patterns()
            self.confidence_threshold = 0.7

    def _get_legacy_patterns(self):
        """Legacy framework patterns for backward compatibility"""
        # All patterns now centralized in framework_definitions.py
        return {}

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
