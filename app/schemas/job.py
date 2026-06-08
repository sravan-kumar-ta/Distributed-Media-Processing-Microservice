from pydantic import BaseModel
from typing import Optional


# eg ops: resize, compress, watermark, thumbnail
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
    result_path: Optional[str]
    error: Optional[str]
