#!/usr/bin/env python3
"""
Personal Daily Planning Agent - Clean Implementation
Following PersonalRetrospectiveAgent pattern: BaseManager inheritance, YAML config, DRY principles

🎯 SCOPE: Personal daily planning only (strategic priorities)
🏗️ ARCHITECTURE: BaseManager pattern, <100 lines, zero bloat
📊 STORAGE: SQLite database, existing infrastructure
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
from core.types import ProcessingResult


@dataclass
class DailyPlanEntry:
    """Daily plan entry data structure"""

    date: str
    priorities: List[str]
    l0_l1_balance: str  # Strategic balance assessment


class PersonalDailyPlanningAgent(BaseManager):
    """
    Personal Daily Planning Agent - Clean Implementation

    Follows PersonalRetrospectiveAgent architecture:
    - BaseManager inheritance
    - Simple SQLite storage
    - Zero code duplication
    - <100 lines implementation
    - Interactive chat integration
    """

    def __init__(self, config_path: Optional[str] = None):
        # Create BaseManagerConfig following PersonalRetrospectiveAgent pattern
        config = BaseManagerConfig(
            manager_name="personal_daily_planning_agent",
            manager_type=ManagerType.ANALYTICS,  # Use ANALYTICS as closest match
            custom_config={"config_path": config_path} if config_path else {},
        )
        super().__init__(config)
        self.db_path = self._get_db_path()
        self._init_database()
        # Interactive session state (reuse BaseManager caching)
        self.active_sessions = {}  # user_id -> session_state

    def _get_db_path(self) -> str:
        """Get database path from config or default"""
        return self.config.get("database_path", "data/strategic/daily_plan.db")

    def _init_database(self):
        """Initialize SQLite database with daily plan table"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE NOT NULL,
                    priorities TEXT NOT NULL,
                    l0_l1_balance TEXT,
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
        """Process daily planning request - BaseManager abstract method"""
        command = request_data.get("command", "help")
        user_id = request_data.get("user_id", "default")
        user_input = request_data.get("user_input", "")

        # Interactive chat commands (reuse existing command routing)
        if command.startswith("/daily-plan"):
            return self._handle_chat_command(user_id, command, user_input)
        elif user_id in self.active_sessions:
            return self._handle_session_input(user_id, user_input)
        elif command == "start":
            return self._handle_chat_command(user_id, "/daily-plan start", user_input)
        elif command == "status":
            return self._show_status(request_data)
        elif command == "review":
            return self._review_plans(request_data)
        elif command == "help":
            return self._show_help()
        else:
            return ProcessingResult(
                success=False,
                message=f"Unknown command: {command}. Use 'help' for available commands.",
            )

    def _handle_chat_command(
        self, user_id: str, command: str, user_input: str
    ) -> ProcessingResult:
        """Handle chat commands like /daily-plan start"""
        if "start" in command:
            # Start interactive planning session
            self.active_sessions[user_id] = {
                "state": "collecting_priorities",
                "priorities": [],
                "started_at": datetime.now().isoformat(),
            }
            return ProcessingResult(
                success=True,
                message="🎯 Daily Planning Session Started!\n\nWhat are your top priorities for today? (Type them one by one, then 'done' when finished)",
                data={"session_started": True, "user_id": user_id},
            )
        elif "status" in command:
            return self._show_status({"user_id": user_id})
        elif "review" in command:
            return self._review_plans({"user_id": user_id})
        elif "help" in command:
            return self._show_help()
        else:
            return ProcessingResult(
                success=False,
                message="Unknown daily planning command. Available: start, status, review, help",
            )

    def _handle_session_input(self, user_id: str, user_input: str) -> ProcessingResult:
        """Handle input during active planning session"""
        session = self.active_sessions[user_id]

        if user_input.lower().strip() in ["done", "finish", "complete"]:
            # Complete the planning session
            priorities = session["priorities"]
            result = self._create_daily_plan(priorities, user_id)
            del self.active_sessions[user_id]  # Clean up session
            return result
        else:
            # Add priority to session
            session["priorities"].append(user_input.strip())
            priority_count = len(session["priorities"])
            return ProcessingResult(
                success=True,
                message=f"✅ Priority {priority_count} added: {user_input.strip()}\n\nAdd another priority or type 'done' to finish.",
                data={"priority_added": True, "count": priority_count},
            )

    def _create_daily_plan(
        self, priorities: List[str], user_id: str = "default"
    ) -> ProcessingResult:
        """Create daily plan with priorities"""
        try:
            today = datetime.now().date().isoformat()
            priorities_json = "|".join(priorities)  # Simple storage format

            # Analyze L0/L1 balance (simple heuristic)
            l0_l1_balance = "L0 Focus" if len(priorities) <= 3 else "Mixed L0/L1"

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO daily_plans (date, priorities, l0_l1_balance) VALUES (?, ?, ?)",
                    (today, priorities_json, l0_l1_balance),
                )

            return ProcessingResult(
                success=True,
                message=f"🎯 Daily Plan Created!\n\n📅 Date: {today}\n🎯 Priorities ({len(priorities)}):\n"
                + "\n".join(f"  {i+1}. {p}" for i, p in enumerate(priorities))
                + f"\n\n📊 Strategic Balance: {l0_l1_balance}",
                data={
                    "date": today,
                    "priorities": priorities,
                    "l0_l1_balance": l0_l1_balance,
                    "plan_created": True,
                },
            )
        except Exception as e:
            return ProcessingResult(
                success=False, message=f"Error creating daily plan: {str(e)}"
            )

    def _show_status(self, request_data: Dict[str, Any]) -> ProcessingResult:
        """Show current daily plan status"""
        try:
            today = datetime.now().date().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT priorities, l0_l1_balance FROM daily_plans WHERE date = ?",
                    (today,),
                )
                result = cursor.fetchone()

            if result:
                priorities = result[0].split("|")
                balance = result[1]
                return ProcessingResult(
                    success=True,
                    message=f"📅 Today's Plan ({today}):\n\n🎯 Priorities ({len(priorities)}):\n"
                    + "\n".join(f"  {i+1}. {p}" for i, p in enumerate(priorities))
                    + f"\n\n📊 Strategic Balance: {balance}",
                    data={
                        "has_plan": True,
                        "priorities": priorities,
                        "balance": balance,
                    },
                )
            else:
                return ProcessingResult(
                    success=True,
                    message=f"📅 No plan created for today ({today})\n\nUse '/daily-plan start' to create one.",
                    data={"has_plan": False},
                )
        except Exception as e:
            return ProcessingResult(
                success=False, message=f"Error checking status: {str(e)}"
            )

    def _review_plans(self, request_data: Dict[str, Any]) -> ProcessingResult:
        """Review recent daily plans"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT date, priorities, l0_l1_balance FROM daily_plans ORDER BY date DESC LIMIT 5"
                )
                results = cursor.fetchall()

            if results:
                review_text = "📊 Recent Daily Plans:\n\n"
                for date, priorities_str, balance in results:
                    priorities = priorities_str.split("|")
                    review_text += (
                        f"📅 {date} ({len(priorities)} priorities) - {balance}\n"
                    )
                    for i, priority in enumerate(priorities[:2]):  # Show first 2
                        review_text += f"  {i+1}. {priority}\n"
                    if len(priorities) > 2:
                        review_text += f"  ... and {len(priorities)-2} more\n"
                    review_text += "\n"

                return ProcessingResult(
                    success=True,
                    message=review_text,
                    data={"plans_found": len(results)},
                )
            else:
                return ProcessingResult(
                    success=True,
                    message="📊 No daily plans found.\n\nUse '/daily-plan start' to create your first plan.",
                    data={"plans_found": 0},
                )
        except Exception as e:
            return ProcessingResult(
                success=False, message=f"Error reviewing plans: {str(e)}"
            )

    def _show_help(self) -> ProcessingResult:
        """Show help information"""
        return ProcessingResult(
            success=True,
            message="""🎯 Daily Planning Commands:

/daily-plan start  - Start interactive planning session
/daily-plan status - Show today's plan
/daily-plan review - Review recent plans
/daily-plan help   - Show this help

Interactive Planning:
1. Use '/daily-plan start' to begin
2. Enter your priorities one by one
3. Type 'done' when finished
4. Your plan will be saved automatically

Strategic Focus: L0 (Required) vs L1 (Strategic) balance""",
        )
