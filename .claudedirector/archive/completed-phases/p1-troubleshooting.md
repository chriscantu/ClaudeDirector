# P1 Organizational Intelligence Troubleshooting Guide

**Comprehensive troubleshooting and FAQ documentation for enterprise support**

## Quick Diagnostic Commands

### System Status Check
```bash
# Check overall P1 system health
./claudedirector org-intelligence status

# Validate configuration
./claudedirector org-intelligence validate

# Test core functionality
./claudedirector org-intelligence test-profile --sample-data
```

### Configuration Diagnostics
```bash
# Check configuration file exists
ls -la config/p1_organizational_intelligence.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/p1_organizational_intelligence.yaml'))"

# Check file permissions
stat config/p1_organizational_intelligence.yaml
```

## Common Issues and Solutions

### Configuration Problems

#### Issue: Configuration File Not Found
```
Error: Configuration file not found: config/p1_organizational_intelligence.yaml
```

**Diagnosis:**
```bash
# Check if config directory exists
ls -la config/

# Check current working directory
pwd

# Check if you're in the correct project root
ls -la | grep claudedirector
```

**Solutions:**
```bash
# Solution 1: Initialize default configuration
./claudedirector org-intelligence init

# Solution 2: Create config directory and setup
mkdir -p config
./claudedirector org-intelligence quick-setup --template platform_infrastructure

# Solution 3: Copy from backup
cp config/backup-*.yaml config/p1_organizational_intelligence.yaml
```

#### Issue: Invalid YAML Syntax
```
Error: could not find expected ':' in "config.yaml", line 42, column 1
```

**Diagnosis:**
```bash
# Validate YAML syntax
python -c "
import yaml
try:
    with open('config/p1_organizational_intelligence.yaml', 'r') as f:
        yaml.safe_load(f)
    print('✅ YAML syntax is valid')
except yaml.YAMLError as e:
    print(f'❌ YAML syntax error: {e}')
"
```

**Solutions:**
```bash
# Solution 1: Reset to default configuration
./claudedirector org-intelligence reset-config --confirm

# Solution 2: Fix common YAML issues
# Check for tabs instead of spaces
cat -A config/p1_organizational_intelligence.yaml | head -20

# Fix indentation
./claudedirector org-intelligence fix-yaml-indentation

# Solution 3: Validate and auto-fix
./claudedirector org-intelligence validate --fix
```

#### Issue: Invalid Profile Type
```
Error: Unknown preset profile type: invalid_profile
```

**Valid Profile Types:**
- `platform_director`
- `backend_director`
- `product_director`
- `design_director`
- `custom`

**Solution:**
```bash
# Check available templates
./claudedirector org-intelligence list-templates

# Reset to valid template
./claudedirector org-intelligence quick-setup --template platform_infrastructure
```

### Weight and Target Issues

#### Issue: Weights Don't Sum to 1.0
```
Error: Domain weights must sum to 1.0, currently sum to 0.85
```

**Diagnosis:**
```bash
# Check current weights
./claudedirector org-intelligence status | grep "weight:"

# Calculate total weights
./claudedirector org-intelligence calculate-weights
```

**Solutions:**
```bash
# Solution 1: Auto-normalize weights
./claudedirector org-intelligence normalize-weights

# Solution 2: Manually adjust weights
./claudedirector org-intelligence customize
# Then redistribute weights to sum to 1.0

# Solution 3: Reset to template defaults
./claudedirector org-intelligence quick-setup --template your_template --reset-weights
```

#### Issue: Invalid Target Values
```
Error: Target values must be positive and realistic (0.0 < target <= 1.0 for percentages)
```

**Common Invalid Targets:**
- Negative values: `-0.1`
- Zero values: `0.0`
- Impossible percentages: `1.5` (150%)
- Wrong units: `200` (for response time in wrong units)

**Solutions:**
```bash
# Check target value ranges
./claudedirector org-intelligence validate-targets

# Reset targets to recommended defaults
./claudedirector org-intelligence configure-domain --domain design_system_leverage --reset-targets

# Set realistic targets
./claudedirector org-intelligence configure-domain --domain platform_adoption
# Enter values between 0.0 and 1.0 for percentages
# Enter appropriate values for time/performance metrics
```

### Performance Issues

#### Issue: Slow Initialization (>2 seconds)
```
Warning: Profile initialization took 3.2s (expected <2.0s)
```

**Diagnosis:**
```bash
# Profile the initialization
./claudedirector org-intelligence profile-init --verbose

# Check configuration file size
ls -lh config/p1_organizational_intelligence.yaml

# Check system resources
top -l 1 | grep "CPU usage"
df -h .
```

**Solutions:**
```bash
# Solution 1: Optimize configuration
./claudedirector org-intelligence optimize-config

# Solution 2: Remove unused domains
./claudedirector org-intelligence cleanup-domains

# Solution 3: Reduce metric complexity
./claudedirector org-intelligence simplify-metrics

# Solution 4: Check for filesystem issues
./claudedirector org-intelligence check-io-performance
```

#### Issue: Slow Impact Calculation (>500ms)
```
Warning: Impact calculation took 750ms (expected <500ms)
```

**Diagnosis:**
```bash
# Profile the calculation
./claudedirector metrics calculate-impact --profile --sample-data

# Check number of active metrics
./claudedirector org-intelligence count-metrics

# Check calculation complexity
./claudedirector org-intelligence analyze-complexity
```

**Solutions:**
```bash
# Solution 1: Optimize metric weights
./claudedirector org-intelligence optimize-weights

# Solution 2: Cache frequent calculations
./claudedirector org-intelligence enable-caching

# Solution 3: Reduce metric granularity
./claudedirector org-intelligence simplify-calculations

# Solution 4: Use performance mode
./claudedirector org-intelligence set-performance-mode
```

### CLI Command Issues

#### Issue: Command Not Found
```
bash: claudedirector: command not found
```

**Diagnosis:**
```bash
# Check if file exists
ls -la ./claudedirector

# Check file permissions
stat ./claudedirector

# Check if you're in the right directory
pwd
ls -la | grep claudedirector
```

**Solutions:**
```bash
# Solution 1: Use relative path
./claudedirector org-intelligence status

# Solution 2: Add to PATH
export PATH="$PWD:$PATH"
claudedirector org-intelligence status

# Solution 3: Make executable
chmod +x claudedirector

# Solution 4: Run with Python directly
python claudedirector org-intelligence status
```

#### Issue: Module Import Errors
```
ModuleNotFoundError: No module named 'lib.claudedirector.p1_features'
```

**Diagnosis:**
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check if modules exist
ls -la lib/claudedirector/p1_features/

# Check Python version
python --version
```

**Solutions:**
```bash
# Solution 1: Set PYTHONPATH
export PYTHONPATH="$PWD:$PYTHONPATH"
./claudedirector org-intelligence status

# Solution 2: Install in development mode
pip install -e .

# Solution 3: Run from project root
cd /path/to/claudedirector
./claudedirector org-intelligence status

# Solution 4: Check virtual environment
source venv/bin/activate  # or venv/bin/activate.fish
./claudedirector org-intelligence status
```

### Integration Issues

#### Issue: GitHub API Connection Failed
```
Error: Failed to connect to GitHub API: 401 Unauthorized
```

**Diagnosis:**
```bash
# Check API key
echo $GITHUB_API_KEY | cut -c1-10  # Show first 10 chars only

# Test API access
curl -H "Authorization: token $GITHUB_API_KEY" https://api.github.com/user

# Check rate limits
./claudedirector metrics test-github-connection --check-limits
```

**Solutions:**
```bash
# Solution 1: Regenerate GitHub token
# Go to GitHub Settings > Developer settings > Personal access tokens
# Create new token with repo, read:org, read:user permissions

# Solution 2: Set environment variable
export GITHUB_API_KEY="your-new-token-here"

# Solution 3: Configure in config file
./claudedirector config set github.api_key "your-token-here"

# Solution 4: Test connection
./claudedirector metrics test-github-connection
```

#### Issue: Jira Connection Failed
```
Error: Failed to connect to Jira: SSL certificate verification failed
```

**Diagnosis:**
```bash
# Check Jira URL
echo $JIRA_BASE_URL

# Test HTTPS connection
curl -I $JIRA_BASE_URL

# Check certificate
openssl s_client -connect yourcompany.atlassian.net:443 -servername yourcompany.atlassian.net
```

**Solutions:**
```bash
# Solution 1: Update certificates
# macOS: brew install ca-certificates
# Linux: sudo apt-get update && sudo apt-get install ca-certificates

# Solution 2: Configure Jira connection
export JIRA_BASE_URL="https://yourcompany.atlassian.net"
export JIRA_API_KEY="your-api-key"

# Solution 3: Test connection
./claudedirector metrics test-jira-connection --verbose

# Solution 4: Skip SSL verification (development only)
./claudedirector config set jira.verify_ssl false
```

### Data and Calculation Issues

#### Issue: No Metrics Data Available
```
Warning: No metrics data available for impact calculation
```

**Diagnosis:**
```bash
# Check metric sources
./claudedirector metrics list-sources

# Check data availability
./claudedirector metrics check-data-availability

# Check integration status
./claudedirector integrations status
```

**Solutions:**
```bash
# Solution 1: Generate sample data for testing
./claudedirector org-intelligence generate-sample-data

# Solution 2: Configure metric sources
./claudedirector integrations setup-github
./claudedirector integrations setup-jira

# Solution 3: Import historical data
./claudedirector metrics import-historical --days 30

# Solution 4: Use manual metric input
./claudedirector metrics set-manual-values
```

#### Issue: Impact Score Always Zero
```
Issue: Organizational impact score consistently calculates to 0.0
```

**Diagnosis:**
```bash
# Check metric values
./claudedirector metrics debug-calculation --verbose

# Check target values
./claudedirector org-intelligence status | grep "target:"

# Check weights
./claudedirector org-intelligence status | grep "weight:"
```

**Solutions:**
```bash
# Solution 1: Verify target values are realistic
./claudedirector org-intelligence configure-domain --domain design_system_leverage
# Set targets that current metrics can achieve

# Solution 2: Check metric units and scaling
./claudedirector metrics validate-units

# Solution 3: Debug calculation step by step
./claudedirector metrics calculate-impact --debug --sample-data

# Solution 4: Reset calculation method
./claudedirector org-intelligence reset-calculation-method
```

## Diagnostic Tools

### Health Check Script
```bash
#!/bin/bash
# p1-health-check.sh

echo "🏥 P1 Organizational Intelligence Health Check"
echo "=============================================="

# Check Python environment
echo "🐍 Python Environment:"
python --version
which python

# Check dependencies
echo "📦 Dependencies:"
python -c "
try:
    import yaml
    print('✅ PyYAML available')
except ImportError:
    print('❌ PyYAML missing')

try:
    import click
    print('✅ Click available')
except ImportError:
    print('❌ Click missing')
"

# Check file structure
echo "📁 File Structure:"
if [ -f "claudedirector" ]; then
    echo "✅ Main CLI executable found"
else
    echo "❌ Main CLI executable missing"
fi

if [ -d "lib/claudedirector/p1_features" ]; then
    echo "✅ P1 features module found"
else
    echo "❌ P1 features module missing"
fi

if [ -f "config/p1_organizational_intelligence.yaml" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
fi

# Check configuration validity
echo "⚙️  Configuration:"
if [ -f "config/p1_organizational_intelligence.yaml" ]; then
    python -c "
import yaml
try:
    with open('config/p1_organizational_intelligence.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print('✅ Configuration YAML is valid')

    if 'director_profile' in config:
        print('✅ Director profile section found')
    else:
        print('❌ Director profile section missing')

    if 'organizational_intelligence' in config:
        print('✅ Organizational intelligence section found')
    else:
        print('❌ Organizational intelligence section missing')

except Exception as e:
    print(f'❌ Configuration error: {e}')
"
fi

# Check CLI functionality
echo "🔧 CLI Functionality:"
if ./claudedirector --help > /dev/null 2>&1; then
    echo "✅ Main CLI responds"
else
    echo "❌ Main CLI not responding"
fi

if ./claudedirector org-intelligence --help > /dev/null 2>&1; then
    echo "✅ P1 CLI commands available"
else
    echo "❌ P1 CLI commands not available"
fi

echo "✅ Health check complete!"
```

### Performance Diagnostic
```python
#!/usr/bin/env python3
# p1-performance-diagnostic.py

import time
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def diagnose_performance():
    print("⚡ P1 Performance Diagnostic")
    print("===========================")

    try:
        # Test imports
        start_time = time.time()
        from lib.claudedirector.p1_features.organizational_intelligence import DirectorProfileManager
        import_time = time.time() - start_time

        print(f"📦 Import time: {import_time:.3f}s", end="")
        if import_time < 0.5:
            print(" ✅")
        elif import_time < 1.0:
            print(" ⚠️  (slow)")
        else:
            print(" ❌ (too slow)")

        # Test initialization
        start_time = time.time()
        try:
            manager = DirectorProfileManager()
            init_time = time.time() - start_time

            print(f"🚀 Initialization: {init_time:.3f}s", end="")
            if init_time < 2.0:
                print(" ✅")
            else:
                print(" ❌ (exceeds 2.0s SLA)")

        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return

        # Test calculation performance
        test_metrics = {
            "component_usage": 0.8,
            "design_consistency": 0.9,
            "platform_adoption": 0.75,
            "developer_satisfaction": 4.2
        }

        start_time = time.time()
        score = manager.calculate_organizational_impact_score(test_metrics)
        calc_time = time.time() - start_time

        print(f"🧮 Calculation: {calc_time:.3f}s", end="")
        if calc_time < 0.5:
            print(" ✅")
        else:
            print(" ❌ (exceeds 0.5s SLA)")

        print(f"📊 Impact score: {score:.3f}")

        # Test executive summary
        start_time = time.time()
        summary = manager.generate_executive_summary()
        summary_time = time.time() - start_time

        print(f"📋 Summary generation: {summary_time:.3f}s", end="")
        if summary_time < 1.0:
            print(" ✅")
        else:
            print(" ⚠️  (slow)")

        print("✅ Performance diagnostic complete!")

    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        print("💡 Try: export PYTHONPATH=$PWD:$PYTHONPATH")
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")

if __name__ == "__main__":
    diagnose_performance()
```

## FAQ

### Q: How do I backup my configuration?
```bash
# Create timestamped backup
cp config/p1_organizational_intelligence.yaml config/backup-$(date +%Y%m%d-%H%M%S).yaml

# List all backups
ls -la config/backup-*.yaml
```

### Q: How do I migrate from one director profile to another?
```bash
# 1. Backup current profile
./claudedirector org-intelligence backup-profile

# 2. Setup new profile
./claudedirector org-intelligence quick-setup --template new_template

# 3. Import selected domains from backup
./claudedirector org-intelligence import-domains --from-backup --selective
```

### Q: How do I add a custom metric?
```yaml
# Add to config/p1_organizational_intelligence.yaml
organizational_intelligence:
  velocity_tracking:
    measurement_domains:
      custom_domain:
        enabled: true
        weight: 0.2
        metrics: ["custom_metric"]
        targets:
          custom_metric: 0.85
```

### Q: How do I troubleshoot slow performance?
```bash
# 1. Run performance diagnostic
python docs/scripts/p1-performance-diagnostic.py

# 2. Enable performance monitoring
./claudedirector org-intelligence set-performance-mode

# 3. Check system resources
./claudedirector org-intelligence system-check

# 4. Optimize configuration
./claudedirector org-intelligence optimize-config
```

### Q: How do I reset everything to defaults?
```bash
# ⚠️  WARNING: This will delete all customizations
./claudedirector org-intelligence reset-all --confirm

# Alternative: Reset just the configuration
./claudedirector org-intelligence reset-config --keep-backups
```

## Getting Support

### Self-Service Resources
1. **Documentation**: `/docs/p1-*.md`
2. **CLI Help**: `./claudedirector org-intelligence --help`
3. **Health Check**: Run the diagnostic scripts above
4. **Sample Data**: `./claudedirector org-intelligence generate-sample-data`

### Log Collection
```bash
# Collect diagnostic information
./claudedirector org-intelligence collect-diagnostics --output diagnostics.zip

# The zip file will contain:
# - Configuration files
# - Error logs
# - System information
# - Performance metrics
```

### Error Reporting
When reporting issues, include:
- **Error message**: Full error text
- **Command executed**: Exact command that failed
- **Configuration**: Your `p1_organizational_intelligence.yaml` (sanitized)
- **Environment**: OS, Python version, installation method
- **Diagnostic output**: Results from health check script

Your P1 Organizational Intelligence system is designed for reliability and ease of troubleshooting! 🔧
