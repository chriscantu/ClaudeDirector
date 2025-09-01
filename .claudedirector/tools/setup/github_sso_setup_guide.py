#!/usr/bin/env python3
"""
GitHub SSO Setup Guide & Repository Discovery
Phase 7 Week 3 - Enterprise GitHub Integration

🏗️ Martin | Platform Architecture - SSO integration
🔒 Elena | Compliance Strategy - Enterprise security
💼 Alvaro | Platform Investment Strategy - Business value

Comprehensive guide for setting up GitHub SSO access and discovering
available repositories within the Procore organization.
"""

import asyncio
import aiohttp
import json
import getpass
from pathlib import Path


async def discover_accessible_repositories(token: str):
    """Discover repositories accessible with the current token"""

    print("\n🔍 Discovering Accessible Repositories")
    print("=" * 50)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    async with aiohttp.ClientSession() as session:
        try:
            # Get user's repositories
            print("\n📂 Your Personal Repositories:")
            async with session.get(
                "https://api.github.com/user/repos?per_page=10", headers=headers
            ) as response:
                if response.status == 200:
                    repos = await response.json()
                    for repo in repos[:5]:  # Show first 5
                        print(
                            f"   • {repo['full_name']} ({'private' if repo['private'] else 'public'})"
                        )
                else:
                    print(f"   ❌ Error fetching personal repos: {response.status}")

            # Get organization repositories
            print("\n🏢 Organization Repositories:")
            async with session.get(
                "https://api.github.com/user/orgs", headers=headers
            ) as response:
                if response.status == 200:
                    orgs = await response.json()
                    for org in orgs:
                        org_name = org["login"]
                        print(f"\n   🏢 {org_name}:")

                        # Get repos for this org
                        async with session.get(
                            f"https://api.github.com/orgs/{org_name}/repos?per_page=10",
                            headers=headers,
                        ) as org_response:
                            if org_response.status == 200:
                                org_repos = await org_response.json()
                                for repo in org_repos[:5]:  # Show first 5
                                    print(
                                        f"      • {repo['name']} ({'private' if repo['private'] else 'public'})"
                                    )
                            else:
                                print(
                                    f"      ❌ Cannot access {org_name} repos (status: {org_response.status})"
                                )
                                if org_response.status == 403:
                                    print(
                                        f"      🔒 SSO authorization needed for {org_name}"
                                    )
                else:
                    print(f"   ❌ Error fetching organizations: {response.status}")

            # Test specific Procore repositories with different patterns
            print("\n🎯 Testing Procore Repository Patterns:")
            procore_patterns = [
                "procore/ui-service-shell",
                "procore/core",
                "procore/web",
                "procore/platform",
                "procoretech/ui-service-shell",
                "procoretech/core",
                "procoretech/web",
                "procoretech/platform",
            ]

            for repo_pattern in procore_patterns:
                async with session.get(
                    f"https://api.github.com/repos/{repo_pattern}", headers=headers
                ) as response:
                    if response.status == 200:
                        repo_data = await response.json()
                        print(f"   ✅ {repo_pattern} - Accessible!")
                        print(
                            f"      📝 {repo_data.get('description', 'No description')}"
                        )
                    elif response.status == 404:
                        print(f"   ❌ {repo_pattern} - Not found or no access")
                    elif response.status == 403:
                        print(f"   🔒 {repo_pattern} - SSO authorization needed")
                    else:
                        print(f"   ❓ {repo_pattern} - Status: {response.status}")

        except Exception as e:
            print(f"❌ Discovery error: {str(e)}")


def show_sso_setup_instructions():
    """Show detailed SSO setup instructions"""

    print("\n" + "=" * 70)
    print("🔐 GitHub SSO Setup Instructions")
    print("=" * 70)

    print("\n📋 **STEP 1: Enable SSO for Your Token**")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Find your 'ClaudeDirector Integration' token")
    print("3. Look for 'Configure SSO' button next to it")
    print("4. Click 'Configure SSO'")
    print("5. You'll see a list of organizations")
    print("6. Find 'Procore Technologies' (or similar)")
    print("7. Click 'Authorize' next to it")
    print("8. Confirm the authorization")

    print("\n📋 **STEP 2: Verify Token Scopes**")
    print("Make sure your token has these scopes:")
    print("• ✅ repo (Full control of private repositories)")
    print("• ✅ read:org (Read org and team membership)")
    print("• ✅ read:user (Read user profile data)")

    print("\n📋 **STEP 3: Organization Access**")
    print("If you don't see 'Procore Technologies' in SSO options:")
    print("• Contact your GitHub admin to add you to the org")
    print("• Ensure you have the right permissions")
    print("• Check if the org name is different (e.g., 'procoretech')")

    print("\n🚨 **Common Issues & Solutions**")
    print("• **404 Not Found**: Repository doesn't exist or no access")
    print("  → Check repository name spelling")
    print("  → Verify you're a member of the organization")
    print("  → Ensure SSO is properly configured")
    print("")
    print("• **403 Forbidden**: SSO authorization needed")
    print("  → Follow Step 1 above to authorize your token")
    print("  → Wait a few minutes for changes to take effect")
    print("")
    print("• **401 Unauthorized**: Token issues")
    print("  → Regenerate your token")
    print("  → Check token hasn't expired")
    print("  → Verify token scopes are correct")


async def main():
    """Main SSO setup and testing function"""

    print("🔐 GitHub SSO Setup & Repository Discovery")
    print("=" * 60)

    print("\n💡 This tool helps you:")
    print("• Set up GitHub SSO access for Procore repositories")
    print("• Discover which repositories you can access")
    print("• Test your token configuration")
    print("• Troubleshoot common SSO issues")

    # Show setup instructions first
    show_sso_setup_instructions()

    # Ask if user wants to test their current setup
    test_now = input(
        "\n🤔 Do you want to test your current GitHub token? (y/n): "
    ).lower()

    if test_now == "y":
        token = getpass.getpass("\n🔑 Enter your GitHub token: ")
        if token:
            await discover_accessible_repositories(token)
        else:
            print("❌ No token provided.")

    print("\n" + "=" * 60)
    print("🎯 Next Steps")
    print("=" * 60)

    print("\n1. **Complete SSO Setup** (if not done)")
    print("   → Follow the instructions above")
    print("   → Authorize your token for Procore organization")

    print("\n2. **Update ClaudeDirector Configuration**")
    print("   → Run the integration wizard again")
    print("   → Use the correct repository names you discovered")

    print("\n3. **Test Real Data Integration**")
    print("   → Once SSO is working, ClaudeDirector will show:")
    print("   → '✅ REAL DATA' instead of '🚨 SIMULATED DATA'")

    print("\n💡 **Pro Tip**: Start with one repository that you know exists")
    print("   and has the right permissions, then expand from there!")


if __name__ == "__main__":
    asyncio.run(main())
