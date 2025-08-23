"""
Framework Definitions - Static Framework Data
===========================================

Static framework definitions to avoid circular dependencies.
These definitions are used by both the legacy and refactored framework engines.

Author: Martin | Platform Architecture
Purpose: Eliminate circular dependency in framework provider initialization
"""

from typing import Dict, Any, List


def get_strategic_frameworks() -> Dict[str, Any]:
    """Get strategic framework definitions without creating engine instances"""
    return {
        "Team Topologies": {
            "description": "Optimal team structure and cognitive load management",
            "keywords": [
                "team",
                "topology",
                "cognitive load",
                "conway",
                "stream",
                "organizational",
                "structure",
            ],
            "confidence_threshold": 0.7,
            "implementation_steps": [
                "Assess current team structure",
                "Identify cognitive load bottlenecks",
                "Design stream-aligned teams",
                "Implement platform teams",
                "Establish enabling teams",
            ],
            "key_considerations": [
                "Team cognitive load limits",
                "Conway's Law implications",
                "Stream alignment priorities",
            ],
            "analysis_components": {
                "team_structure": {
                    "questions": [
                        "How are teams organized?",
                        "What is the cognitive load?",
                    ]
                },
                "communication_patterns": {
                    "questions": [
                        "How do teams communicate?",
                        "What are the interfaces?",
                    ]
                },
            },
        },
        "Good Strategy Bad Strategy": {
            "description": "Strategy kernel development and fluff detection",
            "keywords": [
                "strategy",
                "kernel",
                "diagnosis",
                "guiding policy",
                "coherent action",
                "strategic",
            ],
            "confidence_threshold": 0.7,
            "implementation_steps": [
                "Develop clear diagnosis",
                "Define guiding policy",
                "Create coherent actions",
                "Eliminate strategy fluff",
            ],
            "key_considerations": [
                "Clear problem diagnosis",
                "Coherent action alignment",
                "Strategy vs tactics distinction",
            ],
            "analysis_components": {
                "diagnosis": {
                    "questions": [
                        "What is the core problem?",
                        "What are the root causes?",
                    ]
                },
                "guiding_policy": {
                    "questions": ["What is the approach?", "What are the constraints?"]
                },
            },
        },
        "Capital Allocation Framework": {
            "description": "Engineering resource investment and ROI analysis",
            "keywords": [
                "capital",
                "allocation",
                "investment",
                "roi",
                "resource",
                "budget",
                "financial",
            ],
            "confidence_threshold": 0.7,
            "implementation_steps": [
                "Assess current resource allocation",
                "Calculate platform vs feature ROI",
                "Optimize investment portfolio",
                "Track allocation effectiveness",
            ],
            "key_considerations": [
                "Platform investment ROI",
                "Feature development balance",
                "Long-term vs short-term trade-offs",
            ],
            "analysis_components": {
                "investment_analysis": {
                    "questions": ["What is the ROI?", "What are the costs?"]
                },
                "resource_optimization": {
                    "questions": ["How to optimize allocation?", "What are priorities?"]
                },
            },
        },
        "Crucial Conversations": {
            "description": "High-stakes discussions and stakeholder alignment",
            "keywords": [
                "conversation",
                "stakeholder",
                "alignment",
                "conflict",
                "crucial",
                "communication",
            ],
            "confidence_threshold": 0.7,
            "implementation_steps": [
                "Create psychological safety",
                "Share facts and stories",
                "Ask for others' paths",
                "Talk tentatively",
                "Encourage testing",
            ],
            "key_considerations": [
                "Emotional safety requirements",
                "Fact vs story separation",
                "Mutual respect maintenance",
            ],
            "analysis_components": {
                "safety_creation": {
                    "questions": ["How to create safety?", "What are the risks?"]
                },
                "dialogue_management": {
                    "questions": [
                        "How to share perspectives?",
                        "How to encourage input?",
                    ]
                },
            },
        },
        "Strategic Platform Assessment": {
            "description": "Platform maturity and investment evaluation",
            "keywords": [
                "platform",
                "assessment",
                "maturity",
                "strategic",
                "evaluation",
                "adoption",
            ],
            "confidence_threshold": 0.8,
            "implementation_steps": [
                "Assess platform maturity",
                "Evaluate strategic alignment",
                "Calculate investment ROI",
                "Define improvement roadmap",
            ],
            "key_considerations": [
                "Platform adoption metrics",
                "Strategic business alignment",
                "Investment vs benefit analysis",
            ],
            "analysis_components": {
                "maturity_assessment": {
                    "questions": ["What is the current maturity?", "What are the gaps?"]
                },
                "strategic_alignment": {
                    "questions": [
                        "How does it align with strategy?",
                        "What is the business value?",
                    ]
                },
            },
        },
    }


def get_framework_patterns() -> Dict[str, List[str]]:
    """Get framework detection patterns"""
    frameworks = get_strategic_frameworks()
    return {name: data["patterns"] for name, data in frameworks.items()}


def get_framework_thresholds() -> Dict[str, float]:
    """Get framework confidence thresholds"""
    frameworks = get_strategic_frameworks()
    return {name: data["confidence_threshold"] for name, data in frameworks.items()}
