#!/usr/bin/env python3
"""
Consolidated Stakeholder Manager
Business logic for comprehensive stakeholder management with AI detection
Consolidates StakeholderManager and StakeholderAIManager using DRY principles
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ...context_engineering.stakeholder_intelligence_unified import (
    StakeholderIntelligence as StakeholderEngagementEngine,
)


class ConsolidatedStakeholderManager:
    """
    Unified stakeholder management with both manual and AI-powered capabilities
    Consolidates duplicate functionality from multiple manager classes
    """

    def __init__(self):
        self.engine = StakeholderEngagementEngine()

    # Manual stakeholder management methods
    def add_stakeholder(self, stakeholder_key: str, stakeholder_data: Dict) -> bool:
        """Add stakeholder with validation"""
        try:
            # Validate required fields
            required_fields = ["name", "role", "priorities"]
            for field in required_fields:
                if field not in stakeholder_data:
                    raise ValueError(f"Missing required field: {field}")

            # Add stakeholder through engine
            return self.engine.add_stakeholder(stakeholder_key, stakeholder_data)
        except Exception as e:
            print(f"Error adding stakeholder: {e}")
            return False

    def update_stakeholder(self, stakeholder_key: str, updates: Dict) -> bool:
        """Update existing stakeholder"""
        try:
            return self.engine.update_stakeholder(stakeholder_key, updates)
        except Exception as e:
            print(f"Error updating stakeholder: {e}")
            return False

    def get_stakeholder(self, stakeholder_key: str) -> Optional[Dict]:
        """Get stakeholder by key"""
        try:
            return self.engine.get_stakeholder(stakeholder_key)
        except Exception as e:
            print(f"Error retrieving stakeholder: {e}")
            return None

    def list_stakeholders(self) -> List[Dict]:
        """List all stakeholders"""
        try:
            return self.engine.list_all_stakeholders()
        except Exception as e:
            print(f"Error listing stakeholders: {e}")
            return []

    # AI-powered stakeholder detection methods
    def process_workspace_automatically(
        self, workspace_dir: Optional[Path] = None
    ) -> Dict:
        """Process workspace for automatic stakeholder detection"""
        if workspace_dir is None:
            workspace_dir = Path.cwd() / "workspace" / "meeting-prep"

        try:
            if not workspace_dir.exists():
                return {
                    "status": "error",
                    "message": f"Workspace directory not found: {workspace_dir}",
                }

            # Scan workspace for stakeholder mentions
            detected_stakeholders = self._scan_workspace_files(workspace_dir)

            # Process with AI engine
            results = self.engine.process_detected_stakeholders(detected_stakeholders)

            return {
                "status": "success",
                "detected_count": len(detected_stakeholders),
                "processed_results": results,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _scan_workspace_files(self, workspace_dir: Path) -> List[Dict]:
        """Scan workspace files for stakeholder mentions"""
        detected = []

        for file_path in workspace_dir.rglob("*.md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Simple stakeholder detection patterns
                stakeholder_patterns = [
                    r"@(\w+)",  # @mentions
                    r"([A-Z][a-z]+ [A-Z][a-z]+)",  # Names
                    r"VP[^a-z]*([A-Z][a-z]+)",  # VP titles
                    r"Director[^a-z]*([A-Z][a-z]+)",  # Director titles
                ]

                import re

                for pattern in stakeholder_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        detected.append(
                            {
                                "name": match,
                                "source_file": str(file_path),
                                "detection_method": "pattern_match",
                                "confidence": 0.7,
                            }
                        )
            except Exception as e:
                continue

        return detected

    # Consolidated utility methods
    def generate_stakeholder_report(self) -> Dict:
        """Generate comprehensive stakeholder report"""
        try:
            stakeholders = self.list_stakeholders()

            report = {
                "total_stakeholders": len(stakeholders),
                "last_updated": datetime.now().isoformat(),
                "stakeholders_by_role": {},
                "high_priority_stakeholders": [],
                "recent_interactions": [],
            }

            # Categorize by role
            for stakeholder in stakeholders:
                role = stakeholder.get("role", "Unknown")
                if role not in report["stakeholders_by_role"]:
                    report["stakeholders_by_role"][role] = 0
                report["stakeholders_by_role"][role] += 1

                # Identify high priority
                if stakeholder.get("priority", "medium") == "high":
                    report["high_priority_stakeholders"].append(stakeholder["name"])

            return report
        except Exception as e:
            return {"error": str(e)}

    def get_recommendations(self) -> List[Dict]:
        """Get AI-powered stakeholder engagement recommendations"""
        try:
            return self.engine.get_engagement_recommendations()
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    # Interactive methods for CLI usage
    def add_stakeholder_interactive(self) -> bool:
        """Interactive stakeholder addition"""
        print("🎯 Add New Stakeholder")
        print("=" * 30)

        stakeholder_key = input("Stakeholder key (e.g., 'vp_engineering'): ").strip()
        if not stakeholder_key:
            print("Error: Stakeholder key required")
            return False

        name = input("Full name: ").strip()
        role = input("Role/Title: ").strip()
        priorities = input("Key priorities (comma-separated): ").strip()

        stakeholder_data = {
            "name": name,
            "role": role,
            "priorities": [p.strip() for p in priorities.split(",") if p.strip()],
            "added_date": datetime.now().isoformat(),
            "status": "active",
        }

        success = self.add_stakeholder(stakeholder_key, stakeholder_data)
        if success:
            print(f"✅ Successfully added stakeholder: {name}")
        else:
            print(f"❌ Failed to add stakeholder: {name}")

        return success
