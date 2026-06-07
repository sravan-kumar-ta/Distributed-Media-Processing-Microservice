from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.schemas.job import CreateJobRequest, JobResponse
from app.services.job_service import job_service
from app.services.process_job import process_job

router = APIRouter()

ALLOWED_OPERATIONS = {
    "resize",
    "compress",
    "watermark",
    "thumbnail",
}


@router.post("/jobs", response_model=JobResponse)
def create_job(payload: CreateJobRequest, background_tasks: BackgroundTasks):
    if payload.operation not in ALLOWED_OPERATIONS:
        raise HTTPException(status_code=400, detail="Invalid operation")

    job = job_service.create_job(
        file_id=payload.file_id,
        operation=payload.operation,
    )

    background_tasks.add_task(process_job, job["job_id"])

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
