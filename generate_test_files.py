import os

def create_dummy_auth_log(output_path):
    log_content = """Feb 25 10:15:02 server sshd[1234]: Accepted publickey for user admin from 192.168.1.100 port 54321 ssh2
Feb 25 10:17:15 server sudo: admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/ls
Feb 25 10:20:01 server sshd[4321]: Failed password for invalid user root from 203.0.113.45 port 12345 ssh2
Feb 25 10:20:05 server sshd[4322]: Failed password for invalid user admin from 203.0.113.45 port 12346 ssh2
Feb 25 10:20:09 server sshd[4323]: Failed password for invalid user test from 203.0.113.45 port 12347 ssh2
Feb 25 10:20:13 server sshd[4324]: Failed password for invalid user guest from 203.0.113.45 port 12348 ssh2
Feb 25 10:20:17 server sshd[4325]: Failed password for invalid user user from 203.0.113.45 port 12349 ssh2
Feb 25 10:25:00 server cron[5678]: (root) CMD ( /usr/local/bin/backup.sh)
"""
    with open(output_path, "w") as f:
        f.write(log_content)
    print(f"Created dummy log: {output_path}")

def create_dummy_raw_file(output_path):
    # Dummy raw binary space
    random_data_1 = os.urandom(1024)
    random_data_2 = os.urandom(1024)
    random_data_3 = os.urandom(1024)

    # Valid JPEG header and footer with some dummy data inside
    jpeg_data = b'\xff\xd8\xff' + b'This is a fake JPEG file for testing carving.' + b'\xff\xd9'
    
    # Valid PDF header and footer with some dummy data inside
    pdf_data = b'%PDF' + b'-1.7\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n' + b'%%EOF'

    # Combine them into a single raw file
    raw_content = random_data_1 + jpeg_data + random_data_2 + pdf_data + random_data_3

    with open(output_path, "wb") as f:
        f.write(raw_content)
    print(f"Created dummy raw file: {output_path}")

if __name__ == "__main__":
    os.makedirs("test_files", exist_ok=True)
    create_dummy_auth_log("test_files/sample_auth.log")
    create_dummy_raw_file("test_files/sample_raw.bin")
