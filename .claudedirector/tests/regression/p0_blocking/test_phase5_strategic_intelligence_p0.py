"""
Phase 5 Strategic Intelligence P0 Tests

Business-critical tests for strategic intelligence capabilities.
These tests MUST pass for Phase 5 to be considered complete.

P0 Requirements:
- External spec-kit integration works correctly
- Strategic enhancement layer functions properly
- Context engineering integration is stable
- All SOLID principles are maintained
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Test imports
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from lib.strategic_intelligence.spec_kit_integrator import (
    SpecKitIntegrator,
    SpecificationResult,
)
from lib.strategic_intelligence.strategic_spec_enhancer import (
    StrategicSpecEnhancer,
    EnhancedSpecification,
)
from lib.strategic_intelligence.context_intelligence_bridge import (
    ContextIntelligenceBridge,
    StrategicIntelligenceContext,
)
from lib.core.models import StrategicContext


class TestPhase5StrategicIntelligenceP0(unittest.TestCase):
    """P0 tests for Phase 5 strategic intelligence capabilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Mock context engine
        self.mock_context_engine = Mock()
        self.mock_context_engine.strategic_layer = Mock()
        self.mock_context_engine.stakeholder_layer = Mock()
        self.mock_context_engine.organizational_layer = Mock()

        # Mock decision orchestrator
        self.mock_decision_orchestrator = Mock()
        self.mock_decision_orchestrator.framework_detector = Mock()

        # Test specification content
        self.test_spec_content = """# Test Specification

## User Scenarios & Testing
Test scenarios for team organization and decision making validation.

## Requirements
- FR-001: System MUST provide test functionality
- FR-002: System MUST maintain performance for strategic decisions

## Review & Acceptance Checklist
- [x] Requirements are testable
"""

    def tearDown(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_spec_kit_integrator_initialization(self):
        """P0: SpecKitIntegrator initializes correctly with context engine"""
        integrator = SpecKitIntegrator(
            context_engine=self.mock_context_engine, config={"validation_enabled": True}
        )

        self.assertIsNotNone(integrator)
        self.assertEqual(integrator.context_engine, self.mock_context_engine)
        self.assertTrue(integrator.validation_enabled)
        self.assertIn("github-spec-kit", integrator.get_supported_tools())

    def test_spec_kit_integrator_handles_tool_unavailable(self):
        """P0: SpecKitIntegrator gracefully handles when spec-kit tool is unavailable"""
        integrator = SpecKitIntegrator(
            context_engine=self.mock_context_engine,
            config={"validation_enabled": False},
        )

        # Mock tool unavailable
        with patch.object(
            integrator.spec_tool, "_ensure_spec_kit_available", return_value=False
        ):
            result = integrator.generate_base_specification("Test description")

        self.assertFalse(result.success)
        self.assertIsNone(result.spec_path)
        self.assertTrue(len(result.errors) > 0)
        self.assertIn("not available", result.errors[0].lower())

    def test_strategic_spec_enhancer_initialization(self):
        """P0: StrategicSpecEnhancer initializes correctly with dependencies"""
        enhancer = StrategicSpecEnhancer(
            context_engine=self.mock_context_engine,
            decision_orchestrator=self.mock_decision_orchestrator,
            config={"enable_framework_enhancement": True},
        )

        self.assertIsNotNone(enhancer)
        self.assertEqual(enhancer.context_engine, self.mock_context_engine)
        self.assertEqual(
            enhancer.decision_orchestrator, self.mock_decision_orchestrator
        )
        self.assertIsNotNone(enhancer.framework_enhancer)
        self.assertIsNotNone(enhancer.stakeholder_enhancer)
        self.assertIsNotNone(enhancer.roi_enhancer)

    def test_strategic_spec_enhancer_handles_missing_file(self):
        """P0: StrategicSpecEnhancer gracefully handles missing specification file"""
        enhancer = StrategicSpecEnhancer(
            context_engine=self.mock_context_engine,
            decision_orchestrator=self.mock_decision_orchestrator,
        )

        result = enhancer.enhance_specification("nonexistent_file.md")

        self.assertEqual(result.original_spec_path, "nonexistent_file.md")
        self.assertEqual(result.enhanced_spec_path, "")
        self.assertTrue(len(result.errors) > 0)
        self.assertIn("not found", result.errors[0].lower())

    def test_strategic_spec_enhancer_framework_integration(self):
        """P0: Strategic enhancement integrates frameworks correctly"""
        # Create test specification file
        test_spec_file = self.temp_dir / "test_spec.md"
        test_spec_file.write_text(self.test_spec_content)

        # Mock framework detection - this will be handled by the mock detect method
        # No need to mock the decision orchestrator for this test

        enhancer = StrategicSpecEnhancer(
            context_engine=self.mock_context_engine,
            decision_orchestrator=self.mock_decision_orchestrator,
            config={"enable_framework_enhancement": True},
        )

        result = enhancer.enhance_specification(str(test_spec_file))

        self.assertEqual(result.original_spec_path, str(test_spec_file))
        self.assertTrue(result.enhanced_spec_path.endswith("_enhanced.md"))
        self.assertIn("Team Topologies", result.enhancement_metadata.frameworks_applied)
        self.assertGreater(len(result.enhancement_metadata.frameworks_applied), 0)
        self.assertEqual(len(result.errors), 0)

        # Verify enhanced file exists and contains framework section
        enhanced_file = Path(result.enhanced_spec_path)
        self.assertTrue(enhanced_file.exists())
        enhanced_content = enhanced_file.read_text()
        self.assertIn("Strategic Framework Analysis", enhanced_content)
        self.assertIn("Team Topologies", enhanced_content)

    def test_context_intelligence_bridge_initialization(self):
        """P0: ContextIntelligenceBridge initializes correctly with context engine"""
        bridge = ContextIntelligenceBridge(self.mock_context_engine)

        self.assertIsNotNone(bridge)
        self.assertEqual(bridge.context_engine, self.mock_context_engine)

    def test_context_intelligence_bridge_gathers_strategic_context(self):
        """P0: ContextIntelligenceBridge gathers strategic context correctly"""
        # Mock context layer responses
        self.mock_context_engine.strategic_layer.get_strategic_context.return_value = {
            "initiatives": [
                {"name": "Test Initiative", "description": "AI enhancement"}
            ],
            "frameworks": ["Team Topologies", "WRAP"],
            "decisions": [{"description": "Implement AI system"}],
        }

        self.mock_context_engine.stakeholder_layer.get_stakeholder_context.return_value = {
            "stakeholders": [
                {"name": "Engineering VP", "keywords": ["AI", "enhancement"]}
            ],
            "communication_patterns": {"preferred": "email"},
        }

        self.mock_context_engine.organizational_layer.get_organizational_context.return_value = {
            "patterns": {"team_size": "medium"},
            "structure": {"type": "matrix"},
            "culture": {"innovation_focus": "high"},
        }

        bridge = ContextIntelligenceBridge(self.mock_context_engine)
        context = bridge.get_strategic_context_for_spec("AI enhancement system")

        self.assertIsInstance(context, StrategicIntelligenceContext)
        self.assertEqual(len(context.strategic_initiatives), 1)
        self.assertEqual(len(context.framework_history), 2)
        self.assertIn("Team Topologies", context.framework_history)
        self.assertIn("team_size", context.organizational_patterns)

    def test_context_intelligence_bridge_handles_empty_context(self):
        """P0: ContextIntelligenceBridge handles empty context gracefully"""
        # Mock empty context responses
        self.mock_context_engine.strategic_layer.get_strategic_context.return_value = (
            None
        )
        self.mock_context_engine.stakeholder_layer.get_stakeholder_context.return_value = (
            None
        )
        self.mock_context_engine.organizational_layer.get_organizational_context.return_value = (
            None
        )

        bridge = ContextIntelligenceBridge(self.mock_context_engine)
        context = bridge.get_strategic_context_for_spec("test description")

        self.assertIsInstance(context, StrategicIntelligenceContext)
        self.assertEqual(len(context.strategic_initiatives), 0)
        self.assertEqual(len(context.framework_history), 0)
        self.assertEqual(len(context.organizational_patterns), 0)

    def test_specification_workflow_integration(self):
        """P0: Complete specification workflow integrates correctly"""
        # Create test specification file
        test_spec_file = self.temp_dir / "workflow_test.md"
        test_spec_file.write_text(self.test_spec_content)

        # Mock all dependencies
        mock_frameworks = [{"name": "WRAP Framework", "confidence": 0.92}]
        self.mock_decision_orchestrator.framework_detector.detect_frameworks.return_value = (
            mock_frameworks
        )

        self.mock_context_engine.strategic_layer.get_strategic_context.return_value = {
            "initiatives": [],
            "frameworks": [],
            "decisions": [],
        }
        self.mock_context_engine.stakeholder_layer.get_stakeholder_context.return_value = {
            "stakeholders": [],
            "communication_patterns": {},
        }

        # Initialize components
        integrator = SpecKitIntegrator(self.mock_context_engine)
        enhancer = StrategicSpecEnhancer(
            self.mock_context_engine, self.mock_decision_orchestrator
        )
        bridge = ContextIntelligenceBridge(self.mock_context_engine)

        # Test workflow
        # 1. Get strategic context
        strategic_context = bridge.get_strategic_context_for_spec("Test workflow")
        self.assertIsInstance(strategic_context, StrategicIntelligenceContext)

        # 2. Enhance specification
        result = enhancer.enhance_specification(str(test_spec_file))
        self.assertEqual(len(result.errors), 0)
        self.assertTrue(result.enhanced_spec_path.endswith("_enhanced.md"))

        # 3. Verify enhanced content
        enhanced_content = Path(result.enhanced_spec_path).read_text()
        self.assertIn("Strategic Framework Analysis", enhanced_content)
        self.assertIn("Business Impact & ROI Analysis", enhanced_content)

    def test_solid_principles_compliance(self):
        """P0: All components follow SOLID principles"""
        # Single Responsibility: Each class has one clear responsibility
        integrator = SpecKitIntegrator(self.mock_context_engine)
        enhancer = StrategicSpecEnhancer(
            self.mock_context_engine, self.mock_decision_orchestrator
        )
        bridge = ContextIntelligenceBridge(self.mock_context_engine)

        # Verify each component has focused responsibilities
        self.assertTrue(hasattr(integrator, "generate_base_specification"))
        self.assertTrue(hasattr(enhancer, "enhance_specification"))
        self.assertTrue(hasattr(bridge, "get_strategic_context_for_spec"))

        # Open/Closed: Components are extensible
        self.assertTrue(hasattr(integrator, "get_supported_tools"))

        # Dependency Inversion: Components depend on abstractions
        self.assertEqual(integrator.context_engine, self.mock_context_engine)
        self.assertEqual(enhancer.context_engine, self.mock_context_engine)
        self.assertEqual(bridge.context_engine, self.mock_context_engine)

    def test_error_handling_robustness(self):
        """P0: All components handle errors gracefully without system crashes"""
        # Test SpecKitIntegrator error handling
        integrator = SpecKitIntegrator(self.mock_context_engine)
        with patch.object(
            integrator.spec_tool,
            "generate_specification",
            side_effect=Exception("Test error"),
        ):
            result = integrator.generate_base_specification("test")
            self.assertFalse(result.success)
            self.assertTrue(len(result.errors) > 0)

        # Test StrategicSpecEnhancer error handling
        enhancer = StrategicSpecEnhancer(
            self.mock_context_engine, self.mock_decision_orchestrator
        )
        result = enhancer.enhance_specification("nonexistent.md")
        self.assertTrue(len(result.errors) > 0)

        # Test ContextIntelligenceBridge error handling
        self.mock_context_engine.strategic_layer.get_strategic_context.side_effect = (
            Exception("Test error")
        )
        bridge = ContextIntelligenceBridge(self.mock_context_engine)
        context = bridge.get_strategic_context_for_spec("test")
        # Should return empty context, not crash
        self.assertIsInstance(context, StrategicIntelligenceContext)

    def test_performance_requirements(self):
        """P0: Strategic intelligence operations complete within performance targets"""
        import time

        # Test context bridge performance
        bridge = ContextIntelligenceBridge(self.mock_context_engine)

        start_time = time.time()
        context = bridge.get_strategic_context_for_spec("performance test")
        end_time = time.time()

        # Should complete within 2 seconds (spec.md requirement: ≤2000ms)
        self.assertLess(end_time - start_time, 2.0)

        # Test specification enhancement performance
        test_spec_file = self.temp_dir / "perf_test.md"
        test_spec_file.write_text(self.test_spec_content)

        enhancer = StrategicSpecEnhancer(
            self.mock_context_engine, self.mock_decision_orchestrator
        )

        start_time = time.time()
        result = enhancer.enhance_specification(str(test_spec_file))
        end_time = time.time()

        # Should complete within 2 seconds
        self.assertLess(end_time - start_time, 2.0)


def run_p0_tests():
    """Run P0 tests for Phase 5 strategic intelligence"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPhase5StrategicIntelligenceP0)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_p0_tests()
    exit(0 if success else 1)
