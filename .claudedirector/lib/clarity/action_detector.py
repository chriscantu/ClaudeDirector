"""
Action Detection Engine for Next Action Clarity Framework

Identifies specific next steps and actionable outcomes in strategic conversations.
"""

import re
from typing import List, Dict, Optional, Tuple
from .models import ActionItem, ActionType


class ActionDetectionEngine:
    """Identifies specific next steps and actionable outcomes"""

    def __init__(self):
        self.action_patterns = self._initialize_action_patterns()
        self.specificity_indicators = self._initialize_specificity_indicators()
        self.timeline_patterns = self._initialize_timeline_patterns()

    def _initialize_action_patterns(self) -> Dict[ActionType, List[str]]:
        """Initialize regex patterns for different action types"""
        return {
            ActionType.DECISION: [
                r"I(?:'ve| have)?\s+decided\s+to\s+(.+)",
                r"(?:My|The)\s+decision\s+is\s+to\s+(.+)",
                r"I(?:'m| am)\s+going\s+to\s+(.+)",
                r"I\s+will\s+(.+)",
                r"We(?:'ll| will)\s+(?:go with|choose|select)\s+(.+)",
                r"The\s+right\s+approach\s+is\s+(.+)",
            ],
            ActionType.TASK_ASSIGNMENT: [
                r"I(?:'ll| will)\s+assign\s+(.+)\s+to\s+(.+)",
                r"(.+)\s+(?:will|should)\s+(?:handle|take care of|work on)\s+(.+)",
                r"I(?:'ll| will)\s+have\s+(.+)\s+(?:do|work on|handle)\s+(.+)",
                r"(?:Let's|We'll)\s+have\s+(.+)\s+(?:lead|own|drive)\s+(.+)",
            ],
            ActionType.MEETING_SCHEDULING: [
                r"I(?:'ll| will)\s+schedule\s+(?:a\s+)?(?:meeting|call|session)\s+(?:with\s+)?(.+)",
                r"(?:Let's|We'll)\s+meet\s+(?:with\s+)?(.+)\s+(?:on|by|this|next)\s+(.+)",
                r"I(?:'ll| will)\s+set\s+up\s+(?:a\s+)?(?:meeting|call|session)\s+(.+)",
                r"We\s+need\s+to\s+(?:meet|talk)\s+(?:with\s+)?(.+)",
            ],
            ActionType.RESOURCE_ALLOCATION: [
                r"I(?:'ll| will)\s+allocate\s+(.+)\s+(?:to|for)\s+(.+)",
                r"We(?:'ll| will)\s+invest\s+(.+)\s+(?:in|into)\s+(.+)",
                r"I(?:'m| am)\s+(?:budgeting|planning)\s+(.+)\s+for\s+(.+)",
                r"(?:Let's|We'll)\s+dedicate\s+(.+)\s+to\s+(.+)",
            ],
            ActionType.STAKEHOLDER_ENGAGEMENT: [
                r"I(?:'ll| will)\s+(?:talk to|reach out to|contact|engage)\s+(.+)",
                r"I\s+need\s+to\s+(?:align with|get buy-in from|discuss with)\s+(.+)",
                r"(?:Let's|We'll)\s+bring\s+(.+)\s+into\s+(?:the conversation|this discussion)",
                r"I(?:'ll| will)\s+(?:update|inform|brief)\s+(.+)\s+(?:on|about)\s+(.+)",
            ],
            ActionType.ANALYSIS_REQUEST: [
                r"I(?:'ll| will)\s+(?:analyze|research|investigate|look into)\s+(.+)",
                r"We\s+need\s+to\s+(?:analyze|research|investigate|study)\s+(.+)",
                r"(?:Let's|I'll)\s+(?:dig deeper into|examine|review)\s+(.+)",
                r"I(?:'ll| will)\s+gather\s+(?:data|information|insights)\s+(?:on|about)\s+(.+)",
            ],
            ActionType.PROCESS_CHANGE: [
                r"I(?:'ll| will)\s+(?:implement|establish|create|set up)\s+(?:a\s+)?(?:new\s+)?(.+)\s+process",
                r"We(?:'ll| will)\s+change\s+(?:how we|the way we)\s+(.+)",
                r"(?:Let's|I'll)\s+(?:revise|update|modify)\s+(?:our|the)\s+(.+)\s+process",
                r"I(?:'m| am)\s+going\s+to\s+(?:streamline|optimize|improve)\s+(.+)",
            ],
            ActionType.INVESTMENT_DECISION: [
                r"I(?:'ve| have)\s+decided\s+to\s+(?:invest in|fund|budget for)\s+(.+)",
                r"We(?:'ll| will)\s+(?:invest|spend|allocate)\s+(.+)\s+(?:on|for|in)\s+(.+)",
                r"I(?:'m| am)\s+(?:approving|authorizing)\s+(.+)\s+for\s+(.+)",
                r"(?:Let's|We'll)\s+(?:fund|budget|invest in)\s+(.+)",
            ],
            ActionType.COMMUNICATION: [
                r"I(?:'ll| will)\s+(?:communicate|announce|share|present)\s+(.+)",
                r"(?:Let's|I'll)\s+(?:send|draft|write)\s+(?:a\s+)?(?:message|email|update)\s+(?:to\s+)?(.+)",
                r"I(?:'ll| will)\s+(?:present|share)\s+(?:this|these findings)\s+(?:with|to)\s+(.+)",
                r"We\s+need\s+to\s+(?:communicate|inform|update)\s+(.+)\s+(?:about|on)\s+(.+)",
            ],
            ActionType.TIMELINE_COMMITMENT: [
                r"I(?:'ll| will)\s+(?:do this|complete this|finish this)\s+by\s+(.+)",
                r"(?:This|That)\s+(?:will be|should be)\s+(?:done|completed|finished)\s+by\s+(.+)",
                r"I(?:'m| am)\s+targeting\s+(.+)\s+for\s+completion",
                r"(?:Let's|We'll)\s+aim\s+for\s+(.+)\s+(?:as|by)\s+(?:the\s+)?(?:deadline|target)",
            ],
        }

    def _initialize_specificity_indicators(self) -> Dict[str, float]:
        """Initialize patterns that indicate action specificity"""
        return {
            # High specificity (0.8-1.0)
            r"by\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)": 0.9,
            r"by\s+\d{1,2}/\d{1,2}": 0.95,
            r"by\s+(?:end of|EOD|close of business)": 0.8,
            r"within\s+\d+\s+(?:days|weeks|hours)": 0.85,
            r"(?:exactly|specifically|precisely)\s+": 0.9,
            # Medium specificity (0.5-0.7)
            r"(?:this|next)\s+(?:week|month|quarter)": 0.6,
            r"(?:soon|shortly|quickly)": 0.4,
            r"(?:as soon as possible|ASAP)": 0.5,
            r"in\s+the\s+(?:near\s+)?(?:future|term)": 0.3,
            # Names and specific entities (0.7-0.9)
            r"[A-Z][a-z]+\s+[A-Z][a-z]+": 0.8,  # Person names
            r"@[a-zA-Z0-9_]+": 0.85,  # Mentions
            r"\$[\d,]+": 0.9,  # Specific dollar amounts
            r"\d+%": 0.8,  # Percentages
            # Vague indicators (0.1-0.3)
            r"(?:maybe|perhaps|possibly|potentially)": 0.2,
            r"(?:should|could|might|may)": 0.3,
            r"(?:probably|likely)": 0.4,
            r"(?:eventually|someday|sometime)": 0.1,
        }

    def _initialize_timeline_patterns(self) -> List[Tuple[str, str]]:
        """Initialize patterns for extracting timelines"""
        return [
            (r"by\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)", r"\1"),
            (r"by\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)", r"\1"),
            (r"by\s+(end of|EOD|close of business)", r"\1"),
            (r"within\s+(\d+\s+(?:days|weeks|hours|months))", r"\1"),
            (r"(?:this|next)\s+(week|month|quarter)", r"this \1"),
            (r"by\s+(Q[1-4])", r"\1"),
            (r"in\s+(\d+\s+(?:days|weeks|months))", r"\1"),
        ]

    def extract_action_items(self, text: str) -> List[ActionItem]:
        """Extract actionable items from text"""
        actions = []

        for action_type, patterns in self.action_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    action_text = match.group(0)
                    specificity = self._calculate_specificity(action_text)
                    timeline = self._extract_timeline(action_text)
                    responsible_party = self._extract_responsible_party(
                        action_text, action_type
                    )

                    action = ActionItem(
                        text=action_text.strip(),
                        action_type=action_type,
                        specificity_score=specificity,
                        timeline=timeline,
                        responsible_party=responsible_party,
                        confidence=self._calculate_confidence(action_text, action_type),
                    )
                    actions.append(action)

        return self._deduplicate_actions(actions)

    def _calculate_specificity(self, text: str) -> float:
        """Calculate how specific an action is (0.0 to 1.0)"""
        base_score = 0.5

        for pattern, score_modifier in self.specificity_indicators.items():
            if re.search(pattern, text, re.IGNORECASE):
                if score_modifier > 0.5:  # Positive indicators
                    base_score = min(1.0, base_score + (score_modifier - 0.5))
                else:  # Negative indicators
                    base_score = max(0.0, base_score - (0.5 - score_modifier))

        # Bonus for length and detail
        word_count = len(text.split())
        if word_count > 10:
            base_score = min(1.0, base_score + 0.1)
        elif word_count < 5:
            base_score = max(0.0, base_score - 0.1)

        return round(base_score, 2)

    def _extract_timeline(self, text: str) -> Optional[str]:
        """Extract timeline information from action text"""
        for pattern, replacement in self.timeline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_responsible_party(
        self, text: str, action_type: ActionType
    ) -> Optional[str]:
        """Extract who is responsible for the action"""
        # Look for person names (simple heuristic)
        name_pattern = r"([A-Z][a-z]+\s+[A-Z][a-z]+)"
        name_match = re.search(name_pattern, text)
        if name_match:
            return name_match.group(1)

        # Look for mentions
        mention_pattern = r"@([a-zA-Z0-9_]+)"
        mention_match = re.search(mention_pattern, text)
        if mention_match:
            return f"@{mention_match.group(1)}"

        # Default based on action type and pronouns
        if re.search(r"\bI(?:'ll| will| am)\b", text, re.IGNORECASE):
            return "user"
        elif re.search(r"\b(?:we|us|our team)\b", text, re.IGNORECASE):
            return "team"

        return None

    def _calculate_confidence(self, text: str, action_type: ActionType) -> float:
        """Calculate confidence in action detection"""
        confidence = 0.7  # Base confidence

        # Boost confidence for strong action verbs
        strong_verbs = ["will", "going to", "decided", "commit", "plan"]
        for verb in strong_verbs:
            if verb in text.lower():
                confidence = min(1.0, confidence + 0.1)

        # Reduce confidence for weak language
        weak_language = ["maybe", "might", "could", "should", "perhaps"]
        for weak in weak_language:
            if weak in text.lower():
                confidence = max(0.0, confidence - 0.2)

        return round(confidence, 2)

    def _deduplicate_actions(self, actions: List[ActionItem]) -> List[ActionItem]:
        """Remove duplicate or very similar actions"""
        if not actions:
            return actions

        unique_actions = []
        seen_texts = set()

        for action in sorted(actions, key=lambda x: x.confidence, reverse=True):
            # Simple deduplication based on text similarity
            is_duplicate = False
            action_words = set(action.text.lower().split())

            for seen_text in seen_texts:
                seen_words = set(seen_text.lower().split())
                overlap = len(action_words & seen_words) / len(
                    action_words | seen_words
                )
                if overlap > 0.7:  # 70% similarity threshold
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_actions.append(action)
                seen_texts.add(action.text)

        return unique_actions

    def classify_action_type(self, action_text: str) -> ActionType:
        """Classify the type of an action"""
        text_lower = action_text.lower()

        # Decision keywords
        if any(
            word in text_lower
            for word in ["decide", "decision", "choose", "select", "go with"]
        ):
            return ActionType.DECISION

        # Meeting keywords
        if any(word in text_lower for word in ["meeting", "call", "schedule", "meet"]):
            return ActionType.MEETING_SCHEDULING

        # Resource keywords
        if any(
            word in text_lower
            for word in ["allocate", "budget", "invest", "fund", "resource"]
        ):
            return ActionType.RESOURCE_ALLOCATION

        # Communication keywords
        if any(
            word in text_lower
            for word in ["communicate", "announce", "present", "share", "email"]
        ):
            return ActionType.COMMUNICATION

        # Default to task assignment
        return ActionType.TASK_ASSIGNMENT

    def measure_action_specificity(self, action_text: str) -> float:
        """Measure how specific an action is"""
        return self._calculate_specificity(action_text)

    def validate_action_completeness(self, action_text: str) -> bool:
        """Validate if an action is complete and actionable"""
        # Must have an action verb
        action_verbs = [
            "will",
            "going",
            "plan",
            "decide",
            "schedule",
            "allocate",
            "communicate",
        ]
        has_action_verb = any(verb in action_text.lower() for verb in action_verbs)

        # Must be reasonably specific
        specificity = self._calculate_specificity(action_text)

        # Must not be too vague
        vague_indicators = [
            "maybe",
            "perhaps",
            "might",
            "could",
            "should",
            "eventually",
        ]
        is_vague = any(
            indicator in action_text.lower() for indicator in vague_indicators
        )

        return has_action_verb and specificity >= 0.4 and not is_vague
