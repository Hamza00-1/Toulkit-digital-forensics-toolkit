"""
Activity Tracker Module

This module records tool usage and file processing events into a MySQL database
to power the Home Dashboard's historical statistics and graphs.
"""

import mysql.connector
from datetime import datetime
import traceback
import sys

# Database Configuration (MAMP Defaults)
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'aegis_forensics'
}

def _get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Database connection failed. Ensure MAMP is running and 'aegis_forensics' DB exists: {e}", file=sys.stderr)
        return None

def log_activity(module_name, file_processed=None, status="Success"):
    """
    Logs an activity event to the MySQL database.
    
    Args:
        module_name (str): The name of the module used (e.g., 'Metadata', 'Hasher').
        file_processed (str, optional): The path or name of the file processed.
        status (str): The status of the operation ('Success', 'Error', 'No Findings', etc).
    """
    conn = _get_connection()
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        query = "INSERT INTO activity_logs (timestamp, module, file, status) VALUES (%s, %s, %s, %s)"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = file_processed if file_processed else "N/A"
        
        cursor.execute(query, (timestamp, module_name, file_path, status))
        conn.commit()
    except Exception as e:
        print(f"Failed to log activity to MySQL: {e}", file=sys.stderr)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_dashboard_stats():
    """
    Aggregates data from the database for the dashboard.
    
    Returns:
        dict: A dictionary of statistics: total_files, anomalies, module_counts.
    """
    stats = {
        "total_files": 0,
        "anomalies": 0,
        "module_counts": {},
        "raw_events": []
    }
    
    conn = _get_connection()
    if not conn:
        return stats
        
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get raw events
        cursor.execute("SELECT timestamp, module, file, status FROM activity_logs ORDER BY timestamp ASC")
        events = cursor.fetchall()
        
        if not events:
            return stats
            
        # Convert datetime objects to string format to main compatibility with existing UI
        for event in events:
            if isinstance(event['timestamp'], datetime):
                event['timestamp'] = event['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                
        stats["raw_events"] = events
        
        # Calculate stats
        cursor.execute("SELECT COUNT(DISTINCT file) as count FROM activity_logs WHERE file != 'N/A' AND file != 'Raw String Input'")
        res = cursor.fetchone()
        stats["total_files"] = res['count'] if res else 0
        
        cursor.execute("SELECT COUNT(*) as count FROM activity_logs WHERE status IN ('Danger', 'Anomalies Found')")
        res = cursor.fetchone()
        stats["anomalies"] = res['count'] if res else 0
        
        cursor.execute("SELECT module, COUNT(*) as count FROM activity_logs GROUP BY module")
        for row in cursor.fetchall():
            stats["module_counts"][row['module']] = row['count']
            
    except Exception as e:
        print(f"Failed to retrieve stats from MySQL: {e}", file=sys.stderr)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
    return stats
