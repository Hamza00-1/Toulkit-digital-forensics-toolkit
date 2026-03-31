import os
import fitz  # PyMuPDF
from PIL import Image

def build_test_evidence():
    evidence_dir = os.path.join(os.path.dirname(__file__), "test_evidence")
    if not os.path.exists(evidence_dir):
        os.makedirs(evidence_dir)
        
    # 1. GENERATE A DUMMY PDF WITH XMP METADATA
    pdf_path = os.path.join(evidence_dir, "suspicious_invoice.pdf")
    doc = fitz.open()  # new empty PDF
    page = doc.new_page()  # new page
    
    # Write some text on the page
    p = fitz.Point(50, 72)
    page.insert_text(p, "INVOICE #492019", fontsize=20, fontname="helv", color=(1, 0, 0))
    p = fitz.Point(50, 100)
    page.insert_text(p, "PAYMENT DUE: 50,000 USD via Bitcoin", fontsize=12, fontname="helv")
    
    # Inject juicy metadata for the professor to see!
    doc.set_metadata({
        "author": "Hackerman (John Doe)",
        "creator": "Adobe Illustrator CC 22.0 (Windows)",
        "title": "Wire Transfer Invoice",
        "subject": "Phishing Campaign Targets",
        "keywords": "urgent, payment, wire, confidential",
        "creationDate": "D:20260302115000Z",
    })
    
    doc.save(pdf_path)
    doc.close()
    print(f"[+] Generated forensic PDF payload: {pdf_path}")
    
    # 2. GENERATE A DUMMY IMAGE WITH EXIF DATA
    from PIL import ExifTags
    img_path = os.path.join(evidence_dir, "stolen_blueprint.jpg")
    img = Image.new('RGB', (800, 600), color=(73, 109, 137))
    
    # Inject fake EXIF metadata for the Extractor
    exif = img.getexif()
    exif[ExifTags.Base.Make] = "Rogue Smartphone Mk2"
    exif[ExifTags.Base.Model] = "HackerPhone Pro"
    exif[ExifTags.Base.Software] = "Kali Linux Image Editor"
    exif[ExifTags.Base.DateTime] = "2026:03:02 23:59:00"
    
    img.save(img_path, exif=exif)
    print(f"[+] Generated forensic Image payload: {img_path}")
    
if __name__ == "__main__":
    build_test_evidence()
