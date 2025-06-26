from src.config import GROQ_API_KEY, GROQ_ENDPOINT, MODEL_NAME, TRANSCRIPTION_LANGUAGE

import os
import requests



def transcribe_audio(file_path):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }
    with open(file_path, 'rb') as audio_file:
        files = {
            'file': (os.path.basename(file_path), audio_file, 'audio/webm'),
        }
        data = {
            'model': MODEL_NAME,  # or whichever model Groq supports
            'language': TRANSCRIPTION_LANGUAGE  # Enforce English transcription
        }
        print(f"Uploading {file_path} for transcription...")
        response = requests.post(GROQ_ENDPOINT, headers=headers, data=data, files=files)

    if response.status_code == 200:
        transcription = response.json().get('text', '')
        print("Transcription:", transcription)
        return transcription
    else:
        print("Failed to transcribe:", response.text)
        return None
    
def get_latest_audio_file(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.webm')]
    if not files:
        return None
    files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return os.path.join(folder, files[0])