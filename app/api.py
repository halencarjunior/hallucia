from flask import Flask, request, jsonify
from app.util import validate_packages, filter_only_invalid
from app.validator import process_directory 
import os

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    if not data or "code" not in data or "lang" not in data:
        return jsonify({"error": "Missing 'code' or 'lang' in request body."}), 400

    lang = data["lang"].lower()
    if lang not in ["python", "javascript", "js"]:
        return jsonify({"error": "Unsupported language. Use 'python' or 'javascript'."}), 400

    try:
        result = validate_packages(data["code"], lang)
        if data.get("only_invalid"):
            result = filter_only_invalid([result])[0:1] or []
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/validate-path", methods=["POST"])
def validate_path():
    data = request.get_json()
    if not data or "path" not in data:
        return jsonify({"error": "Missing 'path' in request body."}), 400

    scan_path = data["path"]
    if not os.path.exists(scan_path) or not os.path.isdir(scan_path):
        return jsonify({"error": f"Path '{scan_path}' does not exist or is not a directory."}), 400

    try:
        results = process_directory(scan_path)
        if data.get("only_invalid"):
            results = filter_only_invalid(results)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
