# P1 Organizational Intelligence Testing Guide

**Comprehensive testing and validation procedures for enterprise deployment**

## Testing Overview

The P1 Organizational Intelligence feature includes enterprise-grade testing infrastructure with 85%+ coverage, automated quality gates, and comprehensive validation procedures.

## Test Infrastructure

### Test Categories
- **Unit Tests**: Fast, isolated component testing (22 test methods)
- **Functional Tests**: End-to-end workflow validation (15+ scenarios)
- **Integration Tests**: CLI and system integration testing
- **Performance Tests**: Load testing and scalability validation
- **Security Tests**: Vulnerability scanning and compliance verification

### Coverage Requirements
- **Minimum Coverage**: 85% for all P1 features
- **Performance SLAs**: <2s initialization, <0.5s calculations
- **Quality Gates**: Pre-commit hooks enforce testing standards
- **Multi-Environment**: Python 3.8-3.11 compatibility

## Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Verify test environment
python -c "import pytest; print('✅ Test environment ready')"
```

### Unit Tests
```bash
# Run all P1 unit tests
pytest tests/p1_features/unit/ -v

# Run specific test class
pytest tests/p1_features/unit/test_director_profile_manager.py::TestDirectorProfileManager -v

# Run with coverage reporting
pytest tests/p1_features/unit/ --cov=lib/claudedirector/p1_features --cov-report=html
```

### Functional Tests
```bash
# Run end-to-end workflow tests
pytest tests/p1_features/functional/ -v

# Run CLI integration tests
pytest tests/p1_features/ -m cli -v

# Run performance tests
pytest tests/p1_features/ -m performance -v
```

### Complete Test Suite
```bash
# Run all P1 tests with coverage
pytest tests/p1_features/ \
  --cov=lib/claudedirector/p1_features \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=85 \
  -v
```

## Test Scenarios

### Director Profile Management

#### Unit Test Coverage
```python
# Test basic profile creation
def test_director_profile_creation():
    profile = DirectorProfile(
        role_title="Test Director",
        primary_focus="Testing",
        strategic_priorities=["Priority 1"],
        success_metrics=["Metric 1"],
        enabled_domains={"test_domain": [test_metric]},
        investment_categories={"test_investment": test_investment},
        dashboard_config={"layout": "test"},
        integration_preferences={"tool": True}
    )
    assert profile.role_title == "Test Director"
```

#### Functional Test Scenarios
- **Profile Creation**: Platform, Backend, Product, Custom director setup
- **Configuration Updates**: Weight adjustments, domain changes, target modifications
- **Template Application**: Quick setup with predefined templates
- **Migration Testing**: Profile transitions and role changes

### CLI Integration Testing

#### Command Validation
```bash
# Test CLI command availability
./claudedirector org-intelligence --help

# Test setup commands
./claudedirector org-intelligence setup --help
./claudedirector org-intelligence customize --help
./claudedirector org-intelligence status --help

# Test quick setup templates
./claudedirector org-intelligence quick-setup --help
```

#### Template Testing
```bash
# Test each template type
./claudedirector org-intelligence quick-setup --template design_system
./claudedirector org-intelligence quick-setup --template backend_services
./claudedirector org-intelligence quick-setup --template product_delivery
./claudedirector org-intelligence quick-setup --template platform_infrastructure
```

### Configuration Validation

#### YAML Schema Testing
```python
def test_configuration_schema():
    config = load_test_config()

    # Required sections
    assert "director_profile" in config
    assert "organizational_intelligence" in config

    # Profile structure
    profile = config["director_profile"]
    assert profile["profile_type"] in ["custom", "platform_director", "backend_director"]

    # Measurement domains
    domains = config["organizational_intelligence"]["velocity_tracking"]["measurement_domains"]
    assert len(domains) > 0
```

#### Domain Configuration Testing
```python
def test_domain_configuration():
    manager = DirectorProfileManager("test_config.yaml")

    # Test domain enablement
    manager.customize_profile(enable_domains=["api_service_efficiency"])
    assert "api_service_efficiency" in manager.current_profile.enabled_domains

    # Test weight updates
    manager.customize_profile(update_weights={"design_system_leverage": 0.5})
    design_metrics = manager.current_profile.enabled_domains["design_system_leverage"]
    assert design_metrics[0].weight == 0.5
```

### Performance Testing

#### Initialization Performance
```python
def test_initialization_performance():
    start_time = time.time()
    manager = DirectorProfileManager("large_config.yaml")
    init_time = time.time() - start_time

    # Must initialize within 2 seconds
    assert init_time < 2.0
```

#### Calculation Performance
```python
def test_calculation_performance():
    manager = DirectorProfileManager("test_config.yaml")

    large_metrics = {f"metric_{i}": 0.75 for i in range(100)}

    start_time = time.time()
    score = manager.calculate_organizational_impact_score(large_metrics)
    calc_time = time.time() - start_time

    # Must calculate within 500ms
    assert calc_time < 0.5
    assert 0.0 <= score <= 1.0
```

#### Scalability Testing
```python
def test_large_configuration_handling():
    # Create configuration with 10 domains, 10 metrics each
    large_config = create_large_test_config(domains=10, metrics_per_domain=10)

    manager = DirectorProfileManager()
    manager.config = large_config

    # Test with many concurrent calculations
    import threading
    results = []

    def calculate_score():
        score = manager.calculate_organizational_impact_score(test_metrics)
        results.append(score)

    threads = [threading.Thread(target=calculate_score) for _ in range(10)]

    start_time = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    total_time = time.time() - start_time

    # All calculations should complete within 1 second
    assert total_time < 1.0
    assert len(results) == 10
```

### Security Testing

#### Configuration Validation
```python
def test_configuration_security():
    # Test malformed YAML handling
    with pytest.raises(yaml.YAMLError):
        DirectorProfileManager("malformed_config.yaml")

    # Test missing file handling
    with pytest.raises(Exception, match="Configuration file not found"):
        DirectorProfileManager("nonexistent_file.yaml")

    # Test permission handling
    restricted_config = create_restricted_config_file()
    with pytest.raises(PermissionError):
        DirectorProfileManager(restricted_config)
```

#### Input Sanitization
```python
def test_input_sanitization():
    manager = DirectorProfileManager("test_config.yaml")

    # Test SQL injection attempts
    malicious_input = "'; DROP TABLE profiles; --"
    manager.customize_profile(role_title=malicious_input)

    # Should handle gracefully without security issues
    assert manager.current_profile.role_title == malicious_input  # Stored as string, not executed
```

## Automated Quality Gates

### Pre-commit Testing
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: p1-unit-tests
      name: P1 Unit Tests
      entry: python tools/testing/run_p1_unit_tests.py
      language: python
      files: ^(lib/claudedirector/p1_features/.*\.py|tests/p1_features/unit/.*\.py)$

    - id: p1-test-coverage
      name: P1 Test Coverage Check
      entry: python tools/testing/check_p1_coverage.py
      language: python
      files: ^lib/claudedirector/p1_features/.*\.py$
```

### CI/CD Pipeline Testing
```yaml
# .github/workflows/test-p1-features.yml
jobs:
  test-p1-features:
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
      - name: Run P1 unit tests
        run: |
          pytest tests/p1_features/unit/ -v --tb=short --durations=10 \
            --cov=lib/claudedirector/p1_features \
            --cov-report=xml \
            --cov-fail-under=85

      - name: Performance benchmarks
        run: |
          python -c "
          # Test initialization performance
          start_time = time.time()
          manager = DirectorProfileManager()
          init_time = time.time() - start_time
          assert init_time < 2.0
          "
```

## Manual Testing Procedures

### Setup Validation
```bash
# 1. Fresh installation test
git clone <repo>
cd claudedirector
./claudedirector org-intelligence quick-setup --template design_system

# 2. Configuration validation
./claudedirector org-intelligence validate

# 3. Status verification
./claudedirector org-intelligence status

# Expected: No errors, clean status output
```

### Feature Testing Checklist

#### ✅ Director Profile Setup
- [ ] Platform director template works
- [ ] Backend director template works
- [ ] Product director template works
- [ ] Custom profile creation works
- [ ] Profile status displays correctly

#### ✅ Configuration Management
- [ ] Domain enablement/disablement works
- [ ] Weight adjustments persist correctly
- [ ] Target value updates save properly
- [ ] Configuration file validation passes

#### ✅ CLI Interface
- [ ] All commands respond correctly
- [ ] Help text is comprehensive
- [ ] Error messages are clear
- [ ] Interactive prompts work

#### ✅ Calculation Engine
- [ ] Impact scoring calculates correctly
- [ ] Executive summaries generate
- [ ] Business value calculations work
- [ ] Performance meets SLAs

### Load Testing

#### Concurrent User Simulation
```python
import concurrent.futures
import time

def simulate_director_workflow():
    """Simulate a typical director workflow"""
    manager = DirectorProfileManager()

    # Profile customization
    manager.customize_profile(
        enable_domains=["design_system_leverage"],
        update_weights={"design_system_leverage": 0.4}
    )

    # Impact calculation
    metrics = {"component_usage": 0.8, "design_consistency": 0.9}
    score = manager.calculate_organizational_impact_score(metrics)

    # Executive summary
    summary = manager.generate_executive_summary()

    return score, summary

# Test 50 concurrent director workflows
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    start_time = time.time()
    futures = [executor.submit(simulate_director_workflow) for _ in range(50)]
    results = [future.result() for future in concurrent.futures.as_completed(futures)]
    total_time = time.time() - start_time

print(f"50 concurrent workflows completed in {total_time:.2f}s")
assert total_time < 10.0  # Should complete within 10 seconds
```

## Error Handling Testing

### Configuration Error Scenarios
```python
def test_configuration_error_handling():
    # Missing required sections
    minimal_config = {"director_profile": {}}
    with pytest.raises(KeyError):
        DirectorProfileManager.from_dict(minimal_config)

    # Invalid profile type
    invalid_config = {
        "director_profile": {"profile_type": "invalid_type"}
    }
    with pytest.raises(ValueError):
        DirectorProfileManager.from_dict(invalid_config)

    # Invalid weight values
    invalid_weights = {"domain1": -0.5, "domain2": 1.5}
    manager = DirectorProfileManager("test_config.yaml")
    with pytest.raises(ValueError):
        manager.customize_profile(update_weights=invalid_weights)
```

### CLI Error Handling
```bash
# Test invalid commands
./claudedirector org-intelligence invalid-command
# Expected: Clear error message with available commands

# Test invalid options
./claudedirector org-intelligence setup --invalid-option
# Expected: Option validation error with usage help

# Test missing configuration
rm config/p1_organizational_intelligence.yaml
./claudedirector org-intelligence status
# Expected: Configuration not found error with setup instructions
```

## Test Data Management

### Sample Configurations
```yaml
# tests/fixtures/platform_director_config.yaml
director_profile:
  profile_type: "custom"
  custom_profile:
    role_title: "Test Platform Director"
    primary_focus: "Test platform development"

organizational_intelligence:
  velocity_tracking:
    measurement_domains:
      design_system_leverage:
        enabled: true
        weight: 0.5
        metrics: ["test_metric"]
        targets:
          test_metric: 0.8
```

### Test Utilities
```python
# tests/p1_features/conftest.py
@pytest.fixture
def sample_director_config():
    """Standard director configuration for testing"""
    return load_test_config("platform_director_config.yaml")

@pytest.fixture
def temp_config_file(sample_config):
    """Create temporary config file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_config, f)
        yield f.name
    Path(f.name).unlink()
```

## Deployment Validation

### Pre-Production Checklist
- [ ] All unit tests pass (85%+ coverage)
- [ ] Functional tests validate workflows
- [ ] Performance benchmarks meet SLAs
- [ ] Security scans show no vulnerabilities
- [ ] Documentation is complete and accurate
- [ ] CLI commands work correctly
- [ ] Configuration validation passes
- [ ] Error handling is robust

### Production Readiness
- [ ] Multi-environment testing completed
- [ ] Load testing validates scalability
- [ ] Monitoring and alerting configured
- [ ] Backup and recovery procedures tested
- [ ] Support documentation available
- [ ] Training materials prepared
- [ ] Rollback procedures defined

## Continuous Testing

### Automated Test Execution
```bash
# Run on every commit
git hook: pytest tests/p1_features/unit/ --cov-fail-under=85

# Run on pull requests
CI/CD: pytest tests/p1_features/ --cov-report=xml

# Run nightly
Scheduled: pytest tests/p1_features/ --cov --performance --security
```

### Regression Testing
```bash
# Test against previous versions
pytest tests/p1_features/regression/ -v

# Test configuration migration
pytest tests/p1_features/migration/ -v

# Test backward compatibility
pytest tests/p1_features/compatibility/ -v
```

Your P1 Organizational Intelligence testing infrastructure ensures enterprise-grade quality and reliability! 🚀
