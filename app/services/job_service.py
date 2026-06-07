import uuid


class JobService:
    def __init__(self):
        self.jobs = {}

    def create_job(self, file_id: str, operation: str):
        job_id = str(uuid.uuid4())
        job = {
            "job_id": job_id,
            "file_id": file_id,
            "operation": operation,
            "status": "pending",
        }
        self.jobs[job_id] = job

        return job

    def get_job(self, job_id: str):
        return self.jobs.get(job_id)


job_service = JobService()
