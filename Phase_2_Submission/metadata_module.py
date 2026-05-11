"""
Metadata Extraction Module

This module provides functions to extract hidden metadata from files,
specifically targeting images (using ExifRead) and PDFs (using PyMuPDF).
"""

import os
import exifread
import fitz  # PyMuPDF

def extract_metadata(file_path):
    """
    Extracts metadata from a given file based on its extension.

    Args:
        file_path (str): The path to the file to be analyzed.

    Returns:
        dict: A dictionary containing the extracted metadata, or an error message.
    """
    if not os.path.isfile(file_path):
        return {"Error": "File does not exist or is not a valid file path."}

    ext = file_path.lower().split('.')[-1]
    
    if ext in ['jpg', 'jpeg', 'png', 'tiff']:
        return _extract_image_metadata(file_path)
    elif ext == 'pdf':
        return _extract_pdf_metadata(file_path)
    else:
        return {"Error": f"Unsupported file extension: {ext}. Only Images and PDFs are supported."}

def _extract_image_metadata(file_path):
    """
    Helper function to extract EXIF data from images.

    Args:
        file_path (str): The path to the image file.

    Returns:
        dict: A dictionary containing the extracted EXIF data.
    """
    metadata = {}
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    metadata[tag] = str(tags[tag])
                    
        if not metadata:
            metadata["Info"] = "No EXIF metadata found in the image."
    except Exception as e:
        metadata["Error"] = f"Failed to extract image metadata: {str(e)}"
    
    return metadata

def _extract_pdf_metadata(file_path):
    """
    Helper function to extract document information from PDFs.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary containing the extracted PDF metadata.
    """
    metadata = {}
    try:
        doc = fitz.open(file_path)
        pdf_info = doc.metadata
        for key, value in pdf_info.items():
            if value:
                metadata[key] = value
                
        if not metadata:
            metadata["Info"] = "No metadata found in the PDF document."
    except Exception as e:
        metadata["Error"] = f"Failed to extract PDF metadata: {str(e)}"
    
    finally:
        if 'doc' in locals():
            doc.close()
            
    return metadata
