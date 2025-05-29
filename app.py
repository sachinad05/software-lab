from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Automatically create uploads folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected for upload."}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file
        file.save(file_path)
        return jsonify({"status": "success", "message": "File uploaded successfully."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Upload failed: {str(e)}"}), 500

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify({"status": "success", "files": files})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Could not list files: {str(e)}"}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Download failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)

