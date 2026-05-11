# Aegis Digital Forensics Toolkit - Final Presentation Guide

This document is your ultimate cheat sheet for tomorrow's presentation. It contains exactly what you need to say, what you need to click, and the technical details you need to be ready to explain to your professor.

---

## 1. Pre-Presentation Checklist (Do this 10 mins before!)
1. **Start MAMP**: Open MAMP and click "Start Servers" (Ensure both Apache and MySQL are green).
2. **Database Check**: Ensure your `aegis_forensics` database is created and the `activity_logs` table exists.
3. **Start the GUI Engine**: Run `venv\Scripts\python main_gui.py` from your terminal/IDE.
4. **Start the Web Engine**: Run `venv\Scripts\python web_app.py` from your terminal/IDE.
5. **Open Browser**: Open `http://127.0.0.1:5000` in your web browser.
6. **Windows Defender**: Temporarily turn off "Real-time Protection" in Windows Defender, OR allow the `3_hash_vt_malware.txt` file so it doesn't get deleted during the Hash demo.

---

## 2. Presentation Script & Demonstration Flow

### Phase 1: Introduction (1 minute)
**What to say:** 
> *"Hello, today we are presenting the Aegis Digital Forensics Toolkit. Our goal was to build an enterprise-grade suite, inspired by industry tools like FTK, that allows investigators to process evidence, extract metadata, and identify threats efficiently. We built this with a dual-architecture: a heavy-duty Desktop Client built in Python, and a lightweight Web Dashboard built in Flask for remote triage."*

**What to do:**
* Have the **Desktop GUI** open on your screen. Toggle the "Night Ops" switch in the top right to show off the dark/light mode functionality.

### Phase 2: Core Modules Demonstration (3 minutes)

**Module 1: Metadata Extractor**
* **What to say:** *"First is the Metadata Extractor. This allows us to pull hidden properties like GPS coordinates, author tags, and creation dates from images and PDFs locally."*
* **What to do:** Click the **📁 Load Evidence (EXIF)** button. Load a test image/PDF from your `test_files` folder. Point out the extracted data in the Data Grid.

**Module 3: Cryptographic Validator (The Malware Demo)**
* **What to say:** *"For file integrity and threat intelligence, we built a Cryptographic Hasher. It calculates MD5, SHA-1, and SHA-256 hashes. More importantly, we integrated the VirusTotal API. By querying the API with our hash, we can instantly know if a file is known malware."*
* **What to do:** Click the **🔐 Compute Hashes** button. Load `test_files\3_hash_vt_malware.txt`. Click **"Query VirusTotal"**. Show the "DANGER" verdict.
* **Pro-tip:** *If the professor asks about the malware file, confidently explain: "This is the EICAR test string. It is a completely safe file explicitly designed by cybersecurity researchers to trigger antivirus engines so we can validate our API integration safely."*

**Module 2: Sentinel Syslog Abstractor**
* **What to say:** *"Next, we have the Sentinel Syslog Abstractor. Instead of manually reading thousands of lines of Linux server logs, this module maps the `auth.log` file into a Pandas DataFrame and uses Regular Expressions to instantly flag brute-force SSH attacks."*
* **What to do:** Click the **🔑 Parse Syslog** button. Load your test `.log` file. Show how the anomalies are flagged in red on the bottom viewer.

**Module 4: Message Decoder & Data Carving**
* **What to say:** *"We also included a Decoder to translate Base64, Hex, and Binary payloads back into plain text. Lastly, we have a Data Carving engine that can scan raw byte streams—like RAM dumps—and extract hidden files using Magic Headers."*
* **What to do:** Very quickly click the Decoder or Carving tabs just to show the UI.

### Phase 3: The Activity Dashboard & Database (1 minute)
**What to say:** *"To tie it all together, every action taken by the investigator is logged into a MySQL database. This guarantees a chain of custody. We can view these statistics live on the global dashboard."*
* **What to do:** Click the **📊 Dashboard** button on the Desktop App. Show the live statistics. 

### Phase 4: The Web Application (1 minute)
**What to say:** *"Finally, because modern forensics often requires remote collaboration, we mirrored these capabilities into a Web Application."*
* **What to do:** Switch your screen to your Web Browser (`http://127.0.0.1:5000`).
* **What to say:** *"Built with Flask, this dashboard connects to the exact same MySQL database and Python backend modules. It allows an investigator to upload evidence from any browser, run the same triage scans, and generate reports for non-technical stakeholders."*

---

## 3. Technical Q&A Cheat Sheet (If the Professor Asks)

**Q: What UI framework did you use for the Desktop app?**
* **A:** We used **CustomTkinter** rather than standard Tkinter because it allowed us to build a modern, responsive, dual-tone interface with hardware acceleration, mimicking professional tools like FTK.

**Q: How do you parse the server logs?**
* **A:** We use **Regular Expressions (`re`)** to isolate patterns, and then we load that data into a **`pandas` DataFrame**. This allows us to easily count IP addresses and flag any IP with more than 3 failed login attempts.

**Q: Does your app process files in memory or upload them?**
* **A:** All Metadata extraction (`exifread`, `fitz`), decoding (`base64`), carving, and log parsing happen **locally** on the machine for absolute security. The *only* time data leaves the machine is when we send a SHA-256 string to the VirusTotal REST API via the `requests` library.

**Q: How does the Activity Tracker work?**
* **A:** We use `mysql.connector` to connect to a local MAMP MySQL instance. Every time a forensic module executes, it triggers an `INSERT` statement logging the timestamp, module name, target file, and success/error status.
