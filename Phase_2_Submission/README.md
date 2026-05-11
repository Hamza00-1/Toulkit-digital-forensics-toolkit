# Aegis Forensics Suite: Phase 2 Milestone

**University Project Submission: Part 2 of 4**

This directory contains the second developmental phase of the **Aegis Forensics Toolkit**. The goal of this phase was to expand on the Phase 1 UI architecture by integrating robust pattern-recognition engines capable of parsing both plain text and raw hexadecimal bytes.

## 🏗️ Phase 2 Achievements

### 1. Forensic Engine 2: Syslog Brute-Force Analytics
- Fully developed and integrated `log_module.py`.
- **Purpose**: Instantly parses 10,000+ line security logs (`auth.log`) using deeply optimized Regular Expressions to structure messy syslog strings into a unified matrix (`pandas` dataframe).
- **Automation**: Actively monitors time-deltas between SSH failures to automatically flag anomalous IP addresses attempting Brute-Force intrusions.

### 2. Forensic Engine 3: Hexadecimal Carver
- Fully developed and integrated `recovery_module.py`.
- **Purpose**: Forensically resurrects deleted JPEGs and PDFs from corrupted raw binary streams.
- **The Tech**: It ignores operating-system file allocation tables. It utilizes pure binary iteration to hunt for precise Magic Numbers (e.g. `\xFF\xD8\xFF` for JPEGs) to slice out valid chunks of data stranded in a sea of raw disk memory.

## 🚀 How to Run Phase 2

1. Make sure you have python installed.
2. Install the new Phase 2 dependencies (Pandas):
   ```bash
   pip install -r requirements.txt
   ```
3. Generate the test evidence sandbox:
   ```bash
   python generate_evidence.py
   ```
4. Run the GUI:
   ```bash
   python main_gui.py
   ```
5. Click **Parse Syslog** and select `server_auth.log` to watch the regex engine find the Brute-Force IP.
6. Click **Carve Raw Hex** and select `corrupted_hdd_sector.bin` to dynamically recover a hidden, valid image from the file bytes!

## 🗺️ Project Roadmap (Future Phases)

* **Phase 3:** Cryptography & Remote API Validation (MD5, SHA, Base64 Decoder, VirusTotal Threat API).
* **Phase 4:** Enterprise Web Deployment (Flask Dashboard syncing to live MySQL database).
