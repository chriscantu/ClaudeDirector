# User Configuration Guide

## 🎯 **Overview**

ClaudeDirector now supports personalized system messages and documentation through a centralized user configuration system. Instead of hardcoded names, all system messages will use your configured identity.

## 👤 **Quick Setup**

### **Option 1: Interactive Configuration**
```bash
# Run the interactive setup
python3 .claudedirector/bin/configure-user
```

### **Option 2: Direct File Editing**
```bash
# Edit the configuration file directly
nano .claudedirector/config/user_identity.yaml
```

### **Option 3: Environment Variables**
```bash
export CLAUDEDIRECTOR_USER_NAME="Your Name"
export CLAUDEDIRECTOR_WORK_NAME="Work Name"
export CLAUDEDIRECTOR_FULL_NAME="Your Full Name"
```

## 📁 **Configuration File**

**Location**: `.claudedirector/config/user_identity.yaml`

**Example Configuration**:
```yaml
# ClaudeDirector User Identity Configuration
user:
  name: "Cantu"
  work_name: "Cantu"
  full_name: "Chris Cantu"
  role: "Engineering Director"
  organization: "Platform Team"
```

## 🎯 **Name Usage Contexts**

| Context | Field Used | Example Usage |
|---------|------------|---------------|
| **Default** | `name` | "Cantu's requirement" |
| **Professional** | `work_name` → `name` | P0 enforcement messages |
| **Formal** | `full_name` → `name` | Documentation attribution |
| **Work** | `work_name` → `name` | System messages |

## 🔧 **Environment Variables**

| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAUDEDIRECTOR_USER_NAME` | Primary name | "Cantu" |
| `CLAUDEDIRECTOR_WORK_NAME` | Professional name | "Cantu" |
| `CLAUDEDIRECTOR_FULL_NAME` | Full formal name | "Chris Cantu" |
| `CLAUDEDIRECTOR_USER_ROLE` | Role/title | "Engineering Director" |
| `CLAUDEDIRECTOR_ORGANIZATION` | Organization | "Platform Team" |

**Priority Order**:
1. Environment variables (highest)
2. Configuration file
3. Default "User" (lowest)

## 📊 **Impact Areas**

### **P0 Test Enforcement**
- **Before**: "Michael's requirement: All P0 features must always be tested"
- **After**: "Cantu's requirement: All P0 features must always be tested"

### **System Messages**
- All error messages and notifications use configured name
- Attribution in documentation and reports
- Personalized command-line output

### **Documentation Generation**
- Strategic documents use configured name and role
- Meeting preparation materials include proper attribution
- Executive summaries reference correct identity

## 🛠️ **Technical Implementation**

### **User Configuration API**
```python
from config.user_config import get_user_identity, get_user_name, get_user_attribution

# Get full user identity
user = get_user_identity()
print(f"Name: {user.name}")
print(f"Role: {user.role}")

# Get specific name for context
professional_name = get_user_name("professional")
attribution = get_user_attribution()  # "Cantu's requirement"
```

### **Integration Points**
- **P0 Test Enforcement**: Uses `get_user_attribution()` for requirement messages
- **System Messages**: Uses `get_user_name("professional")` for professional contexts
- **Documentation**: Uses `get_user_name("full")` for formal attribution

## 🔒 **Security Considerations**

### **Sensitive Information**
- User configuration may contain personal information
- Consider adding to `.gitignore` for shared repositories
- Use environment variables for CI/CD environments

### **Recommended .gitignore Addition**
```bash
# User-specific configuration
.claudedirector/config/user_identity.yaml
```

### **CI/CD Environment Setup**
```bash
# Set user identity via environment variables
export CLAUDEDIRECTOR_USER_NAME="CI Bot"
export CLAUDEDIRECTOR_WORK_NAME="CI Bot"
```

## 📋 **Examples**

### **Individual Developer Setup**
```yaml
user:
  name: "Alex"
  work_name: "Alex"
  full_name: "Alex Smith"
  role: "Senior Engineer"
  organization: "Platform Team"
```

### **Team Lead Setup**
```yaml
user:
  name: "Taylor"
  work_name: "Taylor"
  full_name: "Taylor Johnson"
  role: "Engineering Manager"
  organization: "Product Platform"
```

### **Executive Setup**
```yaml
user:
  name: "Jordan"
  work_name: "Jordan"
  full_name: "Jordan Chen"
  role: "VP Engineering"
  organization: "Engineering Division"
```

## 🚀 **Benefits**

### **Personalization**
- System messages feel natural and personal
- Proper attribution in all documentation
- Professional identity in organizational contexts

### **Team Adoption**
- Each team member has personalized experience
- Clear accountability through proper attribution
- Reduces confusion about who set requirements

### **Organizational Scale**
- Works for individual contributors through executives
- Supports multiple organizational contexts
- Environment variable support for automation

## 🔄 **Migration from Hardcoded Names**

### **Automatic Fallback**
- System gracefully handles missing configuration
- Falls back to "User" if no configuration found
- No breaking changes to existing functionality

### **Gradual Adoption**
- Configure individual components over time
- Existing hardcoded references continue working
- Update documentation and messages as needed

## 📞 **Support**

### **Troubleshooting**
- **Config not loading**: Check file path and permissions
- **YAML parsing errors**: Use environment variables as fallback
- **Name not appearing**: Verify configuration syntax

### **Testing Configuration**
```bash
# Test current configuration
python3 -c "
import sys; sys.path.insert(0, '.claudedirector/lib')
from config.user_config import get_user_attribution
print('Current attribution:', get_user_attribution())
"
```

---

## 🎉 **Getting Started**

1. **Configure your identity** using interactive setup or file editing
2. **Test the configuration** to ensure it loads correctly
3. **Run P0 tests** to see personalized enforcement messages
4. **Generate documentation** to see proper attribution

Your ClaudeDirector experience is now personalized and professional!
