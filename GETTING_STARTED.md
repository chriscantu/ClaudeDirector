# Getting Started with ClaudeDirector

## 🎯 **Ultra-Simple Start**

### **Your Two Key Files:**
1. **`./claudedirector`** - Your main command (run this for everything)
2. **`~/engineering-director-workspace/`** - Your actual work files

### **Quick Commands:**
```bash
# Check everything is working
./claudedirector --help

# Check your workspace  
./claudedirector workspace status

# Get strategic help
./claudedirector analyze --persona martin "platform strategy question"
```

---

## 📂 **What Files Are What**

### **🎯 For Daily Use (Your Files):**
- **Your workspace**: `~/engineering-director-workspace/` (your projects, meetings, planning)
- **Main tool**: `./claudedirector` (your primary command)
- **Quick setup**: [docs/WORKSPACE_GUIDE.md](docs/WORKSPACE_GUIDE.md)

### **⚙️ ClaudeDirector Framework (Usually Hidden):**
- **Framework code**: `.claudedirector/` (hidden directory with all implementation)
- **User config**: `config/` (your settings and director templates)
- **AI entry point**: `CLAUDE.md` (for Cursor IDE integration)

### **📚 Documentation (When You Need It):**
- **This file**: README.md (overview and quick start)
- **User guides**: `docs/` (workspace setup, demo materials)
- **Implementation**: `.claudedirector/dev-docs/` (technical details)

---

## 🚀 **Your Success Path**

### **Day 1 (5 minutes):**
1. Test: `./claudedirector --help`
2. Check workspace: `./claudedirector workspace status`
3. Try: `./claudedirector analyze --persona rachel "design system question"`

### **Week 1:**
- Customize personas for your context: [docs/WORKSPACE_GUIDE.md](docs/WORKSPACE_GUIDE.md)
- Set up regular workflow with ClaudeDirector
- Explore template discovery: `./claudedirector templates discover "your domain"`

### **Month 1:**
- Create executive demo: [docs/demo/](docs/demo/)
- Build custom director templates for your team
- Integrate with your strategic planning process

---

## ❓ **Need Help?**

### **Quick References:**
- **Workspace setup**: [docs/WORKSPACE_GUIDE.md](docs/WORKSPACE_GUIDE.md)
- **Executive demos**: [docs/demo/README.md](docs/demo/README.md)
- **Troubleshooting**: `./claudedirector --help` or `.claudedirector/dev-docs/`

### **Common Questions:**
- **"Where are my files?"** → `~/engineering-director-workspace/`
- **"How do I customize?"** → `config/director_templates.yaml`
- **"Executive demo?"** → [docs/demo/](docs/demo/)

---

**🎉 ClaudeDirector is designed to get out of your way and amplify your strategic effectiveness!**

*Framework hidden, workspace separate, maximum value delivered.*
