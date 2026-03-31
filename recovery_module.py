"""
File Recovery (Carving) Module

This module implements basic header/footer carving algorithms to recover
JPEGs and PDFs from raw binary streams or dummy files using magic numbers.
"""

import os

def carve_files(raw_file_path, output_dir):
    """
    Extracts JPEGs and PDFs from a raw binary file using hex signature patterns.

    Args:
        raw_file_path (str): Path to the single binary file to carve from.
        output_dir (str): Directory where the recovered files will be saved.

    Returns:
        list: Names of the successfully recovered files or error messages.
    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            return [f"Failed to create output directory: {str(e)}"]
            
    recovered_files = []
    
    # Magic numbers (Signatures)
    jpeg_header = b'\xff\xd8\xff'
    jpeg_footer = b'\xff\xd9'
    
    pdf_header = b'%PDF'
    pdf_footer = b'%%EOF'
    
    try:
        with open(raw_file_path, 'rb') as f:
            data = f.read()
            
            # Carve for JPEGs
            start_idx = 0
            jpeg_count = 0
            while True:
                start = data.find(jpeg_header, start_idx)
                if start == -1:
                    break
                    
                end = data.find(jpeg_footer, start)
                if end != -1:
                    end += 2 # Include the length of the footer (\xff\xd9 is 2 bytes)
                    jpeg_count += 1
                    recover_path = os.path.join(output_dir, f"recovered_{jpeg_count}.jpeg")
                    with open(recover_path, 'wb') as out_f:
                        out_f.write(data[start:end])
                    recovered_files.append(recover_path)
                    start_idx = end
                else:
                    # If no footer found, step over header to continue search
                    start_idx = start + len(jpeg_header)
            
            # Carve for PDFs
            start_idx = 0
            pdf_count = 0
            while True:
                start = data.find(pdf_header, start_idx)
                if start == -1:
                    break
                    
                end = data.find(pdf_footer, start)
                if end != -1:
                    end += 5 # Include the length of the footer (%%EOF is 5 bytes)
                    pdf_count += 1
                    recover_path = os.path.join(output_dir, f"recovered_{pdf_count}.pdf")
                    with open(recover_path, 'wb') as out_f:
                        out_f.write(data[start:end])
                    recovered_files.append(recover_path)
                    start_idx = end
                else:
                    # If no footer found, step over header to continue search
                    start_idx = start + len(pdf_header)
                    
    except Exception as e:
        return [f"Error carving files: {str(e)}"]
        
    return recovered_files
