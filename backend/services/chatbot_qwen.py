import requests
import json

API_KEY = "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"

def get_qwen_response(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # Optional headers:
        # "HTTP-Referer": "http://localhost:5000",
        # "X-Title": "My AI Chatbot",
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
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Sorry, I'm having trouble responding right now."

    except Exception as e:
        print(f"Exception when calling Qwen: {e}")
        return "Something went wrong while trying to get a response."
