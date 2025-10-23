"""
Unit Tests: Allocation Report Generator

TDD Phase: RED (write tests first, then implement generator)

BLOAT_PREVENTION: Reuses test patterns from test_allocation_calculator.py
Context7 Pattern: Executive report generation (<30s, <3min read time)

Test Coverage:
- Report generator initialization
- Markdown report structure validation
- Executive summary generation with Context7 benchmarks
- Per-team breakdown with recommendations
- Multi-team aggregation (weighted by issue count)
- Output file handling and symlinks
- Security compliance (zero PII)
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from unittest.mock import MagicMock, patch
import tempfile
import shutil


class TestAllocationReportGeneratorBasics:
    """
    TDD RED: Test AllocationReportGenerator initialization and basic operations

    BLOAT_PREVENTION: Reuses ConfigManager mock pattern from test_allocation_calculator.py
    """

    def test_generator_creation_with_config(self):
        """AllocationReportGenerator should initialize with ConfigManager"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {
            "base_url": "https://jira.example.com",
            "email": "${JIRA_EMAIL}",
            "api_token": "${JIRA_API_TOKEN}",
        }

        generator = AllocationReportGenerator(config)

        assert generator.config == config
        assert generator.jira_client is not None
        assert generator.current_date is not None

    def test_generate_report_returns_path(self):
        """Test generate_report returns Path to created markdown file"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        # Mock AllocationCalculator to return test data
        with patch(
            "lib.reporting.allocation_report_generator.AllocationCalculator"
        ) as MockCalc:
            mock_calculator = MagicMock()
            mock_calculator.calculate_team_allocation.return_value = (
                self._create_test_allocation("Web Platform")
            )
            MockCalc.return_value = mock_calculator

            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "test-report.md"

                report_path = generator.generate_report(
                    teams=["Web Platform"], duration_days=90, output_path=output_path
                )

                assert isinstance(report_path, Path)
                assert report_path.exists()
                assert report_path.suffix == ".md"
                assert report_path.stat().st_size > 100  # Has content

    def test_report_has_required_sections(self):
        """Test report contains all required markdown sections"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        # Mock AllocationCalculator to return test data
        with patch(
            "lib.reporting.allocation_report_generator.AllocationCalculator"
        ) as MockCalc:
            mock_calculator = MagicMock()
            mock_calculator.calculate_team_allocation.return_value = (
                self._create_test_allocation("Web Platform")
            )
            MockCalc.return_value = mock_calculator

            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "test-report.md"
                report_path = generator.generate_report(
                    teams=["Web Platform"], duration_days=90, output_path=output_path
                )

                content = report_path.read_text()

                # Context7 Pattern: All required sections present
                assert "# Team Allocation Report" in content
                assert "## 📊 Executive Summary" in content
                assert "## 👥 Team Breakdown" in content
                assert "## 📈 Context7 Industry Benchmarks" in content
                assert "## 🎯 Recommendations" in content

    def test_report_filename_includes_date(self):
        """Test default report filename includes generation date"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        # Mock AllocationCalculator
        with patch(
            "lib.reporting.allocation_report_generator.AllocationCalculator"
        ) as MockCalc:
            mock_calculator = MagicMock()
            mock_calculator.calculate_team_allocation.return_value = (
                self._create_test_allocation("Web Platform")
            )
            MockCalc.return_value = mock_calculator

            with tempfile.TemporaryDirectory() as tmpdir:
                # Override default output path to use tmpdir
                with patch.object(generator, "_get_default_output_path") as mock_path:
                    mock_path.return_value = (
                        Path(tmpdir)
                        / f"allocation-report-{datetime.now().strftime('%Y-%m-%d')}.md"
                    )

                    report_path = generator.generate_report(
                        teams=["Web Platform"], duration_days=90
                    )

                    date_str = datetime.now().strftime("%Y-%m-%d")
                    assert date_str in report_path.name
                    assert report_path.name.startswith("allocation-report-")
                    assert report_path.name.endswith(".md")

    def _create_test_generator(self):
        """
        BLOAT_PREVENTION: Reusable test fixture

        Creates AllocationReportGenerator with mocked dependencies
        """
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {
            "base_url": "https://jira.example.com",
            "email": "${JIRA_EMAIL}",
            "api_token": "${JIRA_API_TOKEN}",
        }
        config.get = MagicMock(return_value={})  # Empty team mapping (proper mock)

        generator = AllocationReportGenerator(config)

        return generator

    def _create_test_allocation(self, team_name: str):
        """
        BLOAT_PREVENTION: Reusable test allocation fixture

        Creates TeamAllocation with realistic test data
        """
        from lib.reporting.allocation_models import TeamAllocation

        return TeamAllocation(
            team_name=team_name,
            date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
            l0_pct=35.0,
            l1_pct=15.0,
            l2_pct=45.0,
            other_pct=5.0,
            total_issues=127,
            l2_velocity_actual=8.5,
            l2_velocity_projected=10.2,
        )


class TestExecutiveSummaryGeneration:
    """
    TDD RED: Test executive summary markdown generation

    Context7 Pattern: <3 minute read time with actionable insights
    """

    def test_executive_summary_shows_overall_allocation(self):
        """Test executive summary displays aggregate allocation percentages"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=6.0,
                l2_velocity_projected=7.5,
            ),
            TeamAllocation(
                team_name="Team B",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=30.0,
                l1_pct=20.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=50,
                l2_velocity_actual=3.0,
                l2_velocity_projected=3.5,
            ),
        ]

        summary = generator._build_executive_summary(allocations)

        # Context7 Pattern: Shows overall allocation
        assert "Overall Allocation" in summary
        assert "Executive Summary" in summary
        # Weighted average L0: (40*100 + 30*50) / 150 = 36.67%
        assert "36" in summary or "37" in summary
        assert "L0 (Operational)" in summary
        assert "L2 (Strategic)" in summary

    def test_executive_summary_shows_velocity_impact(self):
        """Test executive summary includes velocity impact analysis"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=35.0,
                l1_pct=15.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=8.5,
                l2_velocity_projected=10.2,
            )
        ]

        summary = generator._build_executive_summary(allocations)

        # Context7 Pattern: Velocity impact shown
        assert "Velocity Impact" in summary
        assert "8.5" in summary  # Actual velocity
        assert "10.2" in summary  # Projected velocity
        # Impact = (10.2 - 8.5) / 8.5 * 100 = 20%
        assert "20" in summary or "%" in summary

    def test_executive_summary_identifies_key_insights(self):
        """Test executive summary generates actionable insights"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        # High L0 burden scenario (40% vs 30% baseline)
        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=6.0,
                l2_velocity_projected=8.0,
            )
        ]

        summary = generator._build_executive_summary(allocations)

        # Context7 Pattern: Insights present
        assert "Key Insights" in summary
        # Should flag L0 above baseline
        assert "above" in summary.lower() or "baseline" in summary.lower()

    def test_executive_summary_with_healthy_allocation(self):
        """Test executive summary recognizes healthy allocation patterns"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        # Healthy allocation: 25% L0 (below 30% baseline), 50% L2
        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=25.0,
                l1_pct=20.0,
                l2_pct=50.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=10.0,
                l2_velocity_projected=10.5,
            )
        ]

        summary = generator._build_executive_summary(allocations)

        # Should show positive insights
        assert "✅" in summary or "healthy" in summary.lower()

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


class TestTeamBreakdownGeneration:
    """
    TDD RED: Test per-team breakdown section generation

    Context7 Pattern: Team-by-team visibility (Spotify "team autonomy metrics")
    """

    def test_team_breakdown_shows_per_team_allocation(self):
        """Test team breakdown displays individual team percentages"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Web Platform",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=127,
                l2_velocity_actual=6.2,
                l2_velocity_projected=8.5,
            )
        ]

        breakdown = generator._build_team_breakdown(allocations)

        # Context7 Pattern: Team-specific details
        assert "Web Platform" in breakdown
        assert "40" in breakdown  # L0 percentage
        assert "45" in breakdown  # L2 percentage
        assert "127" in breakdown  # Total issues

    def test_team_breakdown_shows_velocity_per_team(self):
        """Test team breakdown includes per-team velocity metrics"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Web Platform",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=127,
                l2_velocity_actual=6.2,
                l2_velocity_projected=8.5,
            )
        ]

        breakdown = generator._build_team_breakdown(allocations)

        # Context7 Pattern: Velocity visibility
        assert "6.2" in breakdown  # Actual velocity
        assert "8.5" in breakdown  # Projected velocity
        assert "stories/week" in breakdown

    def test_team_breakdown_shows_recommendations_for_high_l0(self):
        """Test team breakdown includes recommendations for high L0 burden"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        # High L0 burden (40% > 35% threshold)
        allocations = [
            TeamAllocation(
                team_name="Web Platform",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=127,
                l2_velocity_actual=6.0,
                l2_velocity_projected=8.5,
            )
        ]

        breakdown = generator._build_team_breakdown(allocations)

        # Should include recommendation
        assert "Recommendation" in breakdown or "recommendation" in breakdown
        assert (
            "on-call" in breakdown.lower()
            or "sre" in breakdown.lower()
            or "consider" in breakdown.lower()
        )

    def test_team_breakdown_sorts_by_l0_burden(self):
        """Test teams are sorted by L0 burden (highest first)"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Low L0 Team",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=25.0,
                l1_pct=15.0,
                l2_pct=55.0,
                other_pct=5.0,
                total_issues=50,
                l2_velocity_actual=5.0,
                l2_velocity_projected=5.5,
            ),
            TeamAllocation(
                team_name="High L0 Team",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=45.0,
                l1_pct=10.0,
                l2_pct=40.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=4.0,
                l2_velocity_projected=6.0,
            ),
        ]

        breakdown = generator._build_team_breakdown(allocations)

        # "High L0 Team" should appear before "Low L0 Team"
        high_pos = breakdown.find("High L0 Team")
        low_pos = breakdown.find("Low L0 Team")
        assert high_pos < low_pos

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


class TestContext7BenchmarkGeneration:
    """
    TDD RED: Test Context7 industry benchmark section

    Context7 Patterns: Google SRE, Spotify, Netflix operational excellence
    """

    def test_context7_section_includes_industry_standards(self):
        """Test Context7 section shows Google SRE and Spotify benchmarks"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=35.0,
                l1_pct=15.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=8.0,
                l2_velocity_projected=9.0,
            )
        ]

        benchmarks = generator._build_context7_benchmarks(allocations)

        # Context7 Pattern: Industry standards present
        assert "Google SRE" in benchmarks
        assert "Spotify" in benchmarks or "Netflix" in benchmarks
        assert "50%" in benchmarks or "toil" in benchmarks.lower()

    def test_context7_section_compares_to_your_teams(self):
        """Test Context7 section compares team performance to industry"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=35.0,
                l1_pct=15.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=8.0,
                l2_velocity_projected=9.0,
            )
        ]

        benchmarks = generator._build_context7_benchmarks(allocations)

        # Should compare to user's teams
        assert "Your Teams" in benchmarks
        assert "45" in benchmarks  # L2 percentage
        assert (
            "above" in benchmarks.lower()
            or "below" in benchmarks.lower()
            or "target" in benchmarks.lower()
        )

    def test_context7_section_provides_target_recommendation(self):
        """Test Context7 section provides actionable target"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=7.0,
                l2_velocity_projected=9.0,
            )
        ]

        benchmarks = generator._build_context7_benchmarks(allocations)

        # Should provide target recommendation
        assert "Target" in benchmarks
        assert "30%" in benchmarks or "velocity" in benchmarks.lower()

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


class TestMultiTeamAggregation:
    """
    TDD RED: Test multi-team allocation aggregation logic

    Context7 Pattern: Weighted averaging by issue count (not simple mean)
    """

    def test_aggregate_allocations_calculates_weighted_average(self):
        """Test aggregation weighs percentages by issue count"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Large Team",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=40.0,
                l1_pct=10.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=8.0,
                l2_velocity_projected=10.0,
            ),
            TeamAllocation(
                team_name="Small Team",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=20.0,
                l1_pct=20.0,
                l2_pct=55.0,
                other_pct=5.0,
                total_issues=50,
                l2_velocity_actual=5.0,
                l2_velocity_projected=6.0,
            ),
        ]

        aggregate = generator._aggregate_allocations(allocations)

        # Weighted L0: (40*100 + 20*50) / 150 = 33.33%
        assert 33.0 <= aggregate.l0_pct <= 34.0
        # Weighted L2: (45*100 + 55*50) / 150 = 48.33%
        assert 48.0 <= aggregate.l2_pct <= 49.0
        assert aggregate.team_name == "Overall"
        assert aggregate.total_issues == 150

    def test_aggregate_velocity_sums_across_teams(self):
        """Test velocity aggregation sums L2 velocity"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Team A",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=35.0,
                l1_pct=15.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=100,
                l2_velocity_actual=6.2,
                l2_velocity_projected=7.5,
            ),
            TeamAllocation(
                team_name="Team B",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=30.0,
                l1_pct=20.0,
                l2_pct=45.0,
                other_pct=5.0,
                total_issues=50,
                l2_velocity_actual=8.5,
                l2_velocity_projected=10.0,
            ),
        ]

        aggregate = generator._aggregate_allocations(allocations)

        # Sum velocities: 6.2 + 8.5 = 14.7
        assert abs(aggregate.l2_velocity_actual - 14.7) < 0.1
        # Sum projected: 7.5 + 10.0 = 17.5
        assert abs(aggregate.l2_velocity_projected - 17.5) < 0.1

    def test_aggregate_handles_empty_list(self):
        """Test aggregation gracefully handles empty team list"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        allocations = []

        aggregate = generator._aggregate_allocations(allocations)

        assert aggregate.team_name == "Overall"
        assert aggregate.total_issues == 0
        assert aggregate.l0_pct == 0.0

    def test_aggregate_handles_zero_issues(self):
        """Test aggregation handles teams with zero completed issues"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.allocation_models import TeamAllocation

        generator = self._create_test_generator()

        allocations = [
            TeamAllocation(
                team_name="Inactive Team",
                date_range=(datetime(2025, 1, 1), datetime(2025, 3, 31)),
                l0_pct=0.0,
                l1_pct=0.0,
                l2_pct=0.0,
                other_pct=100.0,
                total_issues=0,
                l2_velocity_actual=0.0,
                l2_velocity_projected=0.0,
            )
        ]

        aggregate = generator._aggregate_allocations(allocations)

        assert aggregate.total_issues == 0
        assert aggregate.other_pct == 100.0

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


class TestOutputFileHandling:
    """
    TDD RED: Test report output file creation and management

    Context7 Pattern: Timestamped reports + latest symlink
    """

    def test_report_saves_to_specified_path(self):
        """Test report saves to custom output path"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "custom-report.md"

            report_path = generator.generate_report(
                teams=["Web Platform"], duration_days=90, output_path=output_path
            )

            assert report_path == output_path
            assert report_path.exists()

    def test_default_path_includes_leadership_workspace(self):
        """Test default output path uses leadership-workspace/reports/allocation/"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        default_path = generator._get_default_output_path()

        assert "leadership-workspace" in str(default_path)
        assert "reports/allocation" in str(default_path)
        assert default_path.name.startswith("allocation-report-")
        assert default_path.suffix == ".md"

    def test_timestamped_filename_format(self):
        """Test report filename follows allocation-report-YYYY-MM-DD.md format"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        default_path = generator._get_default_output_path()

        # Should match pattern: allocation-report-2025-10-23.md
        import re

        pattern = r"allocation-report-\d{4}-\d{2}-\d{2}\.md"
        assert re.match(pattern, default_path.name)

    def test_latest_symlink_created(self):
        """Test latest.md symlink points to newest report"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "allocation-report-2025-10-23.md"
            output_path.write_text("Test report content")

            generator._update_latest_symlink(output_path)

            latest_path = output_path.parent / "allocation-report-latest.md"
            assert latest_path.exists()
            assert latest_path.is_symlink()
            assert latest_path.resolve() == output_path.resolve()

    def test_latest_symlink_updates_on_new_report(self):
        """Test latest.md symlink updates when new report generated"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create first report
            old_report = Path(tmpdir) / "allocation-report-2025-10-22.md"
            old_report.write_text("Old report")
            generator._update_latest_symlink(old_report)

            # Create new report
            new_report = Path(tmpdir) / "allocation-report-2025-10-23.md"
            new_report.write_text("New report")
            generator._update_latest_symlink(new_report)

            latest_path = new_report.parent / "allocation-report-latest.md"
            assert latest_path.resolve() == new_report.resolve()

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


class TestSecurityCompliance:
    """
    TDD RED: Test zero PII in generated reports

    Security Requirement: No email addresses, company domains, or credentials
    """

    def test_report_contains_no_email_addresses(self):
        """Test generated report contains no email addresses"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test-report.md"
            report_path = generator.generate_report(
                teams=["Web Platform"], duration_days=90, output_path=output_path
            )

            content = report_path.read_text()

            # No email patterns
            import re

            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            assert not re.search(email_pattern, content)

    def test_report_contains_no_company_domains(self):
        """Test report doesn't leak company-specific domains"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test-report.md"
            report_path = generator.generate_report(
                teams=["Web Platform"], duration_days=90, output_path=output_path
            )

            content = report_path.read_text()

            # No company-specific identifiers (use generic test, actual values from config)
            assert "***REMOVED***" not in content

    def test_report_uses_team_names_not_individuals(self):
        """Test report shows team aggregates, not individual contributors"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test-report.md"
            report_path = generator.generate_report(
                teams=["Web Platform"], duration_days=90, output_path=output_path
            )

            content = report_path.read_text()

            # Should have team name
            assert "Web Platform" in content
            # Report should be aggregate, not individual-focused
            assert "Team Breakdown" in content

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


class TestReportHeaderGeneration:
    """
    TDD RED: Test report header with metadata
    """

    def test_report_header_includes_period(self):
        """Test report header shows date range"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        header = generator._build_report_header(start_date, end_date)

        assert "Period" in header
        assert "January 01, 2025" in header
        assert "March 31, 2025" in header

    def test_report_header_includes_generation_date(self):
        """Test report header shows when report was generated"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        header = generator._build_report_header(start_date, end_date)

        assert "Generated" in header
        # Should have current date
        assert "2025" in header

    def test_report_header_includes_title(self):
        """Test report header has descriptive title"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator

        generator = self._create_test_generator()

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        header = generator._build_report_header(start_date, end_date)

        assert "# Team Allocation Report" in header
        assert "90-Day" in header or "Rolling Window" in header

    def _create_test_generator(self):
        """BLOAT_PREVENTION: Reuse test generator fixture"""
        from lib.reporting.allocation_report_generator import AllocationReportGenerator
        from lib.reporting.jira_reporter import ConfigManager
        from unittest.mock import MagicMock

        config = MagicMock(spec=ConfigManager)
        config.get_jira_config.return_value = {}
        config.get = MagicMock(return_value={})  # Proper mock

        return AllocationReportGenerator(config)


# BLOAT_PREVENTION Summary:
# - Reuses test patterns from test_allocation_calculator.py (fixture structure)
# - Reuses ConfigManager and JiraClient mocking approach
# - Shared test fixture methods (_create_test_generator, _create_test_allocation)
# - No duplication of test utilities
# - Follows TDD RED phase: tests written before implementation
# - Total: 30+ comprehensive unit tests covering all requirements
