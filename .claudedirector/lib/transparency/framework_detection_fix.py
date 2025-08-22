"""
Quick fix to add common strategic framework patterns to framework detection
"""


def get_updated_framework_patterns():
    """Return updated framework patterns including common strategic frameworks"""

    return {
        # Add common strategic frameworks that were missing
        "OGSM Strategic Framework": {
            "patterns": [
                "ogsm",
                "ogsm strategic framework",
                "ogsm framework",
                "objectives goals strategies measures",
                "ogsm analysis",
                "ogsm planning",
            ],
            "type": "strategic",
            "confidence_weight": 0.9,
        },
        "Blue Ocean Strategy": {
            "patterns": [
                "blue ocean strategy",
                "blue ocean",
                "uncontested market space",
                "value innovation",
                "strategy canvas",
                "four actions framework",
                "blue ocean approach",
            ],
            "type": "strategic",
            "confidence_weight": 0.9,
        },
        "Design Thinking": {
            "patterns": [
                "design thinking",
                "design thinking process",
                "design thinking methodology",
                "empathize define ideate prototype test",
                "human-centered design",
                "design thinking framework",
            ],
            "type": "innovation",
            "confidence_weight": 0.9,
        },
        "Porter's Five Forces": {
            "patterns": [
                "porter's five forces",
                "five forces analysis",
                "competitive forces",
                "porter five forces",
                "competitive analysis framework",
                "industry analysis",
            ],
            "type": "strategic",
            "confidence_weight": 0.9,
        },
        "BCG Matrix": {
            "patterns": [
                "bcg matrix",
                "boston consulting group matrix",
                "stars cash cows dogs question marks",
                "bcg growth share matrix",
                "portfolio analysis",
                "question mark products",
            ],
            "type": "strategic",
            "confidence_weight": 0.8,
        },
        "Jobs-to-be-Done": {
            "patterns": [
                "jobs-to-be-done",
                "jobs to be done",
                "jtbd framework",
                "customer jobs",
                "jobs-to-be-done framework",
                "job story",
            ],
            "type": "innovation",
            "confidence_weight": 0.8,
        },
        "Lean Startup": {
            "patterns": [
                "lean startup",
                "lean startup methodology",
                "minimum viable product",
                "mvp development",
                "build measure learn",
                "validated learning",
            ],
            "type": "innovation",
            "confidence_weight": 0.8,
        },
        # Keep existing patterns
        "Sequential": {
            "patterns": [
                "sequential server",
                "systematic analysis",
                "strategic framework analysis",
                "systematic strategic analysis",
                "sequential methodology",
                "strategic analysis framework",
            ],
            "type": "strategic",
            "confidence_weight": 0.9,
        },
        "Context7": {
            "patterns": [
                "context7 server",
                "proven patterns",
                "architectural patterns",
                "design system methodology",
                "established architectural patterns",
                "context7 framework",
                "proven architectural methodologies",
            ],
            "type": "architectural_patterns",
            "confidence_weight": 0.9,
        },
        # Add more common frameworks
        "OKRs": {
            "patterns": [
                "okr",
                "okrs",
                "objectives and key results",
                "objective key results",
                "okr framework",
                "quarterly objectives",
            ],
            "type": "strategic",
            "confidence_weight": 0.8,
        },
        "SWOT Analysis": {
            "patterns": [
                "swot analysis",
                "swot framework",
                "strengths weaknesses opportunities threats",
                "swot matrix",
                "internal external analysis",
            ],
            "type": "strategic",
            "confidence_weight": 0.8,
        },
    }
