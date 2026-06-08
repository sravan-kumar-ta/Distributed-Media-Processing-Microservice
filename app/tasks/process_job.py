from app.core.celery_app import celery_app
from app.services.file_service import file_service
from app.services.image_service import image_service
from app.services.job_service import job_service


@celery_app.task(name="process_jobs")
def process_jobs(job_id: str):
    try:
        job = job_service.get_job(job_id)

        job_service.update_status(job_id, "processing")

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

        job_service.update_status(job_id, "completed")

        return f"Success: Status changed."

    except Exception:
        job_service.update_status(job_id, "failed")

        raise
