# Embedded Framework Engine SOLID Refactoring Plan

## Current State Analysis

**File**: `.claudedirector/lib/core/embedded_framework_engine.py`
- **Size**: 2,338 lines, 108KB
- **Classes**: 3 (FrameworkAnalysis, SystematicResponse, EmbeddedFrameworkEngine)
- **Methods**: 25+ methods in EmbeddedFrameworkEngine
- **SOLID Violations**: Multiple critical violations

## SOLID Principle Violations Identified

### 1. Single Responsibility Principle (SRP) - CRITICAL
**Current Issues**:
- Framework selection logic
- Framework application and analysis
- Pattern matching and insights generation
- Recommendations and implementation steps
- Confidence calculation
- Persona integration coordination

**Impact**: Massive cognitive load, difficult testing, high coupling

### 2. Open/Closed Principle (OCP) - HIGH
**Current Issues**:
- Adding new frameworks requires modifying core class
- Framework definitions hardcoded in constructor
- No extension points for new analysis types

**Impact**: Risky changes, difficult framework additions

### 3. Interface Segregation Principle (ISP) - MEDIUM
**Current Issues**:
- Clients forced to depend on entire massive interface
- No focused interfaces for specific use cases

**Impact**: Unnecessary dependencies, difficult mocking

### 4. Dependency Inversion Principle (DIP) - HIGH
**Current Issues**:
- High-level analysis depends on low-level framework details
- No abstractions for framework providers
- Tight coupling to specific implementations

**Impact**: Difficult testing, inflexible architecture

## Refactoring Strategy

### Phase 1: Extract Core Abstractions (SRP + DIP)
1. **Framework Provider Interface**
   - `IFrameworkProvider` - Abstract framework definition
   - `IFrameworkAnalyzer` - Analysis contract
   - `IFrameworkSelector` - Selection strategy

2. **Core Service Separation**
   - `FrameworkSelectionService` - Framework selection logic
   - `FrameworkAnalysisService` - Analysis execution
   - `InsightGenerationService` - Insights and recommendations
   - `ConfidenceCalculationService` - Confidence scoring

### Phase 2: Implement Strategy Pattern (OCP)
1. **Framework Strategies**
   - `StrategicPlatformAssessmentStrategy`
   - `TeamTopologiesStrategy`
   - `CapitalAllocationStrategy`
   - etc.

2. **Analysis Strategies**
   - `PatternMatchingAnalyzer`
   - `RecommendationGenerator`
   - `ImplementationPlanner`

### Phase 3: Create Focused Interfaces (ISP)
1. **Client-Specific Interfaces**
   - `IFrameworkSelector` - For framework selection
   - `IAnalysisProvider` - For analysis execution
   - `IInsightGenerator` - For insights generation
   - `IPersonaIntegrator` - For persona integration

### Phase 4: Dependency Injection (DIP)
1. **Service Container**
   - `FrameworkEngineContainer` - DI container
   - Constructor injection for all services
   - Interface-based dependencies

## Implementation Plan

### Step 1: Create Abstractions (Day 1)
```python
# New files to create:
- framework_provider_interface.py
- framework_analysis_service.py
- framework_selection_service.py
- insight_generation_service.py
```

### Step 2: Extract Services (Day 1-2)
```python
# Extract from embedded_framework_engine.py:
- FrameworkSelectionService (lines 1165-1409)
- FrameworkAnalysisService (lines 1410-1563)
- InsightGenerationService (lines 1564-1778)
- ConfidenceCalculationService (lines 1835-1860)
```

### Step 3: Implement Strategies (Day 2-3)
```python
# Create strategy implementations:
- strategic_platform_assessment_strategy.py
- team_topologies_strategy.py
- capital_allocation_strategy.py
```

### Step 4: Refactor Main Engine (Day 3)
```python
# Refactored EmbeddedFrameworkEngine:
- Constructor injection of services
- Orchestration only (no business logic)
- <200 lines total
```

### Step 5: Update Tests (Day 3-4)
```python
# Update existing tests:
- Mock individual services
- Test service interactions
- Maintain backward compatibility
```

## Success Metrics

### Code Quality Improvements
- **File Size**: 2,338 lines → ~200 lines main engine + 6-8 focused services
- **Cyclomatic Complexity**: Reduce from HIGH to LOW per service
- **Test Coverage**: Increase from current to 90%+ per service
- **SOLID Compliance**: 100% compliance across all services

### Maintainability Improvements
- **New Framework Addition**: 1 new file vs modifying core class
- **Testing**: Individual service testing vs monolithic testing
- **Code Review**: Focused changes vs massive file reviews
- **Debugging**: Service-specific debugging vs monolithic debugging

## Risk Mitigation

### Backward Compatibility
- Maintain existing public API
- Facade pattern for existing clients
- Gradual migration path

### Testing Strategy
- Service-by-service testing
- Integration tests for orchestration
- Regression tests for existing functionality

### Rollback Plan
- Feature flags for new architecture
- Parallel implementation during transition
- Quick rollback to monolithic version if needed

## Timeline

- **Day 1**: Abstractions and first service extraction
- **Day 2**: Complete service extraction and strategy implementation
- **Day 3**: Main engine refactoring and integration
- **Day 4**: Testing and validation
- **Day 5**: Documentation and cleanup

**Total Effort**: 5 days for complete SOLID compliance transformation
