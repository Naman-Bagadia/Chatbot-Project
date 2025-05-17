
# serenAI — Your Emotion-Aware AI Companion

> "A chatbot that feels before it speaks."

**serenAI** is an AI-powered mental health companion that uses voice input, emotion detection, and intelligent LLM-based replies to create a personalized and empathetic support experience. Designed to support users emotionally, serenAI listens, analyzes your tone, and responds with emotional intelligence — all through a simple, elegant interface.

---

## 🔧 How It Works

1. **User speaks** through the web interface.
2. **Speech is recorded** and sent to the Python backend.
3. The audio is sent to **Hume AI’s SDK**, which returns emotional signals (like calm, joy, frustration, etc.).
4. The emotion is passed to an **LLM (Qwen 3 4B)** which generates a reply considering both your text and your emotional tone.
5. The chatbot **responds in text** — emotionally aligned with how you sound.

---

## 🧠 Models & Tools Used

| Purpose             | Model/Service   |
|---------------------|-----------------|
| Emotion Detection   | Hume AI SDK     |
| Text Generation     | Qwen 3 4B       |
| Speech Recognition  | Web Speech API  |
| Frontend Framework  | HTML + JS       |
| Backend Framework   | Flask (Python)  |

---

## 🗂️ Features

- Voice input with speech-to-text
- Emotion analysis from audio input
- Emotion-conditioned AI text responses
- Simple and clean web interface
- Fully local + private setup (no cloud speech recognition used)
- Easy to extend with journaling, affirmations, and mood tracking

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/serenAI.git
cd serenAI
```

### 2. Install dependencies

Make sure you have Python 3.9+ installed.

```bash
pip install -r requirements.txt
```

Also install `hume` SDK:

```bash
pip install hume
```

### 3. Add your Hume API key

Create a `.env` file in the root directory and add:

```
HUME_API_KEY=your_hume_api_key_here
```

> You need a valid Hume AI account to obtain the API key.

### 4. Run the Flask backend

```bash
python app.py
```

### 5. Open the interface

Visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
serenAI/
├── app.py                # Flask backend
├── templates/
│   └── index.html        # Frontend UI
├── static/
│   └── script.js         # Web speech + fetch logic
├── hume_utils.py         # Hume integration
├── llm_utils.py          # Emotion-aware prompt logic
├── requirements.txt
└── .env                  # Your API key (not committed)
```

---

## 🛡️ Disclaimer

This app is designed as a supportive tool, not a replacement for professional mental health services.

---

## 💡 Future Ideas

- Mood visualization using matplotlib
- Journaling and gratitude prompts
- Sentiment tracking across days
- TTS (text-to-speech) for chatbot replies

---

## 🔐 License

MIT License
