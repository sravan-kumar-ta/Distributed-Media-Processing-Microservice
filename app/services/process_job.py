import time

from app.services.job_service import job_service


def process_job(job_id: str):
    job_service.update_status(job_id, "processing")
    time.sleep(5)

    job_service.update_status(job_id, "completed")
