# Phase 1B: Hard-coded Value Migration Tracker

## 🎯 **Identified Hard-coded Values**

### **Threshold Values Found**
| File | Line | Current Value | Config Replacement | Status |
|------|------|---------------|-------------------|---------|
| `core/refactored_framework_engine.py` | 145 | `0.6` | `config.get_threshold('stakeholder_profiling_threshold')` | ✅ **COMPLETED** |
| `core/refactored_framework_engine.py` | 290 | `0.7` | `config.get_threshold('quality_threshold')` | ✅ **COMPLETED** |
| `core/refactored_framework_engine.py` | 416 | `0.5` | `config.get_threshold('performance_degradation_limit') * 10` | ✅ **COMPLETED** |
| `core/refactored_framework_engine.py` | 624 | `0.7` | `config.get_threshold('quality_threshold')` | ✅ **COMPLETED** |
| `core/refactored_framework_engine.py` | 626 | `0.5` | `config.get_threshold('performance_degradation_limit') * 10` | ✅ **COMPLETED** |

### **String Literals Found**
| File | Pattern | Config Replacement | Count | Status |
|------|---------|-------------------|-------|---------|
| `core/services/framework_analysis_service.py` | `"high"` | `config.get_enum_values('priority_levels')[1]` | 6 | ✅ **COMPLETED** |
| `core/services/framework_analysis_service.py` | `"medium"` | `config.get_enum_values('priority_levels')[2]` | 4 | ✅ **COMPLETED** |
| Multiple files | `"urgent"` | `config.get_enum_values('priority_levels')[0]` | ~15 | 🔄 Pending |
| Multiple files | `"low"` | `config.get_enum_values('priority_levels')[3]` | ~6 | 🔄 Pending |

## 📊 **Migration Progress**

- **Total Files to Update**: 23
- **Threshold Replacements**: 5/5 ✅ **COMPLETE**
- **Enum Replacements**: 10/41 🔄 **IN PROGRESS**
- **Overall Progress**: 33% (15/46 replacements)

## 🔧 **Next Actions**
1. Start with `core/refactored_framework_engine.py` (highest concentration)
2. Implement config injection pattern
3. Update service constructors
4. Validate with tests after each file
