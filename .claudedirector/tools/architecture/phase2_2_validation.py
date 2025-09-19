#!/usr/bin/env python3
"""
Phase 2.2 Architectural Validation Tool
Validates GitHub spec-kit methodology implementation with SOLID/DRY compliance

🏗️ Martin | Platform Architecture - Architectural compliance validation
🎯 Validates: Sequential thinking + Context7 + SOLID + DRY + BLOAT_PREVENTION + PROJECT_STRUCTURE
"""

import os
import re
import sys
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any
from dataclasses import dataclass, field
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
REPORTING_DIR = PROJECT_ROOT / ".claudedirector" / "lib" / "reporting"
DOCS_DIR = PROJECT_ROOT / "docs"


@dataclass
class ValidationResult:
    """Validation result data structure"""

    category: str
    test_name: str
    passed: bool
    details: str
    violations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ArchitecturalAnalysis:
    """Comprehensive architectural analysis results"""

    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    bloat_prevention_score: float = 0.0
    solid_compliance_score: float = 0.0
    dry_compliance_score: float = 0.0
    project_structure_score: float = 0.0
    mcp_integration_score: float = 0.0
    prd_compliance_score: float = 0.0
    validation_results: List[ValidationResult] = field(default_factory=list)


class Phase2_2ArchitecturalValidator:
    """
    Comprehensive architectural validator for Phase 2.2 implementation

    Validates GitHub spec-kit methodology implementation with:
    - Sequential thinking integration
    - Context7 integration
    - SOLID principles compliance
    - DRY principles compliance
    - BLOAT_PREVENTION_SYSTEM.md adherence
    - PROJECT_STRUCTURE.md compliance
    - PRD chat-only interface requirements
    """

    def __init__(self):
        self.analysis = ArchitecturalAnalysis()
        self.project_root = PROJECT_ROOT
        self.reporting_dir = REPORTING_DIR

        # Phase 2.2 implementation files
        self.phase2_2_files = {
            "conversational_business_intelligence.py": REPORTING_DIR
            / "conversational_business_intelligence.py",
            "weekly_reporter_chat_integration.py": REPORTING_DIR
            / "weekly_reporter_chat_integration.py",
            "phase2_2_integration_test.py": PROJECT_ROOT
            / ".claudedirector"
            / "tests"
            / "phase2_2_integration_test.py",
        }

        print("🏗️ Phase 2.2 Architectural Validator Initialized")
        print(f"📁 Project Root: {self.project_root}")
        print(f"📁 Reporting Directory: {self.reporting_dir}")

    def run_comprehensive_validation(self) -> ArchitecturalAnalysis:
        """Run comprehensive architectural validation"""

        print("\n" + "=" * 80)
        print("PHASE 2.2 COMPREHENSIVE ARCHITECTURAL VALIDATION")
        print("=" * 80)
        print("GitHub Spec-Kit Methodology + Sequential Thinking + Context7")
        print("SOLID + DRY + BLOAT_PREVENTION + PROJECT_STRUCTURE + PRD Compliance")
        print("=" * 80)

        # Validation categories
        validation_categories = [
            ("PROJECT_STRUCTURE Compliance", self._validate_project_structure),
            ("BLOAT_PREVENTION Compliance", self._validate_bloat_prevention),
            ("SOLID Principles Compliance", self._validate_solid_principles),
            ("DRY Principles Compliance", self._validate_dry_principles),
            ("MCP Integration Architecture", self._validate_mcp_integration),
            ("PRD Chat-Only Compliance", self._validate_prd_compliance),
            ("GitHub Spec-Kit Methodology", self._validate_spec_kit_methodology),
            ("Sequential Thinking Integration", self._validate_sequential_thinking),
            ("Context7 Integration", self._validate_context7_integration),
        ]

        # Run all validation categories
        for category_name, validation_function in validation_categories:
            print(f"\n🔍 Validating: {category_name}")
            print("-" * 60)

            try:
                results = validation_function()
                for result in results:
                    self.analysis.validation_results.append(result)
                    self.analysis.total_tests += 1

                    if result.passed:
                        self.analysis.passed_tests += 1
                        print(f"✅ {result.test_name}")
                        if result.details:
                            print(f"   📝 {result.details}")
                    else:
                        self.analysis.failed_tests += 1
                        print(f"❌ {result.test_name}")
                        print(f"   📝 {result.details}")
                        for violation in result.violations:
                            print(f"   🚨 {violation}")
                        for recommendation in result.recommendations:
                            print(f"   💡 {recommendation}")

            except Exception as e:
                print(f"❌ Error validating {category_name}: {e}")
                self.analysis.failed_tests += 1

        # Calculate compliance scores
        self._calculate_compliance_scores()

        # Generate final report
        self._generate_final_report()

        return self.analysis

    def _validate_project_structure(self) -> List[ValidationResult]:
        """Validate PROJECT_STRUCTURE.md compliance"""

        results = []

        # Test 1: Files in correct locations
        expected_locations = {
            "conversational_business_intelligence.py": ".claudedirector/lib/reporting/",
            "weekly_reporter_chat_integration.py": ".claudedirector/lib/reporting/",
            "phase2_2_integration_test.py": ".claudedirector/tests/",
        }

        for filename, expected_path in expected_locations.items():
            file_path = self.project_root / expected_path / filename
            passed = file_path.exists()

            results.append(
                ValidationResult(
                    category="PROJECT_STRUCTURE",
                    test_name=f"File location: {filename}",
                    passed=passed,
                    details=f"Expected: {expected_path}, Exists: {passed}",
                    violations=[] if passed else [f"File not found at {expected_path}"],
                    recommendations=(
                        [] if passed else [f"Move {filename} to {expected_path}"]
                    ),
                )
            )

        # Test 2: No files in wrong directories (user territory)
        leadership_workspace = self.project_root / "leadership-workspace"
        if leadership_workspace.exists():
            for file_info in self.phase2_2_files.items():
                filename, filepath = file_info
                if str(filepath).startswith(str(leadership_workspace)):
                    results.append(
                        ValidationResult(
                            category="PROJECT_STRUCTURE",
                            test_name=f"User territory violation: {filename}",
                            passed=False,
                            details=f"System file found in user territory: {filepath}",
                            violations=[
                                f"System file {filename} in leadership-workspace/"
                            ],
                            recommendations=[
                                f"Move {filename} to .claudedirector/lib/reporting/"
                            ],
                        )
                    )
                else:
                    results.append(
                        ValidationResult(
                            category="PROJECT_STRUCTURE",
                            test_name=f"System territory compliance: {filename}",
                            passed=True,
                            details=f"Correctly located in system territory: {filepath}",
                        )
                    )

        return results

    def _validate_bloat_prevention(self) -> List[ValidationResult]:
        """Validate BLOAT_PREVENTION_SYSTEM.md compliance"""

        results = []

        # Test 1: No duplicate functionality
        bi_file = self.phase2_2_files["conversational_business_intelligence.py"]
        chat_integration_file = self.phase2_2_files[
            "weekly_reporter_chat_integration.py"
        ]

        if bi_file.exists() and chat_integration_file.exists():
            # Check for import patterns (DRY compliance)
            bi_content = bi_file.read_text()
            chat_content = chat_integration_file.read_text()

            # Should import from existing weekly_reporter, not duplicate
            imports_existing = (
                "from .weekly_reporter import" in bi_content
                or "from reporting.weekly_reporter import" in bi_content
            )

            results.append(
                ValidationResult(
                    category="BLOAT_PREVENTION",
                    test_name="Imports existing infrastructure",
                    passed=imports_existing,
                    details=f"Uses existing weekly_reporter.py infrastructure: {imports_existing}",
                    violations=(
                        []
                        if imports_existing
                        else ["Does not import existing weekly_reporter infrastructure"]
                    ),
                    recommendations=(
                        []
                        if imports_existing
                        else ["Import existing components to avoid duplication"]
                    ),
                )
            )

            # Check for graceful fallback patterns
            fallback_pattern = "except ImportError:" in bi_content

            results.append(
                ValidationResult(
                    category="BLOAT_PREVENTION",
                    test_name="Graceful fallback implementation",
                    passed=fallback_pattern,
                    details=f"Implements graceful fallback: {fallback_pattern}",
                    violations=(
                        []
                        if fallback_pattern
                        else ["No graceful fallback for missing dependencies"]
                    ),
                    recommendations=(
                        []
                        if fallback_pattern
                        else ["Add try/except ImportError for missing dependencies"]
                    ),
                )
            )

            # Test 3: No hardcoded duplication
            duplicate_patterns = [
                "class StrategicAnalyzer",  # Should not redefine existing classes
                "class JiraClient",
                "class ConfigManager",
            ]

            has_duplication = any(
                pattern in bi_content for pattern in duplicate_patterns
            )

            results.append(
                ValidationResult(
                    category="BLOAT_PREVENTION",
                    test_name="No class duplication",
                    passed=not has_duplication,
                    details=f"Avoids duplicating existing classes: {not has_duplication}",
                    violations=(
                        ["Duplicates existing class definitions"]
                        if has_duplication
                        else []
                    ),
                    recommendations=(
                        [
                            "Remove duplicate class definitions, import from existing modules"
                        ]
                        if has_duplication
                        else []
                    ),
                )
            )

        return results

    def _validate_solid_principles(self) -> List[ValidationResult]:
        """Validate SOLID principles implementation"""

        results = []

        bi_file = self.phase2_2_files["conversational_business_intelligence.py"]

        if bi_file.exists():
            content = bi_file.read_text()

            # Parse AST for analysis
            try:
                tree = ast.parse(content)

                # Test 1: Single Responsibility Principle
                class_responsibilities = {}
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        methods = [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]
                        class_responsibilities[node.name] = methods

                # Check specific classes for single responsibility
                srp_violations = []

                if "ChatQueryProcessor" in class_responsibilities:
                    processor_methods = class_responsibilities["ChatQueryProcessor"]
                    # Should only handle query processing, not business logic
                    business_methods = [
                        m
                        for m in processor_methods
                        if "calculate" in m.lower() or "generate" in m.lower()
                    ]
                    if business_methods:
                        srp_violations.append(
                            f"ChatQueryProcessor has business logic methods: {business_methods}"
                        )

                if "ConversationalROIEngine" in class_responsibilities:
                    roi_methods = class_responsibilities["ConversationalROIEngine"]
                    # Should only handle ROI calculations, not query parsing
                    parsing_methods = [
                        m
                        for m in roi_methods
                        if "parse" in m.lower() or "classify" in m.lower()
                    ]
                    if parsing_methods:
                        srp_violations.append(
                            f"ConversationalROIEngine has parsing methods: {parsing_methods}"
                        )

                results.append(
                    ValidationResult(
                        category="SOLID",
                        test_name="Single Responsibility Principle",
                        passed=len(srp_violations) == 0,
                        details=f"Classes have single responsibilities: {len(srp_violations) == 0}",
                        violations=srp_violations,
                        recommendations=(
                            [
                                "Separate parsing and business logic into different classes"
                            ]
                            if srp_violations
                            else []
                        ),
                    )
                )

                # Test 2: Open/Closed Principle - extensible methods
                ocp_patterns = [
                    "calculation_methods",
                    "chat_commands",
                    "query_patterns",
                ]
                has_extensible_patterns = any(
                    pattern in content for pattern in ocp_patterns
                )

                results.append(
                    ValidationResult(
                        category="SOLID",
                        test_name="Open/Closed Principle",
                        passed=has_extensible_patterns,
                        details=f"Has extensible patterns for new functionality: {has_extensible_patterns}",
                        violations=(
                            []
                            if has_extensible_patterns
                            else ["No extensible patterns found"]
                        ),
                        recommendations=(
                            []
                            if has_extensible_patterns
                            else [
                                "Add extensible dictionaries/registries for new functionality"
                            ]
                        ),
                    )
                )

                # Test 3: Dependency Inversion - depends on abstractions
                dip_patterns = ["def __init__(self, config", "def __init__(self,"]
                has_dependency_injection = any(
                    pattern in content for pattern in dip_patterns
                )

                results.append(
                    ValidationResult(
                        category="SOLID",
                        test_name="Dependency Inversion Principle",
                        passed=has_dependency_injection,
                        details=f"Uses dependency injection patterns: {has_dependency_injection}",
                        violations=(
                            []
                            if has_dependency_injection
                            else ["No dependency injection patterns"]
                        ),
                        recommendations=(
                            []
                            if has_dependency_injection
                            else ["Use constructor injection for dependencies"]
                        ),
                    )
                )

            except SyntaxError as e:
                results.append(
                    ValidationResult(
                        category="SOLID",
                        test_name="AST Parsing",
                        passed=False,
                        details=f"Syntax error in file: {e}",
                        violations=[f"Syntax error: {e}"],
                        recommendations=["Fix syntax errors in the file"],
                    )
                )

        return results

    def _validate_dry_principles(self) -> List[ValidationResult]:
        """Validate DRY (Don't Repeat Yourself) principles"""

        results = []

        # Test 1: Reuse of existing infrastructure
        bi_file = self.phase2_2_files["conversational_business_intelligence.py"]

        if bi_file.exists():
            content = bi_file.read_text()

            # Check for reuse patterns
            reuse_patterns = [
                "from .weekly_reporter import",
                "from reporting.weekly_reporter import",
                "StrategicAnalyzer",
                "BusinessValueFramework",
                "JiraClient",
                "ConfigManager",
            ]

            reuse_count = sum(1 for pattern in reuse_patterns if pattern in content)
            reuse_score = reuse_count / len(reuse_patterns)

            results.append(
                ValidationResult(
                    category="DRY",
                    test_name="Infrastructure reuse",
                    passed=reuse_score >= 0.5,
                    details=f"Reuses existing infrastructure: {reuse_score:.1%} ({reuse_count}/{len(reuse_patterns)} patterns)",
                    violations=(
                        []
                        if reuse_score >= 0.5
                        else ["Low reuse of existing infrastructure"]
                    ),
                    recommendations=(
                        []
                        if reuse_score >= 0.5
                        else ["Import and reuse more existing components"]
                    ),
                )
            )

            # Test 2: No duplicate constants/strings
            string_literals = re.findall(r'"([^"]*)"', content)
            string_counts = {}
            for s in string_literals:
                if len(s) > 10:  # Only check substantial strings
                    string_counts[s] = string_counts.get(s, 0) + 1

            duplicated_strings = {
                s: count for s, count in string_counts.items() if count > 2
            }

            results.append(
                ValidationResult(
                    category="DRY",
                    test_name="No duplicate strings",
                    passed=len(duplicated_strings) == 0,
                    details=f"Duplicate strings found: {len(duplicated_strings)}",
                    violations=[
                        f"Duplicate string: '{s}' appears {count} times"
                        for s, count in duplicated_strings.items()
                    ],
                    recommendations=(
                        ["Extract duplicate strings to constants"]
                        if duplicated_strings
                        else []
                    ),
                )
            )

        return results

    def _validate_mcp_integration(self) -> List[ValidationResult]:
        """Validate MCP Sequential + Context7 integration"""

        results = []

        bi_file = self.phase2_2_files["conversational_business_intelligence.py"]

        if bi_file.exists():
            content = bi_file.read_text()

            # Test 1: MCP bridge integration
            mcp_patterns = [
                "weekly_reporter_mcp_bridge",
                "MCPEnhancementResult",
                "create_weekly_reporter_mcp_bridge",
            ]

            mcp_integration_count = sum(
                1 for pattern in mcp_patterns if pattern in content
            )
            mcp_integration_score = mcp_integration_count / len(mcp_patterns)

            results.append(
                ValidationResult(
                    category="MCP_INTEGRATION",
                    test_name="MCP bridge integration",
                    passed=mcp_integration_score >= 0.8,
                    details=f"MCP bridge integration: {mcp_integration_score:.1%} ({mcp_integration_count}/{len(mcp_patterns)} patterns)",
                    violations=(
                        []
                        if mcp_integration_score >= 0.8
                        else ["Incomplete MCP bridge integration"]
                    ),
                    recommendations=(
                        []
                        if mcp_integration_score >= 0.8
                        else ["Complete MCP bridge integration patterns"]
                    ),
                )
            )

            # Test 2: Sequential thinking integration
            sequential_patterns = [
                "_enhance_with_mcp_sequential",
                "sequential",
                "strategic_analysis",
            ]

            sequential_count = sum(
                1 for pattern in sequential_patterns if pattern in content
            )

            results.append(
                ValidationResult(
                    category="MCP_INTEGRATION",
                    test_name="Sequential thinking integration",
                    passed=sequential_count >= 2,
                    details=f"Sequential patterns found: {sequential_count}/{len(sequential_patterns)}",
                    violations=(
                        []
                        if sequential_count >= 2
                        else ["Missing Sequential thinking integration"]
                    ),
                    recommendations=(
                        []
                        if sequential_count >= 2
                        else ["Add MCP Sequential integration methods"]
                    ),
                )
            )

            # Test 3: Context7 integration
            context7_patterns = [
                "_enhance_with_context7",
                "context7",
                "industry_insights",
            ]

            context7_count = sum(
                1 for pattern in context7_patterns if pattern in content
            )

            results.append(
                ValidationResult(
                    category="MCP_INTEGRATION",
                    test_name="Context7 integration",
                    passed=context7_count >= 2,
                    details=f"Context7 patterns found: {context7_count}/{len(context7_patterns)}",
                    violations=(
                        [] if context7_count >= 2 else ["Missing Context7 integration"]
                    ),
                    recommendations=(
                        []
                        if context7_count >= 2
                        else ["Add Context7 integration methods"]
                    ),
                )
            )

        return results

    def _validate_prd_compliance(self) -> List[ValidationResult]:
        """Validate PRD chat-only interface compliance"""

        results = []

        # Test 1: No dashboard references
        for filename, filepath in self.phase2_2_files.items():
            if filepath.exists():
                content = filepath.read_text()

                dashboard_keywords = [
                    "dashboard",
                    "chart",
                    "graph",
                    "plot",
                    "visual",
                    "UI component",
                ]
                dashboard_violations = [
                    kw for kw in dashboard_keywords if kw.lower() in content.lower()
                ]

                # Exception: documentation can mention eliminating dashboards
                if "eliminating need for visual dashboards" in content.lower():
                    dashboard_violations = [
                        kw for kw in dashboard_violations if kw != "dashboard"
                    ]

                results.append(
                    ValidationResult(
                        category="PRD_COMPLIANCE",
                        test_name=f"No dashboard references in {filename}",
                        passed=len(dashboard_violations) == 0,
                        details=f"Dashboard keywords found: {dashboard_violations}",
                        violations=[
                            f"PRD violation: Found '{kw}' in {filename}"
                            for kw in dashboard_violations
                        ],
                        recommendations=(
                            [
                                "Remove dashboard/visual references, use chat-only interface"
                            ]
                            if dashboard_violations
                            else []
                        ),
                    )
                )

        # Test 2: Chat command structure
        chat_integration_file = self.phase2_2_files[
            "weekly_reporter_chat_integration.py"
        ]

        if chat_integration_file.exists():
            content = chat_integration_file.read_text()

            # Should have chat commands starting with /
            chat_command_pattern = r'[\'"][/]\w+[\'"]'
            chat_commands = re.findall(chat_command_pattern, content)

            results.append(
                ValidationResult(
                    category="PRD_COMPLIANCE",
                    test_name="Chat command structure",
                    passed=len(chat_commands) >= 5,
                    details=f"Chat commands found: {len(chat_commands)} (examples: {chat_commands[:3]})",
                    violations=(
                        []
                        if len(chat_commands) >= 5
                        else ["Insufficient chat commands for PRD compliance"]
                    ),
                    recommendations=(
                        []
                        if len(chat_commands) >= 5
                        else ["Add more chat commands for comprehensive interface"]
                    ),
                )
            )

            # Test 3: Conversational response format
            response_patterns = [
                "ConversationalResponse",
                "response_text",
                "chat_explanation",
            ]
            response_count = sum(
                1 for pattern in response_patterns if pattern in content
            )

            results.append(
                ValidationResult(
                    category="PRD_COMPLIANCE",
                    test_name="Conversational response format",
                    passed=response_count >= 2,
                    details=f"Conversational patterns: {response_count}/{len(response_patterns)}",
                    violations=(
                        []
                        if response_count >= 2
                        else ["Missing conversational response patterns"]
                    ),
                    recommendations=(
                        []
                        if response_count >= 2
                        else ["Implement conversational response formatting"]
                    ),
                )
            )

        return results

    def _validate_spec_kit_methodology(self) -> List[ValidationResult]:
        """Validate GitHub spec-kit methodology implementation"""

        results = []

        # Test 1: Extends existing infrastructure (spec-kit principle)
        bi_file = self.phase2_2_files["conversational_business_intelligence.py"]

        if bi_file.exists():
            content = bi_file.read_text()

            # Should extend, not replace existing functionality
            extension_patterns = [
                "extends existing",
                "EXTEND existing",
                "DRY compliance",
                "BLOAT_PREVENTION",
            ]

            extension_count = sum(
                1 for pattern in extension_patterns if pattern in content
            )

            results.append(
                ValidationResult(
                    category="SPEC_KIT",
                    test_name="Extension methodology",
                    passed=extension_count >= 2,
                    details=f"Extension patterns found: {extension_count}/{len(extension_patterns)}",
                    violations=(
                        []
                        if extension_count >= 2
                        else ["Does not follow extension methodology"]
                    ),
                    recommendations=(
                        []
                        if extension_count >= 2
                        else ["Document extension of existing infrastructure"]
                    ),
                )
            )

            # Test 2: Modular design (spec-kit principle)
            class_count = len(re.findall(r"class \w+:", content))
            function_count = len(re.findall(r"def \w+\(", content))

            # Should have reasonable modularity (not monolithic)
            good_modularity = class_count >= 3 and function_count >= 10

            results.append(
                ValidationResult(
                    category="SPEC_KIT",
                    test_name="Modular design",
                    passed=good_modularity,
                    details=f"Classes: {class_count}, Functions: {function_count}",
                    violations=(
                        []
                        if good_modularity
                        else ["Insufficient modularity for spec-kit methodology"]
                    ),
                    recommendations=(
                        []
                        if good_modularity
                        else ["Break down into smaller, focused classes and functions"]
                    ),
                )
            )

        return results

    def _validate_sequential_thinking(self) -> List[ValidationResult]:
        """Validate sequential thinking integration"""

        results = []

        for filename, filepath in self.phase2_2_files.items():
            if filepath.exists():
                content = filepath.read_text()

                # Sequential thinking indicators
                sequential_patterns = [
                    "sequential",
                    "step-by-step",
                    "systematic",
                    "methodical",
                    "Progressive",
                ]

                sequential_count = sum(
                    1
                    for pattern in sequential_patterns
                    if pattern.lower() in content.lower()
                )

                results.append(
                    ValidationResult(
                        category="SEQUENTIAL_THINKING",
                        test_name=f"Sequential patterns in {filename}",
                        passed=sequential_count >= 2,
                        details=f"Sequential thinking patterns: {sequential_count}",
                        violations=(
                            []
                            if sequential_count >= 2
                            else ["Insufficient sequential thinking integration"]
                        ),
                        recommendations=(
                            []
                            if sequential_count >= 2
                            else [
                                "Add more sequential/systematic approach documentation"
                            ]
                        ),
                    )
                )

        return results

    def _validate_context7_integration(self) -> List[ValidationResult]:
        """Validate Context7 integration"""

        results = []

        bi_file = self.phase2_2_files["conversational_business_intelligence.py"]

        if bi_file.exists():
            content = bi_file.read_text()

            # Context7 integration patterns
            context7_patterns = [
                "context7",
                "industry_benchmarks",
                "competitive",
                "market",
            ]

            context7_count = sum(
                1 for pattern in context7_patterns if pattern.lower() in content.lower()
            )

            results.append(
                ValidationResult(
                    category="CONTEXT7",
                    test_name="Context7 integration patterns",
                    passed=context7_count >= 3,
                    details=f"Context7 patterns found: {context7_count}/{len(context7_patterns)}",
                    violations=(
                        []
                        if context7_count >= 3
                        else ["Insufficient Context7 integration"]
                    ),
                    recommendations=(
                        []
                        if context7_count >= 3
                        else ["Add more Context7 industry research integration"]
                    ),
                )
            )

        return results

    def _calculate_compliance_scores(self):
        """Calculate compliance scores for each category"""

        category_scores = {}
        category_counts = {}

        for result in self.analysis.validation_results:
            category = result.category
            if category not in category_scores:
                category_scores[category] = 0
                category_counts[category] = 0

            category_counts[category] += 1
            if result.passed:
                category_scores[category] += 1

        # Calculate percentage scores
        if "PROJECT_STRUCTURE" in category_scores:
            self.analysis.project_structure_score = (
                category_scores["PROJECT_STRUCTURE"]
                / category_counts["PROJECT_STRUCTURE"]
                * 100
            )

        if "BLOAT_PREVENTION" in category_scores:
            self.analysis.bloat_prevention_score = (
                category_scores["BLOAT_PREVENTION"]
                / category_counts["BLOAT_PREVENTION"]
                * 100
            )

        if "SOLID" in category_scores:
            self.analysis.solid_compliance_score = (
                category_scores["SOLID"] / category_counts["SOLID"] * 100
            )

        if "DRY" in category_scores:
            self.analysis.dry_compliance_score = (
                category_scores["DRY"] / category_counts["DRY"] * 100
            )

        if "MCP_INTEGRATION" in category_scores:
            self.analysis.mcp_integration_score = (
                category_scores["MCP_INTEGRATION"]
                / category_counts["MCP_INTEGRATION"]
                * 100
            )

        if "PRD_COMPLIANCE" in category_scores:
            self.analysis.prd_compliance_score = (
                category_scores["PRD_COMPLIANCE"]
                / category_counts["PRD_COMPLIANCE"]
                * 100
            )

    def _generate_final_report(self):
        """Generate final comprehensive report"""

        print("\n" + "=" * 80)
        print("PHASE 2.2 ARCHITECTURAL VALIDATION REPORT")
        print("=" * 80)
        print(f"Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Tests: {self.analysis.total_tests}")
        print(f"Passed: {self.analysis.passed_tests}")
        print(f"Failed: {self.analysis.failed_tests}")
        print(
            f"Success Rate: {(self.analysis.passed_tests / self.analysis.total_tests * 100):.1f}%"
        )

        print("\n📊 COMPLIANCE SCORES:")
        print("-" * 40)
        print(f"PROJECT_STRUCTURE:    {self.analysis.project_structure_score:.1f}%")
        print(f"BLOAT_PREVENTION:     {self.analysis.bloat_prevention_score:.1f}%")
        print(f"SOLID Principles:     {self.analysis.solid_compliance_score:.1f}%")
        print(f"DRY Principles:       {self.analysis.dry_compliance_score:.1f}%")
        print(f"MCP Integration:      {self.analysis.mcp_integration_score:.1f}%")
        print(f"PRD Compliance:       {self.analysis.prd_compliance_score:.1f}%")

        # Overall assessment
        overall_score = (
            self.analysis.project_structure_score
            + self.analysis.bloat_prevention_score
            + self.analysis.solid_compliance_score
            + self.analysis.dry_compliance_score
            + self.analysis.mcp_integration_score
            + self.analysis.prd_compliance_score
        ) / 6

        print(f"\n🎯 OVERALL SCORE: {overall_score:.1f}%")

        if overall_score >= 90:
            print(
                "🏆 EXCELLENT: Phase 2.2 implementation exceeds architectural standards"
            )
        elif overall_score >= 80:
            print("✅ GOOD: Phase 2.2 implementation meets architectural standards")
        elif overall_score >= 70:
            print(
                "⚠️  ACCEPTABLE: Phase 2.2 implementation meets minimum standards with improvements needed"
            )
        else:
            print(
                "❌ NEEDS IMPROVEMENT: Phase 2.2 implementation requires significant architectural improvements"
            )

        # Summary of violations and recommendations
        violations = [
            result for result in self.analysis.validation_results if not result.passed
        ]
        if violations:
            print(f"\n🚨 CRITICAL ISSUES TO ADDRESS ({len(violations)}):")
            print("-" * 50)
            for violation in violations[:5]:  # Show top 5
                print(f"❌ {violation.test_name}: {violation.details}")
                for v in violation.violations[:2]:  # Show top 2 violations per test
                    print(f"   🔸 {v}")
                for r in violation.recommendations[:1]:  # Show top recommendation
                    print(f"   💡 {r}")

        print("\n" + "=" * 80)
        print("PHASE 2.2 ARCHITECTURAL VALIDATION COMPLETE")
        print("GitHub Spec-Kit Methodology + Sequential Thinking + Context7")
        print("SOLID + DRY + BLOAT_PREVENTION + PROJECT_STRUCTURE + PRD Compliance")
        print("=" * 80)


def main():
    """Main execution function"""

    print("🏗️ Phase 2.2 Architectural Validator")
    print("GitHub Spec-Kit + Sequential Thinking + Context7 + SOLID + DRY")

    validator = Phase2_2ArchitecturalValidator()
    analysis = validator.run_comprehensive_validation()

    # Save detailed report
    report_path = (
        PROJECT_ROOT
        / "leadership-workspace"
        / "reports"
        / f"phase2_2_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to JSON-serializable format
    report_data = {
        "validation_date": datetime.now().isoformat(),
        "total_tests": analysis.total_tests,
        "passed_tests": analysis.passed_tests,
        "failed_tests": analysis.failed_tests,
        "compliance_scores": {
            "project_structure": analysis.project_structure_score,
            "bloat_prevention": analysis.bloat_prevention_score,
            "solid_principles": analysis.solid_compliance_score,
            "dry_principles": analysis.dry_compliance_score,
            "mcp_integration": analysis.mcp_integration_score,
            "prd_compliance": analysis.prd_compliance_score,
        },
        "validation_results": [
            {
                "category": result.category,
                "test_name": result.test_name,
                "passed": result.passed,
                "details": result.details,
                "violations": result.violations,
                "recommendations": result.recommendations,
            }
            for result in analysis.validation_results
        ],
    }

    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)

    print(f"\n📄 Detailed report saved: {report_path}")

    return 0 if analysis.failed_tests == 0 else 1


if __name__ == "__main__":
    exit(main())
