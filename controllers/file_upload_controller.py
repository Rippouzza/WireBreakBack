# controllers/file_upload_controller.py

from flask import request, jsonify
from services.file_upload_service import handle_file_upload

def upload_file():
    """Controller to handle the file upload request."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Call the service to handle the file processing
        success_count, failure_count = handle_file_upload(file)
        
        return jsonify({
            "message": "File processed successfully",
            "success_count": success_count,
            "failure_count": failure_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
