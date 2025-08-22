#!/usr/bin/env python3
"""Domain Boundary Enforcement Tool
Ensures proper separation between business domains.
"""

import re
import sys

violations = 0
for file_path in sys.argv[1:]:
    try:
        with open(file_path, "r") as f:
            content = f.read()

            # Check for cross-domain imports
            if "domains/decision_intelligence" in file_path:
                if re.search(r"from.*health_assessment", content):
                    print(
                        f"❌ {file_path}: Decision domain importing from Health domain"
                    )
                    violations += 1
            if "domains/health_assessment" in file_path:
                if re.search(r"from.*decision_intelligence", content):
                    print(
                        f"❌ {file_path}: Health domain importing from Decision domain"
                    )
                    violations += 1
    except:
        pass

if violations > 0:
    print(f"\n🏗️ Domain Boundaries: {violations} violations found")
    print("   Use shared interfaces in shared/infrastructure/")
    sys.exit(1)
print("✅ Domain Boundaries: Clean separation maintained")
