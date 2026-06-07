from pydantic import BaseModel


# eg ops: resize, compress, watermark, thumbnail
class CreateJobRequest(BaseModel):
    file_id: str
    operation: str


class JobResponse(BaseModel):
    job_id: str
    status: str
