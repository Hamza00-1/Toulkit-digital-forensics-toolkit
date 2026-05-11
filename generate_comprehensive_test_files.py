import os
import shutil
import fitz
import base64

# 1. Clear the directory
if os.path.exists("test_files"):
    shutil.rmtree("test_files")
os.makedirs("test_files", exist_ok=True)

# 2. Log Analyzer Test File
log_content = """Feb 25 10:15:02 server sshd[1234]: Accepted publickey for user admin from 192.168.1.100 port 54321 ssh2
Feb 25 10:17:15 server sudo: admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/ls
Feb 25 10:20:01 server sshd[4321]: Failed password for invalid user root from 203.0.113.45 port 12345 ssh2
Feb 25 10:20:05 server sshd[4322]: Failed password for invalid user admin from 203.0.113.45 port 12346 ssh2
Feb 25 10:20:09 server sshd[4323]: Failed password for invalid user test from 203.0.113.45 port 12347 ssh2
Feb 25 10:20:13 server sshd[4324]: Failed password for invalid user guest from 203.0.113.45 port 12348 ssh2
Feb 25 10:20:17 server sshd[4325]: Failed password for invalid user user from 203.0.113.45 port 12349 ssh2
Feb 25 10:25:00 server cron[5678]: (root) CMD ( /usr/local/bin/backup.sh)
"""
with open("test_files/1_log_bruteforce.log", "w") as f:
    f.write(log_content)

# 3. File Carver Test File
raw_file = b'\x00' * 512 # random junk 
jpeg_data = b'\xff\xd8\xff' + b'FAKE_JPEG_IMAGE_DATA_FOR_CARVING' + b'\xff\xd9'
raw_file += jpeg_data
raw_file += b'\xab\xcd\xef' * 100 # junk
pdf_data = b'%PDF' + b'-1.7\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n' + b'%%EOF'
raw_file += pdf_data
raw_file += b'\xff' * 256 # junk
with open("test_files/2_carver_raw_stream.bin", "wb") as f:
    f.write(raw_file)

# 4. Hash & VirusTotal Test File (EICAR)
eicar = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
with open("test_files/3_hash_vt_malware.txt", "w") as f:
    f.write(eicar)

# 5. String Decoder Test File
secret_msg = "SuperSecretMalwarePayload_ConnectToIP:192.168.1.100"
b64_msg = base64.b64encode(secret_msg.encode('utf-8')).decode('utf-8')
with open("test_files/4_decoder_payload.b64", "w") as f:
    f.write(b64_msg)

# 6. Metadata Extractor Test File (PDF with metadata)
doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), "This is a dummy PDF file to test the Metadata Extractor!")
metadata = {
    "title": "Top Secret Investigation Report",
    "author": "Rogue Insider Agent",
    "subject": "Confidential Exfiltration Plan",
    "creator": "Malicious PDF Builder v1.0",
    "keywords": "confidential, breach, exploit, payload"
}
doc.set_metadata(metadata)
doc.save("test_files/5_metadata_suspicious.pdf")
doc.close()

print("All test files generated successfully!")
