# Daily Planning Command Recognition & Behavioral Constraint Fixes - PATTERN COMPLIANT

**Feature ID**: 006-daily-planning-command-fixes
**Author**: Martin | Platform Architecture
**Date**: 2025-09-23
**Status**: SPECIFICATION - COMMAND PATTERN COMPLIANCE VALIDATED
**Priority**: P0 - CRITICAL USER EXPERIENCE FAILURE

---

## 🎯 **SEQUENTIAL THINKING + CONTEXT7 PATTERN ANALYSIS**

### **Step 1: Problem Definition**
Daily planning commands **violate established pattern consistency**:
1. **Command Recognition**: Uses inconsistent pattern vs. established `/retrospective` commands
2. **Behavioral Constraints**: AI expands planning into troubleshooting vs. documentation

### **Step 2: Root Cause Analysis - Context7 Pattern Analysis**
**Established Pattern (WORKING)**:
```python
# PersonalRetrospectiveAgent - SUCCESSFUL PATTERN
"/retrospective create"  # Interactive session start
"/retrospective view"    # Display recent entries
"/retrospective help"    # Show available commands
```

**Current Pattern (BROKEN)**:
```python
# DailyPlanningManager - INCONSISTENT PATTERN
"daily plan start"   # No slash prefix - violates established pattern
"daily plan status"  # No slash prefix - not recognized by ConversationalInteractionManager
"daily plan review"  # No slash prefix - breaks user expectations
```

### **Step 3: Solution Architecture - Pattern Consistency**
**BLOAT_PREVENTION_SYSTEM.md COMPLIANT**: Use existing `/retrospective` command routing pattern

**Corrected Commands (CONSISTENT)**:
```python
# ARCHITECTURALLY COMPLIANT PATTERN
"/daily-plan start"   # Matches /retrospective pattern exactly
"/daily-plan status"  # Consistent slash prefix + hyphenation
"/daily-plan review"  # Follows established naming convention
"/daily-plan help"    # Complete pattern consistency
```

### **Step 4: Implementation Strategy - Existing Pattern Reuse**
**PROJECT_STRUCTURE.md COMPLIANT**: Enhance existing ConversationalInteractionManager routing

### **Step 5: Strategic Enhancement - Context7 Pattern Utilization**
- **Slash Command Pattern**: Leverage existing `/retrospective` routing architecture
- **Behavioral Constraint Pattern**: Use PersonalRetrospectiveAgent session management model
- **Integration Coordination Pattern**: Same routing as retrospective commands

### **Step 6: Success Metrics**
- **Pattern Consistency**: 100% alignment with `/retrospective` command structure
- **Command Recognition**: 100% success rate using existing slash command routing
- **User Experience**: Consistent expectations across personal productivity features

---

## 📋 **FUNCTIONAL REQUIREMENTS**

### **F1: Slash Command Pattern Compliance**
**EXISTING PATTERN REUSE** - Zero new routing logic
- **Commands**:
  - `/daily-plan start` (matches `/retrospective create` pattern)
  - `/daily-plan status` (matches `/retrospective view` pattern)
  - `/daily-plan review` (matches `/retrospective view` pattern)
  - `/daily-plan help` (matches `/retrospective help` pattern)
- **Integration**: Use existing `_handle_retrospective_command` pattern for `_handle_daily_plan_command`

### **F2: Interactive Session Management**
**EXISTING PATTERN REUSE** - PersonalRetrospectiveAgent session model
- **Session State**: Reuse `active_sessions` pattern from PersonalRetrospectiveAgent
- **User Interaction**: Same interactive flow as retrospective 3-question format
- **Behavioral Constraints**: Apply PLANNING mode during interactive sessions

### **F3: Command Routing Integration**
**EXISTING INFRASTRUCTURE ENHANCEMENT** - ConversationalInteractionManager
- **Location**: `lib/mcp/conversational_interaction_manager.py`
- **Pattern**: Add `_handle_daily_plan_command` following `_handle_retrospective_command` model
- **Integration**: Use existing RETROSPECTIVE_COMMAND intent classification pattern

### **F4: Behavioral Mode Enforcement**
**EXISTING BASEMANAGER PATTERN** - No new constraint system
- **Planning Mode**: Documentation-only constraints during `/daily-plan` sessions
- **Session Isolation**: Behavioral constraints only active during planning commands
- **Pattern Consistency**: Same constraint model as PersonalRetrospectiveAgent focus

---

## 🏗️ **TECHNICAL ARCHITECTURE - PATTERN REUSE**

### **A1: Slash Command Recognition Enhancement**
```python
# ENHANCE EXISTING: lib/mcp/conversational_interaction_manager.py
# FOLLOW RETROSPECTIVE PATTERN EXACTLY

class InteractionIntent(Enum):  # EXISTING ENUM
    # ... existing intents ...
    DAILY_PLAN_COMMAND = "daily_plan_command"  # ADD (matches RETROSPECTIVE_COMMAND pattern)

# REUSE EXISTING SLASH COMMAND DETECTION
async def _handle_daily_plan_command(
    self, query: str, current_context: Dict[str, Any] = None
) -> UnifiedResponse:
    """Handle daily planning commands - FOLLOWS _handle_retrospective_command PATTERN"""

    # Parse daily planning command from query (same pattern as retrospective)
    query_lower = query.lower().strip()
    user_id = current_context.get("user_id", "default_user") if current_context else "default_user"

    # Extract command and user input (EXACT SAME LOGIC as retrospective)
    if "/daily-plan start" in query_lower:
        command = "/daily-plan start"
    elif "/daily-plan status" in query_lower:
        command = "/daily-plan status"
    elif "/daily-plan review" in query_lower:
        command = "/daily-plan review"
    elif "/daily-plan help" in query_lower:
        command = "/daily-plan help"
    # ... SAME PATTERN as retrospective command parsing
```

### **A2: Session Management Pattern Reuse**
```python
# ENHANCE EXISTING: lib/automation/daily_planning_manager.py
# FOLLOW PersonalRetrospectiveAgent SESSION PATTERN

class DailyPlanningManager(BaseManager):  # EXISTING CLASS
    def __init__(self, config_path: Optional[str] = None):
        # ... existing initialization ...
        self.active_sessions = {}  # SAME PATTERN as PersonalRetrospectiveAgent

    def process_request(self, request_data: Dict[str, Any]) -> ProcessingResult:
        """FOLLOWS PersonalRetrospectiveAgent.process_request PATTERN"""
        command = request_data.get("command", "help")
        user_id = request_data.get("user_id", "default")
        user_input = request_data.get("user_input", "")

        # SAME PATTERN: Interactive chat commands
        if command.startswith("/daily-plan"):
            return self._handle_chat_command(user_id, command, user_input)
        elif user_id in self.active_sessions:
            return self._handle_session_input(user_id, user_input)
        # ... EXACT SAME PATTERN as PersonalRetrospectiveAgent
```

### **A3: Behavioral Mode Integration**
```python
# ENHANCE EXISTING: lib/core/base_manager.py
# ADD BEHAVIORAL MODE TO EXISTING PATTERN

class BaseManager:  # EXISTING CLASS
    def __init__(self, config: BaseManagerConfig):
        # ... existing initialization ...
        self.behavior_mode = "normal"  # ADD TO EXISTING

    def activate_planning_mode(self):
        """Activate planning behavioral constraints"""
        self.behavior_mode = "planning"
        # Behavioral constraints applied via AI prompt engineering
```

---

## 📊 **ARCHITECTURAL COMPLIANCE VALIDATION**

### **✅ PATTERN CONSISTENCY ACHIEVED**
- **Command Structure**: `/daily-plan` matches `/retrospective` pattern exactly
- **Session Management**: Reuses PersonalRetrospectiveAgent interactive session model
- **Routing Logic**: Same ConversationalInteractionManager slash command handling
- **User Experience**: Consistent expectations across personal productivity features

### **✅ BLOAT_PREVENTION_SYSTEM.md COMPLIANCE**
- **Zero New Patterns**: Reuses established `/retrospective` command routing
- **DRY Principle**: Leverages existing slash command detection and session management
- **No Duplication**: Single source of truth for slash command routing maintained

### **✅ PROJECT_STRUCTURE.md COMPLIANCE**
- **Existing Component Enhancement**: All changes within established architecture
- **Domain Boundaries**: MCP, automation, core layers properly utilized
- **Integration Coordination**: Same cross-system coordination as retrospective commands

---

## 🎯 **IMPLEMENTATION PLAN PREVIEW**

### **Phase 1: Command Pattern Alignment** (20 minutes)
- **File**: `lib/mcp/conversational_interaction_manager.py`
- **Change**: Add `/daily-plan` command detection following `/retrospective` pattern
- **Pattern**: Copy `_handle_retrospective_command` → `_handle_daily_plan_command`

### **Phase 2: Session Management Pattern Reuse** (30 minutes)
- **File**: `lib/automation/daily_planning_manager.py`
- **Change**: Add `active_sessions` and interactive session handling
- **Pattern**: Copy PersonalRetrospectiveAgent session management model

### **Phase 3: Behavioral Mode Activation** (20 minutes)
- **File**: `lib/core/base_manager.py`
- **Change**: Add planning mode activation during `/daily-plan` sessions
- **Pattern**: Simple mode flag for AI prompt engineering

### **Phase 4: Integration Testing** (10 minutes)
- **Validation**: End-to-end `/daily-plan start` session testing
- **Pattern**: Same testing approach as `/retrospective create`

**Total Effort**: 1.5 hours (vs. 2+ hours for non-pattern-compliant approach)

---

## 🚀 **BUSINESS VALUE**

### **User Experience Excellence**
- **Consistent Commands**: Users expect `/daily-plan` after learning `/retrospective`
- **Predictable Behavior**: Same interaction model across personal productivity features
- **Reduced Learning Curve**: Existing `/retrospective` users immediately understand `/daily-plan`

### **Architectural Excellence**
- **Pattern Consistency**: All personal productivity features follow same command model
- **Maintainability**: Single pattern to maintain vs. multiple command approaches
- **Future-Proof**: New personal productivity features can follow same established pattern

### **Development Efficiency**
- **Rapid Implementation**: 1.5-hour fix using proven patterns
- **Low Risk**: Reusing successful PersonalRetrospectiveAgent patterns
- **Easy Testing**: Existing test infrastructure covers pattern-compliant commands

---

**Final Approval**: ✅ **PATTERN COMPLIANT**
- **Command Consistency**: ✅ `/daily-plan` matches `/retrospective` pattern
- **BLOAT_PREVENTION_SYSTEM.md**: ✅ Zero new patterns, reuses existing architecture
- **PROJECT_STRUCTURE.md**: ✅ Enhances existing components following established domain boundaries
- **Context7 Pattern Utilization**: ✅ Leverages proven PersonalRetrospectiveAgent success patterns

---

*This specification follows established ClaudeDirector command patterns with Sequential Thinking + Context7 architectural compliance.*
