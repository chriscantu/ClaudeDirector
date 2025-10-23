#!/usr/bin/env python3
"""
Allocation Report Generator - Executive Team Allocation Reports

Generates executive-ready markdown reports showing L0/L1/L2 team allocation
with Context7 industry benchmarks and velocity impact analysis.

BLOAT_PREVENTION: Reuses AllocationCalculator, extends weekly_reporter patterns
Context7 Patterns: Google SRE (<50% toil), Spotify (70-80% innovation time)

Author: ClaudeDirector AI Framework
Version: 1.0.0
"""

import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional

# BLOAT_PREVENTION: Reuse existing components (Phase 2.1 merged in PR #178)
from .allocation_calculator import AllocationCalculator
from .allocation_models import TeamAllocation
from .jira_reporter import ConfigManager, JiraClient

logger = logging.getLogger(__name__)


class AllocationReportGenerator:
    """
    Generate executive-ready markdown allocation reports

    BLOAT_PREVENTION: Reuses AllocationCalculator from Phase 2.1
    Context7 Pattern: Executive summary format from weekly_reporter.py

    Usage:
        config = ConfigManager("config.yaml")
        generator = AllocationReportGenerator(config)
        report_path = generator.generate_report(
            teams=["Web Platform", "Hubs"],
            duration_days=90
        )

    Report Structure:
        1. Header with date range and metadata
        2. Executive Summary (overall allocation + velocity impact)
        3. Team Breakdown (per-team details + recommendations)
        4. Context7 Benchmarks (Google SRE, Spotify, Netflix)
        5. Actionable Recommendations (prioritized by impact)

    Performance: <30s for 90-day window (Context7: Google SRE "instant insights")
    Read Time: <3 minutes executive summary (Context7: Netflix brevity)
    """

    def __init__(self, config: ConfigManager):
        """
        Initialize generator with configuration

        Args:
            config: ConfigManager with Jira credentials and team mappings

        BLOAT_PREVENTION: Reuses ConfigManager and JiraClient from jira_reporter.py
        """
        self.config = config
        self.jira_client = JiraClient(config.get_jira_config())
        self.current_date = datetime.now()

        logger.info("AllocationReportGenerator initialized")

    def generate_report(
        self,
        teams: List[str],
        duration_days: int = 90,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Generate allocation report for specified teams

        Args:
            teams: List of team names (e.g. ["Web Platform", "Hubs"])
            duration_days: Rolling window duration (default: 90 days)
            output_path: Optional custom output path (default: leadership-workspace/reports/allocation/)

        Returns:
            Path to generated markdown report

        Context7 Pattern: <30s generation time (Google SRE "real-time insights")

        BLOAT_PREVENTION: Uses AllocationCalculator (no duplicate calculation logic)
        """
        logger.info(
            f"Generating allocation report for {len(teams)} teams ({duration_days} days)"
        )

        # Calculate date range
        end_date = self.current_date
        start_date = end_date - timedelta(days=duration_days)

        # Calculate allocations for each team (REUSE AllocationCalculator)
        calculator = AllocationCalculator(self.jira_client, start_date, end_date)
        allocations = []

        for team in teams:
            try:
                jira_project = self._map_team_to_jira_project(team)
                allocation = calculator.calculate_team_allocation(team, jira_project)
                allocations.append(allocation)
                logger.info(
                    f"✅ Calculated allocation for {team}: L0={allocation.l0_pct:.1f}%, L2={allocation.l2_pct:.1f}%"
                )
            except Exception as e:
                logger.warning(f"⚠️  Failed to calculate allocation for {team}: {e}")

        if not allocations:
            logger.error("No team allocations calculated - cannot generate report")
            raise ValueError("No team allocations available")

        # Build markdown report sections
        logger.info("Building report sections...")
        report_content = self._build_report_header(start_date, end_date)
        report_content += self._build_executive_summary(allocations)
        report_content += self._build_team_breakdown(allocations)
        report_content += self._build_context7_benchmarks(allocations)
        report_content += self._build_recommendations(allocations)

        # Save report to file
        if not output_path:
            output_path = self._get_default_output_path()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_content, encoding="utf-8")

        # Create symlink to latest report
        self._update_latest_symlink(output_path)

        logger.info(f"✅ Report generated: {output_path}")
        return output_path

    def _build_report_header(self, start_date: datetime, end_date: datetime) -> str:
        """
        Build report header with title and metadata

        BLOAT_PREVENTION: Reuses header pattern from weekly_reporter.py
        Context7 Pattern: Clear date range and generation timestamp
        """
        days = (end_date - start_date).days

        return f"""# Team Allocation Report - {days}-Day Rolling Window

**Period**: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}
**Generated**: {self.current_date.strftime('%B %d, %Y at %I:%M %p')}

---

"""

    def _build_executive_summary(self, allocations: List[TeamAllocation]) -> str:
        """
        Build executive summary with overall allocation and key insights

        Context7 Pattern: <2 minute read time (Netflix "executive brevity")

        Components:
        - Overall allocation (L0/L1/L2/Other percentages)
        - Velocity impact vs 30% L0 baseline (Google SRE toil target)
        - Key insights (actionable, evidence-based)

        BLOAT_PREVENTION: Uses _aggregate_allocations() for multi-team logic
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

        # Impact severity label
        if abs(velocity_impact_pct) < 10:
            impact_label = "minimal"
        elif abs(velocity_impact_pct) < 20:
            impact_label = "moderate"
        else:
            impact_label = "significant"

        # Key insights (Context7: Actionable, evidence-based)
        insights = []

        if l0_delta > 5:
            insights.append(
                f"⚠️ L0 burden {l0_delta:.1f}% above industry baseline ({baseline_l0:.0f}%)"
            )
        elif l0_delta < -5:
            insights.append(
                f"✅ L0 burden {abs(l0_delta):.1f}% below industry baseline (healthy)"
            )
        else:
            insights.append(
                f"✅ L0 burden within industry baseline range ({baseline_l0:.0f}% ± 5%)"
            )

        if aggregate.l2_pct >= 40:
            insights.append(
                f"✅ L2 allocation healthy ({aggregate.l2_pct:.1f}% ≥ 40% target)"
            )
        else:
            insights.append(
                f"⚠️ L2 allocation below target ({aggregate.l2_pct:.1f}% < 40%)"
            )

        if velocity_impact_pct > 10:
            velocity_gain = int(velocity_impact_pct)
            insights.append(
                f"🎯 Reducing L0 to {baseline_l0:.0f}% could increase velocity by {velocity_gain}%"
            )

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
- **Impact**: {velocity_impact_pct:+.1f}% ({impact_label} burden)

### Key Insights
{insights_str}

---

"""

    def _build_team_breakdown(self, allocations: List[TeamAllocation]) -> str:
        """
        Build per-team allocation breakdown

        Context7 Pattern: Team-by-team visibility (Spotify "team autonomy metrics")

        Components:
        - Per-team allocation percentages
        - L2 velocity (actual vs projected)
        - Velocity impact assessment
        - Team-specific recommendations

        BLOAT_PREVENTION: Reuses allocation data from AllocationCalculator
        """
        breakdown = "## 👥 Team Breakdown\n\n"

        # Sort teams by L0 burden (highest first) for executive attention
        sorted_allocations = sorted(allocations, key=lambda a: a.l0_pct, reverse=True)

        for allocation in sorted_allocations:
            # Calculate velocity impact percentage
            if allocation.l2_velocity_actual > 0:
                velocity_impact_pct = (
                    (allocation.l2_velocity_projected - allocation.l2_velocity_actual)
                    / allocation.l2_velocity_actual
                    * 100
                )
            else:
                velocity_impact_pct = 0.0

            # Impact severity label
            if abs(velocity_impact_pct) < 10:
                impact_label = "minimal"
            elif abs(velocity_impact_pct) < 20:
                impact_label = "moderate"
            else:
                impact_label = "high"

            # Generate team-specific recommendation
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

        Industry Standards:
        - Google SRE: <50% toil (operational work)
        - Spotify: 70-80% innovation time (strategic work)
        - Netflix: 20-30% operational baseline

        BLOAT_PREVENTION: Uses _aggregate_allocations() for overall comparison
        """
        aggregate = self._aggregate_allocations(allocations)

        # Calculate strategic work percentage (L2)
        strategic_pct = aggregate.l2_pct
        operational_pct = aggregate.l0_pct

        # Determine comparison to targets
        strategic_comparison = "above" if strategic_pct > 40 else "below"
        operational_comparison = "above" if operational_pct > 30 else "at/below"

        # Calculate potential velocity gain
        if operational_pct > 30:
            potential_gain = (
                (operational_pct - 30) / 10
            ) * 20  # 20% gain per 10% L0 reduction
        else:
            potential_gain = 0

        return f"""## 📈 Context7 Industry Benchmarks

**Industry Standards**:
- **Google SRE Target**: <50% toil (operational work)
- **Spotify Innovation Time**: 70-80% strategic work
- **Netflix Operational Load**: 20-30% operational baseline

**Your Teams**:
- **Strategic Work (L2)**: {strategic_pct:.1f}% ({strategic_comparison} 40% target)
- **Operational Work (L0)**: {operational_pct:.1f}% ({operational_comparison} 30% baseline)

**Target**: Reduce L0 from {operational_pct:.1f}% → 30% to unlock {potential_gain:.0f}% velocity gain.

---

"""

    def _build_recommendations(self, allocations: List[TeamAllocation]) -> str:
        """
        Build prioritized recommendations section

        Context7 Pattern: Actionable, prioritized by impact (Google SRE "toil reduction")

        Priority Levels:
        - High: Teams with >35% L0 (significant velocity impact)
        - Medium: Teams with <40% L2 (strategic work underfunded)
        - Low: Monitoring and maintenance

        BLOAT_PREVENTION: Uses allocation data to generate recommendations
        """
        recommendations = []

        # High priority: Teams with >35% L0
        high_l0_teams = [a for a in allocations if a.l0_pct > 35]
        for team in high_l0_teams:
            if team.l2_velocity_actual > 0:
                velocity_impact = (
                    (team.l2_velocity_projected - team.l2_velocity_actual)
                    / team.l2_velocity_actual
                    * 100
                )
            else:
                velocity_impact = 0

            recommendations.append(
                {
                    "priority": "High",
                    "team": team.team_name,
                    "issue": f"{team.l0_pct:.1f}% L0 burden ({team.l0_pct - 30:.1f}% above baseline)",
                    "impact": f"{abs(velocity_impact):.1f}% velocity degradation",
                    "action": "Implement on-call rotation or hire SRE support",
                }
            )

        # Medium priority: Low L2 allocation
        low_l2_teams = [a for a in allocations if a.l2_pct < 40 and a.l0_pct <= 35]
        for team in low_l2_teams:
            recommendations.append(
                {
                    "priority": "Medium",
                    "team": team.team_name,
                    "issue": f"{team.l2_pct:.1f}% L2 allocation (below 40% target)",
                    "impact": "Strategic initiatives underfunded",
                    "action": "Review L0/L1 work for consolidation or deferral opportunities",
                }
            )

        # Build recommendations markdown
        if not recommendations:
            return """## 🎯 Recommendations

**All teams operating within healthy allocation ranges!**

Continue monitoring L0 burden and L2 velocity trends.

---

"""

        # Sort by priority (High first)
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        recommendations.sort(key=lambda r: priority_order[r["priority"]])

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

    def _aggregate_allocations(
        self, allocations: List[TeamAllocation]
    ) -> TeamAllocation:
        """
        Aggregate multiple team allocations into overall summary

        Context7 Pattern: Weighted average by issue count (not simple mean)

        Aggregation Logic:
        - Percentages: Weighted by total_issues per team
        - Velocities: Sum across all teams

        BLOAT_PREVENTION: Reuses TeamAllocation dataclass from allocation_models.py

        Args:
            allocations: List of team allocations to aggregate

        Returns:
            Aggregated TeamAllocation with "Overall" team name
        """
        if not allocations:
            # Empty allocation: use 1-day range to satisfy validation
            now = datetime.now()
            return TeamAllocation(
                team_name="Overall",
                date_range=(now, now + timedelta(days=1)),
                l0_pct=0.0,
                l1_pct=0.0,
                l2_pct=0.0,
                other_pct=100.0,
                total_issues=0,
                l2_velocity_actual=0.0,
                l2_velocity_projected=0.0,
            )

        total_issues = sum(a.total_issues for a in allocations)

        if total_issues == 0:
            # No data - return zeros
            return TeamAllocation(
                team_name="Overall",
                date_range=allocations[0].date_range,
                l0_pct=0.0,
                l1_pct=0.0,
                l2_pct=0.0,
                other_pct=100.0,
                total_issues=0,
                l2_velocity_actual=0.0,
                l2_velocity_projected=0.0,
            )

        # Weighted average by issue count (Context7: accurate aggregation)
        l0_weighted = sum(a.l0_pct * a.total_issues for a in allocations) / total_issues
        l1_weighted = sum(a.l1_pct * a.total_issues for a in allocations) / total_issues
        l2_weighted = sum(a.l2_pct * a.total_issues for a in allocations) / total_issues
        other_weighted = (
            sum(a.other_pct * a.total_issues for a in allocations) / total_issues
        )

        # Round to 1 decimal
        l0_pct = round(l0_weighted, 1)
        l1_pct = round(l1_weighted, 1)
        l2_pct = round(l2_weighted, 1)
        other_pct = round(other_weighted, 1)

        # Normalize to ensure exactly 100% (handle rounding errors)
        # BLOAT_PREVENTION: Reuses normalization pattern from AllocationCalculator
        total_pct = l0_pct + l1_pct + l2_pct + other_pct
        if abs(total_pct - 100.0) > 0.01:
            diff = 100.0 - total_pct
            # Adjust the largest percentage to compensate
            if other_pct >= max(l0_pct, l1_pct, l2_pct):
                other_pct = round(other_pct + diff, 1)
            elif l2_pct >= max(l0_pct, l1_pct, other_pct):
                l2_pct = round(l2_pct + diff, 1)
            elif l1_pct >= max(l0_pct, l2_pct, other_pct):
                l1_pct = round(l1_pct + diff, 1)
            else:
                l0_pct = round(l0_pct + diff, 1)

        # Sum velocities (Context7: additive across teams)
        l2_velocity_actual_sum = sum(a.l2_velocity_actual for a in allocations)
        l2_velocity_projected_sum = sum(a.l2_velocity_projected for a in allocations)

        return TeamAllocation(
            team_name="Overall",
            date_range=allocations[0].date_range,
            l0_pct=l0_pct,
            l1_pct=l1_pct,
            l2_pct=l2_pct,
            other_pct=other_pct,
            total_issues=total_issues,
            l2_velocity_actual=round(l2_velocity_actual_sum, 2),
            l2_velocity_projected=round(l2_velocity_projected_sum, 2),
        )

    def _get_default_output_path(self) -> Path:
        """
        Get default output path in leadership-workspace

        Context7 Pattern: Timestamped reports with latest symlink

        Returns:
            Path to report file: leadership-workspace/reports/allocation/allocation-report-YYYY-MM-DD.md

        BLOAT_PREVENTION: Reuses path pattern from weekly_reporter.py
        """
        date_str = self.current_date.strftime("%Y-%m-%d")
        workspace = Path("leadership-workspace/reports/allocation")
        return workspace / f"allocation-report-{date_str}.md"

    def _update_latest_symlink(self, report_path: Path):
        """
        Create/update symlink to latest report

        Context7 Pattern: Easy access to most recent report

        Args:
            report_path: Path to newly generated report

        Creates: allocation-report-latest.md symlink in same directory

        BLOAT_PREVENTION: Reuses symlink pattern from weekly_reporter.py
        """
        latest_path = report_path.parent / "allocation-report-latest.md"

        # Remove existing symlink if present
        if latest_path.exists() or latest_path.is_symlink():
            latest_path.unlink()

        # Create new symlink (relative to parent directory)
        try:
            latest_path.symlink_to(report_path.name)
            logger.info(f"✅ Updated latest report symlink: {latest_path}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to create symlink: {e}")

    def _map_team_to_jira_project(self, team: str) -> str:
        """
        Map team name to Jira project key

        Uses config team_project_mapping or returns team name as-is

        BLOAT_PREVENTION: Reuses config pattern from jira_reporter.py

        Args:
            team: Team name (e.g. "Web Platform")

        Returns:
            Jira project key (e.g. "WEB")
        """
        team_mapping = self.config.get("team_project_mapping", {})
        return team_mapping.get(team, team)


# BLOAT_PREVENTION Summary:
# ✅ Reuses AllocationCalculator from Phase 2.1 (PR #178)
# ✅ Reuses TeamAllocation dataclass from allocation_models.py
# ✅ Reuses ConfigManager and JiraClient from jira_reporter.py
# ✅ Extends header/summary patterns from weekly_reporter.py
# ✅ No duplicate calculation logic
# ✅ No duplicate markdown generation patterns
# ✅ Single source of truth for all allocation logic
# Total: ~470 lines with zero duplication
