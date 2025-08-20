#!/usr/bin/env python3
"""
Test User Configuration System
Validates that user identity configuration works correctly with fallbacks.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

from config.user_config import UserConfigManager, UserIdentity, get_user_identity


class TestUserConfiguration(unittest.TestCase):
    """Test user configuration system"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config_path = Path(self.temp_dir) / "user_identity.yaml"

        # Clear any existing environment variables
        self.original_env = {}
        env_vars = [
            'CLAUDEDIRECTOR_USER_NAME',
            'CLAUDEDIRECTOR_WORK_NAME',
            'CLAUDEDIRECTOR_FULL_NAME',
            'CLAUDEDIRECTOR_USER_ROLE',
            'CLAUDEDIRECTOR_ORGANIZATION'
        ]

        for var in env_vars:
            self.original_env[var] = os.environ.get(var)
            if var in os.environ:
                del os.environ[var]

    def tearDown(self):
        """Clean up test environment"""
        # Restore environment variables
        for var, value in self.original_env.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

        # Clean up temp files
        if self.test_config_path.exists():
            self.test_config_path.unlink()
        os.rmdir(self.temp_dir)

    def test_default_user_identity(self):
        """Test default user identity when no config exists"""
        manager = UserConfigManager(self.test_config_path)
        identity = manager.get_user_identity()

        self.assertEqual(identity.name, "User")
        self.assertEqual(identity.work_name, "")
        self.assertEqual(identity.full_name, "")
        self.assertEqual(identity.get_attribution(), "User's requirement")

    def test_yaml_config_loading(self):
        """Test loading configuration from YAML file"""
        # Create test config file
        config_content = """# Test user config
user:
  name: "TestUser"
  work_name: "TestUser"
  full_name: "Test User Full"
  role: "Test Role"
  organization: "Test Org"
"""

        with open(self.test_config_path, 'w') as f:
            f.write(config_content)

        manager = UserConfigManager(self.test_config_path)
        identity = manager.get_user_identity()

        self.assertEqual(identity.name, "TestUser")
        self.assertEqual(identity.work_name, "TestUser")
        self.assertEqual(identity.full_name, "Test User Full")
        self.assertEqual(identity.role, "Test Role")
        self.assertEqual(identity.organization, "Test Org")
        self.assertEqual(identity.get_attribution(), "TestUser's requirement")

    def test_environment_variable_override(self):
        """Test environment variables override file config"""
        # Create test config file
        config_content = """user:
  name: "FileUser"
  work_name: "FileUser"
"""

        with open(self.test_config_path, 'w') as f:
            f.write(config_content)

        # Set environment variables
        os.environ['CLAUDEDIRECTOR_USER_NAME'] = "EnvUser"
        os.environ['CLAUDEDIRECTOR_WORK_NAME'] = "EnvWorkUser"

        manager = UserConfigManager(self.test_config_path)
        identity = manager.get_user_identity()

        # Environment should override file
        self.assertEqual(identity.name, "EnvUser")
        self.assertEqual(identity.work_name, "EnvWorkUser")
        self.assertEqual(identity.get_attribution(), "EnvWorkUser's requirement")

    def test_name_context_selection(self):
        """Test different name contexts"""
        identity = UserIdentity(
            name="Default",
            work_name="WorkName",
            full_name="Full Name",
            role="Test Role"
        )

        self.assertEqual(identity.get_name("default"), "Default")
        self.assertEqual(identity.get_name("work"), "WorkName")
        self.assertEqual(identity.get_name("full"), "Full Name")
        self.assertEqual(identity.get_name("professional"), "WorkName")

        # Test fallback when work_name is empty
        identity_no_work = UserIdentity(name="Default", work_name="")
        self.assertEqual(identity_no_work.get_name("professional"), "Default")

    def test_possessive_forms(self):
        """Test possessive name generation"""
        identity = UserIdentity(name="Cantu")
        self.assertEqual(identity.get_possessive(), "Cantu's")

        identity_s = UserIdentity(name="James")
        self.assertEqual(identity_s.get_possessive(), "James'")

    def test_config_file_parsing_robustness(self):
        """Test configuration file parsing handles various formats"""
        # Test with quotes
        config_content = """user:
  name: "Quoted Name"
  work_name: 'Single Quotes'
  full_name: No Quotes
"""

        with open(self.test_config_path, 'w') as f:
            f.write(config_content)

        manager = UserConfigManager(self.test_config_path)
        identity = manager.get_user_identity()

        self.assertEqual(identity.name, "Quoted Name")
        self.assertEqual(identity.work_name, "Single Quotes")
        self.assertEqual(identity.full_name, "No Quotes")

    def test_p0_enforcement_integration(self):
        """Test that P0 enforcement can use user configuration"""
        # Set up test config
        config_content = """user:
  name: "P0TestUser"
"""

        with open(self.test_config_path, 'w') as f:
            f.write(config_content)

        # Test the specific functions used by P0 enforcement
        manager = UserConfigManager(self.test_config_path)
        identity = manager.get_user_identity()

        attribution = identity.get_attribution()
        professional_name = identity.get_name("professional")

        self.assertEqual(attribution, "P0TestUser's requirement")
        self.assertEqual(professional_name, "P0TestUser")


def run_user_config_tests():
    """Run user configuration test suite"""
    print("🧪 USER CONFIGURATION TEST SUITE")
    print("=" * 50)
    print("Testing user identity and P0 enforcement integration")
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserConfiguration)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 50)
    print(f"📊 USER CONFIGURATION TEST RESULTS")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, error in result.errors:
            print(f"  {test}: {error}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n🎉 ALL USER CONFIGURATION TESTS PASSED")
        print("✅ User configuration system validated")
    else:
        print("\n❌ USER CONFIGURATION TESTS FAILED")
        print("🚫 Configuration system issues detected")

    return success


if __name__ == "__main__":
    success = run_user_config_tests()
    sys.exit(0 if success else 1)
