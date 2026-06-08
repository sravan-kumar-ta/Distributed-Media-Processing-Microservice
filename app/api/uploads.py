import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Request

from app.schemas.upload import UploadResponse
from app.services.file_service import file_service

router = APIRouter()


@router.post("/uploads", response_model=UploadResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    extension = Path(file.filename).suffix
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{extension}"
    storage = request.app.state.storage
    storage.save_upload(file=file, filename=filename)

    file_service.save_file_metadata(
        file_id=file_id,
        storage_key=filename,
        original_filename=file.filename,
    )

    return UploadResponse(
        file_id=file_id,
        file_path=filename,
    )
