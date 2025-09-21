# Weekly Retrospective System

**Status**: Phase 1 Planning - DRY Compliance Required
**Architecture**: TRUE Extension Pattern - Reuse Existing Infrastructure

## Overview

Personal weekly reflection system with 3 standardized questions. STANDALONE implementation with NO JIRA dependencies.

> **IMPORTANT**: This has NOTHING to do with JIRA. Completely separate from `specs/003-weekly-report-agent-phase2/` (business intelligence). This system handles ONLY personal reflection - no business data, no project tracking, no team metrics.

### Questions
1. **Progress**: "What progress did I make this week?"
2. **Improvement**: "How could I have done better?"
3. **Rating**: "On a scale of 1-10, how did I rate my week and why?"

## Architecture

**STANDALONE Strategy** - NO JIRA dependencies, reuse only non-business infrastructure:

```
EXISTING INFRASTRUCTURE (NON-JIRA ONLY):
├── StrategicMemoryManager          → Session management
├── AnalyticsEngine                 → Basic analytics (personal only)
├── RetrospectiveValidator          → Input validation
├── UserIdentity                    → User configuration
└── DatabaseManager                 → Data persistence

STANDALONE IMPLEMENTATION:
├── retrospective_schema.sql        → Database schema extension
├── /retrospective command          → Standalone command system
└── PersonalRetrospectiveSystem     → Standalone personal reflection class

EXPLICITLY EXCLUDED (NO JIRA):
├── ❌ WeeklyReporter               → JIRA business intelligence
├── ❌ JiraClient                   → JIRA API connections
├── ❌ BusinessValueFramework       → Business metrics analysis
└── ❌ Any ChatEnhancedWeeklyReporter → JIRA-based chat systems
```

## Usage

```bash
# Start retrospective
/retrospective

# Alternative commands
/weekly-retrospective
/reflection
```

## Implementation

**Phase 1**: 🎯 TRUE Extension Implementation (reuse existing infrastructure)
**Phase 2**: 📊 Multi-step conversations
**Phase 3**: 📈 Trend analysis
**Phase 4**: 🤖 Advanced insights generation

## Implementation Requirements

### ✅ BLOAT_PREVENTION Compliance
- **✅ No New Infrastructure**: Reuse existing StrategicMemoryManager, AnalyticsEngine
- **✅ Database Extension Only**: Add retrospective_schema.sql
- **✅ Minimal Command Mapping**: Single /retrospective command

### ✅ DRY Principles
- **✅ Session Management**: Use existing StrategicMemoryManager
- **✅ MCP Integration**: Use existing RETROSPECTIVE_ANALYSIS pattern
- **✅ Validation**: Use existing RetrospectiveValidator
- **✅ Analytics**: Use existing AnalyticsEngine retrospective support

### ✅ PROJECT_STRUCTURE Compliance
- **✅ Component Placement**: Extend existing chat infrastructure
- **✅ Database Schema**: Follow existing SQLite conventions
- **✅ Minimal Footprint**: <50 lines of new code

See: `tasks-phase1.md` for implementation details.
