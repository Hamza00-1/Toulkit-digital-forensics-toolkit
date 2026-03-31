# 🔐 Security Policy — Aegis Forensics Suite

## Supported Versions

The following versions are currently supported with security updates:

| Version | Supported |
|---|---|
| Latest (`main` branch) | ✅ |
| Phase 4 release | ✅ |
| Phase 1–3 snapshots | ❌ Legacy only |

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in Aegis Forensics Suite, please report it responsibly:

1. **Email:** Contact the maintainer directly via GitHub ([@Hamza00-1](https://github.com/Hamza00-1)) using the "Report a vulnerability" button in the Security tab.
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (optional but appreciated)

We aim to respond within **72 hours** and will issue a patch within **7 days** for critical vulnerabilities.

---

## ⚠️ Important Usage Warning

Aegis Forensics Suite is designed for **authorized digital forensic investigations** and **educational purposes only**.

### DO ✅
- Use on files and systems you own or have explicit written authorization to analyze
- Use in academic, university, or controlled lab environments
- Use for malware research on isolated sandboxed systems

### DO NOT ❌
- Use to analyze files or systems you do not own or have authorization for
- Use to bypass security controls on production systems
- Use VirusTotal API integration with files containing real user PII/data without consent

**Misuse of this toolkit for unauthorized computer access may violate laws including the Computer Fraud and Abuse Act (CFAA), the UK Computer Misuse Act, or equivalent legislation in your jurisdiction.**

---

## Security Considerations for Deployment

- **Never expose the Flask web app (`web_app.py`) to a public network.** It is intended for `localhost` use only.
- The `uploads/` directory should be protected and never served publicly.
- VirusTotal API keys should be treated as secrets — never hardcode them in source files.
- Review the `.gitignore` to ensure no API keys or sensitive files are accidentally committed.

---

## Dependency Security

We recommend periodically auditing Python dependencies for known CVEs:

```bash
pip install pip-audit
pip-audit
```

---

*Aegis is a forensics tool — handle it responsibly.*
