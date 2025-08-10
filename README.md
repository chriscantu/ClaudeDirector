# ClaudeDirector: Your AI Engineering Director Team

**Zero-setup AI directors** that automatically provide strategic expertise when you need it.

## ✨ Works Out of the Box

### 🎯 **Cursor Users** (Recommended - Native Integration)
1. **Open this repo in Cursor**
2. **Start any conversation** - ClaudeDirector auto-detects and activates
3. **Talk naturally** - your AI director team responds automatically

*No installation, no configuration, no CLI commands needed.*

### 💬 **Claude Chat Users** (Also Zero Setup)
1. **Copy this repo URL**: `https://github.com/chriscantu/ClaudeDirector`
2. **Paste into any Claude conversation**
3. **Start asking strategic questions** - directors activate automatically

### 🤖 **What Happens Automatically:**

```
👤 "Our mobile platform strategy isn't aligned across iOS and Android teams"
🤖 Rachel (UX Strategy): "Let's design a cross-functional alignment strategy..."

👤 "Need to translate platform investments into business value for the board"
🤖 Alvaro (Business Strategy): "I'll help you build the ROI narrative..."

👤 "Platform architecture creating technical debt across multiple teams"
🤖 Martin (Platform Architecture): "Let's create a strategic refactoring roadmap..."
```

**That's it!** Your AI director team is ready to provide strategic expertise.

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
# framework/PERSONAS.md - Make any persona fit your context perfectly
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

<details>
<summary><strong>🔧 Want More Control?</strong> (Click to expand advanced options)</summary>

### Command Line Interface (Optional)
```bash
# See all director types available
./claudedirector templates list

# Find the perfect director for your specific challenge
./claudedirector templates discover "mobile app security compliance"

# Get industry-specific recommendations
./claudedirector templates summary mobile_director --industry fintech --team startup

# Tune activation sensitivity
claudedirector personas tune --sensitivity high    # More responsive
claudedirector personas tune --sensitivity low     # More stable

# Quick overrides in chat
# @marcus, @rachel, @auto
```

### Configuration (Optional)
Most users never need this, but you can customize:
- Director activation thresholds
- Industry-specific priorities
- Team size contexts
- Persona routing preferences

See `config/director_templates.yaml` for advanced configuration options.

### 🤖 **Meet Your Strategic AI Director Team**
- **Rachel**: Design systems strategy, cross-functional alignment
- **Martin**: Platform architecture, technical debt governance
- **Alvaro**: Business strategy, ROI analysis, executive communication
- **Diego**: Engineering leadership, team scaling, platform governance
- **Camille**: Executive strategy, organizational transformation
- **Data**: Analytics governance, metrics frameworks

*Directors automatically activate based on your conversation context - and they're fully customizable for your unique needs!*

### 📊 **Advanced Features Available**
- Executive business intelligence and strategic metrics
- Intelligent meeting tracking and organizational memory
- Persistent context across conversations
- Industry-specific guidance and team size adaptations

*All features work automatically - no configuration required.*

</details>

---

## 📚 **Resources**
- **[Quick Start Guide](docs/QUICK_START_GUIDE.md)** - Detailed walkthrough
- **[Strategic Framework](framework/PERSONAS.md)** - AI director capabilities

---

**Ready to get strategic guidance?** Just start a conversation!
