import time
import tempfile

from pathlib import Path

from app.core.celery_app import celery_app
from app.services.file_service import file_service
from app.services.job_service import job_service
from app.storage.factory import get_storage

from app.tasks.registry import OPERATIONS


@celery_app.task(
    name="process_job",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def process_job(job_id: str):
    """
    Main Celery worker task.

    Workflow:
        1. Load job metadata from Redis
        2. Download source file from storage
        3. Execute requested operation
        4. Upload processed result
        5. Update job status
    """
    started_at = time.perf_counter()

    try:
        # Mark job as actively being processed
        job_service.update_status(job_id, "processing")

        # Retrieve job details
        job = job_service.get_job(job_id)

        if not job:
            raise Exception(f"Job {job_id} not found")

        # Retrieve uploaded file metadata
        file_meta = file_service.get_file_metadata(job["file_id"])

        if not file_meta:
            raise Exception("File metadata not found")

        # Lookup operation configuration
        # (handler, output extension, content type, etc.)
        operation = job["operation"]
        config = OPERATIONS.get(operation)

        if not config:
            raise Exception(f"Unsupported operation: {operation}")

        storage = get_storage()

        # Create isolated temporary workspace
        # All processing happens here before uploading
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)

            # Preserve original file extension
            input_extension = Path(file_meta["storage_key"]).suffix
            input_file = tmp_dir / f"input{input_extension}"

            # Download original file from storage
            storage.download(
                object_key=file_meta["storage_key"],
                local_path=str(input_file),
            )

            # Metadata operations return JSON data
            # instead of producing a processed file.
            if config["metadata_only"]:
                metadata = config["handler"](job, input_file)

                duration = round(time.perf_counter() - started_at, 3)

                job_service.update_status(
                    job_id=job_id,
                    status="completed",
                    result_data=metadata,
                    result_type=config["content_type"],
                    duration=duration,
                )

                return "Success: Metadata extracted."

            # File-producing operations
            # Example:
            #   resize -> .jpg
            #   video_compress -> .mp4
            #   audio_extract -> .mp3
            output_file = tmp_dir / f"output{config['extension']}"

            config["handler"](job, input_file, output_file)

            # Store processed result under a predictable key
            result_key = f"processed/" f"{job_id}" f"{config['extension']}"

            storage.upload(
                local_path=str(output_file),
                object_key=result_key,
            )

        duration = round(time.perf_counter() - started_at, 3)

        # Persist final success state
        job_service.update_status(
            job_id=job_id,
            status="completed",
            result_path=result_key,
            result_type=config["content_type"],
            duration=duration,
        )

        return "Success: Operation completed."

    except Exception as exc:
        # Persist failure information before Celery retries or marks task failed
        job_service.update_status(job_id=job_id, status="failed", error=str(exc))

        raise
