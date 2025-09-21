#!/usr/bin/env python3
"""
Weekly Reporter Chat Integration - Personal Retrospective Focus
Extends existing weekly_reporter.py with chat interface for personal reflection

🏗️ Martin | Platform Architecture - SOLID/DRY compliance
🎯 EXTENDS existing weekly_reporter.py (DRY compliance)
🔒 PERSONAL FOCUS: Individual reflection, not business intelligence

SEQUENTIAL THINKING METHODOLOGY APPLIED:
1. Problem Definition: Add chat interface to existing weekly reporter
2. Current State Analysis: weekly_reporter.py provides core functionality
3. Solution Hypothesis: Extension pattern with conversational layer for personal use
4. Validation: Context7 Lightweight Fallback + Protocol interfaces
5. Execution: Simple chat command routing for personal retrospectives
6. Verification: DRY compliance + personal focus validation

CONTEXT7 PATTERNS IMPLEMENTED:
- Extension Pattern: Builds on existing weekly_reporter.py infrastructure
- Adapter Pattern: Chat interface adapts existing report generation
- Command Pattern: Chat commands route to personal retrospective logic
- Lightweight Fallback: Graceful degradation when dependencies unavailable

BLOAT_PREVENTION: Extends existing infrastructure, no duplication
PROJECT_STRUCTURE: Located in .claudedirector/lib/reporting/ (compliant)
PERSONAL FOCUS: Individual reflection only - no business intelligence
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# REMOVED: JIRA dependencies - personal retrospective system should be standalone
# App already has centralized JIRA integration in .claudedirector/lib/integration/jira_client.py
# Personal retrospectives need NO business data, JIRA connections, or weekly reporter infrastructure

# Personal retrospective system runs completely standalone
WEEKLY_REPORTER_AVAILABLE = False  # Not needed for personal retrospectives
CHAT_BI_AVAILABLE = False  # Not needed for personal retrospectives


# Standalone ConversationalResponse for personal retrospectives
class ConversationalResponse:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 🚀 PHASE 1 EXTENSION: Retrospective Session Management (REUSE existing patterns)
# NOTE: Retrospective session management moved to retrospective_enabled_chat_reporter.py (DRY compliance)
# Removed: RetrospectiveStep, RetrospectiveSessionState, RetrospectiveSessionManager
# Weekly reporter should not manage retrospective sessions (Single Responsibility Principle)


class ChatEnhancedWeeklyReporter:
    """
    DEPRECATED: This class is no longer needed for personal retrospectives

    Personal retrospectives are now handled by RetrospectiveEnabledChatReporter
    which is completely standalone with NO JIRA dependencies.

    This file remains only for backward compatibility but should not be used
    for personal retrospective functionality.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}

        # REMOVED: All JIRA infrastructure - not needed for personal retrospectives
        # App already has centralized JIRA integration in integration/jira_client.py

        logger.info(
            "ChatEnhancedWeeklyReporter initialized in minimal mode - use RetrospectiveEnabledChatReporter for personal retrospectives"
        )

        # DEPRECATED: This class no longer handles any commands for personal retrospectives
        # Use RetrospectiveEnabledChatReporter instead
        self.extended_chat_commands = {
            "/help": self._handle_help_command,
        }

        # All other commands removed - not needed for personal retrospectives
        self.delegated_commands = set()

    async def process_chat_request(self, user_input: str) -> ConversationalResponse:
        """
        DEPRECATED: Use RetrospectiveEnabledChatReporter for personal retrospectives
        """

        return ConversationalResponse(
            success=False,
            response_text="⚠️ **This system is deprecated for personal retrospectives**\n\n"
            "Please use RetrospectiveEnabledChatReporter instead:\n"
            "• Import: `from .retrospective_enabled_chat_reporter import PersonalRetrospectiveSystem`\n"
            "• Commands: `/retrospective`, `/weekly-retrospective`, `/reflection`\n\n"
            "The personal retrospective system is now completely standalone with NO JIRA dependencies.",
            data={"deprecated": True, "redirect": "RetrospectiveEnabledChatReporter"},
            follow_up_suggestions=[
                "Use RetrospectiveEnabledChatReporter for personal retrospectives",
                "Try /retrospective command in the standalone system",
            ],
        )

    async def _handle_help_command(self, args: List[str]) -> ConversationalResponse:
        """Handle /help command - redirect to proper retrospective system"""

        help_text = """
⚠️ **DEPRECATED: ChatEnhancedWeeklyReporter**

**For Personal Retrospectives, use:**
`RetrospectiveEnabledChatReporter` - Standalone system with NO JIRA dependencies

**Available Retrospective Commands:**
• `/retrospective` - Start weekly retrospective process
• `/weekly-retrospective` - Alternative command for retrospective
• `/reflection` - Weekly reflection and progress tracking

**Personal Retrospective Questions:**
1. "What progress did I make this week?"
2. "How could I have done better?"
3. "On a scale of 1-10, how did I rate my week and why?"

**Why This Change:**
• Personal retrospectives should be standalone (NO business data)
• App already has centralized JIRA integration in `integration/jira_client.py`
• Eliminates unnecessary JIRA dependencies for personal reflection
"""

        return ConversationalResponse(
            success=True,
            response_text=help_text.strip(),
            data={"deprecated": True, "redirect": "RetrospectiveEnabledChatReporter"},
            follow_up_suggestions=[
                "Use RetrospectiveEnabledChatReporter for personal retrospectives",
                "Import: PersonalRetrospectiveSystem",
                "Try /retrospective command in standalone system",
            ],
        )


# REMOVED: All JIRA-related methods and Monte Carlo references - personal retrospectives should be standalone
# App already has:
# - Centralized JIRA integration in integration/jira_client.py
# - Monte Carlo simulation in weekly_reporter.py
# Personal retrospectives need NONE of these business analysis features


# Factory function for backward compatibility only
def create_chat_enhanced_weekly_reporter(
    config_path: str,
) -> ChatEnhancedWeeklyReporter:
    """Create deprecated Chat-Enhanced Weekly Reporter - Use RetrospectiveEnabledChatReporter instead"""
    return ChatEnhancedWeeklyReporter(config_path)


if __name__ == "__main__":
    print(
        "⚠️ DEPRECATED: Use RetrospectiveEnabledChatReporter for personal retrospectives"
    )
    print(
        "Personal retrospective system is now completely standalone with NO JIRA dependencies"
    )
