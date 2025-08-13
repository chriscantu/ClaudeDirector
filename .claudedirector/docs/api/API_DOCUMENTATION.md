# ClaudeDirector API Documentation

## Overview

ClaudeDirector provides a comprehensive AI-powered engineering leadership toolkit with strategic frameworks, intelligent detection, and persistent memory capabilities.

## Core Modules

### 🧠 Intelligence Modules

#### StakeholderIntelligence
**Purpose**: AI-powered stakeholder detection and relationship management.

```python
from claudedirector.intelligence.stakeholder import StakeholderIntelligence

# Initialize with configuration
stakeholder_ai = StakeholderIntelligence(config=config)

# Core methods
stakeholders = stakeholder_ai.get_all_stakeholders()
stakeholder = stakeholder_ai.get_stakeholder(stakeholder_id)
profile = stakeholder_ai.create_stakeholder(stakeholder_data)
```

**Key Methods**:
- `get_all_stakeholders()` → List[Dict]: Get all detected stakeholders
- `get_stakeholder(id)` → Dict: Get specific stakeholder by ID
- `create_stakeholder(data)` → Dict: Create new stakeholder profile
- `update_stakeholder(id, data)` → Dict: Update existing stakeholder
- `delete_stakeholder(id)` → bool: Remove stakeholder

**Detection Capabilities**:
- Name extraction from text
- Role identification
- Confidence scoring (0.0-1.0)
- Context preservation
- Relationship mapping

#### TaskIntelligence
**Purpose**: AI-powered task detection and strategic task management.

```python
from claudedirector.intelligence.task import TaskIntelligence

# Initialize task intelligence
task_ai = TaskIntelligence(config=config)

# Core methods
tasks = task_ai.get_all_tasks()
task = task_ai.get_task(task_id)
new_task = task_ai.create_task(task_data)
```

**Key Methods**:
- `get_all_tasks()` → List[Dict]: Get all detected tasks
- `get_task(id)` → Dict: Get specific task by ID
- `create_task(data)` → Dict: Create new task
- `update_task(id, data)` → Dict: Update existing task
- `complete_task(id)` → bool: Mark task as completed

#### MeetingIntelligenceManager
**Purpose**: Meeting analysis and strategic insight extraction.

```python
from claudedirector.intelligence.meeting import MeetingIntelligenceManager

# Initialize meeting intelligence
meeting_ai = MeetingIntelligenceManager(config=config)

# Core methods
insights = meeting_ai.analyze_meeting(meeting_data)
summary = meeting_ai.generate_summary(meeting_id)
```

### ⚙️ Core Configuration

#### ClaudeDirectorConfig
**Purpose**: Centralized configuration management with environment override support.

```python
from claudedirector.core.config import ClaudeDirectorConfig, get_config

# Get default configuration
config = get_config()

# Create custom configuration
custom_config = ClaudeDirectorConfig(
    database_path="custom/path/memory.db",
    stakeholder_auto_create_threshold=0.90,
    task_auto_create_threshold=0.85,
    enable_caching=True
)
```

**Key Configuration Options**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `database_path` | str | "memory/strategic_memory.db" | SQLite database location |
| `stakeholder_auto_create_threshold` | float | 0.85 | Auto-create stakeholder confidence threshold |
| `stakeholder_profiling_threshold` | float | 0.65 | Profile stakeholder confidence threshold |
| `task_auto_create_threshold` | float | 0.80 | Auto-create task confidence threshold |
| `task_review_threshold` | float | 0.60 | Task review confidence threshold |
| `enable_caching` | bool | True | Enable intelligent caching |
| `enable_parallel_processing` | bool | True | Enable parallel AI processing |

### 🎯 Strategic Framework Engine

#### EmbeddedFrameworkEngine
**Purpose**: Research-backed strategic framework activation and guidance.

```python
from claudedirector.core.embedded_framework_engine import EmbeddedFrameworkEngine

# Initialize framework engine
framework_engine = EmbeddedFrameworkEngine()

# Analyze strategic context
result = framework_engine.analyze_strategic_context(
    user_input="Need to make strategic decision about platform architecture"
)

# Get framework recommendations
recommendations = result['recommendations']
activated_frameworks = result['activated_frameworks']
```

**Available Frameworks**:
1. **Rumelt Strategy Kernel** - Good Strategy/Bad Strategy principles
2. **WRAP Decision Framework** - Decisive decision-making process
3. **Scaling Up Excellence** - Organizational scaling strategies
4. **Team Topologies** - Team structure and communication patterns
5. **Accelerate** - High-performing team practices
6. **Crucial Conversations** - Stakeholder communication strategies
7. **Capital Allocation** - Strategic resource allocation

### 🗄️ Database Management

#### DatabaseManager
**Purpose**: SQLite-based persistent memory with schema management.

```python
from claudedirector.core.database import DatabaseManager

# Initialize database
db = DatabaseManager(db_path="memory/strategic_memory.db")

# Execute queries
results = db.execute_query("SELECT * FROM stakeholders WHERE role = ?", ("VP Engineering",))

# Manage schemas
db.create_table_if_not_exists("custom_table", schema_sql)
```

### 🔧 Utility Modules

#### Cache Management
```python
from claudedirector.utils.cache import CacheManager

cache = CacheManager(config=config)
cache.set("key", value, ttl=3600)  # 1 hour TTL
cached_value = cache.get("key")
```

#### Memory Optimization
```python
from claudedirector.utils.memory import MemoryOptimizer

optimizer = MemoryOptimizer(config=config)
optimizer.optimize_memory_usage()
stats = optimizer.get_memory_stats()
```

#### Parallel Processing
```python
from claudedirector.utils.parallel import ParallelProcessor

processor = ParallelProcessor(config=config)
results = processor.parallel_requests(requests_list, max_workers=4)
```

## Error Handling

### Exception Hierarchy

```python
from claudedirector.core.exceptions import (
    ClaudeDirectorError,
    AIDetectionError,
    DatabaseError,
    ConfigurationError,
    WorkspaceError
)

try:
    stakeholder = stakeholder_ai.get_stakeholder("invalid_id")
except AIDetectionError as e:
    print(f"AI Detection failed: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
except ClaudeDirectorError as e:
    print(f"General ClaudeDirector error: {e}")
```

### Common Error Scenarios

| Error Type | Common Causes | Solutions |
|------------|---------------|-----------|
| `ConfigurationError` | Invalid thresholds, missing config files | Validate configuration values |
| `DatabaseError` | Corrupted database, permission issues | Check database permissions, rebuild if needed |
| `AIDetectionError` | Invalid input, model failures | Validate input data, retry with different input |
| `WorkspaceError` | Missing workspace, file permission issues | Ensure workspace exists and is writable |

## Performance Considerations

### Optimization Guidelines

1. **Use Caching**: Enable caching for repeated operations
   ```python
   config.enable_caching = True
   ```

2. **Parallel Processing**: Enable for batch operations
   ```python
   config.enable_parallel_processing = True
   config.max_parallel_workers = 4
   ```

3. **Threshold Tuning**: Adjust AI detection thresholds based on use case
   ```python
   # Stricter detection (fewer false positives)
   config.stakeholder_auto_create_threshold = 0.90

   # More liberal detection (fewer false negatives)
   config.stakeholder_auto_create_threshold = 0.75
   ```

### Performance Benchmarks

| Operation | Target Performance | Memory Usage |
|-----------|-------------------|--------------|
| Stakeholder Detection | < 100ms for small text | < 10MB |
| Task Detection | < 50ms per task | < 5MB |
| Framework Analysis | < 200ms | < 15MB |
| Database Queries | < 10ms for simple queries | < 2MB |

## Integration Examples

### Basic Usage
```python
from claudedirector.core.config import get_config
from claudedirector.intelligence.stakeholder import StakeholderIntelligence
from claudedirector.intelligence.task import TaskIntelligence

# Initialize
config = get_config()
stakeholder_ai = StakeholderIntelligence(config=config)
task_ai = TaskIntelligence(config=config)

# Process meeting notes
meeting_text = """
Meeting with senior leadership about platform roadmap.
Action items: Review architecture proposal by Friday.
Follow up with executive team about budget approval.
"""

# Detect stakeholders
stakeholders = stakeholder_ai.get_all_stakeholders()

# Detect tasks
tasks = task_ai.get_all_tasks()

print(f"Found {len(stakeholders)} stakeholders and {len(tasks)} tasks")
```

### Advanced Framework Integration
```python
from claudedirector.core.embedded_framework_engine import EmbeddedFrameworkEngine

framework_engine = EmbeddedFrameworkEngine()

# Analyze strategic decision
decision_context = """
We need to decide whether to build our authentication system in-house
or adopt a third-party solution. Timeline is tight, but security is critical.
Team has mixed opinions on technical approach.
"""

result = framework_engine.analyze_strategic_context(decision_context)

# Get specific framework guidance
if "Decisive WRAP Decision Framework" in result['activated_frameworks']:
    wrap_guidance = result['framework_specific_guidance']['wrap']
    print("WRAP Framework recommends:")
    for step in wrap_guidance['process_steps']:
        print(f"- {step}")
```

## Type Definitions

### Core Types
```python
from typing import Dict, List, Optional, Any
from claudedirector.core.types import (
    ConfigDict,
    MetadataDict,
    FrameworkResult,
    WorkspaceConfig
)

# Stakeholder data structure
StakeholderData = Dict[str, Any]  # {name, role, confidence, context}

# Task data structure
TaskData = Dict[str, Any]  # {title, description, priority, deadline}

# Framework analysis result
FrameworkAnalysis = Dict[str, Any]  # {frameworks, recommendations, confidence}
```

## Testing

### Unit Testing
```python
import pytest
from unittest.mock import Mock
from claudedirector.intelligence.stakeholder import StakeholderIntelligence

def test_stakeholder_detection():
    config = Mock()
    config.stakeholder_auto_create_threshold = 0.85

    stakeholder_ai = StakeholderIntelligence(config=config)
    # Test stakeholder detection logic
```

### Performance Testing
```python
from claudedirector.tests.performance.test_ai_detection_benchmarks import PerformanceBenchmark

benchmark = PerformanceBenchmark()
# Run performance tests on AI detection modules
```

## Migration Guide

### From Legacy Versions
When upgrading from earlier versions:

1. **Update Configuration**: New threshold parameters available
2. **Database Schema**: Run migration scripts for new schema versions
3. **API Changes**: Some method names have been updated for clarity

### Breaking Changes in v0.6.0
- `detect_stakeholders()` → Use appropriate getter methods
- Configuration parameter names updated
- Enhanced type safety requirements

---

**Note**: This API documentation is automatically generated and updated. For the most current information, refer to the source code and unit tests.
