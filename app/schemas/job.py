from pydantic import BaseModel
from typing import Optional


class CreateJobRequest(BaseModel):
    file_id: str
    operation: str
    width: Optional[int] = None
    height: Optional[int] = None


class JobResponse(BaseModel):
    job_id: str
    status: str


class JobDetailResponse(BaseModel):
    job_id: str
    file_id: str
    operation: str
    status: str

    result_path: str | None = None
    result_type: str | None = None
    result_data: dict | None = None

    download_url: str | None = None
    duration: float | None = None
    error: str | None = None
