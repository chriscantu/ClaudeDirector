# Rolling 90-Day Team Allocation Report

**Status**: Draft - Awaiting Approval
**Owner**: Diego | Engineering Leadership
**Methodology**: GitHub Spec-Kit + Sequential Thinking + Context7

---

## Quick Links

- **[spec.md](./spec.md)**: Complete specification (GitHub Spec-Kit format)
- **[plan.md](./plan.md)**: Implementation plan with ADR-004 refactoring

---

## Overview

Executive report showing platform team allocation across L0 (keep-the-lights-on), L1 (enabling work), and L2 (strategic initiatives) over rolling 90-day windows.

**Business Value**: Provides VP Engineering and VP Product visibility into "invisible work" consuming 60-70% of platform team capacity.

**Technical Approach**: Extends duration-agnostic `jira_reporter.py` architecture (refactored from `weekly_reporter.py` per ADR-004) following DRY principles (BLOAT_PREVENTION compliance).

---

## Approval Status

- ✅ **Problem Statement**: APPROVED
- ✅ **Security Compliance**: APPROVED (git history clean)
- ⏳ **Technical Design**: AWAITING APPROVAL
- ⏳ **Implementation**: PENDING

---

## Architecture Compliance

✅ **PROJECT_STRUCTURE.md**: Files placed in `.claudedirector/lib/reporting/`
✅ **BLOAT_PREVENTION_SYSTEM.md**: REUSE existing infrastructure, zero duplication
✅ **GitHub Spec-Kit Format**: Single consolidated spec.md
✅ **Security Requirements**: No PII/credentials in codebase

---

## Next Steps

Awaiting user approval to proceed with implementation.
