#!/usr/bin/env python3
"""
Minimal coverage test - debugging version
"""
import unittest


def simple_function():
    """A simple function to generate coverage"""
    return "hello world"


class TestMinimalCoverage(unittest.TestCase):
    """Minimal test for coverage debugging"""

    def test_simple_coverage(self):
        """Test that calls a function to generate coverage"""
        result = simple_function()
        self.assertEqual(result, "hello world")


if __name__ == "__main__":
    unittest.main()
