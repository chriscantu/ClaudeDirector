# ClaudeDirector Installation Guide

**Complete installation instructions for all environments and use cases.**

---

## 🎯 **Prerequisites**

### **System Requirements**
- **Python**: 3.9+ (recommended: 3.11)
- **Git**: For repository cloning
- **Cursor**: Recommended IDE for optimal experience
- **Operating System**: macOS, Linux, Windows (WSL recommended)

### **Zero Setup Principle** - P0 Validated
✅ **ClaudeDirector works immediately** without any additional installations
✅ **95%+ setup reliability** across all environments (validated by 29 P0 tests)
✅ **MCP integration gracefully degrades** to fallback mode if external servers unavailable
✅ **Full strategic functionality** maintained without Node.js, Docker, or other dependencies
✅ **Network independence** - basic functionality works offline
✅ **Error recovery** - graceful handling of common setup scenarios

### **Optional Enhancements**
- **Node.js**: 18+ (for enhanced MCP server integration - system works without this)
- **Docker**: For containerized deployment
- **PyYAML**: For advanced configuration features (system works without this)

## 📥 **Installation Methods**

### **Method 1: Cursor Integration (Recommended) - Zero Setup**

#### **Step 1: Clone Repository**
```bash
git clone https://github.com/chriscantu/ClaudeDirector.git
cd ClaudeDirector
```

#### **Step 2: Open in Cursor**
```bash
cursor .
```

#### **Step 3: Start Strategic Conversation**
Ask any strategic question in Cursor:
```
"Test ClaudeDirector transparency: How should we approach platform scaling?"
```

**That's it!** ClaudeDirector is now active with:
- ✅ **Full strategic functionality** (personas, frameworks, transparency)
- ✅ **P0-validated setup** (29 tests prevent setup failures)
- ✅ **95%+ reliability** across all environments
- ✅ **Fallback mode** provides complete capability without external dependencies
- ✅ **Zero additional installations** required

**Expected Response:**
- Persona header with emoji (🎯 Diego | Engineering Leadership)
- MCP transparency disclosure for complex questions
- Framework attribution when strategic frameworks are applied

### **Method 2: Claude Chat Integration**

#### **Share Repository URL**
```
https://github.com/chriscantu/ClaudeDirector
```

#### **Initialize with Test Question**
```
"Using the ClaudeDirector framework, help me develop a strategic approach
to organizational scaling with cross-functional team coordination."
```

### **Method 3: Local Development Setup**

#### **Step 1: Environment Setup**
```bash
# Clone repository
git clone https://github.com/chriscantu/ClaudeDirector.git
cd ClaudeDirector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### **Step 2: Configuration**
```bash
# Copy configuration templates
cp .claudedirector/config/default_config.yaml .claudedirector/config/user_config.yaml

# Edit configuration for your environment
# Optional: Install PyYAML for advanced features
pip install PyYAML
```

#### **Step 3: Validation**
```bash
# Run test suite
python3 .claudedirector/tests/run_mcp_transparency_tests.py

# Test installation
python3 -c "
from claudedirector.core.auto_conversation_integration import get_capture_status
print('✅ ClaudeDirector ready:', get_capture_status()['enabled'])
"
```

## ✅ **Zero Setup Validation**

### **Verify Zero Setup Capability**

Test that ClaudeDirector works without any additional installations:

```bash
# Test that core functionality works
python3 .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py | head -3

# Expected output (with your configured name):
# 🛡️ MANDATORY P0 TEST ENFORCEMENT SYSTEM
# [Your Name]'s requirement: All P0 features always tested, never skipped
```

### **What Works in Zero Setup Mode**
- ✅ **All personas** (Diego, Camille, Rachel, Alvaro, Martin)
- ✅ **Strategic frameworks** (25+ methodologies)
- ✅ **Transparency system** (persona headers, framework attribution)
- ✅ **Conversation tracking** and quality measurement
- ✅ **P0 enforcement** and testing
- ✅ **User configuration** with personal attribution

### **Progressive Enhancement**
ClaudeDirector provides immediate value and progressively enhances capabilities:
- ✅ **Immediate**: All personas, frameworks, and transparency features work instantly
- ✅ **Enhanced**: MCP servers auto-install when needed for advanced analysis
- ✅ **Seamless**: Users see "Installing MCP enhancement..." only when beneficial
- ✅ **Reliable**: Full strategic functionality always available

## 🔧 **Advanced Installation**

### **MCP Server Integration** (Optional)

#### **Optional: Enhanced MCP Integration**

**⚠️ IMPORTANT**: ClaudeDirector works fully without these installations (fallback mode)

```bash
# OPTIONAL: Enhanced MCP servers for additional capabilities
# Sequential MCP Server (strategic analysis)
npm install -g @sequential/mcp-server

# Context7 MCP Server (framework patterns)
pip install context7

# Magic MCP Server (visual generation)
npm install -g @magic/mcp-server
```

**Without MCP servers**: Full strategic functionality with graceful fallback
**With MCP servers**: Enhanced analysis capabilities and visual generation

#### **Configure MCP Servers** (Optional)
```yaml
# .claudedirector/config/mcp_servers.yaml
servers:
  sequential:
    command: "npx"
    args: ["-y", "@sequential/mcp-server"]
    capabilities: ["systematic_analysis", "business_strategy"]

  context7:
    command: "python"
    args: ["-m", "context7.server"]
    capabilities: ["pattern_access", "methodology_lookup"]
```

### **Docker Deployment** (Enterprise)

#### **Build Container**
```bash
# Build ClaudeDirector image
docker build -t claudedirector:latest .

# Run with conversation persistence
docker run -d \
  --name claudedirector \
  -v $(pwd)/data:/app/data \
  -p 8080:8080 \
  claudedirector:latest
```

#### **Docker Compose Setup**
```yaml
# docker-compose.yml
version: '3.8'
services:
  claudedirector:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./.claudedirector/config:/app/.claudedirector/config
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
```

## ✅ **Verification & Testing**

### **Basic Functionality Test**
```bash
# Test core imports
python3 -c "
import sys
sys.path.append('.claudedirector/integration-protection')
from cursor_transparency_bridge import ensure_transparency_compliance
print('✅ Core functionality available')
"

# Test MCP transparency
python3 .claudedirector/tests/run_mcp_transparency_tests.py
```

### **Integration Test**
Ask this question in your chosen environment:
```
"Diego, how should we develop a strategic organizational framework
for complex multi-team platform architecture assessment?"
```

**Verification Checklist:**
- [ ] Persona header appears: `🎯 Diego | Engineering Leadership`
- [ ] MCP disclosure shows: `🔧 Accessing MCP Server: sequential (systematic_analysis)`
- [ ] Processing indicator: `*Analyzing your organizational challenge...*`
- [ ] Framework attribution appears when strategic frameworks are detected
- [ ] Response includes actionable strategic guidance

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Module not found errors
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.claudedirector/lib"

# Or add to virtual environment
echo "$(pwd)/.claudedirector/lib" > venv/lib/python3.11/site-packages/claudedirector.pth
```

#### **MCP Server Issues**
```bash
# Test MCP servers individually
npx -y @sequential/mcp-server --version
python -m context7.server --help

# Check configuration
python3 -c "
import yaml
with open('.claudedirector/config/mcp_servers.yaml') as f:
    config = yaml.safe_load(f)
    print('✅ MCP configuration valid')
"
```

#### **Permission Issues**
```bash
# Make scripts executable
chmod +x .git/hooks/pre-commit-ai-cleanup
chmod +x .claudedirector/tests/run_mcp_transparency_tests.py

# Fix file permissions
find .claudedirector -name "*.py" -exec chmod +x {} \;
```

### **Performance Optimization**

#### **Memory Management**
```bash
# Clear conversation cache
rm -rf .claudedirector/cache/conversations/*

# Optimize database
sqlite3 data/strategic/strategic_memory.db "VACUUM;"
```

#### **Response Time Tuning**
```yaml
# .claudedirector/config/performance.yaml
mcp_settings:
  timeout: 5  # Reduce for faster responses
  cache_ttl: 3600  # Increase for better caching

transparency:
  complexity_threshold: 4  # Increase to reduce MCP calls
```

## 🚀 **Next Steps**

After successful installation:

1. **Quick Start**: Follow [docs/setup/QUICK_START.md](./QUICK_START.md) for immediate usage
2. **Development**: See [docs/development/DEVELOPMENT_GUIDE.md](../development/DEVELOPMENT_GUIDE.md) for extending ClaudeDirector
3. **Architecture**: Review [docs/architecture/OVERVIEW.md](../architecture/OVERVIEW.md) for system understanding
4. **Configuration**: Customize settings in [docs/reference/CONFIGURATION.md](../reference/CONFIGURATION.md)

---

**🎯 Installation complete! ClaudeDirector is ready for strategic leadership guidance.**
