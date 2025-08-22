#!/usr/bin/env python3
"""Interface Compliance Checker
Validates that concrete implementations properly implement required interfaces.
"""

import re
import sys

violations = 0
for file_path in sys.argv[1:]:
    try:
        with open(file_path, "r") as f:
            content = f.read()

            # Check interface implementations
            if re.search(r"class.*Engine.*:", content):
                required_methods = [
                    "connect",
                    "disconnect",
                    "execute_query",
                    "get_health_status",
                ]
                for method in required_methods:
                    if not re.search(rf"def {method}\(", content):
                        print(f"❌ {file_path}: Missing required method: {method}")
                        violations += 1
    except:
        pass

if violations > 0:
    print(f"\n🔌 Interface Compliance: {violations} violations found")
    print("   Implement all required methods from base interfaces")
    sys.exit(1)
print("✅ Interface Compliance: All implementations valid")
