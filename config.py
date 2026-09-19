import os
from pathlib import Path


# Main project folders.
PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data"
MODELS_FOLDER = PROJECT_FOLDER / "models"

# Local Vosk model location.
VOSK_MODEL_FOLDER = MODELS_FOLDER / "vosk-model-small-en-us-0.15"

# The application database will be created here.
DATABASE_PATH = DATA_FOLDER / "assistant.db"

# Safe local demonstration webpage.
DEMO_PAGE_PATH = PROJECT_FOLDER / "demo_site" / "index.html"

# Voice recognition settings.
SAMPLE_RATE = 16000
AUDIO_BLOCK_SIZE = 8000

# Maximum incorrect access-code attempts during one session.
MAX_ACCESS_ATTEMPTS = 3

# The access code is intentionally not stored in SQLite or printed.
# Set it in Windows with:
#   $env:VOICE_ASSISTANT_ACCESS_CODE = "your-code"
ACCESS_CODE = os.environ.get("VOICE_ASSISTANT_ACCESS_CODE", "")


def ensure_project_folders():
    """Create folders required by the application."""
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    MODELS_FOLDER.mkdir(parents=True, exist_ok=True)


def access_code_is_configured():
    """Return True when an access code has been configured."""
    return bool(ACCESS_CODE)


if __name__ == "__main__":
    ensure_project_folders()

    print(f"Project folder: {PROJECT_FOLDER}")
    print(f"Database path: {DATABASE_PATH}")
    print(f"Vosk model exists: {VOSK_MODEL_FOLDER.is_dir()}")
    print(f"Access code configured: {access_code_is_configured()}")
