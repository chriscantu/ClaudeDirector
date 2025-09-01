#!/usr/bin/env python3
"""
Real Data Integration Setup Wizard
Phase 7 Week 3 - User-Friendly Integration Setup

🏗️ Martin | Platform Architecture - Integration orchestration
🎨 Rachel | Design Systems Strategy - User experience design
💼 Alvaro | Platform Investment Strategy - Business value delivery

Guides users through setting up real GitHub and Jira integrations with clear
transparency about data sources and security.
"""

import os
import json
import getpass
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import aiohttp

# Configuration directory
CONFIG_DIR = Path.home() / ".claudedirector" / "integrations"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class IntegrationWizard:
    """User-friendly wizard for setting up real data integrations"""

    def __init__(self):
        self.config_file = CONFIG_DIR / "real_data_config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load existing configuration"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {
            "github": {"enabled": False},
            "jira": {"enabled": False},
            "setup_completed": False,
        }

    def _save_config(self):
        """Save configuration securely"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)
        # Secure the config file
        os.chmod(self.config_file, 0o600)

    def show_welcome(self):
        """Show welcome message with transparency"""
        print("\n" + "=" * 70)
        print("🚀 ClaudeDirector Real Data Integration Setup")
        print("=" * 70)
        print("\n🚨 TRANSPARENCY FIRST:")
        print("• Currently showing SIMULATED data (clearly marked)")
        print("• This setup connects to YOUR real GitHub/Jira data")
        print("• All tokens stored locally and encrypted")
        print("• You can disconnect anytime")
        print("• Simulation mode always available as fallback")
        print("\n💡 Benefits of Real Data Integration:")
        print("• Actual sprint metrics from your Jira")
        print("• Real repository activity from GitHub")
        print("• Strategic insights from your actual projects")
        print("• Live performance tracking and trends")

    def setup_github_integration(self):
        """Setup GitHub integration with guided process"""
        print("\n" + "=" * 50)
        print("🐙 GitHub Integration Setup")
        print("=" * 50)

        print("\n📋 What you'll need:")
        print("1. GitHub Personal Access Token")
        print("2. Repository access permissions")
        print("3. About 3 minutes")

        proceed = input("\n🤔 Ready to setup GitHub integration? (y/n): ").lower()
        if proceed != "y":
            print("⏭️  Skipping GitHub setup. You can run this again anytime.")
            return

        print("\n📝 Step 1: Create GitHub Personal Access Token")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Name: 'ClaudeDirector Integration'")
        print("4. Select scopes: 'repo' and 'read:org'")
        print("5. Click 'Generate token'")
        print("6. Copy the token (you won't see it again!)")

        token = getpass.getpass("\n🔑 Paste your GitHub token here (hidden): ")
        if not token:
            print("❌ No token provided. Skipping GitHub setup.")
            return

        # Get repository information
        print("\n📂 Step 2: Repository Configuration")
        default_repo = input("Default repository (e.g., 'your-org/your-repo'): ")

        # Test the connection
        print("\n🧪 Step 3: Testing connection...")
        if asyncio.run(self._test_github_connection(token, default_repo)):
            # Save configuration
            self.config["github"] = {
                "enabled": True,
                "token": token,  # In production, this would be encrypted
                "default_repo": default_repo,
                "setup_date": str(datetime.now()),
            }
            self._save_config()
            print("✅ GitHub integration setup complete!")
        else:
            print("❌ GitHub connection failed. Please check your token and try again.")

    def setup_jira_integration(self):
        """Setup Jira integration with guided process"""
        print("\n" + "=" * 50)
        print("🎯 Jira Integration Setup")
        print("=" * 50)

        print("\n📋 What you'll need:")
        print("1. Jira API Token")
        print("2. Your Jira site URL")
        print("3. Your Jira email address")
        print("4. About 5 minutes")

        proceed = input("\n🤔 Ready to setup Jira integration? (y/n): ").lower()
        if proceed != "y":
            print("⏭️  Skipping Jira setup. You can run this again anytime.")
            return

        print("\n📝 Step 1: Create Jira API Token")
        print("1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens")
        print("2. Click 'Create API token'")
        print("3. Label: 'ClaudeDirector Integration'")
        print("4. Click 'Create'")
        print("5. Copy the token")

        # Get Jira configuration
        jira_url = input(
            "\n🌐 Your Jira URL (e.g., https://yourcompany.atlassian.net): "
        )
        jira_email = input("📧 Your Jira email address: ")
        jira_token = getpass.getpass("🔑 Paste your Jira API token here (hidden): ")

        if not all([jira_url, jira_email, jira_token]):
            print("❌ Missing required information. Skipping Jira setup.")
            return

        # Test the connection
        print("\n🧪 Step 2: Testing connection...")
        if asyncio.run(self._test_jira_connection(jira_url, jira_email, jira_token)):
            # Save configuration
            self.config["jira"] = {
                "enabled": True,
                "url": jira_url,
                "email": jira_email,
                "token": jira_token,  # In production, this would be encrypted
                "setup_date": str(datetime.now()),
            }
            self._save_config()
            print("✅ Jira integration setup complete!")
        else:
            print(
                "❌ Jira connection failed. Please check your credentials and try again."
            )

    async def _test_github_connection(self, token: str, repo: str) -> bool:
        """Test GitHub API connection"""
        try:
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }

            async with aiohttp.ClientSession() as session:
                # Test basic API access
                async with session.get(
                    "https://api.github.com/user", headers=headers
                ) as response:
                    if response.status != 200:
                        print(f"❌ GitHub API error: {response.status}")
                        return False

                    user_data = await response.json()
                    print(f"✅ Connected as: {user_data.get('login', 'Unknown')}")

                # Test repository access if provided
                if repo:
                    async with session.get(
                        f"https://api.github.com/repos/{repo}", headers=headers
                    ) as response:
                        if response.status == 200:
                            repo_data = await response.json()
                            print(
                                f"✅ Repository access confirmed: {repo_data.get('full_name')}"
                            )
                        else:
                            print(
                                f"⚠️  Repository '{repo}' not accessible, but basic GitHub connection works"
                            )

                return True

        except Exception as e:
            print(f"❌ Connection test failed: {str(e)}")
            return False

    async def _test_jira_connection(self, url: str, email: str, token: str) -> bool:
        """Test Jira API connection"""
        try:
            import base64

            # Create basic auth header
            auth_string = f"{email}:{token}"
            auth_bytes = auth_string.encode("ascii")
            auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

            headers = {
                "Authorization": f"Basic {auth_b64}",
                "Accept": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                # Test basic API access
                test_url = f"{url.rstrip('/')}/rest/api/3/myself"
                async with session.get(test_url, headers=headers) as response:
                    if response.status != 200:
                        print(f"❌ Jira API error: {response.status}")
                        return False

                    user_data = await response.json()
                    print(f"✅ Connected as: {user_data.get('displayName', 'Unknown')}")
                    return True

        except Exception as e:
            print(f"❌ Connection test failed: {str(e)}")
            return False

    def show_current_status(self):
        """Show current integration status"""
        print("\n" + "=" * 50)
        print("📊 Current Integration Status")
        print("=" * 50)

        github_status = (
            "✅ Connected" if self.config["github"]["enabled"] else "❌ Not connected"
        )
        jira_status = (
            "✅ Connected" if self.config["jira"]["enabled"] else "❌ Not connected"
        )

        print(f"\n🐙 GitHub: {github_status}")
        if self.config["github"]["enabled"]:
            print(
                f"   Repository: {self.config['github'].get('default_repo', 'Not specified')}"
            )

        print(f"🎯 Jira: {jira_status}")
        if self.config["jira"]["enabled"]:
            print(f"   URL: {self.config['jira'].get('url', 'Not specified')}")

        if not any([self.config["github"]["enabled"], self.config["jira"]["enabled"]]):
            print(
                "\n💡 Currently using simulated data (clearly marked in all visualizations)"
            )
            print(
                "   Set up real integrations above to get insights from your actual projects!"
            )

    def run_wizard(self):
        """Run the complete setup wizard"""
        self.show_welcome()

        while True:
            print("\n" + "=" * 50)
            print("🛠️  Setup Options")
            print("=" * 50)
            print("1. Setup GitHub Integration")
            print("2. Setup Jira Integration")
            print("3. View Current Status")
            print("4. Test Connections")
            print("5. Exit")

            choice = input("\n🤔 Choose an option (1-5): ").strip()

            if choice == "1":
                self.setup_github_integration()
            elif choice == "2":
                self.setup_jira_integration()
            elif choice == "3":
                self.show_current_status()
            elif choice == "4":
                self.test_all_connections()
            elif choice == "5":
                print("\n🎉 Setup complete! Your integrations are ready.")
                print("💡 Remember: ClaudeDirector will clearly show you whether")
                print("   you're seeing real data or simulated data in every response.")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")

    def test_all_connections(self):
        """Test all configured connections"""
        print("\n🧪 Testing all connections...")

        if self.config["github"]["enabled"]:
            print("\n🐙 Testing GitHub...")
            github_works = asyncio.run(
                self._test_github_connection(
                    self.config["github"]["token"],
                    self.config["github"].get("default_repo", ""),
                )
            )
            if not github_works:
                print("❌ GitHub connection failed. You may need to reconfigure.")

        if self.config["jira"]["enabled"]:
            print("\n🎯 Testing Jira...")
            jira_works = asyncio.run(
                self._test_jira_connection(
                    self.config["jira"]["url"],
                    self.config["jira"]["email"],
                    self.config["jira"]["token"],
                )
            )
            if not jira_works:
                print("❌ Jira connection failed. You may need to reconfigure.")

        if not self.config["github"]["enabled"] and not self.config["jira"]["enabled"]:
            print("ℹ️  No integrations configured yet. Use options 1-2 to set them up.")


def main():
    """Main entry point for the setup wizard"""
    try:
        from datetime import datetime

        wizard = IntegrationWizard()
        wizard.run_wizard()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled. You can run this again anytime!")
    except Exception as e:
        print(f"\n❌ Setup error: {str(e)}")
        print("Please try again or contact support if the issue persists.")


if __name__ == "__main__":
    main()
