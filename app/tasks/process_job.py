from app.core.celery_app import celery_app
from app.services.file_service import file_service
from app.services.image_service import image_service
from app.services.job_service import job_service


@celery_app.task(name="process_jobs")
def process_jobs(job_id: str):
    try:
        job_service.update_status(job_id, "processing")

        job = job_service.get_job(job_id)

        file_meta = file_service.get_file_metadata(job["file_id"])

        input_path = f"storage/uploads/" f"{file_meta['storage_key']}"
        output_path = f"storage/processed/" f"{job_id}.jpg"

        if job["operation"] == "resize":
            image_service.resize(
                input_path=input_path,
                output_path=output_path,
                width=job["width"],
                height=job["height"],
            )
        elif job["operation"] == "thumbnail":
            image_service.create_thumbnail(
                input_path=input_path,
                output_path=output_path,
            )

        job_service.update_status(
            job_id,
            "completed",
            result_path=output_path,
        )

        return f"Success: Operation completed."

    except Exception as exc:

        job_service.update_job(
            job_id,
            status="failed",
            error=str(exc),
        )

        raise
