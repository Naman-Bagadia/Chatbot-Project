# backend/routes/chat.py

from flask import Blueprint, request, jsonify
from backend.services.chatbot_qwen import get_qwen_response

chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    reply = get_qwen_response(user_message)
    return jsonify({"reply": reply})
