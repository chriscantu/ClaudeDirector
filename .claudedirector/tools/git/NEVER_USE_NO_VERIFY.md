# 🚨 CRITICAL: NEVER USE --no-verify

## PERMANENT ENFORCEMENT POLICY

**`--no-verify` usage is PERMANENTLY BLOCKED in this repository.**

### ❌ BLOCKED COMMANDS
```bash
git commit --no-verify     # ❌ BLOCKED
git push --no-verify       # ❌ BLOCKED
```

### ✅ CORRECT USAGE
```bash
git commit -m "message"    # ✅ ALLOWED
git push origin branch     # ✅ ALLOWED
```

## WHY THIS IS ENFORCED

1. **Quality Assurance**: Pre-commit hooks catch issues before they reach the repository
2. **Security**: Prevents sensitive data from being committed
3. **Consistency**: Ensures all code meets our standards
4. **CI/CD Reliability**: Prevents broken code from reaching GitHub

## ENFORCEMENT MECHANISMS

### 1. Git Hooks (Unbypassable)
- `.git/hooks/pre-commit-no-verify-blocker`
- `.git/hooks/pre-push-no-verify-blocker`

### 2. Shell Function Override
- `.claudedirector/tools/git/no-verify-blocker.fish`
- Blocks the command before it even reaches git

### 3. Pre-commit Configuration
- Enhanced security scanner blocks violations
- Mandatory test validation enforces quality

## IF HOOKS ARE FAILING

**DO NOT BYPASS - FIX THE ISSUES:**

1. **Read the error message** - it tells you what's wrong
2. **Fix the underlying problem** - don't mask it
3. **Run tests locally** - ensure everything works
4. **Commit properly** - with full verification

## CONSEQUENCES OF BYPASSING

- **Security Risk**: Sensitive data could be exposed
- **Quality Degradation**: Broken code reaches production
- **CI Failures**: GitHub Actions will fail
- **Team Impact**: Other developers get broken code

## NO EXCEPTIONS

This policy has **NO EXCEPTIONS**:
- Not for "quick fixes"
- Not for "emergency commits"
- Not for "temporary workarounds"
- Not for "just this once"

**If you need to commit, fix the issues properly.**
