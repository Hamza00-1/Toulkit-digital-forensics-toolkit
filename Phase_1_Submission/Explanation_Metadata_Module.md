# Phase 1: Metadata Extraction Module Explanation

This document is designed to explain the inner workings of our `metadata_module.py` script and the external libraries it relies on. It serves as a clear guide to demonstrate our understanding of the Phase 1 implementation.

## Overview of `metadata_module.py`

The `metadata_module.py` script is responsible for extracting hidden information (metadata) from files. In digital forensics, metadata is crucial as it can reveal the history, origin, and author of a file. 

### How It Works:
1. **Entry Point (`extract_metadata`)**:
   - The main function receives a `file_path` as input.
   - It first verifies if the file actually exists on the system.
   - It then checks the file extension to determine the type of the file.
   - Based on the extension (e.g., `.jpg`, `.png`, `.pdf`), it routes the file to the appropriate specialized helper function.
   
2. **Image Processing (`_extract_image_metadata`)**:
   - If the file is an image, this function opens the file in binary read mode (`'rb'`).
   - It filters out bulky, unnecessary data like visual thumbnails (`JPEGThumbnail`, `TIFFThumbnail`) to keep the forensics output clean and relevant.
   - It stores the readable tags in a dictionary structure so it can be easily displayed by the user interface.

3. **PDF Processing (`_extract_pdf_metadata`)**:
   - If the file is a PDF, this function opens the document.
   - It extracts the built-in `metadata` dictionary of the PDF document (which often contains fields like Author, Title, CreationDate, Producer, and ModDate).
   - Finally, it safely closes the document to free up system memory and resources.

---

## The Libraries We Used

To ensure our tool is robust and accurate, we utilized two powerful, well-established Python libraries: **ExifRead** and **PyMuPDF**.

### 1. What is ExifRead?
**ExifRead** is a Python library specifically designed to extract **EXIF** (Exchangeable Image File Format) metadata from image files (such as JPEGs and TIFFs). 

- **Why we used it:** When a digital camera or smartphone takes a picture, it embeds hidden data into the image file. This data can include the exact date and time the photo was taken, the device model, camera settings (aperture, ISO), and sometimes even the exact GPS coordinates (Geotagging) where the photo was taken. `ExifRead` allows our tool to safely parse and pull this data out without altering the original evidence file, which is a fundamental rule in digital forensics.

### 2. What is PyMuPDF?
**PyMuPDF** (which is accessed in Python scripts by importing `fitz`) is a high-performance library for reading, parsing, and manipulating PDF files and other document formats.

- **Why we used it:** PDFs store metadata entirely differently than images. They have specialized data structures that contain document information. PyMuPDF is extremely fast and lightweight compared to other Python PDF libraries. We use it to open the PDF, access its inherent `.metadata` attribute (revealing the creator software, author names, and timestamps), and securely close the file. This process is seamless and ensures we handle the PDF safely.

---

### Summary
By developing `metadata_module.py`, we have created a modular, evidence-safe extraction engine:
* We rely on **ExifRead** to handle the complexities of image EXIF tags.
* We rely on **PyMuPDF** to quickly parse PDF document properties. 
* Our script acts as a router—identifying the file type, using the correct tool for the job, and returning the gathered forensic intelligence in a clean, unified format.
