#!/usr/bin/env python3
"""
Ultra-Minimal Daily Planning Implementation - Terminal Safe
No database initialization during __init__ to avoid hangs

🎯 SCOPE: Minimal daily planning without any blocking operations
🏗️ ARCHITECTURE: Lazy database initialization, no blocking I/O
📊 COMPLIANCE: BLOAT_PREVENTION_SYSTEM.md - minimal, focused implementation
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ProcessingResult:
    """Minimal processing result"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class UltraMinimalDailyPlanningAgent:
    """
    Ultra-Minimal Daily Planning Agent - Terminal Safe

    No initialization blocking operations.
    Lazy database initialization only when needed.
    """

    def __init__(self):
        self.db_path = "data/strategic/daily_plan.db"
        self.active_sessions = {}  # user_id -> session_state
        self._db_initialized = False

    def _ensure_database(self):
        """Lazy database initialization - only when needed"""
        if self._db_initialized:
            return

        try:
            # Create directory with timeout protection
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)

            # Test database connection with timeout
            with sqlite3.connect(self.db_path, timeout=5.0) as conn:
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
                conn.commit()
            self._db_initialized = True
        except Exception as e:
            # Log error but don't fail - database will be retried on next operation
            print(f"Database initialization failed: {e}")
            self._db_initialized = False

    def process_request(self, request_data: Dict[str, Any]) -> ProcessingResult:
        """Process daily planning request"""
        command = request_data.get("command", "help")
        user_id = request_data.get("user_id", "default")
        user_input = request_data.get("user_input", "")

        # Handle commands
        if command == "/daily-plan start":
            return self._start_planning_session(user_id)
        elif command == "/daily-plan status":
            return self._show_status(user_id)
        elif command == "/daily-plan review":
            return self._review_plans()
        elif command == "/daily-plan help":
            return self._show_help()
        elif user_id in self.active_sessions:
            return self._handle_session_input(user_id, user_input)
        else:
            return ProcessingResult(
                success=False,
                message=f"Unknown command: {command}. Use '/daily-plan help' for available commands.",
            )

    def _start_planning_session(self, user_id: str) -> ProcessingResult:
        """Start interactive planning session"""
        self.active_sessions[user_id] = {
            "priorities": [],
            "started_at": datetime.now().isoformat(),
        }

        return ProcessingResult(
            success=True,
            message="🎯 Starting daily planning session!\n\n📝 Enter your priorities (type 'done' when finished):",
            data={"session_started": True},
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
        """Create and save daily plan"""
        if not priorities:
            return ProcessingResult(
                success=False,
                message="❌ No priorities provided. Please add at least one priority.",
            )

        # Assess L0/L1 balance
        l0_count = sum(
            1
            for p in priorities
            if any(
                keyword in p.lower()
                for keyword in [
                    "strategic",
                    "planning",
                    "architecture",
                    "roadmap",
                    "vision",
                ]
            )
        )
        l1_count = len(priorities) - l0_count

        if l0_count > l1_count:
            balance = "L0 Heavy - Strategic focus"
        elif l1_count > l0_count:
            balance = "L1 Heavy - Execution focus"
        else:
            balance = "Balanced - Good L0/L1 mix"

        # Save to SQLite database (required)
        try:
            self._ensure_database()
            today = datetime.now().strftime("%Y-%m-%d")
            priorities_json = ",".join(priorities)

            # Force database initialization if not already done
            if not self._db_initialized:
                self._ensure_database()

            # Save to database with timeout protection
            with sqlite3.connect(self.db_path, timeout=10.0) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO daily_plans (date, priorities, l0_l1_balance) VALUES (?, ?, ?)",
                    (today, priorities_json, balance),
                )
                conn.commit()

            return ProcessingResult(
                success=True,
                message=f"✅ Daily plan created and saved to SQLite!\n\n📅 Date: {today}\n🎯 Priorities: {len(priorities)}\n⚖️ Balance: {balance}\n\nUse '/daily-plan status' to view your plan.",
                data={
                    "plan_created": True,
                    "date": today,
                    "priorities_count": len(priorities),
                    "persisted": True,
                },
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                message=f"❌ Failed to save daily plan to SQLite database: {str(e)}\n\nPlease check database permissions and try again.",
            )

    def _show_status(self, user_id: str) -> ProcessingResult:
        """Show today's plan status"""
        try:
            self._ensure_database()

            # Force database initialization if not already done
            if not self._db_initialized:
                self._ensure_database()

            today = datetime.now().strftime("%Y-%m-%d")

            with sqlite3.connect(self.db_path, timeout=10.0) as conn:
                cursor = conn.execute(
                    "SELECT priorities, l0_l1_balance FROM daily_plans WHERE date = ?",
                    (today,),
                )
                row = cursor.fetchone()

            if row:
                priorities = row[0].split(",") if row[0] else []
                balance = row[1] or "Not assessed"

                return ProcessingResult(
                    success=True,
                    message=f"📅 Today's Plan ({today})\n\n🎯 Priorities:\n"
                    + "\n".join(f"  • {p}" for p in priorities)
                    + f"\n\n⚖️ Strategic Balance: {balance}",
                    data={
                        "has_plan": True,
                        "priorities": priorities,
                        "balance": balance,
                    },
                )
            else:
                return ProcessingResult(
                    success=True,
                    message=f"📅 No plan found for today ({today})\n\nUse '/daily-plan start' to create today's plan.",
                    data={"has_plan": False},
                )
        except Exception as e:
            return ProcessingResult(
                success=False,
                message=f"❌ Failed to retrieve plan status from SQLite database: {str(e)}\n\nPlease check database permissions and try again.",
            )

    def _review_plans(self) -> ProcessingResult:
        """Review recent plans"""
        try:
            self._ensure_database()

            # Force database initialization if not already done
            if not self._db_initialized:
                self._ensure_database()

            with sqlite3.connect(self.db_path, timeout=10.0) as conn:
                cursor = conn.execute(
                    "SELECT date, priorities, l0_l1_balance FROM daily_plans ORDER BY date DESC LIMIT 7"
                )
                rows = cursor.fetchall()

            if not rows:
                return ProcessingResult(
                    success=True,
                    message="📊 No daily plans found in SQLite database\n\nUse '/daily-plan start' to create your first plan.",
                    data={"plans_count": 0},
                )

            message = "📊 Recent Daily Plans (Last 7 days)\n" + "=" * 40 + "\n"
            for row in rows:
                date, priorities_str, balance = row
                priorities = priorities_str.split(",") if priorities_str else []
                message += f"\n📅 {date}\n"
                message += f"🎯 Priorities: {len(priorities)}\n"
                message += f"⚖️ Balance: {balance or 'Not assessed'}\n"
                message += "-" * 20 + "\n"

            return ProcessingResult(
                success=True, message=message, data={"plans_count": len(rows)}
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                message=f"❌ Failed to review plans from SQLite database: {str(e)}\n\nPlease check database permissions and try again.",
            )

    def _show_help(self) -> ProcessingResult:
        """Show help information"""
        help_text = """
🎯 Daily Planning Commands
==========================

COMMANDS:
  /daily-plan start    - Start interactive planning session
  /daily-plan status   - Show today's plan
  /daily-plan review    - Review recent plans (last 7 days)
  /daily-plan help     - Show this help

USAGE:
  1. Start planning: /daily-plan start
  2. Add priorities one by one
  3. Type 'done' when finished
  4. View your plan: /daily-plan status

FEATURES:
  ✅ Strategic balance assessment (L0/L1)
  ✅ SQLite database persistence (required)
  ✅ Interactive session management
  ✅ Recent plans review
  ✅ Terminal-safe implementation
        """

        return ProcessingResult(
            success=True, message=help_text.strip(), data={"help_shown": True}
        )
