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

**SIMPLE STANDALONE System** - No business intelligence, just personal reflection:

```
SIMPLE IMPLEMENTATION:
├── retrospective_enabled_chat_reporter.py → Simple 3-question system
├── RetrospectiveValidator (optional)       → Basic input validation
└── /retrospective command                  → Simple command system

SIMPLE STORAGE:
├── Session storage in memory              → Just for the 3 questions
└── Response storage in session           → Personal responses only

NO BUSINESS FEATURES:
├── ❌ JIRA integration                   → Not needed for personal reflection
├── ❌ Business metrics or KPIs           → Not needed for personal reflection
├── ❌ Strategic analysis                 → Not needed for personal reflection
├── ❌ Performance analytics              → Not needed for personal reflection
├── ❌ ROI calculations                   → Not needed for personal reflection
└── ❌ Monte Carlo simulations            → Not needed for personal reflection
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

## Implementation

### ✅ Simple Personal Retrospective
- **✅ 3 Questions Only**: Progress, Improvement, Rating (1-10)
- **✅ No Business Intelligence**: Personal reflection only
- **✅ Simple Storage**: In-memory session storage
- **✅ Minimal Code**: Single file implementation

### ✅ Focus Requirements
- **✅ Personal Use**: Individual weekly reflection
- **✅ No JIRA**: Completely standalone
- **✅ No Metrics**: No business KPIs or analytics
- **✅ No Strategy**: No strategic planning features

### ✅ Simple Architecture
- **✅ Single File**: retrospective_enabled_chat_reporter.py
- **✅ Basic Validation**: Optional input validation
- **✅ Memory Storage**: Simple session management

See: `tasks-phase1.md` for implementation details.
