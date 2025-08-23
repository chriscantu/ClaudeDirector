"""
Conversation Flow Analyzer for Next Action Clarity Framework

Tracks conversation patterns and identifies clarity indicators.
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .models import (
    Conversation,
    ConversationMessage,
    ClarityMetrics,
    ClarityIndicator,
    StuckPattern,
    ActionItem,
)
from .action_detector import ActionDetectionEngine


class ConversationFlowAnalyzer:
    """Tracks conversation patterns and identifies clarity indicators"""

    def __init__(self):
        self.action_detector = ActionDetectionEngine()
        self.clarity_patterns = self._initialize_clarity_patterns()
        self.stuck_patterns = self._initialize_stuck_patterns()
        self.framework_indicators = self._initialize_framework_indicators()

    def _initialize_clarity_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize patterns that indicate conversation clarity"""
        return {
            "positive": {
                "decision_clarity": [
                    r"(?:I've|I have)\s+(?:decided|chosen|selected)",
                    r"(?:My|The)\s+decision\s+is",
                    r"(?:I'm|I am)\s+going\s+(?:with|to)",
                    r"(?:The|Our)\s+(?:approach|strategy|plan)\s+(?:will be|is)",
                    r"(?:I'll|I will)\s+(?:implement|execute|proceed with)",
                ],
                "action_commitment": [
                    r"(?:I'll|I will)\s+(?:do|handle|take care of|work on)",
                    r"(?:My|Our)\s+next\s+(?:step|action|move)\s+(?:is|will be)",
                    r"(?:I'm|I am)\s+(?:planning|committed|ready)\s+to",
                    r"(?:Let's|We'll)\s+(?:start|begin|initiate|kick off)",
                    r"(?:I'll|I will)\s+(?:schedule|set up|arrange|organize)",
                ],
                "timeline_specificity": [
                    r"by\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)",
                    r"by\s+(?:end of|EOD|close of business)",
                    r"within\s+\d+\s+(?:days|weeks|hours)",
                    r"(?:this|next)\s+(?:week|month|quarter)",
                    r"by\s+\d{1,2}/\d{1,2}(?:/\d{2,4})?",
                ],
                "stakeholder_engagement": [
                    r"(?:I'll|I will)\s+(?:talk to|reach out to|contact|meet with)",
                    r"(?:I'll|I will)\s+(?:align with|get buy-in from|discuss with)",
                    r"(?:Let's|We'll)\s+(?:bring|include|involve)\s+\w+\s+(?:in|into)",
                    r"(?:I'll|I will)\s+(?:update|inform|brief)\s+\w+",
                ],
            },
            "negative": {
                "analysis_paralysis": [
                    r"(?:I'm|I am)\s+(?:still|not sure|uncertain|unclear)",
                    r"(?:I|We)\s+need\s+(?:more|additional)\s+(?:data|information|analysis)",
                    r"(?:Maybe|Perhaps|Possibly)\s+(?:I|we)\s+(?:should|could|might)",
                    r"(?:I'm|I am)\s+(?:torn|conflicted|undecided)\s+(?:between|about)",
                    r"(?:There are|I see)\s+(?:too many|multiple)\s+(?:options|choices)",
                ],
                "decision_avoidance": [
                    r"(?:I|We)\s+(?:should|need to)\s+(?:think about|consider|evaluate)",
                    r"(?:Let me|I'll)\s+(?:think about|consider|sleep on)\s+(?:this|it)",
                    r"(?:I|We)\s+(?:can't|shouldn't)\s+(?:decide|choose)\s+(?:yet|now)",
                    r"(?:I|We)\s+need\s+to\s+(?:wait|see|check)\s+(?:for|with|if)",
                    r"(?:It's|This is)\s+(?:too|very)\s+(?:complex|complicated|difficult)",
                ],
                "circular_discussion": [
                    r"(?:As I mentioned|Like I said)\s+(?:before|earlier)",
                    r"(?:Going back to|Returning to)\s+(?:what|the)",
                    r"(?:Again|Once more),?\s+(?:I|we|the)",
                    r"(?:We've|I've)\s+(?:already|previously)\s+(?:discussed|talked about)",
                    r"(?:This|That)\s+(?:brings us back|takes us back)\s+to",
                ],
                "information_seeking": [
                    r"(?:What|How)\s+(?:about|if|do you think)",
                    r"(?:Can|Could)\s+you\s+(?:tell me|explain|help me understand)",
                    r"(?:I|We)\s+(?:wonder|need to know|want to understand)",
                    r"(?:What's|How's)\s+(?:the|your)\s+(?:take|opinion|view)\s+on",
                    r"(?:Do|Would)\s+you\s+(?:have|know)\s+(?:any|more)",
                ],
            },
        }

    def _initialize_stuck_patterns(self) -> Dict[str, Dict]:
        """Initialize patterns that indicate user is stuck"""
        return {
            "analysis_loop": {
                "description": "User repeatedly requests more analysis without making decisions",
                "patterns": [
                    r"(?:more|additional|further)\s+(?:analysis|data|information)",
                    r"(?:need to|should)\s+(?:analyze|research|investigate)\s+(?:more|further)",
                    r"(?:what|how)\s+(?:about|if)\s+we\s+(?:look at|consider|examine)",
                ],
                "severity_threshold": 3,  # Number of occurrences to trigger
                "intervention": "Suggest using WRAP Decision Framework to structure decision-making",
            },
            "option_paralysis": {
                "description": "User identifies multiple options but cannot choose between them",
                "patterns": [
                    r"(?:I'm|We're)\s+(?:torn|split|undecided)\s+between",
                    r"(?:both|all)\s+(?:options|choices|approaches)\s+(?:seem|look|appear)",
                    r"(?:pros and cons|advantages and disadvantages)\s+(?:of|for)\s+(?:each|both)",
                ],
                "severity_threshold": 2,
                "intervention": "Apply Capital Allocation Framework to evaluate options systematically",
            },
            "perfectionism": {
                "description": "User seeks perfect information before making any decision",
                "patterns": [
                    r"(?:I|we)\s+need\s+to\s+be\s+(?:sure|certain|confident)",
                    r"(?:what if|suppose|imagine)\s+(?:something|things)\s+(?:go wrong|fail)",
                    r"(?:I'm|we're)\s+(?:not|still not)\s+(?:100%|completely)\s+(?:sure|confident)",
                ],
                "severity_threshold": 2,
                "intervention": "Emphasize 'good enough' decision-making and Type 2 reversible decisions",
            },
            "stakeholder_blame": {
                "description": "User blames external stakeholders for inability to proceed",
                "patterns": [
                    r"(?:I|we)\s+(?:can't|cannot)\s+(?:do|proceed|move forward)\s+(?:until|without)",
                    r"(?:waiting|need to wait)\s+(?:for|on)\s+\w+\s+to",
                    r"(?:it's|that's)\s+(?:up to|depends on)\s+\w+\s+to",
                ],
                "severity_threshold": 2,
                "intervention": "Identify proactive steps that can be taken independently",
            },
        }

    def _initialize_framework_indicators(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate strategic framework usage"""
        return {
            "WRAP Decision Framework": [
                r"(?:widen|broaden)\s+(?:options|alternatives)",
                r"(?:reality-test|test)\s+(?:assumptions|our thinking)",
                r"(?:attain|get)\s+(?:distance|perspective)",
                r"(?:prepare|plan)\s+to\s+be\s+wrong",
            ],
            "Good Strategy Bad Strategy": [
                r"(?:kernel|core)\s+of\s+(?:the\s+)?strategy",
                r"(?:diagnosis|problem)\s+(?:of|with)\s+(?:the\s+)?situation",
                r"(?:guiding|coherent)\s+(?:policy|approach)",
                r"(?:coordinated|coherent)\s+(?:actions|set of actions)",
            ],
            "Crucial Conversations": [
                r"(?:start|begin)\s+with\s+(?:heart|the right intentions)",
                r"(?:learn|understand)\s+to\s+look\s+for\s+(?:safety|silence|violence)",
                r"(?:make it safe|create safety)\s+(?:to|for)",
                r"(?:master|control)\s+(?:your|our)\s+(?:stories|emotions)",
            ],
            "Capital Allocation Framework": [
                r"(?:ROI|return on investment|investment return)",
                r"(?:opportunity cost|alternative uses)",
                r"(?:resource|capital)\s+(?:allocation|distribution)",
                r"(?:portfolio|mix)\s+of\s+(?:investments|initiatives)",
            ],
        }

    def analyze_conversation_flow(self, conversation: Conversation) -> ClarityMetrics:
        """Analyze conversation and return comprehensive clarity metrics"""
        # Extract action items
        action_items = self._extract_all_actions(conversation)

        # Analyze clarity indicators
        clarity_indicators = self._analyze_clarity_indicators(conversation)

        # Detect stuck patterns
        stuck_patterns = self._detect_stuck_patterns(conversation)

        # Calculate overall clarity score
        clarity_score = self._calculate_clarity_score(
            action_items, clarity_indicators, stuck_patterns
        )

        # Detect frameworks used
        frameworks_used = self._detect_frameworks_used(conversation)

        # Calculate time to clarity
        time_to_clarity = self._calculate_time_to_clarity(conversation, action_items)

        # Analyze persona effectiveness
        persona_effectiveness = self._analyze_persona_effectiveness(
            conversation, clarity_score
        )

        return ClarityMetrics(
            conversation_id=conversation.id,
            clarity_score=clarity_score,
            action_items=action_items,
            clarity_indicators=clarity_indicators,
            stuck_patterns=stuck_patterns,
            time_to_clarity=time_to_clarity,
            decision_frameworks_used=frameworks_used,
            persona_effectiveness=persona_effectiveness,
        )

    def _extract_all_actions(self, conversation: Conversation) -> List[ActionItem]:
        """Extract all action items from conversation messages"""
        all_actions = []

        for message in conversation.messages:
            if message.speaker == "user":  # Focus on user commitments
                actions = self.action_detector.extract_action_items(message.content)
                all_actions.extend(actions)

        return all_actions

    def _analyze_clarity_indicators(
        self, conversation: Conversation
    ) -> List[ClarityIndicator]:
        """Analyze conversation for clarity indicators"""
        indicators = []

        for message in conversation.messages:
            # Check positive indicators
            for category, patterns in self.clarity_patterns["positive"].items():
                for pattern in patterns:
                    matches = re.finditer(pattern, message.content, re.IGNORECASE)
                    for match in matches:
                        indicators.append(
                            ClarityIndicator(
                                type="positive",
                                text=match.group(0),
                                confidence=0.8,
                                pattern=category,
                            )
                        )

            # Check negative indicators
            for category, patterns in self.clarity_patterns["negative"].items():
                for pattern in patterns:
                    matches = re.finditer(pattern, message.content, re.IGNORECASE)
                    for match in matches:
                        indicators.append(
                            ClarityIndicator(
                                type="negative",
                                text=match.group(0),
                                confidence=0.7,
                                pattern=category,
                            )
                        )

        return indicators

    def _detect_stuck_patterns(self, conversation: Conversation) -> List[StuckPattern]:
        """Detect patterns indicating user is stuck"""
        stuck_patterns = []
        pattern_counts = {}

        # Count occurrences of each stuck pattern
        for message in conversation.messages:
            if message.speaker == "user":
                for pattern_name, pattern_info in self.stuck_patterns.items():
                    count = 0
                    for pattern_regex in pattern_info["patterns"]:
                        count += len(
                            re.findall(pattern_regex, message.content, re.IGNORECASE)
                        )

                    if pattern_name not in pattern_counts:
                        pattern_counts[pattern_name] = 0
                    pattern_counts[pattern_name] += count

        # Create stuck patterns for those exceeding threshold
        for pattern_name, count in pattern_counts.items():
            pattern_info = self.stuck_patterns[pattern_name]
            if count >= pattern_info["severity_threshold"]:
                severity = min(1.0, count / (pattern_info["severity_threshold"] * 2))
                stuck_patterns.append(
                    StuckPattern(
                        pattern_type=pattern_name,
                        description=pattern_info["description"],
                        severity=severity,
                        intervention_suggestion=pattern_info["intervention"],
                    )
                )

        return stuck_patterns

    def _calculate_clarity_score(
        self,
        action_items: List[ActionItem],
        clarity_indicators: List[ClarityIndicator],
        stuck_patterns: List[StuckPattern],
    ) -> float:
        """Calculate overall clarity score (0.0 to 1.0)"""
        base_score = 0.5

        # Action items contribution (40% of score)
        if action_items:
            action_score = sum(
                action.specificity_score * action.confidence for action in action_items
            ) / len(action_items)
            base_score += (action_score - 0.5) * 0.4

        # Clarity indicators contribution (30% of score)
        if clarity_indicators:
            positive_indicators = [
                ind for ind in clarity_indicators if ind.type == "positive"
            ]
            negative_indicators = [
                ind for ind in clarity_indicators if ind.type == "negative"
            ]

            positive_score = sum(ind.confidence for ind in positive_indicators)
            negative_score = sum(ind.confidence for ind in negative_indicators)

            indicator_balance = (positive_score - negative_score) / len(
                clarity_indicators
            )
            base_score += indicator_balance * 0.3

        # Stuck patterns penalty (30% of score)
        if stuck_patterns:
            stuck_penalty = sum(pattern.severity for pattern in stuck_patterns) / len(
                stuck_patterns
            )
            base_score -= stuck_penalty * 0.3

        return max(0.0, min(1.0, base_score))

    def _detect_frameworks_used(self, conversation: Conversation) -> List[str]:
        """Detect which strategic frameworks were used in conversation"""
        frameworks_detected = []

        conversation_text = " ".join(
            message.content for message in conversation.messages
        )

        for framework, patterns in self.framework_indicators.items():
            framework_score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, conversation_text, re.IGNORECASE))
                framework_score += matches

            # Require at least 2 pattern matches to confirm framework usage
            if framework_score >= 2:
                frameworks_detected.append(framework)

        return frameworks_detected

    def _calculate_time_to_clarity(
        self, conversation: Conversation, action_items: List[ActionItem]
    ) -> Optional[int]:
        """Calculate time in seconds to reach actionable clarity"""
        if not action_items or not conversation.messages:
            return None

        # Find first high-confidence action item
        first_clear_action = None
        for message in conversation.messages:
            if message.speaker == "user":
                actions = self.action_detector.extract_action_items(message.content)
                high_confidence_actions = [
                    action
                    for action in actions
                    if action.confidence >= 0.8 and action.specificity_score >= 0.7
                ]
                if high_confidence_actions:
                    first_clear_action = message
                    break

        if first_clear_action:
            time_diff = first_clear_action.timestamp - conversation.start_time
            return int(time_diff.total_seconds())

        return None

    def _analyze_persona_effectiveness(
        self, conversation: Conversation, clarity_score: float
    ) -> Dict[str, float]:
        """Analyze how effective each persona was in driving clarity"""
        persona_effectiveness = {}

        # Track which personas contributed to the conversation
        for message in conversation.messages:
            if message.speaker != "user":
                persona = message.speaker
                if persona not in persona_effectiveness:
                    persona_effectiveness[persona] = []

                # Simple heuristic: measure action-oriented language in persona responses
                action_indicators = len(
                    re.findall(
                        r"(?:recommend|suggest|propose|advise|should|will|next step)",
                        message.content,
                        re.IGNORECASE,
                    )
                )

                effectiveness = min(1.0, action_indicators / 10.0)  # Normalize
                persona_effectiveness[persona].append(effectiveness)

        # Average effectiveness per persona
        for persona in persona_effectiveness:
            scores = persona_effectiveness[persona]
            persona_effectiveness[persona] = (
                sum(scores) / len(scores) if scores else 0.0
            )

        return persona_effectiveness

    def detect_action_indicators(self, message: str) -> List[ClarityIndicator]:
        """Detect action indicators in a single message"""
        indicators = []

        # Check for positive action indicators
        for category, patterns in self.clarity_patterns["positive"].items():
            for pattern in patterns:
                matches = re.finditer(pattern, message, re.IGNORECASE)
                for match in matches:
                    indicators.append(
                        ClarityIndicator(
                            type="positive",
                            text=match.group(0),
                            confidence=0.8,
                            pattern=category,
                        )
                    )

        return indicators

    def calculate_clarity_score(self, conversation: Conversation) -> float:
        """Calculate clarity score for a conversation"""
        metrics = self.analyze_conversation_flow(conversation)
        return metrics.clarity_score

    def identify_stuck_patterns(self, conversation: Conversation) -> List[StuckPattern]:
        """Identify stuck patterns in a conversation"""
        return self._detect_stuck_patterns(conversation)
