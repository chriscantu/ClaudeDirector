# AI Code Cleanup Enforcement System

## 🎯 **Purpose**

Prevents AI agents (including Claude) from leaving excessive code artifacts, redundant documentation, and temporary files without proper justification. Enforces cleanup discipline through automated git pre-commit hooks.

## 🚨 **Problem Addressed**

AI agents commonly generate:
- **Excessive documentation** with redundant sections and AI verbosity
- **Temporary artifacts** that should never be committed
- **Placeholder code** with TODOs and NotImplementedError
- **Verbose comments** with high comment-to-code ratios
- **Redundant files** without consolidation or cleanup

## 🔧 **System Components**

### **1. Pre-commit Hook** (`.git/hooks/pre-commit-ai-cleanup`)
- **Detects AI-generated excess** using pattern matching
- **Enforces file size limits** for different file types
- **Requires cleanup justification** for large additions
- **Blocks commits** with critical violations
- **Generates cleanup scripts** automatically

### **2. Configuration** (`.claudedirector/config/ai_cleanup_config.yaml`)
- **Customizable thresholds** for file sizes and additions
- **Pattern definitions** for detecting AI verbosity
- **Exemption rules** for specific files/directories
- **Enforcement levels** (critical/warning/info)
- **Auto-cleanup actions** and consolidation rules

### **3. Pre-commit Integration** (`.pre-commit-config.yaml`)
- **Integrated workflow** with existing hooks
- **Runs on every commit** automatically
- **Fails fast** on critical violations
- **Provides actionable feedback** and suggestions

## 🛡️ **Enforcement Levels**

### **CRITICAL (Blocks Commit)**
- ❌ **Placeholder Code**: TODO, FIXME, NotImplementedError
- ❌ **Temporary Artifacts**: Files with temp/backup patterns
- ❌ **Excessive Documentation**: Files exceeding size thresholds

### **WARNING (Allows with Caution)**
- ⚠️ **AI Verbosity**: Excessive AI language patterns
- ⚠️ **Redundant Sections**: Too many documentation subsections
- ⚠️ **Comment Overload**: High comment-to-code ratio

### **INFO (Tracks but Allows)**
- ℹ️ **Insufficient Cleanup**: Not enough deletion relative to additions

## 📊 **Detection Patterns**

### **AI Verbosity Markers**
```yaml
ai_verbosity_markers:
  - "comprehensive.*implementation"
  - "detailed.*analysis"
  - "complete.*system"
  - "fully.*documented"
  - "extensive.*testing"
  - "bulletproof.*solution"
```

### **Temporary Artifacts**
```yaml
temporary_artifacts:
  - "test_.*\\.py$"           # Temporary test files
  - ".*_temp\\..*$"           # Temp file patterns
  - ".*_backup\\..*$"         # Backup files
  - "scratch_.*"              # Scratch files
  - "debug_.*"                # Debug files
```

### **Placeholder Code**
```yaml
redundant_code:
  - "# TODO:.*implement"
  - "# FIXME:.*placeholder"
  - "pass  # placeholder"
  - "raise NotImplementedError"
```

## 🚀 **Usage**

### **Automatic Enforcement**
The hook runs automatically on every commit:
```bash
git add .
git commit -m "Your commit message"
# Hook runs automatically and may block commit
```

### **Manual Testing**
Test the hook without committing:
```bash
python3 .git/hooks/pre-commit-ai-cleanup
```

### **Auto-Generated Cleanup**
When violations are detected, a cleanup script is generated:
```bash
# Run the auto-generated cleanup script
./.git/ai_cleanup.sh

# Review changes and re-commit
git add .
git commit -m "Clean commit after AI cleanup"
```

## ⚙️ **Configuration**

### **File Size Thresholds**
```yaml
size_thresholds:
  documentation: 200      # .md files
  test_files: 300        # test_*.py files
  implementation: 500    # regular .py files
  configuration: 100     # .yaml, .json files
```

### **Cleanup Requirements**
```yaml
cleanup_rules:
  max_new_files_without_justification: 3
  max_total_additions_without_review: 1000
  required_cleanup_ratio: 0.1  # 10% cleanup per addition
  max_consecutive_ai_commits: 5
```

### **Exemptions**
```yaml
exemptions:
  files:
    - "docs/ARCHITECTURE.md"
    - "README.md"
  patterns:
    - ".*_COMPLETE\\.md$"
  directories:
    - ".claudedirector/framework/"
```

## 🎯 **Example Violations**

### **Before (Blocked)**
```python
# TODO: implement comprehensive system
def comprehensive_function():
    pass  # placeholder for detailed implementation

# FIXME: placeholder for extensive analysis
def detailed_analysis():
    raise NotImplementedError("Complete system needed")
```

### **After (Allowed)**
```python
def calculate_metrics(data):
    """Calculate platform adoption metrics"""
    return sum(data.values()) / len(data)

def analyze_trends(metrics):
    """Analyze metric trends over time"""
    return [m for m in metrics if m > threshold]
```

## 📈 **Benefits**

### **For Repository Health**
- **Reduced code bloat** through automatic detection
- **Cleaner commit history** without excessive AI artifacts
- **Consistent quality standards** across AI and human contributions
- **Automated cleanup suggestions** with actionable scripts

### **For Development Workflow**
- **Fast feedback** on commit quality issues
- **Educational patterns** showing AI excess to avoid
- **Configurable enforcement** for different project needs
- **Integration ready** with existing pre-commit workflows

## 🔧 **Customization**

### **Adding New Patterns**
Edit `.claudedirector/config/ai_cleanup_config.yaml`:
```yaml
excessive_patterns:
  custom_patterns:
    - "enterprise.*grade"
    - "production.*ready"
    - "industry.*standard"
```

### **Adjusting Thresholds**
```yaml
size_thresholds:
  documentation: 150  # Stricter limit
  test_files: 200     # Smaller test files
```

### **Adding Exemptions**
```yaml
exemptions:
  files:
    - "my_large_doc.md"
  patterns:
    - "integration_test_.*"
```

## 🛠️ **Troubleshooting**

### **Hook Not Running**
```bash
# Make sure hook is executable
chmod +x .git/hooks/pre-commit-ai-cleanup

# Test hook manually
python3 .git/hooks/pre-commit-ai-cleanup
```

### **Configuration Issues**
```bash
# Install PyYAML for full configuration support
pip install PyYAML

# Validate configuration
python3 -c "import yaml; yaml.safe_load(open('.claudedirector/config/ai_cleanup_config.yaml'))"
```

### **False Positives**
Add exemptions to configuration or adjust patterns:
```yaml
exemptions:
  files:
    - "path/to/legitimate/file.py"
```

## 📊 **Monitoring**

The hook provides detailed reporting:
- **Violation counts** by category
- **File size analysis** and recommendations
- **Cleanup ratio tracking** for large additions
- **Pattern matching results** with specific violations
- **Auto-generated cleanup scripts** for immediate action

This system ensures AI agents maintain the same cleanup discipline expected from human developers, preventing repository bloat and maintaining code quality standards.
