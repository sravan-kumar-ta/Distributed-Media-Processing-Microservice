from pathlib import Path
import shutil


class LocalStorage:
    UPLOAD_DIR = Path("storage/uploads")

    def __init__(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file, filename: str):
        destination = self.UPLOAD_DIR / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(destination)
