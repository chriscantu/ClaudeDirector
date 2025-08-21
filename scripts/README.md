# Local CI Validation Scripts

## Overview
These scripts allow you to run the same checks locally that run in the GitHub Actions CI pipeline, eliminating the need for push-and-wait iteration cycles.

## validate-ci-locally.py

### Purpose
Runs **exactly the same checks** as the GitHub Actions pipeline:
- Security Scan (sensitive data detection)
- Black Formatting
- Flake8 Linting
- MyPy Type Checking
- SOLID Principles Validation
- Unit Tests with Coverage (85% minimum)

### Usage
```bash
# Check all CI requirements locally
python3 scripts/validate-ci-locally.py

# Auto-fix formatting issues
python3 scripts/validate-ci-locally.py --fix
```

### Prerequisites
The script will check for required tools and suggest setup:
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Benefits
- **Catch issues before pushing** - no more CI iteration cycles
- **Exact CI match** - same logic as GitHub Actions pipeline
- **Auto-fix mode** - automatically fixes formatting issues
- **Clear output** - colored status messages and summaries
- **Fast feedback** - runs locally in seconds vs minutes in CI

## Security Scanner Alignment

The security scanner now has **intelligent filtering** to prevent false positives:

### Skipped Directories
- `.git/`, `__pycache__/`, `venv/`, `node_modules/`
- `target/`, `build/`, `dist/`

### Skipped File Patterns
- Documentation: `docs/`, `readme`, `security.md`, `example`
- Workspace: `leadership-workspace/`

### Skipped Content Patterns
- Domains: `@company.com`, `@procore.com`, `platform-security.internal`
- Examples: `example`, `test`, `dummy`, `placeholder`, `sample`

This ensures the scanner focuses on **real security violations** while ignoring legitimate documentation and work-related content.
