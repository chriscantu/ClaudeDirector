# Allocation Report Generation - Task Breakdown (Phase 2.2)

**Spec-Kit Format v1.0** | **Status**: Ready for Implementation | **Owner**: Martin | Platform Architecture
**Spec**: 004-allocation-report-generation | **PR**: #179
**Foundation**: Phase 2.1 complete (PR #178 merged - AllocationCalculator 18/18 tests passing)

---

## 📋 **Task Organization**

This document breaks down Phase 2.2 implementation into specific, actionable tasks following **TDD workflow** (RED-GREEN-Refactor) and **Context7 industry patterns**.

**Implementation Strategy**:
- Tasks organized by **User Story** (Phase 2.2 focus)
- **Dependencies** clearly marked
- **Parallel execution** marked with `[P]` where applicable
- **File paths** specified for each task
- **Test-first approach** (write tests before implementation)

**Foundation (Phase 2.1 - COMPLETE)**:
- ✅ AllocationCalculator (18/18 tests passing)
- ✅ TeamAllocation data model (11/11 tests passing)
- ✅ Context7 velocity patterns (Google SRE, Spotify, Netflix)
- ✅ Cross-project hierarchy traversal (L0/L1/L2 classification)
- ✅ Security (14/14 PII prevention tests passing)

---

## 🎯 **Phase 2.2: Report Generation & CLI** (4-7 hours)

### **User Story 2.2.1: Markdown Report Generator**

**Goal**: Generate executive-ready markdown reports from AllocationCalculator data

**Success Criteria**:
- [ ] Report generation <30 seconds (90-day window)
- [ ] Executive summary comprehensible in <3 minutes
- [ ] Multi-team aggregation (overall + individual breakdown)
- [ ] Zero PII in output
- [ ] Context7 industry benchmarks included
- [ ] Unit test coverage >90%

---

#### **Task 2.2.1.1: Create AllocationReportGenerator class (TDD RED)**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Phase 2.1 complete (PR #178)

**Files**:
- `tests/unit/reporting/test_allocation_report_generator.py` (NEW - write first)
- `.claudedirector/lib/reporting/allocation_report_generator.py` (NEW - implement after tests)

**Steps**:

1. **RED**: Write comprehensive unit tests
   ```python
   # tests/unit/reporting/test_allocation_report_generator.py
   import pytest
   from datetime import datetime
   from lib.reporting.allocation_report_generator import AllocationReportGenerator
   from lib.reporting.allocation_models import TeamAllocation
   
   class TestAllocationReportGeneratorBasics:
       def test_generator_creation_with_config(self):
           """Test generator initializes with ConfigManager"""
           config = MockConfigManager()
           generator = AllocationReportGenerator(config)
           assert generator.config == config
       
       def test_generate_report_returns_path(self):
           """Test generate_report returns Path to created file"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(
               teams=["Web Platform"],
               duration_days=90
           )
           assert report_path.exists()
           assert report_path.suffix == ".md"
       
       def test_report_has_required_sections(self):
           """Test report contains all required sections"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(
               teams=["Web Platform"],
               duration_days=90
           )
           content = report_path.read_text()
           assert "# Team Allocation Report" in content
           assert "## 📊 Executive Summary" in content
           assert "## 👥 Team Breakdown" in content
           assert "## 📈 Context7 Industry Benchmarks" in content
       
       def test_report_filename_includes_date(self):
           """Test report filename includes generation date"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(teams=["Web Platform"], duration_days=90)
           assert datetime.now().strftime("%Y-%m-%d") in report_path.name
   
   class TestExecutiveSummaryGeneration:
       def test_executive_summary_shows_overall_allocation(self):
           """Test executive summary shows aggregate allocation percentages"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [
               TeamAllocation(team_name="Team A", l0_pct=40.0, l1_pct=10.0, l2_pct=45.0, other_pct=5.0, ...),
               TeamAllocation(team_name="Team B", l0_pct=30.0, l1_pct=15.0, l2_pct=50.0, other_pct=5.0, ...)
           ]
           summary = generator._build_executive_summary(allocations)
           assert "Overall Allocation" in summary
           assert "35%" in summary  # Average L0: (40+30)/2
           assert "47.5%" in summary  # Average L2: (45+50)/2
       
       def test_executive_summary_shows_velocity_impact(self):
           """Test executive summary shows velocity impact analysis"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [TeamAllocation(l2_velocity_actual=8.5, l2_velocity_projected=10.2, ...)]
           summary = generator._build_executive_summary(allocations)
           assert "Velocity Impact" in summary
           assert "8.5" in summary  # Actual velocity
           assert "10.2" in summary  # Projected velocity
           assert "-16.7%" in summary or "-17%" in summary  # Impact percentage
       
       def test_executive_summary_identifies_key_insights(self):
           """Test executive summary generates actionable insights"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [TeamAllocation(l0_pct=35.0, l2_pct=45.0, ...)]  # L0 above 30% baseline
           summary = generator._build_executive_summary(allocations)
           assert "above baseline" in summary.lower() or "above industry" in summary.lower()
   
   class TestTeamBreakdownGeneration:
       def test_team_breakdown_shows_per_team_allocation(self):
           """Test team breakdown shows individual team percentages"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [
               TeamAllocation(team_name="Web Platform", l0_pct=40.0, l1_pct=10.0, l2_pct=45.0, ...)
           ]
           breakdown = generator._build_team_breakdown(allocations)
           assert "Web Platform" in breakdown
           assert "40%" in breakdown  # L0 percentage
           assert "45%" in breakdown  # L2 percentage
       
       def test_team_breakdown_shows_velocity_per_team(self):
           """Test team breakdown includes per-team velocity metrics"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [
               TeamAllocation(team_name="Web Platform", l2_velocity_actual=6.2, l2_velocity_projected=8.5, ...)
           ]
           breakdown = generator._build_team_breakdown(allocations)
           assert "6.2 stories/week" in breakdown
           assert "8.5" in breakdown
       
       def test_team_breakdown_shows_recommendations(self):
           """Test team breakdown includes actionable recommendations"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [
               TeamAllocation(team_name="Web Platform", l0_pct=40.0, ...)  # High L0 burden
           ]
           breakdown = generator._build_team_breakdown(allocations)
           assert "recommendation" in breakdown.lower() or "consider" in breakdown.lower()
   
   class TestContext7BenchmarkGeneration:
       def test_context7_section_includes_industry_standards(self):
           """Test Context7 section shows Google SRE, Spotify patterns"""
           generator = AllocationReportGenerator(mock_config)
           benchmarks = generator._build_context7_benchmarks([])
           assert "Google SRE" in benchmarks
           assert "Spotify" in benchmarks or "Netflix" in benchmarks
           assert "<50%" in benchmarks or "50%" in benchmarks  # Toil target
       
       def test_context7_section_compares_to_your_teams(self):
           """Test Context7 section compares team performance to industry"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [TeamAllocation(l2_pct=45.0, ...)]
           benchmarks = generator._build_context7_benchmarks(allocations)
           assert "Your Teams" in benchmarks
           assert "45%" in benchmarks
   
   class TestMultiTeamAggregation:
       def test_aggregate_allocations_calculates_weighted_average(self):
           """Test aggregation weighs percentages by issue count"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [
               TeamAllocation(l0_pct=40.0, total_issues=100, ...),
               TeamAllocation(l0_pct=30.0, total_issues=50, ...)
           ]
           aggregate = generator._aggregate_allocations(allocations)
           # Weighted: (40*100 + 30*50) / 150 = 36.67%
           assert 36.0 <= aggregate.l0_pct <= 37.0
       
       def test_aggregate_velocity_sums_across_teams(self):
           """Test velocity aggregation sums L2 velocity"""
           generator = AllocationReportGenerator(mock_config)
           allocations = [
               TeamAllocation(l2_velocity_actual=6.2, ...),
               TeamAllocation(l2_velocity_actual=8.5, ...)
           ]
           aggregate = generator._aggregate_allocations(allocations)
           assert aggregate.l2_velocity_actual == 14.7
   
   class TestOutputFileHandling:
       def test_report_saves_to_leadership_workspace(self):
           """Test report saves to leadership-workspace/reports/allocation/"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(teams=["Web Platform"], duration_days=90)
           assert "leadership-workspace/reports/allocation" in str(report_path)
       
       def test_timestamped_filename_format(self):
           """Test report filename follows allocation-report-YYYY-MM-DD.md format"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(teams=["Web Platform"], duration_days=90)
           assert report_path.name.startswith("allocation-report-")
           assert report_path.name.endswith(".md")
       
       def test_latest_symlink_created(self):
           """Test latest.md symlink points to newest report"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(teams=["Web Platform"], duration_days=90)
           latest_path = report_path.parent / "allocation-report-latest.md"
           assert latest_path.exists()
           assert latest_path.is_symlink()
   
   class TestSecurityCompliance:
       def test_report_contains_no_pii(self):
           """Test generated report contains zero PII"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(teams=["Web Platform"], duration_days=90)
           content = report_path.read_text()
           # Test for common PII patterns
           assert "@procore.com" not in content
           assert "***REMOVED***" not in content
       
       def test_report_uses_team_names_not_individuals(self):
           """Test report shows team aggregates, not individual contributors"""
           generator = AllocationReportGenerator(mock_config)
           report_path = generator.generate_report(teams=["Web Platform"], duration_days=90)
           content = report_path.read_text()
           assert "Web Platform Team" in content
           # Ensure no individual names (would require more sophisticated check)
   ```

2. **Verify tests FAIL** (RED phase confirmed)
   ```bash
   pytest tests/unit/reporting/test_allocation_report_generator.py -v
   # Expected: 18-20 failing tests (class doesn't exist yet)
   ```

**Acceptance**: All tests fail with "ModuleNotFoundError" or "ImportError" (RED phase confirmed)

---

#### **Task 2.2.1.2: Implement AllocationReportGenerator (TDD GREEN)**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 2.2.1.1 (RED phase complete)

**Files**:
- `.claudedirector/lib/reporting/allocation_report_generator.py` (NEW - implement)

**Steps**:

1. **GREEN**: Implement core AllocationReportGenerator class
   ```python
   # .claudedirector/lib/reporting/allocation_report_generator.py
   from pathlib import Path
   from datetime import datetime
   from typing import List, Optional
   import logging
   
   from .allocation_calculator import AllocationCalculator
   from .allocation_models import TeamAllocation
   from .jira_reporter import ConfigManager, JiraClient
   
   logger = logging.getLogger(__name__)
   
   class AllocationReportGenerator:
       """
       Generate executive-ready markdown allocation reports
       
       BLOAT_PREVENTION: Reuses AllocationCalculator from Phase 2.1
       Context7: Executive summary patterns from weekly_reporter.py
       
       Usage:
           generator = AllocationReportGenerator(config)
           report_path = generator.generate_report(
               teams=["Web Platform", "Hubs"],
               duration_days=90
           )
       """
       
       def __init__(self, config: ConfigManager):
           """Initialize generator with config"""
           self.config = config
           self.jira_client = JiraClient(config.get_jira_config())
           self.current_date = datetime.now()
       
       def generate_report(
           self,
           teams: List[str],
           duration_days: int = 90,
           output_path: Optional[Path] = None
       ) -> Path:
           """
           Generate allocation report for specified teams
           
           Args:
               teams: List of Jira project names (e.g. ["Web Platform", "Hubs"])
               duration_days: Rolling window duration (default: 90 days)
               output_path: Optional custom output path
           
           Returns:
               Path to generated markdown report
           
           Context7 Pattern: Report generation <30s (Google SRE "instant insights")
           """
           logger.info(f"Generating allocation report for {len(teams)} teams ({duration_days} days)")
           
           # Calculate date range
           end_date = self.current_date
           start_date = end_date - timedelta(days=duration_days)
           
           # Calculate allocations for each team (REUSE AllocationCalculator)
           calculator = AllocationCalculator(self.jira_client, start_date, end_date)
           allocations = []
           
           for team in teams:
               jira_project = self._map_team_to_jira_project(team)
               allocation = calculator.calculate_team_allocation(team, jira_project)
               allocations.append(allocation)
           
           # Build markdown report sections
           report_content = self._build_report_header(start_date, end_date)
           report_content += self._build_executive_summary(allocations)
           report_content += self._build_team_breakdown(allocations)
           report_content += self._build_context7_benchmarks(allocations)
           report_content += self._build_recommendations(allocations)
           
           # Save report to leadership-workspace
           if not output_path:
               output_path = self._get_default_output_path()
           
           output_path.parent.mkdir(parents=True, exist_ok=True)
           output_path.write_text(report_content, encoding="utf-8")
           
           # Create symlink to latest report
           self._update_latest_symlink(output_path)
           
           logger.info(f"Report generated: {output_path}")
           return output_path
       
       def _build_report_header(self, start_date: datetime, end_date: datetime) -> str:
           """Build report header with title and metadata"""
           return f"""# Team Allocation Report - {(end_date - start_date).days}-Day Rolling Window

**Period**: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}
**Generated**: {self.current_date.strftime('%B %d, %Y at %I:%M %p')}

---

"""
       
       def _build_executive_summary(self, allocations: List[TeamAllocation]) -> str:
           """
           Build executive summary with overall allocation and key insights
           
           Context7 Pattern: <2 minute read time (Netflix "executive summaries")
           """
           # Calculate aggregate allocation (weighted by issue count)
           aggregate = self._aggregate_allocations(allocations)
           
           # Calculate deviation from 30% L0 baseline (Context7: Google SRE toil target)
           baseline_l0 = 30.0
           l0_delta = aggregate.l0_pct - baseline_l0
           
           # Velocity impact analysis
           if aggregate.l2_velocity_actual > 0:
               velocity_impact_pct = (
                   (aggregate.l2_velocity_projected - aggregate.l2_velocity_actual) 
                   / aggregate.l2_velocity_actual
               ) * 100
           else:
               velocity_impact_pct = 0.0
           
           # Key insights (Context7: Actionable, evidence-based)
           insights = []
           if l0_delta > 5:
               insights.append(f"⚠️ L0 burden {l0_delta:.1f}% above industry baseline ({baseline_l0:.0f}%)")
           elif l0_delta < -5:
               insights.append(f"✅ L0 burden {abs(l0_delta):.1f}% below industry baseline (healthy)")
           
           if aggregate.l2_pct >= 40:
               insights.append(f"✅ L2 allocation healthy ({aggregate.l2_pct:.1f}% ≥ 40% target)")
           else:
               insights.append(f"⚠️ L2 allocation below target ({aggregate.l2_pct:.1f}% < 40%)")
           
           if velocity_impact_pct > 10:
               insights.append(f"🎯 Reducing L0 to {baseline_l0:.0f}% could increase velocity by {velocity_impact_pct:.1f}%")
           
           insights_str = "\n".join(f"- {insight}" for insight in insights)
           
           return f"""## 📊 Executive Summary

### Overall Allocation
- **L0 (Operational)**: {aggregate.l0_pct:.1f}% ({l0_delta:+.1f}% vs baseline)
- **L1 (Enabling)**: {aggregate.l1_pct:.1f}%
- **L2 (Strategic)**: {aggregate.l2_pct:.1f}%
- **Other**: {aggregate.other_pct:.1f}%

### Velocity Impact
- **Current L2 Velocity**: {aggregate.l2_velocity_actual:.1f} stories/week
- **Projected (at {baseline_l0:.0f}% L0)**: {aggregate.l2_velocity_projected:.1f} stories/week
- **Impact**: {velocity_impact_pct:+.1f}% ({'moderate' if abs(velocity_impact_pct) < 20 else 'significant'} burden)

### Key Insights
{insights_str}

---

"""
       
       def _build_team_breakdown(self, allocations: List[TeamAllocation]) -> str:
           """
           Build per-team allocation breakdown
           
           Context7 Pattern: Team-by-team visibility (Spotify "team autonomy metrics")
           """
           breakdown = "## 👥 Team Breakdown\n\n"
           
           for allocation in sorted(allocations, key=lambda a: a.l0_pct, reverse=True):
               velocity_impact_pct = (
                   (allocation.l2_velocity_projected - allocation.l2_velocity_actual) 
                   / allocation.l2_velocity_actual * 100
               ) if allocation.l2_velocity_actual > 0 else 0.0
               
               impact_label = "high" if abs(velocity_impact_pct) > 20 else "moderate"
               
               # Generate recommendation based on L0 burden
               recommendation = ""
               if allocation.l0_pct > 35:
                   recommendation = f"\n\n**Recommendation**: Consider dedicating on-call rotation or SRE support to reduce L0 impact on strategic work."
               elif allocation.l2_pct >= 50:
                   recommendation = f"\n\n**Recommendation**: Healthy L2 allocation - maintain current strategic focus."
               
               breakdown += f"""### {allocation.team_name}
- **Allocation**: L0: {allocation.l0_pct:.1f}% | L1: {allocation.l1_pct:.1f}% | L2: {allocation.l2_pct:.1f}% | Other: {allocation.other_pct:.1f}%
- **Total Issues**: {allocation.total_issues} completed
- **L2 Velocity**: {allocation.l2_velocity_actual:.1f} stories/week (actual) vs {allocation.l2_velocity_projected:.1f} (projected)
- **Velocity Impact**: {velocity_impact_pct:+.1f}% ({impact_label} L0 burden){recommendation}

---

"""
           
           return breakdown
       
       def _build_context7_benchmarks(self, allocations: List[TeamAllocation]) -> str:
           """
           Build Context7 industry benchmarks section
           
           Context7 Patterns: Google SRE, Spotify, Netflix operational excellence
           """
           aggregate = self._aggregate_allocations(allocations)
           
           return f"""## 📈 Context7 Industry Benchmarks

**Industry Standards**:
- **Google SRE Target**: <50% toil (operational work)
- **Spotify Innovation Time**: 70-80% strategic work
- **Netflix Operational Load**: 20-30% operational baseline

**Your Teams**:
- **Strategic Work (L2)**: {aggregate.l2_pct:.1f}% ({'above' if aggregate.l2_pct > 40 else 'below'} 40% target)
- **Operational Work (L0)**: {aggregate.l0_pct:.1f}% ({'above' if aggregate.l0_pct > 30 else 'at/below'} 30% baseline)

**Target**: Reduce L0 from {aggregate.l0_pct:.1f}% → 30% to unlock {((aggregate.l0_pct - 30) / 10 * 20):.0f}% velocity gain.

---

"""
       
       def _build_recommendations(self, allocations: List[TeamAllocation]) -> str:
           """Build prioritized recommendations section"""
           recommendations = []
           
           # High priority: Teams with >35% L0
           high_l0_teams = [a for a in allocations if a.l0_pct > 35]
           if high_l0_teams:
               for team in high_l0_teams:
                   velocity_impact = (
                       (team.l2_velocity_projected - team.l2_velocity_actual) 
                       / team.l2_velocity_actual * 100
                   ) if team.l2_velocity_actual > 0 else 0
                   recommendations.append({
                       "priority": "High",
                       "team": team.team_name,
                       "issue": f"{team.l0_pct:.1f}% L0 burden ({team.l0_pct - 30:.1f}% above baseline)",
                       "impact": f"{abs(velocity_impact):.1f}% velocity degradation",
                       "action": "Implement on-call rotation or hire SRE support"
                   })
           
           # Medium priority: Low L2 allocation
           low_l2_teams = [a for a in allocations if a.l2_pct < 40]
           if low_l2_teams:
               for team in low_l2_teams:
                   recommendations.append({
                       "priority": "Medium",
                       "team": team.team_name,
                       "issue": f"{team.l2_pct:.1f}% L2 allocation (below 40% target)",
                       "impact": "Strategic initiatives underfunded",
                       "action": "Review L0/L1 work for consolidation or deferral opportunities"
                   })
           
           # Build recommendations markdown
           if not recommendations:
               return """## 🎯 Recommendations

**All teams operating within healthy allocation ranges!**

Continue monitoring L0 burden and L2 velocity trends.

---

"""
           
           recs_str = ""
           for i, rec in enumerate(recommendations[:5], 1):  # Limit to top 5
               recs_str += f"""{i}. **{rec['priority']} Priority**: {rec['team']}
   - **Current**: {rec['issue']}
   - **Impact**: {rec['impact']}
   - **Action**: {rec['action']}

"""
           
           return f"""## 🎯 Recommendations

{recs_str}
---

"""
       
       def _aggregate_allocations(self, allocations: List[TeamAllocation]) -> TeamAllocation:
           """
           Aggregate multiple team allocations into overall summary
           
           Uses weighted average by issue count for percentages
           Sums velocities across teams
           """
           if not allocations:
               return TeamAllocation(
                   team_name="Overall",
                   date_range=(datetime.now(), datetime.now()),
                   l0_pct=0.0, l1_pct=0.0, l2_pct=0.0, other_pct=0.0,
                   total_issues=0,
                   l2_velocity_actual=0.0,
                   l2_velocity_projected=0.0
               )
           
           total_issues = sum(a.total_issues for a in allocations)
           
           if total_issues == 0:
               # No data - return zeros
               return TeamAllocation(
                   team_name="Overall",
                   date_range=allocations[0].date_range,
                   l0_pct=0.0, l1_pct=0.0, l2_pct=0.0, other_pct=100.0,
                   total_issues=0,
                   l2_velocity_actual=0.0,
                   l2_velocity_projected=0.0
               )
           
           # Weighted average by issue count
           l0_weighted = sum(a.l0_pct * a.total_issues for a in allocations) / total_issues
           l1_weighted = sum(a.l1_pct * a.total_issues for a in allocations) / total_issues
           l2_weighted = sum(a.l2_pct * a.total_issues for a in allocations) / total_issues
           other_weighted = sum(a.other_pct * a.total_issues for a in allocations) / total_issues
           
           # Sum velocities
           l2_velocity_actual_sum = sum(a.l2_velocity_actual for a in allocations)
           l2_velocity_projected_sum = sum(a.l2_velocity_projected for a in allocations)
           
           return TeamAllocation(
               team_name="Overall",
               date_range=allocations[0].date_range,
               l0_pct=round(l0_weighted, 1),
               l1_pct=round(l1_weighted, 1),
               l2_pct=round(l2_weighted, 1),
               other_pct=round(other_weighted, 1),
               total_issues=total_issues,
               l2_velocity_actual=round(l2_velocity_actual_sum, 2),
               l2_velocity_projected=round(l2_velocity_projected_sum, 2)
           )
       
       def _get_default_output_path(self) -> Path:
           """Get default output path in leadership-workspace"""
           date_str = self.current_date.strftime("%Y-%m-%d")
           workspace = Path("leadership-workspace/reports/allocation")
           return workspace / f"allocation-report-{date_str}.md"
       
       def _update_latest_symlink(self, report_path: Path):
           """Create/update symlink to latest report"""
           latest_path = report_path.parent / "allocation-report-latest.md"
           
           # Remove existing symlink if present
           if latest_path.exists() or latest_path.is_symlink():
               latest_path.unlink()
           
           # Create new symlink
           latest_path.symlink_to(report_path.name)
       
       def _map_team_to_jira_project(self, team: str) -> str:
           """Map team name to Jira project key (from config)"""
           # BLOAT_PREVENTION: Reuse team mapping from config
           team_mapping = self.config.get("team_project_mapping", {})
           return team_mapping.get(team, team)
   ```

2. **Run tests to verify GREEN**
   ```bash
   pytest tests/unit/reporting/test_allocation_report_generator.py -v
   # Expected: 18-20 passing tests
   ```

3. **REFACTOR**: Add docstrings, type hints, error handling

**Acceptance**: All 18-20 tests pass (GREEN phase confirmed), report generation working

---

#### **Task 2.2.1.3: Integration test with real AllocationCalculator**

**Status**: 🧪 TEST (Integration)

**Dependencies**: Task 2.2.1.2 (GREEN phase complete)

**Files**:
- `tests/integration/test_allocation_report_end_to_end.py` (NEW)

**Steps**:

1. Create integration test with mock Jira data
   ```python
   def test_end_to_end_report_generation():
       """Test full report generation pipeline"""
       # Setup mock config and Jira client
       config = create_test_config()
       generator = AllocationReportGenerator(config)
       
       # Generate report
       report_path = generator.generate_report(
           teams=["Web Platform", "Hubs"],
           duration_days=90
       )
       
       # Verify report exists and has content
       assert report_path.exists()
       content = report_path.read_text()
       assert len(content) > 1000  # Substantial content
       assert "Web Platform" in content
       assert "Hubs" in content
   ```

2. Run integration tests
   ```bash
   pytest tests/integration/test_allocation_report_end_to_end.py -v
   ```

**Acceptance**: Integration test passes, end-to-end report generation working

---

### **User Story 2.2.2: CLI Integration**

**Goal**: Create `/generate-allocation-report` command for Cursor chat interface

**Success Criteria**:
- [ ] Command executes from Cursor chat
- [ ] Accepts team and duration arguments
- [ ] Defaults from config file
- [ ] Error handling and logging
- [ ] <5 second response to acknowledge command

---

#### **Task 2.2.2.1: Create CLI command handler**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Task 2.2.1.3 (Report generator complete)

**Files**:
- `tests/unit/commands/test_allocation_report_command.py` (NEW)
- `.claudedirector/lib/commands/allocation_report_command.py` (NEW)

**Steps**:

1. **RED**: Write CLI command tests
2. **GREEN**: Implement command handler
   ```python
   def handle_allocation_report_command(args: List[str]) -> str:
       """
       Handle /generate-allocation-report command
       
       Usage:
         /generate-allocation-report
         /generate-allocation-report --teams "Web Platform,Hubs"
         /generate-allocation-report --days 60
       
       BLOAT_PREVENTION: Reuses command pattern from weekly_reporter
       """
       # Parse arguments
       # Load config
       # Generate report
       # Return path to report
   ```

**Acceptance**: CLI command works, tests pass

---

#### **Task 2.2.2.2: Register command in .cursorrules**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 2.2.2.1

**Files**:
- `.cursorrules` (UPDATE)

**Steps**:

1. Add command documentation
   ```
   - `/generate-allocation-report`: Generate rolling 90-day team allocation report
   ```

2. Test command from Cursor chat

**Acceptance**: Command appears in Cursor autocomplete, executes successfully

---

## 📊 **Estimated Effort**

| Phase | Tasks | Estimate | Priority |
|-------|-------|----------|----------|
| 2.2.1 | Report Generator | 3-4 hours | P0 |
| 2.2.2 | CLI Integration | 1-2 hours | P0 |
| **Total** | **6 tasks** | **4-6 hours** | **P0** |

---

## 🎯 **Success Metrics**

- [ ] Report generation <30 seconds (90-day window)
- [ ] Executive summary <3 minutes read time
- [ ] Zero PII in output (security tests pass)
- [ ] >90% unit test coverage
- [ ] CLI command working from Cursor
- [ ] All P0 tests still passing (41/41)

---

## 📚 **References**

- **Phase 2.1 (Complete)**: PR #178 - AllocationCalculator implementation
- **weekly_reporter.py**: Existing report generation patterns to reuse
- **Context7 Patterns**: Industry benchmarks (Google SRE, Spotify, Netflix)
- **BLOAT_PREVENTION**: Zero duplication requirement

---

**Status**: Ready for implementation - Begin Task 2.2.1.1 (RED phase)
**Next Step**: Write tests for AllocationReportGenerator

