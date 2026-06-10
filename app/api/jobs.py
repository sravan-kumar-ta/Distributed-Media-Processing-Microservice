from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse
import shutil
import tempfile
from pathlib import Path

from app.schemas.job import CreateJobRequest, JobResponse, JobDetailResponse
from app.services.job_service import job_service
from app.storage.factory import get_storage
from app.tasks.process_job import process_job

router = APIRouter()

ALLOWED_OPERATIONS = {
    "resize",
    "thumbnail",
    "video_thumbnail",
    "video_metadata",
    "video_compress",
    "audio_extract",
}


def cleanup_temp_dir(temp_dir: str):
    shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/job", response_model=JobResponse)
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
def get_job(job_id: str, request: Request):
    job = job_service.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    download_url = None

    if job["status"] == "completed" and job.get("result_path"):
        download_url = str(request.base_url) + f"jobs/{job_id}/download"

    return {
        **job,
        "download_url": download_url,
    }


@router.get("/jobs")
def list_jobs():
    return job_service.list_jobs()


@router.get("/jobs/{job_id}/download")
def download_result(job_id: str, background_tasks: BackgroundTasks):
    job = job_service.get_job(job_id)

    if not job:
        raise HTTPException(404, "Job not found")

    if job["status"] != "completed":
        raise HTTPException(400, "Job not completed")

    if not job["result_path"]:
        raise HTTPException(404, "No result available")

    storage = get_storage()

    tmp_dir = tempfile.mkdtemp()
    local_file = Path(tmp_dir) / Path(job["result_path"]).name

    storage.download(
        object_key=job["result_path"],
        local_path=str(local_file),
    )

    # Cleanup Temporary Files
    background_tasks.add_task(cleanup_temp_dir, tmp_dir)

    return FileResponse(
        path=str(local_file),
        filename=local_file.name,
    )


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    if job_service.delete_job(job_id):
        return {"message": "Job deleted"}

    return {"message": "Invalid job_id"}
