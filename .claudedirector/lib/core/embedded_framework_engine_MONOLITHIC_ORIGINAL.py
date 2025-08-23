"""
Embedded Strategic Framework Engine
Provides systematic analysis capabilities without external dependencies.

Delivers the same strategic intelligence as MCP integration but with built-in frameworks
for zero-setup user experience.

Author: Martin (Principal Platform Architect)
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import structlog

# Configure logging
logger = structlog.get_logger(__name__)


@dataclass
class FrameworkAnalysis:
    """Result of embedded framework analysis"""

    framework_name: str
    structured_insights: Dict[str, Any]
    recommendations: List[str]
    implementation_steps: List[str]
    key_considerations: List[str]
    analysis_confidence: float


@dataclass
class SystematicResponse:
    """Complete systematic analysis response"""

    analysis: FrameworkAnalysis
    persona_integrated_response: str
    processing_time_ms: int
    framework_applied: str


class EmbeddedFrameworkEngine:
    """
    Built-in systematic analysis frameworks for strategic leadership.

    Provides the systematic analysis capabilities demonstrated in MCP integration
    but with zero external dependencies for true plug-and-play experience.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

        # Strategic Planning Frameworks - Built-in systematic approaches
        self.strategic_frameworks = {
            "strategic_platform_assessment": {
                "name": "Strategic Platform Assessment Framework",
                "domains": ["strategic", "organizational", "technical"],
                "steps": [
                    "Current State Analysis",
                    "Stakeholder Impact Mapping",
                    "Success Metrics Definition",
                    "Implementation Roadmap",
                    "Risk Mitigation Planning",
                ],
                "analysis_components": {
                    "current_state": {
                        "questions": [
                            "What is the current platform/team/system state?",
                            "What are the existing capabilities and gaps?",
                            "What constraints are we working within?",
                        ],
                        "deliverables": [
                            "situational_assessment",
                            "capability_inventory",
                            "constraint_analysis",
                        ],
                    },
                    "stakeholder_mapping": {
                        "questions": [
                            "Who are the key stakeholders and decision makers?",
                            "What are their motivations and concerns?",
                            "How do we align different stakeholder interests?",
                        ],
                        "deliverables": [
                            "stakeholder_matrix",
                            "influence_analysis",
                            "alignment_strategy",
                        ],
                    },
                    "success_metrics": {
                        "questions": [
                            "How will we measure success?",
                            "What are the leading and lagging indicators?",
                            "How do we track both quantitative and qualitative outcomes?",
                        ],
                        "deliverables": [
                            "metrics_framework",
                            "measurement_plan",
                            "reporting_strategy",
                        ],
                    },
                    "implementation_roadmap": {
                        "questions": [
                            "What is our phased approach?",
                            "What are the critical dependencies?",
                            "How do we sequence for maximum impact?",
                        ],
                        "deliverables": [
                            "phased_roadmap",
                            "dependency_analysis",
                            "milestone_planning",
                        ],
                    },
                    "risk_mitigation": {
                        "questions": [
                            "What could go wrong and how likely is it?",
                            "What are our mitigation strategies?",
                            "How do we maintain contingency options?",
                        ],
                        "deliverables": [
                            "risk_assessment",
                            "mitigation_plans",
                            "contingency_strategies",
                        ],
                    },
                },
            },
            "organizational_transformation": {
                "name": "Organizational Transformation Framework",
                "domains": ["organizational", "people", "strategic"],
                "steps": [
                    "Culture & Readiness Assessment",
                    "Change Impact Analysis",
                    "Communication Strategy",
                    "Capability Development Plan",
                    "Adoption & Sustainability",
                ],
                "analysis_components": {
                    "culture_readiness": {
                        "questions": [
                            "What is the current organizational culture?",
                            "How ready is the organization for change?",
                            "What cultural factors will support or hinder transformation?",
                        ],
                        "deliverables": [
                            "culture_assessment",
                            "readiness_evaluation",
                            "change_capacity_analysis",
                        ],
                    },
                    "change_impact": {
                        "questions": [
                            "Who will be impacted and how?",
                            "What changes in roles, processes, and tools are needed?",
                            "What is the scope of disruption?",
                        ],
                        "deliverables": [
                            "impact_mapping",
                            "role_changes",
                            "process_redesign",
                        ],
                    },
                },
            },
            "technical_strategy": {
                "name": "Technical Strategy Framework",
                "domains": ["technical", "strategic", "organizational"],
                "steps": [
                    "Architecture Assessment",
                    "Technical Debt Analysis",
                    "Evolution Roadmap",
                    "Implementation Strategy",
                    "Quality & Governance",
                ],
                "analysis_components": {
                    "architecture_assessment": {
                        "questions": [
                            "What is the current technical architecture?",
                            "What are the scalability and maintainability concerns?",
                            "How well does the architecture support business objectives?",
                        ],
                        "deliverables": [
                            "architecture_review",
                            "scalability_analysis",
                            "alignment_assessment",
                        ],
                    },
                    "technical_debt": {
                        "questions": [
                            "What technical debt exists and what is its impact?",
                            "What is the cost of continuing vs. addressing debt?",
                            "How do we prioritize debt reduction?",
                        ],
                        "deliverables": [
                            "debt_inventory",
                            "impact_analysis",
                            "reduction_strategy",
                        ],
                    },
                },
            },
            "rumelt_strategy_kernel": {
                "name": "Rumelt Strategy Kernel Framework",
                "domains": ["strategic", "organizational"],
                "steps": [
                    "Strategic Diagnosis",
                    "Guiding Policy Development",
                    "Coherent Action Design",
                    "Bad Strategy Detection",
                    "Strategic Leverage Identification",
                ],
                "analysis_components": {
                    "strategic_diagnosis": {
                        "questions": [
                            "What is the true nature of the challenge we face?",
                            "What are the critical obstacles and constraints?",
                            "What insights do we have that others might miss?",
                        ],
                        "deliverables": [
                            "challenge_definition",
                            "obstacle_analysis",
                            "insight_identification",
                        ],
                        "rumelt_principles": [
                            "Focus on the kernel - avoid strategic fluff",
                            "Identify the most critical bottleneck or challenge",
                            "Look for hidden patterns and leverage points",
                        ],
                    },
                    "guiding_policy": {
                        "questions": [
                            "What overall approach will we take to overcome the challenge?",
                            "What will we NOT do (focus and choice)?",
                            "How does this policy create advantage?",
                        ],
                        "deliverables": [
                            "policy_framework",
                            "strategic_choices",
                            "advantage_mechanism",
                        ],
                        "rumelt_principles": [
                            "Good strategy involves choice - what not to do matters",
                            "Policy should anticipate and reduce complexity",
                            "Coherent policies create cumulative advantage",
                        ],
                    },
                    "coherent_action": {
                        "questions": [
                            "What specific actions will implement our guiding policy?",
                            "How do these actions reinforce each other?",
                            "What resources and capabilities do we need?",
                        ],
                        "deliverables": [
                            "action_plan",
                            "resource_allocation",
                            "coordination_mechanisms",
                        ],
                        "rumelt_principles": [
                            "Actions must be coherent and mutually reinforcing",
                            "Focus effort on areas of strategic advantage",
                            "Build on strengths while addressing critical weaknesses",
                        ],
                    },
                    "bad_strategy_detection": {
                        "questions": [
                            "Are we falling into fluff (vague goals without substance)?",
                            "Are we facing the real challenge or avoiding it?",
                            "Are we mistaking goals for strategy?",
                        ],
                        "deliverables": [
                            "strategy_quality_assessment",
                            "red_flag_identification",
                            "strategy_refinement",
                        ],
                        "bad_strategy_patterns": [
                            "Fluff: vague language that sounds profound but says nothing",
                            "Failure to face the challenge: not identifying real obstacles",
                            "Mistaking goals for strategy: wishful thinking without method",
                            "Bad strategic objectives: impossible or impractical goals",
                        ],
                    },
                },
            },
            "decisive_wrap_framework": {
                "name": "Decisive WRAP Decision Framework",
                "domains": ["strategic", "process", "organizational"],
                "steps": [
                    "Widen Your Options",
                    "Reality-Test Your Assumptions",
                    "Attain Distance Before Deciding",
                    "Prepare to Be Wrong",
                ],
                "analysis_components": {
                    "widen_options": {
                        "questions": [
                            "What other options do we have beyond the obvious ones?",
                            "What would we do if our current favorite option disappeared?",
                            "How might we pursue multiple options simultaneously?",
                        ],
                        "deliverables": [
                            "expanded_option_set",
                            "vanishing_options_analysis",
                            "parallel_path_assessment",
                        ],
                        "heath_techniques": [
                            "Vanishing Options Test: What if your preferred option disappeared?",
                            "Opportunity Cost Analysis: What are we giving up?",
                            "AND not OR thinking: How can we pursue multiple paths?",
                            "Find someone who has solved this problem before",
                        ],
                    },
                    "reality_test": {
                        "questions": [
                            "What evidence would prove our assumptions wrong?",
                            "Who disagrees with our assessment and why?",
                            "What would have to be true for each option to succeed?",
                        ],
                        "deliverables": [
                            "assumption_validation",
                            "contrary_evidence",
                            "success_conditions",
                        ],
                        "heath_techniques": [
                            "Consider the Opposite: Actively seek disconfirming evidence",
                            "Zoom Out: Look at similar situations (base rates)",
                            "Zoom In: Get close-up perspective from those affected",
                            "Ooch: Run small experiments before big commitments",
                        ],
                    },
                    "attain_distance": {
                        "questions": [
                            "How will we feel about this decision in 10 minutes, 10 months, 10 years?",
                            "What would we advise our best friend to do?",
                            "What would our successor decide?",
                        ],
                        "deliverables": [
                            "temporal_perspective",
                            "advisor_viewpoint",
                            "emotional_regulation",
                        ],
                        "heath_techniques": [
                            "10-10-10 Rule: How will you feel in 10 min/months/years?",
                            "What would I tell my best friend?: Get outside perspective",
                            "What would our values suggest?: Connect to core principles",
                            "Honor your core priorities: Focus on what matters most",
                        ],
                    },
                    "prepare_for_wrong": {
                        "questions": [
                            "What could go wrong and how would we respond?",
                            "How can we set up early warning systems?",
                            "What would success look like and how will we measure it?",
                        ],
                        "deliverables": [
                            "risk_scenarios",
                            "early_warning_systems",
                            "success_metrics",
                        ],
                        "heath_techniques": [
                            "Pre-mortem Analysis: Imagine failure and work backwards",
                            "Prospective Hindsight: What will we wish we had known?",
                            "Set Tripwires: Automatic decision points based on data",
                            "Bookend your estimate: Consider best and worst case scenarios",
                        ],
                    },
                },
            },
            "scaling_up_excellence": {
                "name": "Scaling Up Excellence Framework",
                "domains": ["organizational", "strategic", "technical"],
                "steps": [
                    "Excellence Definition & Assessment",
                    "Buddhist vs. Catholic Strategy",
                    "Hot Causes Development",
                    "Cool Solutions Implementation",
                    "Connect and Cascade Planning",
                    "Cut and Growth Execution",
                ],
                "analysis_components": {
                    "scaling_assessment": {
                        "questions": [
                            "What excellence are we trying to scale?",
                            "What's the current state of adoption/consistency?",
                            "What are the barriers to scaling this excellence?",
                        ],
                        "deliverables": [
                            "excellence_definition",
                            "current_state_assessment",
                            "barrier_analysis",
                        ],
                        "sutton_rao_principles": [
                            "Mindset over footprint - focus on spreading understanding, not just size",
                            "Excellence must be preserved during scaling, not just replicated",
                            "Assess barriers systematically - technical, cultural, and organizational",
                        ],
                    },
                    "buddhist_catholic_strategy": {
                        "questions": [
                            "What must be standardized (Catholic) vs. what can be adapted locally (Buddhist)?",
                            "Where do we need flexibility vs. strict compliance?",
                            "How do we balance consistency with team autonomy?",
                        ],
                        "deliverables": [
                            "standardization_strategy",
                            "flexibility_zones",
                            "adaptation_guidelines",
                        ],
                        "sutton_rao_principles": [
                            "Catholic: Strict replication for critical standards (security, compliance)",
                            "Buddhist: Local adaptation for context-specific implementations (UX, workflows)",
                            "Balance standardization with flexibility based on risk and context",
                        ],
                    },
                    "hot_causes_development": {
                        "questions": [
                            "Why should teams care about this excellence?",
                            "What emotional drivers will create engagement?",
                            "How do we make this personally meaningful?",
                        ],
                        "deliverables": [
                            "motivation_strategy",
                            "emotional_drivers",
                            "personal_value_proposition",
                        ],
                        "sutton_rao_principles": [
                            "Hot Causes: Emotional engagement and motivation (the 'why')",
                            "Connect excellence to personal and team pride",
                            "Make the benefits tangible and immediately felt",
                        ],
                    },
                    "cool_solutions_implementation": {
                        "questions": [
                            "What practical tools make excellence easier than non-excellence?",
                            "How do we reduce friction for adoption?",
                            "What systems support scaling?",
                        ],
                        "deliverables": [
                            "tool_strategy",
                            "friction_reduction_plan",
                            "support_systems",
                        ],
                        "sutton_rao_principles": [
                            "Cool Solutions: Practical tools and processes (the 'how')",
                            "Make the right thing easier than the wrong thing",
                            "Reduce cognitive load and friction for adoption",
                        ],
                    },
                    "connect_cascade_planning": {
                        "questions": [
                            "How do we connect people to share knowledge?",
                            "What's our cascade strategy across teams/levels?",
                            "How do we prevent knowledge silos?",
                        ],
                        "deliverables": [
                            "connection_strategy",
                            "cascade_plan",
                            "knowledge_sharing_systems",
                        ],
                        "sutton_rao_principles": [
                            "Connect: Link people to share knowledge and prevent isolation",
                            "Cascade: Spread behaviors through organizational layers systematically",
                            "Build bridges between teams and hierarchical levels",
                        ],
                    },
                    "cut_growth_execution": {
                        "questions": [
                            "What negative practices must we eliminate?",
                            "What positive practices do we want to expand?",
                            "How do we sequence elimination and growth?",
                        ],
                        "deliverables": [
                            "elimination_strategy",
                            "growth_strategy",
                            "sequencing_plan",
                        ],
                        "sutton_rao_principles": [
                            "Cut: Eliminate negative behaviors and practices systematically",
                            "Growth: Expand positive behaviors and practices strategically",
                            "Balance elimination and growth - often need to cut before growing",
                        ],
                    },
                },
            },
            "team_topologies": {
                "name": "Team Topologies Framework",
                "domains": ["organizational", "strategic", "technical"],
                "steps": [
                    "Team Type Assessment",
                    "Interaction Mode Design",
                    "Conway's Law Analysis",
                    "Cognitive Load Evaluation",
                    "Team Evolution Strategy",
                ],
                "analysis_components": {
                    "team_type_assessment": {
                        "questions": [
                            "What types of teams do we need for optimal value delivery?",
                            "Which domains need stream-aligned teams vs. platform teams?",
                            "Where do we need enabling or complicated subsystem teams?",
                        ],
                        "deliverables": [
                            "team_type_mapping",
                            "domain_alignment",
                            "team_purpose_definition",
                        ],
                        "skelton_pais_principles": [
                            "Stream-aligned: End-to-end ownership of business domain",
                            "Platform: Self-service internal services for other teams",
                            "Enabling: Temporary assistance to build capabilities",
                            "Complicated Subsystem: Specialized knowledge for complex domains",
                        ],
                    },
                    "interaction_mode_design": {
                        "questions": [
                            "How should teams interact to minimize dependencies?",
                            "Which relationships need collaboration vs. X-as-a-Service?",
                            "Where do we need facilitating interactions?",
                        ],
                        "deliverables": [
                            "interaction_patterns",
                            "dependency_analysis",
                            "communication_protocols",
                        ],
                        "skelton_pais_principles": [
                            "Collaboration: Temporary for discovery and complex problem solving",
                            "X-as-a-Service: Clear API contracts for stable services",
                            "Facilitating: Knowledge transfer until capability is built",
                        ],
                    },
                    "conways_law_analysis": {
                        "questions": [
                            "How does our current team structure affect our architecture?",
                            "What team structure would create our desired architecture?",
                            "Where are Conway's Law misalignments causing problems?",
                        ],
                        "deliverables": [
                            "structure_architecture_mapping",
                            "misalignment_identification",
                            "optimization_strategy",
                        ],
                        "skelton_pais_principles": [
                            "Team structure determines system architecture (Conway's Law)",
                            "Align team boundaries with desired architectural boundaries",
                            "Inverse Conway Maneuver: Design teams to get desired architecture",
                        ],
                    },
                    "cognitive_load_evaluation": {
                        "questions": [
                            "What is the cognitive load on each team?",
                            "Which teams are overwhelmed vs. underutilized?",
                            "How can we optimize team focus and reduce complexity?",
                        ],
                        "deliverables": [
                            "cognitive_load_assessment",
                            "complexity_analysis",
                            "focus_optimization",
                        ],
                        "skelton_pais_principles": [
                            "Teams have limited cognitive capacity (5-9 people optimal)",
                            "Minimize cognitive load through clear boundaries and responsibilities",
                            "Use platform teams to reduce complexity for stream-aligned teams",
                        ],
                    },
                    "team_evolution_strategy": {
                        "questions": [
                            "How should our team structure evolve over time?",
                            "What triggers team topology changes?",
                            "How do we manage team transitions and reorganizations?",
                        ],
                        "deliverables": [
                            "evolution_roadmap",
                            "transition_planning",
                            "change_triggers",
                        ],
                        "skelton_pais_principles": [
                            "Team topologies should evolve with organizational and technical needs",
                            "Plan transitions carefully to maintain flow and minimize disruption",
                            "Use sensing mechanisms to detect when topology changes are needed",
                        ],
                    },
                },
            },
            "accelerate_performance": {
                "name": "Accelerate Team Performance Framework",
                "domains": ["organizational", "technical", "strategic"],
                "steps": [
                    "DORA Metrics Assessment",
                    "Capability Gap Analysis",
                    "Team Composition Optimization",
                    "Performance Improvement Planning",
                    "Culture Development Strategy",
                ],
                "analysis_components": {
                    "dora_metrics_assessment": {
                        "questions": [
                            "What are our current DORA metrics (deployment frequency, lead time, failure rate, recovery time)?",
                            "How do we compare to high-performing teams?",
                            "Which metrics need the most improvement?",
                        ],
                        "deliverables": [
                            "dora_baseline",
                            "performance_comparison",
                            "improvement_priorities",
                        ],
                        "forsgren_humble_kim_principles": [
                            "Elite teams deploy multiple times per day with <1hr lead time",
                            "High performers have <15% change failure rate and <1hr recovery",
                            "DORA metrics predict organizational performance and profitability",
                        ],
                    },
                    "capability_gap_analysis": {
                        "questions": [
                            "What technical capabilities are missing for high performance?",
                            "Which management and cultural capabilities need development?",
                            "What blockers prevent continuous delivery and deployment?",
                        ],
                        "deliverables": [
                            "capability_assessment",
                            "gap_identification",
                            "blocker_analysis",
                        ],
                        "forsgren_humble_kim_principles": [
                            "Technical practices: CI/CD, test automation, trunk-based development",
                            "Management practices: lean product development, team empowerment",
                            "Cultural practices: psychological safety, learning culture, customer focus",
                        ],
                    },
                    "team_composition_optimization": {
                        "questions": [
                            "What is the optimal team size and skill mix?",
                            "How do we balance generalists vs. specialists?",
                            "What psychological safety and cultural factors impact performance?",
                        ],
                        "deliverables": [
                            "team_size_optimization",
                            "skill_mix_strategy",
                            "culture_assessment",
                        ],
                        "forsgren_humble_kim_principles": [
                            "Small autonomous teams (5-9 people) with cross-functional skills",
                            "Psychological safety enables learning from failures and innovation",
                            "T-shaped skills: broad knowledge with deep specialization",
                        ],
                    },
                    "performance_improvement_planning": {
                        "questions": [
                            "What systematic approach will improve our performance metrics?",
                            "How do we prioritize capability building initiatives?",
                            "What measurement and feedback loops ensure progress?",
                        ],
                        "deliverables": [
                            "improvement_roadmap",
                            "capability_building_plan",
                            "measurement_strategy",
                        ],
                        "forsgren_humble_kim_principles": [
                            "Focus on capabilities that improve flow and feedback loops",
                            "Measure outcomes, not just outputs or activity",
                            "Use scientific method: hypothesis, experiment, measure, learn",
                        ],
                    },
                    "culture_development_strategy": {
                        "questions": [
                            "How do we build psychological safety and learning culture?",
                            "What practices encourage experimentation and innovation?",
                            "How do we align team incentives with organizational outcomes?",
                        ],
                        "deliverables": [
                            "culture_strategy",
                            "psychological_safety_plan",
                            "incentive_alignment",
                        ],
                        "forsgren_humble_kim_principles": [
                            "Psychological safety is the foundation of high performance",
                            "Learning culture: encourage experimentation, learning from failures",
                            "Job satisfaction correlates with organizational performance",
                        ],
                    },
                },
            },
            "crucial_conversations": {
                "name": "Crucial Conversations Framework",
                "domains": ["stakeholder", "communication", "organizational"],
                "steps": [
                    "Start with Heart",
                    "Learn to Look",
                    "Make it Safe",
                    "Master Your Stories",
                    "STATE Your Path",
                    "Explore Others' Paths",
                    "Move to Action",
                ],
                "analysis_components": {
                    "start_with_heart": {
                        "questions": [
                            "What do I really want for myself in this conversation?",
                            "What do I want for others and the relationship?",
                            "How would I behave if I really wanted these results?",
                        ],
                        "deliverables": [
                            "intention_clarity",
                            "desired_outcomes",
                            "motivation_alignment",
                        ],
                        "patterson_grenny_principles": [
                            "Focus on what you really want, not just what's easy",
                            "Clarify your real purpose before the conversation begins",
                            "Ask yourself: How would I behave if I really wanted these results?",
                        ],
                    },
                    "learn_to_look": {
                        "questions": [
                            "What signs indicate this conversation is becoming crucial?",
                            "When is safety at risk in our dialogue?",
                            "What patterns of silence or violence am I seeing?",
                        ],
                        "deliverables": [
                            "safety_assessment",
                            "conversation_patterns",
                            "risk_indicators",
                        ],
                        "patterson_grenny_principles": [
                            "Watch for when conversations become crucial (high stakes, differing opinions, strong emotions)",
                            "Recognize signs of safety problems: silence (withdrawing, avoiding, masking) and violence (attacking, labeling, controlling)",
                            "Learn to look at content and conditions of conversation simultaneously",
                        ],
                    },
                    "make_it_safe": {
                        "questions": [
                            "How can I restore safety to this conversation?",
                            "What mutual purpose can we establish?",
                            "How do I demonstrate respect for others' perspectives?",
                        ],
                        "deliverables": [
                            "safety_restoration",
                            "mutual_purpose",
                            "respect_demonstration",
                        ],
                        "patterson_grenny_principles": [
                            "Apologize when appropriate to restore safety",
                            "Contrast to fix misunderstandings (what you don't mean vs. what you do mean)",
                            "Create mutual purpose by finding shared goals and common ground",
                        ],
                    },
                    "master_your_stories": {
                        "questions": [
                            "What story am I telling myself about this situation?",
                            "What are the facts vs. my interpretations?",
                            "What assumptions am I making that might be wrong?",
                        ],
                        "deliverables": [
                            "fact_story_separation",
                            "assumption_testing",
                            "emotional_regulation",
                        ],
                        "patterson_grenny_principles": [
                            "Separate facts from the stories you create about those facts",
                            "Tell the most respectful story first, then test your assumptions",
                            "Take charge of your emotions by taking charge of your stories",
                        ],
                    },
                    "state_your_path": {
                        "questions": [
                            "How can I share my perspective persuasively, not abrasively?",
                            "What facts should I share first?",
                            "How do I encourage others to share their views?",
                        ],
                        "deliverables": [
                            "persuasive_communication",
                            "fact_sharing",
                            "dialogue_invitation",
                        ],
                        "patterson_grenny_principles": [
                            "Share your facts: Start with least controversial facts",
                            "Tell your story: Explain what you're beginning to conclude",
                            "Ask for others' paths: Encourage others to share their views",
                            "Talk tentatively: State your story as a story, not as fact",
                            "Encourage testing: Make it safe for others to express differing views",
                        ],
                    },
                    "explore_others_paths": {
                        "questions": [
                            "How can I encourage others to share their perspectives?",
                            "What am I missing from their point of view?",
                            "How do I listen when they blow up or clam up?",
                        ],
                        "deliverables": [
                            "perspective_exploration",
                            "empathetic_listening",
                            "understanding_building",
                        ],
                        "patterson_grenny_principles": [
                            "Ask: Start with sincere curiosity and genuine questions",
                            "Mirror: Acknowledge the emotions behind their words",
                            "Paraphrase: Restate what you've heard to confirm understanding",
                            "Prime: If they won't share, take your best guess at their perspective",
                        ],
                    },
                    "move_to_action": {
                        "questions": [
                            "What specific actions will we take as a result of this conversation?",
                            "Who will do what by when?",
                            "How will we follow up and ensure accountability?",
                        ],
                        "deliverables": [
                            "action_commitments",
                            "accountability_structure",
                            "follow_up_plan",
                        ],
                        "patterson_grenny_principles": [
                            "Decide how decisions will be made: Command, consult, vote, or consensus",
                            "Document who does what by when",
                            "Plan follow-up and create accountability systems",
                        ],
                    },
                },
            },
            "capital_allocation": {
                "name": "Capital Allocation Framework",
                "domains": ["strategic", "financial", "technical"],
                "steps": [
                    "Investment Assessment",
                    "Strategic Alignment",
                    "ROI Analysis & Measurement",
                    "Risk Assessment & Mitigation",
                    "Portfolio Optimization",
                ],
                "analysis_components": {
                    "investment_assessment": {
                        "questions": [
                            "What are all our potential technology investment opportunities?",
                            "How do we categorize platform vs. product vs. innovation investments?",
                            "What resources and timelines are required for each option?",
                        ],
                        "deliverables": [
                            "investment_portfolio",
                            "opportunity_mapping",
                            "resource_requirements",
                        ],
                        "capital_allocation_principles": [
                            "Comprehensive evaluation of all potential technology investments",
                            "Standardized criteria for comparing diverse investment opportunities",
                            "Clear categorization: Platform (infrastructure), Product (features), Innovation (R&D)",
                        ],
                    },
                    "strategic_alignment": {
                        "questions": [
                            "How do these investments support our business strategy?",
                            "What stakeholder value will each investment create?",
                            "Which investments are critical vs. nice-to-have?",
                        ],
                        "deliverables": [
                            "alignment_matrix",
                            "strategic_contribution",
                            "value_proposition",
                        ],
                        "capital_allocation_principles": [
                            "Business outcome focus: Every investment must contribute to strategic objectives",
                            "Stakeholder value creation: Clear value for customers, users, and business",
                            "Strategic criticality assessment: Must-have vs. should-have vs. could-have",
                        ],
                    },
                    "roi_analysis_measurement": {
                        "questions": [
                            "What are the expected returns from each investment?",
                            "How do we measure both direct and strategic value?",
                            "What metrics will track actual vs. projected returns?",
                        ],
                        "deliverables": [
                            "roi_projections",
                            "value_tracking",
                            "performance_metrics",
                        ],
                        "capital_allocation_principles": [
                            "Multiple ROI metrics: Cost reduction, revenue generation, risk mitigation",
                            "Strategic value metrics: Time to market, developer productivity, platform adoption",
                            "Innovation metrics: Learning velocity, market position, future optionality",
                        ],
                    },
                    "risk_assessment_mitigation": {
                        "questions": [
                            "What technical, market, and organizational risks does each investment carry?",
                            "How can we mitigate the highest-impact risks?",
                            "What contingency plans do we need?",
                        ],
                        "deliverables": [
                            "risk_register",
                            "mitigation_strategies",
                            "contingency_planning",
                        ],
                        "capital_allocation_principles": [
                            "Technical risk: Implementation complexity, dependencies, skill requirements",
                            "Market risk: Technology adoption, competitive landscape, timing",
                            "Organizational risk: Change management, cultural fit, resource availability",
                        ],
                    },
                    "portfolio_optimization": {
                        "questions": [
                            "How should we balance our investment portfolio across categories?",
                            "Which investments should we prioritize, delay, or cancel?",
                            "How do we continuously rebalance based on performance?",
                        ],
                        "deliverables": [
                            "portfolio_recommendations",
                            "reallocation_strategy",
                            "performance_reviews",
                        ],
                        "capital_allocation_principles": [
                            "Portfolio balance: Mix of platform stability, product growth, and innovation exploration",
                            "Dynamic rebalancing: Adjust based on performance, market changes, strategic shifts",
                            "Opportunity cost evaluation: Consider what you're not doing when making choices",
                        ],
                    },
                },
            },
            "decision_framework": {
                "name": "Integrated Strategic Decision Framework",
                "domains": ["strategic", "process"],
                "steps": [
                    "Decision Context Definition",
                    "Strategic Diagnosis (Rumelt)",
                    "Option Generation (WRAP)",
                    "Reality Testing & Analysis",
                    "Decision Implementation Planning",
                ],
                "analysis_components": {
                    "decision_context": {
                        "questions": [
                            "What decision are we making and why now?",
                            "What constraints and requirements must we consider?",
                            "Who are the decision makers and stakeholders?",
                        ],
                        "deliverables": [
                            "decision_statement",
                            "context_analysis",
                            "stakeholder_roles",
                        ],
                    },
                    "strategic_diagnosis": {
                        "questions": [
                            "What is the true nature of the challenge behind this decision?",
                            "What are the critical obstacles we must overcome?",
                            "What insights might give us strategic advantage?",
                        ],
                        "deliverables": [
                            "challenge_diagnosis",
                            "obstacle_identification",
                            "strategic_insights",
                        ],
                        "integration_note": "Applies Rumelt's diagnostic thinking to decision context",
                    },
                    "options_analysis": {
                        "questions": [
                            "What are all viable options (including non-obvious ones)?",
                            "What assumptions underlie each option?",
                            "How do we reality-test these assumptions?",
                        ],
                        "deliverables": [
                            "expanded_options_matrix",
                            "assumption_analysis",
                            "reality_testing_plan",
                        ],
                        "integration_note": "Combines Heath WRAP option widening with rigorous analysis",
                    },
                },
            },
        }

        # Domain-specific best practices and patterns
        self.domain_patterns = {
            "strategic": {
                "rumelt_strategy_patterns": [
                    "Good strategy has a kernel: diagnosis, policy, action",
                    "Focus and choice are essential - decide what NOT to do",
                    "Avoid strategic fluff - be specific and concrete",
                    "Face the challenge directly, don't dodge the hard problems",
                    "Look for leverage points where effort creates disproportionate results",
                ],
                "planning_patterns": [
                    "Start with vision and work backwards to concrete steps",
                    "Balance aspirational goals with pragmatic constraints",
                    "Build alignment before diving into execution details",
                    "Plan in phases to enable learning and adaptation",
                ],
                "stakeholder_patterns": [
                    "Map stakeholders by influence and interest levels",
                    "Identify champions, skeptics, and neutral parties",
                    "Create targeted communication for each stakeholder group",
                    "Build coalitions to support key initiatives",
                ],
                "heath_decision_patterns": [
                    "Widen options before narrowing them - avoid false dichotomies",
                    "Actively seek disconfirming evidence to test assumptions",
                    "Use temporal distance to manage emotional decision-making",
                    "Prepare for failure with pre-mortems and early warning systems",
                ],
                "sutton_rao_scaling_patterns": [
                    "Balance Buddhist flexibility with Catholic standardization based on context",
                    "Hot causes (emotional engagement) must accompany cool solutions (practical tools)",
                    "Connect people and cascade knowledge to prevent scaling failures",
                    "Cut negative practices before growing positive ones for maximum impact",
                ],
            },
            "organizational": {
                "change_patterns": [
                    "Lead with why before explaining what and how",
                    "Address emotional aspects of change alongside logical ones",
                    "Create early wins to build momentum and credibility",
                    "Provide multiple feedback loops and adjustment opportunities",
                ],
                "scaling_patterns": [
                    "Focus on mindset preservation over simple replication",
                    "Balance standardization (Catholic) with local adaptation (Buddhist)",
                    "Connect teams horizontally and cascade vertically for knowledge sharing",
                    "Eliminate negative practices before scaling positive ones",
                ],
                "team_topologies_patterns": [
                    "Team structure determines system architecture (Conway's Law)",
                    "Optimize for fast flow with minimal cognitive load per team",
                    "Use platform teams to reduce complexity for stream-aligned teams",
                    "Design team interactions to minimize dependencies and maximize autonomy",
                ],
                "accelerate_patterns": [
                    "Psychological safety is the foundation of high-performing teams",
                    "Small autonomous teams with T-shaped skills deliver best outcomes",
                    "Measure capabilities and outcomes, not activities or outputs",
                    "Continuous improvement through scientific method and experimentation",
                ],
                "crucial_conversations_patterns": [
                    "Start with heart: Focus on what you really want for everyone",
                    "Make it safe: Create conditions where honest dialogue can occur",
                    "STATE your path: Share facts, tell your story, ask for others' paths",
                    "Move to action: Convert dialogue into concrete commitments and follow-through",
                ],
                "capital_allocation_patterns": [
                    "Portfolio balance: Mix platform stability, product growth, and innovation exploration",
                    "ROI measurement: Quantify both direct returns and strategic value creation",
                    "Risk management: Balance innovation with stability and security",
                    "Opportunity cost evaluation: Consider what you're not doing when making choices",
                ],
                "team_patterns": [
                    "Invest in psychological safety before pushing performance",
                    "Balance autonomy with alignment to organizational goals",
                    "Develop people through challenging assignments and coaching",
                    "Recognize both individual contributions and team achievements",
                ],
            },
            "technical": {
                "architecture_patterns": [
                    "Design for evolution, not just current requirements",
                    "Make implicit assumptions explicit in architectural decisions",
                    "Balance consistency with team autonomy and innovation",
                    "Plan technical debt management as an ongoing capability",
                ],
                "delivery_patterns": [
                    "Optimize for developer productivity and team velocity",
                    "Build quality into the process, not as a separate phase",
                    "Enable experimentation with safe-to-fail approaches",
                    "Instrument systems for observability and learning",
                ],
            },
        }

        # Implementation templates for common scenarios
        self.implementation_templates = {
            "quarterly_planning": {
                "name": "Quarterly Strategic Planning",
                "timeline": "8-12 weeks",
                "key_activities": [
                    "Stakeholder alignment sessions (weeks 1-2)",
                    "Current state assessment (weeks 2-4)",
                    "Strategy development workshops (weeks 4-6)",
                    "Implementation planning (weeks 6-8)",
                    "Communication and rollout (weeks 8-12)",
                ],
                "critical_success_factors": [
                    "Executive sponsorship and visible commitment",
                    "Cross-functional team representation",
                    "Clear decision-making authority and process",
                    "Regular communication and feedback loops",
                ],
            },
            "team_scaling": {
                "name": "Team Scaling Strategy",
                "timeline": "12-16 weeks",
                "key_activities": [
                    "Current team assessment and capacity planning",
                    "Role definition and hiring strategy development",
                    "Onboarding process design and documentation",
                    "Culture integration and team formation",
                    "Performance tracking and adjustment",
                ],
                "critical_success_factors": [
                    "Clear vision of target team structure and capabilities",
                    "Strong hiring and onboarding processes",
                    "Investment in culture and team dynamics",
                    "Gradual scaling with integration checkpoints",
                ],
            },
        }

    def analyze_systematically(
        self,
        user_input: str,
        persona_context: str,
        domain_focus: List[str],
        complexity_level: str = "complex",
    ) -> FrameworkAnalysis:
        """
        Apply systematic analysis frameworks to user input.

        Args:
            user_input: The user's question or challenge
            persona_context: The persona providing analysis (diego, martin, rachel, etc.)
            domain_focus: Primary domains (strategic, organizational, technical)
            complexity_level: Level of analysis depth needed

        Returns:
            FrameworkAnalysis with structured insights and recommendations
        """
        start_time = time.time()

        # Select appropriate framework based on input analysis
        framework = self._select_framework(user_input, domain_focus)

        # Apply the framework to generate structured insights
        insights = self._apply_framework(framework, user_input, persona_context)

        # Generate actionable recommendations
        recommendations = self._generate_recommendations(
            framework, insights, persona_context
        )

        # Create implementation steps
        implementation_steps = self._create_implementation_steps(framework, insights)

        # Identify key considerations and risks
        key_considerations = self._identify_considerations(
            framework, insights, domain_focus
        )

        # Calculate confidence based on framework match and input clarity
        confidence = self._calculate_confidence(framework, user_input, domain_focus)

        processing_time = int((time.time() - start_time) * 1000)

        logger.info(
            "embedded_framework_analysis_complete",
            framework=framework["name"],
            persona=persona_context,
            domains=domain_focus,
            confidence=confidence,
            processing_time_ms=processing_time,
        )

        return FrameworkAnalysis(
            framework_name=framework["name"],
            structured_insights=insights,
            recommendations=recommendations,
            implementation_steps=implementation_steps,
            key_considerations=key_considerations,
            analysis_confidence=confidence,
        )

    def _select_framework(
        self, user_input: str, domain_focus: List[str]
    ) -> Dict[str, Any]:
        """Select the most appropriate framework based on input and domains"""

        input_lower = user_input.lower()

        # Framework selection logic based on keywords and domain focus
        framework_scores = {}

        for framework_name, framework in self.strategic_frameworks.items():
            score = 0.0

            # Domain alignment scoring
            framework_domains = framework.get("domains", [])
            domain_overlap = len(set(domain_focus) & set(framework_domains))
            score += domain_overlap * 0.4

            # Keyword matching scoring
            framework_keywords = {
                "strategic_platform_assessment": [
                    "platform",
                    "strategy",
                    "assessment",
                    "stakeholder",
                    "roadmap",
                    "planning",
                    "quarterly",
                    "q4",
                    "alignment",
                ],
                "organizational_transformation": [
                    "transformation",
                    "change",
                    "organizational",
                    "culture",
                    "team",
                    "scaling",
                    "structure",
                    "communication",
                ],
                "technical_strategy": [
                    "technical",
                    "architecture",
                    "system",
                    "infrastructure",
                    "debt",
                    "engineering",
                    "platform",
                    "design",
                ],
                "rumelt_strategy_kernel": [
                    "strategy",
                    "strategic",
                    "kernel",
                    "diagnosis",
                    "policy",
                    "coherent",
                    "challenge",
                    "obstacle",
                    "leverage",
                    "focus",
                    "choice",
                    "advantage",
                    "bad strategy",
                    "fluff",
                    "good strategy",
                ],
                "decisive_wrap_framework": [
                    "decision",
                    "decide",
                    "options",
                    "choose",
                    "assumptions",
                    "reality",
                    "distance",
                    "wrong",
                    "prepare",
                    "wrap",
                    "widen",
                    "test",
                    "attain",
                    "alternatives",
                    "evidence",
                    "bias",
                ],
                "scaling_up_excellence": [
                    "scaling",
                    "scale up",
                    "adoption",
                    "spread",
                    "rollout",
                    "standardization",
                    "consistency",
                    "quality",
                    "excellence",
                    "practices",
                    "teams",
                    "organization",
                    "across",
                    "multiple",
                    "buddhist",
                    "catholic",
                    "hot causes",
                    "cool solutions",
                    "connect",
                    "cascade",
                    "cut",
                    "growth",
                    "mindset",
                    "footprint",
                ],
                "team_topologies": [
                    "team structure",
                    "organizational design",
                    "team types",
                    "conway's law",
                    "cognitive load",
                    "platform team",
                    "enabling team",
                    "stream-aligned",
                    "complicated subsystem",
                    "interaction modes",
                    "collaboration",
                    "facilitating",
                    "x-as-a-service",
                    "team boundaries",
                    "team topology",
                ],
                "accelerate_performance": [
                    "team performance",
                    "dora metrics",
                    "deployment frequency",
                    "lead time",
                    "psychological safety",
                    "team composition",
                    "high performing teams",
                    "change failure rate",
                    "recovery time",
                    "continuous integration",
                    "team capabilities",
                    "performance metrics",
                    "team culture",
                ],
                "crucial_conversations": [
                    "stakeholder",
                    "difficult conversation",
                    "executive",
                    "alignment",
                    "conflict",
                    "communication",
                    "negotiation",
                    "buy-in",
                    "crucial conversation",
                    "dialogue",
                    "safety",
                    "mutual purpose",
                    "persuasive",
                    "listening",
                    "action",
                ],
                "capital_allocation": [
                    "budget",
                    "investment",
                    "roi",
                    "resource allocation",
                    "prioritization",
                    "cost",
                    "value",
                    "portfolio",
                    "funding",
                    "capital",
                    "financial",
                    "resource",
                    "allocation",
                    "optimization",
                    "returns",
                ],
                "decision_framework": [
                    "decision",
                    "choose",
                    "options",
                    "evaluate",
                    "criteria",
                    "trade-off",
                    "recommendation",
                    "analysis",
                ],
            }

            keywords = framework_keywords.get(framework_name, [])
            keyword_matches = sum(1 for keyword in keywords if keyword in input_lower)
            score += keyword_matches * 0.15

            framework_scores[framework_name] = score

        # Select framework with highest score
        best_framework_name = max(framework_scores, key=framework_scores.get)

        # Prioritize decision and strategy frameworks based on strong signals
        decision_signals = [
            "decision",
            "decide",
            "choose",
            "options",
            "alternative",
            "should we",
            "best approach",
            "which option",
        ]
        strategy_signals = [
            "fluff",
            "bad strategy",
            "real strategy",
            "challenge",
            "obstacle",
            "strategic",
            "leverage",
        ]

        has_decision_signals = any(signal in input_lower for signal in decision_signals)
        has_strategy_signals = any(signal in input_lower for signal in strategy_signals)

        # Override framework selection for strong decision/strategy signals
        if (
            has_decision_signals
            and framework_scores.get("decisive_wrap_framework", 0) >= 0.1
        ):
            best_framework_name = "decisive_wrap_framework"
        elif (
            has_strategy_signals
            and framework_scores.get("rumelt_strategy_kernel", 0) >= 0.1
        ):
            best_framework_name = "rumelt_strategy_kernel"
        elif framework_scores[best_framework_name] < 0.3:
            # Check for specific patterns that should trigger Rumelt or WRAP
            if has_strategy_signals:
                best_framework_name = "rumelt_strategy_kernel"
            elif has_decision_signals:
                best_framework_name = "decisive_wrap_framework"
            else:
                best_framework_name = "strategic_platform_assessment"

        return self.strategic_frameworks[best_framework_name]

    def _apply_framework(
        self, framework: Dict[str, Any], user_input: str, persona_context: str
    ) -> Dict[str, Any]:
        """Apply the selected framework to generate structured insights"""

        insights = {
            "framework_overview": {
                "name": framework["name"],
                "approach": framework["steps"],
                "domains": framework["domains"],
            },
            "analysis_components": {},
        }

        # Apply each component of the framework
        for component_name, component in framework.get(
            "analysis_components", {}
        ).items():
            component_analysis = {
                "focus_questions": component.get("questions", []),
                "key_considerations": self._generate_component_considerations(
                    component_name, user_input, persona_context
                ),
                "deliverables": component.get("deliverables", []),
                "insights": self._generate_component_insights(
                    component_name, user_input, persona_context
                ),
            }
            insights["analysis_components"][component_name] = component_analysis

        # Add domain-specific patterns
        relevant_patterns = self._get_relevant_patterns(
            framework["domains"], user_input
        )
        insights["applicable_patterns"] = relevant_patterns

        return insights

    def _generate_component_considerations(
        self, component_name: str, user_input: str, persona_context: str
    ) -> List[str]:
        """Generate specific considerations for each framework component"""

        # Base considerations by component type
        component_considerations = {
            "current_state": [
                "Document existing capabilities and constraints honestly",
                "Identify both explicit and implicit dependencies",
                "Assess organizational readiness for change",
            ],
            "stakeholder_mapping": [
                "Include both internal and external stakeholders",
                "Consider varying levels of influence and interest",
                "Plan for stakeholder concerns and resistance",
            ],
            "success_metrics": [
                "Balance leading and lagging indicators",
                "Include both quantitative and qualitative measures",
                "Ensure metrics are actionable and timely",
            ],
            "implementation_roadmap": [
                "Sequence activities to build momentum and credibility",
                "Plan for learning and adaptation opportunities",
                "Balance quick wins with long-term strategic value",
            ],
            "risk_mitigation": [
                "Consider both technical and organizational risks",
                "Plan for various failure modes and recovery options",
                "Maintain flexibility for changing circumstances",
            ],
        }

        base_considerations = component_considerations.get(component_name, [])

        # Add persona-specific considerations
        persona_considerations = {
            "diego": [
                "Focus on building team alignment and enthusiasm",
                "Consider multinational and cross-cultural factors",
                "Emphasize collaborative decision-making approaches",
            ],
            "martin": [
                "Apply proven architectural and engineering principles",
                "Consider long-term evolution and maintainability",
                "Balance theoretical best practices with practical constraints",
            ],
            "rachel": [
                "Prioritize user experience and design thinking approaches",
                "Consider accessibility and inclusive design principles",
                "Focus on user research and validation methods",
            ],
        }

        persona_adds = persona_considerations.get(persona_context, [])

        return base_considerations + persona_adds[:2]  # Limit to avoid overwhelming

    def _generate_component_insights(
        self, component_name: str, user_input: str, persona_context: str
    ) -> List[str]:
        """Generate specific insights for each framework component based on input"""

        input_lower = user_input.lower()

        # Generate contextual insights based on keywords in user input
        insight_templates = {
            "current_state": {
                "platform": "Current platform state requires comprehensive capability assessment",
                "team": "Team structure and dynamics are fundamental to current state analysis",
                "system": "System architecture and technical capabilities define current constraints",
            },
            "stakeholder_mapping": {
                "alignment": "Stakeholder alignment challenges suggest need for influence mapping",
                "communication": "Communication patterns reveal stakeholder relationship dynamics",
                "decision": "Decision-making authority requires clear stakeholder role definition",
            },
            "success_metrics": {
                "quarterly": "Quarterly metrics need both strategic and tactical measurement approaches",
                "performance": "Performance indicators should connect individual and organizational success",
                "value": "Value metrics must demonstrate both immediate and long-term impact",
            },
        }

        # Generate insights based on user input keywords
        insights = []
        component_templates = insight_templates.get(component_name, {})

        for keyword, insight_template in component_templates.items():
            if keyword in input_lower:
                insights.append(insight_template)

        # Add default insights if no specific matches
        if not insights:
            default_insights = {
                "current_state": [
                    "Current state assessment provides foundation for strategic planning",
                    "Understanding constraints enables more effective solution design",
                ],
                "stakeholder_mapping": [
                    "Stakeholder engagement strategy determines implementation success",
                    "Early stakeholder alignment prevents downstream execution challenges",
                ],
                "success_metrics": [
                    "Clear success metrics enable effective progress tracking",
                    "Metrics should motivate desired behaviors and outcomes",
                ],
            }
            insights = default_insights.get(
                component_name,
                ["This component requires careful analysis of context and objectives"],
            )

        return insights[:3]  # Limit insights to avoid overwhelming

    def _get_relevant_patterns(
        self, domains: List[str], user_input: str
    ) -> Dict[str, List[str]]:
        """Get relevant patterns based on framework domains and user input"""

        relevant_patterns = {}

        for domain in domains:
            if domain in self.domain_patterns:
                domain_patterns = self.domain_patterns[domain]

                # Include all patterns for the domain, filtered by relevance
                for pattern_type, patterns in domain_patterns.items():
                    if len(relevant_patterns) < 3:  # Limit total patterns
                        relevant_patterns[f"{domain}_{pattern_type}"] = patterns[:2]

        return relevant_patterns

    def _generate_recommendations(
        self, framework: Dict[str, Any], insights: Dict[str, Any], persona_context: str
    ) -> List[str]:
        """Generate actionable recommendations based on framework analysis"""

        recommendations = []

        # Framework-specific recommendation templates
        framework_name = framework["name"]

        if "Platform Assessment" in framework_name:
            recommendations.extend(
                [
                    "Begin with comprehensive stakeholder alignment to establish shared understanding",
                    "Conduct systematic current state analysis before proposing solutions",
                    "Define success metrics that balance strategic goals with tactical execution",
                    "Create phased implementation plan with clear milestones and decision points",
                ]
            )

        elif "Rumelt Strategy Kernel" in framework_name:
            recommendations.extend(
                [
                    "Start with clear diagnosis: identify the specific challenge and obstacles",
                    "Develop a focused guiding policy - be explicit about what you will NOT do",
                    "Design coherent actions that reinforce each other and the policy",
                    "Actively avoid strategic fluff - test every statement for concrete meaning",
                    "Look for leverage points where small efforts can create big results",
                ]
            )

        elif "WRAP Decision" in framework_name:
            recommendations.extend(
                [
                    "WIDEN: Generate more options using the 'vanishing options test'",
                    "REALITY-TEST: Actively seek evidence that contradicts your assumptions",
                    "ATTAIN DISTANCE: Use 10-10-10 rule (10 minutes, 10 months, 10 years)",
                    "PREPARE TO BE WRONG: Conduct pre-mortem analysis and set tripwires",
                    "Consider opportunity costs - what are you giving up with each option?",
                ]
            )

        elif "Integrated Strategic Decision" in framework_name:
            recommendations.extend(
                [
                    "Apply Rumelt's diagnostic thinking to understand the real challenge",
                    "Use WRAP process to expand and reality-test your options",
                    "Combine strategic diagnosis with rigorous decision-making methodology",
                    "Focus on both the choice quality and implementation coherence",
                ]
            )

        elif "Organizational Transformation" in framework_name:
            recommendations.extend(
                [
                    "Assess organizational change readiness before launching transformation initiatives",
                    "Develop comprehensive communication strategy for all stakeholder groups",
                    "Plan for capability development alongside structural changes",
                    "Establish feedback loops and adaptation mechanisms throughout transformation",
                ]
            )

        elif "Scaling Up Excellence" in framework_name:
            recommendations.extend(
                [
                    "DEFINE EXCELLENCE: Clearly articulate what excellence looks like before scaling",
                    "BUDDHIST vs CATHOLIC: Decide what must be standardized vs. locally adapted",
                    "HOT CAUSES + COOL SOLUTIONS: Combine emotional engagement with practical tools",
                    "CONNECT & CASCADE: Build knowledge sharing bridges across teams and levels",
                    "CUT THEN GROW: Eliminate negative practices before expanding positive ones",
                    "MINDSET OVER FOOTPRINT: Focus on spreading understanding, not just increasing size",
                ]
            )

        elif "Team Topologies" in framework_name:
            recommendations.extend(
                [
                    "ASSESS TEAM TYPES: Identify which teams need stream-aligned, platform, enabling, or complicated subsystem focus",
                    "CONWAY'S LAW: Align team structure with desired architecture using Inverse Conway Maneuver",
                    "COGNITIVE LOAD: Keep teams focused with clear boundaries (5-9 people optimal)",
                    "INTERACTION MODES: Design collaboration, X-as-a-Service, and facilitating patterns",
                    "EVOLUTION STRATEGY: Plan team topology changes with sensing mechanisms and careful transitions",
                ]
            )

        elif "Accelerate" in framework_name:
            recommendations.extend(
                [
                    "MEASURE DORA: Establish baseline for deployment frequency, lead time, failure rate, recovery time",
                    "BUILD CAPABILITIES: Focus on technical (CI/CD), management (empowerment), and cultural (psychological safety)",
                    "OPTIMIZE COMPOSITION: Small autonomous teams (5-9 people) with T-shaped skills and cross-functional capabilities",
                    "PSYCHOLOGICAL SAFETY: Create environment where teams can learn from failures and experiment",
                    "SCIENTIFIC METHOD: Use hypothesis-driven improvement with measurement and learning loops",
                ]
            )

        elif "Crucial Conversations" in framework_name:
            recommendations.extend(
                [
                    "START WITH HEART: Clarify what you really want for yourself, others, and the relationship",
                    "LEARN TO LOOK: Watch for when conversations become crucial and safety is at risk",
                    "MAKE IT SAFE: Establish mutual purpose and demonstrate respect for all perspectives",
                    "MASTER YOUR STORIES: Separate facts from assumptions and test your interpretations",
                    "STATE YOUR PATH: Share facts first, tell your story tentatively, encourage others to share",
                    "EXPLORE OTHERS' PATHS: Ask, mirror, paraphrase, and prime to understand their perspective",
                    "MOVE TO ACTION: Convert dialogue into specific commitments with clear accountability",
                ]
            )

        elif "Capital Allocation" in framework_name:
            recommendations.extend(
                [
                    "ASSESS INVESTMENTS: Comprehensively evaluate all technology investment opportunities",
                    "ALIGN STRATEGICALLY: Ensure every investment contributes to business objectives and stakeholder value",
                    "MEASURE ROI: Quantify both direct returns (cost, revenue, risk) and strategic value (velocity, productivity)",
                    "MANAGE RISKS: Identify technical, market, and organizational risks with mitigation strategies",
                    "OPTIMIZE PORTFOLIO: Balance platform stability, product growth, and innovation exploration dynamically",
                ]
            )

        elif "Technical Strategy" in framework_name:
            recommendations.extend(
                [
                    "Conduct thorough architecture assessment to identify scalability constraints",
                    "Prioritize technical debt reduction based on business impact analysis",
                    "Design evolution roadmap that balances innovation with stability",
                    "Implement quality and governance practices to maintain architectural integrity",
                ]
            )

        elif "Decision Framework" in framework_name:
            recommendations.extend(
                [
                    "Clearly define decision context and constraints before evaluating options",
                    "Generate multiple viable options with explicit trade-off analysis",
                    "Establish clear decision criteria aligned with strategic objectives",
                    "Document decision rationale and assumptions for future reference",
                ]
            )

        # Add persona-specific recommendation style
        if persona_context == "diego":
            recommendations = [
                f"{rec} (Focus on building team consensus and enthusiasm)"
                for rec in recommendations[:3]
            ]
        elif persona_context == "martin":
            recommendations = [
                f"{rec} (Apply proven engineering principles and patterns)"
                for rec in recommendations[:3]
            ]
        elif persona_context == "rachel":
            recommendations = [
                f"{rec} (Consider user experience and inclusive design impact)"
                for rec in recommendations[:3]
            ]

        return recommendations[:4]  # Limit to top 4 recommendations

    def _create_implementation_steps(
        self, framework: Dict[str, Any], insights: Dict[str, Any]
    ) -> List[str]:
        """Create specific implementation steps based on framework and analysis"""

        # Use framework steps as base structure
        base_steps = framework.get("steps", [])

        # Enhance with specific implementation guidance
        implementation_steps = []

        for i, step in enumerate(base_steps, 1):
            enhanced_step = f"**Phase {i}: {step}**"

            # Add specific guidance based on step type
            if "assessment" in step.lower() or "analysis" in step.lower():
                enhanced_step += (
                    " - Gather data, interview stakeholders, document findings"
                )
            elif "mapping" in step.lower():
                enhanced_step += " - Create stakeholder matrix, analyze influence patterns, plan engagement"
            elif "strategy" in step.lower() or "planning" in step.lower():
                enhanced_step += (
                    " - Define objectives, create roadmap, align on priorities"
                )
            elif "implementation" in step.lower() or "roadmap" in step.lower():
                enhanced_step += (
                    " - Sequence activities, assign ownership, establish checkpoints"
                )
            elif "risk" in step.lower():
                enhanced_step += (
                    " - Identify risks, develop mitigation plans, create contingencies"
                )

            implementation_steps.append(enhanced_step)

        return implementation_steps

    def _identify_considerations(
        self,
        framework: Dict[str, Any],
        insights: Dict[str, Any],
        domain_focus: List[str],
    ) -> List[str]:
        """Identify key considerations and potential risks"""

        considerations = []

        # Framework-specific considerations
        framework_name = framework["name"]

        if "strategic" in domain_focus:
            considerations.extend(
                [
                    "Ensure alignment between strategic objectives and tactical execution",
                    "Consider long-term implications of short-term decisions",
                    "Balance innovation aspirations with operational realities",
                ]
            )

        if "organizational" in domain_focus:
            considerations.extend(
                [
                    "Address cultural and change management aspects alongside process changes",
                    "Plan for varying readiness levels across different teams and individuals",
                    "Maintain organizational stability while implementing improvements",
                ]
            )

        if "technical" in domain_focus:
            considerations.extend(
                [
                    "Balance technical best practices with delivery timelines and constraints",
                    "Consider evolution and maintenance implications of architectural decisions",
                    "Plan for technical debt management as ongoing capability",
                ]
            )

        # Add framework-specific risks
        if "Platform Assessment" in framework_name:
            considerations.append(
                "Risk: Analysis paralysis - balance thoroughness with action orientation"
            )
        elif "Transformation" in framework_name:
            considerations.append(
                "Risk: Change fatigue - sequence initiatives to maintain engagement"
            )
        elif "Technical Strategy" in framework_name:
            considerations.append(
                "Risk: Over-engineering - balance ideal architecture with practical constraints"
            )

        return considerations[:5]  # Limit to top 5 considerations

    def _calculate_confidence(
        self, framework: Dict[str, Any], user_input: str, domain_focus: List[str]
    ) -> float:
        """Calculate confidence level for framework application"""

        confidence = 0.5  # Base confidence

        # Increase confidence based on domain alignment
        framework_domains = framework.get("domains", [])
        domain_overlap = len(set(domain_focus) & set(framework_domains))
        confidence += domain_overlap * 0.2

        # Increase confidence based on input clarity and specificity
        input_words = len(user_input.split())
        if input_words > 10:  # More detailed input
            confidence += 0.1
        if input_words > 20:  # Very detailed input
            confidence += 0.1

        # Framework-specific confidence adjustments
        if "strategic" in domain_focus and "Strategic" in framework["name"]:
            confidence += 0.1

        return min(confidence, 0.95)  # Cap at 95% confidence


class EmbeddedPersonaIntegrator:
    """
    Integrates embedded framework analysis with persona personalities.

    Maintains the same persona integration patterns as MCP version
    but works with embedded framework analysis.
    """

    def __init__(self, framework_engine: EmbeddedFrameworkEngine):
        self.framework_engine = framework_engine

        # Persona integration patterns from original MCP version
        self.persona_filters = {
            "diego": {
                "voice_characteristics": [
                    "warm and engaging",
                    "collaborative",
                    "multinational perspective",
                    "emotionally intelligent",
                    "pragmatic",
                    "solution-focused",
                ],
                "communication_patterns": {
                    "opening_style": [
                        "Great to connect!",
                        "I'm excited about this challenge",
                        "Let's dive into this",
                    ],
                    "transition_phrases": [
                        "Here's what I'm thinking",
                        "From my experience",
                        "Let me share what's worked",
                    ],
                    "analytical_markers": [
                        "Looking at this systematically",
                        "Breaking this down",
                        "Here's the framework I'd use",
                    ],
                    "personal_touches": [
                        "😊",
                        "What's your gut feeling?",
                        "Let's get real about this",
                    ],
                    "closure_style": [
                        "What resonates most?",
                        "How does this land?",
                        "Let's build on this together",
                    ],
                },
                "systematic_integration": {
                    "prefix_patterns": [
                        "Let me work through this systematically...",
                        "I've been thinking about frameworks for this...",
                        "Here's how I'd approach this step-by-step...",
                    ],
                    "framework_intro": [
                        "Using proven strategic planning approaches...",
                        "Drawing from organizational analysis frameworks...",
                        "Following systematic methodology...",
                    ],
                    "analysis_wrapping": [
                        "What this analysis tells us is...",
                        "The systematic approach suggests...",
                        "Based on this framework...",
                    ],
                },
            },
            "martin": {
                "voice_characteristics": [
                    "thoughtful",
                    "measured",
                    "precise",
                    "pattern-focused",
                    "evolutionary thinking",
                    "principled",
                ],
                "communication_patterns": {
                    "opening_style": [
                        "Let me think about this",
                        "There's an interesting pattern here",
                        "This reminds me of",
                    ],
                    "analytical_markers": [
                        "The trade-offs are",
                        "Evolutionarily",
                        "From an architectural perspective",
                    ],
                    "framework_integration": [
                        "This follows the pattern of",
                        "Using established principles",
                        "The framework suggests",
                    ],
                },
            },
            "rachel": {
                "voice_characteristics": [
                    "collaborative",
                    "user-centered",
                    "systems thinking",
                    "inclusive",
                    "practical",
                    "empathetic",
                ],
                "communication_patterns": {
                    "opening_style": [
                        "Let's think about the user experience",
                        "I love where this is going",
                        "How does this feel for teams?",
                    ],
                    "framework_integration": [
                        "Design systems research shows",
                        "User-centered frameworks suggest",
                        "Cross-team patterns indicate",
                    ],
                },
            },
        }

    def create_systematic_response(
        self,
        persona_name: str,
        user_input: str,
        base_response: str,
        domain_focus: List[str],
        complexity_level: str = "complex",
    ) -> SystematicResponse:
        """
        Create persona-integrated systematic response using embedded frameworks.

        Provides the same enhanced response quality as MCP integration
        but with zero external dependencies.
        """
        start_time = time.time()

        # Apply embedded framework analysis
        framework_analysis = self.framework_engine.analyze_systematically(
            user_input=user_input,
            persona_context=persona_name,
            domain_focus=domain_focus,
            complexity_level=complexity_level,
        )

        # Integrate with persona personality
        persona_response = self._integrate_with_persona(
            persona_name, user_input, framework_analysis
        )

        processing_time = int((time.time() - start_time) * 1000)

        return SystematicResponse(
            analysis=framework_analysis,
            persona_integrated_response=persona_response,
            processing_time_ms=processing_time,
            framework_applied=framework_analysis.framework_name,
        )

    def _integrate_with_persona(
        self, persona_name: str, user_input: str, analysis: FrameworkAnalysis
    ) -> str:
        """Integrate framework analysis with persona personality"""

        persona_filter = self.persona_filters.get(persona_name, {})

        if persona_name == "diego":
            return self._integrate_diego_response(user_input, analysis, persona_filter)
        elif persona_name == "martin":
            return self._integrate_martin_response(user_input, analysis, persona_filter)
        elif persona_name == "rachel":
            return self._integrate_rachel_response(user_input, analysis, persona_filter)
        else:
            return self._integrate_generic_response(user_input, analysis)

    def _integrate_diego_response(
        self,
        user_input: str,
        analysis: FrameworkAnalysis,
        persona_filter: Dict[str, Any],
    ) -> str:
        """Integrate systematic analysis with Diego's warm, collaborative personality"""

        patterns = persona_filter.get("communication_patterns", {})
        systematic = persona_filter.get("systematic_integration", {})

        response_parts = []

        # Diego's warm opening
        opening = self._select_pattern(
            patterns.get("opening_style", ["Great question!"])
        )
        response_parts.append(f"{opening} {self._add_diego_energy()}")

        # Introduce systematic approach naturally
        systematic_intro = self._select_pattern(
            systematic.get(
                "prefix_patterns", ["Let me work through this systematically..."]
            )
        )
        response_parts.append(systematic_intro)

        # Present framework with Diego's collaborative style
        framework_intro = self._select_pattern(
            systematic.get("framework_intro", ["Using proven strategic approaches..."])
        )
        response_parts.append(f"{framework_intro}")
        response_parts.append(
            f"I'm drawing from **{analysis.framework_name}** here - it's been really effective for similar challenges."
        )

        # Add systematic analysis with Diego's warmth
        if analysis.structured_insights:
            analysis_intro = self._select_pattern(
                systematic.get(
                    "analysis_wrapping", ["What this analysis tells us is..."]
                )
            )
            response_parts.append(f"{analysis_intro}")

            # Format key insights with Diego's collaborative perspective
            insights_content = self._format_insights_for_diego(
                analysis.structured_insights
            )
            response_parts.append(insights_content)

        # Add recommendations with Diego's pragmatic style
        if analysis.recommendations:
            response_parts.append("\n**Here's how I'd move forward:**")
            recommendations_content = self._format_recommendations_for_diego(
                analysis.recommendations
            )
            response_parts.append(recommendations_content)

        # Add implementation steps if provided
        if analysis.implementation_steps:
            response_parts.append("\n**Step-by-step approach:**")
            for step in analysis.implementation_steps:
                response_parts.append(f"• {step}")

        # Diego's engaging closure
        closure = self._select_pattern(
            patterns.get("closure_style", ["What resonates most?"])
        )
        response_parts.append(f"\n{closure} {self._add_diego_personal_touch()}")

        return "\n\n".join(response_parts)

    def _integrate_martin_response(
        self,
        user_input: str,
        analysis: FrameworkAnalysis,
        persona_filter: Dict[str, Any],
    ) -> str:
        """Integrate framework analysis with Martin's thoughtful, architectural perspective"""

        patterns = persona_filter.get("communication_patterns", {})

        response_parts = []

        # Martin's thoughtful opening
        opening = self._select_pattern(
            patterns.get("opening_style", ["Let me think about this..."])
        )
        response_parts.append(opening)

        # Present framework with Martin's architectural lens
        framework_intro = self._select_pattern(
            patterns.get(
                "framework_integration", ["This follows established principles..."]
            )
        )
        response_parts.append(f"{framework_intro}")
        response_parts.append(
            f"The **{analysis.framework_name}** provides a structured approach to this challenge."
        )

        # Martin's analytical breakdown
        if analysis.structured_insights:
            response_parts.append(
                "From an architectural perspective, the key components are:"
            )
            insights_content = self._format_insights_for_martin(
                analysis.structured_insights
            )
            response_parts.append(insights_content)

        # Martin's trade-off analysis
        if analysis.key_considerations:
            response_parts.append("**The trade-offs to consider:**")
            for consideration in analysis.key_considerations:
                response_parts.append(f"• {consideration}")

        # Implementation approach with Martin's evolutionary thinking
        if analysis.implementation_steps:
            response_parts.append("\n**Evolutionary implementation approach:**")
            for i, step in enumerate(analysis.implementation_steps, 1):
                response_parts.append(f"{i}. {step}")
                if i == 1:
                    response_parts.append(
                        "   *Start here to establish foundation and validate approach*"
                    )

        return "\n\n".join(response_parts)

    def _integrate_rachel_response(
        self,
        user_input: str,
        analysis: FrameworkAnalysis,
        persona_filter: Dict[str, Any],
    ) -> str:
        """Integrate framework analysis with Rachel's collaborative, user-centered approach"""

        patterns = persona_filter.get("communication_patterns", {})

        response_parts = []

        # Rachel's collaborative opening
        opening = self._select_pattern(
            patterns.get("opening_style", ["Let's think about this together..."])
        )
        response_parts.append(opening)

        # Present framework with user experience focus
        framework_intro = self._select_pattern(
            patterns.get(
                "framework_integration", ["User-centered frameworks suggest..."]
            )
        )
        response_parts.append(f"{framework_intro}")
        response_parts.append(
            f"The **{analysis.framework_name}** helps us think systematically about the user experience implications."
        )

        # Focus on user and team impact
        if analysis.structured_insights:
            response_parts.append("**From a user experience perspective:**")
            insights_content = self._format_insights_for_rachel(
                analysis.structured_insights
            )
            response_parts.append(insights_content)

        # Rachel's inclusive approach to recommendations
        if analysis.recommendations:
            response_parts.append("\n**Inclusive approach to implementation:**")
            for i, rec in enumerate(analysis.recommendations, 1):
                response_parts.append(f"{i}. {rec}")
                if i == 1:
                    response_parts.append(
                        "   *This builds trust and psychological safety*"
                    )

        # Consider accessibility and inclusive design
        response_parts.append("\n**Don't forget to consider:**")
        response_parts.append(
            "• How does this impact different user groups and accessibility needs?"
        )
        response_parts.append(
            "• What feedback loops will help us validate our approach?"
        )
        response_parts.append(
            "• How do we ensure inclusive participation in the process?"
        )

        return "\n\n".join(response_parts)

    def _integrate_generic_response(
        self, user_input: str, analysis: FrameworkAnalysis
    ) -> str:
        """Generic integration for personas without specific filters"""

        response_parts = []

        response_parts.append("Let me provide a systematic analysis of this challenge.")
        response_parts.append(f"Using the **{analysis.framework_name}**:")

        if analysis.structured_insights:
            response_parts.append("**Key insights:**")
            for component, insights in analysis.structured_insights.get(
                "analysis_components", {}
            ).items():
                if insights.get("insights"):
                    response_parts.append(
                        f"• {component.replace('_', ' ').title()}: {insights['insights'][0]}"
                    )

        if analysis.recommendations:
            response_parts.append("\n**Recommendations:**")
            for i, rec in enumerate(analysis.recommendations, 1):
                response_parts.append(f"{i}. {rec}")

        return "\n\n".join(response_parts)

    # Helper methods for persona-specific formatting

    def _select_pattern(self, patterns: List[str]) -> str:
        """Select pattern from list (deterministic for consistency)"""
        if not patterns:
            return ""
        return patterns[0]  # Use first pattern for consistency

    def _add_diego_energy(self) -> str:
        """Add Diego's characteristic energy markers"""
        return "😊"

    def _add_diego_personal_touch(self) -> str:
        """Add Diego's personal connection style"""
        return "I'd love to hear your thoughts on this approach."

    def _format_insights_for_diego(self, insights: Dict[str, Any]) -> str:
        """Format insights with Diego's collaborative interpretation"""
        parts = []

        # Extract key insights from analysis components
        components = insights.get("analysis_components", {})
        for component_name, component_data in components.items():
            component_insights = component_data.get("insights", [])
            if component_insights:
                component_title = component_name.replace("_", " ").title()
                parts.append(f"• **{component_title}**: {component_insights[0]}")

        return (
            "\n".join(parts)
            if parts
            else "Key insights emerging from this systematic analysis..."
        )

    def _format_recommendations_for_diego(self, recommendations: List[str]) -> str:
        """Format recommendations with Diego's action-oriented, supportive style"""
        parts = []
        for i, rec in enumerate(recommendations, 1):
            parts.append(f"{i}. {rec}")
            if i == 1:
                parts.append(
                    "   (I'd start here - builds confidence and shows early value)"
                )
            elif i == len(recommendations):
                parts.append("   (This is where the real transformation happens)")

        return "\n".join(parts)

    def _format_insights_for_martin(self, insights: Dict[str, Any]) -> str:
        """Format insights with Martin's architectural perspective"""
        parts = []

        components = insights.get("analysis_components", {})
        for component_name, component_data in components.items():
            considerations = component_data.get("key_considerations", [])
            if considerations:
                component_title = component_name.replace("_", " ").title()
                parts.append(f"• **{component_title}**: {considerations[0]}")

        return (
            "\n".join(parts)
            if parts
            else "Architectural components require systematic analysis..."
        )

    def _format_insights_for_rachel(self, insights: Dict[str, Any]) -> str:
        """Format insights with Rachel's user-centered approach"""
        parts = []

        components = insights.get("analysis_components", {})
        for component_name, component_data in components.items():
            if "stakeholder" in component_name or "communication" in component_name:
                component_insights = component_data.get("insights", [])
                if component_insights:
                    component_title = component_name.replace("_", " ").title()
                    parts.append(
                        f"• **{component_title}**: {component_insights[0]} (Consider user impact)"
                    )

        if not parts:
            parts.append(
                "• User experience considerations are central to successful implementation"
            )
            parts.append(
                "• Cross-team collaboration patterns will determine adoption success"
            )

        return "\n".join(parts)
