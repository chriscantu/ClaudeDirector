# Strategic Framework Engine API

## Overview

The Strategic Framework Engine provides access to 7 research-backed strategic frameworks integrated into ClaudeDirector. These frameworks automatically activate based on context analysis and provide specific guidance for engineering leadership challenges.

## Core Framework Engine

### EmbeddedFrameworkEngine

```python
from claudedirector.core.embedded_framework_engine import EmbeddedFrameworkEngine

# Initialize the framework engine
framework_engine = EmbeddedFrameworkEngine()

# Analyze strategic context and get framework recommendations
result = framework_engine.analyze_strategic_context(
    user_input="We need to decide on our platform architecture strategy"
)
```

### Analysis Result Structure

```python
{
    "activated_frameworks": ["Rumelt Strategy Kernel", "Decisive WRAP Decision Framework"],
    "primary_framework": "Rumelt Strategy Kernel",
    "confidence_score": 0.89,
    "recommendations": [
        "Apply strategy kernel diagnostic: Does this have a clear strategic logic?",
        "Use WRAP process: Widen options, Reality-test assumptions, Attain distance, Prepare to be wrong"
    ],
    "framework_specific_guidance": {
        "rumelt": {
            "diagnostic_questions": ["What is the strategic logic?", "What are the coherent actions?"],
            "kernel_elements": ["diagnosis", "guiding_policy", "coherent_actions"]
        },
        "wrap": {
            "process_steps": ["Widen your options", "Reality-test assumptions", "Attain distance", "Prepare to be wrong"],
            "decision_techniques": ["Consider the opposite", "10-10-10 rule", "Pre-mortem analysis"]
        }
    }
}
```

## Available Strategic Frameworks

### 1. Rumelt Strategy Kernel
**Source**: "Good Strategy Bad Strategy" by Richard Rumelt  
**Purpose**: Strategic analysis and formulation

```python
# Activates on: strategy, strategic planning, competitive advantage
result = framework_engine.analyze_strategic_context(
    "How should we position our platform against competitors?"
)

# Provides:
# - Diagnostic questions for strategy clarity
# - Kernel elements (diagnosis, guiding policy, coherent actions)
# - Strategic logic validation
```

**Key Components**:
- **Diagnosis**: Understanding the challenge
- **Guiding Policy**: Overall approach to dealing with the challenge  
- **Coherent Actions**: Coordinated steps to implement the policy

### 2. Decisive WRAP Decision Framework
**Source**: "Decisive" by Chip Heath and Dan Heath  
**Purpose**: Better decision-making process

```python
# Activates on: decision, choice, options, evaluate
result = framework_engine.analyze_strategic_context(
    "Should we build in-house or buy a third-party solution?"
)

# Provides:
# - WRAP process steps
# - Decision-making techniques
# - Bias mitigation strategies
```

**WRAP Process**:
- **W**iden your options
- **R**eality-test your assumptions  
- **A**ttain distance before deciding
- **P**repare to be wrong

### 3. Scaling Up Excellence  
**Source**: "Scaling Up Excellence" by Bob Sutton and Huggy Rao  
**Purpose**: Organizational scaling and excellence propagation

```python
# Activates on: scaling, growth, organizational change, team expansion
result = framework_engine.analyze_strategic_context(
    "How do we scale our engineering practices across the organization?"
)

# Provides:
# - Scaling strategies
# - Excellence propagation techniques
# - Change management guidance
```

### 4. Team Topologies
**Source**: "Team Topologies" by Matthew Skelton and Manuel Pais  
**Purpose**: Team structure and communication optimization

```python
# Activates on: team structure, communication, organizational design
result = framework_engine.analyze_strategic_context(
    "How should we organize our engineering teams for better delivery?"
)

# Provides:
# - Team topology patterns
# - Communication flow optimization
# - Conway's Law considerations
```

**Team Types**:
- Stream-aligned teams
- Enabling teams  
- Complicated-subsystem teams
- Platform teams

### 5. Accelerate Team Performance
**Source**: "Accelerate" by Nicole Forsgren, Jez Humble, and Gene Kim  
**Purpose**: High-performing team practices

```python
# Activates on: performance, delivery, devops, team effectiveness
result = framework_engine.analyze_strategic_context(
    "How can we improve our team's delivery performance?"
)

# Provides:
# - Key performance metrics
# - Practices for high performance
# - Transformation guidance
```

### 6. Crucial Conversations
**Source**: "Crucial Conversations" by Patterson, Grenny, McMillan, Switzler  
**Purpose**: Stakeholder communication and difficult conversations

```python
# Activates on: stakeholder, communication, conflict, negotiation
result = framework_engine.analyze_strategic_context(
    "How do I handle disagreement with senior stakeholders about priorities?"
)

# Provides:
# - Conversation techniques
# - Stakeholder management strategies
# - Conflict resolution approaches
```

### 7. Capital Allocation Framework
**Source**: Strategic resource allocation principles  
**Purpose**: Strategic investment and resource allocation decisions

```python
# Activates on: budget, investment, resource allocation, ROI
result = framework_engine.analyze_strategic_context(
    "How should we allocate our engineering budget across initiatives?"
)

# Provides:
# - Investment evaluation criteria
# - Resource allocation strategies
# - ROI analysis frameworks
```

## Framework Activation Logic

### Keyword-Based Activation
Each framework has specific keywords that trigger activation:

```python
# Examples of activation keywords:
{
    "rumelt": ["strategy", "competitive", "strategic planning", "market position"],
    "wrap": ["decision", "choice", "evaluate", "options", "decide"],
    "scaling": ["scale", "growth", "expand", "organizational change"],
    "team_topologies": ["team structure", "communication", "organizational design"],
    "accelerate": ["performance", "delivery", "devops", "metrics"],
    "crucial_conversations": ["stakeholder", "communication", "conflict"],
    "capital_allocation": ["budget", "investment", "resource allocation"]
}
```

### Multi-Framework Activation
The engine can activate multiple frameworks simultaneously when context overlaps:

```python
# Complex scenario activating multiple frameworks
result = framework_engine.analyze_strategic_context("""
    We need to make a strategic decision about scaling our platform team 
    while managing stakeholder expectations and budget constraints.
""")

# May activate: Rumelt Strategy + Team Topologies + Crucial Conversations + Capital Allocation
```

## Persona Integration

### Framework-Aware Personas
Strategic personas automatically incorporate framework guidance:

```python
# Personas that leverage frameworks:
- diego: Engineering leadership (Team Topologies, Accelerate)
- alvaro: Business strategy (Rumelt, Capital Allocation)  
- rachel: Design systems strategy (Scaling Up Excellence)
- camille: Executive strategy (Rumelt, Crucial Conversations)
```

## Advanced Usage

### Context-Rich Analysis
Provide detailed context for better framework selection:

```python
context = """
Context: Engineering leadership role in a growing startup
Challenge: Platform team of 8 needs to scale to support 3 new product lines
Constraints: Limited budget, tight timeline, need to maintain quality
Stakeholders: CTO, Product VPs, Engineering managers
"""

result = framework_engine.analyze_strategic_context(context)
```

### Framework-Specific Guidance Access
Get detailed guidance from specific frameworks:

```python
result = framework_engine.analyze_strategic_context(user_input)

# Access specific framework guidance
if "Team Topologies" in result['activated_frameworks']:
    team_guidance = result['framework_specific_guidance']['team_topologies']
    for pattern in team_guidance['topology_patterns']:
        print(f"Consider: {pattern}")

if "Rumelt Strategy Kernel" in result['activated_frameworks']:
    strategy_guidance = result['framework_specific_guidance']['rumelt']
    for question in strategy_guidance['diagnostic_questions']:
        print(f"Ask: {question}")
```

### Custom Framework Configuration
Configure framework sensitivity and activation thresholds:

```python
# Custom configuration (advanced usage)
framework_engine = EmbeddedFrameworkEngine(
    activation_threshold=0.7,  # Default: 0.6
    max_frameworks=3,          # Default: 5
    prefer_primary=True        # Focus on highest-confidence framework
)
```

## Error Handling

### Framework Analysis Errors
```python
from claudedirector.core.exceptions import FrameworkAnalysisError

try:
    result = framework_engine.analyze_strategic_context(user_input)
except FrameworkAnalysisError as e:
    print(f"Framework analysis failed: {e}")
    # Fallback to basic strategic guidance
```

### Input Validation
```python
# The engine validates input and provides meaningful errors
try:
    result = framework_engine.analyze_strategic_context("")  # Empty input
except ValueError as e:
    print(f"Invalid input: {e}")
```

## Performance Considerations

### Caching
Framework analysis results are cached for improved performance:

```python
# First analysis: ~200ms
result1 = framework_engine.analyze_strategic_context(context)

# Subsequent identical analysis: ~10ms (cached)
result2 = framework_engine.analyze_strategic_context(context)
```

### Batch Analysis
For multiple strategic contexts:

```python
contexts = [
    "Strategic decision about platform architecture",
    "Team scaling challenges",
    "Stakeholder communication issues"
]

# Batch process for efficiency
results = []
for context in contexts:
    result = framework_engine.analyze_strategic_context(context)
    results.append(result)
```

## Integration Examples

### With Strategic Planning
```python
# Integrate framework engine in strategic planning sessions
planning_context = """
Q3 Engineering Strategy Planning:
- Scale platform team from 8 to 15 people
- Launch 2 new product integrations  
- Improve deployment frequency by 50%
- Manage increased stakeholder expectations
"""

result = framework_engine.analyze_strategic_context(planning_context)

# Generate structured planning output
for framework in result['activated_frameworks']:
    print(f"\n{framework} Guidance:")
    guidance = result['framework_specific_guidance'][framework.lower().replace(' ', '_')]
    # Process framework-specific guidance
```

### With Decision Support
```python
# Use for critical engineering decisions
decision_context = """
Decision: Should we migrate to microservices architecture?
Factors: Team size (25 engineers), complexity growing, deployment bottlenecks
Timeline: 6-month window available
Stakeholders: Engineering, Product, Executive team
"""

result = framework_engine.analyze_strategic_context(decision_context)

if "Decisive WRAP Decision Framework" in result['activated_frameworks']:
    wrap_steps = result['framework_specific_guidance']['wrap']['process_steps']
    print("WRAP Decision Process:")
    for i, step in enumerate(wrap_steps, 1):
        print(f"{i}. {step}")
```

---

**Note**: Framework activations are dynamic and context-dependent. The engine continuously learns from usage patterns to improve framework selection accuracy.
