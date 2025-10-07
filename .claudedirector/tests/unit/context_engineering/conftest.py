"""
Context Engineering Component-Specific Test Fixtures

🏗️ Martin | Platform Architecture - Context Engineering Test Support

Fixtures specific to context engineering components (8-layer context system,
memory management, stakeholder intelligence).

EXTENDS: .claudedirector/tests/unit/conftest.py (root fixtures)
SCOPE: Context engineering component testing
"""

import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, List
from datetime import datetime, timedelta


# ============================================================================
# CONTEXT LAYER FIXTURES
# ============================================================================


@pytest.fixture
def mock_conversation_layer():
    """
    Mock conversation memory layer (Layer 1).
    """
    mock = Mock()

    # Conversation retrieval
    mock.get_recent_conversations = Mock(
        return_value=[
            {
                "id": "conv-1",
                "content": "Discussion about team structure",
                "timestamp": datetime.now().isoformat(),
                "topics": ["team_structure", "organizational_design"],
            }
        ]
    )

    # Semantic search
    mock.search_conversations = AsyncMock(
        return_value=[{"content": "Previous strategic discussion", "relevance": 0.92}]
    )

    # Storage
    mock.store_conversation = Mock()

    return mock


@pytest.fixture
def mock_strategic_layer():
    """
    Mock strategic memory layer (Layer 2).
    """
    mock = Mock()

    # Strategic context retrieval
    mock.get_strategic_context = Mock(
        return_value={
            "active_initiatives": [
                {
                    "name": "Platform Scaling",
                    "priority": "HIGH",
                    "status": "IN_PROGRESS",
                }
            ],
            "strategic_goals": [
                {"goal": "Improve platform velocity", "target_date": "2025-12-31"}
            ],
            "recent_decisions": [
                {"decision": "Adopt Team Topologies", "date": "2025-09-15"}
            ],
        }
    )

    # Update strategic context
    mock.update_strategic_context = Mock()

    return mock


@pytest.fixture
def mock_stakeholder_layer():
    """
    Mock stakeholder intelligence layer (Layer 3).
    """
    mock = Mock()

    # Stakeholder information
    mock.get_stakeholder_info = Mock(
        return_value={
            "name": "John Doe",
            "role": "VP Engineering",
            "department": "engineering",
            "communication_style": "direct",
            "strategic_priorities": ["velocity", "quality"],
        }
    )

    # Stakeholder network
    mock.get_stakeholder_network = Mock(
        return_value={
            "direct_reports": ["Alice", "Bob"],
            "key_partners": ["Product VP", "CTO"],
            "influence_score": 0.92,
        }
    )

    return mock


# ============================================================================
# INTELLIGENCE ENGINE FIXTURES
# ============================================================================


@pytest.fixture
def mock_advanced_context_engine():
    """
    Mock 8-layer advanced context engine.
    """
    mock = Mock()

    # Unified context retrieval
    mock.get_unified_context = AsyncMock(
        return_value={
            "conversation_context": {
                "recent_topics": ["team_structure", "platform_scaling"],
                "conversation_count": 15,
            },
            "strategic_context": {
                "active_initiatives": ["Platform Scaling"],
                "strategic_goals": ["Improve velocity"],
            },
            "stakeholder_context": {
                "key_stakeholders": ["VP Engineering", "CTO"],
                "recent_interactions": 23,
            },
            "organizational_context": {
                "team_size": 50,
                "growth_rate": 0.15,
                "team_dynamics": "collaborative",
            },
            "unified_score": 0.88,
        }
    )

    # Context updates
    mock.update_context = Mock()
    mock.clear_context = Mock()

    return mock


# ============================================================================
# ANALYTICS & INTELLIGENCE FIXTURES
# ============================================================================


@pytest.fixture
def mock_analytics_engine():
    """
    Mock analytics engine for context insights.
    """
    mock = Mock()

    # Performance analytics
    mock.analyze_performance = Mock(
        return_value={
            "metrics": {
                "context_retrieval_time_ms": 45.0,
                "context_relevance_score": 0.88,
                "cache_hit_rate": 0.75,
            },
            "insights": [
                "Context retrieval performing well",
                "High relevance scores indicate good context quality",
            ],
        }
    )

    # Trend analysis
    mock.analyze_trends = Mock(
        return_value={
            "trends": [
                {
                    "topic": "platform_scaling",
                    "frequency": 15,
                    "trend": "increasing",
                    "confidence": 0.85,
                }
            ],
        }
    )

    return mock


@pytest.fixture
def mock_organizational_learning_engine():
    """
    Mock organizational learning engine (Layer 5).
    """
    mock = Mock()

    # Learning patterns
    mock.identify_learning_patterns = Mock(
        return_value={
            "patterns": [
                {
                    "pattern": "team_topologies_application",
                    "frequency": 8,
                    "success_rate": 0.875,
                    "insights": ["Effective for organizational scaling"],
                }
            ],
        }
    )

    # Knowledge consolidation
    mock.consolidate_knowledge = Mock(
        return_value={
            "consolidated_insights": [
                "Team Topologies effective for our org",
                "Platform teams reduce cognitive load",
            ],
            "confidence": 0.88,
        }
    )

    return mock


# ============================================================================
# WORKSPACE INTEGRATION FIXTURES
# ============================================================================


@pytest.fixture
def mock_workspace_integration():
    """
    Mock workspace integration for file monitoring.
    """
    mock = Mock()

    # File monitoring
    mock.monitor_workspace = Mock(
        return_value={
            "files_monitored": 45,
            "recent_changes": [
                {
                    "file": "current-initiatives/platform-scaling.md",
                    "change_type": "modified",
                    "timestamp": datetime.now().isoformat(),
                }
            ],
        }
    )

    # Context extraction from files
    mock.extract_context_from_file = Mock(
        return_value={
            "topics": ["platform_scaling", "team_structure"],
            "stakeholders_mentioned": ["VP Engineering", "CTO"],
            "strategic_themes": ["velocity", "scalability"],
        }
    )

    return mock


# ============================================================================
# SAMPLE CONTEXT DATA
# ============================================================================


@pytest.fixture
def sample_conversation_context():
    """
    Sample conversation context for testing.
    """
    return {
        "id": "conv-test-123",
        "user_input": "How should we scale our engineering organization?",
        "timestamp": datetime.now().isoformat(),
        "topics": ["organizational_scaling", "team_structure"],
        "sentiment": "analytical",
        "complexity": "HIGH",
    }


@pytest.fixture
def sample_stakeholder_data():
    """
    Sample stakeholder data for intelligence tests.
    """
    return {
        "stakeholder_id": "stakeholder-123",
        "name": "Jane Smith",
        "role": "VP Engineering",
        "department": "engineering",
        "email": "jane.smith@example.com",
        "communication_preferences": {
            "style": "data-driven",
            "frequency": "weekly",
            "format": "executive_brief",
        },
        "strategic_priorities": [
            {"priority": "platform_velocity", "importance": 0.95},
            {"priority": "team_scalability", "importance": 0.90},
        ],
        "decision_authority": ["engineering", "platform", "architecture"],
        "recent_interactions": [
            {
                "date": (datetime.now() - timedelta(days=2)).isoformat(),
                "topic": "Q4 platform strategy",
                "outcome": "approved_platform_investment",
            }
        ],
    }


@pytest.fixture
def sample_unified_context():
    """
    Sample unified context from all 8 layers.
    """
    return {
        "conversation_context": {
            "recent_topics": ["platform_scaling", "team_structure"],
            "active_discussion": "organizational_design",
        },
        "strategic_context": {
            "active_initiatives": ["Platform Scaling Initiative"],
            "strategic_goals": ["Improve platform velocity", "Scale team to 100"],
        },
        "stakeholder_context": {
            "primary_stakeholder": "VP Engineering",
            "key_stakeholders": ["CTO", "Product VP"],
        },
        "learning_context": {
            "successful_patterns": ["team_topologies"],
            "lessons_learned": ["Platform teams reduce cognitive load"],
        },
        "organizational_context": {
            "current_team_size": 50,
            "target_team_size": 100,
            "team_dynamics": "collaborative",
        },
        "team_dynamics_context": {
            "collaboration_score": 0.85,
            "velocity_trend": "increasing",
        },
        "realtime_context": {
            "active_incidents": 0,
            "system_health": "healthy",
        },
        "ml_pattern_context": {
            "detected_patterns": ["scaling_challenge", "platform_investment_needed"],
            "confidence": 0.88,
        },
    }


# ============================================================================
# CONFIGURATION FIXTURES (Phase 6: Fix Category C Errors)
# ============================================================================


@pytest.fixture
def mock_config():
    """
    Mock ClaudeDirectorConfig for context engineering tests.

    Provides a mock configuration object compatible with the current
    ClaudeDirectorConfig API (no database_path in __init__).

    Phase 6 Fix: Tests were using outdated `database_path` parameter.
    Current API uses `config_file` parameter only.
    """
    mock = Mock()

    # Current ClaudeDirectorConfig API - config_file parameter
    mock.config_file = None

    # Database path as property (not __init__ parameter)
    mock.database_path = None

    # Common config properties
    mock.thresholds = Mock()
    mock.enums = Mock()
    mock.security = Mock()
    mock.messages = Mock()
    mock.paths = Mock()

    # Backwards compatibility for dict-like access
    mock.get = Mock(return_value=None)

    return mock


@pytest.fixture
def temp_db(tmp_path):
    """
    Temporary database path for testing.

    Creates a temporary database file path for tests that need
    database isolation.

    Phase 6 Fix: Provides database path as property, not __init__ parameter.
    """
    db_path = tmp_path / "test_strategic_memory.db"
    return str(db_path)


@pytest.fixture
def sample_meeting_content():
    """
    Sample meeting content for meeting intelligence tests.
    """
    return """
    # Weekly 1:1 with VP Engineering

    ## Participants
    - Sarah Chen (VP Engineering)
    - John Smith (Engineering Director)

    ## Agenda
    1. Platform scaling strategy
    2. Team structure optimization
    3. Q4 resource planning

    ## Action Items
    - [ ] Sarah: Review platform architecture proposal by Friday
    - [ ] John: Present team topology recommendation next week
    - [ ] Sarah: Schedule follow-up on budget allocation

    ## Stakeholders Mentioned
    - Alice Johnson (Product VP)
    - Bob Williams (CTO)
    """
