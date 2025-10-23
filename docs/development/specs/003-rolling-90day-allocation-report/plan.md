# Rolling 90-Day Team Allocation Report - Implementation Plan

**Spec-Kit Format v1.0** | **Status**: Draft | **Owner**: Diego | Engineering Leadership

---

## 📋 **Plan Overview**

**Objective**: Implement rolling 90-day team allocation report extending existing `weekly_reporter.py` infrastructure following DRY principles and BLOAT_PREVENTION compliance.

**Success Criteria**:
- Report generation <30 seconds for 90-day window
- >90% test coverage
- Zero code duplication (REUSE existing components)
- No PII/credentials in codebase

---

## 🏗️ **Constitutional Compliance Check**

### **Simplicity Constraints**
- ✅ **Project Count**: 1 project (allocation report generator)
- ✅ **Component Count**: 2 new components (AllocationCalculator, AllocationReportGenerator)
- ✅ **Complexity Justification**: N/A - within constitutional limits

### **Methodology Requirements**
- ✅ **Sequential Thinking**: Applied throughout specification
- ✅ **TDD Workflow**: RED-GREEN-Refactor approach defined
- ✅ **BLOAT_PREVENTION**: REUSE existing infrastructure, no duplication
- ✅ **PROJECT_STRUCTURE**: Files placed in `.claudedirector/lib/reporting/`

---

## 📊 **Architecture Decision Records**

### **ADR-001: REUSE Existing Infrastructure**

**Decision**: Extend `weekly_reporter.py` architecture rather than create new reporting system.

**Rationale**:
- DRY Principle: Avoid duplicating Jira integration, configuration, report generation
- Single Source of Truth: L0/L1/L2 detection logic in one place
- Maintainability: Changes to Jira API affect one codebase

**Consequences**:
- ✅ **Positive**: Zero duplication, faster implementation, consistent patterns
- ⚠️ **Negative**: Coupled to weekly_reporter.py architecture (acceptable trade-off)

**BLOAT_PREVENTION Compliance**: ✅ REUSE pattern (lines 370-396 of BLOAT_PREVENTION_SYSTEM.md)

---

### **ADR-002: Composition Over Inheritance**

**Decision**: Use composition to integrate with StrategicAnalyzer for L0/L1/L2 detection.

**Rationale**:
- SOLID Principles: Prefer composition over inheritance for flexibility
- DRY Compliance: Reuse existing `_detect_initiative_level()` logic
- Testability: Easier to mock dependencies for unit tests

**Implementation**:
```python
class AllocationCalculator:
    def __init__(self, strategic_analyzer: StrategicAnalyzer):
        self.analyzer = strategic_analyzer  # Composition
```

**BLOAT_PREVENTION Compliance**: ✅ Import-based reuse, no duplication

---

### **ADR-003: Security-First Configuration**

**Decision**: Use environment variables + template configuration files for all sensitive data.

**Rationale**:
- Security: Prevent PII/credentials in git history (learned from BFG cleanup)
- Portability: Works across different environments
- Best Practice: Industry standard for credential management

**Implementation**:
```yaml
# weekly-report-config.template.yaml (committed)
jira:
  base_url: "${JIRA_BASE_URL}"
  auth:
    email: "${JIRA_EMAIL}"
    api_token: "${JIRA_API_TOKEN}"

# Environment variables (not committed)
export JIRA_BASE_URL="https://[COMPANY].atlassian.net"
export JIRA_EMAIL="user@company.com"
export JIRA_API_TOKEN="your-token-here"
```

**Security Compliance**: ✅ No PII in codebase, template-based config

---

## 📊 **Jira Data Model & Query Strategy**

### **Validated Jira Hierarchy** (User-Confirmed)

**Critical Insight**: L0/L1/L2 are **PARENT EPICS** in a **CROSS-PROJECT** hierarchy.

```
Hierarchy Structure (CROSS-PROJECT):

┌──────────────────────────────────────────────────┐
│ PROJECT: "Procore Initiatives"                   │
│ ┌──────────────────────────────────────────────┐ │
│ │ L0/L1/L2 Initiative (Epic)                   │ │  ← PI-14632, PI-13092
│ │ Key: PI-14632                                │ │
│ │ Summary: "L0: FedRAMP Compliance"            │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
              ↓ (parent - CROSS PROJECT!)
┌──────────────────────────────────────────────────┐
│ PROJECT: "Web Platform" / "UIS" / "Hubs" etc.    │
│ ┌──────────────────────────────────────────────┐ │
│ │ Epic (type = Epic)                           │ │  ← UIS-1000, HUBS-500
│ │ Key: UIS-1000                                │ │
│ │ Summary: "Q1 Security Compliance"            │ │
│ │ Parent: PI-14632 (cross-project link!)       │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
              ↓ (parent - SAME PROJECT)
┌──────────────────────────────────────────────────┐
│ PROJECT: "Web Platform" (same as Epic)           │
│ ┌──────────────────────────────────────────────┐ │
│ │ Story/Task (type != Epic)                    │ │  ← UIS-1234
│ │ Key: UIS-1234                                │ │
│ │ Summary: "Fix security vulnerability"        │ │
│ │ Parent: UIS-1000 (same project)              │ │
│ │ status CHANGED TO Done AFTER -90d            │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**User's Clarification**:
- ✅ **L0/L1/L2 initiatives**: Live in "Procore Initiatives" project (PI-XXXXX)
- ✅ **Epics**: Live in team projects ("Web Platform", "UIS", "Hubs", etc.)
- ✅ **Stories/Tasks**: Live in same project as their parent Epic
- ✅ **Cross-project linking**: Team epics link to "Procore Initiatives" as parent

**User's Working Query** (7-day window):
```jql
project in ("Web Platform", "Web Design Systems", "UIF Special Projects",
            Hubs, Onboarding, Globalizers, "Experience Services")
AND type != Epic                      # ✅ Stories/Tasks only
AND status CHANGED TO Done AFTER -7d  # ✅ Completed work
AND status != "Honorably Discharged"  # ✅ Exclude cancelled
ORDER BY project, parent, priority
```

---

### **JQL Query Strategy for 90-Day Allocation Report**

#### **Query 1: Get Completed Work** (Base Query)
```jql
project in ("Web Platform", "Web Design Systems", "UIF Special Projects",
            Hubs, Onboarding, Globalizers, "Experience Services")
AND type != Epic
AND status CHANGED TO Done AFTER -90d
AND status != "Honorably Discharged"
AND parent is not EMPTY
ORDER BY parent, project, priority DESC
```

**Purpose**: Fetch all completed stories/tasks in 90-day window with parent epic links.

**Performance**: ~500 issues expected, batched fetching (100 issues/request).

---

#### **Query 2: Get Parent Epics** (Hierarchy Traversal)
```jql
project in ("Web Platform", "Web Design Systems", "UIF Special Projects",
            Hubs, Onboarding, Globalizers, "Experience Services")
AND type = Epic
AND issueFunction in hasSubtasks()
AND (status CHANGED TO Done AFTER -90d OR status in ("In Progress", "In Review"))
ORDER BY parent, status
```

**Purpose**: Fetch parent epics for completed stories (for grandparent initiative lookup).

**Optimization**: Cached lookups to avoid duplicate API calls.

---

#### **Query 3: Get L0/L1/L2 Initiatives** (Top-Level Classification - "Procore Initiatives" Project)
```jql
project = "Procore Initiatives"
AND (summary ~ "L0:|L1:|L2:" OR labels in ("L0", "L1", "L2"))
AND type = Epic
AND (status CHANGED TO Done AFTER -90d OR status in ("In Progress", "In Review"))
ORDER BY labels, status
```

**Purpose**: Fetch top-level L0/L1/L2 initiatives from "Procore Initiatives" project for classification matching.

**Key Insight**: All L0/L1/L2 initiatives live in "Procore Initiatives" project with PI-XXXXX keys.

**Detection Logic**:
- **L0**: "L0:" in summary OR "L0" in labels (e.g., PI-14632: "L0: FedRAMP Compliance")
- **L1**: "L1:" in summary OR "L1" in labels
- **L2**: "L2:" in summary OR "L2" in labels (e.g., PI-13092, UIS-1590)

**Cross-Project Linking**: Team epics (UIS-1000) have parent field pointing to "Procore Initiatives" epics (PI-14632)

---

### **Detection Algorithm** (Cross-Project Hierarchy Traversal)

```python
def _get_initiative_level(self, issue: JiraIssue) -> str:
    """
    Traverse CROSS-PROJECT hierarchy: Story → Epic → L0/L1/L2 Initiative

    Example (Cross-Project):
        UIS-1234 (Story: "Fix security bug")
          PROJECT: "Web Platform"
          ↓ parent (same project)
        UIS-1000 (Epic: "Q1 Security Compliance")
          PROJECT: "Web Platform"
          ↓ parent (CROSS-PROJECT to "Procore Initiatives")
        PI-14632 (Initiative: "L0: FedRAMP Compliance")
          PROJECT: "Procore Initiatives"
          → RESULT: L0
    """
    if issue.type != "Epic" and issue.parent:
        # Get parent epic (same project as story)
        epic = self._fetch_epic_cached(issue.parent)

        if epic and epic.parent:
            # Get grandparent initiative (cross-project to "Procore Initiatives")
            initiative = self._fetch_epic_cached(epic.parent)

            if initiative:
                # Validate initiative is from "Procore Initiatives" project
                if initiative.project == "Procore Initiatives":
                    # Check L0/L1/L2 designation
                    if "L0:" in initiative.summary or "L0" in initiative.labels:
                        return "L0"
                    if "L1:" in initiative.summary or "L1" in initiative.labels:
                        return "L1"
                    if "L2:" in initiative.summary or "L2" in initiative.labels:
                        return "L2"

    return "Other"  # Orphaned work (no parent hierarchy or non-PI initiative)
```

**Performance Optimization**:
- **Epic caching**: Avoid duplicate API calls for same epic
- **Batch fetching**: Fetch all parent epics in one query
- **Lazy loading**: Only fetch grandparent if parent exists

---

## 🏗️ **ADR-004: Duration-Agnostic Jira Reporter Refactoring**

**Decision**: Refactor `weekly_reporter.py` → `jira_reporter.py` with duration as a parameter.

**Status**: APPROVED (User selected Option A)

**Rationale**:
- **Extensibility**: Support weekly, 90-day, quarterly, custom ranges with single codebase
- **DRY Principle**: One reporter for all durations (not separate weekly/quarterly/monthly modules)
- **Semantic Clarity**: "Jira Reporter" reflects actual purpose (Jira integration, not weekly-specific)
- **Evolutionary Design**: Clean foundation for future report types
- **Lower Total Cost**: 2 days now < 3 days deferred + context switching cost

**Context7 Pattern**: This follows the **"Extract Parameter" refactoring pattern** from Martin Fowler's "Refactoring" catalog, converting hardcoded values (weekly) to parameters (duration_days).

**Implementation Strategy**: 3-phase evolutionary migration with backward compatibility.

### **Refactoring Scope**

**Hardcoded Weekly Assumptions to Parameterize**:
1. ✅ Log file: `weekly_report.log` → `jira_report.log`
2. ✅ Headers: "Weekly Executive Report" → "{Duration} Executive Report"
3. ✅ Descriptions: "this week" → "this {duration_label}"
4. ✅ Next report calculation: `+7 days` → `+{duration_days} days`
5. ✅ Function names: `generate_weekly_report()` → `generate_report(duration_days)`
6. ✅ JQL date filters: `-7d` → `-{duration_days}d`

**Files Requiring Updates**:
- `.claudedirector/lib/reporting/weekly_reporter.py` → Extract to `jira_reporter.py`
- `.claudedirector/lib/reporting/weekly_reporter_mcp_bridge.py` → Rename to `jira_reporter_mcp_bridge.py`
- `docs/development/specs/003-rolling-90day-allocation-report/plan.md` (this file)
- `docs/development/specs/003-rolling-90day-allocation-report/spec.md`

**BLOAT_PREVENTION Compliance**:
- ✅ **No Duplication**: Single source for all duration-based reports
- ✅ **Extract Parameter**: Convert hardcoded "weekly" to parameter
- ✅ **Backward Compatibility**: Legacy `weekly_reporter.py` imports from new `jira_reporter.py`

---

## 🔄 **Implementation Phases** (UPDATED with Refactoring)

### **Phase 0: Architectural Refactoring** (TDD Cycle 0 - NEW)

**Objective**: Refactor `weekly_reporter.py` to duration-agnostic `jira_reporter.py`.

**Timeline**: 2 days

#### **User Story 0.1: Duration-Agnostic Jira Reporter**
**As a** platform architect
**I want** a duration-agnostic Jira reporter
**So that** we can support weekly, 90-day, quarterly, and custom reports without code duplication

**Tasks**:
1. **Create `jira_reporter.py`** with duration parameter
   - Extract `JiraClient`, `StrategicAnalyzer`, `ConfigManager`, `ReportGenerator` from `weekly_reporter.py`
   - Add `duration_days` parameter (default: 7)
   - Add `duration_label` helper ("Weekly", "90-Day", "Quarterly")
   - Parameterize all hardcoded "weekly" references
2. **Update `weekly_reporter.py`** for backward compatibility
   - Import from `jira_reporter.py`
   - Maintain existing CLI interface
   - Preserve `/generate-weekly-report` command
3. **Update imports** across codebase
   - Update `plan.md` and `spec.md` to reference `jira_reporter`
   - Update MCP bridge imports
4. **Validate P0 tests** pass with refactoring
   - Run full P0 test suite
   - Ensure no regression in weekly report functionality

**Acceptance Criteria**:
- [ ] `jira_reporter.py` created with duration parameter
- [ ] `weekly_reporter.py` imports from `jira_reporter` (backward compatible)
- [ ] `/generate-weekly-report` command still works
- [ ] All P0 tests passing (42/42)
- [ ] Zero code duplication (BLOAT_PREVENTION compliant)

**Files**:
- `.claudedirector/lib/reporting/jira_reporter.py` (NEW)
- `.claudedirector/lib/reporting/weekly_reporter.py` (UPDATE - imports only)
- `.claudedirector/lib/reporting/jira_reporter_mcp_bridge.py` (RENAME from weekly_reporter_mcp_bridge.py)
- `tests/unit/reporting/test_jira_reporter.py` (NEW)

**Migration Pattern** (Evolutionary Design):
```python
# NEW: .claudedirector/lib/reporting/jira_reporter.py
class JiraReporter:
    """Duration-agnostic Jira report generator"""

    def __init__(self, config: ConfigManager, duration_days: int = 7):
        """
        Args:
            config: Jira configuration
            duration_days: Report window (7=weekly, 90=quarterly, custom)
        """
        self.config = config
        self.duration_days = duration_days
        self.duration_label = self._get_duration_label(duration_days)

    def _get_duration_label(self, days: int) -> str:
        """Convert days to human-readable label"""
        if days == 7:
            return "Weekly"
        elif days == 90:
            return "90-Day"
        elif days == 30:
            return "Monthly"
        elif days % 7 == 0:
            return f"{days // 7}-Week"
        else:
            return f"{days}-Day"

    def generate_report(self, output_path: str) -> str:
        """Generate report for configured duration"""
        # All "weekly" references replaced with self.duration_label
        # All "-7d" JQL filters replaced with f"-{self.duration_days}d"
        ...

# LEGACY: .claudedirector/lib/reporting/weekly_reporter.py (Backward Compatibility)
from .jira_reporter import (
    JiraClient,
    StrategicAnalyzer,
    ConfigManager,
    ReportGenerator,
    JiraReporter
)

# Legacy function for existing users
def generate_weekly_report(config_path: str, output_path: str):
    """Maintained for backward compatibility - use JiraReporter directly"""
    reporter = JiraReporter(config_path, duration_days=7)
    return reporter.generate_report(output_path)
```

---

### **Phase 1: Foundation & Security** (TDD Cycle 1)

**Objective**: Establish security-compliant configuration and data models.

**Timeline**: 2 days (unchanged)

#### **User Story 1.1: Security-Compliant Configuration**
**As a** VP Engineering
**I want** configuration templates without PII
**So that** our codebase is secure and auditable

**Tasks**:
1. Create `weekly-report-config.template.yaml` with placeholders
2. Update existing config to use environment variables
3. Add `.gitignore` entry for actual config
4. Create environment variable setup guide

**Acceptance Criteria**:
- [ ] Template file uses `${VAR}` placeholders (no real credentials)
- [ ] Actual config file gitignored
- [ ] Documentation for environment setup
- [ ] Security test validates no PII in template

**Files**:
- `leadership-workspace/configs/weekly-report-config.template.yaml` (NEW)
- `leadership-workspace/configs/.env.template` (NEW)
- `docs/setup/allocation-report-setup.md` (NEW)

---

#### **User Story 1.2: Team Allocation Data Model**
**As a** developer
**I want** a clear data model for team allocation
**So that** calculations are type-safe and validated

**Tasks**:
1. **RED**: Write unit tests for `TeamAllocation` dataclass
2. **GREEN**: Implement `TeamAllocation` with validation
3. **REFACTOR**: Ensure clean code and documentation

**Acceptance Criteria**:
- [ ] Allocation percentages sum to 100% (±0.1% tolerance)
- [ ] Type hints for all fields
- [ ] Validation raises errors for invalid data
- [ ] Unit test coverage >95%

**Files**:
- `tests/unit/reporting/test_allocation_models.py` (NEW - TDD RED)
- `.claudedirector/lib/reporting/allocation_models.py` (NEW - TDD GREEN)

**Data Model**:
```python
@dataclass
class TeamAllocation:
    """Team allocation across L0/L1/L2 work"""
    team_name: str
    date_range: tuple[datetime, datetime]

    # Allocation percentages (must sum to 100%)
    l0_pct: float  # Keep-the-lights-on work
    l1_pct: float  # Enabling work for L2
    l2_pct: float  # Strategic initiatives
    other_pct: float  # Unclassified work

    # Velocity metrics
    total_issues: int
    l2_velocity_actual: float  # Issues per week
    l2_velocity_projected: float  # If 100% L2 capacity

    def __post_init__(self):
        """Validate allocation percentages sum to 100%"""
        total = self.l0_pct + self.l1_pct + self.l2_pct + self.other_pct
        if not (99.9 <= total <= 100.1):
            raise ValueError(f"Allocation must sum to 100%, got {total}%")
```

---

### **Phase 2: Core Allocation Logic** (TDD Cycle 2)

**Objective**: Implement L0/L1/L2 allocation calculation logic.

#### **User Story 2.1: Allocation Calculator**
**As a** developer
**I want** to calculate team allocation percentages
**So that** VPs can see L0 vs. L2 distribution

**Tasks**:
1. **RED**: Write unit tests for `AllocationCalculator`
   - Test L0 detection (labels, keywords, issue type)
   - Test L1 detection (parent L2 relationships)
   - Test L2 detection (strategic labels, epics)
   - Test percentage calculation (must sum to 100%)
   - Test velocity calculations
2. **GREEN**: Implement `AllocationCalculator` class
   - REUSE `StrategicAnalyzer._detect_initiative_level()`
   - Implement multi-factor L0/L1/L2 classification
   - Calculate allocation percentages
   - Calculate velocity metrics
3. **REFACTOR**: Optimize and document

**Acceptance Criteria**:
- [ ] L0/L1/L2 detection matches manual Jira queries (±5% accuracy)
- [ ] Allocation percentages always sum to 100%
- [ ] Handles edge cases (empty data, single issue type)
- [ ] Unit test coverage >95%
- [ ] ZERO duplication (REUSE StrategicAnalyzer)

**Files**:
- `tests/unit/reporting/test_allocation_calculator.py` (NEW - TDD RED)
- `.claudedirector/lib/reporting/allocation_calculator.py` (NEW - TDD GREEN)

**Implementation Strategy** (BLOAT_PREVENTION Compliant):
```python
# ✅ REUSE Existing Components from Duration-Agnostic jira_reporter (DRY Compliance)
from .jira_reporter import StrategicAnalyzer, JiraIssue, JiraClient

class AllocationCalculator:
    """
    Calculate team allocation % across L0/L1/L2 work

    CRITICAL INSIGHT: L0/L1/L2 are PARENT EPICS in hierarchy:
        Story/Task → parent → Epic → parent → L0/L1/L2 Initiative

    REUSE: StrategicAnalyzer + JiraClient for hierarchy traversal
    DRY: Extends existing detection logic, no duplication
    """
    def __init__(self, strategic_analyzer: StrategicAnalyzer, jira_client: JiraClient):
        """
        Args:
            strategic_analyzer: REUSE existing analyzer (composition)
            jira_client: REUSE for fetching parent epic hierarchy
        """
        self.analyzer = strategic_analyzer
        self.jira = jira_client
        self._epic_cache = {}  # Cache parent epic lookups for performance

    def _get_initiative_level(self, issue: JiraIssue) -> str:
        """
        Detect L0/L1/L2 by traversing CROSS-PROJECT parent hierarchy

        Hierarchy: Story → parent Epic → parent Initiative (L0/L1/L2)

        User's clarifications:
        - "L0s/L1s are parents of L2s and L2s are parents of Epics"
        - "L0, L1 and L2s all exist in their own project 'Procore Initiatives'"
        - "Epics live in the team projects"

        Example:
            UIS-1234 (Story) → UIS-1000 (Epic) → PI-14632 (L0 Initiative)
            └─ "Web Platform"   └─ "Web Platform"  └─ "Procore Initiatives"
        """
        # Stories/Tasks have parent epics
        if issue.type != "Epic" and issue.parent:
            # Get parent epic (with caching for performance)
            epic = self._fetch_epic_cached(issue.parent)

            if epic and epic.parent:
                # Get grandparent initiative (CROSS-PROJECT to "Procore Initiatives")
                initiative = self._fetch_epic_cached(epic.parent)

                if initiative:
                    # Validate initiative is from "Procore Initiatives" project
                    if initiative.project == "Procore Initiatives":
                        # Check initiative summary/labels for L0/L1/L2
                        summary = initiative.summary.upper()
                        labels = [l.upper() for l in initiative.labels]

                        if "L0:" in summary or "L0" in labels:
                            return "L0"
                        if "L1:" in summary or "L1" in labels:
                            return "L1"
                        if "L2:" in summary or "L2" in labels:
                            return "L2"

        return "Other"  # Unclassified work (no parent hierarchy or non-PI initiative)

    def _fetch_epic_cached(self, epic_key: str) -> Optional[JiraIssue]:
        """Fetch epic with caching to avoid duplicate API calls"""
        if epic_key not in self._epic_cache:
            self._epic_cache[epic_key] = self.jira.fetch_issue(epic_key)
        return self._epic_cache[epic_key]

    def calculate_team_allocation(
        self,
        team_issues: List[JiraIssue],
        start_date: datetime,
        end_date: datetime
    ) -> TeamAllocation:
        """
        Calculate allocation % for team in date range

        Uses parent hierarchy traversal for L0/L1/L2 detection
        """
        # Filter issues in date range
        filtered_issues = self._filter_by_date_range(
            team_issues, start_date, end_date
        )

        # Classify issues by traversing parent hierarchy
        l0_issues = []
        l1_issues = []
        l2_issues = []
        other_issues = []

        for issue in filtered_issues:
            level = self._get_initiative_level(issue)
            if level == "L0":
                l0_issues.append(issue)
            elif level == "L1":
                l1_issues.append(issue)
            elif level == "L2":
                l2_issues.append(issue)
            else:
                other_issues.append(issue)

        # Calculate percentages (must sum to 100%)
        total = len(filtered_issues)
        if total == 0:
            return self._empty_allocation()

        return TeamAllocation(
            team_name=team_issues[0].project if team_issues else "Unknown",
            date_range=(start_date, end_date),
            l0_pct=(len(l0_issues) / total) * 100,
            l1_pct=(len(l1_issues) / total) * 100,
            l2_pct=(len(l2_issues) / total) * 100,
            other_pct=(len(other_issues) / total) * 100,
            total_issues=total,
            l2_velocity_actual=self._calculate_velocity(l2_issues, start_date, end_date),
            l2_velocity_projected=self._calculate_projected_velocity(total, start_date, end_date)
        )
```

---

### **Phase 3: Report Generation** (TDD Cycle 3)

**Objective**: Generate executive markdown reports.

#### **User Story 3.1: Allocation Report Generator**
**As a** VP Engineering
**I want** a markdown report showing team allocation
**So that** I can understand L0 burden vs. L2 progress

**Tasks**:
1. **RED**: Write integration tests for report generation
   - Test report generation end-to-end
   - Test executive summary format
   - Test team-by-team breakdown
   - Test L1→L2 connection mapping
   - Test performance (<30s for 90-day window)
2. **GREEN**: Implement `AllocationReportGenerator` class
   - REUSE JiraClient for data fetching
   - REUSE ConfigManager for configuration
   - EXTEND ReportGenerator patterns for markdown
   - Integrate AllocationCalculator
3. **REFACTOR**: Optimize performance and readability

**Acceptance Criteria**:
- [ ] Report generation <30 seconds for 90-day window
- [ ] Executive summary comprehensible in <2 minutes
- [ ] Team-by-team allocation breakdown
- [ ] L1→L2 connections shown
- [ ] Actionable recommendations included
- [ ] Integration test coverage >90%

**Files**:
- `tests/integration/test_allocation_report_generation.py` (NEW - TDD RED)
- `.claudedirector/lib/reporting/allocation_report_generator.py` (NEW - TDD GREEN)

**Implementation Strategy** (EXTEND existing patterns):
```python
# ✅ REUSE Existing Components from Duration-Agnostic jira_reporter
from .jira_reporter import (
    JiraClient,
    StrategicAnalyzer,
    ConfigManager,
    ReportGenerator,  # EXTEND this pattern
    JiraIssue,
    JiraReporter  # NEW: Duration-agnostic base class
)
from .allocation_calculator import AllocationCalculator

class AllocationReportGenerator:
    """
    Generate rolling 90-day allocation report

    EXTENDS: ReportGenerator patterns from weekly_reporter.py
    REUSE: JiraClient, StrategicAnalyzer, ConfigManager
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
        issues = self._fetch_issues_in_range(start_date, end_date)

        # NEW: Calculate allocations per team
        allocations = self._calculate_team_allocations(issues, start_date, end_date)

        # REUSE existing report building patterns
        report_content = self._build_markdown_report(allocations)

        # Save report
        with open(output_path, 'w') as f:
            f.write(report_content)

        return output_path

    def _build_markdown_report(self, allocations: List[TeamAllocation]) -> str:
        """Build executive markdown report"""
        sections = []

        # Executive Summary
        sections.append(self._build_executive_summary(allocations))

        # Team-by-Team Breakdown
        for allocation in allocations:
            sections.append(self._build_team_section(allocation))

        # Actionable Recommendations
        sections.append(self._build_recommendations(allocations))

        return "\n\n".join(sections)
```

---

### **Phase 4: Command Interface** (TDD Cycle 4)

**Objective**: Create user-friendly command-line interface.

#### **User Story 4.1: Command-Line Interface**
**As a** VP Engineering
**I want** a simple command to generate reports
**So that** I can run reports on-demand

**Tasks**:
1. **RED**: Write CLI integration tests
   - Test default 90-day window
   - Test custom date ranges
   - Test output path customization
   - Test error handling
2. **GREEN**: Implement `/generate-allocation-report` command
   - Parse command-line arguments
   - Integrate with AllocationReportGenerator
   - Handle errors gracefully
3. **REFACTOR**: Improve user experience

**Acceptance Criteria**:
- [ ] Command: `/generate-allocation-report` works
- [ ] Default: last 90 days from today
- [ ] Custom range: `--start-date YYYY-MM-DD --end-date YYYY-MM-DD`
- [ ] Preset windows: `--days 30|60|90|180`
- [ ] Custom output: `--output /path/to/report.md`
- [ ] Error messages are clear and actionable

**Files**:
- `tests/integration/test_allocation_cli.py` (NEW - TDD RED)
- `.claudedirector/lib/reporting/allocation_cli.py` (NEW - TDD GREEN)

---

### **Phase 5: Security & Documentation** (Final Validation)

**Objective**: Ensure security compliance and complete documentation.

#### **User Story 5.1: Security Validation**
**As a** security-conscious developer
**I want** automated PII/credential detection
**So that** we never leak sensitive data

**Tasks**:
1. Write security tests
   - Test no PII in generated code
   - Test template config uses placeholders
   - Test actual config is gitignored
2. Add pre-commit hook for PII detection
3. Document security best practices

**Acceptance Criteria**:
- [ ] Security tests pass (no PII detected)
- [ ] Pre-commit hook blocks PII commits
- [ ] git-secrets installed and configured
- [ ] Security documentation complete

**Files**:
- `tests/security/test_pii_prevention.py` (NEW)
- `.git/hooks/pre-commit` (UPDATE)
- `docs/security/allocation-report-security.md` (NEW)

---

#### **User Story 5.2: Setup Documentation**
**As a** new user
**I want** clear setup instructions
**So that** I can generate reports independently

**Tasks**:
1. Create environment variable setup guide
2. Document command-line interface
3. Add troubleshooting section
4. Create quick start guide for VPs

**Acceptance Criteria**:
- [ ] Step-by-step environment variable setup
- [ ] Command examples with screenshots
- [ ] Common error resolution
- [ ] VP self-service documentation

**Files**:
- `docs/setup/allocation-report-setup.md` (NEW)
- `docs/guides/allocation-report-user-guide.md` (NEW)

---

## 📊 **Implementation Timeline** (UPDATED with Refactoring)

| Phase | Duration | Deliverables | Dependencies |
|-------|----------|--------------|--------------|
| **Phase 0** (NEW) | 2 days | Duration-agnostic `jira_reporter.py` refactoring | spec.md + plan.md approval |
| **Phase 1** | 2 days | Security config + data models | Phase 0 |
| **Phase 2** | 3 days | AllocationCalculator + tests | Phase 1 |
| **Phase 3** | 3 days | Report generator + tests | Phase 2 |
| **Phase 4** | 2 days | CLI + integration tests | Phase 3 |
| **Phase 5** | 2 days | Security + documentation | Phase 4 |
| **TOTAL** | **14 days** | Working `/generate-allocation-report` + refactored architecture | - |

**Timeline Impact**: +2 days (was 12 days, now 14 days)
**Rationale**: Clean architecture foundation reduces future refactoring cost by 50% (prevents 3-day deferred refactoring)

---

## 🧪 **Testing Strategy**

### **Unit Tests** (>90% Coverage Required)
```
tests/unit/reporting/
├── test_allocation_models.py           # TeamAllocation dataclass
├── test_allocation_calculator.py       # L0/L1/L2 detection logic
└── test_allocation_report_builder.py   # Markdown generation
```

### **Integration Tests**
```
tests/integration/
├── test_allocation_report_generation.py  # End-to-end report generation
├── test_allocation_cli.py                # Command-line interface
└── test_jira_integration.py              # Live Jira data fetching
```

### **Security Tests**
```
tests/security/
└── test_pii_prevention.py  # PII/credential detection
```

### **Performance Tests**
```
tests/performance/
└── test_allocation_performance.py  # <30s generation validation
```

---

## 🔒 **Security Requirements**

### **PII/Credentials Protection**
- ✅ Template configuration file with placeholders only
- ✅ Environment variables for all sensitive data
- ✅ Actual config files gitignored
- ✅ Pre-commit hook blocks PII commits
- ✅ git-secrets automated detection

### **Prevention Measures**
```bash
# Environment variables (not committed)
export JIRA_BASE_URL="https://[COMPANY].atlassian.net"
export JIRA_EMAIL="user@company.com"
export JIRA_API_TOKEN="your-token-here"

# Template config (committed)
jira:
  base_url: "${JIRA_BASE_URL}"
  auth:
    email: "${JIRA_EMAIL}"
    api_token: "${JIRA_API_TOKEN}"

# .gitignore
weekly-report-config.yaml
.env
```

---

## 📋 **Validation Checklist**

### **Constitutional Compliance**
- [ ] Simplicity: 1 project, 2 components (within limits)
- [ ] Sequential Thinking: Applied throughout
- [ ] TDD Workflow: RED-GREEN-Refactor for all code
- [ ] BLOAT_PREVENTION: REUSE existing infrastructure
- [ ] PROJECT_STRUCTURE: Files in correct locations

### **Code Quality**
- [ ] DRY Principle: Zero duplication
- [ ] SOLID Principles: Single responsibility per class
- [ ] Type Hints: Complete type annotations
- [ ] Test Coverage: >90% unit, >90% integration
- [ ] Performance: <30s report generation

### **Security**
- [ ] No PII in codebase
- [ ] No credentials in code
- [ ] Template configs with placeholders
- [ ] Environment variables enforced
- [ ] Security tests passing

### **Documentation**
- [ ] Setup guide complete
- [ ] User guide for VPs
- [ ] Troubleshooting section
- [ ] API documentation

---

## 🎯 **Success Metrics**

### **Technical Metrics**
- Report generation time: <30 seconds (90-day window)
- Test coverage: >90% unit, >90% integration
- Code duplication: 0% (BLOAT_PREVENTION compliant)
- L0/L1/L2 detection accuracy: ±5% vs. manual queries

### **Business Metrics**
- VP comprehension time: <2 minutes
- Self-service adoption: VPs can generate reports independently
- Decision impact: Enables $500K+ quarterly resource allocation
- Visibility improvement: Makes 60-70% L0 burden visible

---

## 🚨 **Risk Mitigation**

### **Risk 1: Inconsistent Jira Labeling**
**Mitigation**: Multi-factor detection (labels + keywords + issue type + priority)

### **Risk 2: Performance Issues**
**Mitigation**: Batched Jira API calls, paginated fetching, <30s target

### **Risk 3: PII Leakage**
**Mitigation**: Template configs, environment variables, security tests, pre-commit hooks

### **Risk 4: Over-Engineering**
**Mitigation**: Constitutional simplicity constraints, REUSE existing infrastructure

---

## 📝 **Implementation Authorization**

**Ready to Proceed When**:
1. ✅ spec.md validated and approved
2. ⏳ plan.md reviewed and approved (THIS DOCUMENT)
3. ⏳ tasks.md generated from this plan
4. ⏳ User says "approved" or "proceed"

**Upon Approval, Will**:
1. Generate `tasks.md` with detailed task breakdown
2. Execute implementation following TDD workflow
3. Complete all phases with >90% test coverage
4. Deliver working `/generate-allocation-report` command

---

*This implementation plan follows GitHub Spec-Kit methodology with TDD workflow, Constitutional compliance, BLOAT_PREVENTION enforcement, and PROJECT_STRUCTURE alignment.*
