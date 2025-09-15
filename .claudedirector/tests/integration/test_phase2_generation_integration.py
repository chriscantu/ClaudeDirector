#!/usr/bin/env python3
"""
Integration Tests for Phase 2 Generation Compliance System
==========================================================

🏗️ Martin | Platform Architecture with Sequential Thinking + Context7 MCP Integration

INTEGRATION TEST COVERAGE:
✅ Real UnifiedFactory integration with Phase 2 components
✅ Actual PROJECT_STRUCTURE.md parsing and compliance
✅ End-to-end generation workflow validation
✅ Performance benchmarking and optimization validation
✅ Cross-component interaction testing
✅ Real-world usage scenario simulation

SEQUENTIAL THINKING APPLIED:
1. Problem Definition: Validate Phase 2 components work together in real environment
2. Root Cause Analysis: Integration issues often arise from component boundaries
3. Solution Architecture: Comprehensive integration testing with real dependencies
4. Implementation Strategy: Real environment testing with performance monitoring
5. Strategic Enhancement: Context7 MCP integration validation
6. Success Metrics: <2s end-to-end performance, 100% integration success

Author: Strategic Team (Diego, Martin, Camille) with Sequential Thinking methodology
"""

import unittest
import time
import tempfile
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import shutil
import json

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .claudedirector.lib.core.generation.solid_template_engine import (
        SOLIDTemplateEngine,
        SOLIDPrinciple,
        TemplateContext,
        GenerationResult,
    )
    from .claudedirector.lib.core.generation.structure_aware_placement_engine import (
        StructureAwarePlacementEngine,
        ComponentCategory,
        PlacementRule,
        PlacementResult,
    )
    from .claudedirector.lib.core.unified_factory import (
        UnifiedFactory,
        ComponentType,
        create_solid_template_engine,
        create_structure_aware_placement_engine,
    )

    IMPORTS_AVAILABLE = True
except ImportError:
    # Fallback for test environment
    sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
    try:
        from lib.core.generation.solid_template_engine import (
            SOLIDTemplateEngine,
            SOLIDPrinciple,
            TemplateContext,
            GenerationResult,
        )
        from lib.core.generation.structure_aware_placement_engine import (
            StructureAwarePlacementEngine,
            ComponentCategory,
            PlacementRule,
            PlacementResult,
        )
        from lib.core.unified_factory import (
            UnifiedFactory,
            ComponentType,
            create_solid_template_engine,
            create_structure_aware_placement_engine,
        )

        IMPORTS_AVAILABLE = True
    except ImportError:
        IMPORTS_AVAILABLE = False


class TestPhase2GenerationIntegration(unittest.TestCase):
    """
    Integration tests for Phase 2 Generation Compliance System

    Tests real component interactions and end-to-end workflows
    """

    @classmethod
    def setUpClass(cls):
        """Set up integration test environment with real project structure"""
        if not IMPORTS_AVAILABLE:
            raise unittest.SkipTest(
                "Phase 2 components not available for integration testing"
            )

        cls.temp_dir = Path(tempfile.mkdtemp())
        cls.integration_project = cls.temp_dir / "integration_test_project"
        cls.integration_project.mkdir(parents=True, exist_ok=True)

        # Create realistic project structure
        cls._create_realistic_project_structure()

        # Performance tracking
        cls.performance_metrics = {
            "initialization_times": [],
            "generation_times": [],
            "placement_times": [],
            "end_to_end_times": [],
        }

    @classmethod
    def tearDownClass(cls):
        """Clean up integration test environment and report performance"""
        if cls.temp_dir.exists():
            shutil.rmtree(cls.temp_dir)

        # Report performance metrics
        if hasattr(cls, "performance_metrics"):
            cls._report_performance_metrics()

    @classmethod
    def _create_realistic_project_structure(cls):
        """Create realistic project structure for integration testing"""
        # Create PROJECT_STRUCTURE.md with comprehensive structure
        project_structure_content = """# ClaudeDirector Project Structure

## Core System Components (Lines 71-75)

### .claudedirector/lib/core/
**Purpose**: Foundational system components and core infrastructure

#### Foundational Components
- `database.py` - SQLite + DuckDB + Faiss hybrid database architecture
- `config.py` - Configuration management and environment setup
- `models.py` - Core data models and schemas
- `validation.py` - Input validation and data integrity

#### Generation Components (.claudedirector/lib/core/generation/)
- `solid_template_engine.py` - SOLID principle-enforced code generation
- `structure_aware_placement_engine.py` - Automatic PROJECT_STRUCTURE.md compliance
- `__init__.py` - Generation module exports

#### Validation Components (.claudedirector/lib/core/validation/)
- `unified_prevention_engine.py` - Consolidated validation and prevention
- `proactive_compliance_engine.py` - Proactive architectural compliance
- Process compliance enforcement (removed - non-functional)

### .claudedirector/lib/ai_intelligence/
**Purpose**: AI Enhancement System for strategic intelligence

- `decision_orchestrator.py` - Decision intelligence coordination
- `enhanced_framework_detection.py` - Strategic framework recognition
- `mcp_integration.py` - MCP server coordination

### .claudedirector/tests/
**Purpose**: Comprehensive testing infrastructure

#### Unit Tests (.claudedirector/tests/unit/)
- `core/` - Core component unit tests
- `ai_intelligence/` - AI system unit tests
- `integration/` - Cross-component integration tests

#### P0 Tests (.claudedirector/tests/regression/p0_blocking/)
- `test_*_p0.py` - Business-critical blocking tests

#### Integration Tests (.claudedirector/tests/integration/)
- `test_*_integration.py` - System integration validation
"""

        # Create directory structure
        docs_dir = cls.integration_project / "docs" / "architecture"
        docs_dir.mkdir(parents=True, exist_ok=True)

        project_structure_file = docs_dir / "PROJECT_STRUCTURE.md"
        project_structure_file.write_text(project_structure_content)

        # Create lib directory structure
        lib_core = cls.integration_project / ".claudedirector" / "lib" / "core"
        lib_core.mkdir(parents=True, exist_ok=True)

        generation_dir = lib_core / "generation"
        generation_dir.mkdir(parents=True, exist_ok=True)

        validation_dir = lib_core / "validation"
        validation_dir.mkdir(parents=True, exist_ok=True)

        ai_intelligence_dir = (
            cls.integration_project / ".claudedirector" / "lib" / "ai_intelligence"
        )
        ai_intelligence_dir.mkdir(parents=True, exist_ok=True)

        tests_dir = cls.integration_project / ".claudedirector" / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        cls.project_structure_path = project_structure_file

    @classmethod
    def _report_performance_metrics(cls):
        """Report performance metrics from integration tests"""
        metrics = cls.performance_metrics

        print("\n" + "=" * 60)
        print("PHASE 2 INTEGRATION PERFORMANCE METRICS")
        print("=" * 60)

        for metric_name, times in metrics.items():
            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)

                print(f"{metric_name.replace('_', ' ').title()}:")
                print(f"  Average: {avg_time:.2f}ms")
                print(f"  Maximum: {max_time:.2f}ms")
                print(f"  Minimum: {min_time:.2f}ms")
                print(f"  Samples: {len(times)}")
                print()

    def setUp(self):
        """Set up individual integration test"""
        self.integration_config = {
            "project_root": str(self.integration_project),
            "project_structure_path": str(self.project_structure_path),
            "performance_mode": "production",
            "context7_enabled": True,
        }

    def test_unified_factory_real_integration(self):
        """Test real UnifiedFactory integration with Phase 2 components"""
        start_time = time.time()

        # Initialize UnifiedFactory
        factory = UnifiedFactory(self.integration_config)

        initialization_time = (time.time() - start_time) * 1000
        self.performance_metrics["initialization_times"].append(initialization_time)

        # Verify component type support
        self.assertTrue(
            factory.supports_component_type(ComponentType.SOLID_TEMPLATE_ENGINE)
        )
        self.assertTrue(
            factory.supports_component_type(
                ComponentType.STRUCTURE_AWARE_PLACEMENT_ENGINE
            )
        )

        # Create components via factory
        solid_engine = factory.create_component(
            ComponentType.SOLID_TEMPLATE_ENGINE, config=self.integration_config
        )

        placement_engine = factory.create_component(
            ComponentType.STRUCTURE_AWARE_PLACEMENT_ENGINE,
            config=self.integration_config,
        )

        # Verify component creation
        self.assertIsInstance(solid_engine, SOLIDTemplateEngine)
        self.assertIsInstance(placement_engine, StructureAwarePlacementEngine)

        # Verify components are properly configured
        self.assertEqual(
            str(placement_engine.project_root), str(self.integration_project)
        )

    def test_real_project_structure_parsing_integration(self):
        """Test integration with real PROJECT_STRUCTURE.md parsing"""
        start_time = time.time()

        placement_engine = StructureAwarePlacementEngine(self.integration_config)

        parsing_time = (time.time() - start_time) * 1000
        self.performance_metrics["initialization_times"].append(parsing_time)

        # Verify PROJECT_STRUCTURE.md was parsed
        self.assertIsInstance(placement_engine._placement_rules, dict)
        self.assertGreater(len(placement_engine._placement_rules), 0)

        # Verify specific placement rules exist
        self.assertIn(ComponentCategory.GENERATION, placement_engine._placement_rules)
        self.assertIn(ComponentCategory.VALIDATION, placement_engine._placement_rules)
        self.assertIn(
            ComponentCategory.AI_INTELLIGENCE, placement_engine._placement_rules
        )

        # Verify generation rule details
        generation_rule = placement_engine._placement_rules[
            ComponentCategory.GENERATION
        ]
        self.assertEqual(
            generation_rule.base_path, ".claudedirector/lib/core/generation"
        )
        self.assertIn("*_template*.py", generation_rule.patterns)

    def test_end_to_end_generation_workflow_integration(self):
        """Test complete end-to-end generation workflow"""
        # Initialize components
        solid_engine = SOLIDTemplateEngine(self.integration_config)
        placement_engine = StructureAwarePlacementEngine(self.integration_config)

        # Test realistic workflow scenarios
        workflow_scenarios = [
            {
                "component_name": "user_authentication_processor",
                "principle": SOLIDPrinciple.SINGLE_RESPONSIBILITY,
                "component_type": "processor",
                "expected_placement": "core",
            },
            {
                "component_name": "payment_validation_engine",
                "principle": SOLIDPrinciple.OPEN_CLOSED,
                "component_type": "validation",
                "expected_placement": "validation",
            },
            {
                "component_name": "recommendation_template_generator",
                "principle": SOLIDPrinciple.DEPENDENCY_INVERSION,
                "component_type": "template",
                "expected_placement": "generation",
            },
        ]

        for scenario in workflow_scenarios:
            with self.subTest(component=scenario["component_name"]):
                start_time = time.time()

                # Step 1: Generate SOLID template
                context = TemplateContext(
                    name=scenario["component_name"],
                    namespace=f"claudedirector.lib.{scenario['component_type']}",
                    dependencies=["typing", "abc", "dataclasses"],
                    context_data={"component_type": scenario["component_type"]},
                )

                generation_start = time.time()
                template_result = solid_engine.generate_template(
                    principle=scenario["principle"],
                    template_type="class",
                    context=context,
                )
                generation_time = (time.time() - generation_start) * 1000
                self.performance_metrics["generation_times"].append(generation_time)

                # Step 2: Determine placement
                placement_start = time.time()
                placement_path = placement_engine.determine_placement(
                    component_name=scenario["component_name"],
                    component_type=scenario["component_type"],
                    context={"project_root": str(self.integration_project)},
                )
                placement_time = (time.time() - placement_start) * 1000
                self.performance_metrics["placement_times"].append(placement_time)

                total_time = (time.time() - start_time) * 1000
                self.performance_metrics["end_to_end_times"].append(total_time)

                # Verify results
                self.assertIsInstance(template_result, GenerationResult)
                self.assertIsInstance(template_result.code, str)
                self.assertGreater(len(template_result.code), 0)
                self.assertIn(scenario["component_name"], template_result.code)

                self.assertIsInstance(placement_path, Path)
                self.assertIn(scenario["expected_placement"], str(placement_path))

                # Performance requirements
                self.assertLess(
                    generation_time,
                    2000,
                    f"Generation time {generation_time}ms exceeds 2s limit",
                )
                self.assertLess(
                    placement_time,
                    2000,
                    f"Placement time {placement_time}ms exceeds 2s limit",
                )
                self.assertLess(
                    total_time, 3000, f"End-to-end time {total_time}ms exceeds 3s limit"
                )

    def test_context7_mcp_integration_real_patterns(self):
        """Test Context7 MCP integration with real architectural patterns"""
        solid_engine = SOLIDTemplateEngine(self.integration_config)
        placement_engine = StructureAwarePlacementEngine(self.integration_config)

        # Verify Context7 patterns are loaded
        self.assertIn("framework_pattern", solid_engine._context7_patterns)
        self.assertIn("best_practice", solid_engine._context7_patterns)
        self.assertIn("pattern_access", solid_engine._context7_patterns)

        self.assertIn("pattern_access", placement_engine._context7_patterns)
        self.assertIn("framework_pattern", placement_engine._context7_patterns)
        self.assertIn("best_practice", placement_engine._context7_patterns)

        # Test Context7 pattern descriptions are meaningful
        solid_patterns = solid_engine._context7_patterns
        self.assertIn("Context7", solid_patterns["framework_pattern"])
        self.assertIn("architectural", solid_patterns["framework_pattern"])

        placement_patterns = placement_engine._context7_patterns
        self.assertIn("Context7", placement_patterns["pattern_access"])
        self.assertIn("pattern", placement_patterns["pattern_access"])

    def test_performance_benchmarking_integration(self):
        """Test performance benchmarking under realistic load"""
        solid_engine = SOLIDTemplateEngine(self.integration_config)
        placement_engine = StructureAwarePlacementEngine(self.integration_config)

        # Benchmark multiple operations
        num_operations = 10

        for i in range(num_operations):
            # Generate template
            context = TemplateContext(
                name=f"BenchmarkComponent{i}",
                namespace="claudedirector.benchmark",
                dependencies=["typing"],
                context_data={"iteration": i},
            )

            start_time = time.time()
            template_result = solid_engine.generate_template(
                principle=SOLIDPrinciple.SINGLE_RESPONSIBILITY,
                template_type="class",
                context=context,
            )
            generation_time = (time.time() - start_time) * 1000
            self.performance_metrics["generation_times"].append(generation_time)

            # Determine placement
            start_time = time.time()
            placement_path = placement_engine.determine_placement(
                component_name=f"benchmark_component_{i}",
                component_type="processor",
                context={"project_root": str(self.integration_project)},
            )
            placement_time = (time.time() - start_time) * 1000
            self.performance_metrics["placement_times"].append(placement_time)

            # Verify performance requirements
            self.assertLess(generation_time, 2000)
            self.assertLess(placement_time, 2000)

        # Calculate performance statistics
        avg_generation = sum(self.performance_metrics["generation_times"]) / len(
            self.performance_metrics["generation_times"]
        )
        avg_placement = sum(self.performance_metrics["placement_times"]) / len(
            self.performance_metrics["placement_times"]
        )

        # Performance assertions
        self.assertLess(
            avg_generation,
            1000,
            f"Average generation time {avg_generation}ms exceeds 1s target",
        )
        self.assertLess(
            avg_placement,
            1000,
            f"Average placement time {avg_placement}ms exceeds 1s target",
        )

    def test_error_recovery_integration(self):
        """Test error recovery and resilience in integration scenarios"""
        # Test with invalid configurations
        invalid_configs = [
            {"project_root": "/nonexistent/path"},
            {"project_structure_path": "/invalid/structure.md"},
            {"invalid_key": "invalid_value"},
        ]

        for invalid_config in invalid_configs:
            with self.subTest(config=invalid_config):
                try:
                    # Should handle gracefully without crashing
                    solid_engine = SOLIDTemplateEngine(invalid_config)
                    placement_engine = StructureAwarePlacementEngine(invalid_config)

                    # Basic operations should still work
                    context = TemplateContext(name="ErrorRecoveryTest")
                    result = solid_engine.generate_template(
                        principle=SOLIDPrinciple.SINGLE_RESPONSIBILITY,
                        template_type="class",
                        context=context,
                    )

                    self.assertIsInstance(result, GenerationResult)

                except Exception as e:
                    self.fail(
                        f"Integration failed to handle invalid config gracefully: {e}"
                    )

    def test_concurrent_operations_integration(self):
        """Test concurrent operations and thread safety"""
        import threading
        import queue

        solid_engine = SOLIDTemplateEngine(self.integration_config)
        placement_engine = StructureAwarePlacementEngine(self.integration_config)

        results_queue = queue.Queue()
        num_threads = 5
        operations_per_thread = 3

        def worker_thread(thread_id):
            """Worker thread for concurrent testing"""
            thread_results = []

            for i in range(operations_per_thread):
                try:
                    # Generate template
                    context = TemplateContext(name=f"ConcurrentTest{thread_id}_{i}")
                    template_result = solid_engine.generate_template(
                        principle=SOLIDPrinciple.OPEN_CLOSED,
                        template_type="class",
                        context=context,
                    )

                    # Determine placement
                    placement_path = placement_engine.determine_placement(
                        component_name=f"concurrent_test_{thread_id}_{i}",
                        component_type="template",
                        context={"project_root": str(self.integration_project)},
                    )

                    thread_results.append(
                        {
                            "thread_id": thread_id,
                            "iteration": i,
                            "template_success": isinstance(
                                template_result, GenerationResult
                            ),
                            "placement_success": isinstance(placement_path, Path),
                        }
                    )

                except Exception as e:
                    thread_results.append(
                        {"thread_id": thread_id, "iteration": i, "error": str(e)}
                    )

            results_queue.put(thread_results)

        # Start threads
        threads = []
        for thread_id in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)  # 10 second timeout

        # Collect results
        all_results = []
        while not results_queue.empty():
            all_results.extend(results_queue.get())

        # Verify all operations succeeded
        expected_operations = num_threads * operations_per_thread
        self.assertEqual(len(all_results), expected_operations)

        for result in all_results:
            self.assertNotIn("error", result, f"Concurrent operation failed: {result}")
            self.assertTrue(result.get("template_success", False))
            self.assertTrue(result.get("placement_success", False))


if __name__ == "__main__":
    unittest.main(verbosity=2)
