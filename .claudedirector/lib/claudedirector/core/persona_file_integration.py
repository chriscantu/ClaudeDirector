"""
Persona File Integration for ClaudeDirector
Connects AI personas with controlled file generation in workspace
"""

from typing import Dict, Optional, List, Any

from .workspace_file_handler import WorkspaceFileHandler


class PersonaFileIntegration:
    """Integrates AI personas with workspace file lifecycle management"""

    def __init__(self, workspace_path: Optional[str] = None):
        self.file_handler = WorkspaceFileHandler(workspace_path)

        # Map personas to their preferred content types
        self.persona_content_preferences = {
            "alvaro": [
                "strategic_analysis",
                "executive_presentation",
                "quarterly_planning",
                "meeting_prep",
            ],
            "rachel": [
                "strategic_analysis",
                "methodology_documentation",
                "executive_presentation",
                "meeting_prep",
            ],
            "diego": [
                "strategic_analysis",
                "meeting_prep",
                "quarterly_planning",
                "session_summary",
            ],
            "camille": [
                "strategic_analysis",
                "framework_research",
                "methodology_documentation",
                "executive_presentation",
            ],
            "martin": [
                "strategic_analysis",
                "framework_research",
                "methodology_documentation",
                "session_summary",
            ],
            "marcus": [
                "strategic_analysis",
                "meeting_prep",
                "session_summary",
                "quarterly_planning",
            ],
            "david": [
                "strategic_analysis",
                "executive_presentation",
                "quarterly_planning",
                "meeting_prep",
            ],
        }

        # Content type templates for different scenarios
        self.content_templates = {
            "strategic_analysis": {
                "business_context": "Strategic analysis and recommendations",
                "filename_pattern": "strategic-analysis-{persona}-{timestamp}.md",
            },
            "meeting_prep": {
                "business_context": "Executive meeting preparation materials",
                "filename_pattern": "meeting-prep-{persona}-{timestamp}.md",
            },
            "executive_presentation": {
                "business_context": "Executive stakeholder presentation",
                "filename_pattern": "executive-presentation-{timestamp}.md",
            },
            "quarterly_planning": {
                "business_context": "Quarterly strategic planning",
                "filename_pattern": "q{quarter}-planning-{timestamp}.md",
            },
            "framework_research": {
                "business_context": "Strategic framework research and methodology",
                "filename_pattern": "framework-research-{timestamp}.md",
            },
            "methodology_documentation": {
                "business_context": "Strategic methodology documentation",
                "filename_pattern": "methodology-{timestamp}.md",
            },
            "session_summary": {
                "business_context": "Strategic session summary and action items",
                "filename_pattern": "session-summary-{timestamp}.md",
            },
        }

    def persona_generate_file(
        self,
        persona: str,
        content: str,
        content_type: str,
        business_context: Optional[str] = None,
        custom_filename: Optional[str] = None,
    ) -> Optional[str]:
        """Generate file through persona with lifecycle management"""

        # Check if persona typically creates this content type
        if not self._should_persona_create_content(persona, content_type):
            return None

        # Use template business context if not provided
        if not business_context:
            template = self.content_templates.get(content_type, {})
            business_context = template.get(
                "business_context", f"{persona} strategic analysis"
            )

        # Generate filename if not provided
        if not custom_filename:
            custom_filename = self._generate_persona_filename(persona, content_type)

        # Add persona context to content
        enhanced_content = self._add_persona_context(content, persona, content_type)

        # Request file creation through lifecycle manager
        created_file = self.file_handler.request_file_creation(
            content=enhanced_content,
            content_type=content_type,
            suggested_filename=custom_filename,
            business_context=business_context,
            persona=persona,
        )

        return created_file

    def _should_persona_create_content(self, persona: str, content_type: str) -> bool:
        """Check if persona should create this type of content"""
        preferred_types = self.persona_content_preferences.get(persona, [])
        return content_type in preferred_types

    def _generate_persona_filename(self, persona: str, content_type: str) -> str:
        """Generate appropriate filename for persona and content type"""
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d")
        quarter = (datetime.now().month - 1) // 3 + 1

        template = self.content_templates.get(content_type, {})
        pattern = template.get(
            "filename_pattern", "{persona}-{content_type}-{timestamp}.md"
        )

        filename = pattern.format(
            persona=persona,
            content_type=content_type.replace("_", "-"),
            timestamp=timestamp,
            quarter=quarter,
        )

        return filename

    def _add_persona_context(
        self, content: str, persona: str, content_type: str
    ) -> str:
        """Add persona context to content"""

        persona_headers = {
            "alvaro": "# 🎯 Strategic Business Analysis\n*Alvaro - Executive Strategy & ROI*\n\n",
            "rachel": "# 🎨 UX Strategy & Cross-Functional Alignment\n*Rachel - Design Strategy & Experience*\n\n",
            "diego": "# 🏗️ Engineering Leadership & Team Strategy\n*Diego - Platform Engineering & Team Management*\n\n",
            "camille": "# 💡 Strategic Technology & Transformation\n*Camille - Executive Technology Strategy*\n\n",
            "martin": "# 🔧 Platform Architecture & Technical Strategy\n*Martin - Technical Architecture & Systems*\n\n",
            "marcus": "# 📈 Platform Adoption & Change Management\n*Marcus - Internal Adoption & Marketing*\n\n",
            "david": "# 💰 Financial Planning & Investment Strategy\n*David - Budget & Resource Allocation*\n\n",
        }

        header = persona_headers.get(
            persona, f"# Strategic Analysis\n*{persona.title()}*\n\n"
        )

        return header + content

    def create_consolidated_session_summary(
        self, session_insights: Dict[str, Any], participating_personas: List[str]
    ) -> Optional[str]:
        """Create consolidated summary from multiple persona insights"""

        if not session_insights or not participating_personas:
            return None

        # Build comprehensive session summary
        summary_content = self._build_session_summary(
            session_insights, participating_personas
        )

        # Request creation of session summary
        created_file = self.file_handler.request_file_creation(
            content=summary_content,
            content_type="session_summary",
            suggested_filename="session-summary",
            business_context="Multi-persona strategic session summary",
            persona="collaborative",
        )

        return created_file

    def _build_session_summary(
        self, insights: Dict[str, Any], personas: List[str]
    ) -> str:
        """Build comprehensive session summary content"""
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        summary = f"""# Strategic Session Summary
*Generated: {timestamp}*
*Participating Personas: {', '.join(p.title() for p in personas)}*

---

## 🎯 Executive Summary

[Summary of key strategic insights and recommendations across all persona perspectives]

---

## 📋 Strategic Insights by Area

"""

        # Add persona-specific sections
        persona_sections = {
            "alvaro": "## 💼 Business Strategy & ROI (Alvaro)",
            "rachel": "## 🎨 UX Strategy & Design (Rachel)",
            "diego": "## 🏗️ Engineering Leadership (Diego)",
            "camille": "## 💡 Technology Strategy (Camille)",
            "martin": "## 🔧 Technical Architecture (Martin)",
            "marcus": "## 📈 Adoption Strategy (Marcus)",
            "david": "## 💰 Financial Strategy (David)",
        }

        for persona in personas:
            if persona in persona_sections:
                summary += f"\n{persona_sections[persona]}\n\n"
                persona_insights = insights.get(
                    persona, "No specific insights captured."
                )
                summary += f"{persona_insights}\n\n---\n"

        summary += """
## 🚀 Next Actions

[Strategic action items and follow-up recommendations]

## 📊 Key Metrics & Success Criteria

[Measurable outcomes and success indicators]

---

*This summary consolidates insights from multiple strategic AI personas for comprehensive leadership perspective.*
"""

        return summary

    def offer_session_consolidation(self) -> bool:
        """Offer to consolidate current session files"""
        print("\n💡 **Session Consolidation Available**")
        print(
            "Would you like to consolidate this session's insights into a comprehensive summary?"
        )

        response = input("Create session summary? [y/n]: ").strip().lower()
        return response == "y"

    def show_workspace_status(self):
        """Show current workspace and lifecycle status"""
        self.file_handler.show_lifecycle_status()

    def configure_file_preferences(self):
        """Configure file generation preferences"""
        self.file_handler.configure_lifecycle_settings()

    def initialize_workspace_for_personas(self):
        """Initialize workspace for persona-based file generation"""
        self.file_handler.initialize_workspace()

        print(f"\n🎯 **Persona File Integration Ready**")
        print(f"Workspace: {self.file_handler.workspace_path}")
        print(
            f"Generation Mode: {self.file_handler.lifecycle_manager.config.generation_mode.value}"
        )
        print(
            f"Auto-archive: {self.file_handler.lifecycle_manager.config.auto_archive_days} days"
        )

        # Show persona capabilities
        print(f"\n**🎭 Persona Content Capabilities:**")
        for persona, content_types in self.persona_content_preferences.items():
            print(f"  {persona.title()}: {', '.join(content_types)}")


# Utility functions for persona integration
def get_content_type_for_request(request_context: str) -> str:
    """Determine appropriate content type based on request context"""

    context_keywords = {
        "meeting": "meeting_prep",
        "presentation": "executive_presentation",
        "quarterly": "quarterly_planning",
        "q1": "quarterly_planning",
        "q2": "quarterly_planning",
        "q3": "quarterly_planning",
        "q4": "quarterly_planning",
        "framework": "framework_research",
        "methodology": "methodology_documentation",
        "summary": "session_summary",
        "analysis": "strategic_analysis",
    }

    request_lower = request_context.lower()

    for keyword, content_type in context_keywords.items():
        if keyword in request_lower:
            return content_type

    # Default to strategic analysis
    return "strategic_analysis"


def extract_business_context(request: str) -> str:
    """Extract business context from user request"""

    # Look for business context indicators
    business_indicators = [
        "platform",
        "engineering",
        "team",
        "strategy",
        "roi",
        "budget",
        "stakeholder",
        "executive",
        "leadership",
    ]

    request_words = request.lower().split()
    relevant_context = []

    for word in request_words:
        if word in business_indicators:
            relevant_context.append(word)

    if relevant_context:
        return f"Strategic analysis related to: {', '.join(relevant_context)}"
    else:
        return "Strategic engineering leadership analysis"
