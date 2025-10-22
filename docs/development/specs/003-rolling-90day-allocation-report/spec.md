# Rolling 90-Day Team Allocation Report Specification

**Spec-Kit Format v1.0** | **Status**: Draft - Awaiting Approval | **Owner**: Diego | Engineering Leadership

---

## 📋 **Executive Summary**

**Business Impact**: Provides VP Engineering and VP Product with visibility into platform team resource allocation across L0/L1/L2 work, enabling data-driven decisions for $500K+ quarterly resource allocation and realistic capacity planning.

**Technical Scope**: Extends existing `.claudedirector/lib/reporting/weekly_reporter.py` architecture to generate rolling 90-day allocation reports showing percentage breakdown of L0 (keep-the-lights-on), L1 (enabling work), and L2 (strategic initiatives) with velocity impact analysis.

**Success Criteria**:
- VPs understand team allocation in <2 minutes
- Report generation <30 seconds
- Enables identification of teams with >60% L0 burden (crisis threshold)
- No PII/credentials in codebase (security requirement)
- Zero code duplication (BLOAT_PREVENTION compliance)
- Follows PROJECT_STRUCTURE.md placement rules

---

## 🎯 **Problem Statement & Industry Context**

### **Root Cause** (Sequential Thinking Step 1)

**Stakeholder Perception**:
> "Platform teams aren't working on anything" or "Platform teams are working on the wrong things"
> — VP Engineering, VP Product (repeated concern)

**Reality**: Platform teams allocate 60-70% capacity to **invisible L0 work** (security patches, production issues, compliance) that leadership doesn't track. L2 strategic initiatives progress slowly, creating perception of underperformance.

**The Gap**: Leadership lacks visibility into "keep-the-lights-on" work, sets expectations assuming 100% L2 capacity.

### **Context7 Industry Benchmarking**

**Google SRE "Toil Problem"**: SRE teams track "toil percentage" (target: <50% operational work)
**Spotify "Innovation Time"**: Teams track innovation vs. maintenance (target: 20-30% innovation minimum)
**Netflix "Operational Load"**: Platform teams quantify operational burden (target: 30-40% operational, 60-70% strategic)

**Pattern**: Make invisible work visible through quantified allocation data.

---

## 🏗️ **Constitutional Compliance**

### **Simplicity Constraints**
- **Project Count**: 1 project (allocation report generator)
- **Component Count**: 2 components (AllocationCalculator, AllocationReportGenerator)
- **Complexity Justification**: N/A - within simplicity limits

### **Methodology Requirements**
- ✅ **Sequential Thinking**: 6-step methodology applied (problem → design → implementation)
- ✅ **Spec-Kit Format**: Using GitHub Spec-Kit template structure
- ✅ **Security-First**: PII/credentials removed from git history, template-based config
- ✅ **BLOAT_PREVENTION**: REUSE existing `weekly_reporter.py` infrastructure (no duplication)

### **PROJECT_STRUCTURE.md Compliance**
```
.claudedirector/lib/reporting/                    # ✅ Correct location per PROJECT_STRUCTURE.md
├── weekly_reporter.py                            # ✅ EXISTING - REUSE
├── allocation_calculator.py                      # ✅ NEW - L0/L1/L2 calculation logic
└── allocation_report_generator.py                # ✅ NEW - Report generation (extends ReportGenerator)

leadership-workspace/configs/                     # ✅ User territory
├── weekly-report-config.template.yaml            # ✅ EXISTING - EXTEND with allocation queries
└── weekly-report-config.yaml                     # ✅ User config (gitignored)

leadership-workspace/reports/                     # ✅ User territory
└── allocation-report-YYYY-MM-DD.md               # ✅ Generated reports
```

### **BLOAT_PREVENTION_SYSTEM.md Compliance**
- ✅ **DRY Principle**: REUSE existing JiraClient, StrategicAnalyzer, ConfigManager
- ✅ **No Duplication**: Extend existing `_detect_initiative_level()` logic (not duplicate)
- ✅ **Single Source of Truth**: Allocation logic in ONE location (`allocation_calculator.py`)
- ✅ **Import-Based Reuse**: `from .weekly_reporter import JiraClient, StrategicAnalyzer`

---

## 📊 **Functional Requirements**

### **REQ-F1: L0/L1/L2 Allocation Calculation**
**Acceptance Criteria**:
- [ ] Calculate percentage allocation: L0 | L1 | L2 | Other (must sum to 100%)
- [ ] Support rolling date ranges (default: last 90 days, custom start/end dates)
- [ ] Detect L0 work via: labels, keywords, issue type, priority (graceful fallback)
- [ ] Detect L1 work via: parent L2 epic relationships + L1 labels
- [ ] Detect L2 work via: labels, parent epics, strategic keywords
- [ ] Handle inconsistent Jira labeling (multi-factor detection)

### **REQ-F2: Velocity Impact Analysis**
**Acceptance Criteria**:
- [ ] Calculate L2 velocity (issues per week) based on actual allocation
- [ ] Show projected velocity if L2 allocation increased (e.g., 20% → 50%)
- [ ] Identify teams with >60% L0 allocation (crisis threshold)
- [ ] Display velocity comparison: L2 actual vs. if 100% capacity

### **REQ-F3: Executive Report Generation**
**Acceptance Criteria**:
- [ ] Generate markdown report with executive summary
- [ ] Team-by-team allocation breakdown
- [ ] L1→L2 connections (show enabling work supporting strategic initiatives)
- [ ] Actionable recommendations based on allocation data
- [ ] Report generation <30 seconds for 90-day window

### **REQ-F4: Command-Line Interface**
**Acceptance Criteria**:
- [ ] Command: `/generate-allocation-report` (follows weekly report pattern)
- [ ] Default: last 90 days from today
- [ ] Custom range: `--start-date YYYY-MM-DD --end-date YYYY-MM-DD`
- [ ] Preset windows: `--days 30|60|90|180`
- [ ] Custom output: `--output /path/to/report.md`

---

## 🔧 **Non-Functional Requirements**

### **REQ-NF1: Performance**
- Report generation: <30 seconds for 90-day window with 500 issues
- Jira API calls: Batched (100 issues per request), paginated
- Memory usage: <200MB for complete analysis

### **REQ-NF2: Security**
- ❌ No PII in codebase (email addresses, names)
- ❌ No credentials in code (API tokens, passwords)
- ❌ No company-specific data (use placeholders: "[PROJECT-1]")
- ✅ Environment variables for all sensitive data
- ✅ Template configuration files (`.template.yaml`)
- ✅ Actual configs gitignored

### **REQ-NF3: Code Quality**
- DRY Compliance: REUSE existing infrastructure (no duplication)
- SOLID Principles: Single responsibility per class
- Test Coverage: >90% unit test coverage
- Type Hints: Complete type annotations

---

## 🏗️ **Technical Architecture**

### **Component Design** (BLOAT_PREVENTION Compliant)

```python
# ✅ REUSE Existing Components (DRY Compliance)
from .weekly_reporter import (
    JiraClient,              # REUSE - Jira API integration
    StrategicAnalyzer,       # REUSE - L0/L1/L2 detection logic
    ConfigManager,           # REUSE - YAML configuration
    ReportGenerator,         # REUSE - Report building patterns
    JiraIssue,              # REUSE - Data model
    Initiative              # REUSE - Data model
)

# ✅ NEW Components (Minimal Additions)
class AllocationCalculator:
    """
    Calculate team allocation % across L0/L1/L2 work

    REUSE: StrategicAnalyzer._detect_initiative_level() for classification
    DRY: Extends existing detection logic, no duplication
    """
    def __init__(self, strategic_analyzer: StrategicAnalyzer):
        self.analyzer = strategic_analyzer  # Composition over duplication

    def calculate_team_allocation(
        self,
        team_issues: List[JiraIssue],
        date_range: tuple
    ) -> TeamAllocation:
        """Calculate allocation % for team in date range"""
        # REUSE existing _detect_initiative_level() logic
        l0_issues = [i for i in team_issues if self.analyzer._is_l0_work(i)]
        l1_issues = [i for i in team_issues if self.analyzer._is_l1_work(i)]
        l2_issues = [i for i in team_issues if self.analyzer._is_l2_work(i)]

        # Calculate percentages (must sum to 100%)
        total = len(team_issues)
        return TeamAllocation(
            l0_pct=(len(l0_issues) / total) * 100,
            l1_pct=(len(l1_issues) / total) * 100,
            l2_pct=(len(l2_issues) / total) * 100,
            # ... velocity calculations
        )

class AllocationReportGenerator:
    """
    Generate rolling 90-day allocation report

    EXTENDS: ReportGenerator patterns from weekly_reporter.py
    REUSE: ConfigManager, JiraClient, StrategicAnalyzer
    """
    def __init__(
        self,
        config: ConfigManager,
        jira_client: JiraClient,
        analyzer: StrategicAnalyzer
    ):
        self.config = config
        self.jira = jira_client
        self.analyzer = analyzer
        self.calculator = AllocationCalculator(analyzer)  # NEW

    def generate_allocation_report(
        self,
        start_date: datetime,
        end_date: datetime,
        output_path: str
    ) -> str:
        """Generate allocation report - EXTENDS existing patterns"""
        # REUSE existing fetch_issues() patterns
        issues = self.jira.fetch_issues(jql_with_date_range)

        # NEW: Calculate allocations
        allocations = self.calculator.calculate_team_allocation(issues, date_range)

        # REUSE existing report building patterns
        report_content = self._build_allocation_report(allocations)

        return output_path
```

### **Data Flow**
```
1. User runs: /generate-allocation-report --days 90
2. AllocationReportGenerator initialized with REUSED components
3. JiraClient fetches issues in date range (REUSE existing logic)
4. StrategicAnalyzer detects L0/L1/L2 (REUSE _detect_initiative_level)
5. AllocationCalculator calculates percentages
6. ReportGenerator builds markdown (EXTEND existing patterns)
7. Save to leadership-workspace/reports/ (user territory)
```

### **Integration Points** (BLOAT_PREVENTION Compliant)
- **JiraClient**: REUSE existing Jira API integration (no duplicate API logic)
- **StrategicAnalyzer**: REUSE existing L0/L1/L2 detection (no duplicate classification)
- **ConfigManager**: REUSE existing YAML configuration (no duplicate config logic)
- **ReportGenerator**: EXTEND existing markdown generation (no duplicate report logic)

---

## 📊 **Implementation Plan**

### **Phase 1: Data Model & Calculator** (5 days)
**Deliverables**:
- [ ] `TeamAllocation` dataclass with validation
- [ ] `AllocationCalculator` class with L0/L1/L2 detection
- [ ] Unit tests (>90% coverage)

**Success Criteria**:
- Allocation percentages sum to 100% (±0.1% tolerance)
- L0/L1/L2 detection matches manual Jira queries (±5% accuracy)
- All unit tests passing

**Dependencies**: Access to existing `weekly_reporter.py` codebase

### **Phase 2: Report Generator** (5 days)
**Deliverables**:
- [ ] `AllocationReportGenerator` class
- [ ] Executive markdown report template
- [ ] JQL queries extended in config template
- [ ] Integration tests with live Jira data

**Success Criteria**:
- Report generation <30 seconds for 90-day window
- Report comprehensible to VPs in <2 minutes
- Integration tests passing with test Jira environment

**Dependencies**: Phase 1 complete, test Jira environment access

### **Phase 3: CLI & Documentation** (3 days)
**Deliverables**:
- [ ] `/generate-allocation-report` command implementation
- [ ] Security-compliant template configuration files
- [ ] User documentation for VPs
- [ ] Environment variable setup guide

**Success Criteria**:
- Command follows weekly report pattern
- No PII/credentials in codebase (security validated)
- Documentation enables VP self-service

**Dependencies**: Phase 2 complete

---

## 🧪 **Testing Strategy**

### **Unit Tests** (>90% Coverage Required)
```python
# tests/unit/reporting/test_allocation_calculator.py
def test_allocation_percentages_sum_to_100():
    """CRITICAL: Allocation must always sum to 100%"""

def test_l0_detection_with_labels():
    """Test L0 detection using Jira labels"""

def test_l0_detection_with_keywords():
    """Test L0 detection using compliance keywords (graceful fallback)"""

def test_l1_to_l2_connection_mapping():
    """Test L1 enabling work mapped to parent L2 initiatives"""
```

### **Integration Tests**
```python
# tests/integration/test_allocation_report_generation.py
def test_generate_report_with_live_jira_data():
    """End-to-end test with test Jira environment"""

def test_report_generation_performance():
    """Validate <30s generation time for 90-day window"""
```

### **Security Tests**
```python
# tests/security/test_pii_prevention.py
def test_no_pii_in_generated_code():
    """Ensure no email addresses, API tokens, company names in code"""

def test_template_config_uses_placeholders():
    """Validate template config has placeholders, not real data"""
```

---

## 🔒 **Security Requirements** (Git History Clean)

### **PII/Credentials Protection**
- ✅ **Git history cleaned**: BFG Repo-Cleaner removed PII/credentials from 680 commits
- ✅ **API token revoked**: User confirmed Jira API token revoked
- ✅ **Main branch clean**: Force pushed clean history to GitHub

### **Prevention Measures** (Implementation Required)
- [ ] Template configuration file: `weekly-report-config.template.yaml`
- [ ] Environment variables: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
- [ ] Generic examples only: "[PROJECT-1]" not "Web Platform"
- [ ] Pre-commit hook: Block commits with PII/credentials
- [ ] git-secrets: Automated credential detection

---

## 📋 **Review & Acceptance Checklist**

### **Specification Quality**
- [x] Clear problem statement with Context7 industry benchmarking
- [x] Executable specification with acceptance criteria
- [x] Technical architecture with DRY/BLOAT_PREVENTION compliance
- [x] Testing strategy with >90% coverage requirement
- [x] Security requirements with PII/credential protection

### **Constitutional Compliance**
- [x] Simplicity: 1 project, 2 components (within limits)
- [x] Sequential Thinking: 6-step methodology applied
- [x] Spec-Kit Format: GitHub Spec-Kit template structure
- [x] PROJECT_STRUCTURE.md: Correct file placement in `.claudedirector/lib/reporting/`
- [x] BLOAT_PREVENTION_SYSTEM.md: REUSE existing infrastructure, zero duplication

### **Technical Feasibility**
- [x] Solution extends existing `weekly_reporter.py` (DRY)
- [x] Performance requirements achievable (<30s generation)
- [x] Security requirements enforced (no PII in code)
- [x] Integration approach minimizes code duplication

### **Business Alignment**
- [x] Solves VP visibility problem ("make invisible work visible")
- [x] Enables $500K+ quarterly resource allocation decisions
- [x] Success metrics measurable (<2 min comprehension, <30s generation)
- [x] Risk mitigation (tight budget constraints addressed)

---

## 📝 **Approval Status**

**Problem Statement**: ✅ APPROVED (User confirmed: "yes, the problem statement is accurate")
**Technical Design**: ⏳ AWAITING APPROVAL
**Security Compliance**: ✅ APPROVED (Git history clean, PII removed)
**Final Approval**: ⏳ PENDING

---

## 🚀 **Implementation Authorization**

**Ready to Proceed When**:
1. ✅ Problem statement validated (APPROVED)
2. ✅ Security requirements met (APPROVED - git history clean)
3. ⏳ Technical design approved (AWAITING)
4. ⏳ User says "approved" or "proceed"

**Upon Approval, Will Implement**:
1. Create security-compliant template configuration files
2. Implement AllocationCalculator (L0/L1/L2 detection)
3. Implement AllocationReportGenerator (extending weekly reporter)
4. Create `/generate-allocation-report` command
5. Add comprehensive tests (>90% coverage)
6. Document setup with environment variables

---

*This specification follows GitHub Spec-Kit methodology with Sequential Thinking, Context7 benchmarking, PROJECT_STRUCTURE.md compliance, and BLOAT_PREVENTION_SYSTEM.md enforcement.*
