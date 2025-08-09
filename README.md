# ClaudeDirector: Strategic Leadership AI Framework

**Claude specialized for engineering directors** - Get strategic AI assistance with persistent memory and intelligent task tracking.

## 🚀 Quick Start (1 minute)

### 1. Install ClaudeDirector
```bash
git clone https://github.com/chriscantu/ClaudeDirector.git
cd ClaudeDirector
```

### 2. One-Command Setup
```bash
# Single command sets up everything
./claudedirector setup
```

### 3. Start Using ClaudeDirector
```bash
# Daily executive dashboard
./claudedirector alerts

# Scan workspace for stakeholders and tasks
./claudedirector stakeholders scan
./claudedirector tasks scan

# View your strategic intelligence
./claudedirector status
```

**That's it!** ClaudeDirector is now your strategic leadership assistant.

## ✨ What You Get

### 🧠 **Strategic AI Personas**
12 specialized personas for different leadership contexts:
- **diego**: Engineering leadership, platform strategy
- **camille**: Strategic technology, organizational scaling
- **rachel**: Design systems, cross-functional alignment
- **alvaro**: Platform ROI, business value communication

### 📊 **Executive Business Intelligence**
Transform technical work into business outcomes:
- **Strategic Metrics**: Decision velocity, platform ROI, initiative health
- **Executive Dashboards**: Real-time KPIs for leadership meetings
- **Investment Tracking**: ROI analysis and portfolio optimization
- **Board Reports**: Quarterly reviews and stakeholder updates

### 🎯 **Intelligent Meeting Tracking**
- Automatically detects new meeting prep directories
- Extracts strategic intelligence from meeting notes
- Builds persistent memory across leadership sessions
- Suggests optimal AI personas for different meeting types

### 🗄️ **Persistent Strategic Memory**
- SQLite database stores organizational intelligence
- Executive sessions, stakeholder relationships, platform insights
- Context persists across Claude conversations
- No more re-explaining your org structure every session

## 🎯 **Unified Command Interface**

All ClaudeDirector features accessible through single `claudedirector` command:

### **📊 Executive Dashboard**
```bash
./claudedirector alerts              # Daily executive alerts
./claudedirector status              # System health overview
./claudedirector metrics             # Business metrics summary
./claudedirector dashboard           # Executive KPI dashboard
```

### **🧠 Meeting Intelligence**
```bash
./claudedirector meetings scan       # Process meeting files
./claudedirector meetings demo       # See demo
```

### **👥 Stakeholder Management**
```bash
./claudedirector stakeholders scan   # AI detect stakeholders
./claudedirector stakeholders list   # View all stakeholders
./claudedirector stakeholders alerts # Daily engagement alerts
```

### **🎯 Task Management**
```bash
./claudedirector tasks scan          # AI detect tasks
./claudedirector tasks list          # View my tasks
./claudedirector tasks overdue       # Critical overdue items
./claudedirector tasks followups     # Stakeholder follow-ups
```

### **⚡ Smart Development**
```bash
./claudedirector git setup          # Intelligent git hooks
./claudedirector git commit -m "msg" # Optimized commits
```

### **💼 Business Intelligence**
```bash
./claudedirector roi calculate       # Calculate investment ROI
./claudedirector reports quarterly   # Generate quarterly business review
./claudedirector reports board       # Create board presentation
```



## 🏗️ Architecture

ClaudeDirector provides **unified strategic leadership AI** through:

1. **🎭 Strategic AI Foundation**: 12 specialized personas for different leadership contexts
2. **🧠 Intelligent Automation**: AI-powered stakeholder detection and task extraction
3. **📊 Executive Intelligence**: Business metrics, ROI tracking, and executive reporting
4. **💾 Persistent Memory**: Strategic intelligence that persists across sessions

### **🏗️ Clean Architecture**
Enterprise-grade organization optimized for strategic leadership:
- **Strategic Intelligence**: Persistent memory across leadership sessions
- **Business Intelligence**: ROI tracking and executive reporting
- **Meeting Intelligence**: Automated stakeholder and task extraction
- **Unified Interface**: Single command for all strategic operations

## 📚 Advanced Features (Optional)

### Jira Integration for Strategic Reporting

<details>
<summary>🔧 Enterprise Jira Integration Setup (Click to expand)</summary>

If you want automated strategic initiative tracking and executive reporting:

```bash
# Set up the Python service
cd strategic_integration_service
python -m venv venv
source venv/bin/activate
pip install -e .

# Configure environment
cp env.example .env
# Edit .env with your Jira credentials

# Extract strategic initiatives
sis-extract-l2 --output workspace/l2-initiatives.json
sis-weekly-report --output workspace/weekly-slt-report.md
```

**Features:**
- Automated L2 strategic initiative extraction
- Weekly SLT executive reports
- Monthly PI initiative analysis
- Performance optimization with multi-tier caching

**Requirements:**
- Jira API access
- Strategic initiative structure in your Jira instance
- Organizational buy-in for automated reporting

</details>

### Custom Persona Development

<details>
<summary>🎭 Creating Custom Strategic Personas (Click to expand)</summary>

You can extend ClaudeDirector with your own strategic personas:

**Quick Setup:**
1. Edit `claude_config.yaml` in the project root
2. Add your custom personas and strategic context
3. Define auto-activation rules and business priorities

**Example Configuration:**
```yaml
personas:
  custom_cto:
    description: "CTO-level strategic technology leadership"
    context: "Technology vision and architectural decisions"
    triggers: ["technical strategy", "architecture roadmap"]

strategic_context:
  priorities:
    - "Platform scalability and developer experience"
    - "Design system adoption and consistency"
```

**Features:**
- Organization-specific strategic priorities
- Custom stakeholder relationship mapping
- Tailored business metrics and KPI focus
- Context-aware persona auto-activation

See `claude_config.yaml` for detailed configuration examples.

</details>



## 🚀 Next Steps

### Immediate Value (Day 1)
1. ✅ **Set up meeting tracking** - Let ClaudeDirector learn your meeting patterns
2. ✅ **Try strategic personas** - Use `@diego` for platform decisions, `@alvaro` for business metrics
3. ✅ **View business metrics** - `./claudedirector metrics` for instant ROI insights

### Strategic Value (Week 1)
1. **Generate business reports** - Use `./claudedirector reports quarterly` for executive summaries
2. **Track ROI performance** - Monitor platform investment returns and optimization opportunities
3. **Leverage AI insights** - Use `@alvaro` for translating technical work into business value

### Enterprise Value (Month 1)
1. **Executive dashboard adoption** - Regular KPI monitoring and strategic decision support
2. **Board presentation ready** - Generate professional reports with `./claudedirector reports board`
3. **Scale team adoption** - Share business intelligence patterns across leadership team

## 🆘 Getting Help

### Quick Troubleshooting
```bash
# Check system health
./claudedirector status

# Test business metrics
./claudedirector metrics

# Re-setup if needed
./claudedirector setup
```

### Common Issues
- **Import errors**: Run from project root directory
- **Setup issues**: Re-run `./claudedirector setup`
- **Business metrics not showing**: Check `./claudedirector metrics` output
- **Persona customization**: Edit `claude_config.yaml` for organization-specific personas
- **Meeting tracking not working**: Verify `workspace/meeting-prep/` directory exists

---

**ClaudeDirector**: From AI assistant to strategic platform engineering partner.

*Built for engineering directors who want strategic AI that remembers, learns, and delivers measurable business value.*
