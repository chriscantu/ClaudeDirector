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

from ..core.base_manager import BaseManager
from ..core.types import ProcessingResult


@dataclass
class RetrospectiveEntry:
    """Single retrospective entry with 3 questions"""

    date: str
    went_well: str
    could_improve: str
    next_focus: str


class PersonalRetrospectiveAgent(BaseManager):
    """
    Personal Retrospective Agent - Clean Implementation

    Follows PR #150 architecture:
    - BaseManager inheritance
    - YAML configuration
    - Zero code duplication
    - <100 lines implementation
    """

    def __init__(self, config_path: Optional[str] = None):
        super().__init__(
            manager_name="personal_retrospective_agent",
            manager_type="retrospective",
            config_path=config_path,
        )
        self.db_path = self._get_db_path()
        self._init_database()

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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def process_request(self, request_data: Dict[str, Any]) -> ProcessingResult:
        """Process retrospective request - BaseManager abstract method"""
        command = request_data.get("command", "help")

        if command == "create":
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
            )

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO retrospectives
                    (date, went_well, could_improve, next_focus)
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        entry.date,
                        entry.went_well,
                        entry.could_improve,
                        entry.next_focus,
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
                    SELECT date, went_well, could_improve, next_focus
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

3-Question Framework:
  1. What went well this week?
  2. What could have gone better?
  3. What will I focus on next week?
        """
        return ProcessingResult(success=True, message=help_text.strip())
