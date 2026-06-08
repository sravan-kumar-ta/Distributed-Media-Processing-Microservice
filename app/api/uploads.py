import shutil
import tempfile
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

    storage_key = f"uploads/{file_id}{extension}"

    storage = request.app.state.storage

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension,
    ) as tmp_file:
        shutil.copyfileobj(
            file.file,
            tmp_file,
        )

        temp_path = tmp_file.name

    try:
        storage.upload(local_path=temp_path, object_key=storage_key)

        file_service.save_file_metadata(
            file_id=file_id,
            storage_key=storage_key,
            original_filename=file.filename,
        )

    finally:
        Path(temp_path).unlink(missing_ok=True)

    return UploadResponse(
        file_id=file_id,
        file_path=storage_key,
    )
