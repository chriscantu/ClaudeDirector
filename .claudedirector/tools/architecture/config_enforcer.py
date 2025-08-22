#!/usr/bin/env python3
"""Configuration-First Enforcement Tool
Detects hard-coded values that should be in configuration files.
"""

import re
import sys

hardcode_patterns = [
    r'["\'][^"\']*(?:urgent|high|medium|low)[^"\'"]*["\']',
    r'["\'][^"\']*(?:excellent|healthy|at_risk|failing)[^"\'"]*["\']',
    r'["\'][^"\']*(?:strategic|operational|technical)[^"\'"]*["\']',
    r"0\.[0-9]+(?=\s*[,)])",
]

violations = 0
for file_path in sys.argv[1:]:
    if not file_path.endswith(".py"):
        continue
    try:
        with open(file_path, "r") as f:
            content = f.read()
            for i, line in enumerate(content.split("\n"), 1):
                if "test" not in file_path.lower() and not line.strip().startswith("#"):
                    for pattern in hardcode_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            print(
                                f"❌ {file_path}:{i} Hard-coded value: {line.strip()[:50]}..."
                            )
                            violations += 1
    except:
        pass

sys.exit(1 if violations > 0 else 0)
