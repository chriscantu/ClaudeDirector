"""
ClaudeDirector Chat Enhancement Detector

Provides organic, context-aware suggestions for CLI enhancements
without disrupting the chat-first experience.

Design Principles:
- Chat-first: Always functional without CLI
- Organic: Suggests enhancements based on natural conversation cues
- Optional: Never requires CLI setup
- Graceful: Smooth degradation when CLI unavailable
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class EnhancementType(Enum):
    """Types of CLI enhancements that could be beneficial"""

    TEMPLATE_DISCOVERY = "template_discovery"
    WORKSPACE_ANALYSIS = "workspace_analysis"
    STAKEHOLDER_INTELLIGENCE = "stakeholder_intelligence"

    AUTOMATED_REPORTING = "automated_reporting"


@dataclass
class EnhancementSuggestion:
    """Represents a contextual enhancement suggestion"""

    enhancement_type: EnhancementType
    confidence: float  # 0.0 to 1.0
    trigger_context: str
    user_benefit: str
    setup_effort: str  # "30 seconds", "2 minutes", etc.
    organic_prompt: str


class ChatEnhancementDetector:
    """
    Detects conversation contexts where CLI enhancements would be valuable
    and provides organic, non-intrusive suggestions.
    """

    def __init__(self):
        self.conversation_history: List[str] = []
        self.detected_context: Dict[str, int] = {}
        self.suggestion_cooldown: Dict[EnhancementType, int] = {}

    def analyze_message(self, message: str) -> Optional[EnhancementSuggestion]:
        """
        Analyze a chat message for enhancement opportunities.

        Returns suggestion only when high confidence + appropriate context.
        """
        self.conversation_history.append(message.lower())

        # Keep only last 10 messages for context
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)

        # Track conversation context
        self._update_context_tracking(message.lower())

        # Check for enhancement opportunities
        return self._evaluate_enhancement_suggestions()

    def _update_context_tracking(self, message: str):
        """Update context tracking based on message content"""

        # Template discovery context
        template_keywords = [
            "director template",
            "engineering director for",
            "mobile director",
            "backend director",
            "platform director",
            "data director",
            "different type of director",
            "customize director",
        ]
        if any(keyword in message for keyword in template_keywords):
            self.detected_context["template_discovery"] = (
                self.detected_context.get("template_discovery", 0) + 1
            )

        # Workspace analysis context
        workspace_keywords = [
            "analyze my project",
            "review my codebase",
            "assess my architecture",
            "stakeholder map",
            "team structure",
            "current initiatives",
        ]
        if any(keyword in message for keyword in workspace_keywords):
            self.detected_context["workspace_analysis"] = (
                self.detected_context.get("workspace_analysis", 0) + 1
            )

        # Metrics/reporting context
        metrics_keywords = [
            "quarterly report",
            "kpi tracking",
            "progress report",
            "status update",
            "executive summary",
        ]
        if any(keyword in message for keyword in metrics_keywords):
            self.detected_context["metrics_reporting"] = (
                self.detected_context.get("metrics_reporting", 0) + 1
            )

    def _evaluate_enhancement_suggestions(self) -> Optional[EnhancementSuggestion]:
        """Evaluate if an enhancement suggestion should be made"""

        # Template discovery suggestion
        if (
            self.detected_context.get("template_discovery", 0) >= 2
            and EnhancementType.TEMPLATE_DISCOVERY not in self.suggestion_cooldown
        ):

            return EnhancementSuggestion(
                enhancement_type=EnhancementType.TEMPLATE_DISCOVERY,
                confidence=0.85,
                trigger_context="Multiple template/director customization requests",
                user_benefit="Discover optimized director templates for your specific domain (mobile, data, backend, etc.)",
                setup_effort="30 seconds",
                organic_prompt=(
                    "💡 **Tip**: Since you're exploring different director types, "
                    "you might find the template discovery helpful. It can suggest "
                    "optimized director configurations for your specific domain.\n\n"
                    'Try: `./claudedirector templates discover "your domain"`\n'
                    "*(Optional - your chat experience works perfectly without this)*"
                ),
            )

        # Workspace analysis suggestion
        if (
            self.detected_context.get("workspace_analysis", 0) >= 2
            and EnhancementType.WORKSPACE_ANALYSIS not in self.suggestion_cooldown
        ):

            return EnhancementSuggestion(
                enhancement_type=EnhancementType.WORKSPACE_ANALYSIS,
                confidence=0.80,
                trigger_context="Multiple workspace/project analysis requests",
                user_benefit="Automated analysis of your workspace structure, stakeholder relationships, and strategic initiatives",
                setup_effort="1 minute",
                organic_prompt=(
                    "💡 **Enhancement available**: I notice you're analyzing workspace elements. "
                    "The ClaudeDirector workspace analyzer can automatically map your "
                    "stakeholder relationships and current initiatives.\n\n"
                    "Try: `./claudedirector workspace status`\n"
                    "*(This is optional - I can continue helping through chat)*"
                ),
            )

        return None

    def mark_suggestion_shown(self, enhancement_type: EnhancementType):
        """Mark that a suggestion was shown to avoid spam"""
        self.suggestion_cooldown[enhancement_type] = len(self.conversation_history)

    def should_show_setup_nudge(self) -> bool:
        """
        Determine if a gentle setup nudge is appropriate.
        Only after extended productive conversation.
        """
        return (
            len(self.conversation_history) > 8
            and len(self.detected_context) >= 2
            and "setup_nudge_shown" not in self.suggestion_cooldown
        )

    def generate_setup_nudge(self) -> str:
        """Generate a gentle, optional setup nudge"""
        return (
            "🚀 **You're getting great value from ClaudeDirector!** "
            "If you'd like even more capabilities (workspace analysis, automated reporting, "
            "stakeholder intelligence), there's an optional 2-minute setup that unlocks "
            "advanced features.\n\n"
            "But no pressure - everything we're doing works perfectly in chat! 😊\n\n"
            'Interested? Just ask: *"How do I set up the advanced features?"*'
        )


# Global instance for use across the framework
chat_enhancer = ChatEnhancementDetector()


def analyze_for_enhancements(message: str) -> Optional[str]:
    """
    Convenience function to analyze messages and return enhancement prompts.

    Returns organic enhancement suggestion if appropriate, None otherwise.
    """
    suggestion = chat_enhancer.analyze_message(message)

    if suggestion and suggestion.confidence > 0.75:
        chat_enhancer.mark_suggestion_shown(suggestion.enhancement_type)
        return suggestion.organic_prompt

    # Check for setup nudge opportunity
    if chat_enhancer.should_show_setup_nudge():
        chat_enhancer.mark_suggestion_shown("setup_nudge_shown")
        return chat_enhancer.generate_setup_nudge()

    return None
