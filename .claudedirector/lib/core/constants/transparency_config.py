"""
Configuration constants for transparency module.

This file centralizes hard-coded values to improve maintainability
and adherence to SOLID principles (DRY principle).
"""

# Framework Detection Thresholds
STRATEGIC_KEYWORD_THRESHOLD = 0.3
DEFAULT_CONFIDENCE_SCORE = 0.0

# Validation Test Constants
TEST_ANALYSIS_DURATION = 0.15
TEST_PROCESSING_TIME = 0.05
TEST_RESPONSE_TIME = 0.1
TEST_LATENCY_THRESHOLD = 0.01
TEST_FRAMEWORK_SCORES = {
    "team_topologies": 0.15,
    "good_strategy": 0.08,
    "wrap_framework": 0.12,
}
TEST_PERFORMANCE_THRESHOLD = 0.5

# Domain Keywords
STAKEHOLDER_ANALYSIS_DOMAIN = "stakeholder_analysis"
TECHNICAL_DOMAIN = "technical"
STRATEGIC_DOMAIN = "strategic"
