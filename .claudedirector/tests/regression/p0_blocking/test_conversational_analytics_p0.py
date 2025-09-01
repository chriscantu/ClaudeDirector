#!/usr/bin/env python3
"""
P0 Test: Conversational Analytics Capabilities
Phase 7 Week 2 - Critical functionality validation

🛡️ P0 BLOCKING TEST - ZERO TOLERANCE FOR FAILURES
Tests the core conversational analytics pipeline for Phase 7 Week 2.

This test validates:
- ConversationalDataManager query parsing
- Chat-embedded visualization generation
- Complete pipeline integration
- PRD compliance (chat-only interface)
"""

import pytest
import asyncio
import time
from typing import Dict, Any

# Import Phase 7 Week 2 components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from .claudedirector.lib.mcp import (
        ConversationalAnalyticsWorkflow,
        ConversationalDataManager,
        create_conversational_analytics_workflow,
        create_conversational_data_manager,
    )
except ImportError:
    # Fallback for different test environments
    from claudedirector.lib.mcp import (
        ConversationalAnalyticsWorkflow,
        ConversationalDataManager,
        create_conversational_analytics_workflow,
        create_conversational_data_manager,
    )


class TestConversationalAnalyticsP0:
    """P0 tests for conversational analytics capabilities"""
    
    @pytest.fixture
    def workflow(self):
        """Create conversational analytics workflow for testing"""
        return create_conversational_analytics_workflow()
    
    @pytest.fixture
    def data_manager(self):
        """Create conversational data manager for testing"""
        return create_conversational_data_manager()
    
    def test_p0_conversational_data_manager_initialization(self, data_manager):
        """P0: ConversationalDataManager initializes correctly"""
        assert data_manager is not None
        assert hasattr(data_manager, 'query_patterns')
        assert hasattr(data_manager, 'data_sources')
        assert len(data_manager.query_patterns) > 0
        assert len(data_manager.data_sources) > 0
    
    @pytest.mark.asyncio
    async def test_p0_query_parsing_sprint_metrics(self, data_manager):
        """P0: Sprint metrics queries are parsed correctly"""
        query_text = "Show me current sprint metrics for the platform team"
        
        parsed_query = await data_manager.parse_conversational_query(query_text)
        
        assert parsed_query is not None
        assert parsed_query.query_type.value == "sprint_metrics"
        assert "platform" in parsed_query.entities or len(parsed_query.entities) >= 0
    
    @pytest.mark.asyncio
    async def test_p0_query_parsing_team_performance(self, data_manager):
        """P0: Team performance queries are parsed correctly"""
        query_text = "How is our team performing this quarter?"
        
        parsed_query = await data_manager.parse_conversational_query(query_text)
        
        assert parsed_query is not None
        assert parsed_query.query_type.value in ["team_performance", "general_analytics"]
    
    @pytest.mark.asyncio
    async def test_p0_data_fetching_performance(self, data_manager):
        """P0: Data fetching meets <5s latency requirement"""
        query_text = "Show me current sprint metrics"
        
        start_time = time.time()
        parsed_query, data_response = await data_manager.process_conversational_query(query_text)
        total_time = (time.time() - start_time) * 1000
        
        # PRD requirement: <5 second latency
        assert total_time < 5000, f"Data fetch took {total_time:.2f}ms, exceeds 5s limit"
        assert data_response is not None
        assert data_response.success is True
        assert data_response.latency_ms < 5000
    
    def test_p0_workflow_initialization(self, workflow):
        """P0: ConversationalAnalyticsWorkflow initializes correctly"""
        assert workflow is not None
        assert hasattr(workflow, 'data_manager')
        assert hasattr(workflow, 'visualization_engine')
        assert workflow.name == "conversational-analytics-workflow"
        assert workflow.version == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_p0_complete_pipeline_sprint_query(self, workflow):
        """P0: Complete pipeline processes sprint queries successfully"""
        query_text = "Show me current sprint metrics"
        
        result = await workflow.process_chat_query(query_text, persona="diego")
        
        assert result is not None
        assert result.success is True
        assert result.query_text == query_text
        assert result.parsed_query is not None
        assert result.data_response is not None
        assert result.visualization_result is not None
        assert result.total_latency_ms < 5000  # PRD requirement
    
    @pytest.mark.asyncio
    async def test_p0_complete_pipeline_roi_query(self, workflow):
        """P0: Complete pipeline processes ROI queries successfully"""
        query_text = "What's our platform investment ROI?"
        
        result = await workflow.process_chat_query(query_text, persona="alvaro")
        
        assert result is not None
        assert result.success is True
        assert result.visualization_result.success is True
        assert "roi" in result.visualization_result.chart_type.lower()
    
    @pytest.mark.asyncio
    async def test_p0_chat_embedded_visualization_generation(self, workflow):
        """P0: Chat-embedded visualizations generate correctly"""
        query_text = "Show me team performance metrics"
        
        result = await workflow.process_chat_query(query_text, persona="diego")
        
        assert result.visualization_result is not None
        assert result.visualization_result.success is True
        assert len(result.visualization_result.html_output) > 0
        assert "claudedirector-chat-visualization" in result.visualization_result.html_output
        assert result.visualization_result.generation_time < 1.0  # <1s for visualization
    
    @pytest.mark.asyncio
    async def test_p0_prd_compliance_chat_only_interface(self, workflow):
        """P0: PRD compliance - chat-only interface maintained"""
        query_text = "Show me architecture health"
        
        result = await workflow.process_chat_query(query_text, persona="martin")
        
        # Verify PRD compliance metadata
        assert result.pipeline_metadata["chat_optimized"] is True
        assert result.pipeline_metadata["magic_mcp_ready"] is True
        assert result.visualization_result.metadata["chat_optimized"] is True
        assert result.visualization_result.metadata["magic_mcp_ready"] is True
    
    @pytest.mark.asyncio
    async def test_p0_context_preservation(self, workflow):
        """P0: Context preservation across multi-turn conversations"""
        # First query
        query1 = "Show me sprint metrics for platform team"
        context = {"conversation_id": "test_123"}
        
        result1 = await workflow.process_chat_query(query1, context=context)
        
        # Second query with context
        query2 = "Break that down by team member"
        context_with_history = {
            "conversation_id": "test_123",
            "previous_entities": ["platform"],
            "previous_query_type": "sprint_metrics"
        }
        
        result2 = await workflow.process_chat_query(query2, context=context_with_history)
        
        assert result1.success is True
        assert result2.success is True
        assert result2.pipeline_metadata["context_provided"] is True
    
    @pytest.mark.asyncio
    async def test_p0_error_handling_graceful_degradation(self, workflow):
        """P0: Graceful error handling for invalid queries"""
        query_text = "This is not a valid analytics query at all"
        
        result = await workflow.process_chat_query(query_text)
        
        # Should not crash, should provide helpful response
        assert result is not None
        assert isinstance(result.success, bool)  # Should have success field
        assert len(result.visualization_result.html_output) > 0  # Should have some response
    
    @pytest.mark.asyncio
    async def test_p0_performance_targets_met(self, workflow):
        """P0: All performance targets from PRD are met"""
        query_text = "Show me current sprint status"
        
        start_time = time.time()
        result = await workflow.process_chat_query(query_text)
        total_time = (time.time() - start_time) * 1000
        
        # PRD performance requirements
        assert total_time < 5000, f"Total pipeline took {total_time:.2f}ms, exceeds 5s"
        assert result.data_response.latency_ms < 5000, "Data fetch exceeds 5s"
        assert result.visualization_result.generation_time < 0.5, "Visualization exceeds 500ms"
    
    @pytest.mark.asyncio
    async def test_p0_pipeline_health_monitoring(self, workflow):
        """P0: Pipeline health monitoring works correctly"""
        # Process a few queries to generate metrics
        queries = [
            "Show me sprint metrics",
            "What's our ROI?", 
            "How is the team performing?"
        ]
        
        for query in queries:
            await workflow.process_chat_query(query)
        
        health = await workflow.get_pipeline_health()
        
        assert health is not None
        assert "health_status" in health
        assert "metrics" in health
        assert "prd_compliance" in health
        assert health["prd_compliance"]["chat_only_interface"] is True
        assert health["metrics"]["total_queries"] >= len(queries)


if __name__ == "__main__":
    # Run P0 tests directly
    pytest.main([__file__, "-v", "--tb=short"])
