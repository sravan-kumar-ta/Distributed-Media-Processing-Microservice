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
