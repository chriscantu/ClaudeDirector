# ClaudeDirector Data Preservation Protocol

## 🚨 CRITICAL RULES (Non-Negotiable)

### **Rule 1: User Data Sacred**
- **User data must be preserved above ALL other tasks**
- **No exceptions, no shortcuts, no assumptions**
- **When in doubt, preserve everything**

### **Rule 2: Explicit Confirmation Required**
- **User data deletions require explicit confirmation from user**
- **Must specify exactly what will be deleted**
- **Must explain why deletion is necessary**
- **Must wait for user approval before proceeding**

### **Rule 3: Workspace and Database Priority**
- **Workspace files are user's primary work product**
- **Database files contain user's strategic intelligence**
- **Configuration files may contain user customizations**
- **Always preserve, never assume files are "system only"**

---

## 📋 DATA PRESERVATION CHECKLIST

### **Before ANY File Operations:**

#### **✅ IDENTIFY USER DATA:**
- [ ] Workspace directories (`~/engineering-director-workspace/`, any `workspace/`)
- [ ] Database files (`*.db`, `*.sqlite`, `*.sqlite3`)
- [ ] Configuration files with user customizations
- [ ] Any files in user-created directories
- [ ] Cache files that might contain user work
- [ ] Log files that might contain user data

#### **✅ MOVE vs DELETE DECISION:**
- [ ] Can this file be moved instead of deleted?
- [ ] Does this file contain any user customizations?
- [ ] Could this file be needed for data recovery?
- [ ] Is this file part of user's work product?

#### **✅ EXPLICIT USER CONFIRMATION (if deletion needed):**
- [ ] List exactly which files will be deleted
- [ ] Explain why deletion is necessary
- [ ] Show file sizes and modification dates
- [ ] Ask user to explicitly type "DELETE" to confirm
- [ ] Wait for user approval before proceeding

---

## 🛡️ PROTECTION MECHANISMS

### **1. Pre-Operation Data Audit:**
```bash
# Always run before major changes
echo "📊 PRE-OPERATION DATA AUDIT:"
echo "User workspace: $(ls -la ~/engineering-director-workspace/ 2>/dev/null | wc -l) items"
echo "Database files: $(find . -name "*.db" -o -name "*.sqlite" | wc -l) files"
echo "Config files: $(find . -name "*config*" | wc -l) files"
```

### **2. Move-First Policy:**
```bash
# ALWAYS try to move files before considering deletion
mkdir -p .backup/$(date +%Y%m%d_%H%M%S)/
mv suspicious_files/ .backup/$(date +%Y%m%d_%H%M%S)/
```

### **3. User Confirmation Template:**
```markdown
🚨 USER DATA DELETION REQUIRED

Files to be deleted:
- /path/to/file1 (size: XMB, modified: DATE)
- /path/to/file2 (size: XMB, modified: DATE)

Reason for deletion:
[Explain why these files cannot be moved or preserved]

⚠️ WARNING: This action cannot be undone.

Please type "DELETE" to confirm, or "MOVE" to move to backup instead:
```

---

## 📊 POST-OPERATION VERIFICATION

### **Required After Any File Operations:**
1. **✅ User Workspace Intact:**
   ```bash
   ls -la ~/engineering-director-workspace/
   ```

2. **✅ Critical Files Present:**
   ```bash
   ls -la .claudedirector/lib/claudedirector/core/
   ```

3. **✅ No Unexpected File Loss:**
   ```bash
   git status --porcelain
   ```

4. **✅ Functionality Preserved:**
   ```bash
   ./claudedirector --help
   ```

---

## 🚨 EMERGENCY RECOVERY PROCEDURES

### **If User Data is Accidentally Deleted:**

#### **1. Immediate Actions:**
- [ ] STOP all operations immediately
- [ ] Check git history: `git log --name-only`
- [ ] Check for backup copies in system
- [ ] Look for auto-backups or tmp files

#### **2. Recovery Methods:**
```bash
# Check git for deleted files
git log --diff-filter=D --summary

# Recover from git if possible
git checkout HEAD~1 -- path/to/deleted/file

# Check system backups
ls -la ~/.Trash/
ls -la /tmp/
```

#### **3. User Communication:**
- Immediately inform user of data loss
- Provide exact list of what was lost
- Explain all recovery attempts made
- Provide all available options for data recovery

---

## 💡 BEST PRACTICES

### **Always Safe Operations:**
- **Move files** instead of deleting when possible
- **Create timestamped backups** before major changes
- **Use git branches** for experimental restructuring
- **Test operations** on copies first

### **User-First Mindset:**
- **User's work is the most important thing**
- **Framework can be rebuilt, user data cannot**
- **When uncertain, ask the user**
- **Preserve now, optimize later**

### **Documentation:**
- **Log all file operations** performed
- **Document where files were moved**
- **Maintain audit trail** of changes
- **Keep recovery instructions** updated

---

## ✅ COMMITMENT

**I, as ClaudeDirector's AI assistant, commit to:**

1. **🔒 Never delete user data without explicit permission**
2. **🛡️ Always attempt to move/backup before deleting**
3. **📋 Follow the checklist for every file operation**
4. **🚨 Immediately alert user if any data is at risk**
5. **🔄 Perform post-operation verification every time**

**User data preservation is not negotiable. User's work and strategic intelligence is sacred.**

---

*This protocol ensures that ClaudeDirector always protects what matters most: the user's work and data.*
