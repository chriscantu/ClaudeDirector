# Retrospective Command Integration Fix - Spec Kit

## Problem Statement

The retrospective feature has 3 critical failures:
1. **No `/retrospective` command** - Missing proper chat command integration
2. **Manual code execution** - Had to write Python code instead of natural chat interaction
3. **Missing 4th question** - No "How would I rate this week on a scale of 1-10?" question

## Root Cause Analysis

**Primary Issue**: `RETROSPECTIVE_AVAILABLE = False` in `conversational_interaction_manager.py:58`
- The retrospective agent exists but is disabled in the command routing system
- Intent patterns are configured but not activated
- Missing integration with the main chat command processor

## Solution Architecture

### 1. Enable Retrospective Agent Integration
**File**: `.claudedirector/lib/mcp/conversational_interaction_manager.py`
- Change `RETROSPECTIVE_AVAILABLE = False` to `True`
- Add retrospective agent initialization
- Follow exact same pattern as `daily_planning_manager`

### 2. Add Missing 4th Question
**File**: `.claudedirector/lib/agents/personal_retrospective_agent.py`
- Add rating question to the 3-question framework
- Update database schema to include `rating` field
- Update session handling to capture rating

### 3. Fix Command Routing
**File**: `.claudedirector/lib/mcp/conversational_interaction_manager.py`
- Ensure `_handle_retrospective_command` properly delegates to agent
- Follow exact same pattern as `_handle_daily_plan_command`

## Implementation Plan

### Phase 1: Enable Agent Integration (15 minutes)
1. Set `RETROSPECTIVE_AVAILABLE = True`
2. Add retrospective agent property following daily-planning pattern
3. Initialize agent in constructor

### Phase 2: Add Rating Question (10 minutes)
1. Update database schema to include `rating` field
2. Add 4th question to session flow
3. Update completion logic to save rating

### Phase 3: Test Integration (5 minutes)
1. Test `/retrospective create` command
2. Verify 4-question flow works
3. Test `/retrospective view` shows ratings

## Files to Modify

1. `.claudedirector/lib/mcp/conversational_interaction_manager.py` - Enable integration
2. `.claudedirector/lib/agents/personal_retrospective_agent.py` - Add rating question
3. `.claudedirector/config/weekly_report_config.yaml.template` - Update config

## Success Criteria

- ✅ `/retrospective create` works as natural chat command
- ✅ 4-question flow: went well, could improve, next focus, rating (1-10)
- ✅ `/retrospective view` shows complete entries with ratings
- ✅ No manual Python code execution required
- ✅ Follows exact same pattern as `/daily-plan` commands

## Architecture Compliance

- **DRY**: Reuses existing command routing patterns
- **SOLID**: Single responsibility for each component
- **BLOAT_PREVENTION**: No code duplication, follows established patterns
- **PROJECT_STRUCTURE**: All changes in existing files, no new directories

## Estimated Effort: 30 minutes total
- Phase 1: 15 minutes (agent integration)
- Phase 2: 10 minutes (rating question)
- Phase 3: 5 minutes (testing)
