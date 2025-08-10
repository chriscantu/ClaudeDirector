# 🛡️ SECURITY POLICY - ClaudeDirector Platform

## **CRITICAL SECURITY MANDATE**
**--persona-martin: ZERO TOLERANCE for sensitive data in version control**

---

## **🚨 SECURITY INCIDENT RESPONSE**

### **Immediate Actions if Sensitive Data is Committed:**

1. **STOP ALL PUSHES** to remote repositories
2. **CONTACT SECURITY TEAM** immediately
3. **FOLLOW GIT HISTORY SANITIZATION** procedures below
4. **ROTATE ALL POTENTIALLY EXPOSED CREDENTIALS**

---

## **🔒 PROTECTED DATA CATEGORIES**

### **NEVER COMMIT THESE FILES:**

#### **Database Files**
- `*.db`, `*.sqlite`, `*.sqlite3`
- `strategic_memory.db` (contains strategic intelligence)
- `stakeholder*.db` (contains relationship data)
- `meeting*.db` (contains meeting intelligence)

#### **Credentials & Secrets**
- `*.key`, `*.pem`, `*.p12`, `*.pfx`
- Files containing `password`, `credential`, `secret`
- `.env` files (except `.env.template`)
- API keys, tokens, connection strings

#### **Strategic Data**
- Board presentation materials
- Stakeholder relationship data
- Executive session notes
- Financial projections
- Organizational charts with sensitive info

---

## **🛡️ PREVENTION MECHANISMS**

### **1. Pre-commit Security Scanner**
Location: `tools/security/sensitive_data_scanner.py`

**Automatically blocks commits containing:**
- Database files
- Credential patterns
- Sensitive content patterns
- Strategic data markers

### **2. Enhanced .gitignore**
Comprehensive patterns prevent accidental staging

### **3. Pre-commit Hooks**
```bash
# Install hooks
pre-commit install

# Test security scanner
python3 tools/security/sensitive_data_scanner.py
```

---

## **🔧 GIT HISTORY SANITIZATION**

### **If Sensitive Data is Already Committed:**

```bash
# 1. Install git-filter-repo
pip install git-filter-repo

# 2. Remove specific file from ALL history
git filter-repo --path SENSITIVE_FILE --invert-paths --force

# 3. Remove specific pattern from ALL history
git filter-repo --path-regex 'PATTERN' --invert-paths --force

# 4. Re-add remote (filter-repo removes it for safety)
git remote add origin <repository-url>

# 5. Force push (COORDINATE WITH TEAM)
git push --force-with-lease --all
git push --force-with-lease --tags
```

### **Example: Remove Database Files**
```bash
# Remove all database files from history
git filter-repo --path-regex '.*\.(db|sqlite|sqlite3)$' --invert-paths --force
```

---

## **📋 SECURITY CHECKLIST**

### **Before Every Commit:**
- [ ] No database files staged
- [ ] No credential files staged
- [ ] No `.env` files (except templates)
- [ ] No strategic data files
- [ ] Pre-commit hooks passing
- [ ] Security scanner passing

### **Before Every Push:**
- [ ] All commits security-scanned
- [ ] No sensitive data in diff
- [ ] Remote is trusted repository
- [ ] Team notified of security-relevant changes

---

## **🎯 SECURITY ARCHITECTURE PRINCIPLES**

### **1. Defense in Depth**
- Multiple prevention layers
- Automated scanning
- Manual verification
- Process enforcement

### **2. Fail-Safe Defaults**
- Block by default
- Require explicit approval
- Conservative scanning
- Zero false negatives preferred

### **3. Least Privilege**
- Minimal sensitive data storage
- Environment-based secrets
- Encrypted data at rest
- Secure communication channels

---

## **🚨 INCIDENT ESCALATION**

### **Severity Levels:**

#### **CRITICAL** - Immediate Action Required
- Production credentials exposed
- Strategic database in git history
- Customer data exposed
- Financial information leaked

#### **HIGH** - Action Required Within 1 Hour
- Development credentials exposed
- Internal documentation leaked
- System architecture exposed

#### **MEDIUM** - Action Required Within 24 Hours
- Test data with PII patterns
- Internal process documentation
- Non-sensitive configuration

---

## **📞 SECURITY CONTACTS**

- **Platform Security**: martin@platform-security.internal
- **Incident Response**: security-incident@company.com
- **Compliance Team**: compliance@company.com

---

## **🔍 SECURITY MONITORING**

### **Automated Monitoring:**
- Pre-commit security scans
- CI/CD security gates
- Repository monitoring
- Credential leak detection

### **Manual Audits:**
- Quarterly security reviews
- Annual pen testing
- Code security audits
- Incident post-mortems

---

## **📚 SECURITY TRAINING**

### **Required Training:**
1. Git security best practices
2. Credential management
3. Data classification
4. Incident response procedures

### **Resources:**
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Git Security Documentation](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**Remember: When in doubt, DO NOT COMMIT. Consult security team first.**

*This policy enforced by --persona-martin's zero-tolerance security mandate.*
