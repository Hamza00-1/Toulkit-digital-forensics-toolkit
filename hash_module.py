"""
Hash Analysis Module

This module provides functions to compute cryptographic hashes of files
and to query the VirusTotal public API to check for malicious signatures.
"""

import hashlib
import requests
import os

def compute_hashes(file_path):
    """
    Computes MD5, SHA-1, and SHA-256 hashes for a given file.
    
    Args:
        file_path (str): The path to the file.
        
    Returns:
        dict: A dictionary containing the computed hashes or an error message.
    """
    if not os.path.isfile(file_path):
        return {"Error": "File does not exist or is not a valid file path."}

    hashes = {
        'MD5': hashlib.md5(),
        'SHA-1': hashlib.sha1(),
        'SHA-256': hashlib.sha256()
    }
    
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                for h in hashes.values():
                    h.update(chunk)
    except Exception as e:
        return {"Error": f"Failed to read file: {str(e)}"}
        
    return {name: h.hexdigest() for name, h in hashes.items()}


def check_virustotal(sha256_hash, api_key):
    """
    Queries the VirusTotal API v3 to check if a file hash is flagged.
    
    Args:
        sha256_hash (str): The SHA-256 hash of the file.
        api_key (str): The user's VirusTotal API key.
        
    Returns:
        dict: A dictionary containing the VT analysis results or an error message.
    """
    if not api_key or api_key.strip() == "":
        return {"Error": "A valid VirusTotal API key is required."}

    url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)
            undetected = stats.get('undetected', 0)
            
            return {
                "Status": "Success",
                "Malicious": malicious,
                "Suspicious": suspicious,
                "Undetected": undetected,
                "Verdict": "DANGER" if malicious > 0 else "CLEAN"
            }
        elif response.status_code == 404:
            return {"Status": "Not Found", "Info": "This hash has never been seen by VirusTotal."}
        elif response.status_code == 401:
            return {"Error": "Unauthorized. Invalid API key."}
        elif response.status_code == 429:
            return {"Error": "Rate limit exceeded. Too many requests."}
        else:
            return {"Error": f"API returned status code: {response.status_code}"}
            
    except Exception as e:
        return {"Error": f"Connection failed: {str(e)}"}
