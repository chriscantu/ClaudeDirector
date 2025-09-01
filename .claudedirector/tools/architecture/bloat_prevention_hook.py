#!/usr/bin/env python3
"""
Pre-commit Bloat Prevention Hook

🏗️ Martin | Platform Architecture - Real-time Duplication Prevention

Integration: Pre-commit hook that prevents code bloat before it enters the repository
Performance: <5s analysis time for changed files only
Enforcement: Blocks commits that introduce significant duplication or architectural violations
"""

import sys
import asyncio
import subprocess
from pathlib import Path
from typing import List, Set
import json

# Add the tools directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import our bloat analyzer
try:
    from bloat_prevention_system import create_bloat_analyzer, DuplicationSeverity

    ANALYZER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Bloat analyzer not available - running in basic mode: {e}")
    ANALYZER_AVAILABLE = False


class PreCommitBloatPrevention:
    """
    Pre-commit hook for preventing code bloat

    🏗️ Martin | Platform Architecture

    Hook Strategy:
    1. Analyze only changed/new files for performance
    2. Check against existing codebase for duplications
    3. Validate architectural compliance
    4. Block commits with HIGH or CRITICAL severity issues
    5. Provide actionable feedback for resolution
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.severity_threshold = (
            DuplicationSeverity.HIGH if ANALYZER_AVAILABLE else None
        )

    def get_staged_python_files(self) -> List[str]:
        """Get list of staged Python files"""

        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                print(f"❌ Failed to get staged files: {result.stderr}")
                return []

            # Filter for Python files
            python_files = [
                f
                for f in result.stdout.strip().split("\n")
                if f.endswith(".py") and f.strip()
            ]

            return python_files

        except Exception as e:
            print(f"❌ Error getting staged files: {e}")
            return []

    async def analyze_staged_files(self, staged_files: List[str]) -> dict:
        """Analyze staged files for bloat and duplication"""

        if not ANALYZER_AVAILABLE:
            return {"status": "skipped", "message": "Bloat analyzer not available"}

        if not staged_files:
            return {"status": "success", "message": "No Python files to analyze"}

        try:
            # Create analyzer
            analyzer = create_bloat_analyzer(str(self.project_root))

            # Analyze only staged files
            report = await analyzer.analyze_project_for_bloat(
                target_paths=staged_files,
                enable_mcp_analysis=False,  # Skip MCP for speed in pre-commit
            )

            return {
                "status": "completed",
                "report": report,
                "staged_files": staged_files,
            }

        except Exception as e:
            return {"status": "error", "message": f"Analysis failed: {e}"}

    def evaluate_blocking_issues(self, analysis_result: dict) -> tuple[bool, List[str]]:
        """Evaluate if analysis results should block the commit"""

        if analysis_result["status"] != "completed":
            return False, []  # Don't block on analysis errors

        report = analysis_result["report"]
        blocking_issues = []
        should_block = False

        # Check severity breakdown
        severity_breakdown = report.get("severity_breakdown", {})

        # Block on HIGH or CRITICAL severity issues
        high_severity_count = severity_breakdown.get("high", 0)
        critical_severity_count = severity_breakdown.get("critical", 0)

        if critical_severity_count > 0:
            should_block = True
            blocking_issues.append(
                f"🚨 CRITICAL: {critical_severity_count} critical duplication(s) detected"
            )

        if high_severity_count > 0:
            should_block = True
            blocking_issues.append(
                f"⚠️  HIGH: {high_severity_count} high-severity duplication(s) detected"
            )

        # Check for specific architectural violations
        violations_count = report.get("architectural_violations", 0)
        if violations_count > 3:  # Threshold for blocking
            should_block = True
            blocking_issues.append(
                f"🏗️ ARCHITECTURE: {violations_count} architectural violations detected"
            )

        return should_block, blocking_issues

    def generate_feedback_message(
        self, analysis_result: dict, blocking_issues: List[str]
    ) -> str:
        """Generate helpful feedback message for developers"""

        if analysis_result["status"] != "completed":
            return f"⚠️  Bloat analysis {analysis_result['status']}: {analysis_result.get('message', 'Unknown error')}"

        report = analysis_result["report"]
        staged_files = analysis_result["staged_files"]

        message_parts = [
            "🏗️ Code Bloat Prevention Analysis",
            "=" * 40,
            f"📁 Files analyzed: {len(staged_files)}",
            f"🔍 Duplications found: {report['duplications_found']['total']}",
            f"🏗️ Architectural violations: {report['architectural_violations']}",
            f"⏱️  Analysis time: {report['processing_time_seconds']:.2f}s",
        ]

        if blocking_issues:
            message_parts.extend(
                ["", "🚫 COMMIT BLOCKED - Issues must be resolved:", ""]
            )
            message_parts.extend(f"   {issue}" for issue in blocking_issues)

            # Add specific recommendations
            recommendations = report.get("consolidation_recommendations", [])
            if recommendations:
                message_parts.extend(["", "🔧 Recommended Actions:", ""])
                for i, rec in enumerate(recommendations[:3]):
                    message_parts.append(
                        f"   {i+1}. {rec['description']} (Effort: {rec.get('estimated_effort_hours', 'N/A')}h)"
                    )
        else:
            # Provide informational feedback
            moderate_count = report.get("severity_breakdown", {}).get("moderate", 0)
            if moderate_count > 0:
                message_parts.extend(
                    [
                        "",
                        f"ℹ️  Note: {moderate_count} moderate duplication(s) detected",
                        "   Consider consolidating when convenient",
                    ]
                )

        # Add prevention tips
        message_parts.extend(
            [
                "",
                "💡 Prevention Tips:",
                "   • Check existing implementations before creating new ones",
                "   • Use centralized constants instead of hard-coded strings",
                "   • Follow established architectural patterns",
                "   • Run 'python tools/architecture/bloat_prevention_system.py' for full analysis",
            ]
        )

        return "\n".join(message_parts)

    async def run_hook(self) -> int:
        """Run the pre-commit bloat prevention hook"""

        print("🏗️ Running Code Bloat Prevention Hook...")

        # Get staged files
        staged_files = self.get_staged_python_files()

        if not staged_files:
            print("✅ No Python files staged - skipping bloat analysis")
            return 0

        print(f"🔍 Analyzing {len(staged_files)} staged Python file(s)...")

        # Analyze staged files
        analysis_result = await self.analyze_staged_files(staged_files)

        # Evaluate if we should block the commit
        should_block, blocking_issues = self.evaluate_blocking_issues(analysis_result)

        # Generate feedback message
        feedback = self.generate_feedback_message(analysis_result, blocking_issues)
        print(feedback)

        if should_block:
            print(
                "\n🚫 COMMIT BLOCKED - Please resolve the issues above before committing"
            )
            return 1  # Non-zero exit code blocks the commit
        else:
            print("\n✅ Bloat prevention check passed - commit allowed")
            return 0


async def main():
    """Main entry point for pre-commit hook"""

    # Determine project root (look for .git directory)
    current_dir = Path.cwd()
    project_root = current_dir

    while project_root != project_root.parent:
        if (project_root / ".git").exists():
            break
        project_root = project_root.parent

    # Run the hook
    hook = PreCommitBloatPrevention(str(project_root))
    exit_code = await hook.run_hook()

    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
