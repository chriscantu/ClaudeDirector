# Enhanced ClaudeDirector Commands
**Session Context Preservation and Recovery Commands**

## Overview

Enhanced command set for ClaudeDirector framework with automatic session context preservation, intelligent recovery, and strategic continuity across restarts.

---

## Core Session Management Commands

### `/session-start [type]`
**Purpose**: Start new session with context tracking
**Usage**: `/session-start strategic`
**Example**:
```bash
/session-start executive
# Output: ✅ Strategic session started (ID: abc123...)
```

### `/session-status`
**Purpose**: Show current session context status and quality
**Usage**: `/session-status`
**Example**:
```bash
/session-status
# Output:
# ✅ Strategic session ready (Context quality: 87%)
# Session ID: abc123
# Context Gaps: 0
# Last Backup: 2 minutes ago
```

### `/session-backup`
**Purpose**: Manually trigger context backup
**Usage**: `/session-backup`
**Example**:
```bash
/session-backup
# Output: ✅ Context backup completed (Quality: 92%)
```

### `/session-restore [session-id]`
**Purpose**: Restore specific session context
**Usage**: `/session-restore abc123`
**Example**:
```bash
/session-restore abc123
# Output: 🔄 Restoring session context...
#         ✅ Context restored (Quality: 87%)
#         ⚠️  2 context gaps detected - see /context-recover
```

---

## Context Management Commands

### `/context-validate`
**Purpose**: Check for context gaps and completeness
**Usage**: `/context-validate`
**Example**:
```bash
/context-validate
# Output:
# ✅ Context Validation Results:
# - Stakeholder context: Complete ✅
# - Strategic initiatives: Complete ✅
# - Executive context: Missing ⚠️
# - ROI discussions: Incomplete ⚠️
#
# Overall Quality: 67%
# Recommendation: Run /context-recover for missing context
```

### `/context-recover`
**Purpose**: Interactive context recovery with guided prompts
**Usage**: `/context-recover`
**Example**:
```bash
/context-recover
# Output:
# 🔄 **Context Recovery Required**
#
# Before continuing strategic work, please refresh the following context:
#
# 1. **Executive session preparation incomplete**
#    - Please provide recent executive session context and preparations
#
# 2. **ROI strategy conversations missing**
#    - Please refresh ROI strategy discussions and current positioning
#
# Please provide the missing context so we can continue effectively.
```

### `/context-quality`
**Purpose**: Show detailed context completeness scoring
**Usage**: `/context-quality`
**Example**:
```bash
/context-quality
# Output:
# 📊 Context Quality Analysis:
#
# Stakeholder Context: ████████░░ 80%
# Strategic Initiatives: ██████████ 100%
# Executive Context: ██████░░░░ 60%
# ROI Discussions: ████░░░░░░ 40%
# Coalition Mapping: ███████░░░ 70%
#
# Overall Quality: 74%
# Status: Good - Minor gaps detected
```

---

## Strategic Context Commands

### `/stakeholder-update [key] [details]`
**Purpose**: Update stakeholder context and trigger backup
**Usage**: `/stakeholder-update steve_davis "wants ROI understanding, open to evidence-based platform case"`
**Example**:
```bash
/stakeholder-update hemendra_pal "product-focused, not strong platform advocate"
# Output: ✅ Stakeholder context updated
#         🔄 Context backup triggered
#         📊 Context quality improved to 82%
```

### `/initiative-update [key] [status] [details]`
**Purpose**: Update strategic initiative status and context
**Usage**: `/initiative-update PI-14741 at_risk "resource reallocation needed"`
**Example**:
```bash
/initiative-update PI-14741 in_progress "platform investment ROI case development"
# Output: ✅ Initiative context updated
#         🔄 Context backup triggered
```

### `/executive-prep [stakeholder] [context]`
**Purpose**: Store executive session preparation context
**Usage**: `/executive-prep steve_davis "ROI presentation preparation"`
**Example**:
```bash
/executive-prep steve_davis "ROI platform investment discussion, coalition building focus"
# Output: ✅ Executive context stored
#         📋 Session preparation saved
#         🔄 Context backup triggered
```

### `/roi-context [discussion-details]`
**Purpose**: Store ROI strategy discussion context
**Usage**: `/roi-context "Platform investment → productivity gains → business value"`
**Example**:
```bash
/roi-context "Target stakeholder wants $200K ROI demo, focus on productivity gains and competitive advantage"
# Output: ✅ ROI context stored
#         💰 Investment strategy preserved
#         🔄 Context backup triggered
```

---

## Memory and Intelligence Commands

### `/memory-recall [type] [filter]`
**Purpose**: Recall stored strategic memory with context
**Usage**: `/memory-recall executive_sessions stakeholder=steve_davis`
**Example**:
```bash
/memory-recall strategic_initiatives status=in_progress
# Output:
# 📋 Found 3 strategic initiatives:
#
# PI-14741: Platform Investment ROI Case
#   Status: in_progress
#   Priority: high
#   Assignee: Chris Cantu
#   Business Value: $200K+ productivity gains
#
# PI-15628: New Relic Migration
#   Status: in_progress
#   Priority: medium
#   Business Value: Cost optimization + compliance
```

### `/stakeholder-map`
**Purpose**: Show current stakeholder coalition mapping
**Usage**: `/stakeholder-map`
**Example**:
```bash
/stakeholder-map
# Output:
# 🗺️  **Stakeholder Coalition Map**
#
# **Platform Advocates** ✅
# - SLT Ally: Platform strategy supporter
# - Platform Advocate: Platform expertise and advocacy
# - Technical Authority: Technical leadership
# - Architecture Lead: Architecture validation
#
# **Platform Opposition** ❌
# - Director A: Product delivery focus
# - SLT Member B: 100% product focused, conflicts with advocates
#
# **Unclear/Target** ❓
# - VP Engineering: Wants ROI understanding (TARGET)
# - Marfise: Potential advocate, unclear pressure
```

### `/framework-health`
**Purpose**: Complete framework health and performance check
**Usage**: `/framework-health`
**Example**:
```bash
/framework-health
# Output:
# 🏥 **ClaudeDirector Framework Health**
#
# Session Management: ✅ Operational
# Memory System: ✅ Operational (99.2% uptime)
# Context Preservation: ✅ Active (Last backup: 3 min ago)
# Database Performance: ✅ Optimal (avg 15ms response)
#
# Active Sessions: 1
# Total Context Records: 247
# Backup Success Rate: 98.5%
#
# **Recommendations**: None - system operating optimally
```

---

## Advanced Recovery Commands

### `/context-gap-analysis`
**Purpose**: Detailed analysis of context gaps with recovery strategies
**Usage**: `/context-gap-analysis`
**Example**:
```bash
/context-gap-analysis
# Output:
# 🔍 **Context Gap Analysis**
#
# **High Priority Gaps**:
# 1. Executive Context Missing (Severity: HIGH)
#    Impact: Blocks VP/SLT preparation effectiveness
#    Recovery: Refresh recent executive interactions and decisions
#    Estimated Recovery Time: 5-10 minutes
#
# 2. ROI Discussion Thread Incomplete (Severity: MEDIUM)
#    Impact: Reduces business case development continuity
#    Recovery: Summarize recent ROI strategy conversations
#    Estimated Recovery Time: 3-5 minutes
```

### `/auto-recovery`
**Purpose**: Automatic context recovery using available data sources
**Usage**: `/auto-recovery`
**Example**:
```bash
/auto-recovery
# Output:
# 🤖 **Automatic Context Recovery**
#
# Scanning available data sources...
# ✅ Found 15 stakeholder references in recent documents
# ✅ Found 8 initiative references in Jira data
# ✅ Found 3 executive session references in calendar
#
# Auto-recovered context:
# - Stakeholder context: 23% improvement
# - Initiative context: 45% improvement
# - Executive context: 12% improvement
#
# Overall context quality: 67% → 78%
# Manual recovery still recommended for critical gaps
```

### `/context-checkpoint`
**Purpose**: Create manual context checkpoint for recovery
**Usage**: `/context-checkpoint "before target stakeholder ROI meeting"`
**Example**:
```bash
/context-checkpoint "pre-executive-session-preparation"
# Output: ✅ Context checkpoint created
#         📸 Snapshot ID: checkpoint_abc123
#         💾 All current context preserved
#         🔄 Available for future restoration
```

---

## Integration Commands

### `/framework-init`
**Purpose**: Initialize enhanced framework with context detection
**Usage**: `/framework-init`
**Example**:
```bash
/framework-init
# Output:
# 🚀 **Initializing ClaudeDirector Enhanced Framework**
#
# 🔍 Checking for previous sessions...
# 📋 Previous session detected (2 hours ago)
# 🔄 Initiating context recovery...
# ✅ Context restored (Quality: 87%)
# ⚠️  1 context gap detected - run /context-recover
#
# **Ready for strategic work** (with minor context recovery recommended)
```

### `/framework-upgrade`
**Purpose**: Upgrade existing ClaudeDirector to enhanced version
**Usage**: `/framework-upgrade`
**Example**:
```bash
/framework-upgrade
# Output:
# ⬆️  **Upgrading ClaudeDirector Framework**
#
# ✅ Session context schema created
# ✅ Enhanced memory manager initialized
# ✅ Context preservation system activated
# 🔄 Migrating existing data...
# ✅ Migration complete (247 records processed)
#
# **Enhanced framework ready** - automatic context preservation active
```

---

## Usage Patterns

### **Daily Strategic Work Pattern**
```bash
# Morning startup
/framework-init
/context-validate
/stakeholder-map

# During strategic work
/executive-prep steve_davis "ROI platform investment discussion"
/roi-context "Focus on $200K productivity gains, competitive advantage"

# End of day
/session-backup
```

### **Executive Preparation Pattern**
```bash
# Before executive meeting
/context-validate
/memory-recall executive_sessions stakeholder=steve_davis days=30
/stakeholder-update steve_davis "current context and positioning"
/executive-prep steve_davis "meeting agenda and strategic objectives"
```

### **Context Recovery Pattern**
```bash
# After restart/context loss
/framework-init
/context-recover
/context-gap-analysis
/auto-recovery
/context-validate
```

---

**Result**: Complete command interface for ClaudeDirector enhanced framework with systematic context preservation, intelligent recovery, and strategic session continuity.
