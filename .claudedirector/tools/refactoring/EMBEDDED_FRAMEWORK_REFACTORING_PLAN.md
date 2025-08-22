# Embedded Framework Engine Refactoring Plan

## Current State: MASSIVE MONOLITH
- **File**: `embedded_framework_engine.py`
- **Size**: 2,338 lines
- **Classes**: 2 main classes + 2 data classes
- **Problem**: Violates Single Responsibility Principle, untestable

## Refactoring Strategy: DECOMPOSITION BY RESPONSIBILITY

### 1. Data Models (NEW: `framework_models.py`)
```python
@dataclass
class FrameworkAnalysis:
    # Result of embedded framework analysis

@dataclass
class SystematicResponse:
    # Complete systematic analysis response
```

### 2. Framework Selection Logic (NEW: `framework_selector.py`)
```python
class FrameworkSelector:
    def select_framework(self, query: str, context: Dict) -> str
    def _calculate_framework_fitness(self, query: str, framework: str) -> float
    def _get_framework_patterns(self, framework: str) -> List[str]
```

### 3. Framework Application Engine (NEW: `framework_processor.py`)
```python
class FrameworkProcessor:
    def apply_framework(self, framework: str, query: str, context: Dict) -> FrameworkAnalysis
    def _generate_insights(self, framework: str, query: str) -> Dict[str, Any]
    def _generate_recommendations(self, framework: str, insights: Dict) -> List[str]
    def _create_implementation_steps(self, framework: str, recommendations: List) -> List[str]
    def _identify_considerations(self, framework: str, context: Dict) -> List[str]
```

### 4. Confidence & Quality Assessment (NEW: `analysis_validator.py`)
```python
class AnalysisValidator:
    def calculate_confidence(self, analysis: FrameworkAnalysis) -> float
    def validate_completeness(self, analysis: FrameworkAnalysis) -> bool
    def assess_quality_metrics(self, analysis: FrameworkAnalysis) -> Dict[str, float]
```

### 5. Persona Integration (NEW: `persona_integrator.py`)
```python
class PersonaIntegrator:
    def create_systematic_response(self, analysis: FrameworkAnalysis, persona: str) -> SystematicResponse
    def _integrate_with_persona(self, analysis: FrameworkAnalysis, persona: str) -> str
    def _integrate_diego_response(self, analysis: FrameworkAnalysis) -> str
    def _integrate_martin_response(self, analysis: FrameworkAnalysis) -> str
    def _integrate_rachel_response(self, analysis: FrameworkAnalysis) -> str
```

### 6. Main Orchestrator (REFACTORED: `embedded_framework_engine.py`)
```python
class EmbeddedFrameworkEngine:
    def __init__(self, config: Optional[Dict] = None)
    def analyze_systematically(self, query: str, context: Dict = None) -> SystematicResponse
    # Coordinates all the specialized components
```

## Refactoring Benefits

### Before (Current):
- ❌ 2,338 lines in one file
- ❌ Impossible to unit test effectively
- ❌ Multiple responsibilities mixed together
- ❌ High cognitive complexity
- ❌ Hard to maintain and extend

### After (Refactored):
- ✅ 6 focused files (~300-400 lines each)
- ✅ Each class has single responsibility
- ✅ Easy to unit test in isolation
- ✅ Clear separation of concerns
- ✅ Maintainable and extensible
- ✅ Follows SOLID principles

## Implementation Steps

1. **Create data models** (`framework_models.py`)
2. **Extract framework selector** (`framework_selector.py`)
3. **Extract framework processor** (`framework_processor.py`)
4. **Extract analysis validator** (`analysis_validator.py`)
5. **Extract persona integrator** (`persona_integrator.py`)
6. **Refactor main engine** (updated `embedded_framework_engine.py`)
7. **Update imports** across the codebase
8. **Add unit tests** for each focused component
9. **Integration testing** to ensure no regressions

## Testing Strategy (Post-Refactoring)

Each component can now be tested independently:
- `FrameworkSelector` → Test framework selection logic
- `FrameworkProcessor` → Test framework application
- `AnalysisValidator` → Test confidence calculations
- `PersonaIntegrator` → Test persona-specific formatting
- `EmbeddedFrameworkEngine` → Test orchestration with mocks

## Success Metrics

- ✅ All files under 500 lines
- ✅ Each class has single responsibility
- ✅ 95%+ unit test coverage achievable
- ✅ No functional regressions
- ✅ Improved maintainability score
