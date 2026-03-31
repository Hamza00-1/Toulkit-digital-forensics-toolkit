"""
Message Decoding Module

This module provides functions to quickly decode common encodings
often found during forensic investigations: Base64, Hexadecimal, and Binary.
"""

import base64
import binascii

def decode_message(encoded_str, encoding_type):
    """
    Decodes a string based on the specified encoding type.
    
    Args:
        encoded_str (str): The encoded message.
        encoding_type (str): The type of encoding ('Base64', 'Hex', 'Binary').
        
    Returns:
        str: The decoded ASCII text, or an error message if parsing fails.
    """
    if not encoded_str or encoded_str.strip() == "":
        return "Error: Input string is empty."
        
    encoded_str = encoded_str.strip()
    
    try:
        if encoding_type == 'Base64':
            # Add padding if missing
            pad_len = len(encoded_str) % 4
            if pad_len:
                encoded_str += "=" * (4 - pad_len)
            decoded_bytes = base64.b64decode(encoded_str)
            return decoded_bytes.decode('utf-8', errors='replace')
            
        elif encoding_type == 'Hex':
            # Remove common hex prefixes and spaces
            clean_str = encoded_str.replace("0x", "").replace(" ", "").replace("\\x", "")
            decoded_bytes = binascii.unhexlify(clean_str)
            return decoded_bytes.decode('utf-8', errors='replace')
            
        elif encoding_type == 'Binary':
            # Remove spaces and process 8-bit chunks
            clean_str = encoded_str.replace(" ", "")
            if len(clean_str) % 8 != 0:
                return "Error: Binary string length must be a multiple of 8."
                
            chars = [chr(int(clean_str[i:i+8], 2)) for i in range(0, len(clean_str), 8)]
            return "".join(chars)
            
        else:
            return f"Error: Unsupported encoding type '{encoding_type}'"
            
    except Exception as e:
        return f"Error decoding {encoding_type}: {str(e)}"
