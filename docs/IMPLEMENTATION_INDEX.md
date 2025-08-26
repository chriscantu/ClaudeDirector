# Implementation Index

**Navigation to implementation documentation.**

---

## 🎯 **Product Requirements & Strategy**

### **Single Source of Truth**
- **[Product Requirements Document (PRD)](requirements/PRODUCT_REQUIREMENTS_DOCUMENT.md)** - Feature prioritization and business justification
- **[Feature Status Matrix](requirements/FEATURE_STATUS_MATRIX.md)** - Real-time implementation status vs. requirements
- **[Investment ROI Tracking](requirements/FEATURE_STATUS_MATRIX.md#-investment-and-roi-tracking)** - Business value and financial performance

## 🚀 **Getting Started**

### **Quick Setup**
- **[Quick Start Guide](setup/QUICK_START.md)** - Get running in 5 minutes
- **[Installation Guide](setup/INSTALLATION.md)** - Complete installation for all environments

### **First Steps**
1. **Setup**: Follow [Quick Start](setup/QUICK_START.md) for immediate usage
2. **Test**: Verify with strategic questions and transparency validation
3. **Customize**: Configure personas and frameworks for your context

## 🏗️ **Development**

### **Core Development**
- **[Development Guide](development/DEVELOPMENT_GUIDE.md)** - Architecture and extension guide
- **[API Reference](reference/API_REFERENCE.md)** - API documentation

### **Architecture Deep-Dive**
- **[Architecture Overview](architecture/OVERVIEW.md)** - System architecture and design patterns
- **[Component Guide](architecture/COMPONENTS.md)** - Detailed component documentation
- **[Decision Records](architecture/DECISIONS.md)** - Architectural decision history

## 📚 **Reference Documentation**

### **API & Integration**
- **[API Reference](reference/API_REFERENCE.md)** - API documentation
- **[Configuration Guide](reference/CONFIGURATION.md)** - Configuration options and tuning
- **[MCP Integration](reference/MCP_INTEGRATION.md)** - MCP server integration guide

### **Strategic Frameworks**
- **[Strategic Frameworks Guide](STRATEGIC_FRAMEWORKS_GUIDE.md)** - 25+ strategic methodologies
- **[Framework Detection](reference/FRAMEWORK_DETECTION.md)** - Framework detection patterns

## 🧪 **Testing & Quality**

### **Unified Testing Architecture**
- **[Testing Architecture](architecture/TESTING_ARCHITECTURE.md)** - Unified testing system design
- **[Test Registry](../claudedirector/config/test_registry.yaml)** - Single source of truth for all tests
- **[Unified Test Runner](../claudedirector/tools/testing/unified_test_runner.py)** - Consistent test execution

### **Test Execution**
- **Local Validation**: `python .claudedirector/tools/testing/unified_test_runner.py local_quick`
- **Pre-Push Validation**: `python .claudedirector/tools/testing/unified_test_runner.py pre_push`
- **CI Full Suite**: `python .claudedirector/tools/testing/unified_test_runner.py ci_full`

### **System Administration**
- **Database Setup**: `python .claudedirector/tools/setup/setup_database.py`
- **Note**: Legacy CLI (`bin/claudedirector`) has been deprecated in favor of Cursor integration

### **Quality Assurance**
- **[Quality Standards](reference/QUALITY_STANDARDS.md)** - Code quality and standards
- **[AI Cleanup Guidelines](reference/AI_CLEANUP.md)** - AI cleanup enforcement guide

## 🔧 **Advanced Topics**

### **Customization**
- **[Custom Personas](advanced/CUSTOM_PERSONAS.md)** - Creating custom strategic personas
- **[Framework Extension](advanced/FRAMEWORK_EXTENSION.md)** - Adding custom frameworks
- **[MCP Development](advanced/MCP_DEVELOPMENT.md)** - Developing custom MCP servers

### **Production Deployment**
- **[Deployment Guide](deployment/DEPLOYMENT_GUIDE.md)** - Production deployment strategies
- **[Monitoring](deployment/MONITORING.md)** - System monitoring and observability
- **[Security](SECURITY.md)** - Security considerations and best practices

## 📊 **Performance & Optimization**

### **Performance**
- **[Performance Tuning](reference/PERFORMANCE_TUNING.md)** - Response time optimization
- **[Memory Management](reference/MEMORY_MANAGEMENT.md)** - Memory usage optimization
- **[Caching Strategies](reference/CACHING.md)** - Caching for improved performance

## 🎯 **Quick Reference**

### **Essential Commands**
```bash
# Run quick local validation
python .claudedirector/tools/testing/unified_test_runner.py local_quick

# Run pre-push validation (before git push)
python .claudedirector/tools/testing/unified_test_runner.py pre_push --validate

# Run complete CI test suite locally
python .claudedirector/tools/testing/unified_test_runner.py ci_full

# Validate test architecture consistency
python .claudedirector/tools/testing/unified_test_runner.py local_quick --validate
```

### **Key File Locations**
```
📁 ClaudeDirector/
├── 📁 docs/setup/                           # Installation and quick start
├── 📁 docs/development/                     # Development guides
├── 📁 docs/architecture/                    # Architecture documentation
│   └── 📄 TESTING_ARCHITECTURE.md          # Unified testing system design
├── 📁 .claudedirector/config/               # Configuration files
│   └── 📄 test_registry.yaml               # Single source of truth for tests
├── 📁 .claudedirector/tools/testing/        # Unified testing tools
│   └── 📄 unified_test_runner.py           # Consistent test execution
├── 📁 .claudedirector/tests/                # Test suites
└── 📄 README.md                             # Project overview
```

### **Support & Resources**
- **[Troubleshooting](reference/TROUBLESHOOTING.md)** - Common issues and solutions
- **[FAQ](reference/FAQ.md)** - Frequently asked questions
- **[Changelog](CHANGELOG.md)** - Version history and changes
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

---

**🎯 Navigate to specific guides based on your needs. All documentation is focused and actionable.**
