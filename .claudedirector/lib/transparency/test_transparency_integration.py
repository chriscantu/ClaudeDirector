"""
Comprehensive Test Suite for Transparency System Integration
Tests MCP transparency, framework detection, and persona integration
"""

import pytest
import asyncio
import time
from unittest.mock import Mock

from .integrated_transparency import IntegratedTransparencySystem, TransparencyContext, create_transparency_system
from .persona_integration import TransparentPersonaManager, PersonaIntegrationFactory, MCPIntegrationHelper
from .mcp_transparency import MCPCall
from .framework_detection import FrameworkUsage


class TestTransparencyContext:
    """Test the TransparencyContext class"""

    def test_context_initialization(self):
        context = TransparencyContext("diego")
        assert context.persona == "diego"
        assert len(context.mcp_context.mcp_calls) == 0
        assert len(context.detected_frameworks) == 0
        assert not context.has_enhancements

    def test_context_with_mcp_calls(self):
        context = TransparencyContext("camille")
        context.mcp_context.add_mcp_call(
            MCPCall("test_server", "test_capability", 0.1, True)
        )
        assert context.has_enhancements
        assert context.mcp_context.has_mcp_calls()

    def test_context_with_frameworks(self):
        context = TransparencyContext("rachel")
        context.detected_frameworks.append(
            FrameworkUsage("OGSM", 0.9, ["goal", "strategy"])
        )
        assert context.has_enhancements
        assert len(context.detected_frameworks) == 1


class TestIntegratedTransparencySystem:
    """Test the main integrated transparency system"""

    def test_system_initialization(self):
        system = IntegratedTransparencySystem()
        assert system.transparency_enabled
        assert system.mcp_disclosure_enabled
        assert system.framework_attribution_enabled

    def test_system_configuration(self):
        config = {
            'transparency_enabled': False,
            'mcp_disclosure_enabled': True,
            'framework_attribution_enabled': False
        }
        system = IntegratedTransparencySystem(config)
        assert not system.transparency_enabled
        assert system.mcp_disclosure_enabled
        assert not system.framework_attribution_enabled

    def test_track_mcp_call(self):
        system = IntegratedTransparencySystem()
        context = system.create_transparency_context("diego")

        system.track_mcp_call(context, "test_server", "test_capability", 0.1)

        assert len(context.mcp_context.mcp_calls) == 1
        assert context.mcp_context.mcp_calls[0].server_name == "test_server"

    def test_apply_transparency_disabled(self):
        config = {'transparency_enabled': False}
        system = IntegratedTransparencySystem(config)
        context = system.create_transparency_context("alvaro")

        original_response = "Test response"
        result = system.apply_transparency(context, original_response)

        assert result == original_response

    def test_apply_transparency_with_mcp(self):
        system = IntegratedTransparencySystem()
        context = system.create_transparency_context("martin")

        # Add MCP call
        system.track_mcp_call(context, "test_server", "analysis", 0.1)

        original_response = "Test response"
        result = system.apply_transparency(context, original_response)

        # Should contain both original response and transparency info
        assert "Test response" in result
        assert "Enhanced Response" in result or "MCP" in result

    def test_performance_stats_tracking(self):
        system = IntegratedTransparencySystem()
        context = system.create_transparency_context("diego")

        # Apply transparency multiple times
        for _ in range(3):
            system.apply_transparency(context, "test")

        stats = system.get_performance_stats()
        assert stats['total_requests'] == 3


class TestTransparentPersonaManager:
    """Test the transparent persona manager integration"""

    @pytest.fixture
    def transparency_system(self):
        return create_transparency_system("minimal")

    @pytest.fixture
    def persona_manager(self, transparency_system):
        return TransparentPersonaManager(transparency_system)

    @pytest.mark.asyncio
    async def test_generate_persona_response(self, persona_manager):
        response = await persona_manager.generate_persona_response(
            "diego", "What's the strategic approach?"
        )

        assert response.persona == "diego"
        assert "strategic" in response.content.lower()
        assert response.transparency_summary is not None

    @pytest.mark.asyncio
    async def test_generate_response_with_mcp_tracking(self, persona_manager):
        # Create a custom persona handler that uses MCP
        async def diego_handler(query, **kwargs):
            context = kwargs.get('transparency_context')
            if context:
                # Simulate MCP call
                persona_manager.track_mcp_call(
                    context, "strategy_server", "analysis", 0.05, True
                )
            return "Strategic analysis using advanced frameworks."

        persona_manager.register_persona("diego", diego_handler)

        response = await persona_manager.generate_persona_response("diego", "Analyze this")

        assert response.enhancements_applied
        assert response.transparency_summary['mcp_calls'] == 1
        assert "strategy_server" in response.transparency_summary['mcp_servers_used']

    @pytest.mark.asyncio
    async def test_error_handling(self, persona_manager):
        # Register a handler that raises an exception
        async def error_handler(query, **kwargs):
            raise ValueError("Test error")

        persona_manager.register_persona("error_test", error_handler)

        response = await persona_manager.generate_persona_response("error_test", "test")

        assert "error" in response.content.lower()
        assert response.persona == "error_test"

    def test_performance_stats(self, persona_manager):
        stats = persona_manager.get_performance_stats()
        assert 'total_requests' in stats
        assert 'enhanced_requests' in stats
        assert 'enhancement_rate' in stats

    def test_persona_stats(self, persona_manager):
        persona_manager.register_persona("test_persona", Mock())

        stats = persona_manager.get_persona_stats()
        assert "test_persona" in stats['registered_personas']
        assert not stats['has_original_manager']


class TestMCPIntegrationHelper:
    """Test the MCP integration helper"""

    @pytest.fixture
    def setup_helper(self):
        transparency_system = create_transparency_system("debug")
        persona_manager = TransparentPersonaManager(transparency_system)
        context = transparency_system.create_transparency_context("alvaro")

        helper = MCPIntegrationHelper(context, persona_manager)
        return helper, context, persona_manager

    @pytest.mark.asyncio
    async def test_successful_mcp_call(self, setup_helper):
        helper, context, persona_manager = setup_helper

        result = await helper.call_mcp_server("test_server", "analysis", param1="value1")

        assert result['server'] == "test_server"
        assert result['capability'] == "analysis"
        assert len(context.mcp_context.mcp_calls) == 1
        assert context.mcp_context.mcp_calls[0].success

    @pytest.mark.asyncio
    async def test_failed_mcp_call(self, setup_helper):
        helper, context, persona_manager = setup_helper

        # Mock the _simulate_mcp_call to raise an exception
        async def failing_call(*args, **kwargs):
            raise ConnectionError("MCP server unavailable")

        helper._simulate_mcp_call = failing_call

        with pytest.raises(ConnectionError):
            await helper.call_mcp_server("failing_server", "test")

        assert len(context.mcp_context.mcp_calls) == 1
        assert not context.mcp_context.mcp_calls[0].success
        assert "MCP server unavailable" in context.mcp_context.mcp_calls[0].error_message


class TestPersonaIntegrationFactory:
    """Test the persona integration factory"""

    def test_create_transparent_manager(self):
        manager = PersonaIntegrationFactory.create_transparent_manager("default")

        assert isinstance(manager, TransparentPersonaManager)
        assert manager.transparency_system.transparency_enabled

    def test_create_minimal_config(self):
        manager = PersonaIntegrationFactory.create_transparent_manager("minimal")

        assert isinstance(manager, TransparentPersonaManager)
        assert manager.transparency_system.mcp_disclosure_enabled
        assert not manager.transparency_system.framework_attribution_enabled

    def test_wrap_existing_manager(self):
        original_manager = Mock()
        wrapped_manager = PersonaIntegrationFactory.wrap_existing_manager(
            original_manager, "debug"
        )

        assert isinstance(wrapped_manager, TransparentPersonaManager)
        assert wrapped_manager.original_persona_manager == original_manager
        assert wrapped_manager.debug_mode


class TestEndToEndIntegration:
    """End-to-end integration tests"""

    @pytest.mark.asyncio
    async def test_full_transparency_pipeline(self):
        # Create complete integrated system
        transparency_system = create_transparency_system("default")
        persona_manager = TransparentPersonaManager(transparency_system)

        # Register a comprehensive persona handler
        async def comprehensive_handler(query, **kwargs):
            context = kwargs.get('transparency_context')
            mcp_helper = MCPIntegrationHelper(context, persona_manager)

            # Simulate multiple MCP calls
            await mcp_helper.call_mcp_server("analytics_server", "sentiment_analysis")
            await mcp_helper.call_mcp_server("knowledge_server", "fact_checking")

            # Return response that will trigger framework detection
            return """
            Using OGSM strategic framework, I've analyzed your query.
            The objectives are clear, and I've applied Blue Ocean Strategy
            principles to identify new market opportunities.
            """

        persona_manager.register_persona("diego", comprehensive_handler)

        # Generate response
        response = await persona_manager.generate_persona_response(
            "diego", "Analyze our market position"
        )

        # Validate comprehensive transparency
        assert response.enhancements_applied
        assert response.transparency_summary['mcp_calls'] == 2
        assert "analytics_server" in response.transparency_summary['mcp_servers_used']
        assert "knowledge_server" in response.transparency_summary['mcp_servers_used']
        assert response.transparency_summary['frameworks_detected'] > 0

        # Validate response content includes transparency information
        assert "Enhanced Response" in response.content or "MCP" in response.content
        assert "OGSM" in response.content
        assert "Blue Ocean" in response.content

    @pytest.mark.asyncio
    async def test_performance_under_load(self):
        """Test transparency system performance under load"""
        transparency_system = create_transparency_system("minimal")
        persona_manager = TransparentPersonaManager(transparency_system)

        async def simple_handler(query, **kwargs):
            context = kwargs.get('transparency_context')
            persona_manager.track_mcp_call(context, "test_server", "quick_call", 0.01)
            return f"Quick response to: {query}"

        persona_manager.register_persona("fast_persona", simple_handler)

        # Generate multiple concurrent responses
        tasks = [
            persona_manager.generate_persona_response("fast_persona", f"Query {i}")
            for i in range(10)
        ]

        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()

        # Validate all responses processed successfully
        assert len(responses) == 10
        for response in responses:
            assert response.transparency_summary['mcp_calls'] == 1
            assert response.enhancements_applied

        # Validate reasonable performance
        total_time = end_time - start_time
        assert total_time < 2.0  # Should complete in under 2 seconds

        # Check performance stats
        stats = persona_manager.get_performance_stats()
        assert stats['total_requests'] == 10
        assert stats['enhanced_requests'] == 10
        assert stats['enhancement_rate'] == 100.0


class TestConfigurationVariations:
    """Test different configuration variations"""

    @pytest.mark.asyncio
    async def test_mcp_only_configuration(self):
        config = {
            'transparency_enabled': True,
            'mcp_disclosure_enabled': True,
            'framework_attribution_enabled': False
        }
        system = IntegratedTransparencySystem(config)
        persona_manager = TransparentPersonaManager(system)

        async def mcp_handler(query, **kwargs):
            context = kwargs.get('transparency_context')
            persona_manager.track_mcp_call(context, "test_server", "analysis", 0.1)
            return "Response using OGSM framework analysis"

        persona_manager.register_persona("test", mcp_handler)

        response = await persona_manager.generate_persona_response("test", "query")

        # Should have MCP transparency but not framework attribution
        assert response.transparency_summary['mcp_calls'] == 1
        assert response.transparency_summary['frameworks_detected'] == 0

    @pytest.mark.asyncio
    async def test_framework_only_configuration(self):
        config = {
            'transparency_enabled': True,
            'mcp_disclosure_enabled': False,
            'framework_attribution_enabled': True
        }
        system = IntegratedTransparencySystem(config)
        persona_manager = TransparentPersonaManager(system)

        async def framework_handler(query, **kwargs):
            context = kwargs.get('transparency_context')
            persona_manager.track_mcp_call(context, "test_server", "analysis", 0.1)
            return "Using OGSM strategic framework for analysis"

        persona_manager.register_persona("test", framework_handler)

        response = await persona_manager.generate_persona_response("test", "query")

        # Should have framework detection but not MCP transparency
        assert response.transparency_summary['mcp_calls'] == 0
        assert response.transparency_summary['frameworks_detected'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
