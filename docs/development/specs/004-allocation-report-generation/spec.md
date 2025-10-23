# Allocation Report Generation - Phase 2.2

**Spec-Kit Format v1.0** | **Status**: Draft | **Owner**: Diego | Engineering Leadership

---

## 📋 **Executive Summary**

**Business Impact**: Enable VPs to understand team allocation in <2 minutes via markdown reports showing L0/L1/L2 breakdown with velocity impact analysis.

**Technical Scope**: Build `AllocationReportGenerator` to create executive-ready markdown reports using the completed `AllocationCalculator` (Phase 2.1).

**Success Criteria**:
- Report generation <30 seconds for 90-day window
- Executive summary comprehensible in <2 minutes
- Command: `/generate-allocation-report --days 90`
- Zero PII/credentials in output

**Foundation**: Built on Phase 2.1 complete implementation
- ✅ AllocationCalculator (18/18 tests passing)
- ✅ TeamAllocation data model
- ✅ Cross-project hierarchy traversal
- ✅ Context7 velocity patterns

---

## 🎯 **Problem Statement**

**Current State**: AllocationCalculator produces data, but no user-facing output.

**Gap**: Leadership needs markdown reports showing:
- Team allocation summary (L0/L1/L2/Other percentages)
- Velocity impact analysis (vs. 30% L0 baseline)
- Historical context (quarter-over-quarter trends)
- Actionable recommendations

**User Need**: VPs want to see allocation reports in leadership-workspace without running Python code directly.

---

## 📊 **Implementation Scope**

### **Phase 2.2: Report Generation** (This Spec)

**Components**:
1. `AllocationReportGenerator` class
2. Markdown report templates (executive summary, team breakdown, recommendations)
3. Integration with leadership-workspace output directory
4. CLI command: `/generate-allocation-report`

**Out of Scope** (Future):
- Historical trend analysis (Phase 3)
- L1→L2 connection mapping (Phase 4)
- Multi-team comparisons (Phase 5)

---

## 🏗️ **Technical Design**

### **Architecture** (BLOAT_PREVENTION Compliant)

```python
# REUSE existing components from Phase 2.1
from .allocation_calculator import AllocationCalculator
from .allocation_models import TeamAllocation
from .jira_reporter import JiraClient, ConfigManager

class AllocationReportGenerator:
    """
    Generate markdown allocation reports

    BLOAT_PREVENTION: Reuses AllocationCalculator, extends ReportGenerator patterns
    Context7: Executive summary format from weekly_reporter.py
    """

    def __init__(self, config: ConfigManager):
        self.config = config
        self.jira_client = JiraClient(config.get_jira_config())

    def generate_report(
        self,
        teams: List[str],
        duration_days: int = 90,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate allocation report for specified teams

        Returns: Path to generated markdown report
        """
        # Calculate allocations
        # Build markdown report
        # Save to leadership-workspace/reports/
        pass
```

### **Report Structure**

```markdown
# Team Allocation Report - 90-Day Rolling Window
**Period**: Jan 1, 2025 - Mar 31, 2025
**Generated**: Oct 23, 2025

---

## 📊 Executive Summary

### Overall Allocation
- **L0 (Operational)**: 35% (5% above baseline)
- **L1 (Enabling)**: 15%
- **L2 (Strategic)**: 45%
- **Other**: 5%

### Velocity Impact
- **Current L2 Velocity**: 8.5 stories/week
- **Projected (at 30% L0)**: 10.2 stories/week
- **Impact**: -16.7% (moderate burden)

### Key Insights
- ⚠️ L0 burden 5% above industry baseline (30%)
- ✅ L2 allocation healthy (45% > 40% target)
- 🎯 Reducing L0 to 30% could increase velocity by 20%

---

## 👥 Team Breakdown

### Web Platform Team
- **Allocation**: L0: 40% | L1: 10% | L2: 45% | Other: 5%
- **Total Issues**: 127 completed
- **L2 Velocity**: 6.2 stories/week (actual) vs 8.5 (projected)
- **Velocity Impact**: -27.1% (high L0 burden)

**Top L0 Work**:
- Production incidents: 25%
- Security patches: 10%
- Compliance (FedRAMP): 5%

**Recommendation**: Consider dedicating on-call rotation to reduce L0 impact on strategic work.

---

## 📈 Context7 Industry Benchmarks

- **Google SRE Target**: <50% toil (operational work)
- **Spotify Innovation Time**: 70-80% strategic work
- **Your Teams**: 45% strategic (room for improvement)

**Target**: Reduce L0 from 35% → 30% to unlock 20% velocity gain.

---

## 🎯 Recommendations

1. **High Priority**: Reduce L0 burden on Web Platform team
   - Current: 40% L0 (10% above baseline)
   - Impact: -27% velocity degradation
   - Action: Implement on-call rotation or hire SRE support

2. **Medium Priority**: Maintain healthy L2 allocation
   - Current: 45% L2 (exceeds 40% target)
   - Continue current strategic work balance

3. **Low Priority**: Monitor "Other" category
   - Current: 5% (acceptable)
   - If grows >10%, investigate classification gaps
```

---

## 📋 **Acceptance Criteria**

**Must Have**:
- [ ] Generate markdown report for single team
- [ ] Generate markdown report for multiple teams
- [ ] Report includes executive summary (<2 min read)
- [ ] Report includes velocity impact analysis
- [ ] Report saves to leadership-workspace/reports/
- [ ] Report generation <30 seconds for 90-day window
- [ ] CLI command `/generate-allocation-report` works
- [ ] Zero PII in output

**Should Have**:
- [ ] Context7 industry benchmarks in report
- [ ] Actionable recommendations based on allocation
- [ ] Top L0 work categories shown
- [ ] Team comparison summary

**Won't Have** (Phase 3+):
- Historical trend charts
- L1→L2 connection mapping
- Cross-quarter comparisons

---

## 🧪 **Testing Strategy**

**Unit Tests**:
- Report generation with mock data
- Markdown formatting validation
- File path handling
- Edge cases (no data, single team)

**Integration Tests**:
- End-to-end report generation with real Jira mock
- CLI command execution
- Output file validation

**Target Coverage**: >90% for new code

---

## 📊 **Success Metrics**

- Report generation time: <30 seconds (90-day window)
- Executive comprehension: <2 minutes to understand
- Adoption: 3+ VPs using reports within 2 weeks
- Zero PII incidents

---

## 🔗 **Dependencies**

**Completed** (Phase 2.1):
- ✅ AllocationCalculator
- ✅ TeamAllocation model
- ✅ Context7 velocity patterns
- ✅ Security (PII prevention)

**Required**:
- Markdown template system
- CLI integration with Cursor
- leadership-workspace write permissions

---

## 🚀 **Implementation Plan**

**Phase 2.2.1**: Report Generation Core (2-3 hours)
- AllocationReportGenerator class
- Markdown template rendering
- File output handling

**Phase 2.2.2**: CLI Integration (1-2 hours)
- `/generate-allocation-report` command
- Argument parsing (teams, days, output)
- Error handling and logging

**Phase 2.2.3**: Polish & Testing (1-2 hours)
- Integration tests
- Documentation
- Performance validation

**Total Estimate**: 4-7 hours

---

## 📚 **References**

- **Phase 2.1 (Complete)**: PR #178 - AllocationCalculator implementation
- **weekly_reporter.py**: Existing report generation patterns to reuse
- **Context7 Patterns**: Industry benchmarks for recommendations
- **BLOAT_PREVENTION**: Zero duplication requirement

---

**Status**: Ready for implementation
**Next Step**: Create `tasks.md` and begin Phase 2.2.1
