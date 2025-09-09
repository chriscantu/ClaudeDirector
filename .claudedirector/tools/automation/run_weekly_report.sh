#!/bin/bash
# Wrapper script for Python weekly report generator
# Provides backward compatibility with existing bash script interface

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/weekly_report_generator.py"

# Check if Python script exists
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Error: Python weekly report generator not found at $PYTHON_SCRIPT"
    exit 1
fi

# Pass all arguments to Python script
python3 "$PYTHON_SCRIPT" "$@"
