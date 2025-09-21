#!/usr/bin/env python3
"""
Personal Weekly Retrospective System - STANDALONE Implementation
Pure personal reflection system

Personal Weekly Retrospective - Simple 3-Question Chat System

FOCUS: Individual weekly reflection with 3 standardized questions
SCOPE: Personal progress tracking only - NO business intelligence

SIMPLE IMPLEMENTATION:
1. Ask 3 personal questions in sequence
2. Store responses for personal tracking
3. Complete standalone system with minimal dependencies

NO BUSINESS FEATURES:
- No external integrations
- No business metrics or KPIs
- No strategic analysis
- No performance analytics
- No ROI calculations
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

# Simple personal retrospective system - minimal dependencies
try:
    # Basic validation for personal retrospective responses
    from ..core.validation import (
        RetrospectiveValidator,
    )  # Basic input validation only

    VALIDATION_AVAILABLE = True
except ImportError:
    # Simple fallback validation for personal retrospectives
    VALIDATION_AVAILABLE = False

    class _SimpleValidator:
        def validate_progress_response(self, response: str) -> bool:
            return len(response.strip()) > 10

        def validate_improvement_response(self, response: str) -> bool:
            return len(response.strip()) > 10

        def validate_rating(self, rating: Any) -> bool:
            try:
                r = int(rating)
                return 1 <= r <= 10
            except:
                return False

        def validate_rating_explanation(self, explanation: str) -> bool:
            return len(explanation.strip()) > 5

    # Use simple validator for personal retrospectives
    RetrospectiveValidator = _SimpleValidator


# Standalone ConversationalResponse for personal retrospectives
@dataclass
class ConversationalResponse:
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 🚀 MINIMAL STATE MANAGEMENT: Lightweight enum (Context7 pattern)
class RetrospectiveStep(Enum):
    """Retrospective conversation steps - minimal state management"""

    PROGRESS = "progress"
    IMPROVEMENT = "improvement"
    RATING = "rating"
    COMPLETE = "complete"


@dataclass
class RetrospectiveSession:
    """
    Simple retrospective session data for personal tracking only
    """

    session_id: str
    current_step: RetrospectiveStep
    week_ending: str
    created_at: datetime
    responses: Dict[str, str] = field(default_factory=dict)  # Store personal responses


class PersonalRetrospectiveSystem:
    """
    Simple Personal Retrospective Chat System

    Handles 3 personal questions for weekly reflection:
    1. "What progress did I make this week?"
    2. "How could I have done better?"
    3. "On a scale of 1-10, how did I rate my week and why?"
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize simple retrospective system for personal reflection"""

        # Minimal configuration
        self.config_path = config_path or "personal_retrospective_config"

        # Basic validation for personal responses
        if VALIDATION_AVAILABLE:
            self.validator = RetrospectiveValidator()
        else:
            self.validator = RetrospectiveValidator()  # Uses fallback

        # Simple session tracking for personal retrospectives
        self.active_sessions: Dict[str, RetrospectiveSession] = {}

        # Simple command registry for personal retrospectives
        self.commands = {
            "/retrospective": self._handle_retrospective_command,
            "/weekly-retrospective": self._handle_retrospective_command,
            "/reflection": self._handle_retrospective_command,
        }

        logger.info("Personal Retrospective System initialized - 3 questions only")

    async def _handle_retrospective_command(
        self, user_input: str
    ) -> ConversationalResponse:
        """
        Handle simple personal retrospective commands - 3 questions only
        """

        try:
            # Parse command and extract user response
            parts = user_input.strip().split(maxsplit=1)
            command = parts[0].lower()
            user_response = parts[1] if len(parts) > 1 else ""

            # Simple user session (just using default for personal retrospectives)
            user_id = "personal_user"
            existing_session = self.active_sessions.get(user_id)

            if existing_session:
                # Continue existing session
                return await self._continue_retrospective_session(
                    existing_session, user_response
                )
            else:
                # Start new retrospective session
                return await self._start_new_retrospective_session(user_id)

        except Exception as e:
            logger.error(f"Error handling retrospective command: {e}")
            return ConversationalResponse(
                success=False,
                message="Sorry, I encountered an error processing your retrospective request.",
                error_message=str(e),
                suggestions=[
                    "Try starting a new retrospective with /retrospective",
                    "Check your input format",
                ],
            )

    async def _start_new_retrospective_session(
        self, user_id: str
    ) -> ConversationalResponse:
        """Start new personal retrospective session"""

        try:
            # Create simple session for personal retrospective
            session_id = f"retro_{int(datetime.now().timestamp())}"

            # Calculate week ending (Sunday)
            today = datetime.now()
            days_until_sunday = (6 - today.weekday()) % 7
            week_ending = (today + timedelta(days=days_until_sunday)).strftime(
                "%Y-%m-%d"
            )

            retrospective_session = RetrospectiveSession(
                session_id=session_id,
                current_step=RetrospectiveStep.PROGRESS,
                week_ending=week_ending,
                created_at=datetime.now(),
            )

            self.active_sessions[user_id] = retrospective_session

            return ConversationalResponse(
                success=True,
                message=f"🎯 **Personal Weekly Retrospective - Week Ending {week_ending}**\n\n"
                f"Let's reflect on your week! I'll ask you 3 simple questions.\n\n"
                f"**Question 1 of 3:** What progress did you make this week?\n\n"
                f"Please share your key accomplishments, learnings, or milestones.",
                data={
                    "session_id": session_id,
                    "current_step": "progress",
                    "week_ending": week_ending,
                },
                suggestions=[
                    "Share your key accomplishments",
                    "Mention any important learnings",
                    "Describe milestones you reached",
                ],
            )

        except Exception as e:
            logger.error(f"Error starting retrospective session: {e}")
            return ConversationalResponse(
                success=False,
                message="Sorry, I couldn't start your retrospective session.",
                error_message=str(e),
            )

    async def _continue_retrospective_session(
        self, session: RetrospectiveSession, user_response: str
    ) -> ConversationalResponse:
        """Continue personal retrospective session - 3 questions only"""

        try:
            if session.current_step == RetrospectiveStep.PROGRESS:
                if not self.validator.validate_progress_response(user_response):
                    return ConversationalResponse(
                        success=False,
                        message="Please provide a more detailed response about your progress (at least 10 characters).",
                        suggestions=[
                            "Share specific accomplishments",
                            "Mention key learnings",
                            "Describe completed tasks",
                        ],
                    )

                # Store progress response
                session.responses["progress"] = user_response
                session.current_step = RetrospectiveStep.IMPROVEMENT

                return ConversationalResponse(
                    success=True,
                    message="**Question 2 of 3:** How could you have done better this week?\n\n"
                    "Think about areas for improvement, missed opportunities, or lessons learned.",
                    data={"current_step": "improvement"},
                    suggestions=[
                        "Identify areas for improvement",
                        "Mention missed opportunities",
                        "Share lessons learned",
                    ],
                )

            elif session.current_step == RetrospectiveStep.IMPROVEMENT:
                if not self.validator.validate_improvement_response(user_response):
                    return ConversationalResponse(
                        success=False,
                        message="Please provide a more detailed response about improvements (at least 10 characters).",
                        suggestions=[
                            "Be specific about improvements",
                            "Mention actionable changes",
                            "Share learning opportunities",
                        ],
                    )

                # Store improvement response
                session.responses["improvement"] = user_response
                session.current_step = RetrospectiveStep.RATING

                return ConversationalResponse(
                    success=True,
                    message="**Question 3 of 3:** On a scale of 1-10, how would you rate your week?\n\n"
                    "Please provide your rating and a brief explanation why.\n"
                    "Format: `8 | Had great progress on key projects but missed some deadlines`",
                    data={"current_step": "rating"},
                    suggestions=[
                        "Rate from 1-10 with explanation",
                        "Consider both achievements and challenges",
                        "Be honest about your week's quality",
                    ],
                )

            elif session.current_step == RetrospectiveStep.RATING:
                # Parse rating and explanation
                try:
                    parts = user_response.split("|", 1)
                    rating_str = parts[0].strip()
                    explanation = parts[1].strip() if len(parts) > 1 else ""

                    if not self.validator.validate_rating(rating_str):
                        return ConversationalResponse(
                            success=False,
                            message="Please provide a valid rating from 1-10.",
                            suggestions=[
                                "Use format: '8 | explanation'",
                                "Rating must be between 1-10",
                            ],
                        )

                    if not self.validator.validate_rating_explanation(explanation):
                        return ConversationalResponse(
                            success=False,
                            message="Please provide an explanation for your rating.",
                            suggestions=[
                                "Use format: 'rating | explanation'",
                                "Explain why you chose this rating",
                            ],
                        )

                    # Store rating and explanation
                    session.responses["rating"] = rating_str
                    session.responses["rating_explanation"] = explanation

                    # Complete the retrospective session
                    return await self._complete_retrospective_session(session)

                except Exception as e:
                    return ConversationalResponse(
                        success=False,
                        message="Please use the format: `rating | explanation` (e.g., `8 | Great week with good progress`)",
                        suggestions=[
                            "Use format: 'number | explanation'",
                            "Rating must be 1-10",
                        ],
                    )

            else:
                return ConversationalResponse(
                    success=False,
                    message="This retrospective session is already complete. Start a new one with /retrospective",
                )

        except Exception as e:
            logger.error(f"Error continuing retrospective session: {e}")
            return ConversationalResponse(
                success=False,
                message="Sorry, I encountered an error processing your response.",
                error_message=str(e),
            )

    async def _complete_retrospective_session(
        self, session: RetrospectiveSession
    ) -> ConversationalResponse:
        """Complete personal retrospective session"""

        try:
            # Clean up session
            user_id = "personal_user"
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]

            session.current_step = RetrospectiveStep.COMPLETE

            return ConversationalResponse(
                success=True,
                message=f"🎉 **Personal Retrospective Complete!**\n\n"
                f"Thank you for reflecting on your week ending {session.week_ending}. "
                f"Your responses have been saved.\n\n"
                f"**Your 3 Responses:**\n"
                f"1. **Progress**: {session.responses.get('progress', 'N/A')[:50]}...\n"
                f"2. **Improvement**: {session.responses.get('improvement', 'N/A')[:50]}...\n"
                f"3. **Rating**: {session.responses.get('rating', 'N/A')}/10 - {session.responses.get('rating_explanation', 'N/A')[:30]}...\n\n"
                f"Start your next retrospective anytime with `/retrospective`",
                data={
                    "session_completed": True,
                    "week_ending": session.week_ending,
                    "responses": session.responses,
                },
                suggestions=[
                    "Start next week's retrospective with /retrospective",
                    "Review your weekly progress patterns",
                    "Set goals based on improvement areas",
                ],
            )

        except Exception as e:
            logger.error(f"Error completing retrospective session: {e}")
            return ConversationalResponse(
                success=False,
                message="Your retrospective responses were saved, but I encountered an error completing the session.",
                error_message=str(e),
            )

    async def process_command(self, user_input: str) -> ConversationalResponse:
        """Main entry point for processing simple personal retrospective commands"""

        command = user_input.strip().lower()

        if command in self.commands:
            handler = self.commands[command]
            return await handler(user_input)
        else:
            return ConversationalResponse(
                success=False,
                message=f"Unknown command: {command}. Available commands: {', '.join(self.commands.keys())}",
                suggestions=[
                    "Use /retrospective to start a new retrospective",
                    "Use /weekly-retrospective for weekly reflection",
                    "Use /reflection for general reflection",
                ],
            )


# Simple factory function
def create_personal_retrospective_system(
    config_path: Optional[str] = None,
) -> PersonalRetrospectiveSystem:
    """Create simple personal retrospective system - 3 questions only"""
    return PersonalRetrospectiveSystem(config_path)


# CLI interface for testing
async def main():
    """CLI interface for testing simple personal retrospective system"""
    import sys

    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    retrospective_system = create_personal_retrospective_system(config_path)

    print("🎯 Simple Personal Weekly Retrospective System")
    print("3 questions: Progress, Improvement, Rating")
    print("Available commands: /retrospective, /weekly-retrospective, /reflection")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit"]:
                break

            if user_input.startswith("/"):
                response = await retrospective_system.process_command(user_input)
                print(f"\nAssistant: {response.message}")
                if response.suggestions:
                    print("\nSuggestions:")
                    for suggestion in response.suggestions:
                        print(f"  • {suggestion}")
                print()
            else:
                print(
                    "Please use a retrospective command: /retrospective, /weekly-retrospective, or /reflection\n"
                )

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")

    print("Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
