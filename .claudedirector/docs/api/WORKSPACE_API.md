# Workspace Management API

## Overview

ClaudeDirector provides intelligent workspace management for engineering leadership files, with automatic organization, lifecycle management, and smart archiving capabilities.

## Core Workspace Components

### WorkspaceFileHandler
**Purpose**: Central workspace file management and organization.

```python
from claudedirector.core.workspace_file_handler import WorkspaceFileHandler

# Initialize workspace handler
workspace = WorkspaceFileHandler()

# Core workspace operations
workspace_path = workspace.get_workspace_path()
files = workspace.list_workspace_files()
metadata = workspace.get_file_metadata(file_path)
```

**Key Methods**:
- `get_workspace_path()` → str: Get current workspace location
- `list_workspace_files()` → List[Path]: List all workspace files
- `create_file(path, content)` → bool: Create new file with lifecycle tracking
- `get_file_metadata(path)` → Dict: Get file metadata and lifecycle info
- `archive_file(path)` → bool: Archive file with indexing

### File Lifecycle Management

#### FileLifecycleManager
**Purpose**: Intelligent file generation, retention, and archiving.

```python
from claudedirector.core.file_lifecycle_manager import FileLifecycleManager

# Initialize lifecycle manager
lifecycle = FileLifecycleManager(workspace_path="~/leadership-workspace")

# File lifecycle operations
lifecycle.create_file_with_lifecycle(
    file_path="analysis/market-research.md",
    content="# Market Analysis\n...",
    retention_score=8.5,  # High value content
    generation_mode="professional"  # Quality level
)

# Check file lifecycle status
status = lifecycle.get_file_lifecycle_status("analysis/market-research.md")
print(f"Retention score: {status['retention_score']}")
print(f"Auto-archive date: {status['auto_archive_date']}")
```

**Generation Modes**:
- `minimal`: Essential content only, lower retention scores
- `professional`: Balanced content with good retention
- `research`: Comprehensive content with high retention scores

**Lifecycle Phases**:
1. **Creation**: File created with metadata and retention scoring
2. **Active Use**: Regular access extends retention period
3. **Aging**: Reduced access, eligible for archiving recommendations
4. **Archive**: Moved to archive with full-text search indexing

### Smart File Organization

#### SmartFileOrganizer
**Purpose**: Intelligent file consolidation and cross-session insights.

```python
from claudedirector.core.smart_file_organizer import SmartFileOrganizer

# Initialize smart organizer
organizer = SmartFileOrganizer(workspace_path="~/leadership-workspace")

# Identify consolidation opportunities
opportunities = organizer.identify_consolidation_opportunities()
for opp in opportunities:
    print(f"Consolidate: {opp.files} → {opp.suggested_name}")
    print(f"Confidence: {opp.confidence_score}")
    print(f"Reasoning: {opp.reasoning}")

# Apply consolidation
organizer.consolidate_files(opportunity=opportunities[0])

# Generate cross-session insights
insights = organizer.generate_cross_session_insights()
print(f"Most productive patterns: {insights['productive_patterns']}")
print(f"Content evolution: {insights['content_evolution']}")
```

**Consolidation Types**:
- **Topic-based**: Files on similar subjects
- **Temporal**: Files from same time period/session
- **Outcome-focused**: Files contributing to same goal
- **Reference**: Supporting materials and research

### Advanced Archiving

#### AdvancedArchivingSystem
**Purpose**: Full-text search and intelligent archive management.

```python
from claudedirector.core.advanced_archiving import AdvancedArchivingSystem

# Initialize advanced archiving
archiver = AdvancedArchivingSystem(
    workspace_path="~/leadership-workspace",
    archive_path="~/leadership-workspace/archived"
)

# Archive with full-text indexing
archiver.archive_file_with_indexing(
    file_path="old-project/requirements.md",
    tags=["requirements", "project-alpha", "2024-q1"],
    category="project-documentation"
)

# Search archived content
results = archiver.search_archived_files(
    query="authentication requirements",
    category="project-documentation",
    date_range=("2024-01-01", "2024-03-31")
)

for result in results:
    print(f"File: {result['file_path']}")
    print(f"Match: {result['snippet']}")
    print(f"Relevance: {result['score']}")
```

**Search Capabilities**:
- **Full-text search**: Content-based search with ranking
- **Metadata filtering**: By tags, category, date range
- **Similarity search**: Find related content
- **Historical tracking**: Access patterns and usage analytics

### Pattern Recognition

#### PatternRecognitionEngine
**Purpose**: Workflow optimization and template suggestions.

```python
from claudedirector.core.pattern_recognition import PatternRecognitionEngine

# Initialize pattern recognition
pattern_engine = PatternRecognitionEngine(workspace_path="~/leadership-workspace")

# Update patterns from recent usage
pattern_engine.update_patterns_from_usage(
    session_files=["standup-notes.md", "action-items.md", "decisions.md"],
    session_outcome="successful_planning",
    duration_minutes=45
)

# Get pattern insights
insights = pattern_engine.get_pattern_insights()
print(f"Most effective workflows: {insights['top_workflows']}")
print(f"Optimal session length: {insights['optimal_duration']}")
print(f"Success indicators: {insights['success_patterns']}")

# Get workflow optimization suggestions
suggestions = pattern_engine.suggest_workflow_optimizations()
for suggestion in suggestions:
    print(f"Optimization: {suggestion['description']}")
    print(f"Expected impact: {suggestion['impact_score']}")
```

**Pattern Types**:
- **Workflow patterns**: Successful file creation sequences
- **Timing patterns**: Optimal session durations and scheduling
- **Content patterns**: Effective document structures
- **Outcome patterns**: Factors leading to successful sessions

## Workspace Configuration

### Configuration Options
```python
# Default workspace configuration
workspace_config = {
    "generation_mode": "professional",           # Content quality level
    "consolidate_analysis": True,               # Enable smart consolidation
    "max_session_files": 20,                    # Files per session limit
    "auto_archive_days": 30,                    # Days before auto-archive eligibility
    "pattern_tracking": True,                   # Enable workflow pattern learning
    "advanced_search": True,                    # Enable full-text archive search
    "retention_scoring": True,                  # Enable automatic retention scoring
    "cross_session_insights": True              # Enable productivity analytics
}
```

### Workspace Structure
```
~/leadership-workspace/
├── current-initiatives/          # Active projects and initiatives
├── meeting-prep/                 # Meeting preparation and notes
├── analysis-results/             # Strategic analysis outputs
├── decisions/                    # Decision records and rationale
├── templates/                    # Reusable templates and frameworks
├── archived/                     # Archived files with search index
│   ├── index.db                 # SQLite full-text search index
│   └── 2024/                    # Archived files by year
├── file_metadata.json           # File lifecycle metadata
└── .workspace_config.yaml       # Workspace configuration
```

## Workspace Operations

### File Creation with Lifecycle
```python
# Create strategic analysis with high retention
workspace.create_strategic_analysis(
    title="Platform Architecture Decision",
    content=analysis_content,
    stakeholders=["CTO", "VP Engineering"],
    frameworks=["WRAP Decision Framework"],
    retention_days=90  # Extended retention for strategic decisions
)

# Create meeting notes with standard retention
workspace.create_meeting_notes(
    meeting_type="standup",
    attendees=["team_alpha"],
    content=notes_content,
    retention_days=14  # Standard retention for regular meetings
)
```

### Batch Operations
```python
# Batch archive old files
old_files = workspace.find_files_older_than(days=60)
results = workspace.batch_archive(
    files=old_files,
    preserve_structure=True,
    create_index=True
)

# Batch consolidation of related files
related_groups = organizer.group_related_files(
    directory="current-initiatives/",
    similarity_threshold=0.7
)

for group in related_groups:
    consolidated = organizer.consolidate_file_group(group)
    print(f"Consolidated {len(group)} files into {consolidated}")
```

### Search and Discovery
```python
# Search across workspace and archives
results = workspace.search_all_content(
    query="team scaling strategy",
    include_archived=True,
    date_range="last_6_months",
    file_types=["md", "txt"]
)

# Find files by pattern or template
template_files = workspace.find_files_by_pattern(
    pattern="strategic_analysis_*",
    framework="Team Topologies"
)

# Get recommendations based on current context
recommendations = workspace.get_content_recommendations(
    current_files=["platform-strategy.md"],
    context="architecture_decision"
)
```

## Integration Examples

### With Strategic Frameworks
```python
# Workspace integrates with framework engine
framework_result = framework_engine.analyze_strategic_context(context)

# Automatically create structured files based on framework
if "Rumelt Strategy Kernel" in framework_result['activated_frameworks']:
    workspace.create_from_template(
        template="rumelt_strategy_analysis",
        context=framework_result,
        auto_populate=True
    )
```

### With AI Detection
```python
# Workspace can trigger AI analysis
stakeholders_in_file = workspace.extract_stakeholders(file_path)
tasks_in_file = workspace.extract_tasks(file_path)

# Update file metadata with AI insights
workspace.update_file_metadata(
    file_path,
    stakeholders=stakeholders_in_file,
    tasks=tasks_in_file,
    ai_analysis_date=datetime.now()
)
```

### With Performance Monitoring
```python
# Track workspace performance metrics
metrics = workspace.get_performance_metrics()
print(f"Files created this week: {metrics['files_created']}")
print(f"Average file retention: {metrics['avg_retention_days']}")
print(f"Archive utilization: {metrics['archive_search_frequency']}")
print(f"Consolidation efficiency: {metrics['consolidation_ratio']}")
```

## Migration and Compatibility

### Legacy Workspace Migration
```python
# Migrate from old 'engineering-director-workspace'
migrator = WorkspaceMigrator()

migration_result = migrator.migrate_workspace(
    old_path="~/engineering-director-workspace",
    new_path="~/leadership-workspace",
    preserve_history=True,
    update_references=True
)

print(f"Migrated {migration_result['files_moved']} files")
print(f"Updated {migration_result['references_updated']} references")
```

### Backup and Restore
```python
# Create workspace backup
backup_path = workspace.create_backup(
    include_archives=True,
    compress=True,
    exclude_temporary=True
)

# Restore from backup
restore_result = workspace.restore_from_backup(
    backup_path=backup_path,
    target_workspace="~/leadership-workspace-restored",
    verify_integrity=True
)
```

## Error Handling

### Workspace Exceptions
```python
from claudedirector.core.exceptions import (
    WorkspaceError,
    FileLifecycleError,
    ArchivingError
)

try:
    workspace.create_file(path, content)
except WorkspaceError as e:
    logger.error(f"Workspace operation failed: {e}")
except FileLifecycleError as e:
    logger.error(f"File lifecycle error: {e}")
except ArchivingError as e:
    logger.error(f"Archiving failed: {e}")
```

### Data Protection
```python
# Workspace operations respect data protection rules
try:
    # This will fail if trying to archive files with retention overrides
    workspace.force_archive(file_with_retention_override)
except DataProtectionError as e:
    print(f"Cannot archive: {e.message}")
    print(f"Retention override until: {e.retention_date}")
```

## Performance Considerations

### Optimization Settings
```python
# Optimize for different usage patterns
workspace_config = {
    # For heavy content creation
    "content_creator": {
        "max_session_files": 50,
        "auto_save_interval": 300,  # 5 minutes
        "pattern_analysis": "detailed"
    },
    
    # For strategic analysis
    "strategic_analyst": {
        "retention_default": 60,  # days
        "consolidation_threshold": 0.8,
        "framework_integration": True
    },
    
    # For team leadership
    "team_leader": {
        "stakeholder_tracking": True,
        "meeting_integration": True,
        "cross_session_insights": True
    }
}
```

### Performance Metrics
- **File Operations**: < 50ms for standard operations
- **Search Performance**: < 200ms for workspace search, < 500ms including archives
- **Pattern Recognition**: Updates in background, < 1s for insights
- **Archive Operations**: Batched for efficiency, < 2s per file with indexing

---

**Note**: All workspace operations respect user privacy and data protection. Files are never shared or transmitted outside the local workspace without explicit user action.
