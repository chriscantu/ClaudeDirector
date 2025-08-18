# 📁 Leadership Workspace Organization

**Last Updated**: $(date)
**Status**: ✅ Organized and Clean
**Auto-Cleanup**: Enabled (Weekly Sundays)

---

## 🗂️ **Current Directory Structure**

### **Active Work Areas**
```
leadership-workspace/
├── strategy/           # Current strategic analysis and planning
├── reports/            # Weekly reports and status updates
├── meeting-prep/       # SLT reviews, 1:1s, stakeholder meetings
├── current-initiatives/ # Active projects and initiatives
├── data/              # Analysis data and research
└── configs/           # Configuration files and templates
```

### **Archive Organization**
```
archive/
├── completed-projects/ # Finished work and final reports
├── security-work/      # Security enhancement project files
├── context-system/     # Framework development files
├── outdated-analysis/  # Historical analysis and research
└── temp-work/         # Temporary files (auto-deleted after 30 days)
```

---

## 🤖 **Automated Cleanup System**

### **Weekly Cleanup** (Sundays)
- Moves completed project files to archive
- Organizes security and framework development files
- Removes temporary files older than 30 days
- Updates workspace documentation

### **File Organization Patterns**
```
Security Files → archive/security-work/
Context System → archive/context-system/
Completed TODOs → archive/completed-projects/
Temporary Analysis → archive/temp-work/
```

### **Manual Cleanup Commands**
```bash
# Run immediate cleanup
python3 leadership-workspace/scripts/workspace_cleanup.py

# Weekly maintenance
./leadership-workspace/scripts/weekly_cleanup.sh

# Check workspace status
find leadership-workspace -maxdepth 1 -name "*.md" | wc -l
```

---

## 📋 **File Naming Conventions**

### **Current Work** (Keep in main directories)
- **Strategy**: `TOPIC_STRATEGIC_ANALYSIS.md`
- **Reports**: `weekly-report-YYYY-MM-DD.md`
- **Meeting Prep**: `meeting-type-YYYY-MM-DD.md`
- **Initiatives**: `project-name-status.md`

### **Archive Candidates** (Auto-moved)
- **Completed**: `*_COMPLETE.md`, `*_FINAL_REPORT.md`
- **Security**: `*SECURITY*`, `*TRUST*`, `*PROCESS_FAILURE*`
- **Context**: `*CONTEXT*`, `*FRAMEWORK*`, `*RESTART*`
- **Temporary**: `*VALIDATION*`, `*IMPROVEMENT*`

---

## 🎯 **Best Practices**

### **Keep Main Workspace Clean**
- ✅ Only active work in root directories
- ✅ Use descriptive, consistent file names
- ✅ Archive completed work regularly
- ✅ Delete unnecessary temporary files

### **Strategy Directory Organization**
- **Current Focus**: Design system offsite planning
- **Active Projects**: Platform ROI analysis, SLT communication
- **Completed**: Moved to archive/completed-projects/

### **Automated Maintenance**
- **Sunday Cleanup**: Automatic file organization
- **30-Day Cleanup**: Remove old temporary files
- **Workspace Monitoring**: Alert when directories get too large

---

## 🚨 **When to Run Manual Cleanup**

### **Immediate Cleanup Needed If**:
- More than 10 markdown files in workspace root
- Completed project files not archived
- Security/framework work files accumulating
- Strategy directory over 15 files

### **Commands**:
```bash
# Quick status check
ls -la leadership-workspace/*.md | wc -l

# Emergency cleanup
python3 leadership-workspace/scripts/workspace_cleanup.py

# Full reorganization
./leadership-workspace/scripts/weekly_cleanup.sh
```

---

**The workspace is now organized and will stay clean with automated weekly maintenance!** 🧹✨
