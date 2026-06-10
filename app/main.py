from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.jobs import router as job_router
from app.api.uploads import router as upload_router
from app.services.storage_service import create_storage_dirs

app = FastAPI(title="Media Processor")

create_storage_dirs()

app.include_router(health_router, tags=["Health"])
app.include_router(upload_router, tags=["Upload"])
app.include_router(job_router, tags=["Job"])
