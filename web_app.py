"""
Aegis Forensics Suite - Web Application Backend
Runs the forensic toolkit entirely within a web browser using Flask.
"""

from flask import Flask, render_template, request, jsonify, url_for
import os
import json
from werkzeug.utils import secure_filename

# Import Core Forensic Modules
from metadata_module import extract_metadata
from log_module import parse_auth_log
from hash_module import compute_hashes, check_virustotal
from decoding_module import decode_message
import activity_tracker

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

@app.context_processor
def inject_global_data():
    """Injects MySQL database stats and available server workspace files into all templates."""
    stats = activity_tracker.get_dashboard_stats()
    
    # Get all successfully extracted unique target files from the MySQL DB
    processed_targets = []
    for event in stats.get('raw_events', []):
        if event['file'] != 'N/A' and event['file'] != 'Raw String Input':
            full_path = event['file']
            basename = os.path.basename(full_path)
            if basename not in processed_targets:
                processed_targets.append(basename)
                
    # Get all raw files waiting in the server sandbox
    workspace_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        workspace_files = os.listdir(app.config['UPLOAD_FOLDER'])
        
    return dict(
        db_stats=stats,
        workspace_files=workspace_files,
        processed_targets=processed_targets
    )

@app.route('/')
def dashboard():
    """Renders the main Executive Dashboard."""
    stats = activity_tracker.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats, page="dashboard")

@app.route('/metadata', methods=['GET', 'POST'])
def metadata_view():
    """Handles EXIF and Document Metadata extraction."""
    result = None
    if request.method == 'POST':
        server_file = request.form.get('server_file')
        
        filepath = None
        filename = None
        
        if server_file and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], server_file)):
            filename = server_file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        elif 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
        if filepath:
            result = extract_metadata(filepath)
            status = "Error" if "Error" in result else "Success"
            activity_tracker.log_activity("Web: Metadata", filename, status)
        else:
            result = {"Error": "No file uploaded or selected from workspace"}
                
    return render_template('metadata.html', result=json.dumps(result, indent=4) if result else None, page="metadata")

@app.route('/hasher', methods=['GET', 'POST'])
def hasher_view():
    """Handles File Hashing and VirusTotal querying."""
    result = None
    if request.method == 'POST':
        server_file = request.form.get('server_file')
        vt_key = request.form.get('vt_key', '')
        
        filepath = None
        filename = None
        
        if server_file and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], server_file)):
            filename = server_file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        elif 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
        if filepath:
            hashes = compute_hashes(filepath)
            result = {"Hashes": hashes}
            status = "Success"
            
            if vt_key and "Error" not in hashes:
                vt_result = check_virustotal(hashes.get("SHA-256"), vt_key)
                result["VirusTotal"] = vt_result
                if vt_result.get("Verdict") == "DANGER":
                    status = "Danger"
                    
            activity_tracker.log_activity("Web: Hasher", filename, status)
        else:
            result = {"Error": "No file uploaded or selected from workspace"}

    return render_template('hasher.html', result=result, page="hasher")

@app.route('/decoder', methods=['GET', 'POST'])
def decoder_view():
    """Handles string decoding."""
    result = None
    if request.method == 'POST':
        raw_text = request.form.get('raw_text', '')
        enc_type = request.form.get('enc_type', 'Base64')
        
        if raw_text:
            result = decode_message(raw_text, enc_type)
            status = "Error" if result.startswith("Error") else "Success"
            activity_tracker.log_activity(f"Web: Decoder ({enc_type})", "Raw String", status)
            
    return render_template('decoder.html', result=result, page="decoder")

@app.route('/logs', methods=['GET', 'POST'])
def logs_view():
    """Handles Syslog analysis."""
    result = None
    if request.method == 'POST':
        server_file = request.form.get('server_file')
        
        filepath = None
        filename = None
        
        if server_file and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], server_file)):
            filename = server_file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        elif 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
        if filepath:
            df, anomalies = parse_auth_log(filepath)
            result = {
                "total_events": len(df),
                "anomalies": anomalies,
                "preview": df.head(15).to_html(classes="min-w-full divide-y divide-gray-700") if not df.empty else ""
            }
            status = "Anomalies Found" if anomalies else "Success"
            activity_tracker.log_activity("Web: Logs", filename, status)
        else:
            result = {"Error": "No file uploaded or selected from workspace"}
                
    return render_template('logs.html', result=result, page="logs")


if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)
    
    # Run the Flask app on localhost:5000
    print("[*] Starting Aegis Web Application...")
    print("[*] Access via http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
