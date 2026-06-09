from fastapi import APIRouter, HTTPException

from app.schemas.job import CreateJobRequest, JobResponse, JobDetailResponse
from app.services.job_service import job_service

from app.tasks.process_job import process_job

router = APIRouter()

ALLOWED_OPERATIONS = {
    "resize",
    "thumbnail",
    "video_thumbnail",
    "video_metadata",
}


@router.post("/jobs", response_model=JobResponse)
def create_job(payload: CreateJobRequest):
    if payload.operation not in ALLOWED_OPERATIONS:
        raise HTTPException(status_code=400, detail="Invalid operation")

    if payload.operation == "resize" and (
        payload.width is None or payload.height is None
    ):
        raise HTTPException(
            status_code=400,
            detail=("width and height required"),
        )

    job = job_service.create_job(
        file_id=payload.file_id,
        operation=payload.operation,
        width=payload.width,
        height=payload.height,
    )

    process_job.delay(job["job_id"])

    return JobResponse(
        job_id=job["job_id"],
        status=job["status"],
    )


@router.get("/jobs/{job_id}", response_model=JobDetailResponse)
def get_job(job_id: str):
    job = job_service.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.get("/jobs")
def list_jobs():
    return job_service.list_jobs()
