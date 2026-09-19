import json
import queue
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model

from config import AUDIO_BLOCK_SIZE, SAMPLE_RATE, VOSK_MODEL_FOLDER


class OfflineSpeechRecognizer:
    """Capture one short command and recognize it locally with Vosk."""

    def __init__(self):
        model_path = Path(VOSK_MODEL_FOLDER)

        if not model_path.is_dir():
            raise FileNotFoundError(
                f"Vosk model folder was not found: {model_path}"
            )

        self.model = Model(str(model_path))
        

    def recognize_once(self, duration_seconds=6):
        """
        Listen for one command for a limited time.

        Audio is held temporarily in memory and is not saved to disk.
        """
        audio_queue = queue.Queue()
        recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"Microphone status: {status}")
            audio_queue.put(bytes(indata))

        print(f"Listening for up to {duration_seconds} seconds...")
        print("Speak a short test phrase, such as: open calculator")

        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=AUDIO_BLOCK_SIZE,
                device=None,
                dtype="int16",
                channels=1,
                callback=audio_callback,
            ):
                sd.sleep(int(duration_seconds * 1000))
        except Exception as error:
            raise RuntimeError(f"Microphone capture failed: {error}") from error

        while not audio_queue.empty():
            audio_data = audio_queue.get()

            if recognizer.AcceptWaveform(audio_data):
                result = json.loads(recognizer.Result())
                recognized_text = result.get("text", "").strip()

                if recognized_text:
                    return recognized_text

        final_result = json.loads(recognizer.FinalResult())
        return final_result.get("text", "").strip()


def main():
    print("Loading the local Vosk model...")
    recognizer = OfflineSpeechRecognizer()
    print("Vosk model loaded successfully.")
    print("No voice recording will be saved.")

    try:
        recognized_text = recognizer.recognize_once(duration_seconds=6)
    except (FileNotFoundError, RuntimeError) as error:
        print(f"Speech test failed: {error}")
        return

    if recognized_text:
        print(f"Recognized text: {recognized_text}")
    else:
        print("No speech was recognized. Try speaking more clearly and try again.")


if __name__ == "__main__":
    main()
