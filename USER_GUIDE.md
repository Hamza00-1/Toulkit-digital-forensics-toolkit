# Aegis Forensics Suite: Enterprise User Guide (FTK Edition)

## 1. Executive Summary
The **Aegis Forensics Suite** has been globally upgraded to function as a high-density, analytical workstation, utilizing industry-standard design philosophies (similar to Exterro FTK and Autopsy). Instead of simple consumer-grade "apps", Aegis utilizes a **Professional 3-Pane Interface** across both its Desktop and Web modalities to maximize information density.

---

## 2. Navigating the 3-Pane Enterprise Layout

Whether you launch the Native Desktop Client (`main_gui.py`) or the Internal Web Server (`web_app.py`, accessed via Chrome/Edge), the layout operates the exact same way.

1. **Top Control Ribbon:** Your primary tools (Dashboard, Syslog Parser, Hasher) live at the very top of the screen. Clicking these will load the specific "Engine" into your workspace.
   - *Desktop Exclusive:* The "Night Ops" switch at the far right of the ribbon toggles between Dark Mode and Light Mode.
2. **Left Pane (Evidence Tree):** A consolidated view displaying the footprint of the investigation: showing exactly which evidence payloads have been loaded into memory and what operations have been executed.
3. **Top-Right Pane (Data Grid Viewer):** This is where structured, analytical data is rendered. For example:
   - Extracted EXIF attributes become a strict table.
   - 10,000 lines of raw authentication Syslogs are abstracted into a Pandas DataFrame table inside this grid.
   - Dashboard KPIs display as a grid.
4. **Bottom-Right Pane (Raw Detail / Hex Viewer):** This is your raw technical workspace. Whenever a tool runs, the pure JSON HTTP response from VirusTotal, the raw ASCII string from the Decoder, or the severe Threat Vector alerts from the Log Engine are pushed into this Hacker-style green/black terminal window for deep analysis.

---

## 3. Launch & Execution Modalities

### Mode A: Native Desktop Workstation (Recommended for deep local inspection)
Run the primary C++ customized Python script:
```cmd
python main_gui.py
```

### Mode B: Enterprise Web Platform (Recommended for browser-based workflow)
Run the web application server backend:
```cmd
python web_app.py
```
- Open any Chromium or Webkit browser and navigate to `http://127.0.0.1:5000` to access the full 3-Pane Web Workspace.

---

## 4. Forensic Engines inside the Data Grid

### 📊 Global Analytics Dashboard
- Automatically aggregates and populates the Data Grid with total system executions.
- The Engine parses the underlying database and pushes the most recent operations directly into the grid.

### 📄 Document Metadata Inspector
- Upload target `.jpg` or `.pdf` files.
- The extracted EXIF tags natively populate the top Data Grid for clean reading, while the raw JSON stream is piped into the bottom text viewer.

### 🔐 Cryptographic Integrity & VirusTotal
- Drag a payload to compute MD5, SHA-1, and SHA-256 values directly into the Data Grid.
- Input a VirusTotal API V3 key. The Engine will ping global repositories, and place the highly structured Threat Verdict (DANGER / CLEAN) directly into the Data Grid, while dumping the raw HTTP API payload into the text viewer.

### 🧩 Translation Decoder
- Designed to tightly decode Base64, Hexadecimal, and Binary payloads back to standard ASCII inside the bottom text viewer while keeping the control interface small in the top grid.

### 📈 Sentinel Syslog Abstractor
- Select raw Linux/Windows Authentication files.
- The system will dynamically build a Pandas DataFrame, formatting raw logs into the structured **Top Right Data Grid**.
- Any Brute Force signatures detected by Regex will immediately trigger a Critical Alert dumped explicitly into the **Bottom Right Hex Viewer**.
