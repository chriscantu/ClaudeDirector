# Rolling 90-Day Team Allocation Report - Task Breakdown

**Spec-Kit Format v1.0** | **Status**: Phase 2.1 COMPLETE (PR #178 MERGED) | **Owner**: Martin | Platform Architecture

---

## 📋 **Task Organization**

This document breaks down the implementation plan into specific, actionable tasks following **TDD workflow** (RED-GREEN-Refactor) and **GitHub Spec-Kit** methodology.

**Implementation Strategy**:
- Tasks organized by **User Story** (one story per phase)
- **Dependencies** clearly marked
- **Parallel execution** marked with `[P]` where applicable
- **File paths** specified for each task
- **Test-first approach** (write tests before implementation)

**Current Status**:
- ✅ **Phase 0**: COMPLETE (ADR-004 refactoring)
- ✅ **Phase 1**: COMPLETE (Security + Data Models)
- ✅ **Phase 2.1**: COMPLETE (AllocationCalculator - 18/18 tests passing)
- 🎯 **Phase 2.2+**: See spec `004-allocation-report-generation` (PR #179)

---

## ✅ **Phase 0: Architectural Refactoring** - COMPLETE

### **User Story 0.1: Duration-Agnostic Jira Reporter** ✅

**Status**: ✅ COMPLETE - Merged in PR #178

**Goal**: Refactor `weekly_reporter.py` → `jira_reporter.py` with duration as parameter

**Success Criteria**:
- ✅ `jira_reporter.py` created with duration parameter
- ✅ `weekly_reporter.py` imports from `jira_reporter` (backward compatible)
- ✅ `/generate-weekly-report` command still works
- ✅ All P0 tests passing (41/41)

---

#### **Task 0.1.1: Create duration-agnostic JiraReporter base class** ✅

**Status**: ✅ COMPLETE (PR #178)

**Dependencies**: None

**Files**:
- `tests/unit/reporting/test_jira_reporter.py` (NEW - write first)
- `.claudedirector/lib/reporting/jira_reporter.py` (NEW - implement after tests)

**Steps**:
1. **RED**: Write unit tests for `JiraReporter` class
   ```python
   # tests/unit/reporting/test_jira_reporter.py
   def test_duration_label_weekly():
       assert JiraReporter._get_duration_label(7) == "Weekly"

   def test_duration_label_90day():
       assert JiraReporter._get_duration_label(90) == "90-Day"

   def test_duration_parameter_defaults_to_7():
       reporter = JiraReporter(config)
       assert reporter.duration_days == 7
   ```

2. **GREEN**: Implement `JiraReporter` class
   ```python
   # .claudedirector/lib/reporting/jira_reporter.py
   class JiraReporter:
       def __init__(self, config: ConfigManager, duration_days: int = 7):
           self.config = config
           self.duration_days = duration_days
           self.duration_label = self._get_duration_label(duration_days)

       def _get_duration_label(self, days: int) -> str:
           if days == 7: return "Weekly"
           elif days == 90: return "90-Day"
           elif days == 30: return "Monthly"
           elif days % 7 == 0: return f"{days // 7}-Week"
           else: return f"{days}-Day"
   ```

3. **REFACTOR**: Clean up and add docstrings

**Acceptance**: Unit tests pass, duration parameter works correctly

---

#### **Task 0.1.2: Extract core classes from weekly_reporter to jira_reporter** ✅

**Status**: ✅ COMPLETE (PR #178)

**Dependencies**: Task 0.1.1

**Files**:
- `.claudedirector/lib/reporting/jira_reporter.py` (UPDATE)
- `tests/unit/reporting/test_jira_reporter.py` (UPDATE)

**Steps**:
1. **RED**: Write tests for extracted classes
   - `JiraClient` initialization and API calls
   - `StrategicAnalyzer` L0/L1/L2 detection
   - `ConfigManager` YAML loading
   - `ReportGenerator` markdown generation

2. **GREEN**: Copy classes from `weekly_reporter.py` to `jira_reporter.py`
   - Copy `JiraIssue` dataclass
   - Copy `StrategicScore` dataclass
   - Copy `Initiative` dataclass
   - Copy `JiraClient` class
   - Copy `StrategicAnalyzer` class
   - Copy `ConfigManager` class
   - Copy `ReportGenerator` base class

3. **REFACTOR**: Remove duplication, ensure clean imports

**Acceptance**: All classes available in `jira_reporter`, tests pass

---

#### **Task 0.1.3: Parameterize hardcoded "weekly" references** ✅

**Status**: ✅ COMPLETE (PR #178)

**Dependencies**: Task 0.1.2

**Files**:
- `.claudedirector/lib/reporting/jira_reporter.py` (UPDATE)
- `tests/unit/reporting/test_jira_reporter_parameterization.py` (NEW)

**Steps**:
1. **RED**: Write tests for parameterization
   ```python
   def test_log_file_uses_generic_name():
       # Should be jira_report.log not weekly_report.log
       assert log_path.name == "jira_report.log"

   def test_report_header_uses_duration_label():
       reporter = JiraReporter(config, duration_days=90)
       header = reporter._build_header()
       assert "90-Day Executive Report" in header

   def test_jql_uses_duration_days():
       reporter = JiraReporter(config, duration_days=90)
       jql = reporter._build_jql_date_filter()
       assert "-90d" in jql
   ```

2. **GREEN**: Replace hardcoded values
   - Log file: `weekly_report.log` → `jira_report.log`
   - Headers: `"Weekly Executive Report"` → `f"{self.duration_label} Executive Report"`
   - Descriptions: `"this week"` → `f"this {self.duration_label.lower()}"`
   - JQL filters: `"-7d"` → `f"-{self.duration_days}d"`
   - Next report: `+7 days` → `+{self.duration_days} days`

3. **REFACTOR**: Extract string formatting to helper methods

**Acceptance**: All "weekly" references parameterized, tests pass

---

#### **Task 0.1.4: Update weekly_reporter.py for backward compatibility** ✅

**Status**: ✅ COMPLETE (PR #178)

**Dependencies**: Task 0.1.3

**Files**:
- `.claudedirector/lib/reporting/weekly_reporter.py` (UPDATE)
- `tests/integration/test_weekly_reporter_backward_compat.py` (NEW)

**Steps**:
1. **RED**: Write backward compatibility tests
   ```python
   def test_weekly_reporter_imports_from_jira_reporter():
       from .weekly_reporter import JiraClient
       assert JiraClient is not None

   def test_generate_weekly_report_command_works():
       result = generate_weekly_report(config_path, output_path)
       assert result.exists()
   ```

2. **GREEN**: Update `weekly_reporter.py` to import from `jira_reporter`
   ```python
   # LEGACY: Backward compatibility wrapper
   from .jira_reporter import (
       JiraClient,
       StrategicAnalyzer,
       ConfigManager,
       ReportGenerator,
       JiraReporter,
       JiraIssue,
       StrategicScore,
       Initiative
   )

   def generate_weekly_report(config_path: str, output_path: str):
       """Legacy function - use JiraReporter directly"""
       config = ConfigManager(config_path)
       reporter = JiraReporter(config, duration_days=7)
       return reporter.generate_report(output_path)
   ```

3. **REFACTOR**: Add deprecation warnings

**Acceptance**: `/generate-weekly-report` command still works, imports succeed

---

#### **Task 0.1.5: Rename MCP bridge for consistency** ✅

**Status**: ✅ COMPLETE (PR #178)

**Dependencies**: Task 0.1.4

**Files**:
- `.claudedirector/lib/reporting/jira_reporter_mcp_bridge.py` (RENAME from weekly_reporter_mcp_bridge.py)
- `.claudedirector/lib/reporting/jira_reporter.py` (UPDATE imports)

**Steps**:
1. Rename file: `weekly_reporter_mcp_bridge.py` → `jira_reporter_mcp_bridge.py`
2. Update imports in `jira_reporter.py`
3. Update backward compatibility imports in `weekly_reporter.py`

**Acceptance**: MCP bridge works with new name, no broken imports

---

#### **Task 0.1.6: Run P0 test suite validation** ✅

**Status**: ✅ COMPLETE (PR #178 - 41/41 P0 tests passing)

**Dependencies**: Task 0.1.5

**Files**:
- All P0 tests

**Steps**:
1. Run full P0 test suite: `python .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py`
2. Verify 42/42 tests pass
3. Run weekly report generation: `/generate-weekly-report`
4. Verify report generates successfully

**Acceptance**: All P0 tests pass, no regression in weekly report functionality

---

## 📊 **Phase 1: Foundation & Security** (2 days) ✅ **COMPLETE**

### **User Story 1.1: Security-Compliant Configuration** ✅

**Goal**: Create template configuration with environment variables (no PII)

**Success Criteria**:
- [x] Template file uses `${VAR}` placeholders
- [x] Actual config file gitignored
- [x] Security test validates no PII in template
- [x] JQL config template created and versioned (.claudedirector/config/)

---

#### **Task 1.1.1: Create environment variable template**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Phase 0 complete

**Files**:
- `leadership-workspace/configs/weekly-report-config.template.yaml` (NEW)
- `leadership-workspace/configs/.env.template` (NEW)
- `.gitignore` (UPDATE)

**Steps**:
1. Create template config with placeholders:
   ```yaml
   jira:
     base_url: "${JIRA_BASE_URL}"
     auth:
       email: "${JIRA_EMAIL}"
       api_token: "${JIRA_API_TOKEN}"
   ```

2. Create `.env.template`:
   ```bash
   JIRA_BASE_URL=https://[YOUR-COMPANY].atlassian.net
   JIRA_EMAIL=[YOUR-EMAIL]@[YOUR-COMPANY].com
   JIRA_API_TOKEN=[YOUR-API-TOKEN]
   ```

3. Update `.gitignore`:
   ```
   leadership-workspace/configs/weekly-report-config.yaml
   leadership-workspace/configs/.env
   ```

**Acceptance**: Template uses placeholders, actual configs gitignored

---

#### **Task 1.1.2: Add JQL queries for allocation report**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 1.1.1

**Files**:
- `leadership-workspace/configs/weekly-report-config.template.yaml` (UPDATE)

**Steps**:
1. Add allocation-specific JQL queries to template:
   ```yaml
   jql_queries:
     # Rolling 90-day allocation queries
     allocation_completed_work: 'project in (...) AND type != Epic AND status CHANGED TO Done AFTER -{duration}d AND status != "Honorably Discharged" AND parent is not EMPTY ORDER BY parent, project, priority DESC'

     allocation_parent_epics: 'project in (...) AND type = Epic AND issueFunction in hasSubtasks() AND (status CHANGED TO Done AFTER -{duration}d OR status in ("In Progress", "In Review")) ORDER BY parent, status'

     allocation_l0_l1_l2_initiatives: 'project = "Procore Initiatives" AND (summary ~ "L0:|L1:|L2:" OR labels in ("L0", "L1", "L2")) AND type = Epic AND (status CHANGED TO Done AFTER -{duration}d OR status in ("In Progress", "In Review")) ORDER BY labels, status'
   ```

**Acceptance**: Allocation JQL queries available in template

---

#### **Task 1.1.3: Create security test for PII prevention**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Task 1.1.2

**Files**:
- `tests/security/test_pii_prevention.py` (NEW)

**Steps**:
1. **RED**: Write security tests
   ```python
   def test_template_config_has_no_real_email():
       with open('leadership-workspace/configs/weekly-report-config.template.yaml') as f:
           content = f.read()
       assert '@' not in content or '${' in content  # Only placeholders

   def test_template_config_has_no_api_tokens():
       with open('leadership-workspace/configs/weekly-report-config.template.yaml') as f:
           content = f.read()
       assert 'ATATT' not in content  # No real Jira tokens

   def test_actual_config_is_gitignored():
       gitignore = open('.gitignore').read()
       assert 'weekly-report-config.yaml' in gitignore
   ```

2. **GREEN**: Ensure templates pass tests (already done in Task 1.1.1)

3. **REFACTOR**: Add to CI pipeline

**Acceptance**: Security tests pass, no PII in templates

---

### **User Story 1.2: Team Allocation Data Model** ✅

**Goal**: Create type-safe data model for team allocation

**Success Criteria**:
- [x] Allocation percentages sum to 100% (±0.1% tolerance)
- [x] Type hints for all fields
- [x] Validation raises errors for invalid data
- [x] Unit test coverage >95% (11/11 tests passing - 100%)

---

#### **Task 1.2.1: Create TeamAllocation dataclass with validation**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: None (parallel with Task 1.1.x)

**Files**:
- `tests/unit/reporting/test_allocation_models.py` (NEW - write first)
- `.claudedirector/lib/reporting/allocation_models.py` (NEW - implement after tests)

**Steps**:
1. **RED**: Write unit tests
   ```python
   def test_allocation_percentages_sum_to_100():
       allocation = TeamAllocation(
           team_name="Web Platform",
           date_range=(start, end),
           l0_pct=30.0, l1_pct=20.0, l2_pct=40.0, other_pct=10.0,
           total_issues=100, l2_velocity_actual=4.0, l2_velocity_projected=10.0
       )
       assert 99.9 <= allocation.total_percentage <= 100.1

   def test_allocation_rejects_invalid_percentages():
       with pytest.raises(ValueError):
           TeamAllocation(..., l0_pct=50, l1_pct=50, l2_pct=50, other_pct=0)

   def test_allocation_has_type_hints():
       assert TeamAllocation.__annotations__['l0_pct'] == float
   ```

2. **GREEN**: Implement `TeamAllocation` dataclass
   ```python
   from dataclasses import dataclass
   from datetime import datetime
   from typing import Tuple

   @dataclass
   class TeamAllocation:
       team_name: str
       date_range: Tuple[datetime, datetime]
       l0_pct: float
       l1_pct: float
       l2_pct: float
       other_pct: float
       total_issues: int
       l2_velocity_actual: float
       l2_velocity_projected: float

       def __post_init__(self):
           total = self.l0_pct + self.l1_pct + self.l2_pct + self.other_pct
           if not (99.9 <= total <= 100.1):
               raise ValueError(f"Allocation must sum to 100%, got {total}%")

       @property
       def total_percentage(self) -> float:
           return self.l0_pct + self.l1_pct + self.l2_pct + self.other_pct
   ```

3. **REFACTOR**: Add helper methods, clean up validation

**Acceptance**: Data model validates correctly, tests pass with >95% coverage

---

## ✅ **Phase 2.1: Core Allocation Logic** - COMPLETE

### **User Story 2.1: Allocation Calculator** ✅

**Status**: ✅ COMPLETE - Merged in PR #178

**Goal**: Calculate team allocation % across L0/L1/L2 work

**Success Criteria**:
- ✅ L0/L1/L2 detection matches manual Jira queries (±5% accuracy)
- ✅ Allocation percentages always sum to 100%
- ✅ Handles edge cases (empty data, single issue type)
- ✅ Unit test coverage 100% (18/18 tests passing)
- ✅ ZERO duplication (REUSE StrategicAnalyzer patterns)
- ✅ Context7 velocity patterns (Google SRE, Spotify, Netflix)
- ✅ Cross-project hierarchy traversal

---

#### **Task 2.1.1: [P] Create AllocationCalculator class with hierarchy traversal** ✅

**Status**: ✅ COMPLETE (PR #178 - 18/18 tests GREEN)

**Dependencies**: Phase 1 complete

**Files**:
- `tests/unit/reporting/test_allocation_calculator.py` (NEW - write first)
- `.claudedirector/lib/reporting/allocation_calculator.py` (NEW - implement after tests)

**Steps**:
1. **RED**: Write comprehensive unit tests
   ```python
   def test_detect_l0_via_procore_initiatives_parent():
       # Story → Epic → PI-14632 (L0: FedRAMP)
       issue = JiraIssue(key="UIS-1234", parent="UIS-1000", ...)
       epic = JiraIssue(key="UIS-1000", parent="PI-14632", ...)
       initiative = JiraIssue(key="PI-14632", summary="L0: FedRAMP", project="Procore Initiatives", ...)

       calculator = AllocationCalculator(analyzer, jira_client)
       level = calculator._get_initiative_level(issue)
       assert level == "L0"

   def test_detect_l1_via_parent_chain():
       # Test L1 detection
       pass

   def test_detect_l2_via_parent_chain():
       # Test L2 detection
       pass

   def test_orphaned_work_returns_other():
       issue = JiraIssue(key="UIS-1234", parent=None, ...)
       level = calculator._get_initiative_level(issue)
       assert level == "Other"

   def test_epic_caching_avoids_duplicate_api_calls():
       # Test that same epic only fetched once
       pass
   ```

2. **GREEN**: Implement `AllocationCalculator`
   ```python
   from .jira_reporter import StrategicAnalyzer, JiraIssue, JiraClient

   class AllocationCalculator:
       def __init__(self, strategic_analyzer: StrategicAnalyzer, jira_client: JiraClient):
           self.analyzer = strategic_analyzer
           self.jira = jira_client
           self._epic_cache = {}

       def _get_initiative_level(self, issue: JiraIssue) -> str:
           """Traverse CROSS-PROJECT hierarchy"""
           if issue.type != "Epic" and issue.parent:
               epic = self._fetch_epic_cached(issue.parent)
               if epic and epic.parent:
                   initiative = self._fetch_epic_cached(epic.parent)
                   if initiative and initiative.project == "Procore Initiatives":
                       if "L0:" in initiative.summary or "L0" in initiative.labels:
                           return "L0"
                       if "L1:" in initiative.summary or "L1" in initiative.labels:
                           return "L1"
                       if "L2:" in initiative.summary or "L2" in initiative.labels:
                           return "L2"
           return "Other"

       def _fetch_epic_cached(self, epic_key: str):
           if epic_key not in self._epic_cache:
               self._epic_cache[epic_key] = self.jira.fetch_issue(epic_key)
           return self._epic_cache[epic_key]
   ```

3. **REFACTOR**: Optimize caching, add error handling

**Acceptance**: L0/L1/L2 detection works via cross-project hierarchy, tests pass

---

#### **Task 2.1.2: [P] Implement allocation percentage calculation**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Task 2.1.1

**Files**:
- `tests/unit/reporting/test_allocation_calculator.py` (UPDATE)
- `.claudedirector/lib/reporting/allocation_calculator.py` (UPDATE)

**Steps**:
1. **RED**: Write tests for percentage calculation
   ```python
   def test_calculate_team_allocation_percentages():
       issues = [
           JiraIssue(...),  # L0 issue
           JiraIssue(...),  # L0 issue
           JiraIssue(...),  # L1 issue
           JiraIssue(...),  # L2 issue
       ]
       allocation = calculator.calculate_team_allocation(issues, start, end)
       assert allocation.l0_pct == 50.0  # 2/4
       assert allocation.l1_pct == 25.0  # 1/4
       assert allocation.l2_pct == 25.0  # 1/4
       assert allocation.other_pct == 0.0

   def test_allocation_always_sums_to_100():
       allocation = calculator.calculate_team_allocation(issues, start, end)
       assert 99.9 <= allocation.total_percentage <= 100.1

   def test_empty_issues_handles_gracefully():
       allocation = calculator.calculate_team_allocation([], start, end)
       assert allocation is not None
   ```

2. **GREEN**: Implement calculation logic
   ```python
   def calculate_team_allocation(
       self, team_issues: List[JiraIssue],
       start_date: datetime, end_date: datetime
   ) -> TeamAllocation:
       filtered = self._filter_by_date_range(team_issues, start_date, end_date)

       l0_issues = [i for i in filtered if self._get_initiative_level(i) == "L0"]
       l1_issues = [i for i in filtered if self._get_initiative_level(i) == "L1"]
       l2_issues = [i for i in filtered if self._get_initiative_level(i) == "L2"]
       other_issues = [i for i in filtered if self._get_initiative_level(i) == "Other"]

       total = len(filtered)
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

3. **REFACTOR**: Extract helper methods, optimize loops

**Acceptance**: Allocation calculation accurate, percentages sum to 100%

---

#### **Task 2.1.3: Implement velocity impact analysis**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Task 2.1.2

**Files**:
- `tests/unit/reporting/test_allocation_calculator.py` (UPDATE)
- `.claudedirector/lib/reporting/allocation_calculator.py` (UPDATE)

**Steps**:
1. **RED**: Write velocity tests
   ```python
   def test_l2_velocity_calculation():
       # 4 L2 issues completed over 90 days = ~0.31 issues/week
       l2_issues = [JiraIssue(...) for _ in range(4)]
       velocity = calculator._calculate_velocity(l2_issues, start_90d_ago, end_today)
       assert 0.3 <= velocity <= 0.35

   def test_projected_velocity_if_100_percent_l2():
       # If team had 40% L2 actual, projected is 2.5x higher
       allocation = calculator.calculate_team_allocation(issues, start, end)
       assert allocation.l2_velocity_projected > allocation.l2_velocity_actual
   ```

2. **GREEN**: Implement velocity methods
   ```python
   def _calculate_velocity(self, issues: List[JiraIssue], start: datetime, end: datetime) -> float:
       days = (end - start).days
       weeks = days / 7.0
       return len(issues) / weeks if weeks > 0 else 0.0

   def _calculate_projected_velocity(self, total_issues: int, start: datetime, end: datetime) -> float:
       days = (end - start).days
       weeks = days / 7.0
       return total_issues / weeks if weeks > 0 else 0.0
   ```

3. **REFACTOR**: Add velocity trend analysis

**Acceptance**: Velocity calculations accurate, projected velocity shows impact

---

## 🎯 **Phase 2.2+: Report Generation & CLI**

**Status**: 🚀 In Progress - See spec `004-allocation-report-generation` (PR #179)

**Remaining Work:**
- Phase 2.2: AllocationReportGenerator (markdown output)
- Phase 2.3: CLI integration (`/generate-allocation-report`)
- Phase 3: Historical trend analysis
- Phase 4: L1→L2 connection mapping
- Phase 5: Multi-team comparisons

**All subsequent phases moved to:** `docs/development/specs/004-allocation-report-generation/`

---

## 📊 **Phase 3: Report Generation** (MOVED TO SPEC 004)

### **User Story 3.1: Allocation Report Generator**

**Goal**: Generate executive markdown reports

**Success Criteria**:
- [ ] Report generation <30 seconds for 90-day window
- [ ] Executive summary comprehensible in <2 minutes
- [ ] Team-by-team allocation breakdown
- [ ] L1→L2 connections shown
- [ ] Integration test coverage >90%

---

#### **Task 3.1.1: Create AllocationReportGenerator class**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Phase 2 complete

**Files**:
- `tests/integration/test_allocation_report_generation.py` (NEW - write first)
- `.claudedirector/lib/reporting/allocation_report_generator.py` (NEW - implement after tests)

**Steps**:
1. **RED**: Write integration tests
   ```python
   def test_generate_allocation_report_end_to_end():
       config = ConfigManager('configs/test-config.yaml')
       generator = AllocationReportGenerator(config, jira_client, analyzer)

       output = generator.generate_allocation_report(
           start_date=datetime.now() - timedelta(days=90),
           end_date=datetime.now(),
           output_path='reports/test-allocation.md'
       )

       assert output.exists()
       content = output.read_text()
       assert '90-Day Team Allocation Report' in content
       assert 'L0:' in content and 'L1:' in content and 'L2:' in content

   def test_report_generation_performance():
       start = time.time()
       generator.generate_allocation_report(...)
       elapsed = time.time() - start
       assert elapsed < 30  # Must complete in <30 seconds
   ```

2. **GREEN**: Implement `AllocationReportGenerator`
   ```python
   from .jira_reporter import JiraClient, StrategicAnalyzer, ConfigManager, JiraReporter
   from .allocation_calculator import AllocationCalculator

   class AllocationReportGenerator:
       def __init__(self, config: ConfigManager, jira_client: JiraClient, analyzer: StrategicAnalyzer):
           self.config = config
           self.jira = jira_client
           self.analyzer = analyzer
           self.calculator = AllocationCalculator(analyzer, jira_client)

       def generate_allocation_report(self, start_date: datetime, end_date: datetime, output_path: str) -> str:
           # Fetch issues in range
           issues = self._fetch_issues_in_range(start_date, end_date)

           # Calculate allocations per team
           allocations = self._calculate_team_allocations(issues, start_date, end_date)

           # Build markdown report
           report_content = self._build_markdown_report(allocations)

           # Save report
           with open(output_path, 'w') as f:
               f.write(report_content)

           return output_path
   ```

3. **REFACTOR**: Extract report sections, optimize queries

**Acceptance**: Reports generate successfully in <30s

---

#### **Task 3.1.2: Build executive summary section**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 3.1.1

**Files**:
- `.claudedirector/lib/reporting/allocation_report_generator.py` (UPDATE)

**Steps**:
1. Implement `_build_executive_summary()`:
   ```python
   def _build_executive_summary(self, allocations: List[TeamAllocation]) -> str:
       total_issues = sum(a.total_issues for a in allocations)
       avg_l0 = sum(a.l0_pct for a in allocations) / len(allocations)
       avg_l2 = sum(a.l2_pct for a in allocations) / len(allocations)

       crisis_teams = [a for a in allocations if a.l0_pct > 60]

       return f"""# 90-Day Team Allocation Report

**Period**: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}

## 🎯 Executive Summary

**Total Work Analyzed**: {total_issues} completed issues across {len(allocations)} teams

**Average Allocation**:
- L0 (Keep-the-lights-on): {avg_l0:.1f}%
- L2 (Strategic initiatives): {avg_l2:.1f}%

**⚠️ Teams with High L0 Burden** (>60%): {len(crisis_teams)} teams
{''.join(f'- {t.team_name}: {t.l0_pct:.1f}% L0' for t in crisis_teams)}
"""
   ```

**Acceptance**: Executive summary clear and actionable

---

#### **Task 3.1.3: Build team-by-team breakdown section**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 3.1.2

**Files**:
- `.claudedirector/lib/reporting/allocation_report_generator.py` (UPDATE)

**Steps**:
1. Implement `_build_team_section()`:
   ```python
   def _build_team_section(self, allocation: TeamAllocation) -> str:
       return f"""### {allocation.team_name}

**Allocation Breakdown**:
- 🔴 L0 (Keep-the-lights-on): {allocation.l0_pct:.1f}%
- 🟡 L1 (Enabling L2 work): {allocation.l1_pct:.1f}%
- 🟢 L2 (Strategic initiatives): {allocation.l2_pct:.1f}%
- ⚪ Other (Unclassified): {allocation.other_pct:.1f}%

**Velocity Analysis**:
- L2 Actual Velocity: {allocation.l2_velocity_actual:.2f} issues/week
- L2 Projected (if 100% capacity): {allocation.l2_velocity_projected:.2f} issues/week
- **Velocity Impact**: {allocation.l0_pct:.1f}% L0 burden reducing L2 velocity by {(1 - allocation.l2_velocity_actual / allocation.l2_velocity_projected) * 100:.1f}%
"""
   ```

**Acceptance**: Team breakdowns show allocation and velocity impact

---

#### **Task 3.1.4: Build L1→L2 connection mapping**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 3.1.3

**Files**:
- `.claudedirector/lib/reporting/allocation_report_generator.py` (UPDATE)

**Steps**:
1. Implement `_build_l1_l2_connections()`:
   ```python
   def _build_l1_l2_connections(self, allocations: List[TeamAllocation]) -> str:
       connections = []
       for allocation in allocations:
           l1_issues = [i for i in allocation.issues if self.calculator._get_initiative_level(i) == "L1"]
           for l1 in l1_issues:
               l2_parent = self._find_l2_parent(l1)
               if l2_parent:
                   connections.append((l1, l2_parent))

       return f"""## 🔗 L1→L2 Connections

**Enabling Work Supporting Strategic Initiatives**:

{''.join(f'- {l1.key}: {l1.summary} → **{l2.key}**: {l2.summary}' for l1, l2 in connections)}
"""
   ```

**Acceptance**: L1→L2 connections clearly shown

---

## 🖥️ **Phase 4: Command Interface** (2 days)

### **User Story 4.1: Command-Line Interface**

**Goal**: Create user-friendly `/generate-allocation-report` command

**Success Criteria**:
- [ ] Command works with default 90-day window
- [ ] Supports custom date ranges
- [ ] Error messages clear and actionable

---

#### **Task 4.1.1: Create CLI entry point**

**Status**: 🔴 RED (Write Tests First)

**Dependencies**: Phase 3 complete

**Files**:
- `tests/integration/test_allocation_cli.py` (NEW - write first)
- `.claudedirector/lib/reporting/allocation_cli.py` (NEW - implement after tests)

**Steps**:
1. **RED**: Write CLI tests
   ```python
   def test_cli_default_90_days():
       result = subprocess.run([
           'python', '.claudedirector/lib/reporting/allocation_cli.py',
           '--config', 'configs/test-config.yaml'
       ], capture_output=True)
       assert result.returncode == 0
       assert 'allocation-report-' in result.stdout.decode()

   def test_cli_custom_date_range():
       result = subprocess.run([
           'python', '.claudedirector/lib/reporting/allocation_cli.py',
           '--start-date', '2025-01-01',
           '--end-date', '2025-03-31'
       ], capture_output=True)
       assert result.returncode == 0
   ```

2. **GREEN**: Implement CLI
   ```python
   import argparse
   from datetime import datetime, timedelta

   def main():
       parser = argparse.ArgumentParser(
           description='Generate rolling team allocation report'
       )
       parser.add_argument('--config', default='leadership-workspace/configs/weekly-report-config.yaml')
       parser.add_argument('--days', type=int, default=90)
       parser.add_argument('--start-date', type=str)
       parser.add_argument('--end-date', type=str)
       parser.add_argument('--output', type=str)

       args = parser.parse_args()

       # Calculate date range
       if args.start_date and args.end_date:
           start = datetime.strptime(args.start_date, '%Y-%m-%d')
           end = datetime.strptime(args.end_date, '%Y-%m-%d')
       else:
           end = datetime.now()
           start = end - timedelta(days=args.days)

       # Generate report
       config = ConfigManager(args.config)
       jira_client = JiraClient(config.get_jira_config())
       analyzer = StrategicAnalyzer(config)
       generator = AllocationReportGenerator(config, jira_client, analyzer)

       output = args.output or f'leadership-workspace/reports/allocation-report-{datetime.now().strftime("%Y-%m-%d")}.md'
       result = generator.generate_allocation_report(start, end, output)

       print(f"✅ Allocation report generated: {result}")

   if __name__ == '__main__':
       main()
   ```

3. **REFACTOR**: Add error handling, validation

**Acceptance**: CLI works with all options, errors are clear

---

#### **Task 4.1.2: Create /generate-allocation-report command wrapper**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 4.1.1

**Files**:
- `.cursor/commands/generate-allocation-report.md` (NEW)

**Steps**:
1. Create Cursor command wrapper:
   ```markdown
   # Generate Allocation Report

   Generate rolling team allocation report showing L0/L1/L2 distribution.

   ## Usage

   `/generate-allocation-report [options]`

   ## Options

   - `--days 90` - Rolling window (default: 90)
   - `--start-date YYYY-MM-DD` - Custom start date
   - `--end-date YYYY-MM-DD` - Custom end date
   - `--output path/to/report.md` - Custom output path

   ## Examples

   ```bash
   # Default 90-day window
   /generate-allocation-report

   # Custom 60-day window
   /generate-allocation-report --days 60

   # Specific date range
   /generate-allocation-report --start-date 2025-01-01 --end-date 2025-03-31
   ```
   ```

**Acceptance**: Command documented and accessible

---

## 🔒 **Phase 5: Security & Documentation** (2 days)

### **User Story 5.1: Security Validation**

**Goal**: Automated PII/credential detection

**Success Criteria**:
- [ ] Security tests pass
- [ ] Pre-commit hook blocks PII
- [ ] git-secrets configured

---

#### **Task 5.1.1: Add pre-commit hook for PII detection**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: None (parallel)

**Files**:
- `.pre-commit-config.yaml` (UPDATE)
- `.git/hooks/pre-commit` (UPDATE)

**Steps**:
1. Add security hook to `.pre-commit-config.yaml`:
   ```yaml
   - repo: local
     hooks:
       - id: pii-credential-scan
         name: PII & Credential Scanner
         entry: python .claudedirector/tools/security/pii_scanner.py
         language: system
         types: [yaml, python]
   ```

2. Test hook prevents commits with PII

**Acceptance**: Pre-commit hook blocks PII commits

---

#### **Task 5.1.2: Install and configure git-secrets**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 5.1.1

**Files**:
- `docs/setup/allocation-report-setup.md` (NEW)

**Steps**:
1. Document git-secrets installation:
   ```bash
   # macOS
   brew install git-secrets

   # Configure
   git secrets --install
   git secrets --register-aws
   git secrets --add 'ATATT[0-9A-Za-z]+'  # Jira tokens
   git secrets --add '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Emails
   ```

2. Add to setup documentation

**Acceptance**: git-secrets prevents credential commits

---

### **User Story 5.2: Setup Documentation**

**Goal**: Complete setup guide for VPs

**Success Criteria**:
- [ ] Step-by-step environment setup
- [ ] Command examples
- [ ] Troubleshooting section

---

#### **Task 5.2.1: Create environment variable setup guide**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: None (parallel)

**Files**:
- `docs/setup/allocation-report-setup.md` (NEW)

**Steps**:
1. Create setup documentation with:
   - Environment variable configuration
   - Jira API token generation
   - Configuration file setup
   - First report generation
   - Troubleshooting common issues

**Acceptance**: VP can follow guide and generate report independently

---

#### **Task 5.2.2: Create user guide for VPs**

**Status**: 🟢 GREEN (Implementation)

**Dependencies**: Task 5.2.1

**Files**:
- `docs/guides/allocation-report-user-guide.md` (NEW)

**Steps**:
1. Create user guide covering:
   - What the report shows
   - How to interpret allocation percentages
   - Understanding velocity impact
   - Making resource allocation decisions
   - When to run reports (monthly recommended)

**Acceptance**: VP understands how to use reports for decision-making

---

## 📊 **Task Summary**

**Total Tasks**: 33 tasks across 6 phases

**Phase Breakdown**:
- Phase 0 (Refactoring): 6 tasks, 2 days
- Phase 1 (Foundation): 5 tasks, 2 days
- Phase 2 (Core Logic): 3 tasks, 3 days
- Phase 3 (Report Generation): 4 tasks, 3 days
- Phase 4 (CLI): 2 tasks, 2 days
- Phase 5 (Security & Docs): 4 tasks, 2 days

**Parallel Tasks** (marked with [P]):
- Phase 1: Tasks 1.1.x and 1.2.x can run in parallel
- Phase 2: Task 2.1.1 and 2.1.2 can run in parallel
- Phase 5: Tasks 5.1.x and 5.2.x can run in parallel

**TDD Approach**:
- 🔴 RED: Write tests first (15 tasks)
- 🟢 GREEN: Implement to pass tests (18 tasks)
- 🔄 REFACTOR: Clean up and optimize (all tasks)

---

## 🎯 **Ready to Begin Implementation**

**Next Step**: Execute Phase 0, Task 0.1.1 (Create duration-agnostic JiraReporter base class)

**Command**: Proceed with TDD implementation following task order
