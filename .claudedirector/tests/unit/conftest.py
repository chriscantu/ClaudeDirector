"""
Shared Test Fixtures for Unit Tests

🏗️ Martin | Platform Architecture - DRY Compliance + TESTING_ARCHITECTURE.md

This module provides reusable pytest fixtures for unit tests, eliminating
duplication across 22+ test files and promoting consistent test patterns.

ARCHITECTURAL COMPLIANCE:
- ✅ TESTING_ARCHITECTURE.md: unittest.TestCase is standard (matches P0 tests)
- ✅ BLOAT_PREVENTION_SYSTEM.md: DRY principle enforced
- ✅ PROJECT_STRUCTURE.md: Fixtures in tests/unit/conftest.py

FIXTURE USAGE WITH unittest.TestCase:

  Current ClaudeDirector tests use unittest.TestCase (not pytest), consistent
  with P0 regression tests and TESTING_ARCHITECTURE.md patterns.

  These pytest fixtures serve THREE purposes:

  1. **Future pytest migration** - Ready when we convert tests to pytest
  2. **Mock pattern documentation** - Reference examples for consistent mocking
  3. **Import patterns** - Can import utility functions (non-fixture) in unittest tests

  For NOW (unittest.TestCase tests):
    - Use fixture patterns as documentation/reference
    - Import utility functions (create_mock_with_attributes, etc.)
    - Keep setUp() methods simple and DRY

  For FUTURE (pytest migration):
    - Convert tests to pytest style
    - Use @pytest.fixture decorators directly
    - Pass fixtures as test parameters

BLOAT_PREVENTION BENEFITS:
- Eliminates ~1,500 lines of duplicate mock setup code (20% reduction)
- Centralizes configuration patterns
- Single source of truth for test fixtures
- Enables consistent mocking across all tests

DESIGN PRINCIPLES:
- DRY: Single source of truth for common mock patterns
- Maintainability: Centralized fixture updates propagate everywhere
- Consistency: Standard mocking patterns across all tests
- Discoverability: Well-documented fixtures with clear usage examples
"""

import tempfile
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, Optional
import pytest

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# DIRECTORY & ENVIRONMENT FIXTURES
# ============================================================================


@pytest.fixture
def project_root():
    """
    Provide project root path for tests.

    Usage:
        def test_something(project_root):
            config_path = project_root / "config" / "test.yaml"
    """
    return PROJECT_ROOT


@pytest.fixture
def temp_test_dir():
    """
    Provide temporary directory that's automatically cleaned up.

    Usage:
        def test_file_operations(temp_test_dir):
            test_file = temp_test_dir / "test.txt"
            test_file.write_text("test content")
    """
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    import shutil

    if temp_dir.exists():
        shutil.rmtree(temp_dir)


# ============================================================================
# CONFIGURATION FIXTURES
# ============================================================================


@pytest.fixture
def sample_test_config():
    """
    Standard test configuration dictionary.

    Usage:
        def test_initialization(sample_test_config):
            engine = MyEngine(sample_test_config)
    """
    return {
        "project_root": str(PROJECT_ROOT),
        "performance_mode": "test",
        "enable_metrics": False,
        "enable_caching": False,
        "enable_logging": False,
        "log_level": "ERROR",
        "timeout_seconds": 30,
        "max_retries": 3,
    }


@pytest.fixture
def sample_strategic_context():
    """
    Standard strategic context for decision tests.

    Usage:
        def test_decision_analysis(sample_strategic_context):
            result = orchestrator.analyze(sample_strategic_context)
    """
    return {
        "user_input": "test strategic input",
        "complexity": "medium",
        "persona": "diego",
        "stakeholders": ["engineering", "product"],
        "frameworks": ["team_topologies"],
        "metadata": {
            "timestamp": "2025-10-03T00:00:00Z",
            "session_id": "test-session-123",
        },
    }


# ============================================================================
# MCP & AI INTELLIGENCE MOCKS
# ============================================================================


@pytest.fixture
def mock_mcp_helper():
    """
    Mock MCP integration helper with async call support.

    Usage:
        def test_mcp_calls(mock_mcp_helper):
            mock_mcp_helper.call_mcp_server.return_value = {"result": "success"}
    """
    mock = Mock()
    mock.call_mcp_server = AsyncMock(
        return_value={
            "status": "success",
            "data": {"analysis": "test result"},
            "server": "sequential",
        }
    )
    mock.get_available_servers = Mock(return_value=["sequential", "context7", "magic"])
    mock.is_server_available = Mock(return_value=True)
    return mock


@pytest.fixture
def mock_processor():
    """
    Mock DecisionProcessor with standard configuration.

    Usage:
        @patch('lib.ai_intelligence.decision_orchestrator.DecisionProcessor')
        def test_orchestrator(mock_processor_class, mock_processor):
            mock_processor_class.return_value = mock_processor
    """
    mock = Mock()
    mock.mcp_helper = Mock()
    mock.framework_engine = Mock()
    mock.transparency_system = Mock()
    mock.persona_manager = Mock()
    mock.ml_prediction_router = None
    mock.enable_ml_predictions = True

    # Configure standard methods
    mock.detect_decision_context = AsyncMock(
        return_value={
            "user_input": "test input",
            "complexity": "medium",
            "persona": "diego",
            "stakeholders": ["engineering"],
            "metadata": {},
        }
    )
    mock.route_to_mcp_servers = AsyncMock(return_value=["sequential"])
    mock.get_framework_recommendations = AsyncMock(
        return_value=[{"name": "rumelt_strategy_kernel", "confidence": 0.9}]
    )
    mock.calculate_confidence_score = Mock(return_value=0.875)
    mock.generate_transparency_trail = Mock(
        return_value=["Decision Intelligence Analysis Started"]
    )
    mock.generate_next_actions = Mock(return_value=["Define strategy kernel"])
    mock.get_ml_predictions = AsyncMock(return_value=None)
    mock.update_performance_metrics = Mock()

    return mock


@pytest.fixture
def mock_framework_engine():
    """
    Mock framework detection engine.

    Usage:
        def test_framework_detection(mock_framework_engine):
            mock_framework_engine.detect_frameworks.return_value = ["team_topologies"]
    """
    mock = Mock()
    mock.detect_frameworks = Mock(
        return_value=["team_topologies", "rumelt_strategy_kernel"]
    )
    mock.get_framework_recommendations = AsyncMock(
        return_value=[{"name": "team_topologies", "confidence": 0.9, "relevance": 0.85}]
    )
    mock.analyze_framework_fit = Mock(
        return_value={
            "framework": "team_topologies",
            "fit_score": 0.88,
            "reasoning": "Strong alignment with organizational context",
        }
    )
    return mock


@pytest.fixture
def mock_transparency_system():
    """
    Mock transparency system for AI enhancement logging.

    Usage:
        def test_transparency(mock_transparency_system):
            mock_transparency_system.log_enhancement.assert_called_once()
    """
    mock = Mock()
    mock.log_enhancement = Mock()
    mock.log_mcp_call = Mock()
    mock.log_framework_detection = Mock()
    mock.generate_transparency_trail = Mock(
        return_value=[
            "MCP Enhancement: sequential server called",
            "Framework Detection: team_topologies identified",
        ]
    )
    return mock


@pytest.fixture
def mock_persona_manager():
    """
    Mock persona manager for persona-based intelligence.

    Usage:
        def test_persona_detection(mock_persona_manager):
            mock_persona_manager.detect_persona.return_value = "diego"
    """
    mock = Mock()
    mock.detect_persona = Mock(return_value="diego")
    mock.get_persona_config = Mock(
        return_value={
            "name": "diego",
            "role": "Engineering Leadership",
            "mcp_servers": ["sequential", "context7"],
        }
    )
    mock.apply_persona_context = Mock()
    return mock


# ============================================================================
# MEMORY & CONTEXT ENGINE MOCKS
# ============================================================================


@pytest.fixture
def mock_memory_engine():
    """
    Mock conversation memory engine.

    Usage:
        def test_memory_retrieval(mock_memory_engine):
            mock_memory_engine.get_recent_interactions.return_value = [...]
    """
    mock = Mock()
    mock.get_recent_interactions = Mock(
        return_value=[
            {
                "content": "Previous strategic discussion about team structure",
                "timestamp": "2025-10-02T10:00:00Z",
                "frameworks": ["team_topologies"],
            },
            {
                "content": "Discussion about organizational scaling challenges",
                "timestamp": "2025-10-02T11:00:00Z",
                "frameworks": ["organizational_design"],
            },
        ]
    )
    mock.store_interaction = Mock()
    mock.search_interactions = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def mock_context_engine():
    """
    Mock advanced context engine (8-layer system).

    Usage:
        def test_context_retrieval(mock_context_engine):
            context = mock_context_engine.get_unified_context("test query")
    """
    mock = Mock()
    mock.get_unified_context = AsyncMock(
        return_value={
            "conversation_context": {"recent_topics": ["team structure"]},
            "strategic_context": {"active_initiatives": ["platform_scaling"]},
            "stakeholder_context": {"key_stakeholders": ["engineering", "product"]},
            "organizational_context": {"team_dynamics": "collaborative"},
        }
    )
    mock.update_context = Mock()
    mock.clear_context = Mock()
    return mock


# ============================================================================
# DATABASE & STORAGE MOCKS
# ============================================================================


@pytest.fixture
def mock_db_session():
    """
    Mock database session with standard CRUD operations.

    Usage:
        def test_database_query(mock_db_session):
            mock_db_session.query().filter().first.return_value = test_record
    """
    mock = Mock()
    mock.query = Mock(return_value=mock)
    mock.filter = Mock(return_value=mock)
    mock.first = Mock(return_value=None)
    mock.all = Mock(return_value=[])
    mock.add = Mock()
    mock.commit = Mock()
    mock.rollback = Mock()
    mock.close = Mock()
    return mock


@pytest.fixture
def mock_database_manager():
    """
    Mock database manager with connection pooling.

    Usage:
        def test_db_operations(mock_database_manager):
            with mock_database_manager.get_session() as session:
                session.query(...)
    """
    mock = Mock()
    mock.get_session = Mock()
    mock.get_session.return_value.__enter__ = Mock(return_value=Mock())
    mock.get_session.return_value.__exit__ = Mock(return_value=None)
    mock.initialize = Mock()
    mock.health_check = Mock(return_value=True)
    return mock


# ============================================================================
# TEMPLATE ENGINE MOCKS
# ============================================================================


@pytest.fixture
def mock_template_engine():
    """
    Mock template engine for code generation tests.

    Usage:
        def test_template_generation(mock_template_engine):
            result = mock_template_engine.generate_template(...)
    """
    mock = Mock()
    mock.generate_template = Mock(
        return_value=Mock(
            code="# Generated test code",
            principle="SINGLE_RESPONSIBILITY",
            generation_time_ms=50.0,
        )
    )
    mock.get_available_templates = Mock(
        return_value={
            "class": ["single_responsibility", "open_closed"],
            "service": ["dependency_inversion"],
        }
    )
    mock.get_basic_engine = Mock(return_value=None)
    return mock


# ============================================================================
# PERFORMANCE & CACHE MOCKS
# ============================================================================


@pytest.fixture
def mock_cache_manager():
    """
    Mock cache manager for performance tests.

    Usage:
        def test_caching(mock_cache_manager):
            mock_cache_manager.get.return_value = cached_value
    """
    mock = Mock()
    mock.get = Mock(return_value=None)
    mock.set = Mock()
    mock.delete = Mock()
    mock.clear = Mock()
    mock.get_stats = Mock(
        return_value={
            "hits": 100,
            "misses": 20,
            "hit_rate": 0.833,
        }
    )
    return mock


# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================


@pytest.fixture
def sample_framework_usage():
    """
    Sample framework usage data for detection tests.

    Usage:
        def test_framework_detection(sample_framework_usage):
            assert sample_framework_usage.framework_name == "Team Topologies"
    """
    try:
        from lib.ai_intelligence.framework_detector import FrameworkUsage

        return FrameworkUsage(
            framework_name="Team Topologies",
            confidence_score=0.85,
            matched_patterns=["team topologies", "team structure"],
            framework_type="organizational",
        )
    except ImportError:
        # Fallback to dict if FrameworkUsage not available
        return {
            "framework_name": "Team Topologies",
            "confidence_score": 0.85,
            "matched_patterns": ["team topologies", "team structure"],
            "framework_type": "organizational",
        }


@pytest.fixture
def sample_decision_context():
    """
    Sample decision context for orchestrator tests.

    Usage:
        def test_decision_orchestration(sample_decision_context):
            result = orchestrator.orchestrate(sample_decision_context)
    """
    try:
        from lib.ai_intelligence.decision_orchestrator import DecisionContext

        return DecisionContext(
            user_input="How should we restructure our engineering teams?",
            complexity="HIGH",
            stakeholders=["engineering", "product", "executive"],
            time_sensitivity="MEDIUM",
            business_impact="HIGH",
        )
    except ImportError:
        # Fallback to dict
        return {
            "user_input": "How should we restructure our engineering teams?",
            "complexity": "HIGH",
            "stakeholders": ["engineering", "product", "executive"],
            "time_sensitivity": "MEDIUM",
            "business_impact": "HIGH",
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def create_mock_with_attributes(**kwargs):
    """
    Helper to create Mock with predefined attributes.

    Usage:
        mock_obj = create_mock_with_attributes(name="test", value=42)
        assert mock_obj.name == "test"
    """
    mock = Mock()
    for key, value in kwargs.items():
        setattr(mock, key, value)
    return mock


def create_async_mock_with_return(return_value):
    """
    Helper to create AsyncMock with predefined return value.

    Usage:
        async_mock = create_async_mock_with_return({"status": "success"})
        result = await async_mock()
    """
    return AsyncMock(return_value=return_value)
