import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/audio/transcriptions'
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

MODEL_NAME = 'whisper-large-v3'
TRANSCRIPTION_LANGUAGE = 'en'

# Paths and Locations
AUDIO_FOLDER = 'recordings'

# Filepath to store extracted address JSON
ADDRESS_JSON_PATH = 'address.json'

# User agent for Nominatim API
USER_AGENT = 'FormAutoFillBot/1.0 (dmohandm11@gmail.com)'

# Frontend Path
INDEX_HTML_PATH = 'templates/index.html'

