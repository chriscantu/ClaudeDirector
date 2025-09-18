"""
Unit tests for Weekly Report Agent

Tests the foundation functionality of the WeeklyReportAgent following
ClaudeDirector testing patterns.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from lib.agents.weekly_report_agent import (
    WeeklyReportAgent,
    WeeklyReportConfig,
    TeamMapping,
    BusinessValueFramework,
)
from lib.core.types import ProcessingResult


class TestWeeklyReportAgent:
    """Test suite for WeeklyReportAgent foundation functionality"""

    @pytest.fixture
    def sample_config(self):
        """Sample configuration for testing"""
        teams = [
            TeamMapping(
                name="Web Platform",
                jira_project="WP",
                focus_areas=["Build system", "Developer tooling"],
                business_value_framework="velocity_multiplier",
            ),
            TeamMapping(
                name="Design System",
                jira_project="DS",
                focus_areas=["Component library", "Design tokens"],
                business_value_framework="consistency_impact",
            ),
        ]

        frameworks = [
            BusinessValueFramework(
                name="velocity_multiplier",
                metrics=["development_velocity", "deployment_frequency"],
                impact_categories=["Developer Productivity", "Time to Market"],
                roi_calculation="velocity_increase * team_count",
            ),
            BusinessValueFramework(
                name="consistency_impact",
                metrics=["design_consistency", "component_reuse"],
                impact_categories=["Brand Consistency", "Development Efficiency"],
                roi_calculation="consistency_savings + efficiency_gain",
            ),
        ]

        return WeeklyReportConfig(
            teams=teams,
            business_frameworks=frameworks,
            jira_base_url="https://test.atlassian.net",
            jira_username="test@example.com",
            jira_api_token="test-token",
        )

    def test_agent_initialization(self, sample_config):
        """Test agent initializes correctly with configuration"""
        agent = WeeklyReportAgent(sample_config)

        assert agent.config == sample_config
        assert len(agent.frameworks_map) == 2
        assert "velocity_multiplier" in agent.frameworks_map
        assert "consistency_impact" in agent.frameworks_map

    def test_business_frameworks_loading(self, sample_config):
        """Test business frameworks are loaded correctly"""
        agent = WeeklyReportAgent(sample_config)

        velocity_framework = agent.frameworks_map["velocity_multiplier"]
        assert velocity_framework.name == "velocity_multiplier"
        assert "Developer Productivity" in velocity_framework.impact_categories

        consistency_framework = agent.frameworks_map["consistency_impact"]
        assert consistency_framework.name == "consistency_impact"
        assert "Brand Consistency" in consistency_framework.impact_categories

    def test_component_initialization(self, sample_config):
        """Test that Jira client and executive summary are initialized"""
        agent = WeeklyReportAgent(sample_config)

        # For Phase 1, we expect components to be None (placeholders)
        assert agent.jira_client is None
        assert agent.executive_summary is None

    @pytest.mark.asyncio
    async def test_team_data_collection_structure(self, sample_config):
        """Test team data collection returns correct structure"""
        agent = WeeklyReportAgent(sample_config)

        # Mock the Jira client to avoid actual API calls
        agent.jira_client = Mock()

        with patch.object(
            agent, "_get_team_jira_metrics", new_callable=AsyncMock
        ) as mock_metrics:
            mock_metrics.return_value = {
                "project": "WP",
                "tickets_completed": 5,
                "velocity_points": 25,
            }

            team_data = await agent._collect_team_data()

            assert len(team_data) == 2  # Two teams configured
            assert "Web Platform" in team_data
            assert "Design System" in team_data

            wp_data = team_data["Web Platform"]
            assert "config" in wp_data
            assert "metrics" in wp_data
            assert "collection_timestamp" in wp_data
            assert wp_data["config"].name == "Web Platform"

    @pytest.mark.asyncio
    async def test_performance_analysis_structure(self, sample_config):
        """Test performance analysis returns correct structure"""
        agent = WeeklyReportAgent(sample_config)

        # Sample team data
        team_data = {
            "Web Platform": {
                "config": sample_config.teams[0],
                "metrics": {"velocity_points": 25, "tickets_completed": 5},
                "collection_timestamp": datetime.now().isoformat(),
            }
        }

        analysis = await agent._analyze_team_performance(team_data)

        assert "Web Platform" in analysis
        wp_analysis = analysis["Web Platform"]
        assert wp_analysis["status"] == "success"
        assert "velocity_trend" in wp_analysis
        assert "completion_rate" in wp_analysis
        assert "recommendations" in wp_analysis

    @pytest.mark.asyncio
    async def test_business_value_translation(self, sample_config):
        """Test business value translation logic"""
        agent = WeeklyReportAgent(sample_config)

        # Sample analysis results
        analysis_results = {
            "Web Platform": {
                "status": "success",
                "velocity_trend": "improving",
                "completion_rate": 0.85,
                "recommendations": ["Optimize build pipeline"],
            }
        }

        business_insights = await agent._translate_business_value(analysis_results)

        assert len(business_insights) == 1
        insight = business_insights[0]
        assert insight["team"] == "Web Platform"
        assert insight["framework"] == "velocity_multiplier"
        assert "business_value" in insight
        assert "roi_impact" in insight

    @pytest.mark.asyncio
    async def test_executive_report_generation(self, sample_config):
        """Test executive report generation structure"""
        agent = WeeklyReportAgent(sample_config)

        # Mock executive summary
        agent.executive_summary = Mock()
        agent.executive_summary.generate_summary = AsyncMock(
            return_value="Test executive summary"
        )

        business_insights = [
            {
                "team": "Web Platform",
                "framework": "velocity_multiplier",
                "business_value": "Improved development velocity",
                "roi_impact": "Positive",
            }
        ]

        report = await agent._generate_executive_report(business_insights)

        assert "executive_summary" in report
        assert "team_details" in report
        assert "generated_at" in report
        assert "report_type" in report
        assert report["report_type"] == "weekly_strategic_update"

    def test_markdown_formatting(self, sample_config):
        """Test markdown report formatting"""
        agent = WeeklyReportAgent(sample_config)

        content = {
            "generated_at": "2025-09-18T10:00:00",
            "executive_summary": "Test summary",
            "team_details": [
                {
                    "team": "Web Platform",
                    "framework": "velocity_multiplier",
                    "business_value": "Improved velocity",
                    "roi_impact": "Positive",
                    "strategic_alignment": "On track",
                }
            ],
        }

        markdown = agent._format_markdown_report(content)

        assert "# Weekly Strategic Platform Report" in markdown
        assert "## Executive Summary" in markdown
        assert "### Web Platform" in markdown
        assert "Test summary" in markdown
        assert "ClaudeDirector Weekly Report Agent" in markdown

    @pytest.mark.asyncio
    async def test_error_handling_in_data_collection(self, sample_config):
        """Test error handling during data collection"""
        agent = WeeklyReportAgent(sample_config)
        agent.jira_client = None  # Simulate initialization failure

        result = await agent.generate_weekly_report()

        assert not result.success
        assert "Jira client not initialized" in result.message
        assert result.data["error_type"] == "RuntimeError"

    @pytest.mark.asyncio
    async def test_successful_report_generation(self, sample_config):
        """Test successful end-to-end report generation"""
        agent = WeeklyReportAgent(sample_config)

        # Mock all external dependencies
        agent.jira_client = Mock()
        agent.executive_summary = Mock()
        agent.executive_summary.generate_summary = AsyncMock(
            return_value="Success summary"
        )

        with patch.object(
            agent, "_get_team_jira_metrics", new_callable=AsyncMock
        ) as mock_metrics:
            mock_metrics.return_value = {"velocity_points": 25}

            result = await agent.generate_weekly_report()

            assert result.success
            assert "successfully" in result.message
            assert "report_content" in result.data
            assert "teams_analyzed" in result.data
            assert result.data["teams_analyzed"] == 2

    @pytest.mark.asyncio
    async def test_config_file_loading(self, tmp_path):
        """Test loading configuration from YAML file"""
        config_content = """
teams:
  - name: "Test Team"
    jira_project: "TT"
    focus_areas: ["Testing"]
    business_value_framework: "test_framework"

business_frameworks:
  - name: "test_framework"
    metrics: ["test_metric"]
    impact_categories: ["Test Impact"]
    roi_calculation: "test_calculation"

jira_base_url: "https://test.example.com"
jira_username: "test@example.com"
jira_api_token: "test-token"
"""

        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)

        agent = await WeeklyReportAgent.create_from_config_file(str(config_file))

        assert len(agent.config.teams) == 1
        assert agent.config.teams[0].name == "Test Team"
        assert len(agent.config.business_frameworks) == 1
        assert agent.config.jira_base_url == "https://test.example.com"
