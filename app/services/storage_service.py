from pathlib import Path

UPLOAD_DIR = Path("storage/uploads")

PROCESSED_DIR = Path("storage/processed")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
