"""
Core Component-Specific Test Fixtures

🏗️ Martin | Platform Architecture - Core Component Test Support

Fixtures specific to core components (database, models, validation,
generation engines).

EXTENDS: .claudedirector/tests/unit/conftest.py (root fixtures)
SCOPE: Core component testing
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from typing import Dict, Any, List


# ============================================================================
# GENERATION ENGINE FIXTURES
# ============================================================================


@pytest.fixture
def mock_basic_solid_engine():
    """
    Mock BasicSOLIDTemplateEngine (shared foundation).
    """
    mock = Mock()

    # Basic template generation
    mock.generate_basic_template = Mock(
        return_value={
            "code": "# Generated SOLID template",
            "principle": "SINGLE_RESPONSIBILITY",
            "generation_time_ms": 35.0,
        }
    )

    # Template availability
    mock.get_basic_templates = Mock(
        return_value={
            "class": ["single_responsibility"],
            "service": ["dependency_inversion"],
        }
    )

    return mock


@pytest.fixture
def mock_project_structure_parser():
    """
    Mock PROJECT_STRUCTURE.md parser for placement engine tests.
    """
    mock = Mock()

    # Parse PROJECT_STRUCTURE.md
    mock.parse_structure = Mock(
        return_value={
            "directories": {
                "ai_intelligence": {
                    "path": ".claudedirector/lib/ai_intelligence/",
                    "purpose": "AI Enhancement System",
                    "components": [
                        "decision_orchestrator.py",
                        "enhanced_framework_detection.py",
                    ],
                },
                "core": {
                    "path": ".claudedirector/lib/core/",
                    "purpose": "Foundational Components",
                    "subdirectories": {
                        "generation": ".claudedirector/lib/core/generation/",
                    },
                },
                "context_engineering": {
                    "path": ".claudedirector/lib/context_engineering/",
                    "purpose": "8-Layer Context System",
                    "components": [
                        "advanced_context_engine.py",
                        "conversation_layer.py",
                    ],
                },
            },
            "placement_rules": [
                {
                    "component_type": "ai_enhancement",
                    "target_directory": ".claudedirector/lib/ai_intelligence/",
                },
                {
                    "component_type": "core_foundation",
                    "target_directory": ".claudedirector/lib/core/",
                },
            ],
        }
    )

    # Validate placement
    mock.validate_placement = Mock(
        return_value={
            "valid": True,
            "target_directory": ".claudedirector/lib/ai_intelligence/",
            "reasoning": "AI enhancement component matches directory purpose",
        }
    )

    return mock


@pytest.fixture
def sample_component_metadata():
    """
    Sample component metadata for placement tests.
    """
    return {
        "name": "EnhancedDecisionEngine",
        "type": "ai_enhancement",
        "category": "decision_intelligence",
        "dependencies": ["mcp_helper", "framework_engine"],
        "purpose": "Advanced strategic decision orchestration",
        "complexity": "HIGH",
    }


# ============================================================================
# DATABASE & MODEL FIXTURES
# ============================================================================


@pytest.fixture
def sample_database_config():
    """
    Sample database configuration for testing.
    """
    return {
        "database_url": "sqlite:///:memory:",
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "echo": False,
        "enable_logging": False,
    }


@pytest.fixture
def mock_database_engine():
    """
    Mock SQLAlchemy database engine.
    """
    mock = Mock()
    mock.connect = Mock(return_value=Mock())
    mock.execute = Mock()
    mock.dispose = Mock()
    return mock


@pytest.fixture
def mock_session_factory():
    """
    Mock session factory for database tests.
    """
    mock = Mock()
    mock_session = Mock()
    mock_session.query = Mock(return_value=mock_session)
    mock_session.filter = Mock(return_value=mock_session)
    mock_session.first = Mock(return_value=None)
    mock_session.all = Mock(return_value=[])
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.rollback = Mock()
    mock_session.close = Mock()
    mock.return_value = mock_session
    return mock


# ============================================================================
# VALIDATION FIXTURES
# ============================================================================


@pytest.fixture
def mock_validation_engine():
    """
    Mock validation engine for input validation tests.
    """
    mock = Mock()

    # Validation methods
    mock.validate_input = Mock(
        return_value={
            "valid": True,
            "errors": [],
            "sanitized_input": "test input",
        }
    )

    mock.validate_config = Mock(
        return_value={
            "valid": True,
            "errors": [],
            "warnings": [],
        }
    )

    mock.validate_file_path = Mock(
        return_value={
            "valid": True,
            "exists": True,
            "readable": True,
            "absolute_path": "/test/path/file.py",
        }
    )

    return mock


# ============================================================================
# SDK ENHANCEMENT FIXTURES
# ============================================================================


@pytest.fixture
def sample_sdk_error_config():
    """
    Sample SDK error handling configuration.
    """
    return {
        "error_patterns": {
            "rate_limit": {
                "pattern": r"rate.*limit.*exceeded",
                "severity": "HIGH",
                "retry_strategy": "exponential_backoff",
            },
            "authentication": {
                "pattern": r"authentication.*failed",
                "severity": "CRITICAL",
                "retry_strategy": "none",
            },
        },
        "retry_strategies": {
            "exponential_backoff": {
                "base_delay": 1.0,
                "max_delay": 60.0,
                "multiplier": 2.0,
                "max_retries": 5,
            },
        },
        "circuit_breaker": {
            "failure_threshold": 5,
            "success_threshold": 2,
            "timeout_seconds": 60,
        },
    }


@pytest.fixture
def mock_sdk_enhanced_manager():
    """
    Mock SDKEnhancedManager for error handling tests.
    """
    mock = Mock()

    # Error categorization
    mock.categorize_error = Mock(
        return_value={
            "category": "rate_limit",
            "severity": "HIGH",
            "retry_recommended": True,
            "retry_strategy": "exponential_backoff",
        }
    )

    # Retry logic
    mock.execute_with_retry = Mock(
        return_value={
            "status": "success",
            "attempts": 2,
            "total_duration_ms": 150.0,
            "result": {"data": "test result"},
        }
    )

    # Circuit breaker
    mock.check_circuit_breaker = Mock(
        return_value={
            "state": "closed",
            "failure_count": 0,
            "last_failure_time": None,
        }
    )

    return mock
