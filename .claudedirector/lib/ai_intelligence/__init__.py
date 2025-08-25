"""
Advanced AI Intelligence - Phase 1 Implementation

Team: Martin (Lead) + Berny (Senior AI Developer)

This module provides enhanced decision intelligence capabilities by orchestrating
existing ClaudeDirector infrastructure:

- 4 Operational MCP Servers (Sequential, Context7, Magic, Playwright)
- 25+ Strategic Frameworks (87.5% accuracy baseline)
- Complete Transparency System (audit trail and real-time disclosure)
- Persona-Specific Routing (Diego, Camille, Rachel, Alvaro, Martin)

Key Components:
- DecisionIntelligenceOrchestrator: Core orchestration of existing infrastructure
- MCPEnhancedDecisionPipeline: Enhanced decision pipeline with MCP coordination
- MCPEnhancedFrameworkEngine: Framework engine with MCP server intelligence
- FrameworkMCPCoordinator: Framework-MCP server coordination optimization

Technical Approach:
- Lightweight enhancements to existing proven systems
- <50MB additional storage (current DB is 216KB)
- <100MB additional memory (local chat app focused)
- <500ms processing latency (leveraging existing MCP performance)
- 90%+ decision detection accuracy target (from 87.5% baseline)
"""

from .decision_orchestrator import (
    DecisionIntelligenceOrchestrator,
    DecisionContext,
    DecisionIntelligenceResult,
    DecisionComplexity,
    create_decision_intelligence_orchestrator,
)

__all__ = [
    "DecisionIntelligenceOrchestrator",
    "DecisionContext",
    "DecisionIntelligenceResult",
    "DecisionComplexity",
    "create_decision_intelligence_orchestrator",
]
