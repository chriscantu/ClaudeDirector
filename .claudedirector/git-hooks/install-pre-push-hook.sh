#!/bin/bash
# Install Pre-push CI Validation Hook
# Copies the pre-push CI validation script to git hooks

echo "🔧 INSTALLING PRE-PUSH CI VALIDATION HOOK"
echo "============================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Copy the pre-push hook
cp .claudedirector/git-hooks/pre-push-ci-validation.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push

echo "✅ Pre-push CI validation hook installed successfully"
echo ""
echo "📋 WHAT THIS DOES:"
echo "  • Runs complete GitHub CI workflow locally before push"
echo "  • Prevents CI failures by catching issues early"
echo "  • Validates package structure, security, code quality"
echo "  • Runs all P0 feature tests"
echo "  • Checks P0 CI coverage compliance"
echo ""
echo "⚡ PERFORMANCE:"
echo "  • Typical runtime: 30-60 seconds"
echo "  • Prevents wasted GitHub Actions minutes"
echo "  • Catches issues before they reach CI"
echo ""
echo "🚀 USAGE:"
echo "  • Hook runs automatically on 'git push'"
echo "  • Push is blocked if any validation fails"
echo "  • Fix issues locally and push again"
echo ""
echo "🛠️ BYPASS (Emergency Only):"
echo "  • git push --no-verify (skips all hooks)"
echo "  • Only use for critical hotfixes"
echo ""
echo "✅ Installation complete - next push will validate CI locally!"
