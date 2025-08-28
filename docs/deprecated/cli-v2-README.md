# Deprecated CLI Archive

## Overview

This directory contains the deprecated ClaudeDirector CLI tool that was removed in v3.0.0.

## Why Deprecated

The CLI tool represented architectural debt and maintenance overhead when ClaudeDirector is designed for **Cursor-first integration**. Key issues:

1. **No Context Engineering Integration**: The CLI couldn't access our 7-layer strategic context system
2. **Missing Organizational Learning**: No support for our ML-powered organizational intelligence
3. **No Analytics Engine**: Missing our advanced analytics and predictive capabilities
4. **Legacy Focus**: Primarily supported outdated P1/P2.1 features
5. **Maintenance Overhead**: Complex 1,200+ line CLI for features better accessed in Cursor

## Migration Path

**OLD CLI Commands → NEW Cursor Integration:**

```bash
# OLD
./bin/claudedirector status
./bin/claudedirector alerts
./bin/claudedirector reports executive

# NEW - Ask Cursor directly:
"Show me system status and health"
"Generate executive alerts for today"
"Create an executive summary report"
```

## Superior Cursor Capabilities

ClaudeDirector through Cursor provides:

- **Context Engineering**: 7-layer strategic memory system
- **Organizational Learning**: Real-time cultural analysis and change tracking
- **Advanced Analytics**: ML-powered initiative health scoring
- **Framework Intelligence**: Automatic strategic framework detection
- **Multi-Persona Guidance**: Diego, Camille, Rachel, Alvaro, Martin, etc.
- **Real-time Integration**: Live workspace monitoring and context updates

## Files Archived

- `claudedirector-legacy.py` - Original CLI implementation (1,211 lines)
- `README.md` - This documentation

## System Administration

For database maintenance and system setup, use:

```bash
python .claudedirector/tools/setup/setup_database.py
```

## Complete Removal Timeline

The deprecated CLI stub will be completely removed in v4.0.0.
