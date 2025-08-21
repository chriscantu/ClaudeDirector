#!/usr/bin/env python3
"""
CLI Context Bridge - Cross-Environment Context Preservation
Martin's solution for seamless Cursor ↔ CLI strategic context continuity
"""

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List
from pathlib import Path

from memory.session_context_manager import SessionContextManager


class CLIContextBridge:
    """
    Bridge ClaudeDirector strategic context between Cursor and CLI environments
    Enables seamless context preservation across different AI interfaces
    """

    def __init__(self, db_path: str = None):
        """Initialize CLI context bridge with database connection"""
        if db_path is None:
            # Default to ClaudeDirector strategic memory database
            base_path = Path(__file__).parent.parent.parent.parent.parent
            db_path = base_path / ".claudedirector" / "data" / "strategic_memory.db"

        self.db_path = str(db_path)
        self.session_manager = SessionContextManager(self.db_path)

    def export_current_context(self, format_type: str = "markdown", output_file: str = None) -> str:
        """
        Export current strategic context in portable format

        Args:
            format_type: 'markdown', 'json', or 'yaml'
            output_file: Optional file path to save export

        Returns:
            Formatted context string
        """
        # Get current strategic context
        strategic_context = self._gather_strategic_context()
        session_context = self._gather_session_context()

        if format_type == "markdown":
            exported_content = self._format_markdown_export(strategic_context, session_context)
        elif format_type == "json":
            exported_content = self._format_json_export(strategic_context, session_context)
        elif format_type == "yaml":
            exported_content = self._format_yaml_export(strategic_context, session_context)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(exported_content)

        return exported_content

    def import_context_from_file(self, file_path: str) -> bool:
        """
        Import strategic context from exported file

        Args:
            file_path: Path to context export file

        Returns:
            True if import successful
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Detect format and parse
            if file_path.endswith('.json'):
                context_data = json.loads(content)
            elif file_path.endswith('.md'):
                context_data = self._parse_markdown_context(content)
            else:
                # Try to detect format from content
                context_data = self._auto_parse_context(content)

            # Import into database
            return self._import_strategic_context(context_data)

        except Exception as e:
            print(f"❌ Context import failed: {e}")
            return False

    def create_cli_session_export(self) -> str:
        """
        Create CLI-optimized context export for immediate use

        Returns:
            Markdown-formatted context ready for CLI sharing
        """
        strategic_context = self._gather_strategic_context()
        session_context = self._gather_session_context()

        cli_export = f"""# ClaudeDirector Strategic Context - CLI Session
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source**: Cursor Session Strategic Memory

## 🎯 **Current Strategic Context**

### **Active Stakeholders**
{self._format_stakeholders_for_cli(strategic_context.get('stakeholders', []))}

### **Strategic Initiatives**
{self._format_initiatives_for_cli(strategic_context.get('initiatives', []))}

### **Recent Strategic Intelligence**
{self._format_intelligence_for_cli(strategic_context.get('intelligence', []))}

### **Current Session Context**
{self._format_session_for_cli(session_context)}

---

## 📋 **For CLI Continuation**

**Context Summary**: {self._generate_context_summary(strategic_context, session_context)}

**Key Personas**: {self._extract_active_personas(session_context)}

**Next Actions**: {self._extract_pending_actions(session_context)}

---

**Usage**: Share this context when starting CLI sessions to maintain strategic continuity.
"""
        return cli_export

    def _gather_strategic_context(self) -> Dict[str, Any]:
        """Gather current strategic context from database"""
        context = {
            'stakeholders': [],
            'initiatives': [],
            'intelligence': []
        }

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get stakeholder intelligence
                cursor = conn.execute("""
                    SELECT stakeholder_id, title, summary, position_on_platform,
                           influence_level, strategic_importance, recent_interactions
                    FROM stakeholder_intelligence
                    ORDER BY updated_at DESC
                """)
                context['stakeholders'] = [
                    {
                        'id': row[0], 'title': row[1], 'summary': row[2],
                        'position': row[3], 'influence': row[4],
                        'importance': row[5], 'recent': row[6]
                    }
                    for row in cursor.fetchall()
                ]

                # Get strategic intelligence
                cursor = conn.execute("""
                    SELECT intelligence_id, category, title, content,
                           business_impact, confidence_level, tags
                    FROM strategic_intelligence
                    ORDER BY updated_at DESC
                """)
                context['intelligence'] = [
                    {
                        'id': row[0], 'category': row[1], 'title': row[2],
                        'content': row[3], 'impact': row[4],
                        'confidence': row[5], 'tags': row[6]
                    }
                    for row in cursor.fetchall()
                ]

        except Exception as e:
            print(f"⚠️ Error gathering strategic context: {e}")

        return context

    def _gather_session_context(self) -> Dict[str, Any]:
        """Gather current session context from database"""
        context = {}

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get most recent session
                cursor = conn.execute("""
                    SELECT session_id, session_type, active_personas,
                           stakeholder_context, strategic_initiatives_context,
                           conversation_thread, decision_context, action_items_context,
                           context_quality_score, last_backup_timestamp
                    FROM session_context
                    ORDER BY last_backup_timestamp DESC LIMIT 1
                """)

                row = cursor.fetchone()
                if row:
                    context = {
                        'session_id': row[0],
                        'session_type': row[1],
                        'active_personas': json.loads(row[2] or '[]'),
                        'stakeholder_context': json.loads(row[3] or '{}'),
                        'initiatives_context': json.loads(row[4] or '{}'),
                        'conversation_thread': json.loads(row[5] or '[]'),
                        'decisions': json.loads(row[6] or '[]'),
                        'action_items': json.loads(row[7] or '[]'),
                        'quality_score': row[8],
                        'last_backup': row[9]
                    }

        except Exception as e:
            print(f"⚠️ Error gathering session context: {e}")

        return context

    def _format_markdown_export(self, strategic_context: Dict, session_context: Dict) -> str:
        """Format context as comprehensive markdown export"""
        export_content = f"""# ClaudeDirector Strategic Context Export
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Quality Score**: {session_context.get('quality_score', 'N/A')}

## 🎯 Strategic Context

### Stakeholders
{self._format_stakeholders_detailed(strategic_context.get('stakeholders', []))}

### Strategic Intelligence
{self._format_intelligence_detailed(strategic_context.get('intelligence', []))}

## 📋 Session Context

### Active Personas
{', '.join(session_context.get('active_personas', []))}

### Recent Decisions
{self._format_decisions(session_context.get('decisions', []))}

### Pending Actions
{self._format_actions(session_context.get('action_items', []))}

### Conversation Context
{self._format_conversation_thread(session_context.get('conversation_thread', []))}
"""
        return export_content

    def _format_stakeholders_for_cli(self, stakeholders: List[Dict]) -> str:
        """Format stakeholders for CLI consumption"""
        if not stakeholders:
            return "No active stakeholders"

        formatted = []
        for stakeholder in stakeholders[:5]:  # Top 5 for CLI brevity
            formatted.append(f"• **{stakeholder['title']}**: {stakeholder['summary'][:100]}...")

        return '\n'.join(formatted)

    def _format_initiatives_for_cli(self, initiatives: List[Dict]) -> str:
        """Format initiatives for CLI consumption"""
        if not initiatives:
            return "No active initiatives"

        # Extract from strategic intelligence with business strategy category
        formatted = []
        for item in initiatives:
            if item.get('category') == 'BUSINESS_STRATEGY':
                formatted.append(f"• **{item['title']}**: {item['content'][:100]}...")

        return '\n'.join(formatted) if formatted else "No active strategic initiatives"

    def _format_intelligence_for_cli(self, intelligence: List[Dict]) -> str:
        """Format strategic intelligence for CLI consumption"""
        if not intelligence:
            return "No recent intelligence"

        formatted = []
        for item in intelligence[:3]:  # Top 3 for CLI brevity
            formatted.append(f"• **{item['title']}** ({item['category']}): {item['content'][:80]}...")

        return '\n'.join(formatted)

    def _format_session_for_cli(self, session_context: Dict) -> str:
        """Format session context for CLI consumption"""
        if not session_context:
            return "No active session context"

        lines = []
        if session_context.get('session_type'):
            lines.append(f"**Session Type**: {session_context['session_type']}")

        if session_context.get('active_personas'):
            lines.append(f"**Active Personas**: {', '.join(session_context['active_personas'])}")

        if session_context.get('quality_score'):
            lines.append(f"**Context Quality**: {session_context['quality_score']:.1%}")

        return '\n'.join(lines) if lines else "Minimal session context available"

    def _generate_context_summary(self, strategic_context: Dict, session_context: Dict) -> str:
        """Generate concise context summary for CLI use"""
        stakeholder_count = len(strategic_context.get('stakeholders', []))
        intelligence_count = len(strategic_context.get('intelligence', []))
        session_type = session_context.get('session_type', 'strategic')

        return f"{session_type.title()} session with {stakeholder_count} stakeholders, {intelligence_count} intelligence items"

    def _extract_active_personas(self, session_context: Dict) -> str:
        """Extract active personas for CLI reference"""
        personas = session_context.get('active_personas', [])
        return ', '.join(personas) if personas else 'No active personas'

    def _extract_pending_actions(self, session_context: Dict) -> str:
        """Extract pending actions for CLI reference"""
        actions = session_context.get('action_items', [])
        if actions:
            return f"{len(actions)} pending actions (see full export for details)"
        return "No pending actions"

    # Additional helper methods for detailed formatting...
    def _format_stakeholders_detailed(self, stakeholders: List[Dict]) -> str:
        if not stakeholders:
            return "No stakeholders"

        formatted = []
        for s in stakeholders:
            formatted.append(f"""
**{s['title']}**
- Position: {s['position']}
- Influence: {s['influence']}
- Summary: {s['summary']}
""")
        return '\n'.join(formatted)

    def _format_intelligence_detailed(self, intelligence: List[Dict]) -> str:
        if not intelligence:
            return "No intelligence"

        formatted = []
        for i in intelligence:
            formatted.append(f"""
**{i['title']}** ({i['category']})
- Content: {i['content']}
- Impact: {i['impact']}
- Confidence: {i['confidence']}
""")
        return '\n'.join(formatted)

    def _format_decisions(self, decisions: List[Dict]) -> str:
        if not decisions:
            return "No recent decisions"
        return '\n'.join([f"• {d}" for d in decisions])

    def _format_actions(self, actions: List[Dict]) -> str:
        if not actions:
            return "No pending actions"
        return '\n'.join([f"• {a}" for a in actions])

    def _format_conversation_thread(self, thread: List[Dict]) -> str:
        if not thread:
            return "No conversation context"
        return '\n'.join([f"• {t}" for t in thread])

    def _format_json_export(self, strategic_context: Dict, session_context: Dict) -> str:
        """Format context as JSON export"""
        export_data = {
            'export_metadata': {
                'timestamp': datetime.now().isoformat(),
                'source': 'ClaudeDirector-Cursor',
                'format_version': '1.0'
            },
            'strategic_context': strategic_context,
            'session_context': session_context
        }
        return json.dumps(export_data, indent=2)

    def _format_yaml_export(self, strategic_context: Dict, session_context: Dict) -> str:
        """Format context as YAML export"""
        # Simplified YAML formatting for dependency-free implementation
        yaml_content = f"""# ClaudeDirector Context Export
export_metadata:
  timestamp: {datetime.now().isoformat()}
  source: ClaudeDirector-Cursor
  format_version: '1.0'

strategic_context:
  stakeholders: {len(strategic_context.get('stakeholders', []))} items
  intelligence: {len(strategic_context.get('intelligence', []))} items

session_context:
  session_type: {session_context.get('session_type', 'unknown')}
  quality_score: {session_context.get('quality_score', 0.0)}
  active_personas: {session_context.get('active_personas', [])}
"""
        return yaml_content


def main():
    """CLI interface for context bridge operations"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python cli_context_bridge.py <command> [options]")
        print("Commands:")
        print("  export-cli     - Create CLI-optimized context export")
        print("  export-full    - Create full context export")
        print("  import <file>  - Import context from file")
        return

    bridge = CLIContextBridge()
    command = sys.argv[1]

    if command == "export-cli":
        cli_export = bridge.create_cli_session_export()
        print(cli_export)

    elif command == "export-full":
        format_type = sys.argv[2] if len(sys.argv) > 2 else "markdown"
        output_file = sys.argv[3] if len(sys.argv) > 3 else None

        full_export = bridge.export_current_context(format_type, output_file)
        if output_file:
            print(f"✅ Context exported to {output_file}")
        else:
            print(full_export)

    elif command == "import" and len(sys.argv) > 2:
        file_path = sys.argv[2]
        success = bridge.import_context_from_file(file_path)
        if success:
            print("✅ Context imported successfully")
        else:
            print("❌ Context import failed")

    else:
        print("❌ Unknown command or missing arguments")


if __name__ == "__main__":
    main()
