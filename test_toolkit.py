import unittest
import os
import shutil
import tempfile
import pandas as pd
from unittest.mock import patch, MagicMock

# Import the toolkit modules
from metadata_module import extract_metadata, _extract_image_metadata, _extract_pdf_metadata
from log_module import parse_auth_log
from recovery_module import carve_files

class TestMetadataModule(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.dummy_jpg = os.path.join(self.test_dir, 'dummy.jpg')
        self.dummy_pdf = os.path.join(self.test_dir, 'dummy.pdf')
        self.dummy_txt = os.path.join(self.test_dir, 'dummy.txt')
        
        # Create dummy files
        with open(self.dummy_jpg, 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01')
        with open(self.dummy_pdf, 'wb') as f:
            f.write(b'%PDF-1.4\n%EOF')
        with open(self.dummy_txt, 'w') as f:
            f.write('Not an image or pdf')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_extract_invalid_file(self):
        res = extract_metadata(os.path.join(self.test_dir, 'nonexistent.jpg'))
        self.assertIn('Error', res)
        self.assertEqual(res['Error'], "File does not exist or is not a valid file path.")

    def test_extract_unsupported_ext(self):
        res = extract_metadata(self.dummy_txt)
        self.assertIn('Error', res)
        self.assertTrue(res['Error'].startswith("Unsupported file extension: txt."))

    @patch('metadata_module.exifread.process_file')
    def test_extract_image_metadata(self, mock_process_file):
        # Mocking EXIF metadata returned by exifread
        mock_process_file.return_value = {
            'Image Model': 'TestCamera',
            'EXIF DateTimeOriginal': '2023:01:01 12:00:00'
        }
        res = extract_metadata(self.dummy_jpg)
        self.assertNotIn('Error', res)
        self.assertEqual(res.get('Image Model'), 'TestCamera')
        self.assertEqual(res.get('EXIF DateTimeOriginal'), '2023:01:01 12:00:00')

    @patch('metadata_module.fitz.open')
    def test_extract_pdf_metadata(self, mock_fitz_open):
        # Mocking PDF metadata returned by PyMuPDF (fitz)
        mock_doc = MagicMock()
        mock_doc.metadata = {
            'title': 'Secret Document',
            'author': 'Agent 007'
        }
        mock_fitz_open.return_value = mock_doc
        
        res = extract_metadata(self.dummy_pdf)
        self.assertNotIn('Error', res)
        self.assertEqual(res.get('title'), 'Secret Document')
        self.assertEqual(res.get('author'), 'Agent 007')
        mock_doc.close.assert_called_once()

class TestLogModule(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, 'auth.log')
        
        # Create a dummy log file with mixed content
        log_content = """Feb 25 10:00:00 server sshd[1234]: Accepted publickey for admin from 192.168.1.100 port 54321 ssh2
Feb 25 10:05:00 server sshd[1235]: Failed password for invalid user root from 10.0.0.5 port 22 ssh2
Feb 25 10:05:05 server sshd[1236]: Failed password for invalid user root from 10.0.0.5 port 22 ssh2
Feb 25 10:05:10 server sshd[1237]: Failed password for invalid user root from 10.0.0.5 port 22 ssh2
Feb 25 10:05:15 server sshd[1238]: Failed password for invalid user root from 10.0.0.5 port 22 ssh2
Feb 25 10:10:00 server sudo[2000]: admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/bash
Invalid log line that should be ignored by the regex
"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_auth_log(self):
        df, anomalies = parse_auth_log(self.log_file)
        
        # We expect 6 valid log entries
        self.assertEqual(len(df), 6)
        
        # Check that 'Failed Login' was assigned correctly
        failed_logins = df[df['event_type'] == 'Failed Login']
        self.assertEqual(len(failed_logins), 4)
        
        # Check that the anomaly (IP > 3 failed attempts) was caught
        self.assertEqual(len(anomalies), 1)
        self.assertIn("10.0.0.5", anomalies[0])
        self.assertIn("4", anomalies[0]) # 4 failed attempts

class TestRecoveryModule(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.raw_file = os.path.join(self.test_dir, 'memory_dump.bin')
        self.output_dir = os.path.join(self.test_dir, 'recovered_files')
        
        # Prepare mock binary stream
        jpeg_header = b'\xff\xd8\xff'
        jpeg_footer = b'\xff\xd9'
        pdf_header = b'%PDF'
        pdf_footer = b'%%EOF'
        
        junk_data = b'\x00\x01\x02' * 50
        
        # Stream: JUNK + JPEG1 + JUNK + PDF1 + JUNK + JPEG2
        binary_content = (
            junk_data + 
            jpeg_header + b'image1DATA' + jpeg_footer +
            junk_data +
            pdf_header + b'pdf1DATA' + pdf_footer +
            junk_data +
            jpeg_header + b'image2DATA' + jpeg_footer +
            junk_data
        )
        
        with open(self.raw_file, 'wb') as f:
            f.write(binary_content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_carve_files(self):
        recovered = carve_files(self.raw_file, self.output_dir)
        
        # We expect 3 files to be recovered: 2 JPEGs, 1 PDF
        self.assertEqual(len(recovered), 3)
        
        # Verify extension presence
        jpeg_count = sum(1 for f in recovered if f.endswith('.jpeg'))
        pdf_count = sum(1 for f in recovered if f.endswith('.pdf'))
        
        self.assertEqual(jpeg_count, 2)
        self.assertEqual(pdf_count, 1)

        # Check content of one of the recovered files
        for fpath in recovered:
            self.assertTrue(os.path.exists(fpath))
            with open(fpath, 'rb') as f:
                content = f.read()
                if fpath.endswith('.pdf'):
                    self.assertTrue(content.startswith(b'%PDF'))
                    self.assertTrue(content.endswith(b'%%EOF'))
                elif fpath.endswith('.jpeg'):
                    self.assertTrue(content.startswith(b'\xff\xd8\xff'))
                    self.assertTrue(content.endswith(b'\xff\xd9'))

if __name__ == '__main__':
    unittest.main()
