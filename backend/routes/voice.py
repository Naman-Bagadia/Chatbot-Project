from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from backend.services.transcribe import transcribe_audio

voice_bp = Blueprint('voice', __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@voice_bp.route('/transcribe', methods=['POST'])
def transcribe_voice():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    transcription = transcribe_audio(file_path)
    os.remove(file_path)  # optional cleanup

    return jsonify({"transcript": transcription})
