import json
import uuid

from app.services.redis_service import redis_client


class JobService:
    PREFIX = "job"

    def _key(self, job_id: str):
        return f"{self.PREFIX}:{job_id}"

    def create_job(
        self,
        file_id: str,
        operation: str,
        width: int | None = None,
        height: int | None = None,
    ):
        job_id = str(uuid.uuid4())

        job = {
            "job_id": job_id,
            "file_id": file_id,
            "operation": operation,
            "width": width,
            "height": height,
            "status": "pending",
            "result_path": None,
            "result_data": None,
            "duration": None,
            "error": None,
        }

        redis_client.set(self._key(job_id), json.dumps(job))

        return job

    def get_job(self, job_id: str):
        data = redis_client.get(self._key(job_id))

        if not data:
            return None

        return json.loads(data)

    def update_status(
        self,
        job_id: str,
        status: str,
        result_path: str | None = None,
        result_data: dict | None = None,
        duration: float | None = None,
        error: str | None = None,
    ):
        job = self.get_job(job_id)

        if not job:
            return

        job["status"] = status

        if result_path is not None:
            job["result_path"] = result_path

        if result_data is not None:
            job["result_data"] = result_data
        
        if duration is not None:
            job["duration"] = duration

        if error is not None:
            job["error"] = error

        redis_client.set(
            self._key(job_id),
            json.dumps(job),
        )

    def list_jobs(self):
        jobs = []

        for key in redis_client.scan_iter("job:*"):
            data = redis_client.get(key)

            if data:
                jobs.append(json.loads(data))

        return jobs


job_service = JobService()
