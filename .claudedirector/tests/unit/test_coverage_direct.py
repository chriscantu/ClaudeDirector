#!/usr/bin/env python3
"""
Direct Coverage Test
Imports actual library code directly for coverage measurement.
"""

import sys
import unittest
from pathlib import Path

# Add project paths for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))


class TestDirectCoverage(unittest.TestCase):
    """Direct test that exercises actual library code for coverage"""

    def test_import_and_use_formatting(self):
        """Test direct import and usage of formatting module"""
        # Test 1: Direct file import
        formatting_path = PROJECT_ROOT / ".claudedirector/lib/utils/formatting.py"
        self.assertTrue(
            formatting_path.exists(),
            f"Formatting module should exist at {formatting_path}",
        )

        # Test 2: Execute actual Python code from the module
        import importlib.util

        spec = importlib.util.spec_from_file_location("formatting", formatting_path)
        formatting_module = importlib.util.module_from_spec(spec)

        # This will actually execute the code and generate coverage
        spec.loader.exec_module(formatting_module)

        # Verify it loaded with actual functions that exist
        self.assertTrue(hasattr(formatting_module, "format_success"))
        self.assertTrue(hasattr(formatting_module, "format_error"))
        self.assertTrue(hasattr(formatting_module, "format_file_size"))

        # Actually call functions to exercise the code
        success_msg = formatting_module.format_success("test success")
        self.assertIn("test success", success_msg)

        file_size = formatting_module.format_file_size(1024)
        self.assertIsInstance(file_size, str)

    def test_import_and_use_exceptions(self):
        """Test direct import and usage of exceptions module"""
        exceptions_path = PROJECT_ROOT / ".claudedirector/lib/core/exceptions.py"
        self.assertTrue(
            exceptions_path.exists(),
            f"Exceptions module should exist at {exceptions_path}",
        )

        # Execute actual Python code from the module
        import importlib.util

        spec = importlib.util.spec_from_file_location("exceptions", exceptions_path)
        exceptions_module = importlib.util.module_from_spec(spec)

        # This will actually execute the code and generate coverage
        spec.loader.exec_module(exceptions_module)

        # Verify it loaded and use it
        self.assertTrue(hasattr(exceptions_module, "ClaudeDirectorError"))

        # Actually use the class to generate more coverage
        error_class = getattr(exceptions_module, "ClaudeDirectorError")
        test_error = error_class("test message")
        self.assertEqual(str(test_error), "test message")

    def test_import_and_use_cache(self):
        """Test direct import and usage of cache module"""
        cache_path = PROJECT_ROOT / ".claudedirector/lib/utils/cache.py"
        self.assertTrue(
            cache_path.exists(), f"Cache module should exist at {cache_path}"
        )

        # Execute actual Python code from the module
        import importlib.util

        spec = importlib.util.spec_from_file_location("cache", cache_path)
        cache_module = importlib.util.module_from_spec(spec)

        # This will actually execute the code and generate coverage
        spec.loader.exec_module(cache_module)

        # Verify it loaded
        self.assertTrue(hasattr(cache_module, "CacheManager"))


if __name__ == "__main__":
    unittest.main()
