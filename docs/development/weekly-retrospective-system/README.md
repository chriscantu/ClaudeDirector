# Weekly Retrospective System

**Status**: Phase 1 Planning - DRY Compliance Required
**Architecture**: TRUE Extension Pattern - Reuse Existing Infrastructure

## Overview

Personal weekly reflection system with 3 standardized questions. Must REUSE existing ClaudeDirector infrastructure (no duplicates).

> **Note**: This is completely separate from `specs/003-weekly-report-agent-phase2/` (business intelligence). This system handles personal reflection only.

### Questions
1. **Progress**: "What progress did I make this week?"
2. **Improvement**: "How could I have done better?"
3. **Rating**: "On a scale of 1-10, how did I rate my week and why?"

## Architecture

**Extension Strategy** - REUSE existing components:

```
EXISTING INFRASTRUCTURE (MUST REUSE):
├── StrategicMemoryManager          → Session management
├── AnalyticsEngine                 → Retrospective analysis support
├── RetrospectiveValidator          → Input validation
├── MCPIntegrationManager           → RETROSPECTIVE_ANALYSIS pattern
├── UserIdentity                    → User configuration
└── DatabaseManager                 → Data persistence

REQUIRED ADDITIONS:
├── retrospective_schema.sql        → Database schema extension
├── /retrospective command          → Command mapping only
└── RetrospectiveEnabledChatReporter → Minimal extension class
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
