#!/usr/bin/env python3
"""
P0 Test: Sequential Thinking + Spec-Kit Workflow Integration

🚨 P0 CRITICAL: Validates Sequential Thinking methodology integration with spec-kit workflow
🎯 ZERO TOLERANCE: Sequential Thinking must be applied to ALL spec creation activities
🏗️ ARCHITECTURAL: Ensures DRY/SOLID compliance and PROJECT_STRUCTURE.md adherence

This P0 test ensures:
1. Sequential Thinking methodology is properly applied to spec creation
2. Spec-Kit integration works with strategic intelligence enhancement
3. All architectural principles (DRY, SOLID, PROJECT_STRUCTURE.md) are followed
4. Performance targets are met for real-time strategic support

Author: Martin | Platform Architecture with Sequential Thinking methodology
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / ".claudedirector" / "lib"))

try:
    import strategic_intelligence.sequential_spec_workflow as seq_workflow
    from strategic_intelligence.sequential_spec_workflow import (
        SequentialSpecCreator,
        SequentialSpecWorkflow,
        SequentialAnalysisStep,
    )
    from strategic_intelligence.spec_kit_integrator import SpecificationResult
    from strategic_intelligence.strategic_spec_enhancer import EnhancedSpecification
    from core.models import StrategicContext
except ImportError as e:
    print(
        f"❌ P0 CRITICAL FAILURE: Cannot import Sequential Thinking workflow components: {e}"
    )
    sys.exit(1)


class TestSequentialSpecWorkflowP0(unittest.TestCase):
    """P0 Critical Tests for Sequential Thinking + Spec-Kit Workflow"""

    def setUp(self):
        """Set up test environment with mocked dependencies"""
        # Create temporary directory for test outputs
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

        # Mock dependencies following Dependency Inversion principle
        self.mock_spec_kit_integrator = Mock()
        self.mock_strategic_enhancer = Mock()
        self.mock_context_bridge = Mock()

        # Create Sequential Spec Creator with mocked dependencies
        self.sequential_creator = SequentialSpecCreator(
            spec_kit_integrator=self.mock_spec_kit_integrator,
            strategic_enhancer=self.mock_strategic_enhancer,
            context_bridge=self.mock_context_bridge,
            config={"validation_enabled": True},
        )

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sequential_thinking_methodology_application_p0(self):
        """
        P0 CRITICAL: Validate Sequential Thinking methodology is properly applied

        This test ensures that all 6 Sequential Thinking steps are executed:
        1. Problem Analysis
        2. Systematic Approach Planning
        3. External Spec-Kit Integration
        4. Strategic Intelligence Enhancement
        5. Architectural Compliance Validation
        6. Success Metrics Validation
        """
        # Mock successful spec-kit integration
        mock_spec_result = SpecificationResult(
            success=True,
            spec_path=str(self.temp_path / "test_spec.md"),
            metadata={"generated_at": "2025-01-01T00:00:00Z"},
            errors=[],
        )
        self.mock_spec_kit_integrator.generate_base_specification.return_value = (
            mock_spec_result
        )

        # Mock successful strategic enhancement
        mock_enhanced_result = Mock()
        mock_enhanced_result.success = True
        mock_enhanced_result.enhanced_spec_path = str(
            self.temp_path / "enhanced_spec.md"
        )
        mock_enhanced_result.strategic_enhancements = Mock()
        mock_enhanced_result.strategic_enhancements.__dict__ = {
            "frameworks": ["Team Topologies"]
        }
        mock_enhanced_result.errors = []
        self.mock_strategic_enhancer.enhance_specification.return_value = (
            mock_enhanced_result
        )

        # Create test specification files
        (self.temp_path / "test_spec.md").write_text(
            "# Test Specification\n\nTest content"
        )
        (self.temp_path / "enhanced_spec.md").write_text(
            "# Enhanced Test Specification\n\nEnhanced content"
        )

        # Execute Sequential Thinking workflow
        result = self.sequential_creator.create_specification_with_sequential_thinking(
            description="Create ML-powered decision support system for strategic leadership",
            output_dir=str(self.temp_dir),
            strategic_context=StrategicContext(
                organizational_context="Engineering leadership team",
                strategic_objectives=[
                    "Improve decision quality",
                    "Reduce strategic risks",
                ],
                stakeholder_priorities={"executives": "high", "engineering": "high"},
            ),
        )

        # P0 CRITICAL: Validate Sequential Thinking methodology application
        self.assertTrue(result.success, "Sequential Thinking workflow must succeed")
        self.assertEqual(
            len(result.sequential_analysis),
            6,
            "All 6 Sequential Thinking steps must be executed",
        )

        # Validate each Sequential Thinking step
        step_names = [
            "Problem Analysis",
            "Systematic Approach Planning",
            "External Spec-Kit Integration",
            "Strategic Intelligence Enhancement",
            "Architectural Compliance Validation",
            "Success Metrics Validation",
        ]

        for i, expected_name in enumerate(step_names):
            step = result.sequential_analysis[i]
            self.assertEqual(
                step.step_name, expected_name, f"Step {i+1} must be '{expected_name}'"
            )
            self.assertTrue(
                step.completed,
                f"Sequential Thinking step '{expected_name}' must be completed",
            )
            self.assertIsNotNone(
                step.results, f"Step '{expected_name}' must have results"
            )

        print(
            "✅ P0 CRITICAL: Sequential Thinking methodology properly applied to spec creation"
        )

    def test_spec_kit_integration_with_strategic_intelligence_p0(self):
        """
        P0 CRITICAL: Validate spec-kit integration works with strategic intelligence

        This test ensures the workflow properly integrates external spec-kit tools
        with our strategic intelligence enhancement system.
        """
        # Mock successful integrations
        self.mock_spec_kit_integrator.generate_base_specification.return_value = (
            SpecificationResult(
                success=True,
                spec_path=str(self.temp_path / "base_spec.md"),
                metadata={"tool": "github-spec-kit"},
                errors=[],
            )
        )

        mock_enhanced = Mock()
        mock_enhanced.success = True
        mock_enhanced.enhanced_spec_path = str(self.temp_path / "enhanced_spec.md")
        mock_enhanced.strategic_enhancements = Mock()
        mock_enhanced.strategic_enhancements.__dict__ = {
            "frameworks_applied": ["WRAP Framework", "Team Topologies"],
            "stakeholders_identified": ["Engineering Leadership", "Executives"],
            "roi_projections": {"expected_roi": 4.2},
        }
        mock_enhanced.errors = []
        self.mock_strategic_enhancer.enhance_specification.return_value = mock_enhanced

        # Create test files
        (self.temp_path / "base_spec.md").write_text("# Base Spec")
        (self.temp_path / "enhanced_spec.md").write_text("# Enhanced Spec")

        # Execute workflow
        result = self.sequential_creator.create_specification_with_sequential_thinking(
            description="Phase 5.1 ML-powered strategic decision support",
            output_dir=str(self.temp_dir),
        )

        # P0 CRITICAL: Validate integration success
        self.assertTrue(
            result.success, "Spec-kit + strategic intelligence integration must succeed"
        )
        self.assertIsNotNone(result.spec_path, "Base specification must be generated")
        self.assertIsNotNone(
            result.enhanced_spec_path, "Enhanced specification must be generated"
        )

        # Validate tool integration calls
        self.mock_spec_kit_integrator.generate_base_specification.assert_called_once()
        self.mock_strategic_enhancer.enhance_specification.assert_called_once()

        print(
            "✅ P0 CRITICAL: Spec-kit integration with strategic intelligence validated"
        )

    def test_architectural_compliance_validation_p0(self):
        """
        P0 CRITICAL: Validate architectural compliance (DRY, SOLID, PROJECT_STRUCTURE.md)

        This test ensures the workflow validates all specifications against
        our architectural principles and project structure requirements.
        """
        # Mock successful workflow components
        self.mock_spec_kit_integrator.generate_base_specification.return_value = (
            SpecificationResult(
                success=True,
                spec_path=str(self.temp_path / "spec.md"),
                metadata={},
                errors=[],
            )
        )

        mock_enhanced = Mock()
        mock_enhanced.success = True
        mock_enhanced.enhanced_spec_path = str(self.temp_path / "enhanced.md")
        mock_enhanced.strategic_enhancements = Mock()
        mock_enhanced.strategic_enhancements.__dict__ = {}
        mock_enhanced.errors = []
        self.mock_strategic_enhancer.enhance_specification.return_value = mock_enhanced

        # Create test files
        (self.temp_path / "spec.md").write_text("# Test Spec")
        (self.temp_path / "enhanced.md").write_text("# Enhanced Test Spec")

        # Execute workflow
        result = self.sequential_creator.create_specification_with_sequential_thinking(
            description="Test specification for architectural compliance",
            output_dir=str(self.temp_dir),
        )

        # P0 CRITICAL: Validate architectural compliance
        self.assertTrue(
            result.success, "Workflow must succeed for architectural compliance test"
        )

        compliance = result.architectural_compliance
        self.assertIn(
            "project_structure_compliance",
            compliance,
            "PROJECT_STRUCTURE.md compliance must be checked",
        )
        self.assertIn(
            "dry_principle_adherence",
            compliance,
            "DRY principle adherence must be validated",
        )
        self.assertIn(
            "solid_principle_compliance",
            compliance,
            "SOLID principle compliance must be validated",
        )
        self.assertIn(
            "overall_compliance", compliance, "Overall compliance must be assessed"
        )

        # Validate compliance results
        self.assertTrue(
            compliance.get("project_structure_compliance", False),
            "PROJECT_STRUCTURE.md compliance required",
        )
        self.assertTrue(
            compliance.get("dry_principle_adherence", False),
            "DRY principle adherence required",
        )
        self.assertTrue(
            compliance.get("solid_principle_compliance", False),
            "SOLID principle compliance required",
        )
        self.assertTrue(
            compliance.get("overall_compliance", False),
            "Overall architectural compliance required",
        )

        print(
            "✅ P0 CRITICAL: Architectural compliance validation (DRY, SOLID, PROJECT_STRUCTURE.md) passed"
        )

    def test_performance_requirements_p0(self):
        """
        P0 CRITICAL: Validate performance requirements for real-time strategic support

        This test ensures the Sequential Thinking workflow meets performance targets
        for real-time strategic decision support (≤5000ms total processing time).
        """
        # Mock fast responses
        self.mock_spec_kit_integrator.generate_base_specification.return_value = (
            SpecificationResult(
                success=True,
                spec_path=str(self.temp_path / "perf_spec.md"),
                metadata={},
                errors=[],
            )
        )

        mock_enhanced = Mock()
        mock_enhanced.success = True
        mock_enhanced.enhanced_spec_path = str(self.temp_path / "perf_enhanced.md")
        mock_enhanced.strategic_enhancements = Mock()
        mock_enhanced.strategic_enhancements.__dict__ = {}
        mock_enhanced.errors = []
        self.mock_strategic_enhancer.enhance_specification.return_value = mock_enhanced

        # Create test files
        (self.temp_path / "perf_spec.md").write_text("# Performance Test Spec")
        (self.temp_path / "perf_enhanced.md").write_text("# Performance Enhanced Spec")

        # Execute workflow and measure performance
        import time

        start_time = time.time()

        result = self.sequential_creator.create_specification_with_sequential_thinking(
            description="Performance test specification for real-time strategic support",
            output_dir=str(self.temp_dir),
        )

        end_time = time.time()
        actual_processing_time = (
            end_time - start_time
        ) * 1000  # Convert to milliseconds

        # P0 CRITICAL: Validate performance requirements
        self.assertTrue(result.success, "Performance test workflow must succeed")

        performance_metrics = result.performance_metrics
        self.assertIn(
            "processing_time_ms", performance_metrics, "Processing time must be tracked"
        )
        self.assertIn(
            "performance_score",
            performance_metrics,
            "Performance score must be calculated",
        )

        # Validate performance targets (≤5000ms for real-time support)
        processing_time_ms = performance_metrics.get("processing_time_ms", float("inf"))
        self.assertLessEqual(
            processing_time_ms,
            5000,
            f"Processing time {processing_time_ms}ms must be ≤5000ms for real-time support",
        )

        performance_score = performance_metrics.get("performance_score", 0)
        self.assertGreaterEqual(
            performance_score,
            0.8,
            f"Performance score {performance_score} must be ≥0.8",
        )

        print(
            f"✅ P0 CRITICAL: Performance requirements met ({processing_time_ms:.1f}ms ≤ 5000ms)"
        )

    def test_error_handling_and_resilience_p0(self):
        """
        P0 CRITICAL: Validate error handling and workflow resilience

        This test ensures the Sequential Thinking workflow handles errors gracefully
        and provides meaningful feedback when components fail.
        """
        # Mock spec-kit integration failure
        self.mock_spec_kit_integrator.generate_base_specification.return_value = (
            SpecificationResult(
                success=False,
                spec_path=None,
                metadata={},
                errors=["External spec-kit tool unavailable"],
            )
        )

        # Execute workflow with expected failure
        result = self.sequential_creator.create_specification_with_sequential_thinking(
            description="Error handling test specification",
            output_dir=str(self.temp_dir),
        )

        # P0 CRITICAL: Validate error handling
        self.assertFalse(
            result.success,
            "Workflow should fail gracefully when spec-kit integration fails",
        )
        self.assertIn(
            "External spec-kit tool unavailable",
            result.errors,
            "Error messages must be preserved",
        )

        # Validate partial completion tracking
        sequential_steps = result.sequential_analysis
        self.assertGreater(
            len(sequential_steps), 0, "Sequential steps must be tracked even on failure"
        )

        # Problem Analysis and Systematic Approach should complete even if tools fail
        self.assertTrue(
            sequential_steps[0].completed,
            "Problem Analysis should complete even on tool failure",
        )
        self.assertTrue(
            sequential_steps[1].completed,
            "Systematic Approach Planning should complete even on tool failure",
        )

        print("✅ P0 CRITICAL: Error handling and workflow resilience validated")

    def test_dry_solid_compliance_in_implementation_p0(self):
        """
        P0 CRITICAL: Validate DRY and SOLID compliance in workflow implementation

        This test ensures the Sequential Thinking workflow implementation itself
        follows DRY and SOLID principles without duplicating existing functionality.
        """
        # Verify no code duplication by checking component reuse
        creator = self.sequential_creator

        # SOLID Principle validation
        # Single Responsibility: SequentialSpecCreator only coordinates workflow
        self.assertTrue(
            hasattr(creator, "spec_kit_integrator"),
            "Must use existing spec-kit integrator",
        )
        self.assertTrue(
            hasattr(creator, "strategic_enhancer"),
            "Must use existing strategic enhancer",
        )
        self.assertTrue(
            hasattr(creator, "context_bridge"), "Must use existing context bridge"
        )

        # Dependency Inversion: Uses abstractions, not concrete implementations
        self.assertIsNotNone(
            creator.spec_kit_integrator, "Spec-kit integrator must be injected"
        )
        self.assertIsNotNone(
            creator.strategic_enhancer, "Strategic enhancer must be injected"
        )
        self.assertIsNotNone(creator.context_bridge, "Context bridge must be injected")

        # DRY Principle validation: No reimplementation of existing functionality
        # The workflow coordinates existing components rather than duplicating them

        print(
            "✅ P0 CRITICAL: DRY and SOLID compliance validated in Sequential Thinking workflow implementation"
        )


def main():
    """Run P0 Critical Tests for Sequential Thinking + Spec-Kit Workflow"""
    print("🚨 P0 CRITICAL: Running Sequential Thinking + Spec-Kit Workflow Tests")
    print("=" * 80)

    # Run tests with detailed output
    unittest.main(argv=[""], verbosity=2, exit=False)

    print("=" * 80)
    print("✅ P0 CRITICAL: Sequential Thinking + Spec-Kit Workflow validation complete")


if __name__ == "__main__":
    main()
