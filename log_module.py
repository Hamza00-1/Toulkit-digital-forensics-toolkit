"""
Log Analysis Module

This module provides functions to parse standard Auth style logs (e.g. Linux auth.log)
using regular expressions and returning the structured data as a pandas DataFrame.
It also flags simple anomalies such as multiple failed login attempts.
"""

import pandas as pd
import re

def parse_auth_log(file_path):
    """
    Parses an auth log file and identifies simple anomalies.

    Args:
        file_path (str): Path to the log file.

    Returns:
        tuple: (pandas.DataFrame, list) containing the parsed log data and a list of flagged anomalies.
    """
    log_data = []
    
    # Standard syslog format: Mon DD HH:MM:SS Hostname Process: Message
    log_pattern = re.compile(
        r'^(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<process>[^:]+):\s+(?P<message>.*)$'
    )
    
    # Common SSH failed login pattern
    failed_login_pattern = re.compile(r'Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+) port \d+ ssh2')
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = log_pattern.match(line)
                if match:
                    entry = match.groupdict()
                    
                    # Check for failed SSH login attempts
                    failed_match = failed_login_pattern.search(entry['message'])
                    if failed_match:
                        entry['event_type'] = 'Failed Login'
                        entry['target_user'] = failed_match.group('user')
                        entry['source_ip'] = failed_match.group('ip')
                    else:
                        entry['event_type'] = 'Other'
                        entry['target_user'] = None
                        entry['source_ip'] = None
                        
                    log_data.append(entry)
    except Exception as e:
        return pd.DataFrame(), [f"Error reading log file: {str(e)}"]

    if not log_data:
        return pd.DataFrame(), ["No valid log entries found or file is empty."]
        
    df = pd.DataFrame(log_data)
    
    # Flag Anomalies (e.g., more than 3 failed attempts from a single IP)
    anomalies = []
    failed_attempts = df[df['event_type'] == 'Failed Login']
    
    if not failed_attempts.empty:
        ip_counts = failed_attempts['source_ip'].value_counts()
        suspicious_ips = ip_counts[ip_counts > 3]
        
        for ip, count in suspicious_ips.items():
            anomalies.append(f"Suspicious Activity: IP Address {ip} had {count} failed login attempts.")
            
    return df, anomalies
