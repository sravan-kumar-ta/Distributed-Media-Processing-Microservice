from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.jobs import router as job_router
from app.api.uploads import router as upload_router
from app.services.storage_service import create_storage_dirs

USE_LOCAL_STORAGE = False


if USE_LOCAL_STORAGE:
    from app.storage.local import LocalStorage

    storage = LocalStorage()
else:
    from app.storage.s3 import S3Storage

    storage = S3Storage()


app = FastAPI(title="Media Processor")

app.state.storage = storage

create_storage_dirs()

app.include_router(health_router, tags=["Health"])
app.include_router(upload_router, tags=["Upload"])
app.include_router(job_router, tags=["Job"])
