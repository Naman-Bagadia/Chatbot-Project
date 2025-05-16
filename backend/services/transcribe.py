import assemblyai as aai

aai.settings.api_key = "7655224606ff43b5bd80daac44faeaa1"

transcriber = aai.Transcriber()

def transcribe_audio(file_path):
    try:
        transcript = transcriber.transcribe(file_path)
        return transcript.text
    except Exception as e:
        return f"Error: {e}"
