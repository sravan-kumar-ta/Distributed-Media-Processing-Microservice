import time

from app.core.celery_app import celery_app
from app.services.job_service import job_service


@celery_app.task(name="process_jobs")
def process_jobs(job_id: str):
    job_service.update_status(job_id, "processing")
    time.sleep(5)
    job_service.update_status(job_id, "completed")
    return f"Success: Status changed."
