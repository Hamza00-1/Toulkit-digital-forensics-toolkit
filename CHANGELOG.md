# 📝 Changelog — Aegis Forensics Suite

All notable changes to this project are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

- PDF export of investigation reports
- Cross-module timeline reconstruction

---

## [4.0.0] — 2026-03-31 — Enterprise Full-Stack Release

### Added
- **Flask Web Application** (`web_app.py`) with full 3-pane browser workspace
- **Jinja2 Templates**: `dashboard.html`, `metadata.html`, `hasher.html`, `decoder.html`, `logs.html`, `layout.html`
- **MySQL Backend** via `activity_tracker.py` — persistent logging of all forensic operations
- **Global Analytics Dashboard** — aggregates KPIs from MySQL into Data Grid
- **Server Workspace Sidebar** — right-click context menu routing (no re-upload)
- **`database_setup.sql`** — one-click schema initialization script
- **`test_toolkit.py`** — automated test suite for all forensic engines
- **`generate_test_files.py`** — helper to generate sample evidence files
- **`USER_GUIDE.md`** — comprehensive enterprise user documentation
- **Presentation Website** (`presentation_web/`) — static HTML/CSS overview

### Changed
- `main_gui.py` upgraded to full 5-engine enterprise layout (from Phase 1 prototype)
- All modules now integrate with `activity_tracker` for unified logging

---

## [3.0.0] — 2026-03 — Cryptography & Remote API Phase

### Added
- **`hash_module.py`** — MD5, SHA-1, SHA-256 computation with chunked streaming
- **VirusTotal API v3 Integration** — live threat verdict from 70+ AV engines
- **`decoding_module.py`** — Base64, Hexadecimal, Binary payload decoder

---

## [2.0.0] — 2026-03 — Log Analytics & File Recovery Phase

### Added
- **`log_module.py`** — multi-threaded Regex syslog parser with pandas DataFrame output
- **SSH Brute-Force Detection** — auto-flags IPs with 3+ failed auth attempts
- **`recovery_module.py`** — raw binary carver for JPEG and PDF magic number signatures

---

## [1.0.0] — 2026-03 — Phase 1 Foundation (University Milestone)

### Added
- Initial **CustomTkinter** desktop GUI — FTK-style 3-pane layout
- **`metadata_module.py`** — EXIF extraction (ExifRead) + PDF metadata (PyMuPDF)
- Phase 1 university submission directory (`Phase_1_Submission/`)
- Initial `requirements.txt`

---

*Aegis Forensics Suite — Built for Security Researchers & Digital Forensic Analysts*
