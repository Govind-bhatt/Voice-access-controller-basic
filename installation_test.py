import sqlite3
import sys
from pathlib import Path

import pyautogui
import sounddevice as sd
import vosk
from playwright.sync_api import sync_playwright


PROJECT_FOLDER = Path(__file__).resolve().parent
MODEL_FOLDER = PROJECT_FOLDER / "models" / "vosk-model-small-en-us-0.15"


def main():
    print("Voice assistant installation test")
    print("---------------------------------")
    print(f"Python version: {sys.version.split()[0]}")
    print("Vosk import: OK")
    print("sounddevice import: OK")
    print("PyAutoGUI import: OK")
    print("Playwright import: OK")

    try:
        sqlite3.connect(":memory:").close()
        print("SQLite test: OK")
    except sqlite3.Error as error:
        print(f"SQLite test: FAILED ({error})")

    if MODEL_FOLDER.is_dir():
        print(f"Vosk model folder: OK ({MODEL_FOLDER})")
    else:
        print(f"Vosk model folder: NOT FOUND ({MODEL_FOLDER})")

    try:
        input_device = sd.query_devices(kind="input")
        print(f"Microphone: OK ({input_device['name']})")
    except Exception as error:
        print(f"Microphone: FAILED ({error})")

    print(f"Screen size detected: {pyautogui.size()}")

    with sync_playwright() as playwright:
        print("Playwright engine: OK")
        print(f"Chromium executable available: {bool(playwright.chromium.executable_path)}")

    print("---------------------------------")
    print("Installation test finished.")


if __name__ == "__main__":
    main()
