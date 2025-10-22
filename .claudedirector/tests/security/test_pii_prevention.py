"""
Security Test: PII Prevention in Configuration Templates

CRITICAL: Ensures no Personally Identifiable Information (PII) or company-specific
data is committed to version control.

Test Coverage:
- Template files contain only placeholders (no real emails, tokens, URLs)
- Actual config files are properly gitignored
- No hardcoded company names or team names in templates
- No API tokens or credentials in codebase

TDD Phase: RED (write tests first, then ensure templates pass)
"""

import pytest
from pathlib import Path
import re


class TestPIIPreventionInTemplates:
    """Validate configuration templates are PII-free"""

    @pytest.fixture
    def project_root(self) -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent.parent.parent

    @pytest.fixture
    def template_config_path(self, project_root) -> Path:
        """Path to weekly report config template"""
        return (
            project_root
            / "leadership-workspace"
            / "configs"
            / "weekly-report-config.template.yaml"
        )

    @pytest.fixture
    def env_template_path(self, project_root) -> Path:
        """Path to environment variable template"""
        return project_root / "leadership-workspace" / "configs" / "env.template"

    @pytest.fixture
    def gitignore_path(self, project_root) -> Path:
        """Path to .gitignore"""
        return project_root / ".gitignore"

    def test_template_config_exists(self, template_config_path):
        """Ensure template configuration file exists"""
        assert (
            template_config_path.exists()
        ), f"Template config not found: {template_config_path}"

    def test_env_template_exists(self, env_template_path):
        """Ensure environment variable template exists"""
        assert (
            env_template_path.exists()
        ), f"Env template not found: {env_template_path}"

    def test_template_config_has_no_real_email(self, template_config_path):
        """
        Validate: No real email addresses in template

        SECURITY: Email addresses should use placeholders like:
        - [YOUR-EMAIL]@[YOUR-COMPANY].com
        - ${JIRA_EMAIL}

        NOT: actualuser@procore.com or any real domain
        """
        content = template_config_path.read_text()

        # Pattern: matches real email addresses (not placeholders)
        real_email_pattern = r"\b[A-Za-z0-9._%+-]+@(?!(\[YOUR-|example\.com))[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        matches = re.findall(real_email_pattern, content)
        assert len(matches) == 0, f"Found real email addresses in template: {matches}"

    def test_template_config_has_no_api_tokens(self, template_config_path):
        """
        Validate: No real Jira API tokens in template

        SECURITY: Jira tokens start with "ATATT" - these should NEVER appear in templates
        Only environment variable placeholders like ${JIRA_API_TOKEN} are allowed
        """
        content = template_config_path.read_text()

        # Jira Cloud API tokens start with ATATT
        assert (
            "ATATT" not in content
        ), "Found real Jira API token in template (starts with ATATT)"

        # Jira Data Center PAT tokens are typically 20+ alphanumeric
        # This is a heuristic - we check for suspicious long alphanumeric strings
        suspicious_tokens = re.findall(
            r'api_token:\s*["\']?([A-Za-z0-9]{20,})["\']?', content
        )
        # Filter out placeholders
        real_tokens = [
            t for t in suspicious_tokens if not t.startswith("[") and "${" not in t
        ]
        assert (
            len(real_tokens) == 0
        ), f"Found suspicious API tokens in template: {real_tokens}"

    def test_template_config_has_no_real_urls(self, template_config_path):
        """
        Validate: No real company Jira URLs in template

        SECURITY: URLs should use placeholders like:
        - https://[YOUR-COMPANY].atlassian.net
        - ${JIRA_BASE_URL}

        NOT: https://procore.atlassian.net or any real company domain
        """
        content = template_config_path.read_text()

        # Pattern: matches real Atlassian URLs (not placeholders)
        real_url_pattern = r"https://(?!\[YOUR-)[A-Za-z0-9-]+\.atlassian\.net"

        matches = re.findall(real_url_pattern, content)
        assert len(matches) == 0, f"Found real Atlassian URLs in template: {matches}"

    def test_template_config_has_no_hardcoded_project_names(self, template_config_path):
        """
        Validate: No real Jira project keys or team names

        SECURITY: Project keys should use placeholders like:
        - [PROJECT-1], [PROJECT-2], [PROJECT-3]
        - [Team 1 Name], [Team 2 Name]

        NOT: WEB, UIS, WEBDS, or any real project keys
        """
        content = template_config_path.read_text()

        # Known company-specific project patterns (you can add more)
        forbidden_patterns = [
            r"\bWEB-\d+",  # Example: WEB-1234
            r"\bUIS-\d+",  # Example: UIS-1234
            r"\bWEBDS-\d+",  # Example: WEBDS-1234
            r'project\s*=\s*["\'](?!\[)[A-Z]{2,}["\']',  # project = "ABC" (not placeholder)
        ]

        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content)
            assert (
                len(matches) == 0
            ), f"Found real project keys matching pattern '{pattern}': {matches}"

    def test_env_template_has_no_real_credentials(self, env_template_path):
        """
        Validate: Environment template has only placeholders

        SECURITY: All values should be [PLACEHOLDER] format or generic examples
        """
        content = env_template_path.read_text()

        # Check for real email addresses
        real_email_pattern = (
            r"JIRA_EMAIL=(?!\[YOUR-)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
        )
        matches = re.findall(real_email_pattern, content)
        assert len(matches) == 0, f"Found real email in env template: {matches}"

        # Check for real API tokens (ATATT prefix)
        assert "ATATT" not in content, "Found real Jira token in env template"

        # Check for real URLs
        real_url_pattern = (
            r"JIRA_BASE_URL=https://(?!\[YOUR-)[A-Za-z0-9-]+\.atlassian\.net"
        )
        matches = re.findall(real_url_pattern, content)
        assert len(matches) == 0, f"Found real Atlassian URL in env template: {matches}"

    def test_actual_config_is_gitignored(self, gitignore_path):
        """
        Validate: Actual config files are in .gitignore

        SECURITY: Ensures real configs can't accidentally be committed
        """
        gitignore_content = gitignore_path.read_text()

        # Check for weekly-report-config.yaml (actual config, not template)
        assert (
            "weekly-report-config.yaml" in gitignore_content
        ), "Actual config file 'weekly-report-config.yaml' not in .gitignore"

        # Check for .env files
        assert (
            ".env" in gitignore_content
            or "leadership-workspace/configs/.env" in gitignore_content
        ), ".env files not properly gitignored"

    def test_jira_reporter_has_no_hardcoded_team_names(self, project_root):
        """
        Validate: jira_reporter.py contains no company-specific team names

        SECURITY: After Phase 0 fix, this should be clean
        """
        jira_reporter_path = (
            project_root / ".claudedirector" / "lib" / "reporting" / "jira_reporter.py"
        )

        if not jira_reporter_path.exists():
            pytest.skip("jira_reporter.py not yet created")

        content = jira_reporter_path.read_text()

        # Known team names that should NOT appear
        forbidden_teams = [
            "Web Platform",
            "Web Design Systems",
            "Design Systems",
            "Experience Services",
            "Hubs",
            "Globalizers",
            "Onboarding",
            "UIF Special Projects",
        ]

        for team_name in forbidden_teams:
            # Allow in comments explaining the fix, but not in code
            # Check for string literals (quotes)
            pattern = f"[\"'].*{re.escape(team_name)}.*[\"']"
            matches = re.findall(pattern, content)

            # Filter out comments and security explanations
            code_matches = [
                m
                for m in matches
                if "SECURITY:" not in m and "no hardcoded" not in m.lower()
            ]

            assert (
                len(code_matches) == 0
            ), f"Found hardcoded team name '{team_name}' in jira_reporter.py: {code_matches}"

    def test_jira_reporter_has_no_hardcoded_initiative_names(self, project_root):
        """
        Validate: jira_reporter.py contains no company-specific initiative names

        SECURITY: After Phase 0 fix, this should be clean
        """
        jira_reporter_path = (
            project_root / ".claudedirector" / "lib" / "reporting" / "jira_reporter.py"
        )

        if not jira_reporter_path.exists():
            pytest.skip("jira_reporter.py not yet created")

        content = jira_reporter_path.read_text()

        # Known initiative names that should NOT appear (unless in comments explaining removal)
        forbidden_initiatives = [
            "Hammer",
            "FedRAMP",
            "Admin Pages",
            "***REMOVED*** Explore",
        ]

        for initiative_name in forbidden_initiatives:
            # Check for string literals (quotes)
            pattern = f"[\"'].*{re.escape(initiative_name)}.*[\"']"
            matches = re.findall(pattern, content)

            # Filter out comments and security explanations
            code_matches = [
                m
                for m in matches
                if "SECURITY:" not in m
                and "no hardcoded" not in m.lower()
                and "no company-specific" not in m.lower()
            ]

            assert (
                len(code_matches) == 0
            ), f"Found hardcoded initiative name '{initiative_name}' in jira_reporter.py: {code_matches}"


class TestGitHistoryPIIRemediation:
    """
    Validate git history PII remediation status

    NOTE: These tests validate that sensitive data has been removed from git history.
    If git history cleanup was performed using BFG Repo-Cleaner, this test should pass.
    """

    @pytest.fixture
    def project_root(self) -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent.parent.parent

    def test_git_repo_exists(self, project_root):
        """Ensure we're in a git repository"""
        git_dir = project_root / ".git"
        assert git_dir.exists(), "Not in a git repository"

    def test_no_committed_weekly_report_configs(self, project_root):
        """
        Validate: No actual weekly-report-config.yaml files in git history

        SECURITY: Only the .template.yaml should exist in git
        """
        import subprocess

        try:
            # Check if actual config file exists in git history
            result = subprocess.run(
                [
                    "git",
                    "log",
                    "--all",
                    "--",
                    "leadership-workspace/configs/weekly-report-config.yaml",
                ],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=10,
            )

            # If git log returns commits, the file was committed at some point
            if result.stdout.strip():
                pytest.fail(
                    "Found weekly-report-config.yaml in git history - "
                    "should be cleaned with BFG Repo-Cleaner"
                )
        except subprocess.TimeoutExpired:
            pytest.fail("Git command timed out")
        except FileNotFoundError:
            pytest.skip("Git not available in test environment")


class TestSecurityBestPractices:
    """
    Validate security best practices are documented
    """

    @pytest.fixture
    def project_root(self) -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent.parent.parent

    def test_security_documentation_exists(self, project_root):
        """Ensure SECURITY.md exists with guidance"""
        security_doc = project_root / "docs" / "SECURITY.md"
        assert security_doc.exists(), "SECURITY.md not found"

        content = security_doc.read_text()
        assert (
            "environment variable" in content.lower()
        ), "SECURITY.md should document environment variable usage"

    def test_ai_trust_framework_exists(self, project_root):
        """Ensure AI Trust Framework documents PII/credential boundaries"""
        ai_trust_doc = project_root / "docs" / "development" / "AI_TRUST_FRAMEWORK.md"
        assert ai_trust_doc.exists(), "AI_TRUST_FRAMEWORK.md not found"

        content = ai_trust_doc.read_text()
        assert any(
            keyword in content.lower() for keyword in ["credential", "pii", "security"]
        ), "AI_TRUST_FRAMEWORK.md should document security boundaries"
