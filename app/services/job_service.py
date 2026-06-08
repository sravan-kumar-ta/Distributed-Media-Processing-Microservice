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
        }

        redis_client.set(self._key(job_id), json.dumps(job))

        return job

    def get_job(self, job_id: str):
        data = redis_client.get(self._key(job_id))

        if not data:
            return None

        return json.loads(data)

    def update_status(self, job_id: str, status: str):
        job = self.get_job(job_id)

        if not job:
            return

        job["status"] = status

        redis_client.set(
            self._key(job_id),
            json.dumps(job),
        )


job_service = JobService()
