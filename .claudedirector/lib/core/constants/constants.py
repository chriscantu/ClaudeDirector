#!/usr/bin/env python3
"""
Centralized Configuration Constants for ClaudeDirector
Eliminates hard-coded strings throughout the system - SOLID Compliance Initiative
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from pathlib import Path


@dataclass
class FrameworkConstants:
    """Strategic framework definitions and patterns"""

    # Framework Names (consistent across system)
    TEAM_TOPOLOGIES = "Team Topologies"
    GOOD_STRATEGY_BAD_STRATEGY = "Good Strategy Bad Strategy"
    WRAP_FRAMEWORK = "WRAP Framework"
    CRUCIAL_CONVERSATIONS = "Crucial Conversations"
    DESIGN_THINKING = "Design Thinking"
    PORTER_FIVE_FORCES = "Porter's Five Forces"
    BLUE_OCEAN_STRATEGY = "Blue Ocean Strategy"
    JOBS_TO_BE_DONE = "Jobs-to-be-Done"
    LEAN_STARTUP = "Lean Startup"
    SWOT_ANALYSIS = "SWOT Analysis"
    KOTTER_8_STEP = "Kotter's 8-Step Change Model"
    ADKAR_FRAMEWORK = "ADKAR Framework"
    BUSINESS_MODEL_CANVAS = "Business Model Canvas"
    COMPETITIVE_ANALYSIS = "Competitive Analysis"
    CAPITAL_ALLOCATION_FRAMEWORK = "Capital Allocation Framework"
    TECHNICAL_STRATEGY_FRAMEWORK = "Technical Strategy Framework"
    STRATEGIC_PLATFORM_ASSESSMENT = "Strategic Platform Assessment"
    OGSM_STRATEGIC_FRAMEWORK = "OGSM Strategic Framework"
    THINKING_IN_SYSTEMS = "Thinking in Systems"
    DESIGN_SYSTEM_SCALING = "Design System Scaling"

    # Framework Categories
    STRATEGIC_FRAMEWORKS = "Strategic Frameworks"
    ORGANIZATIONAL_FRAMEWORKS = "Organizational Frameworks"
    TECHNICAL_FRAMEWORKS = "Technical Frameworks"
    DESIGN_FRAMEWORKS = "Design Frameworks"


@dataclass
class PersonaConstants:
    """Strategic persona definitions"""

    # Persona Names
    DIEGO = "Diego"
    CAMILLE = "Camille"
    RACHEL = "Rachel"
    ALVARO = "Alvaro"
    MARTIN = "Martin"
    MARCUS = "Marcus"
    DAVID = "David"
    SOFIA = "Sofia"
    ELENA = "Elena"

    # Persona Domains
    ENGINEERING_LEADERSHIP = "Engineering Leadership"
    STRATEGIC_TECHNOLOGY = "Strategic Technology"
    DESIGN_SYSTEMS_STRATEGY = "Design Systems Strategy"
    BUSINESS_STRATEGY = "Business Strategy"
    PLATFORM_ARCHITECTURE = "Platform Architecture"
    CHANGE_MANAGEMENT = "Change Management"
    FINANCIAL_STRATEGY = "Financial Strategy"
    VENDOR_STRATEGY = "Vendor Strategy"
    COMPLIANCE_STRATEGY = "Compliance Strategy"

    # Persona Templates
    ATTRIBUTION_TEMPLATES = {
        DIEGO: "This analysis combines {frameworks} methodology, adapted through my organizational leadership experience.",
        CAMILLE: "This strategic approach uses {frameworks} framework, positioned through my executive technology leadership perspective.",
        RACHEL: "This recommendation follows {frameworks} methodology, customized through my cross-functional design experience.",
        ALVARO: "This analysis leverages {frameworks} framework, applied through my competitive business strategy experience.",
        MARTIN: "This approach uses {frameworks} patterns, adapted through my evolutionary architecture experience.",
    }


@dataclass
class SystemConstants:
    """Core system configuration constants"""

    # Performance Thresholds
    CONTEXT_RETRIEVAL_TIMEOUT_MS = 200
    ML_PREDICTION_TIMEOUT_S = 5
    TRANSPARENCY_OVERHEAD_MS = 50
    P0_TEST_TIMEOUT_S = 30

    # Quality Thresholds
    MIN_CONVERSATION_QUALITY = 0.7
    ML_ACCURACY_THRESHOLD = 0.85
    FRAMEWORK_DETECTION_CONFIDENCE = 0.87

    # System Messages
    P0_ENFORCEMENT_HEADER = "🛡️ MANDATORY P0 TEST ENFORCEMENT SYSTEM"
    ZERO_TOLERANCE_MESSAGE = "Zero tolerance for P0 feature regressions"
    BLOCKING_TESTS_HEADER = "🚨 BLOCKING P0 FEATURES (MUST PASS):"
    HIGH_PRIORITY_HEADER = "🔺 HIGH PRIORITY P0 FEATURES:"

    # File Paths
    P0_TEST_DEFINITIONS = (
        ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml"
    )
    USER_CONFIG_TEMPLATE = ".claudedirector/config/user_identity.yaml.template"
    USER_CONFIG_FILE = ".claudedirector/config/user_identity.yaml"
    STRATEGIC_MEMORY_DB = "data/strategic/strategic_memory.db"

    # Architectural Validation
    ARCHITECTURAL_PRINCIPLES = [
        "Single Source of Truth",
        "Context Engineering First",
        "P0 Test Protection",
        "User/System Separation",
        "Documentation Requirements",
    ]


@dataclass
class MLConstants:
    """Machine Learning and AI constants"""

    # Model Configuration
    DEFAULT_RANDOM_STATE = 42
    MIN_TRAINING_SAMPLES = 10
    TEST_SIZE = 0.2
    MIN_ACCURACY_THRESHOLD = 0.85
    CONFIDENCE_THRESHOLD = 0.7

    # Feature Categories
    COMMUNICATION_FEATURES = "communication_features"
    TEMPORAL_FEATURES = "temporal_features"
    NETWORK_FEATURES = "network_features"
    CONTEXTUAL_FEATURES = "contextual_features"

    # Model Types
    DECISION_TREE = "decision_tree"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    NEURAL_NETWORK = "neural_network"

    # Prediction Categories
    COLLABORATION_SUCCESS = "collaboration_success"
    TEAM_COORDINATION = "team_coordination"
    STRATEGIC_ALIGNMENT = "strategic_alignment"


@dataclass
class TransparencyConstants:
    """AI transparency and disclosure constants"""

    # MCP Server Disclosure Templates
    MCP_SEQUENTIAL_DISCLOSURE = (
        "🔧 Accessing MCP Server: sequential (systematic_analysis)"
    )
    MCP_CONTEXT7_DISCLOSURE = "🔧 Accessing MCP Server: context7 (pattern_access)"
    MCP_MAGIC_DISCLOSURE = "🔧 Accessing MCP Server: magic (diagram_generation)"

    # Framework Attribution Templates
    FRAMEWORK_DETECTED_TEMPLATE = "📚 Strategic Framework: {framework_name} detected"
    FRAMEWORK_ATTRIBUTION_HEADER = "📚 Strategic Framework:"

    # Processing Messages
    ANALYZING_MESSAGE = "*Analyzing your challenge using systematic frameworks...*"
    PROCESSING_STRATEGIC_REQUEST = (
        "*Processing strategic request with enhanced AI capabilities...*"
    )
    APPLYING_FRAMEWORKS = (
        "*Applying proven strategic methodologies to your situation...*"
    )

    # Transparency Headers
    PERSONA_DISCLOSURE_TEMPLATE = "🎯 {persona_name} | {persona_domain}"
    MCP_ENHANCEMENT_TEMPLATE = "🔧 Accessing MCP Server: {server_name} ({capability})"


class ConfigurationManager:
    """Centralized configuration management with type safety"""

    def __init__(self):
        self.framework = FrameworkConstants()
        self.persona = PersonaConstants()
        self.system = SystemConstants()
        self.ml = MLConstants()
        self.transparency = TransparencyConstants()

    def get_framework_name(self, framework_key: str) -> str:
        """Get standardized framework name"""
        return getattr(self.framework, framework_key, framework_key)

    def get_persona_template(self, persona_name: str) -> str:
        """Get persona attribution template"""
        return self.persona.ATTRIBUTION_TEMPLATES.get(
            persona_name, "This analysis applies {frameworks} methodology."
        )

    def get_system_threshold(self, threshold_name: str) -> float:
        """Get system performance threshold"""
        return getattr(self.system, threshold_name, 0.0)

    def get_ml_config(self, config_name: str) -> Any:
        """Get ML configuration value"""
        return getattr(self.ml, config_name, None)

    def get_transparency_template(self, template_name: str) -> str:
        """Get transparency disclosure template"""
        return getattr(self.transparency, template_name, "")


# Global configuration instance
CONFIG = ConfigurationManager()

# Convenience accessors for common patterns
FRAMEWORKS = CONFIG.framework
PERSONAS = CONFIG.persona
SYSTEM = CONFIG.system
ML_CONFIG = CONFIG.ml
TRANSPARENCY = CONFIG.transparency
