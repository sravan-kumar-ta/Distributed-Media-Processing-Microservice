from fastapi import APIRouter, HTTPException

from app.schemas.job import CreateJobRequest, JobResponse
from app.services.job_service import job_service

from app.tasks.process_job import process_jobs

router = APIRouter()

ALLOWED_OPERATIONS = {
    "resize",
    "compress",
    "watermark",
    "thumbnail",
}


@router.post("/jobs", response_model=JobResponse)
def create_job(payload: CreateJobRequest):
    if payload.operation not in ALLOWED_OPERATIONS:
        raise HTTPException(status_code=400, detail="Invalid operation")

    job = job_service.create_job(
        file_id=payload.file_id,
        operation=payload.operation,
        width=payload.width,
        height=payload.height,
    )

    process_jobs.delay(job["job_id"])

    return JobResponse(
        job_id=job["job_id"],
        status=job["status"],
    )


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = job_service.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
