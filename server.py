"""
Combined server for Store-Counter application.
This script serves both the React frontend and Python backend API.
Uses PyTorch for advanced people detection and tracking.
"""
import os
import sys
from flask import Flask, send_from_directory, request, jsonify
import subprocess
from flask_cors import CORS

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import backend Blueprint
from backend.app import backend_app  # Changed to match the new name

# Create the main application
app = Flask(__name__, static_folder='frontend/build')
CORS(app)  # Add CORS handling here

# Mount the backend API at /api
app.register_blueprint(backend_app, url_prefix='/api')

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Determine port based on environment (default to 8080 for Docker)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)