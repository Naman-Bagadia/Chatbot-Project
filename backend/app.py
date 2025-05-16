from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import base64
import time

app = Flask(__name__, static_folder='../Frontend')
CORS(app)

# Qwen API key and chat function
QWEN_API_KEY = "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"

def get_qwen_response(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "qwen/qwen3-4b:free",
        "messages": [
            {"role": "system", "content": "You are a supportive and emotionally intelligent mental health assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Sorry, I'm having trouble responding right now."
    except Exception as e:
        print(f"Exception when calling Qwen: {e}")
        return "Something went wrong while trying to get a response."

# AssemblyAI API key and transcription functions
ASSEMBLYAI_API_KEY = "7655224606ff43b5bd80daac44faeaa1"
ASSEMBLYAI_UPLOAD_URL = "https://api.assemblyai.com/v2/upload"
ASSEMBLYAI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"

headers_assemblyai = {
    "authorization": ASSEMBLYAI_API_KEY,
    "content-type": "application/json"
}

def upload_audio(audio_bytes):
    upload_headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "transfer-encoding": "chunked"
    }
    response = requests.post(ASSEMBLYAI_UPLOAD_URL, headers=upload_headers, data=audio_bytes)
    if response.status_code == 200:
        return response.json()['upload_url']
    else:
        print(f"Upload failed: {response.text}")
        return None

def request_transcription(upload_url):
    json_data = {
        "audio_url": upload_url,
        "auto_chapters": False
    }
    response = requests.post(ASSEMBLYAI_TRANSCRIPT_URL, json=json_data, headers=headers_assemblyai)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Transcription request failed: {response.text}")
        return None

def get_transcription_result(transcript_id):
    url = f"{ASSEMBLYAI_TRANSCRIPT_URL}/{transcript_id}"
    while True:
        response = requests.get(url, headers=headers_assemblyai)
        if response.status_code != 200:
            print(f"Error fetching transcription: {response.text}")
            return None
        status = response.json()['status']
        if status == 'completed':
            return response.json()['text']
        elif status == 'error':
            print(f"Transcription error: {response.json()['error']}")
            return None
        else:
            time.sleep(2)

# Routes
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({"reply": "No message received."})
    reply = get_qwen_response(message)
    return jsonify({"reply": reply})

@app.route('/voice', methods=['POST'])
def voice():
    data = request.json
    audio_b64 = data.get('audio')
    if not audio_b64:
        return jsonify({"transcript": None, "error": "No audio data received."})

    try:
        audio_bytes = base64.b64decode(audio_b64.split(',')[1])  # Remove data URL prefix
    except Exception as e:
        return jsonify({"transcript": None, "error": "Invalid audio data."})

    upload_url = upload_audio(audio_bytes)
    if not upload_url:
        return jsonify({"transcript": None, "error": "Audio upload failed."})

    transcript_id = request_transcription(upload_url)
    if not transcript_id:
        return jsonify({"transcript": None, "error": "Transcription request failed."})

    transcript_text = get_transcription_result(transcript_id)
    if not transcript_text:
        return jsonify({"transcript": None, "error": "Transcription failed."})

    # Get bot response to transcript text
    bot_reply = get_qwen_response(transcript_text)

    return jsonify({"transcript": transcript_text, "reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
