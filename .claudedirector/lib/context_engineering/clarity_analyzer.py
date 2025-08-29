"""
Clarity Analyzer - Phase 10 Consolidation

Unified clarity analysis engine consolidating:
- clarity/action_detector.py (316 lines)
- clarity/clarity_metrics.py (509 lines)
- clarity/conversation_analyzer.py (437 lines)
- clarity/models.py (225 lines)

Total: 1,487 lines consolidated into enterprise-grade unified module
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import re
import statistics
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from enum import Enum


# === DATA MODELS (from clarity/models.py) ===


class ActionType(Enum):
    """Types of actions that can be identified in strategic conversations"""

    DECISION = "decision"
    TASK_ASSIGNMENT = "task_assignment"
    MEETING_SCHEDULING = "meeting_scheduling"
    RESOURCE_ALLOCATION = "resource_allocation"
    STAKEHOLDER_ENGAGEMENT = "stakeholder_engagement"
    ANALYSIS_REQUEST = "analysis_request"
    PROCESS_CHANGE = "process_change"
    INVESTMENT_DECISION = "investment_decision"
    COMMUNICATION = "communication"
    TIMELINE_COMMITMENT = "timeline_commitment"


@dataclass
class ActionItem:
    """Represents a specific actionable item identified in conversation"""

    text: str
    action_type: ActionType
    specificity_score: float  # 0.0 to 1.0, higher = more specific
    timeline: Optional[str] = None
    responsible_party: Optional[str] = None
    dependencies: List[str] = None
    confidence: float = 0.0  # AI confidence in action detection

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class ClarityIndicator:
    """Indicators that suggest conversation clarity or lack thereof"""

    type: str  # "positive", "negative", "neutral"
    text: str
    confidence: float
    pattern: str  # The pattern that matched this indicator


@dataclass
class ClarityMetrics:
    """Comprehensive clarity metrics for a conversation"""

    overall_score: float  # 0.0 to 1.0
    action_clarity_score: float
    decision_clarity_score: float
    context_clarity_score: float

    # Component metrics
    action_items_count: int
    clear_actions_count: int
    vague_statements_count: int
    decision_points_count: int
    ambiguous_references_count: int

    # Quality indicators
    specificity_scores: List[float]
    confidence_scores: List[float]
    clarity_indicators: List[ClarityIndicator]

    def __post_init__(self):
        if self.specificity_scores is None:
            self.specificity_scores = []
        if self.confidence_scores is None:
            self.confidence_scores = []
        if self.clarity_indicators is None:
            self.clarity_indicators = []


@dataclass
class ConversationAnalysis:
    """Complete analysis of a strategic conversation"""

    # Basic metrics
    word_count: int
    sentence_count: int
    paragraph_count: int

    # Clarity analysis
    clarity_metrics: ClarityMetrics
    action_items: List[ActionItem]

    # Strategic content
    key_decisions: List[str]
    stakeholder_mentions: List[str]
    strategic_themes: List[str]

    # Quality measures
    coherence_score: float
    completeness_score: float
    actionability_score: float


# === ACTION DETECTION ENGINE (from clarity/action_detector.py) ===


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
                    responsible_party = self._extract_responsible_party(action_text, action_type)

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

    def _extract_responsible_party(self, text: str, action_type: ActionType) -> Optional[str]:
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
                overlap = len(action_words & seen_words) / len(action_words | seen_words)
                if overlap > 0.7:  # 70% similarity threshold
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_actions.append(action)
                seen_texts.add(action.text)

        return unique_actions


# === CLARITY METRICS ENGINE (from clarity/clarity_metrics.py) ===


class ClarityMetricsEngine:
    """Calculates comprehensive clarity metrics for strategic conversations"""

    def __init__(self):
        self.clarity_indicators = self._initialize_clarity_indicators()
        self.vague_patterns = self._initialize_vague_patterns()
        self.decision_patterns = self._initialize_decision_patterns()

    def _initialize_clarity_indicators(self) -> Dict[str, Dict[str, float]]:
        """Initialize patterns that indicate clarity"""
        return {
            "positive": {
                r"specifically": 0.8,
                r"exactly": 0.9,
                r"clearly": 0.7,
                r"precisely": 0.8,
                r"I will": 0.7,
                r"we will": 0.7,
                r"the plan is": 0.8,
                r"decided to": 0.9,
                r"going to": 0.7,
                r"by \w+day": 0.8,
                r"by \d+/\d+": 0.9,
            },
            "negative": {
                r"maybe": 0.8,
                r"perhaps": 0.7,
                r"might": 0.6,
                r"could": 0.5,
                r"should probably": 0.7,
                r"not sure": 0.9,
                r"unclear": 0.8,
                r"ambiguous": 0.9,
                r"vague": 0.8,
                r"somehow": 0.6,
                r"kind of": 0.5,
                r"sort of": 0.5,
            },
        }

    def _initialize_vague_patterns(self) -> List[str]:
        """Initialize patterns that indicate vagueness"""
        return [
            r"(?:maybe|perhaps|possibly)\s+we\s+(?:should|could|might)",
            r"(?:I think|I believe|I guess)\s+(?:maybe|perhaps)",
            r"(?:something|someone)\s+(?:should|could|might)",
            r"(?:at some point|eventually|someday)",
            r"(?:kind of|sort of|pretty much)",
            r"(?:not really sure|not entirely clear)",
            r"(?:probably|likely)\s+(?:should|could|might)",
        ]

    def _initialize_decision_patterns(self) -> List[str]:
        """Initialize patterns that indicate clear decisions"""
        return [
            r"(?:I|we)\s+(?:have\s+)?decided\s+to",
            r"(?:I|we)\s+will\s+(?:definitely|certainly)",
            r"(?:I|we)\s+are\s+going\s+to",
            r"the\s+decision\s+is\s+to",
            r"(?:I|we)\s+commit\s+to",
            r"(?:I|we)\s+plan\s+to",
        ]

    def calculate_clarity_metrics(
        self, text: str, action_items: List[ActionItem]
    ) -> ClarityMetrics:
        """Calculate comprehensive clarity metrics"""

        # Basic counts
        sentences = self._split_sentences(text)
        words = text.split()

        # Calculate component scores
        action_clarity = self._calculate_action_clarity(action_items)
        decision_clarity = self._calculate_decision_clarity(text)
        context_clarity = self._calculate_context_clarity(text)

        # Calculate overall score
        overall_score = (action_clarity + decision_clarity + context_clarity) / 3

        # Count specific elements
        clear_actions = sum(1 for action in action_items if action.specificity_score >= 0.6)
        vague_statements = self._count_vague_statements(text)
        decision_points = self._count_decision_points(text)
        ambiguous_refs = self._count_ambiguous_references(text)

        # Generate clarity indicators
        indicators = self._generate_clarity_indicators(text)

        # Collect scores
        specificity_scores = [action.specificity_score for action in action_items]
        confidence_scores = [action.confidence for action in action_items]

        return ClarityMetrics(
            overall_score=round(overall_score, 2),
            action_clarity_score=round(action_clarity, 2),
            decision_clarity_score=round(decision_clarity, 2),
            context_clarity_score=round(context_clarity, 2),
            action_items_count=len(action_items),
            clear_actions_count=clear_actions,
            vague_statements_count=vague_statements,
            decision_points_count=decision_points,
            ambiguous_references_count=ambiguous_refs,
            specificity_scores=specificity_scores,
            confidence_scores=confidence_scores,
            clarity_indicators=indicators,
        )

    def _calculate_action_clarity(self, action_items: List[ActionItem]) -> float:
        """Calculate clarity of action items"""
        if not action_items:
            return 0.3  # Low score for no actions

        # Average specificity of actions
        avg_specificity = statistics.mean([action.specificity_score for action in action_items])

        # Bonus for having multiple actions
        action_bonus = min(0.2, len(action_items) * 0.05)

        # Penalty for very low confidence actions
        low_confidence_penalty = sum(1 for action in action_items if action.confidence < 0.5) * 0.1

        score = avg_specificity + action_bonus - low_confidence_penalty
        return max(0.0, min(1.0, score))

    def _calculate_decision_clarity(self, text: str) -> float:
        """Calculate clarity of decisions made"""
        decision_count = self._count_decision_points(text)

        if decision_count == 0:
            return 0.4  # Neutral score for no decisions

        # Score based on decision patterns
        score = 0.6  # Base score for having decisions

        # Check for clear decision language
        for pattern in self.decision_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.1

        # Penalty for vague decision language
        vague_decision_patterns = [
            r"(?:maybe|perhaps)\s+(?:decide|choose)",
            r"not\s+sure\s+(?:what|which)",
        ]
        for pattern in vague_decision_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score -= 0.2

        return max(0.0, min(1.0, score))

    def _calculate_context_clarity(self, text: str) -> float:
        """Calculate clarity of context and background"""
        words = text.split()
        word_count = len(words)

        # Base score adjusted for content length
        if word_count < 50:
            base_score = 0.3  # Too brief
        elif word_count > 500:
            base_score = 0.6  # Might be too verbose
        else:
            base_score = 0.7  # Good length

        # Check for context indicators
        context_indicators = [
            r"(?:because|since|given that|due to)",
            r"(?:background|context|situation)",
            r"(?:currently|right now|at present)",
            r"(?:previously|before|earlier)",
        ]

        for pattern in context_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                base_score += 0.05

        # Penalty for ambiguous references
        ambiguous_refs = self._count_ambiguous_references(text)
        ambiguous_penalty = ambiguous_refs * 0.05

        score = base_score - ambiguous_penalty
        return max(0.0, min(1.0, score))

    def _count_vague_statements(self, text: str) -> int:
        """Count vague statements in text"""
        count = 0
        for pattern in self.vague_patterns:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count

    def _count_decision_points(self, text: str) -> int:
        """Count clear decision points in text"""
        count = 0
        for pattern in self.decision_patterns:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count

    def _count_ambiguous_references(self, text: str) -> int:
        """Count ambiguous references like 'this', 'that', 'it'"""
        ambiguous_patterns = [
            r"\bthis\b(?!\s+\w+)",  # "this" not followed by a noun
            r"\bthat\b(?!\s+\w+)",  # "that" not followed by a noun
            r"\bit\b(?!\s+(?:is|was|will))",  # "it" in certain contexts
            r"\bthey\b(?!\s+(?:are|were|will))",  # "they" without clear antecedent
        ]

        count = 0
        for pattern in ambiguous_patterns:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count

    def _generate_clarity_indicators(self, text: str) -> List[ClarityIndicator]:
        """Generate specific clarity indicators found in text"""
        indicators = []

        for indicator_type, patterns in self.clarity_indicators.items():
            for pattern, confidence in patterns.items():
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    indicator = ClarityIndicator(
                        type=indicator_type,
                        text=match.group(0),
                        confidence=confidence,
                        pattern=pattern,
                    )
                    indicators.append(indicator)

        return indicators

    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting"""
        return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]


# === CONVERSATION ANALYZER (from clarity/conversation_analyzer.py) ===


class ConversationAnalyzer:
    """Comprehensive conversation analysis combining all clarity components"""

    def __init__(self):
        self.action_detector = ActionDetectionEngine()
        self.metrics_engine = ClarityMetricsEngine()

    def analyze_conversation(self, text: str) -> ConversationAnalysis:
        """Perform complete conversation analysis"""

        # Basic text metrics
        words = text.split()
        sentences = self._split_sentences(text)
        paragraphs = self._split_paragraphs(text)

        # Extract action items
        action_items = self.action_detector.extract_action_items(text)

        # Calculate clarity metrics
        clarity_metrics = self.metrics_engine.calculate_clarity_metrics(text, action_items)

        # Extract strategic content
        key_decisions = self._extract_key_decisions(text)
        stakeholder_mentions = self._extract_stakeholder_mentions(text)
        strategic_themes = self._extract_strategic_themes(text)

        # Calculate quality scores
        coherence_score = self._calculate_coherence(text, sentences)
        completeness_score = self._calculate_completeness(text, action_items)
        actionability_score = self._calculate_actionability(action_items)

        return ConversationAnalysis(
            word_count=len(words),
            sentence_count=len(sentences),
            paragraph_count=len(paragraphs),
            clarity_metrics=clarity_metrics,
            action_items=action_items,
            key_decisions=key_decisions,
            stakeholder_mentions=stakeholder_mentions,
            strategic_themes=strategic_themes,
            coherence_score=round(coherence_score, 2),
            completeness_score=round(completeness_score, 2),
            actionability_score=round(actionability_score, 2),
        )

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    def _extract_key_decisions(self, text: str) -> List[str]:
        """Extract key decisions mentioned in the conversation"""
        decision_patterns = [
            r"(?:I|we)\s+(?:have\s+)?decided\s+to\s+([^.!?]+)",
            r"(?:my|our)\s+decision\s+is\s+to\s+([^.!?]+)",
            r"(?:I|we)\s+will\s+(?:definitely|certainly)\s+([^.!?]+)",
        ]

        decisions = []
        for pattern in decision_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                decisions.append(match.group(1).strip())

        return decisions

    def _extract_stakeholder_mentions(self, text: str) -> List[str]:
        """Extract stakeholder mentions"""
        # Person names pattern
        name_pattern = r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"
        names = re.findall(name_pattern, text)

        # Role mentions
        role_patterns = [
            r"\b(?:CEO|CTO|VP|director|manager|lead|team)\b",
            r"\b(?:engineering|product|design|marketing)\s+(?:team|lead|manager)\b",
        ]

        roles = []
        for pattern in role_patterns:
            roles.extend(re.findall(pattern, text, re.IGNORECASE))

        return list(set(names + roles))

    def _extract_strategic_themes(self, text: str) -> List[str]:
        """Extract strategic themes from conversation"""
        theme_patterns = {
            "platform strategy": r"\b(?:platform|architecture|technical)\s+(?:strategy|approach|direction)\b",
            "organizational": r"\b(?:organizational|team|structure|hierarchy)\b",
            "investment": r"\b(?:investment|budget|funding|resource)\b",
            "performance": r"\b(?:performance|metrics|measurement|tracking)\b",
            "stakeholder": r"\b(?:stakeholder|alignment|communication|engagement)\b",
            "decision making": r"\b(?:decision|choice|selection|direction)\b",
        }

        themes = []
        for theme, pattern in theme_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                themes.append(theme)

        return themes

    def _calculate_coherence(self, text: str, sentences: List[str]) -> float:
        """Calculate coherence of the conversation"""
        if len(sentences) < 2:
            return 0.5

        # Simple coherence based on connecting words and consistent topics
        connecting_words = [
            "therefore",
            "however",
            "moreover",
            "furthermore",
            "additionally",
            "consequently",
            "meanwhile",
            "similarly",
            "in contrast",
            "on the other hand",
        ]

        coherence_score = 0.6  # Base score

        # Check for connecting words
        for word in connecting_words:
            if word.lower() in text.lower():
                coherence_score += 0.05

        # Penalty for very short or very long sentences
        avg_sentence_length = len(text.split()) / len(sentences)
        if 10 <= avg_sentence_length <= 25:
            coherence_score += 0.1
        else:
            coherence_score -= 0.05

        return max(0.0, min(1.0, coherence_score))

    def _calculate_completeness(self, text: str, action_items: List[ActionItem]) -> float:
        """Calculate completeness of the conversation"""
        completeness_score = 0.5  # Base score

        # Has clear context
        if re.search(r"\b(?:background|context|situation|currently)\b", text, re.IGNORECASE):
            completeness_score += 0.15

        # Has decisions
        if re.search(r"\b(?:decided|decision|will|going to)\b", text, re.IGNORECASE):
            completeness_score += 0.15

        # Has action items
        if action_items:
            completeness_score += 0.1
            # Bonus for specific actions
            specific_actions = sum(1 for action in action_items if action.specificity_score >= 0.6)
            if specific_actions > 0:
                completeness_score += 0.1

        return max(0.0, min(1.0, completeness_score))

    def _calculate_actionability(self, action_items: List[ActionItem]) -> float:
        """Calculate how actionable the conversation outcomes are"""
        if not action_items:
            return 0.2

        # Average specificity and confidence
        avg_specificity = statistics.mean([action.specificity_score for action in action_items])
        avg_confidence = statistics.mean([action.confidence for action in action_items])

        # Bonus for having timelines and responsible parties
        timeline_bonus = (
            sum(1 for action in action_items if action.timeline) / len(action_items) * 0.2
        )
        responsibility_bonus = (
            sum(1 for action in action_items if action.responsible_party) / len(action_items) * 0.1
        )

        actionability = (
            (avg_specificity + avg_confidence) / 2 + timeline_bonus + responsibility_bonus
        )
        return max(0.0, min(1.0, actionability))


# === MAIN CLARITY ANALYZER INTERFACE ===


class ClarityAnalyzer:
    """
    Unified Clarity Analyzer - Phase 10 Consolidation

    Main interface consolidating all clarity analysis functionality.
    Provides backward compatibility with legacy clarity modules.
    """

    def __init__(self):
        self.conversation_analyzer = ConversationAnalyzer()
        self.action_detector = ActionDetectionEngine()
        self.metrics_engine = ClarityMetricsEngine()

    def analyze(self, text: str) -> ConversationAnalysis:
        """Main analysis method - comprehensive conversation analysis"""
        return self.conversation_analyzer.analyze_conversation(text)

    def extract_actions(self, text: str) -> List[ActionItem]:
        """Extract action items from text"""
        return self.action_detector.extract_action_items(text)

    def calculate_metrics(self, text: str, action_items: List[ActionItem] = None) -> ClarityMetrics:
        """Calculate clarity metrics"""
        if action_items is None:
            action_items = self.extract_actions(text)
        return self.metrics_engine.calculate_clarity_metrics(text, action_items)

    def get_clarity_score(self, text: str) -> float:
        """Get overall clarity score for text"""
        action_items = self.extract_actions(text)
        metrics = self.calculate_metrics(text, action_items)
        return metrics.overall_score


# === LEGACY COMPATIBILITY (Backward Compatibility Layer) ===


# For backward compatibility during migration
def get_clarity_analyzer() -> ClarityAnalyzer:
    """Factory function for creating clarity analyzer"""
    return ClarityAnalyzer()


# Legacy imports compatibility
ActionDetector = ActionDetectionEngine  # Legacy name
ClarityMetrics = ClarityMetricsEngine  # Legacy name
ConversationAnalyzer = ConversationAnalyzer  # Already correct name
