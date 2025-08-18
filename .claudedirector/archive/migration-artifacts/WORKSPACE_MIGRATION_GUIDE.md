# 🔄 Workspace Migration Guide

## 🎯 **Workspace Name Change: `engineering-director-workspace` → `leadership-workspace`** ✅ **COMPLETED**

ClaudeDirector has updated the default workspace directory name to be more **inclusive and intuitive** for all leadership roles.

---

## 📋 **What Changed**

### **🔄 Directory Name**
- **Old**: `~/engineering-director-workspace/` (legacy)
- **New**: `~/leadership-workspace/` ✅ **ACTIVE**

### **🎯 Why the Change**
- **More Inclusive**: Works for VPs, CTOs, Principal Engineers, Tech Leads
- **Clearer Purpose**: "Leadership workspace" is more intuitive
- **Professional Language**: Business-friendly terminology
- **Future-Proof**: Adapts to role changes and organizational structure

---

## 🛠️ **Migration Options**

### **🎯 Option 1: Automatic Migration (Recommended)**

ClaudeDirector will automatically detect your legacy workspace and offer migration:

```bash
# When you run ClaudeDirector, you'll see:
📁 Found legacy workspace: ~/engineering-director-workspace
💡 Consider migrating to new location: ~/leadership-workspace

# Follow the prompts to migrate
```

### **🎯 Option 2: Manual Migration Script**

Use the built-in migration utility:

```bash
# Interactive migration (recommended)
python .claudedirector/dev-tools/migrate_workspace_name.py

# Or specific migration modes:
python .claudedirector/dev-tools/migrate_workspace_name.py --mode move
python .claudedirector/dev-tools/migrate_workspace_name.py --mode copy
python .claudedirector/dev-tools/migrate_workspace_name.py --mode symlink
```

### **🎯 Option 3: Manual Steps**

If you prefer to handle migration manually:

```bash
# 1. Move your workspace (if you have legacy directory)
mv ~/engineering-director-workspace ~/leadership-workspace

# 2. Update environment variable (add to your shell config)
export CLAUDEDIRECTOR_WORKSPACE="$HOME/leadership-workspace"

# 3. Verify migration
ls -la ~/leadership-workspace
```

---

## 🔧 **Migration Modes Explained**

### **📦 Move Mode (Recommended)**
- **What**: Renames the directory
- **Pros**: Clean, simple, one location
- **Cons**: Original directory no longer exists
- **Best For**: Most users

### **📋 Copy Mode**
- **What**: Creates copy at new location
- **Pros**: Preserves original as backup
- **Cons**: Uses double disk space
- **Best For**: Users who want backup safety

### **🔗 Symlink Mode**
- **What**: Creates symbolic link to original location
- **Pros**: No data movement, preserves original paths
- **Cons**: More complex, link dependency
- **Best For**: Users with external dependencies on original path

---

## ⚙️ **Environment Variable Update**

If you have `CLAUDEDIRECTOR_WORKSPACE` set, update it:

### **Shell Configuration Files**

**Bash/Zsh** (`~/.bashrc`, `~/.zshrc`):
```bash
# Old
export CLAUDEDIRECTOR_WORKSPACE="$HOME/engineering-director-workspace"

# New
export CLAUDEDIRECTOR_WORKSPACE="$HOME/leadership-workspace"
```

**Fish Shell** (`~/.config/fish/config.fish`):
```fish
# Old
set -x CLAUDEDIRECTOR_WORKSPACE "$HOME/engineering-director-workspace"

# New
set -x CLAUDEDIRECTOR_WORKSPACE "$HOME/leadership-workspace"
```

---

## 🛡️ **Data Safety**

### **✅ What's Protected**
- **All your strategic work files** are preserved during migration
- **File metadata** and lifecycle settings are maintained
- **Retention markings** and archived sessions are preserved
- **Configuration files** and preferences are kept

### **🔍 Verification Steps**
After migration, verify your data:

```bash
# Check workspace structure
ls -la ~/leadership-workspace/

# Verify important directories
ls ~/leadership-workspace/current-initiatives/
ls ~/leadership-workspace/meeting-prep/
ls ~/leadership-workspace/analysis-results/

# Check file counts match
find ~/leadership-workspace -type f | wc -l
```

---

## 🆘 **Troubleshooting**

### **❓ Migration Script Won't Run**
```bash
# Make script executable
chmod +x .claudedirector/dev-tools/migrate_workspace_name.py

# Or run with python directly
python3 .claudedirector/dev-tools/migrate_workspace_name.py
```

### **❓ Permission Errors**
```bash
# Check ownership
ls -la ~/engineering-director-workspace/

# Fix permissions if needed
chmod -R u+w ~/engineering-director-workspace/
```

### **❓ Both Directories Exist**
If both old and new directories exist:
1. **Compare contents** to ensure they're the same
2. **Choose which to keep** as your primary workspace
3. **Set environment variable** to point to chosen location
4. **Archive or remove** the unused directory

### **❓ ClaudeDirector Still Uses Old Location**
1. **Check environment variable**: `echo $CLAUDEDIRECTOR_WORKSPACE`
2. **Restart shell session** or reload configuration
3. **Verify new directory exists**: `ls -la ~/leadership-workspace`

---

## 🎯 **Post-Migration Checklist**

- [ ] New workspace directory exists and is accessible
- [ ] All strategic work files are present
- [ ] Environment variable updated (if used)
- [ ] Shell configuration reloaded
- [ ] ClaudeDirector recognizes new workspace location
- [ ] File lifecycle settings preserved
- [ ] Legacy directory handled (moved, archived, or removed)

---

## 📞 **Need Help?**

The migration is designed to be safe and straightforward, but if you encounter issues:

1. **Run analysis first**: `python migrate_workspace_name.py --analyze-only`
2. **Use interactive mode**: Provides step-by-step guidance
3. **Check logs**: Migration script provides detailed output
4. **Backup important files**: Before any major changes

---

**🎯 The new `leadership-workspace` name better reflects the inclusive, professional nature of ClaudeDirector while maintaining all your valuable strategic work.**
