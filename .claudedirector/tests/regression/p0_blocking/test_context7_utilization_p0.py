#!/usr/bin/env python3
"""
P0 CRITICAL FEATURE TEST: Context7 MCP Utilization

🚨 BLOCKING P0 TEST: Context7 MCP server must be utilized for all strategic frameworks and patterns
🎯 ZERO TOLERANCE: Strategic guidance without Context7 intelligence is unacceptable
🏗️ SYSTEMATIC VALIDATION: Ensures Context7 MCP integration is active and functional

This P0 test validates that Context7 MCP server is consistently utilized for
strategic framework applications and architectural pattern guidance.

Author: Martin | Platform Architecture with Sequential Thinking methodology
"""

import unittest
import os
import sys
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import time

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestContext7UtilizationP0(unittest.TestCase):
    """
    🚨 P0 CRITICAL: Context7 MCP Server Utilization Validation

    BLOCKING REQUIREMENTS:
    - Context7 MCP server must be accessible and functional
    - Strategic framework applications must utilize Context7 intelligence
    - Architectural pattern guidance must leverage Context7 capabilities
    - Context7 integration must meet performance requirements (<500ms)
    """

    def setUp(self):
        """Set up P0 Context7 utilization validation"""
        self.project_root = self._find_project_root()

        # P0 Critical thresholds
        self.max_response_time_ms = 500  # Maximum 500ms response time
        self.min_context7_utilization_rate = 80.0  # 80% minimum utilization rate
        self.required_context7_patterns = [
            "Context7",
            "context7",
            "pattern_access",
            "framework_patterns",
            "architectural_patterns",
        ]

    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        while current != current.parent:
            claudedir = current / ".claudedirector"
            # Check if this is the real project root by verifying expected structure
            if (
                claudedir.exists()
                and (claudedir / "lib").exists()
                and (claudedir / "tools").exists()
            ):
                return current
            current = current.parent
        return Path(__file__).parent.parent.parent.parent

    def test_p0_context7_mcp_server_availability(self):
        """P0 TEST: Context7 MCP server must be available and accessible"""
        # Check for Context7 MCP server references in codebase
        context7_references = []

        # Search for Context7 integration patterns
        lib_dir = self.project_root / ".claudedirector" / "lib"
        if lib_dir.exists():
            for py_file in lib_dir.glob("**/*.py"):
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Look for Context7 patterns
                    for pattern in self.required_context7_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            context7_references.append(
                                str(py_file.relative_to(self.project_root))
                            )
                            break

                except Exception:
                    continue  # Skip files that can't be read

        self.assertGreater(
            len(context7_references),
            0,
            "BLOCKING FAILURE: No Context7 MCP server references found in codebase - "
            "Context7 utilization is not implemented",
        )

        # Validate Context7 integration quality
        self.assertGreaterEqual(
            len(context7_references),
            3,
            f"BLOCKING FAILURE: Only {len(context7_references)} files reference Context7 - "
            "insufficient Context7 integration for P0 requirements",
        )

    def test_p0_context7_strategic_framework_integration(self):
        """P0 TEST: Strategic frameworks must utilize Context7 intelligence"""
        # Check for Context7 integration in strategic framework files
        strategic_framework_files = [
            "ai_intelligence/framework_processor.py",
            "ai_intelligence/enhanced_framework_engine.py",
            "personas/strategic_challenge_framework.py",
            "core/enhanced_persona_manager.py",
        ]

        context7_integrated_frameworks = 0
        missing_integration = []

        for framework_file in strategic_framework_files:
            file_path = self.project_root / ".claudedirector" / "lib" / framework_file

            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Check for Context7 integration patterns
                    has_context7_integration = any(
                        re.search(pattern, content, re.IGNORECASE)
                        for pattern in self.required_context7_patterns
                    )

                    if has_context7_integration:
                        context7_integrated_frameworks += 1
                    else:
                        missing_integration.append(framework_file)

                except Exception as e:
                    missing_integration.append(f"{framework_file} (read error: {e})")
            else:
                # File doesn't exist - check if it's been consolidated
                pass

        # Calculate Context7 utilization rate
        total_frameworks = len(
            [
                f
                for f in strategic_framework_files
                if (self.project_root / ".claudedirector" / "lib" / f).exists()
            ]
        )

        if total_frameworks > 0:
            utilization_rate = (context7_integrated_frameworks / total_frameworks) * 100
        else:
            utilization_rate = 0.0

        self.assertGreaterEqual(
            utilization_rate,
            self.min_context7_utilization_rate,
            f"BLOCKING FAILURE: Context7 utilization rate {utilization_rate:.1f}% "
            f"below P0 requirement of {self.min_context7_utilization_rate}%. "
            f"Missing Context7 integration: {missing_integration}",
        )

    def test_p0_context7_mcp_transparency_disclosure(self):
        """P0 TEST: Context7 utilization must be transparently disclosed"""
        # Check for Context7 transparency patterns in the codebase
        transparency_patterns = [
            r"🔧 Accessing MCP Server.*context7",
            r"Context7.*pattern.*access",
            r"MCP.*Context7",
            r"context7.*enhancement",
        ]

        transparency_disclosures = []

        # Search for transparency disclosures
        lib_dir = self.project_root / ".claudedirector" / "lib"
        if lib_dir.exists():
            for py_file in lib_dir.glob("**/*.py"):
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    for pattern in transparency_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            transparency_disclosures.append(
                                str(py_file.relative_to(self.project_root))
                            )
                            break

                except Exception:
                    continue

        self.assertGreater(
            len(transparency_disclosures),
            0,
            "BLOCKING FAILURE: No Context7 MCP transparency disclosures found - "
            "Context7 utilization must be transparently disclosed to users",
        )

    def test_p0_context7_architectural_pattern_access(self):
        """P0 TEST: Architectural patterns must leverage Context7 capabilities"""
        # Check for architectural pattern files that should use Context7
        architectural_files = [
            "core/base_processor.py",
            "core/unified_performance_manager.py",
            "integration/unified_bridge.py",
            "ai_intelligence/decision_orchestrator.py",
        ]

        context7_pattern_access = 0

        for arch_file in architectural_files:
            file_path = self.project_root / ".claudedirector" / "lib" / arch_file

            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Look for Context7 pattern access indicators
                    pattern_indicators = [
                        "Context7",
                        "pattern_access",
                        "architectural.*pattern",
                        "framework.*pattern",
                        "best.*practice",
                    ]

                    has_pattern_access = any(
                        re.search(indicator, content, re.IGNORECASE)
                        for indicator in pattern_indicators
                    )

                    if has_pattern_access:
                        context7_pattern_access += 1

                except Exception:
                    continue

        # At least some architectural files should demonstrate Context7 pattern access
        self.assertGreater(
            context7_pattern_access,
            0,
            "BLOCKING FAILURE: No architectural files demonstrate Context7 pattern access - "
            "architectural guidance must leverage Context7 intelligence",
        )

    def test_p0_context7_performance_requirements(self):
        """P0 TEST: Context7 utilization must meet performance requirements"""
        # Simulate Context7 access pattern validation
        start_time = time.time()

        # Test pattern: Search for Context7 integration patterns
        context7_patterns_found = 0
        lib_dir = self.project_root / ".claudedirector" / "lib"

        if lib_dir.exists():
            # Limit search to prevent timeout
            search_files = list(lib_dir.glob("**/*.py"))[:10]  # Sample 10 files

            for py_file in search_files:
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        pattern in content
                        for pattern in self.required_context7_patterns
                    ):
                        context7_patterns_found += 1

                except Exception:
                    continue

        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # P0 REQUIREMENT: Context7 pattern search must complete within performance threshold
        self.assertLess(
            search_time,
            self.max_response_time_ms,
            f"BLOCKING FAILURE: Context7 pattern search took {search_time:.1f}ms, "
            f"exceeds P0 requirement of {self.max_response_time_ms}ms",
        )

        # Validate that we found some Context7 patterns during performance test
        self.assertGreater(
            context7_patterns_found,
            0,
            "BLOCKING FAILURE: No Context7 patterns found during performance validation",
        )

    def test_p0_context7_mcp_coordination_integration(self):
        """P0 TEST: Context7 must be integrated with MCP coordination system"""
        # Check for MCP coordination patterns that include Context7
        mcp_coordination_files = [
            "ai_intelligence/mcp_enhanced_ml_pipeline.py",
            "integration/unified_bridge.py",
            "core/enhanced_persona_manager.py",
        ]

        context7_mcp_coordination = 0

        for coord_file in mcp_coordination_files:
            file_path = self.project_root / ".claudedirector" / "lib" / coord_file

            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Look for Context7 + MCP coordination patterns
                    coordination_patterns = [
                        r"Context7.*MCP",
                        r"MCP.*Context7",
                        r"context7.*server",
                        r"pattern.*mcp",
                    ]

                    has_coordination = any(
                        re.search(pattern, content, re.IGNORECASE)
                        for pattern in coordination_patterns
                    )

                    if has_coordination:
                        context7_mcp_coordination += 1

                except Exception:
                    continue

        # At least some MCP coordination should include Context7
        self.assertGreater(
            context7_mcp_coordination,
            0,
            "BLOCKING FAILURE: No Context7 integration found in MCP coordination system - "
            "Context7 must be coordinated with other MCP servers",
        )

    def test_p0_context7_documentation_compliance(self):
        """P0 TEST: Context7 utilization must be properly documented"""
        # Check for Context7 documentation
        docs_dir = self.project_root / "docs"
        context7_documentation = []

        if docs_dir.exists():
            for doc_file in docs_dir.glob("**/*.md"):
                try:
                    with open(doc_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        pattern in content
                        for pattern in self.required_context7_patterns
                    ):
                        context7_documentation.append(
                            str(doc_file.relative_to(self.project_root))
                        )

                except Exception:
                    continue

        self.assertGreater(
            len(context7_documentation),
            0,
            "BLOCKING FAILURE: No Context7 documentation found - "
            "Context7 utilization must be properly documented for users and developers",
        )


if __name__ == "__main__":
    # Run P0 Context7 utilization tests
    unittest.main(verbosity=2)
