from fastapi import FastAPI

from app.storage.factory import get_storage

app = FastAPI(title="Media Processor")

storage = get_storage()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/test-upload")
def test_upload():
    storage.upload(source="sample.txt", destination="storage/uploads/sample.txt")

    return {"message": "uploaded"}
