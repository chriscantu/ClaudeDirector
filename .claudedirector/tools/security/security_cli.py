#!/usr/bin/env python3
"""
Security Scanner CLI
Lightweight interface to lib/security/scanners/ business logic
"""

import sys
from pathlib import Path

# Add lib path for imports
lib_path = Path(__file__).parent.parent.parent / ".claudedirector" / "lib"
sys.path.insert(0, str(lib_path))

from security.scanners.enhanced_security_scanner import EnhancedSecurityScanner


def main():
    """Lightweight CLI interface to Security Scanners"""
    try:
        scanner = EnhancedSecurityScanner()
        
        if len(sys.argv) < 2:
            print("Usage: security_cli.py <command> [args]")
            print("Commands: scan, validate, report")
            return
        
        command = sys.argv[1]
        
        if command == "scan":
            print("🔒 Running security scan...")
            results = scanner.scan_project()
            threats = results.get("threats_detected", 0)
            if threats == 0:
                print("✅ No security threats detected")
            else:
                print(f"⚠️  {threats} security threats found")
                
        elif command == "validate":
            print("🛡️  Validating security compliance...")
            is_compliant = scanner.validate_compliance()
            if is_compliant:
                print("✅ Security compliance validated")
            else:
                print("❌ Security compliance issues found")
                sys.exit(1)
                
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
