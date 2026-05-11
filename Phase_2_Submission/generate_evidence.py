import os
from PIL import Image, ExifTags

def build_phase_two_evidence():
    evidence_dir = os.path.join(os.path.dirname(__file__), "test_evidence")
    if not os.path.exists(evidence_dir):
        os.makedirs(evidence_dir)
        
    # ==========================================
    # 1. GENERATE A DUMMY SYSLOG FOR LOG PARSER
    # ==========================================
    log_path = os.path.join(evidence_dir, "server_auth.log")
    
    anomalous_logs = [
        "Mar 31 15:42:01 server1 sshd[1024]: Accepted publickey for admin from 192.168.1.50 port 50212 ssh2\n",
        "Mar 31 16:10:22 server1 sshd[1050]: Failed password for root from 185.15.22.90 port 44342 ssh2\n",
        "Mar 31 16:10:24 server1 sshd[1050]: Failed password for root from 185.15.22.90 port 44342 ssh2\n",
        "Mar 31 16:10:25 server1 sshd[1050]: Failed password for root from 185.15.22.90 port 44342 ssh2\n",
        "Mar 31 16:10:27 server1 sshd[1050]: Failed password for root from 185.15.22.90 port 44342 ssh2\n", # Brute force trigger!
        "Mar 31 16:11:00 server1 sshd[1050]: Accepted password for root from 185.15.22.90 port 44342 ssh2\n", # Ah oh, they got in
        "Mar 31 16:15:22 server1 sudo: root : TTY=pts/0 ; PWD=/root ; USER=root ; COMMAND=/bin/bash\n"
    ]
    
    with open(log_path, "w") as f:
        f.writelines(anomalous_logs)
    print(f"[+] Generated forensic Syslog payload: {log_path}")

    # ==========================================
    # 2. GENERATE A BINARY FILE FOR HEX CARVER
    # ==========================================
    # The carver strips valid JPEGs out of corrupted hard drive memory/binary files.
    # We will make a tiny jpeg, then pack it into a text file surrounded by garbage.
    
    tiny_img_path = os.path.join(evidence_dir, "temp.jpg")
    img = Image.new('RGB', (100, 100), color=(255, 0, 0))
    img.save(tiny_img_path)
    
    # Read the valid JPEG bytes (FF D8 FF E0 ... FF D9)
    with open(tiny_img_path, "rb") as f:
        valid_jpeg_bytes = f.read()
        
    os.remove(tiny_img_path) # delete tmp file
    
    # Create the corrupted binary evidence file
    corrupt_bin_path = os.path.join(evidence_dir, "corrupted_hdd_sector.bin")
    
    with open(corrupt_bin_path, "wb") as f:
        # Write 500 bytes of garbage text/binary
        f.write(b"GARBAGE_DATA_FROM_PREVIOUS_PROGRAM_" * 20)
        # Inject the "deleted" valid image bytes in the middle of the sector
        f.write(valid_jpeg_bytes)
        # Write more garbage data
        f.write(b"MORE_CORRUPTED_SECTOR_DATA_THAT_CONFUSES_WINDOWS" * 20)
        
    print(f"[+] Generated corrupted binary stream for Carver: {corrupt_bin_path}")

if __name__ == "__main__":
    build_phase_two_evidence()
