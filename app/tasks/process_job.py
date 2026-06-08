from pathlib import Path
import tempfile

from app.core.celery_app import celery_app
from app.services.file_service import file_service
from app.services.image_service import image_service
from app.services.job_service import job_service
from app.storage.factory import get_storage


@celery_app.task(name="process_jobs")
def process_jobs(job_id: str):
    try:
        job_service.update_status(job_id, "processing")

        job = job_service.get_job(job_id)

        if not job:
            raise Exception(f"Job {job_id} not found")

        file_meta = file_service.get_file_metadata(job["file_id"])

        if not file_meta:
            raise Exception("File metadata not found")

        storage = get_storage()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            input_file = tmp_dir / "input.jpg"
            output_file = tmp_dir / "output.jpg"

            storage.download(
                object_key=file_meta["storage_key"],
                local_path=str(input_file),
            )

            if job["operation"] == "resize":
                image_service.resize(
                    input_path=str(input_file),
                    output_path=str(output_file),
                    width=job["width"],
                    height=job["height"],
                )

            elif job["operation"] == "thumbnail":
                image_service.create_thumbnail(
                    input_path=str(input_file),
                    output_path=str(output_file),
                )

            else:
                raise Exception(f"Unsupported operation: " f"{job['operation']}")

            result_key = f"processed/" f"{job_id}.jpg"

            storage.upload(
                local_path=str(output_file),
                object_key=result_key,
            )

        job_service.update_status(
            job_id=job_id,
            status="completed",
            result_path=result_key,
        )

        return f"Success: Operation completed."
    
    except Exception as exc:

        job_service.update_status(
            job_id=job_id,
            status="failed",
            error=str(exc),
        )

        raise
        