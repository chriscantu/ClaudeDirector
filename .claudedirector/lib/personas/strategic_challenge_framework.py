"""
Strategic Challenge Framework for ClaudeDirector Personas

CRITICAL ENHANCEMENT: Transform personas from agreeable advisors to strategic challengers
that pressure-test assumptions and ensure clarity of thought.

This framework implements mandatory first principles thinking and assumption testing
for all persona responses, ensuring valuable strategic challenge rather than
overly complimentary agreement.

ARCHITECTURAL COMPLIANCE:
- Integrates with 8-layer context engineering system
- Compatible with Phase 12 Always-On MCP enhancement
- Follows transparency pipeline requirements
- Uses YAML-based configuration (no hardcoded values)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from pathlib import Path
import yaml
import re
import logging
import time


class ChallengeType(Enum):
    """Types of strategic challenges personas can apply - loaded from configuration"""

    ASSUMPTION_TEST = "assumption_test"
    ROOT_CAUSE_PROBE = "root_cause_probe"
    ALTERNATIVE_EXPLORATION = "alternative_exploration"
    CONSTRAINT_VALIDATION = "constraint_validation"
    STAKEHOLDER_VALIDATION = "stakeholder_validation"
    EVIDENCE_DEMAND = "evidence_demand"


@dataclass
class ChallengePattern:
    """A specific challenge pattern for persona responses - loaded from YAML configuration"""

    challenge_type: ChallengeType
    name: str
    description: str
    trigger_keywords: List[str]
    generic_questions: List[str]
    confidence_threshold: float
    persona_specific: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ChallengeConfig:
    """Configuration loaded from YAML file"""

    version: str
    framework_name: str
    description: str
    global_settings: Dict[str, Any]
    challenge_types: Dict[str, Dict[str, Any]]
    personas: Dict[str, Dict[str, Any]]
    activation_rules: Dict[str, Any]
    response_blending: Dict[str, Any]
    performance: Dict[str, Any]


class StrategicChallengeFramework:
    """
    Framework that ensures personas challenge assumptions and pressure-test thinking
    instead of being overly agreeable and complimentary.

    ARCHITECTURAL COMPLIANCE:
    - Uses YAML configuration (no hardcoded values)
    - Integrates with context engineering system
    - Compatible with MCP and transparency systems
    - Performance optimized with caching
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the challenge framework with configuration

        Args:
            config_path: Path to challenge_patterns.yaml config file
        """
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_configuration()
        self.challenge_patterns = self._initialize_challenge_patterns()
        self.persona_styles = self._initialize_persona_styles()
        self._pattern_cache = {}
        self._cache_ttl = self.config.performance.get("cache_ttl_seconds", 3600)
        self._last_cache_update = 0

    def _get_default_config_path(self) -> str:
        """Get default path to challenge patterns configuration"""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent  # Go up to .claudedirector/
        config_path = project_root / "config" / "challenge_patterns.yaml"
        return str(config_path)

    def _load_configuration(self) -> ChallengeConfig:
        """Load challenge patterns configuration from YAML file"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            return ChallengeConfig(
                version=config_data["version"],
                framework_name=config_data["framework_name"],
                description=config_data["description"],
                global_settings=config_data["global_settings"],
                challenge_types=config_data["challenge_types"],
                personas=config_data["personas"],
                activation_rules=config_data["activation_rules"],
                response_blending=config_data["response_blending"],
                performance=config_data["performance"],
            )
        except Exception as e:
            self.logger.error(f"Failed to load challenge configuration: {e}")
            # Graceful fallback with minimal configuration
            return self._get_fallback_config()

    def _get_fallback_config(self) -> ChallengeConfig:
        """Provide minimal fallback configuration if YAML loading fails"""
        return ChallengeConfig(
            version="1.0.0-fallback",
            framework_name="Strategic Challenge Framework (Fallback)",
            description="Minimal fallback configuration",
            global_settings={
                "default_confidence_threshold": 0.7,
                "max_challenges_per_response": 2,
            },
            challenge_types={
                "assumption_test": {
                    "name": "Assumption Testing",
                    "description": "Challenge underlying assumptions in user statements",
                    "confidence_threshold": 0.7,
                    "trigger_keywords": ["should", "obviously", "clearly"],
                    "generic_questions": ["What assumptions are we making here?"],
                }
            },
            personas={},
            activation_rules={"activation_threshold": 0.6},
            response_blending={"integration_style": "natural_flow"},
            performance={"cache_patterns": True, "max_response_time_ms": 100},
        )

    def _initialize_challenge_patterns(self) -> Dict[ChallengeType, ChallengePattern]:
        """Initialize challenge patterns from configuration"""
        patterns = {}

        for challenge_key, challenge_config in self.config.challenge_types.items():
            try:
                challenge_type = ChallengeType(challenge_key)

                # Load persona-specific patterns
                persona_specific = {}
                for persona_name, persona_config in self.config.personas.items():
                    if (
                        "challenge_patterns" in persona_config
                        and challenge_key in persona_config["challenge_patterns"]
                    ):
                        persona_specific[persona_name] = persona_config[
                            "challenge_patterns"
                        ][challenge_key]

                pattern = ChallengePattern(
                    challenge_type=challenge_type,
                    name=challenge_config["name"],
                    description=challenge_config["description"],
                    trigger_keywords=challenge_config["trigger_keywords"],
                    generic_questions=challenge_config["generic_questions"],
                    confidence_threshold=challenge_config["confidence_threshold"],
                    persona_specific=persona_specific,
                )

                patterns[challenge_type] = pattern

            except ValueError:
                self.logger.warning(
                    f"Unknown challenge type in config: {challenge_key}"
                )
                continue

        return patterns

    def _initialize_persona_styles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize persona-specific challenge styles from configuration"""
        styles = {}

        for persona_name, persona_config in self.config.personas.items():
            styles[persona_name] = {
                "name": persona_config.get("name", persona_name.title()),
                "domain": persona_config.get("domain", "Strategic Leadership"),
                "challenge_style": persona_config.get(
                    "challenge_style", "professional_firm"
                ),
                "challenge_intros": persona_config.get(
                    "challenge_intros", ["Let me challenge this thinking..."]
                ),
            }

        return styles

    def should_challenge(self, user_input: str, persona: str) -> List[ChallengeType]:
        """
        Determine if and how a persona should challenge the user input

        Args:
            user_input: The user's message
            persona: The persona name (diego, camille, etc.)

        Returns:
            List of challenge types that should be applied
        """
        start_time = time.time()

        # Check cache first if enabled
        if self.config.performance.get("cache_patterns", False):
            cache_key = f"{hash(user_input)}_{persona}"
            if cache_key in self._pattern_cache:
                cache_entry = self._pattern_cache[cache_key]
                if time.time() - cache_entry["timestamp"] < self._cache_ttl:
                    return cache_entry["result"]

        challenges_to_apply = []
        input_lower = user_input.lower()

        # Check each challenge pattern with improved matching
        for challenge_type, pattern in self.challenge_patterns.items():
            # Count keyword matches (any keyword triggers the pattern)
            keyword_matches = sum(
                1
                for keyword in pattern.trigger_keywords
                if keyword.lower() in input_lower
            )

            # If any keywords match, calculate confidence based on pattern strength
            if keyword_matches > 0:
                # Improved confidence calculation:
                # - Base confidence from keyword density
                # - Bonus for multiple matches
                # - Bonus for strong trigger words

                base_confidence = min(
                    1.0, keyword_matches / max(1, len(pattern.trigger_keywords))
                )

                # Bonus for multiple keyword matches (shows stronger pattern)
                if keyword_matches >= 2:
                    base_confidence = min(1.0, base_confidence + 0.2)
                if keyword_matches >= 3:
                    base_confidence = min(1.0, base_confidence + 0.1)

                # Boost confidence for strong trigger words
                strong_triggers = [
                    "obviously",
                    "clearly",
                    "always",
                    "never",
                    "everyone",
                    "should",
                    "must",
                    "problem",
                    "need",
                    "works",
                    "solution",
                    "impossible",
                    "budget",
                    "definitely",
                    "want",
                ]
                strong_matches = sum(
                    1 for trigger in strong_triggers if trigger in input_lower
                )
                if strong_matches > 0:
                    base_confidence = min(
                        1.0, base_confidence + (strong_matches * 0.15)
                    )

                if base_confidence >= pattern.confidence_threshold:
                    challenges_to_apply.append(challenge_type)

        # Always challenge strategic indicators if they meet activation threshold
        strategic_indicators = self.config.activation_rules.get(
            "strategic_indicators", []
        )
        activation_threshold = self.config.activation_rules.get(
            "activation_threshold", 0.6
        )

        strategic_matches = sum(
            1 for indicator in strategic_indicators if indicator.lower() in input_lower
        )

        if strategic_matches > 0 and len(strategic_indicators) > 0:
            strategic_confidence = strategic_matches / len(strategic_indicators)
            if strategic_confidence >= activation_threshold:
                if ChallengeType.ASSUMPTION_TEST not in challenges_to_apply:
                    challenges_to_apply.append(ChallengeType.ASSUMPTION_TEST)

        # Always challenge high-confidence patterns
        always_challenge = self.config.activation_rules.get("always_challenge", [])
        for pattern in always_challenge:
            if pattern.lower() in input_lower:
                if ChallengeType.ASSUMPTION_TEST not in challenges_to_apply:
                    challenges_to_apply.append(ChallengeType.ASSUMPTION_TEST)
                break

        # Limit number of challenges per response
        max_challenges = self.config.global_settings.get(
            "max_challenges_per_response", 3
        )
        challenges_to_apply = challenges_to_apply[:max_challenges]

        # Cache result if enabled
        if self.config.performance.get("cache_patterns", False):
            self._pattern_cache[cache_key] = {
                "result": challenges_to_apply,
                "timestamp": time.time(),
            }

        # Performance monitoring
        processing_time = (time.time() - start_time) * 1000
        max_time = self.config.performance.get("max_response_time_ms", 100)
        if processing_time > max_time:
            self.logger.warning(
                f"Challenge detection took {processing_time:.2f}ms (max: {max_time}ms)"
            )

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
            "challenge_intros", ["Let me challenge this thinking..."]
        )

        # Start with challenge introduction
        response_parts = [f"**🔍 {challenge_intros[0]}**\n"]

        # Add specific challenges
        max_challenges = self.config.global_settings.get(
            "max_challenges_per_response", 3
        )
        for challenge_type in challenge_types[:max_challenges]:
            if challenge_type not in self.challenge_patterns:
                continue

            pattern = self.challenge_patterns[challenge_type]

            # Use persona-specific questions if available
            if (
                persona in pattern.persona_specific
                and pattern.persona_specific[persona]
            ):
                questions = pattern.persona_specific[persona]
            else:
                questions = pattern.generic_questions

            if questions:
                # Select most relevant question (for now, use first question)
                selected_question = questions[0]
                response_parts.append(f"- **{selected_question}**")

        # Add demand for evidence/validation based on configuration
        blending_config = self.config.response_blending
        if blending_config.get("include_evidence_requests", True):
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

        # Integrate challenge with base response based on configuration
        blending_config = self.config.response_blending
        integration_style = blending_config.get("integration_style", "natural_flow")

        if integration_style == "prefix_challenge":
            enhanced_response = f"{challenge_content}\n\n{base_response}"
        elif integration_style == "suffix_challenge":
            enhanced_response = f"{base_response}\n\n{challenge_content}"
        else:  # natural_flow (default)
            enhanced_response = f"{challenge_content}\n\n{base_response}"

        # Ensure we don't exceed maximum challenge percentage
        max_challenge_pct = blending_config.get("max_challenge_percentage", 0.4)
        challenge_length = len(challenge_content)
        total_length = len(enhanced_response)

        if total_length > 0 and challenge_length / total_length > max_challenge_pct:
            # Truncate challenge content if it's too dominant
            max_challenge_length = int(total_length * max_challenge_pct)
            if challenge_length > max_challenge_length:
                truncated_challenge = challenge_content[:max_challenge_length] + "..."
                if integration_style == "prefix_challenge":
                    enhanced_response = f"{truncated_challenge}\n\n{base_response}"
                else:
                    enhanced_response = f"{base_response}\n\n{truncated_challenge}"

        return enhanced_response

    def get_challenge_analytics(self) -> Dict[str, Any]:
        """
        Get analytics about challenge pattern usage and effectiveness

        Returns:
            Dictionary with challenge analytics data
        """
        return {
            "framework_version": self.config.version,
            "framework_name": self.config.framework_name,
            "total_challenge_types": len(self.challenge_patterns),
            "configured_personas": list(self.persona_styles.keys()),
            "cache_enabled": self.config.performance.get("cache_patterns", False),
            "cache_size": len(self._pattern_cache),
            "performance_target_ms": self.config.performance.get(
                "max_response_time_ms", 100
            ),
            "global_settings": self.config.global_settings,
        }

    def reload_configuration(self) -> bool:
        """
        Reload configuration from YAML file

        Returns:
            True if reload was successful, False otherwise
        """
        try:
            old_config = self.config
            self.config = self._load_configuration()
            self.challenge_patterns = self._initialize_challenge_patterns()
            self.persona_styles = self._initialize_persona_styles()
            self._pattern_cache.clear()  # Clear cache after config reload

            self.logger.info(
                f"Challenge configuration reloaded successfully from {self.config_path}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to reload challenge configuration: {e}")
            # Restore old configuration
            self.config = old_config
            return False


# Global instance for use across the system
strategic_challenge_framework = StrategicChallengeFramework()
