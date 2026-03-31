# Aegis Forensics Suite: Phase 1 Milestone

**University Project Submission: Part 1 of 4**

This directory contains the first developmental phase of the **Aegis Forensics Toolkit**. The goal of this phase was to establish the core graphical architecture and successfully integrate the first working forensic engine.

## 🏗️ Phase 1 Achievements

### 1. Graphical User Interface Architecture
- Developed a highly resilient, enterprise-style layout using pure `CustomTkinter` in Python. 
- Designed a 3-pane analytical FTK-style layout (Evidence Sidebar, Tabular Data Top-Grid, Raw Console Output Bottom-Grid).
- Wired buttons to future execution streams to demonstrate the ultimate software roadmap.

### 2. Forensic Engine 1: Metadata & EXIF Extraction
- Fully developed and integrated `metadata_module.py`.
- **Purpose**: Instantly strips deep-level GPS, hardware timestamps, and author properties from JPEGs and PDF payloads without detonating or rendering them.
- **Tools utilized**: Requires the powerful `ExifRead` and `PyMuPDF` algorithms for pure byte-level header parsing.

## 🚀 How to Run Phase 1

1. Ensure Python 3.8+ is installed.
2. Install the Phase 1 dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the GUI script:
   ```bash
   python main_gui.py
   ```
4. Click the **Extract Metadata (Active)** button to test the first core forensic module.

## 🗺️ Project Roadmap (Future Phases)

* **Phase 2:** Log Analytics & Hexadecimal Carving (Integrating standard RegEx capabilities).
* **Phase 3:** Cryptography & Remote API Validation (MD5, SHA, VirusTotal).
* **Phase 4:** Enterprise Deployment (Full MySQL database tracking and Flask Web App sandbox).
