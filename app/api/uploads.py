import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Request

from app.schemas.upload import UploadResponse

router = APIRouter()


@router.post("/uploads", response_model=UploadResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    extension = Path(file.filename).suffix
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{extension}"
    storage = request.app.state.storage

    file_path = storage.save_upload(file=file, filename=filename)

    return UploadResponse(
        file_id=file_id,
        file_path=file_path,
    )
