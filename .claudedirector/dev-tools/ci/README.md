# Local CI Validation Scripts

## Overview
These scripts allow you to run the same checks locally that run in the GitHub Actions CI pipeline, eliminating the need for push-and-wait iteration cycles.

## validate-ci-locally.py

### Purpose
Runs **exactly the same checks** as the GitHub Actions pipeline:
- Security Scan (sensitive data detection)

Additional checks will be added in future iterations:
- Black Formatting (coming in Part 3)
- Flake8 Linting (coming in Part 3)
- MyPy Type Checking (coming in Part 4)
- SOLID Principles Validation (coming in Part 4)

### Usage
```bash
# Check all CI requirements locally
python3 .claudedirector/dev-tools/ci/validate-ci-locally.py

# Future: Auto-fix formatting issues (Part 3)
# python3 .claudedirector/dev-tools/ci/validate-ci-locally.py --fix
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
- **Clear output** - colored status messages and summaries
- **Fast feedback** - runs locally in seconds vs minutes in CI

## Security Scanner Implementation

The security scanner has **intelligent filtering** to prevent false positives:

### Skipped Directories
- `.git/`, `__pycache__/`, `.mypy_cache/`, `venv/`, `.venv/`
- `node_modules/`, `target/`, `build/`, `dist/`

### Skipped File Patterns
- Documentation: `docs/`, `readme`, `security.md`, `example`
- Workspace: `leadership-workspace/`

### Skipped Content Patterns
- Domains: `@company.com`, `@procore.com`, `platform-security.internal`
- Examples: `example`, `test`, `dummy`, `placeholder`, `sample`

This ensures the scanner focuses on **real security violations** while ignoring legitimate documentation and work-related content.

## Iterative Implementation Strategy

This is **Part 2/5** of our iterative CI pipeline implementation:

1. ✅ **Security Scanner** (Part 1 - completed)
2. ✅ **Local CI Validation** (Part 2 - this script)
3. 🔄 **Code Quality Gates** (Part 3 - Black/Flake8)
4. 🔄 **Advanced Quality** (Part 4 - MyPy/SOLID)
5. 🔄 **Test Infrastructure** (Part 5 - coverage when working)

Each part is atomic, focused, and independently testable.
