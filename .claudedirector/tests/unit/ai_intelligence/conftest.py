"""
AI Intelligence Component-Specific Test Fixtures

🏗️ Martin | Platform Architecture - AI Intelligence Test Support

Fixtures specific to AI intelligence components (decision orchestration,
framework detection, MCP coordination).

EXTENDS: .claudedirector/tests/unit/conftest.py (root fixtures)
SCOPE: AI intelligence component testing
"""

import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, List


# ============================================================================
# DECISION ORCHESTRATION FIXTURES
# ============================================================================


@pytest.fixture
def mock_decision_processor():
    """
    Specialized mock for DecisionProcessor (UnifiedAIEngine alias).

    Configured for ultra-lightweight facade pattern testing.
    """
    mock = Mock()

    # Standard dependencies
    mock.mcp_helper = Mock()
    mock.framework_engine = Mock()
    mock.transparency_system = Mock()
    mock.persona_manager = Mock()
    mock.ml_prediction_router = None
    mock.enable_ml_predictions = True

    # Decision detection
    mock.detect_decision_context = AsyncMock(
        return_value={
            "user_input": "test strategic decision",
            "complexity": "HIGH",
            "persona": "diego",
            "stakeholders": ["engineering", "executive"],
            "time_sensitivity": "MEDIUM",
            "business_impact": "HIGH",
            "metadata": {},
        }
    )

    # MCP routing
    mock.route_to_mcp_servers = AsyncMock(return_value=["sequential", "context7"])

    # Framework recommendations
    mock.get_framework_recommendations = AsyncMock(
        return_value=[
            {"name": "rumelt_strategy_kernel", "confidence": 0.92, "relevance": 0.88},
            {"name": "team_topologies", "confidence": 0.85, "relevance": 0.82},
        ]
    )

    # Scoring & metrics
    mock.calculate_confidence_score = Mock(return_value=0.875)
    mock.update_performance_metrics = Mock()

    # Transparency
    mock.generate_transparency_trail = Mock(
        return_value=[
            "Decision Intelligence Analysis Started",
            "MCP Sequential Server: Strategic analysis requested",
            "Framework Detection: 2 frameworks identified",
            "Confidence Score: 87.5%",
        ]
    )

    # Action generation
    mock.generate_next_actions = Mock(
        return_value=[
            "Define strategy kernel with clear diagnosis",
            "Apply Team Topologies principles to team structure",
            "Coordinate with stakeholders on implementation timeline",
        ]
    )

    # ML predictions (optional)
    mock.get_ml_predictions = AsyncMock(return_value=None)

    return mock


# ============================================================================
# FRAMEWORK DETECTION FIXTURES
# ============================================================================


@pytest.fixture
def mock_baseline_detector():
    """
    Mock baseline framework detector (FrameworkDetectionMiddleware).
    """
    mock = Mock()

    # Standard framework detection
    mock.detect_frameworks_used = Mock(
        return_value=[
            Mock(
                framework_name="Team Topologies",
                confidence_score=0.85,
                matched_patterns=[
                    "team topologies",
                    "team structure",
                    "cognitive load",
                ],
                framework_type="organizational",
            ),
            Mock(
                framework_name="Good Strategy Bad Strategy",
                confidence_score=0.78,
                matched_patterns=["strategy kernel", "coherent actions"],
                framework_type="strategic",
            ),
        ]
    )

    # Framework library access
    mock.get_available_frameworks = Mock(
        return_value=[
            "team_topologies",
            "rumelt_strategy_kernel",
            "crucial_conversations",
            "accelerate_performance",
        ]
    )

    return mock


@pytest.fixture
def mock_mcp_enhanced_framework_engine():
    """
    Mock MCP-enhanced framework engine for advanced detection.
    """
    mock = Mock()

    # Enhanced detection with context awareness
    mock.detect_frameworks_with_context = AsyncMock(
        return_value={
            "frameworks": [
                {
                    "name": "Team Topologies",
                    "confidence": 0.92,
                    "context_relevance": 0.88,
                    "business_impact": "HIGH",
                    "application_guidance": "Stream-aligned teams recommended",
                }
            ],
            "contextual_insights": [
                "Organizational scaling patterns detected",
                "Cross-functional coordination challenges identified",
            ],
            "mcp_enhancements_applied": ["sequential", "context7"],
        }
    )

    # Proactive suggestions
    mock.suggest_frameworks = AsyncMock(
        return_value=[
            {
                "framework": "capital_allocation",
                "relevance_score": 0.87,
                "reason": "Platform investment decision context detected",
            }
        ]
    )

    return mock


# ============================================================================
# MCP PIPELINE FIXTURES
# ============================================================================


@pytest.fixture
def mock_mcp_pipeline():
    """
    Mock MCP enhanced decision pipeline.
    """
    mock = Mock()

    # Pipeline execution
    mock.execute_pipeline = AsyncMock(
        return_value={
            "status": "success",
            "stages_completed": ["detection", "analysis", "recommendation"],
            "parallel_servers": ["sequential", "context7"],
            "execution_time_ms": 450.0,
            "results": {
                "strategic_analysis": "Comprehensive analysis complete",
                "framework_recommendations": [
                    "team_topologies",
                    "rumelt_strategy_kernel",
                ],
                "confidence_score": 0.88,
            },
        }
    )

    # Stage-specific execution
    mock.execute_stage = AsyncMock(
        return_value={
            "stage": "analysis",
            "status": "success",
            "duration_ms": 150.0,
            "data": {"insights": ["Strategic insight 1", "Strategic insight 2"]},
        }
    )

    # Health check
    mock.health_check = AsyncMock(
        return_value={
            "status": "healthy",
            "servers_available": ["sequential", "context7", "magic"],
            "average_latency_ms": 120.0,
        }
    )

    return mock


# ============================================================================
# SAMPLE AI INTELLIGENCE DATA
# ============================================================================


@pytest.fixture
def sample_complex_decision():
    """
    Sample complex strategic decision for testing.
    """
    return {
        "user_input": (
            "How should we restructure our engineering organization to support "
            "both product velocity and platform investment? We have 5 teams, "
            "limited budget, and executive pressure for faster delivery."
        ),
        "complexity": "VERY_HIGH",
        "stakeholders": ["engineering", "product", "executive", "finance"],
        "time_sensitivity": "HIGH",
        "business_impact": "CRITICAL",
        "frameworks_likely": [
            "team_topologies",
            "capital_allocation",
            "organizational_design",
        ],
        "expected_mcp_servers": ["sequential", "context7"],
    }


@pytest.fixture
def sample_framework_detection_result():
    """
    Sample framework detection result with high confidence.
    """
    return {
        "frameworks_detected": [
            {
                "name": "Team Topologies",
                "confidence": 0.92,
                "matched_patterns": [
                    "stream-aligned teams",
                    "cognitive load",
                    "platform team",
                ],
                "application_context": "organizational_structure",
                "business_impact": "HIGH",
            },
            {
                "name": "Rumelt Strategy Kernel",
                "confidence": 0.88,
                "matched_patterns": [
                    "diagnosis",
                    "guiding policy",
                    "coherent actions",
                ],
                "application_context": "strategic_planning",
                "business_impact": "CRITICAL",
            },
        ],
        "contextual_insights": [
            "Organizational scaling challenges detected",
            "Platform vs product trade-off analysis needed",
            "Executive stakeholder alignment critical",
        ],
        "recommended_next_steps": [
            "Apply Team Topologies assessment to current structure",
            "Develop strategy kernel with clear diagnosis",
            "Coordinate with executive stakeholders on priorities",
        ],
    }
