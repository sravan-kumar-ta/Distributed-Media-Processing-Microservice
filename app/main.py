from fastapi import FastAPI

from app.api.uploads import router as upload_router
from app.api.jobs import router as job_router
from app.services.storage_service import create_storage_dirs

USE_LOCAL_STORAGE = True


if USE_LOCAL_STORAGE:
    from app.storage.local import LocalStorage

    storage = LocalStorage()
else:
    from app.storage.s3 import S3Storage

    storage = S3Storage()


app = FastAPI(title="Media Processor")

app.state.storage = storage

create_storage_dirs()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "media-processor",
    }


app.include_router(upload_router)
app.include_router(job_router)
