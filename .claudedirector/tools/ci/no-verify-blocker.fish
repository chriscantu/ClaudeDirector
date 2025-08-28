# Fish shell function to block --no-verify usage
# Add this to your ~/.config/fish/config.fish or source it in your shell

function git
    # Check if any argument contains --no-verify
    for arg in $argv
        if string match -q "*no-verify*" $arg
            echo "🚨 CRITICAL VIOLATION: --no-verify usage is PERMANENTLY BLOCKED"
            echo "============================================================"
            echo "❌ COMMAND BLOCKED: git $argv"
            echo "============================================================"
            echo ""
            echo "🛡️ ENFORCEMENT: --no-verify bypasses are not allowed"
            echo "   Fix the underlying issues instead of bypassing verification"
            echo ""
            echo "✅ Use proper git commands without --no-verify"
            echo "❌ --no-verify is disabled for security and quality assurance"
            echo ""
            return 1
        end
    end

    # If no --no-verify detected, run the actual git command
    command git $argv
end
