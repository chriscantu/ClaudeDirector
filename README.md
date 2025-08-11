# ClaudeDirector: Your AI Engineering Director Team

**Zero-setup AI directors** that automatically provide strategic expertise when you need it.

---

## ✨ **Quick Start** 

### **🎯 Cursor Users** (Native Integration)
1. **Open this repo in Cursor**
2. **Start any conversation** - ClaudeDirector auto-detects and activates
3. **Talk naturally** - your AI director team responds automatically

### **💬 Claude Chat Users** (Also Zero Setup)
1. **Copy this repo URL**: `https://github.com/chriscantu/ClaudeDirector`
2. **Paste into any Claude conversation**
3. **Start asking strategic questions** - directors activate automatically

### **🤖 What Happens Automatically:**

```
👤 "Our mobile platform strategy isn't aligned across iOS and Android teams"
🤖 Rachel (UX Strategy): "Let's design a cross-functional alignment strategy..."

👤 "Need to translate platform investments into business value for the board"
🤖 Alvaro (Business Strategy): "I'll help you build the ROI narrative..."

👤 "Platform architecture creating technical debt across multiple teams"
🤖 Martin (Platform Architecture): "Let's create a strategic refactoring roadmap..."
```

---

## 🎯 **Instantly Customize for YOUR Context** 

**Make it yours in under 2 minutes!** Every engineering team is unique - customize directors for your industry, team size, and strategic priorities.

### ⚡ **Super Easy Customization**

**Option 1: Quick CLI Discovery** (30 seconds)
```bash
# Find directors perfect for your specific challenges
./claudedirector templates discover "fintech mobile security compliance"
./claudedirector templates summary mobile_director --industry fintech --team startup
```

**Option 2: Edit Your Strategic Personas** (2 minutes)
```yaml
# CLAUDE.md - Make any persona fit your context perfectly
--persona-rachel
**Identity**: Your Design System Director (edit role for your needs)
**Priorities**: Your specific UX/design system priorities
**Strategic Focus**: Your unique cross-team alignment challenges
```

**Option 3: Create Custom Director Templates** (5 minutes)
```yaml
# config/director_templates.yaml - Build directors for your exact domain
your_fintech_mobile_director:
  domain: "fintech_mobile_security"
  personas: ["rachel", "martin"]  # Your preferred strategic leaders
  activation_keywords:
    "fintech mobile compliance": 0.95
    "financial app security": 0.9
  strategic_priorities:
    - "regulatory_compliance_by_design"
    - "mobile_security_architecture"
```

### 🏆 **What You Can Customize:**
- **Industry expertise**: Fintech, healthcare, enterprise SaaS, e-commerce, gaming
- **Team dynamics**: Startup constraints vs enterprise scale challenges
- **Domain focus**: Mobile, backend, data, infrastructure, product, DevOps
- **Strategic priorities**: What matters most to YOUR organization
- **Leadership style**: How you prefer strategic guidance delivered

**✨ Your customizations work instantly - no restart, no setup, just better strategic guidance!**

---

## 🚀 Ready to Start?

**Just start a conversation** - directors will automatically provide strategic expertise tailored to your context.

### 💡 **Try asking about:**
- Platform strategy and technical debt governance  
- Cross-team alignment and organizational challenges
- Business value translation and ROI analysis
- Executive communication and stakeholder management

---

## 📂 **Your Workspace**

**ClaudeDirector keeps your work separate from the framework:**

- **Your work**: `~/engineering-director-workspace/` (your projects, meetings, planning)
- **Framework**: This directory (AI directors, configuration, tools)

**[→ Workspace Setup Guide](docs/WORKSPACE_GUIDE.md)**

---

## 🎯 **Your Complete AI Director Team**

- **Rachel**: Design systems strategy, cross-functional alignment
- **Martin**: Platform architecture, technical debt governance  
- **Alvaro**: Business strategy, ROI analysis, executive communication
- **Diego**: Engineering leadership, team scaling, platform governance
- **Camille**: Executive strategy, organizational transformation
- **Data**: Analytics governance, metrics frameworks

*Directors automatically activate based on your conversation context - and they're fully customizable for your unique needs!*

---

<details>
<summary><strong>🔧 Advanced Options</strong> (Click to expand)</summary>

### Command Line Interface

```bash
# Main command interface
./claudedirector --help

# Template management
./claudedirector templates list
./claudedirector templates discover "your domain"

# Workspace management  
./claudedirector workspace status
./claudedirector workspace migrate
```

### Configuration Files

- `config/claude_config.yaml` - Core ClaudeDirector settings
- `config/director_templates.yaml` - Director template definitions
- `CLAUDE.md` - Framework entry point and persona definitions

### Advanced Features Available

- Executive business intelligence and strategic metrics
- Intelligent meeting tracking and organizational memory
- Persistent context across conversations
- Industry-specific customizations
- Team size contexts
- Persona routing preferences

</details>

---

## 📊 **Executive Demo Materials**

**Need to present ClaudeDirector to leadership?**

**[→ Complete Demo Package](docs/demo/)** - Ready-to-use presentation materials with ROI frameworks and business value propositions.

---

**🎉 Your AI engineering director team is ready to transform your strategic effectiveness!**

*Zero setup, immediate value, customizable in minutes.*