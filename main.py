from src.utils import transcribe_audio, get_latest_audio_file
from src.config import AUDIO_FOLDER

import time
import src.extract_address as extract_address


def main():
    print("Waiting for audio recording...")
    while True:
        file_path = get_latest_audio_file(AUDIO_FOLDER)
        if file_path:
            transcription = transcribe_audio(file_path)
            break
        time.sleep(2)
    if transcription:
        extract_address.main(transcription)
    return transcription

if __name__ == '__main__':
    main()
