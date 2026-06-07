from fastapi import FastAPI

from app.api.uploads import router as upload_router
from app.api.jobs import router as job_router

USE_LOCAL_STORAGE = True


if USE_LOCAL_STORAGE:
    from app_local.local_storage import LocalStorage

    storage = LocalStorage()
else:
    from app.services.s3_service import S3Service

    storage = S3Service()


app = FastAPI(title="Media Processor")

app.state.storage = storage


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(upload_router)
app.include_router(job_router)
