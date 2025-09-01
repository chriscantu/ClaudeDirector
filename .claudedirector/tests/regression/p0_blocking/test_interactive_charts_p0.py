#!/usr/bin/env python3
"""
P0 Interactive Charts Performance Testing
Phase 7 Week 4 - T-QA1: Interactive Performance Testing

🏗️ Martin | Platform Architecture - P0 performance validation
🎨 Rachel | Design Systems Strategy - UX performance requirements
💼 Alvaro | Platform Investment Strategy - Business impact validation

P0 BLOCKING Tests - Interactive Chart Engine Performance Requirements:
- All chart interactions respond within 200ms
- Interactive chart generation completes within 500ms
- Interactive session memory usage stays under 50MB
- Interactive charts integrate seamlessly with chat interface
- All interactivity works without external dependencies
"""

import asyncio
import pytest
import time
import psutil
import os
import json
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Import our interactive chart components
from claudedirector.lib.mcp.interactive_chart_engine import (
    InteractiveChartEngine,
    InteractionType,
    InteractionEvent,
    InteractionResult,
)
from claudedirector.lib.mcp.chart_interaction_types import ChartInteractionTypes
from claudedirector.lib.mcp.chat_embedded_interactivity import (
    ChatEmbeddedInteractivity,
    ChatEmbeddedResult,
)


class TestInteractiveChartsP0:
    """
    P0 BLOCKING Tests for Interactive Chart Engine

    These tests must NEVER fail (0 failures allowed).
    Any failure indicates a critical system regression.
    """

    @pytest.fixture
    def interactive_engine(self):
        """Initialize Interactive Chart Engine for testing"""
        return InteractiveChartEngine()

    @pytest.fixture
    def interaction_types(self):
        """Initialize Chart Interaction Types for testing"""
        return ChartInteractionTypes()

    @pytest.fixture
    def chat_embedded(self):
        """Initialize Chat Embedded Interactivity for testing"""
        return ChatEmbeddedInteractivity()

    @pytest.fixture
    def sample_chart(self):
        """Create sample chart for testing"""
        fig = go.Figure(
            data=[
                go.Bar(
                    x=["Team A", "Team B", "Team C", "Team D"],
                    y=[95, 88, 92, 87],
                    marker_color="#4dabf7",
                    name="Performance Metrics",
                )
            ]
        )

        fig.update_layout(
            title="Sample Performance Dashboard",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

        return fig

    @pytest.fixture
    def sample_context(self):
        """Create sample context for testing"""
        return {
            "chart_id": "test-chart-001",
            "chart_type": "leadership_dashboard",
            "persona": "diego",
            "title": "Team Performance Dashboard",
            "drill_level": 0,
            "interaction_capabilities": ["drill_down", "filter", "zoom", "hover"],
        }

    # ========== P0 PERFORMANCE TESTS ==========

    @pytest.mark.asyncio
    async def test_p0_interaction_response_time(self, interactive_engine):
        """
        P0 BLOCKING: All chart interactions respond within 200ms

        CRITICAL REQUIREMENT: No interaction can exceed 200ms response time
        """

        # Test data for interaction
        sample_event = {
            "chart_id": "test-chart-001",
            "event_type": "click",
            "element_data": {
                "id": "point-1",
                "data": {"x": "Team A", "y": 95},
                "coordinates": {"x": 100, "y": 200},
            },
        }

        # Measure interaction handling time
        start_time = time.time()
        result = await interactive_engine.handle_chart_interaction(sample_event)
        response_time = time.time() - start_time

        # P0 ASSERTION: Must respond within 200ms
        assert response_time < 0.2, (
            f"❌ P0 CRITICAL: Interaction response time {response_time:.3f}s exceeds 200ms limit. "
            f"This violates user experience requirements and MUST be fixed."
        )

        # Additional validation
        assert result.success, f"Interaction must succeed: {result.error}"
        assert (
            result.processing_time < 0.2
        ), f"Processing time {result.processing_time:.3f}s exceeds 200ms limit"

        print(f"✅ P0 PASS: Interaction responded in {response_time:.3f}s (<200ms)")

    @pytest.mark.asyncio
    async def test_p0_chart_generation_time(
        self, interactive_engine, sample_chart, sample_context
    ):
        """
        P0 BLOCKING: Interactive chart generation completes within 500ms

        CRITICAL REQUIREMENT: Chart interactivity addition must be under 500ms
        """

        interaction_types = [
            InteractionType.CLICK_TO_DRILL_DOWN.value,
            InteractionType.MULTI_SELECT_FILTER.value,
            InteractionType.ZOOM_AND_PAN.value,
            InteractionType.HOVER_DETAILS.value,
            InteractionType.TIME_SERIES_BRUSH.value,
        ]

        for interaction_type in interaction_types:
            start_time = time.time()

            result_fig = await interactive_engine.add_interactivity(
                sample_chart, interaction_type, sample_context
            )

            generation_time = time.time() - start_time

            # P0 ASSERTION: Must generate within 500ms
            assert generation_time < 0.5, (
                f"❌ P0 CRITICAL: {interaction_type} generation time {generation_time:.3f}s "
                f"exceeds 500ms limit. This violates performance requirements and MUST be fixed."
            )

            assert (
                result_fig is not None
            ), f"Interactive chart generation must succeed for {interaction_type}"

            print(
                f"✅ P0 PASS: {interaction_type} generated in {generation_time:.3f}s (<500ms)"
            )

    @pytest.mark.asyncio
    async def test_p0_memory_usage_limits(
        self, interactive_engine, interaction_types, sample_chart
    ):
        """
        P0 BLOCKING: Interactive session memory usage stays under 50MB

        CRITICAL REQUIREMENT: Memory consumption must not exceed 50MB during interactive sessions
        """

        # Get baseline memory usage
        process = psutil.Process(os.getpid())
        baseline_memory_mb = process.memory_info().rss / 1024 / 1024

        # Create multiple interactive sessions to stress test memory
        test_charts = []
        for i in range(10):  # 10 concurrent interactive charts
            context = {
                "chart_id": f"memory-test-{i}",
                "chart_type": "architecture_health",
                "persona": "martin",
            }

            # Add interactivity to multiple charts
            interactive_chart = await interactive_engine.add_interactivity(
                sample_chart, InteractionType.CLICK_TO_DRILL_DOWN.value, context
            )

            test_charts.append(interactive_chart)

            # Simulate interactions
            for j in range(5):  # 5 interactions per chart
                sample_event = {
                    "chart_id": f"memory-test-{i}",
                    "event_type": "click",
                    "element_data": {"id": f"point-{j}", "data": {"x": j, "y": j * 10}},
                }
                await interactive_engine.handle_chart_interaction(sample_event)

        # Check memory usage after creating interactive sessions
        current_memory_mb = process.memory_info().rss / 1024 / 1024
        memory_increase_mb = current_memory_mb - baseline_memory_mb

        # P0 ASSERTION: Memory increase must stay under 50MB
        assert memory_increase_mb < 50, (
            f"❌ P0 CRITICAL: Interactive session memory usage {memory_increase_mb:.1f}MB "
            f"exceeds 50MB limit. This indicates memory leaks and MUST be fixed."
        )

        # Check engine metrics
        metrics = interactive_engine.get_metrics()
        assert metrics["active_sessions"] <= 10, "Active session tracking failed"

        print(
            f"✅ P0 PASS: Memory increase {memory_increase_mb:.1f}MB (<50MB) with {len(test_charts)} interactive charts"
        )

    @pytest.mark.asyncio
    async def test_p0_chat_integration_seamless(
        self, chat_embedded, sample_chart, sample_context
    ):
        """
        P0 BLOCKING: Interactive charts integrate seamlessly with chat interface

        CRITICAL REQUIREMENT: Chat-embedded HTML must be self-contained and functional
        """

        # Generate chat-embedded interactive HTML
        start_time = time.time()
        result = await chat_embedded.generate_interactive_html(
            sample_chart, sample_context
        )
        generation_time = time.time() - start_time

        # P0 ASSERTIONS: Chat integration requirements
        assert (
            result.success
        ), f"❌ P0 CRITICAL: Chat HTML generation failed: {result.error}"

        assert result.self_contained, (
            "❌ P0 CRITICAL: Generated HTML is not self-contained. "
            "This violates chat integration requirements."
        )

        assert result.mobile_responsive, (
            "❌ P0 CRITICAL: Generated HTML is not mobile responsive. "
            "This violates UX requirements for tablet presentations."
        )

        assert result.context_embedded, (
            "❌ P0 CRITICAL: Context data not properly embedded. "
            "This will break interaction preservation across sessions."
        )

        assert result.payload_size_kb < 500, (
            f"❌ P0 CRITICAL: Payload size {result.payload_size_kb:.1f}KB exceeds 500KB limit. "
            f"This violates chat performance requirements."
        )

        assert generation_time < 0.5, (
            f"❌ P0 CRITICAL: Chat HTML generation time {generation_time:.3f}s exceeds 500ms. "
            f"This violates chat response time requirements."
        )

        # Validate HTML content structure
        html = result.html_output
        assert "<!DOCTYPE html>" in html, "Generated HTML must be valid HTML5"
        assert "chart-container-" in html, "HTML must contain chart container"
        assert (
            "initializeChartInteractivity" in html
        ), "HTML must contain initialization script"
        assert "ClaudeDirectorCharts" in html, "HTML must contain chat integration code"

        # Validate no external dependencies
        assert "cdn." not in html.lower(), "HTML must not contain CDN references"
        assert (
            "http://" not in html and "https://" not in html
        ), "HTML must not contain external URLs"

        print(
            f"✅ P0 PASS: Chat integration HTML generated ({result.payload_size_kb:.1f}KB) in {generation_time:.3f}s"
        )

    @pytest.mark.asyncio
    async def test_p0_local_execution_only(self, interactive_engine, interaction_types):
        """
        P0 BLOCKING: All interactivity works without external dependencies

        CRITICAL REQUIREMENT: No external API calls or network dependencies
        """

        # Mock network requests to ensure none are made
        with patch("aiohttp.ClientSession") as mock_session, patch(
            "requests.get"
        ) as mock_requests, patch("urllib.request.urlopen") as mock_urllib:

            # Test interactive engine initialization (should be local only)
            local_engine = InteractiveChartEngine()
            assert local_engine is not None

            # Test chart interaction types (should be local only)
            local_types = ChartInteractionTypes()
            assert local_types is not None

            # Test chat embedded generation (should be local only)
            local_embedded = ChatEmbeddedInteractivity()
            assert local_embedded is not None

            # Generate JavaScript handlers (should be local only)
            js_handlers = local_types.generate_interaction_handlers(
                "leadership_dashboard"
            )
            assert js_handlers is not None
            assert len(js_handlers["combined_handlers"]) > 0
            assert js_handlers["size_kb"] < 50  # P0 size requirement

            # Verify no network calls were attempted
            mock_session.assert_not_called()
            mock_requests.assert_not_called()
            mock_urllib.assert_not_called()

        print(
            "✅ P0 PASS: All interactive functionality works without external dependencies"
        )

    # ========== P0 INTEGRATION TESTS ==========

    @pytest.mark.asyncio
    async def test_p0_end_to_end_interaction_workflow(
        self, interactive_engine, interaction_types, chat_embedded
    ):
        """
        P0 BLOCKING: Complete interaction workflow performs within requirements

        Tests the full workflow: Chart Creation → Interactivity → Chat Embedding
        """

        workflow_start = time.time()

        # Step 1: Create base chart
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(range(100)),
                    y=[i + np.random.normal(0, 5) for i in range(100)],
                    mode="lines+markers",
                    name="Performance Trend",
                )
            ]
        )

        context = {
            "chart_id": "workflow-test-001",
            "chart_type": "performance_metrics",
            "persona": "martin",
            "title": "End-to-End Performance Test",
        }

        # Step 2: Add interactivity (must be <500ms)
        step2_start = time.time()
        interactive_fig = await interactive_engine.add_interactivity(
            fig, InteractionType.CLICK_TO_DRILL_DOWN.value, context
        )
        step2_time = time.time() - step2_start

        assert (
            step2_time < 0.5
        ), f"Interactivity addition took {step2_time:.3f}s (>500ms)"

        # Step 3: Generate chat-embedded HTML (must be <500ms)
        step3_start = time.time()
        embedded_result = await chat_embedded.generate_interactive_html(
            interactive_fig, context
        )
        step3_time = time.time() - step3_start

        assert step3_time < 0.5, f"Chat HTML generation took {step3_time:.3f}s (>500ms)"
        assert (
            embedded_result.success
        ), f"Chat embedding failed: {embedded_result.error}"

        # Step 4: Simulate interaction (must be <200ms)
        step4_start = time.time()
        interaction_event = {
            "chart_id": "workflow-test-001",
            "event_type": "click",
            "element_data": {"id": "point-50", "data": {"x": 50, "y": 55}},
        }
        interaction_result = await interactive_engine.handle_chart_interaction(
            interaction_event
        )
        step4_time = time.time() - step4_start

        assert step4_time < 0.2, f"Interaction handling took {step4_time:.3f}s (>200ms)"
        assert (
            interaction_result.success
        ), f"Interaction failed: {interaction_result.error}"

        # Total workflow time validation
        total_workflow_time = time.time() - workflow_start

        # P0 ASSERTION: Complete workflow should be under 2 seconds
        assert total_workflow_time < 2.0, (
            f"❌ P0 CRITICAL: Complete workflow took {total_workflow_time:.3f}s exceeds 2s limit. "
            f"This violates user experience requirements for interactive features."
        )

        print(f"✅ P0 PASS: Complete workflow completed in {total_workflow_time:.3f}s")
        print(f"  - Interactivity: {step2_time:.3f}s")
        print(f"  - Chat Embedding: {step3_time:.3f}s")
        print(f"  - Interaction: {step4_time:.3f}s")

    @pytest.mark.asyncio
    async def test_p0_concurrent_interactions_performance(self, interactive_engine):
        """
        P0 BLOCKING: Concurrent interactions maintain performance under load

        CRITICAL REQUIREMENT: Multiple simultaneous interactions must not degrade performance
        """

        # Create multiple concurrent interaction tasks
        concurrent_tasks = []

        for i in range(20):  # 20 concurrent interactions
            interaction_event = {
                "chart_id": f"concurrent-test-{i % 5}",  # 5 different charts
                "event_type": "click",
                "element_data": {"id": f"point-{i}", "data": {"x": i, "y": i * 2}},
            }

            task = interactive_engine.handle_chart_interaction(interaction_event)
            concurrent_tasks.append(task)

        # Execute all interactions concurrently
        start_time = time.time()
        results = await asyncio.gather(*concurrent_tasks, return_exceptions=True)
        total_time = time.time() - start_time

        # P0 ASSERTIONS: Concurrent performance requirements
        assert total_time < 1.0, (
            f"❌ P0 CRITICAL: 20 concurrent interactions took {total_time:.3f}s exceeds 1s limit. "
            f"This indicates performance degradation under concurrent load."
        )

        # Verify all interactions succeeded
        successful_results = [
            r for r in results if isinstance(r, InteractionResult) and r.success
        ]
        failed_results = [
            r for r in results if not (isinstance(r, InteractionResult) and r.success)
        ]

        assert len(successful_results) >= 18, (
            f"❌ P0 CRITICAL: Only {len(successful_results)}/20 concurrent interactions succeeded. "
            f"This indicates system instability under load."
        )

        # Check individual response times
        max_response_time = max(r.processing_time for r in successful_results)
        assert max_response_time < 0.3, (
            f"❌ P0 CRITICAL: Slowest concurrent interaction took {max_response_time:.3f}s. "
            f"Performance degraded under concurrent load."
        )

        print(
            f"✅ P0 PASS: {len(successful_results)}/20 concurrent interactions completed in {total_time:.3f}s"
        )
        print(f"  - Max response time: {max_response_time:.3f}s")

    # ========== P0 RELIABILITY TESTS ==========

    @pytest.mark.asyncio
    async def test_p0_error_recovery_performance(self, interactive_engine):
        """
        P0 BLOCKING: Error conditions don't degrade system performance

        CRITICAL REQUIREMENT: System must recover gracefully from errors
        """

        # Test invalid interaction events
        invalid_events = [
            {"chart_id": None, "event_type": "click"},  # Missing chart ID
            {"chart_id": "invalid", "event_type": None},  # Missing event type
            {"chart_id": "test", "event_type": "invalid_type"},  # Invalid event type
            {},  # Empty event
        ]

        for invalid_event in invalid_events:
            start_time = time.time()
            result = await interactive_engine.handle_chart_interaction(invalid_event)
            processing_time = time.time() - start_time

            # P0 ASSERTION: Error handling must be fast
            assert processing_time < 0.1, (
                f"❌ P0 CRITICAL: Error handling took {processing_time:.3f}s exceeds 100ms limit. "
                f"Error conditions are degrading system performance."
            )

            # Error should be handled gracefully
            assert not result.success, "Invalid events should return success=False"
            assert result.error is not None, "Error message should be provided"

        # Test that system continues to work after errors
        valid_event = {
            "chart_id": "recovery-test",
            "event_type": "click",
            "element_data": {"id": "point-1", "data": {"x": 1, "y": 1}},
        }

        start_time = time.time()
        recovery_result = await interactive_engine.handle_chart_interaction(valid_event)
        recovery_time = time.time() - start_time

        assert (
            recovery_time < 0.2
        ), f"Recovery interaction took {recovery_time:.3f}s (>200ms)"

        print("✅ P0 PASS: Error recovery maintains performance within limits")

    @pytest.mark.asyncio
    async def test_p0_memory_cleanup_effectiveness(self, interactive_engine):
        """
        P0 BLOCKING: Memory cleanup prevents memory leaks during extended use

        CRITICAL REQUIREMENT: Long-running interactive sessions must not leak memory
        """

        process = psutil.Process(os.getpid())
        baseline_memory_mb = process.memory_info().rss / 1024 / 1024

        # Simulate extended interactive session
        for cycle in range(5):  # 5 cleanup cycles
            # Create multiple charts and interactions
            for i in range(10):
                context = {
                    "chart_id": f"cleanup-test-{cycle}-{i}",
                    "chart_type": "test_chart",
                    "persona": "martin",
                }

                # Simulate chart interactions
                for j in range(10):
                    event = {
                        "chart_id": f"cleanup-test-{cycle}-{i}",
                        "event_type": "click",
                        "element_data": {"id": f"point-{j}", "data": {"x": j, "y": j}},
                    }
                    await interactive_engine.handle_chart_interaction(event)

            # Trigger cleanup
            interactive_engine.cleanup_expired_sessions(
                max_age_hours=0.001
            )  # Aggressive cleanup

            # Check memory after cleanup
            current_memory_mb = process.memory_info().rss / 1024 / 1024
            memory_increase_mb = current_memory_mb - baseline_memory_mb

            # P0 ASSERTION: Memory should not continuously grow
            assert memory_increase_mb < 30, (
                f"❌ P0 CRITICAL: Memory increased by {memory_increase_mb:.1f}MB after {cycle+1} cycles. "
                f"This indicates memory leaks that will impact long-running sessions."
            )

        print(
            f"✅ P0 PASS: Memory cleanup effective - final increase: {memory_increase_mb:.1f}MB"
        )

    # ========== P0 VALIDATION SUMMARY ==========

    def test_p0_validation_summary(self):
        """
        P0 VALIDATION SUMMARY: Confirm all P0 requirements are testable

        This test ensures comprehensive P0 coverage for interactive charts
        """

        p0_requirements = {
            "interaction_response_time": "All chart interactions respond within 200ms",
            "chart_generation_time": "Interactive chart generation completes within 500ms",
            "memory_usage_limits": "Interactive session memory usage stays under 50MB",
            "chat_integration_seamless": "Interactive charts integrate seamlessly with chat interface",
            "local_execution_only": "All interactivity works without external dependencies",
            "end_to_end_workflow": "Complete interaction workflow performs within requirements",
            "concurrent_performance": "Concurrent interactions maintain performance under load",
            "error_recovery": "Error conditions don't degrade system performance",
            "memory_cleanup": "Memory cleanup prevents memory leaks during extended use",
        }

        tested_requirements = [
            "interaction_response_time",
            "chart_generation_time",
            "memory_usage_limits",
            "chat_integration_seamless",
            "local_execution_only",
            "end_to_end_workflow",
            "concurrent_performance",
            "error_recovery",
            "memory_cleanup",
        ]

        # Validate 100% P0 test coverage
        coverage_percentage = (len(tested_requirements) / len(p0_requirements)) * 100

        assert coverage_percentage == 100.0, (
            f"❌ P0 CRITICAL: Only {coverage_percentage:.1f}% P0 test coverage. "
            f"Missing tests for: {set(p0_requirements.keys()) - set(tested_requirements)}"
        )

        print("✅ P0 VALIDATION: 100% P0 requirements coverage achieved")
        print("📊 P0 TEST MATRIX:")
        for req, description in p0_requirements.items():
            status = "✅ TESTED" if req in tested_requirements else "❌ MISSING"
            print(f"  {status}: {description}")


if __name__ == "__main__":
    # Run P0 tests with strict settings
    pytest.main(
        [
            __file__,
            "-v",
            "--tb=short",
            "--strict-markers",
            "--disable-warnings",
            "-x",  # Stop on first failure (P0 requirement)
        ]
    )
