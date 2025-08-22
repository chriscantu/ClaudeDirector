"""
P0 Features Test Configuration

Berny's testing framework for AI pipeline components.
Ensures backwards compatibility and validates AI enhancements.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import MagicMock, patch

# Import existing ClaudeDirector components to ensure compatibility
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from memory.optimized_db_manager import get_db_manager
from lib.claudedirector.p0_features.shared.ai_pipeline.ai_base import (
    AIModelConfig,
    AIEngineBase,
)
from lib.claudedirector.p0_features.shared.database_manager.db_base import (
    DatabaseConfig,
    QueryContext,
)


@pytest.fixture(scope="session")
def test_database():
    """Create isolated test database for P0 features testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_strategic_memory.db"

        # Initialize with existing ClaudeDirector schema to ensure compatibility
        db_manager = get_db_manager(str(db_path))

        # Ensure backwards compatibility: existing tables should work
        with db_manager.get_connection() as conn:
            # Test existing stakeholder table compatibility
            conn.execute(
                """
                INSERT INTO stakeholder_profiles_enhanced
                (stakeholder_key, display_name, role_title, organization, strategic_importance)
                VALUES ('test_stakeholder', 'Test User', 'Test Role', 'Test Org', 'high')
            """
            )
            conn.commit()

        yield str(db_path)


@pytest.fixture
def ai_model_config():
    """Standard AI model configuration for testing"""
    return AIModelConfig(
        model_name="test_decision_detector",
        accuracy_threshold=0.85,
        max_inference_time_ms=200,
        parameters={"test_mode": True, "mock_predictions": True},
    )


@pytest.fixture
def sample_meeting_content():
    """Sample meeting content for decision detection testing"""
    return {
        "strategic_decision": """
        Meeting Notes: Product Strategy Review
        Date: 2025-01-09

        DECISION POINT: We need to prioritize the mobile app redesign project.

        Discussion:
        - Current mobile app has 60% user satisfaction
        - Competitor apps averaging 85% satisfaction
        - Engineering team estimates 6 months for complete redesign
        - Product team recommends phased approach over 3 months

        DECISION MADE: Proceed with phased mobile redesign approach
        Timeline: Start Q1 2025, complete by end Q1
        Owner: Sarah (Product Director)
        Budget: $150K approved

        Next steps:
        1. Sarah to create detailed project plan by Jan 15
        2. Engineering team to assess technical feasibility
        3. Design team to begin user research phase
        """,
        "no_decision": """
        Weekly Team Standup
        Date: 2025-01-09

        Team updates:
        - Bob finished API integration
        - Alice working on UI components
        - Charlie debugging test suite

        Blockers:
        - Waiting for design assets from external team
        - Database performance needs optimization

        Next week focus:
        - Complete current sprint tasks
        - Plan next sprint priorities
        """,
        "multiple_decisions": """
        Executive Planning Session
        Date: 2025-01-09

        DECISION 1: Platform Architecture
        We will migrate from monolith to microservices architecture
        Timeline: 18 months, starting Q2 2025
        Budget: $2M approved

        DECISION 2: Team Structure
        Create dedicated Platform Engineering team
        Headcount: 8 engineers, 2 leads
        Start date: March 1, 2025

        DECISION 3: Technology Stack
        Standardize on Kubernetes for container orchestration
        Migration plan: Pilot in Q2, full deployment by Q4
        """,
    }


@pytest.fixture
def sample_initiative_data():
    """Sample strategic initiative data for health scoring"""
    return {
        "healthy_initiative": {
            "id": "init_001",
            "name": "Mobile App Redesign",
            "start_date": "2025-01-01",
            "target_end_date": "2025-03-31",
            "current_progress": 0.3,
            "stakeholder_engagement_score": 0.9,
            "milestone_completion_rate": 0.8,
            "budget_utilization": 0.25,
            "risk_indicators": ["minor_delay"],
            "team_satisfaction": 0.85,
        },
        "at_risk_initiative": {
            "id": "init_002",
            "name": "Legacy System Migration",
            "start_date": "2024-10-01",
            "target_end_date": "2025-02-28",
            "current_progress": 0.4,
            "stakeholder_engagement_score": 0.6,
            "milestone_completion_rate": 0.5,
            "budget_utilization": 0.8,
            "risk_indicators": [
                "scope_creep",
                "resource_constraints",
                "stakeholder_disengagement",
            ],
            "team_satisfaction": 0.6,
        },
        "failing_initiative": {
            "id": "init_003",
            "name": "AI Integration Project",
            "start_date": "2024-08-01",
            "target_end_date": "2024-12-31",
            "current_progress": 0.2,
            "stakeholder_engagement_score": 0.3,
            "milestone_completion_rate": 0.2,
            "budget_utilization": 0.9,
            "risk_indicators": [
                "major_delays",
                "budget_overrun",
                "technical_blockers",
                "stakeholder_disengagement",
            ],
            "team_satisfaction": 0.4,
        },
    }


@pytest.fixture
def backwards_compatibility_test_data():
    """Test data to ensure P0 features don't break existing functionality"""
    return {
        "existing_stakeholder_workflow": [
            "stakeholder_profiles_enhanced table exists",
            "stakeholder engagement tracking works",
            "meeting intelligence processing continues",
            "task detection remains functional",
        ],
        "existing_cli_commands": [
            "./claudedirector stakeholders list",
            "./claudedirector tasks scan",
            "./claudedirector meetings scan",
            "./claudedirector status",
        ],
        "existing_database_schema": [
            "stakeholder_profiles_enhanced",
            "meeting_sessions",
            "strategic_tasks",
            "workspace_changes",
        ],
    }


@pytest.fixture
def performance_benchmarks():
    """Performance benchmarks for AI components"""
    return {
        "decision_detection": {
            "max_inference_time_ms": 200,
            "min_accuracy": 0.85,
            "max_memory_usage_mb": 100,
        },
        "health_prediction": {
            "max_inference_time_ms": 200,
            "min_accuracy": 0.80,
            "max_memory_usage_mb": 150,
        },
        "pattern_recognition": {
            "max_inference_time_ms": 500,  # More complex processing
            "min_accuracy": 0.75,
            "max_memory_usage_mb": 200,
        },
    }


@pytest.fixture
def mock_ai_models():
    """Mock AI models for testing without actual ML dependencies"""

    class MockDecisionDetector:
        def __init__(self, accuracy=0.90):
            self.accuracy = accuracy

        def predict(self, text: str) -> Dict[str, Any]:
            # Mock decision detection based on keywords
            decisions = []
            if "DECISION" in text.upper():
                # Extract decision-like patterns
                lines = text.split("\n")
                for i, line in enumerate(lines):
                    if "DECISION" in line.upper():
                        decisions.append(
                            {
                                "decision_text": line.strip(),
                                "confidence": self.accuracy,
                                "timeline": "Q1 2025" if "Q1" in text else "TBD",
                                "owner": "Sarah" if "Sarah" in text else "TBD",
                                "decision_type": "strategic",
                            }
                        )

            return {
                "decisions_detected": len(decisions),
                "decisions": decisions,
                "confidence": self.accuracy,
                "processing_time_ms": 50,  # Mock fast processing
            }

    class MockHealthPredictor:
        def __init__(self, accuracy=0.85):
            self.accuracy = accuracy

        def predict(self, initiative_data: Dict[str, Any]) -> Dict[str, Any]:
            # Mock health scoring based on key indicators
            progress = initiative_data.get("current_progress", 0)
            stakeholder_score = initiative_data.get("stakeholder_engagement_score", 0)
            milestone_rate = initiative_data.get("milestone_completion_rate", 0)
            risks = len(initiative_data.get("risk_indicators", []))

            # Simple scoring algorithm
            health_score = (progress + stakeholder_score + milestone_rate) / 3
            health_score = max(0, health_score - (risks * 0.1))

            if health_score >= 0.8:
                status = "healthy"
                risk_level = "low"
            elif health_score >= 0.6:
                status = "at_risk"
                risk_level = "medium"
            else:
                status = "failing"
                risk_level = "high"

            return {
                "health_score": health_score,
                "status": status,
                "risk_level": risk_level,
                "confidence": self.accuracy,
                "processing_time_ms": 75,
                "recommendations": [
                    (
                        "Increase stakeholder engagement"
                        if stakeholder_score < 0.7
                        else None
                    ),
                    "Address timeline delays" if milestone_rate < 0.7 else None,
                    "Focus on risk mitigation" if risks > 2 else None,
                ],
            }

    return {
        "decision_detector": MockDecisionDetector(),
        "health_predictor": MockHealthPredictor(),
        "high_accuracy_detector": MockDecisionDetector(accuracy=0.95),
        "low_accuracy_detector": MockDecisionDetector(accuracy=0.70),
    }
