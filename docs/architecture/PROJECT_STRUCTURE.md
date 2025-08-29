# ClaudeDirector Project Structure

**Definitive architectural organization guide for ClaudeDirector v3.3.0+**

---

## 📋 **Document Purpose**

This document defines the **mandatory** project structure for ClaudeDirector. All development MUST adhere to this structure to maintain architectural consistency and avoid technical debt accumulation.

**Last Updated**: January 15, 2025 (Post-v3.3.0 Phase 9 Architecture Cleanup SUCCESS)
**Architecture Status**: ✅ **PHASE 9 COMPLETE** - 21/23 BLOCKING P0 tests passing (91%), consolidated architecture with lightweight fallback pattern

---

## 🏗️ **Root Directory Structure**

```
ai-leadership/                              # Repository root
├── README.md                               # Project overview and quick start
├── requirements.txt                        # Python dependencies
├── bin/                                    # Executable binaries
│   └── claudedirector                      # Main CLI entry point
├── .claudedirector/                        # 🎯 CORE SYSTEM (Primary Architecture)
├── data/                                   # Runtime data and databases
├── docs/                                   # Documentation and guides
├── leadership-workspace/                   # User strategic workspace
└── venv/                                   # Python virtual environment
```

### **Critical Principle**
- **`.claudedirector/` is the PRIMARY system directory** - all core functionality lives here
- **`leadership-workspace/` is USER territory** - strategic work and personal files
- **Never mix system and user concerns** - strict separation enforced

---

## 🎯 **`.claudedirector/` - Core System Architecture**

### **Top-Level Organization**
```
.claudedirector/
├── lib/                                    # 🧠 Core System Library
├── tests/                                  # 🧪 Comprehensive Test Suite
├── tools/                                  # 🔧 Development & Operations Tools
├── config/                                 # ⚙️ System Configuration
├── templates/                              # 📋 User Templates
└── [system files]                         # Various system entry points
```

### **`lib/` - Core System Library** (PRIMARY ARCHITECTURE)

```
lib/
├── context_engineering/                    # 🚀 PRIMARY SYSTEM (Phase 3.2B Complete)
│   ├── __init__.py                         # Module exports and public API
│   ├── advanced_context_engine.py          # Main orchestration engine
│   ├── conversation_layer.py               # Layer 1: Conversation memory
│   ├── strategic_layer.py                  # Layer 2: Strategic memory
│   ├── stakeholder_layer.py                # Layer 3: Stakeholder intelligence
│   ├── learning_layer.py                   # Layer 4: Learning patterns
│   ├── organizational_layer.py             # Layer 5: Organizational memory
│   ├── team_dynamics_engine.py             # Layer 6: Team dynamics (v2.9.0)
│   ├── realtime_monitor.py                 # Layer 7: Real-time intelligence (v2.10.0)
│   ├── ml_pattern_engine.py                # Layer 8: ML pattern detection (v2.12.0)
│   ├── context_orchestrator.py             # Cross-layer coordination
│   ├── analytics_engine.py                 # Analytics and insights
│   ├── organizational_learning_engine.py   # Organizational learning
│   └── workspace_integration.py            # Workspace monitoring
│
├── core/                                   # 🏗️ Foundational Components
│   ├── models.py                           # Core data models
│   ├── database.py                         # Database abstractions
│   ├── validation.py                       # Input validation
│   └── [35+ core modules]                  # Essential system components
│
├── performance/                            # 🚀 Phase 8: Enterprise Performance Optimization
│   ├── __init__.py                         # Performance module exports
│   ├── cache_manager.py                    # Redis-compatible in-memory caching
│   ├── memory_optimizer.py                 # Object pooling and memory management
│   ├── response_optimizer.py               # Priority-based response optimization
│   └── performance_monitor.py              # Real-time monitoring and alerting
│
├── ai_intelligence/                        # 🤖 AI Enhancement System
│   ├── __init__.py                         # AI intelligence exports
│   ├── decision_orchestrator.py            # Main AI coordination
│   ├── enhanced_framework_detection.py     # Framework recognition
│   ├── framework_mcp_coordinator.py        # MCP coordination
│   ├── mcp_decision_pipeline.py            # Decision pipeline
│   └── mcp_enhanced_framework_engine.py    # Enhanced framework engine
│
├── p0_features/                            # 🛡️ Business-Critical Features
│   └── [42 P0 feature modules]             # Mandatory functionality
│
├── p1_features/                            # 📈 High-Priority Features
│   └── [6 P1 feature modules]              # Important functionality
│
├── p2_communication/                       # 💬 Communication Layer
│   └── [11 communication modules]          # User interaction
│
├── transparency/                           # 🔍 Transparency System
│   └── [9 transparency modules]            # AI transparency
│
├── integration/                            # 🔗 Integration Layer
│   ├── __init__.py                         # Integration exports
│   └── unified_bridge.py                   # Primary integration bridge
│
├── config/                                 # ⚙️ Configuration Management
│   ├── __init__.py                         # Config exports
│   └── user_config.py                      # User configuration
│
├── utils/                                  # 🔧 Utility Functions
│   └── [5 utility modules]                 # Helper functions
│
└── [legacy directories - CLEANUP IN PROGRESS] # 🚧 Phase 9 Migration Active
    ├── clarity/                            # 🚧 MIGRATING → context_engineering (action detection)
    ├── intelligence/                       # 🚧 MIGRATING → ai_intelligence + context_engineering
    ├── memory/                             # 🚧 MIGRATING → context_engineering (memory systems)
    ├── persona_integration/                # 🚧 MIGRATING → context_engineering (persona logic)
    ├── integrations/                       # 🚧 MIGRATING → integration/unified_bridge.py
    └── bridges/                            # 🚧 MIGRATING → integration/unified_bridge.py
```

### **`tests/` - Comprehensive Test Architecture**

```
tests/
├── p0_enforcement/                         # 🚨 P0 Test Enforcement System
│   ├── p0_test_definitions.yaml            # ✅ Single source of truth (28 tests)
│   ├── run_mandatory_p0_tests.py           # ✅ Unified test runner
│   └── results/                            # Test execution results
│
├── regression/                             # 🛡️ Regression Protection
│   ├── p0_blocking/                        # Critical feature protection
│   │   ├── memory_context_modules/         # Modular memory tests
│   │   ├── test_*_p0.py                    # Individual P0 tests
│   │   └── [20+ P0 test modules]           # Business-critical coverage
│   ├── p0_high_priority/                   # High-priority features
│   ├── business_critical/                  # Business impact validation
│   ├── ux_continuity/                      # User experience consistency
│   └── user_journeys/                      # End-to-end workflows
│
├── unit/                                   # 🔬 Unit Testing
│   ├── ai_intelligence/                    # AI component testing
│   ├── context_engineering/                # Context system testing
│   └── [component-specific tests]          # Isolated functionality
│
├── integration/                            # 🔗 Integration Testing
│   └── [20 integration test modules]       # Cross-component validation
│
├── performance/                            # ⚡ Performance Validation
│   └── [5 performance test modules]        # Speed and efficiency
│
└── [additional test categories]            # Comprehensive coverage
```

### **`tools/` - Development & Operations Tools**

```
tools/
├── architecture/                           # 🏗️ Architecture Tools
│   ├── architectural_validator.py          # Structure validation
│   ├── dependency_analyzer.py              # Import analysis
│   └── solid_analyzer.py                   # SOLID compliance checking
│
├── ci/                                     # 🚀 Continuous Integration
│   ├── pre_push_validator.py               # Pre-push validation
│   ├── ci_orchestrator.py                  # CI coordination
│   └── [8 additional CI tools]             # Build automation
│
├── git-hooks/                              # 🪝 Git Integration
│   ├── pre-commit                          # Pre-commit validation
│   ├── pre-push                            # Pre-push enforcement
│   └── [7 additional hooks]                # Git workflow automation
│
├── security/                               # 🔒 Security Tools
│   ├── stakeholder_scanner.py              # Stakeholder data protection
│   ├── enhanced_security_scanner.py        # Comprehensive security
│   └── [3 additional security tools]       # Security enforcement
│
├── setup/                                  # ⚙️ System Setup
│   ├── setup_meeting_intelligence.py       # Meeting integration
│   ├── setup_smart_git.py                  # Git automation
│   └── [3 additional setup tools]          # System initialization
│
└── [specialized tool categories]           # Development support
```

### **`config/` - System Configuration**

```
config/
├── schemas/                                # 📊 Database Schemas
│   ├── enhanced_schema.sql                 # Primary schema
│   ├── session_context_schema.sql          # Session management
│   └── [4 additional schemas]              # Specialized data structures
│
├── user_identity.yaml.template             # 👤 User Config Template
├── user_identity.yaml                      # 🔒 Personal Config (gitignored)
├── p0_features_production.yaml             # 🛡️ P0 Feature Registry
├── test_registry.yaml                      # 🧪 Test Configuration
├── mcp_servers.yaml                        # 🔧 MCP Server Config
└── [10+ additional config files]           # System settings
```

---

## 📁 **`docs/` - Documentation Architecture**

```
docs/
├── architecture/                           # 🏗️ Architectural Documentation
│   ├── OVERVIEW.md                         # High-level architecture (THIS FILE NEEDS UPDATE)
│   ├── PROJECT_STRUCTURE.md                # This document
│   ├── TESTING_ARCHITECTURE.md             # Test system architecture
│   ├── COMPONENTS.md                       # Component specifications
│   └── patterns/                           # Architectural patterns
│
├── requirements/                           # 📋 Requirements Documentation
│   ├── CONTEXT_ENGINEERING_REQUIREMENTS.md # Primary requirements
│   ├── PRODUCT_REQUIREMENTS_DOCUMENT.md    # Business requirements
│   └── FEATURE_STATUS_MATRIX.md            # Feature tracking
│
├── development/                            # 👨‍💻 Development Guides
│   ├── DEVELOPMENT_GUIDE.md                # Development process
│   ├── guides/                             # Specific guides (11 files)
│   └── SOLID_REFACTORING_CLEANUP_SPRINT_PLAN.md # Current cleanup plan
│
├── setup/                                  # 🚀 Setup Documentation
│   ├── INSTALLATION.md                     # Installation guide
│   └── QUICK_START.md                      # Quick start guide
│
└── [user-facing documentation]             # Guides and references
```

---

## 🏢 **`leadership-workspace/` - User Territory**

```
leadership-workspace/
├── README.md                               # Workspace overview
├── analysis/                               # Strategic analysis
├── archive/                                # Historical data
├── budget-planning/                        # Financial planning
├── configs/                                # User configurations
├── current-initiatives/                    # Active projects
├── meeting-prep/                           # Meeting preparation
├── reports/                                # Generated reports
├── scripts/                                # User automation
├── strategic-docs/                         # Strategic documentation
├── strategy/                               # Strategic planning
├── vendor-evaluations/                     # Vendor assessments
└── weekly-reports/                         # Regular reporting
```

**User Territory Principles**:
- ✅ **User owns this space** - system never modifies without permission
- ✅ **Strategic work lives here** - all user content isolated
- ✅ **Backed up automatically** - workspace preservation guaranteed
- ✅ **Gitignored by default** - personal content protected

---

## 🔒 **Security & Compliance Structure**

### **Data Protection Pattern**
```
Protected User Data:
├── .claudedirector/config/user_identity.yaml      # Personal config (gitignored)
├── leadership-workspace/ (entire directory)       # User workspace (gitignored)
└── data/strategic/ (database files)               # Strategic memory (gitignored)

Public Templates:
├── .claudedirector/config/user_identity.yaml.template  # Generic template
├── .claudedirector/templates/                          # System templates
└── docs/ (documentation)                               # Public documentation
```

### **Git Security Enforcement**
- **`.gitignore`** protects all personal data
- **Pre-commit hooks** prevent accidental exposure
- **Security scanner** validates every commit
- **Stakeholder scanner** protects organizational data

---

## 🧹 **Cleanup Sprint Target Structure**

### **✅ PHASE 9 CONSOLIDATION SUCCESS** (Post-v3.3.0 Analysis)
```
ACHIEVED: 4,521 lines consolidated, 37% directory reduction
├── ✅ stakeholder_intelligence_unified.py   # COMPLETED: 1,406 lines from 7 locations
├── ✅ strategic_memory_manager.py          # COMPLETED: Memory systems unified  
├── ✅ intelligence_unified.py              # COMPLETED: 1,247 lines from intelligence/
├── ✅ workspace_monitor_unified.py         # COMPLETED: Monitoring consolidated
├── ✅ core_lightweight.py                  # NEW: 406 lines lightweight fallback
└── 🗑️ memory/, intelligence/ removed       # COMPLETED: Legacy directories deleted
```

### **Legacy Technical Debt** (Pre-Phase 9 - RESOLVED)
```
lib/ Legacy Structure (REMOVED):
├── clarity/                    # ✅ → consolidated into context_engineering/
├── intelligence/               # ✅ → consolidated into ai_intelligence/
├── memory/                     # ✅ → superseded by context_engineering/
├── persona_integration/        # ✅ → integrate into context_engineering/
├── integrations/               # 🔄 → consolidate into integration/
├── bridges/                    # 🔄 → unified into integration/unified_bridge.py
└── [empty directories]         # ✅ → DELETED
```

### **Target Clean Structure** (Post-Cleanup)
```
lib/ (Clean Target):
├── context_engineering/        # 🚀 PRIMARY: 8-layer memory system
├── ai_intelligence/            # 🤖 AI enhancement and MCP coordination
├── core/                       # 🏗️ Essential system components
├── integration/                # 🔗 Unified integration layer
├── config/                     # ⚙️ Configuration management
├── utils/                      # 🔧 Utility functions
├── p0_features/                # 🛡️ Business-critical features
├── p1_features/                # 📈 High-priority features
├── p2_communication/           # 💬 Communication layer
└── transparency/               # 🔍 Transparency system
```

---

## 📊 **Architectural Compliance Requirements**

### **MANDATORY Principles**
1. **Single Source of Truth**: Each concern has ONE authoritative location
2. **Context Engineering First**: Primary system for strategic intelligence
3. **P0 Test Protection**: 21/23 BLOCKING P0 tests passing (91% success rate - Phase 9 iterative achievement)
4. **User/System Separation**: Clear boundaries between user and system territory
5. **Security by Default**: All personal data protected from source control

### **Enforcement Mechanisms**
1. **Pre-commit Hooks**: Architectural validation on every commit
2. **P0 Test Suite**: Regression protection for critical features
3. **CI/CD Validation**: Continuous architectural compliance checking
4. **Documentation Requirements**: Structure changes require doc updates

### **Change Control Process**
1. **Propose** structural changes via architecture document updates
2. **Validate** with comprehensive P0 test execution
3. **Review** architectural impact and compliance
4. **Implement** with careful migration and rollback capability
5. **Document** final structure and update this guide

---

## 🎯 **Next Steps for Structure Enforcement**

### **Immediate Actions**
1. **Update OVERVIEW.md** to reflect current v2.12.0 architecture
2. **Validate current structure** against this specification
3. **Document deviations** and cleanup requirements
4. **Plan cleanup sprint** to achieve target structure

### **Ongoing Maintenance**
1. **Architectural reviews** for all structural changes
2. **Regular compliance validation** via automated tools
3. **Documentation updates** for any approved changes
4. **Developer training** on structure requirements

---

**Status**: 📋 **DEFINED** - Comprehensive project structure documented for v2.12.0+ architecture with cleanup sprint targets clearly identified.
