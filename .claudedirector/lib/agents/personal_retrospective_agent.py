#!/usr/bin/env python3
"""
Personal Retrospective Agent - Clean Implementation
Following PR #150 patterns: BaseManager inheritance, YAML config, DRY principles

🎯 SCOPE: Personal reflection only (3 questions)
🏗️ ARCHITECTURE: BaseManager pattern, <100 lines, zero bloat
📊 STORAGE: SQLite database, existing infrastructure
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType
from ..core.types import ProcessingResult


@dataclass
class RetrospectiveEntry:
    """Single retrospective entry with 4 questions"""

    date: str
    went_well: str
    could_improve: str
    next_focus: str
    rating: int


class PersonalRetrospectiveAgent(BaseManager):
    """
    Personal Retrospective Agent - Clean Implementation

    Follows PR #150 architecture:
    - BaseManager inheritance
    - YAML configuration
    - Zero code duplication
    - <100 lines implementation

    Phase 2: Interactive chat integration
    """

    def __init__(self, config_path: Optional[str] = None):
        # Create BaseManagerConfig following the pattern
        config = BaseManagerConfig(
            manager_name="personal_retrospective_agent",
            manager_type=ManagerType.ANALYTICS,  # Use ANALYTICS as closest match
            custom_config={"config_path": config_path} if config_path else {},
        )
        super().__init__(config)
        self.db_path = self._get_db_path()
        self._init_database()
        # Phase 2: Interactive session state (reuse BaseManager caching)
        self.active_sessions = {}  # user_id -> session_state

    def _get_db_path(self) -> str:
        """Get database path from config or default"""
        return self.config.get("database_path", "data/strategic/retrospective.db")

    def _init_database(self):
        """Initialize SQLite database with retrospective table"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS retrospectives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE NOT NULL,
                    went_well TEXT NOT NULL,
                    could_improve TEXT NOT NULL,
                    next_focus TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def manage(self, operation: str, *args, **kwargs) -> ProcessingResult:
        """Execute manager operation - BaseManager abstract method implementation"""
        # Convert operation to request_data format for backward compatibility
        if isinstance(operation, str) and args and isinstance(args[0], dict):
            request_data = args[0]
            request_data["command"] = operation
        else:
            request_data = kwargs.get("request_data", {"command": operation})

        return self.process_request(request_data)

    def process_request(self, request_data: Dict[str, Any]) -> ProcessingResult:
        """Process retrospective request - BaseManager abstract method"""
        command = request_data.get("command", "help")
        user_id = request_data.get("user_id", "default")
        user_input = request_data.get("user_input", "")

        # Phase 2: Interactive chat commands (reuse existing command routing)
        if command.startswith("/retrospective"):
            return self._handle_chat_command(user_id, command, user_input)
        elif user_id in self.active_sessions:
            return self._handle_session_input(user_id, user_input)
        elif command == "create":
            return self._create_retrospective(request_data)
        elif command == "view":
            return self._view_retrospectives(request_data)
        elif command == "help":
            return self._show_help()
        else:
            return ProcessingResult(
                success=False,
                message=f"Unknown command: {command}. Use 'help' for available commands.",
            )

    def _create_retrospective(self, data: Dict[str, Any]) -> ProcessingResult:
        """Create new retrospective entry"""
        try:
            entry = RetrospectiveEntry(
                date=data.get("date", datetime.now().strftime("%Y-%m-%d")),
                went_well=data.get("went_well", ""),
                could_improve=data.get("could_improve", ""),
                next_focus=data.get("next_focus", ""),
                rating=data.get("rating", 5),
            )

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO retrospectives
                    (date, went_well, could_improve, next_focus, rating)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        entry.date,
                        entry.went_well,
                        entry.could_improve,
                        entry.next_focus,
                        entry.rating,
                    ),
                )

            return ProcessingResult(
                success=True,
                message=f"Retrospective saved for {entry.date}",
                data={"entry": entry},
            )
        except Exception as e:
            return ProcessingResult(
                success=False, message=f"Error saving retrospective: {e}"
            )

    def _view_retrospectives(self, data: Dict[str, Any]) -> ProcessingResult:
        """View retrospective entries"""
        try:
            limit = data.get("limit", 5)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT date, went_well, could_improve, next_focus, rating
                    FROM retrospectives
                    ORDER BY date DESC
                    LIMIT ?
                """,
                    (limit,),
                )

                entries = [
                    RetrospectiveEntry(
                        date=row[0],
                        went_well=row[1],
                        could_improve=row[2],
                        next_focus=row[3],
                        rating=row[4],
                    )
                    for row in cursor.fetchall()
                ]

            return ProcessingResult(
                success=True,
                message=f"Retrieved {len(entries)} retrospective entries",
                data={"entries": entries},
            )
        except Exception as e:
            return ProcessingResult(
                success=False, message=f"Error retrieving retrospectives: {e}"
            )

    def _show_help(self) -> ProcessingResult:
        """Show help information"""
        help_text = """
Personal Retrospective Agent - Clean Implementation

Commands:
  create    - Create new retrospective entry
  view      - View recent retrospective entries
  help      - Show this help message

Chat Commands (Phase 2):
  /retrospective create  - Start interactive retrospective
  /retrospective view    - View recent retrospectives
  /retrospective help    - Show this help

4-Question Framework:
  1. What went well this week?
  2. What could have gone better?
  3. What will I focus on next week?
  4. How would I rate this week on a scale of 1-10?
        """
        return ProcessingResult(success=True, message=help_text.strip())

    # Phase 2: Interactive Chat Methods (DRY - extends existing patterns)
    def _handle_chat_command(
        self, user_id: str, command: str, user_input: str
    ) -> ProcessingResult:
        """Handle /retrospective chat commands (reuse existing command logic)"""
        if command == "/retrospective create":
            return self._start_interactive_session(user_id)
        elif command == "/retrospective view":
            return self._view_retrospectives({"limit": 5})
        elif command == "/retrospective help":
            return self._show_help()
        else:
            return ProcessingResult(
                success=False,
                message="Unknown chat command. Use '/retrospective help' for available commands.",
            )

    def _start_interactive_session(self, user_id: str) -> ProcessingResult:
        """Start interactive retrospective session (reuse BaseManager session patterns)"""
        questions = [
            "What went well this week?",
            "What could have gone better?",
            "What will I focus on next week?",
            "How would I rate this week on a scale of 1-10?",
        ]

        self.active_sessions[user_id] = {
            "step": 0,
            "questions": questions,
            "responses": {},
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

        return ProcessingResult(
            success=True,
            message=f"Starting retrospective for {self.active_sessions[user_id]['date']}\n\nQuestion 1: {questions[0]}",
        )

    def _handle_session_input(self, user_id: str, user_input: str) -> ProcessingResult:
        """Handle user input during active session (reuse existing response patterns)"""
        session = self.active_sessions[user_id]
        current_step = session["step"]
        questions = session["questions"]

        # Store response
        session["responses"][questions[current_step]] = user_input.strip()

        # Move to next question or complete
        if current_step < len(questions) - 1:
            session["step"] += 1
            next_question = questions[session["step"]]
            return ProcessingResult(
                success=True, message=f"Question {session['step'] + 1}: {next_question}"
            )
        else:
            # Complete retrospective (reuse existing _create_retrospective logic)
            rating_text = session["responses"].get(questions[3], "5")
            try:
                rating = int(rating_text)
                if rating < 1 or rating > 10:
                    rating = 5  # Default to 5 if invalid
            except ValueError:
                rating = 5  # Default to 5 if not a number

            result = self._create_retrospective(
                {
                    "date": session["date"],
                    "went_well": session["responses"].get(questions[0], ""),
                    "could_improve": session["responses"].get(questions[1], ""),
                    "next_focus": session["responses"].get(questions[2], ""),
                    "rating": rating,
                }
            )

            # Clean up session
            del self.active_sessions[user_id]

            if result.success:
                return ProcessingResult(
                    success=True,
                    message=f"✅ Retrospective completed and saved!\n\nUse '/retrospective view' to see your entries.",
                )
            else:
                return result
