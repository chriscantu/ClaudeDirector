# WRAP Decision Framework

**Heath Brothers' systematic methodology for making better strategic decisions.**

---

## ⚖️ **Framework Overview**

**Source**: "Decisive" by Heath Brothers
**Application**: Strategic decision-making, option evaluation, reducing decision bias
**Persona Alignment**: All personas for major decisions, especially Camille and Diego

### **When This Framework Activates**
- Major strategic decisions (technology adoption, organizational changes)
- Investment decisions (platform vs feature trade-offs)
- Architectural decisions with significant long-term impact
- Team structure and process decisions
- Vendor and technology selection

## 🧩 **The WRAP Framework**

### **Core Principle**
Most decisions fail due to four predictable biases. WRAP provides a systematic process to overcome these biases and make better strategic decisions.

### **The Four-Step Process**

#### **1. 🔍 Widen Your Options**
**Problem**: Narrow framing - considering too few alternatives
**Solution**: Deliberately generate more options before deciding

**Techniques**:
- **Vanishing Options Test**: "If your current options disappeared, what would you do?"
- **Opportunity Cost**: "If I did not have this option, how else could I spend this money/time?"
- **Find Someone Who's Solved Your Problem**: Look for analogous solutions in other domains
- **Consider Simultaneous Options**: "Can we do both?" or "Can we test multiple approaches?"

**Strategic Questions**:
- "What other options should we consider?"
- "Who has faced a similar challenge successfully?"
- "What would we do if our preferred option wasn't available?"
- "Can we find a way to pursue multiple options simultaneously?"

**Example Application**:
```
Platform Architecture Decision:
Initial framing: "Should we build microservices or stick with monolith?"

Widened options:
- Modular monolith with clear service boundaries
- Gradual extraction of specific services only
- Event-driven architecture with selective decomposition
- Hybrid approach: monolith for stable features, services for scaling needs
- Buy vs build analysis for platform components
```

#### **2. 🧪 Reality-Test Your Assumptions**
**Problem**: Confirmation bias - seeking information that confirms our preferences
**Solution**: Actively test key assumptions and seek disconfirming evidence

**Techniques**:
- **Devil's Advocate**: "What are the strongest arguments against this option?"
- **Pre-mortem Analysis**: "If this decision failed, what would be the most likely reasons?"
- **Small Experiments**: "How can we test this on a small scale first?"
- **Outside View**: "What do people with no stake in this decision think?"

**Strategic Questions**:
- "What assumptions is this decision based on?"
- "What evidence would prove this option wrong?"
- "How can we test this cheaply before committing fully?"
- "What do external experts think about this approach?"

**Example Application**:
```
Platform Adoption Strategy:
Assumption: "Teams will adopt our platform if we build better features"

Reality tests:
- Interview 5 teams about real adoption barriers
- Survey current platform users about satisfaction vs usage
- A/B test: improved features vs improved documentation
- Analyze adoption patterns: what correlates with success?
- Shadow teams during platform integration attempts
```

#### **3. ⏰ Attain Distance Before Deciding**
**Problem**: Temporary emotions cloud judgment
**Solution**: Gain perspective through time, distance, and values clarification

**Techniques**:
- **10-10-10 Rule**: "How will I feel about this in 10 minutes, 10 months, 10 years?"
- **Core Values Test**: "Does this align with our organizational/technical values?"
- **Sleep On It**: Allow time for emotional distance from immediate pressures
- **Zoom Out**: "What would someone watching from the outside recommend?"

**Strategic Questions**:
- "How will this decision look in 6 months? 2 years?"
- "What are our core values, and how does this align?"
- "What would I recommend to someone else facing this decision?"
- "Am I being influenced by temporary pressures or emotions?"

**Example Application**:
```
Team Restructuring Decision:
Immediate pressure: "We need to reorganize immediately due to project delays"

Distance perspectives:
- 10 months: Will this team structure still make sense after current project?
- 2 years: Does this align with our platform scaling roadmap?
- Core values: Does this support our principles of team autonomy and ownership?
- Outside view: What would a consultant with no emotional investment recommend?
```

#### **4. 🛡️ Prepare to Be Wrong**
**Problem**: Overconfidence in our predictions
**Solution**: Plan for multiple scenarios and build in flexibility

**Techniques**:
- **Scenario Planning**: "What if our assumptions are wrong?"
- **Reversible Decisions**: "How can we make this decision reversible?"
- **Tripwires**: "What signals would indicate we need to change course?"
- **Options Thinking**: "How can we maintain flexibility as we learn more?"

**Strategic Questions**:
- "What would we do if this doesn't work as expected?"
- "How can we make this decision reversible or adjustable?"
- "What early warning signs should we watch for?"
- "How can we preserve options while moving forward?"

**Example Application**:
```
Platform Technology Selection:
Decision: Adopting new database technology for platform

Preparation for being wrong:
- Reversibility: Maintain data export capabilities and migration scripts
- Tripwires: Performance metrics, developer satisfaction scores, operational load
- Scenarios: If performance doesn't meet expectations, if maintenance overhead too high
- Options: Evaluate 2-3 alternatives with lower switching costs
- Timeline: 3-month trial with go/no-go decision point
```

## 🎯 **Application in Engineering Leadership**

### **Technology Adoption Decisions**
```
W - Widen: Consider build vs buy vs open source vs hybrid solutions
R - Reality-test: Prototype with actual use cases, get team feedback
A - Attain distance: Consider 2-year maintenance and scaling implications
P - Prepare: Plan migration strategy and fallback options
```

### **Team Structure Decisions**
```
W - Widen: Consider matrix, cross-functional, platform team, squad models
R - Reality-test: Interview teams using different models, pilot approaches
A - Attain distance: Align with long-term product and platform roadmap
P - Prepare: Define success metrics and adjustment mechanisms
```

### **Platform Investment Decisions**
```
W - Widen: Consider platform features, infrastructure, tooling, or process improvements
R - Reality-test: Measure current pain points, validate with user research
A - Attain distance: Evaluate ROI over 12-24 month timeframe
P - Prepare: Create iterative delivery plan with checkpoints and pivots
```

## 📊 **Decision Quality Metrics**

### **Process Metrics**
- **Options Considered**: Aim for 3-5 meaningful alternatives
- **Assumptions Tested**: Identify and test 3-5 key assumptions
- **Stakeholder Input**: Gather perspectives from affected teams
- **Timeline**: Allow appropriate time for each WRAP step

### **Outcome Metrics**
- **Decision Satisfaction**: Post-decision survey at 3 and 12 months
- **Adjustment Frequency**: How often decisions need modification
- **Unexpected Consequences**: Rate of significant surprises
- **Stakeholder Alignment**: Level of buy-in and support

## 🔧 **Framework Integration**

### **Combines Effectively With**
- **Good Strategy Bad Strategy**: Use WRAP to validate strategic kernel elements
- **Team Topologies**: Apply WRAP to team structure decisions
- **Capital Allocation Framework**: Use WRAP for investment decision processes
- **Technical Strategy Framework**: Apply systematic decision-making to technical choices

### **Persona-Specific Applications**

#### **Camille (Strategic Technology)**
- Executive technology decisions with broad organizational impact
- Strategic vendor and platform selections
- Long-term technology roadmap decisions
- Business-technology alignment choices

#### **Diego (Engineering Leadership)**
- Team structure and process decisions
- Technology adoption across engineering organization
- Platform vs product development trade-offs
- Organizational scaling decisions

#### **Martin (Platform Architecture)**
- Architecture pattern and technology selections
- System design decisions with long-term implications
- Technical debt prioritization decisions
- Integration and interface design choices

## ✅ **WRAP Quality Checklist**

### **Widen Your Options**
- [ ] Considered at least 3 meaningful alternatives
- [ ] Applied vanishing options test
- [ ] Researched how others solved similar problems
- [ ] Explored simultaneous or hybrid approaches

### **Reality-Test Your Assumptions**
- [ ] Identified key assumptions underlying the decision
- [ ] Sought disconfirming evidence
- [ ] Conducted small experiments or pilots where possible
- [ ] Gathered outside perspectives

### **Attain Distance Before Deciding**
- [ ] Applied 10-10-10 rule for temporal perspective
- [ ] Evaluated alignment with core organizational values
- [ ] Allowed time for emotional distance from immediate pressures
- [ ] Considered what an outside advisor would recommend

### **Prepare to Be Wrong**
- [ ] Developed contingency plans for likely failure modes
- [ ] Identified early warning signals and tripwires
- [ ] Built in reversibility or flexibility where possible
- [ ] Created checkpoints for decision reevaluation

## 🎯 **Common Decision Traps to Avoid**

### **The Narrow Frame**
- Avoid: "Should we do X or not do X?"
- Better: "What are all the ways we could achieve goal Y?"

### **Confirmation Bias**
- Avoid: Only seeking information that supports preferred option
- Better: Actively search for reasons why each option might fail

### **Temporary Emotions**
- Avoid: Making permanent decisions based on temporary pressures
- Better: Create space for reflection and long-term perspective

### **Overconfidence**
- Avoid: Assuming decisions will work exactly as planned
- Better: Plan for multiple scenarios and build in flexibility

---

**⚖️ Apply WRAP systematically to overcome decision biases and make better strategic choices with confidence and clarity.**
