import time

from pathlib import Path
import tempfile

from app.core.celery_app import celery_app
from app.services.file_service import file_service
from app.services.image_service import image_service
from app.services.job_service import job_service
from app.services.video_service import video_service
from app.storage.factory import get_storage


@celery_app.task(
    name="process_job",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def process_job(job_id: str):
    started_at = time.perf_counter()
    try:
        job_service.update_status(job_id, "processing")

        job = job_service.get_job(job_id)

        if not job:
            raise Exception(f"Job {job_id} not found")

        file_meta = file_service.get_file_metadata(job["file_id"])

        if not file_meta:
            raise Exception("File metadata not found")

        storage = get_storage()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            extension = Path(file_meta["storage_key"]).suffix

            input_file = tmp_dir / f"input{extension}"
            output_file = tmp_dir / "output.jpg"

            storage.download(
                object_key=file_meta["storage_key"],
                local_path=str(input_file),
            )

            if job["operation"] == "resize":
                image_service.resize(
                    input_path=str(input_file),
                    output_path=str(output_file),
                    width=job["width"],
                    height=job["height"],
                )

            elif job["operation"] == "thumbnail":
                image_service.create_thumbnail(
                    input_path=str(input_file),
                    output_path=str(output_file),
                )

            elif job["operation"] == "video_thumbnail":
                video_service.generate_thumbnail(
                    input_path=str(input_file),
                    output_path=str(output_file),
                )

            elif job["operation"] == "watermark":
                image_service.add_watermark(
                    input_path=str(input_file),
                    output_path=str(output_file),
                    watermark_text=job["watermark_text"],
                )

            elif job["operation"] == "video_metadata":
                metadata = video_service.get_metadata(
                    input_path=str(input_file),
                )
                duration = round(time.perf_counter() - started_at, 3)
                job_service.update_status(
                    job_id=job_id,
                    status="completed",
                    result_data=metadata,
                    result_type="application/json",
                    duration=duration,
                )

                return "Success: Metadata extracted."

            elif job["operation"] == "video_compress":
                output_file = tmp_dir / "compressed.mp4"
                video_service.compress_video(
                    input_path=str(input_file),
                    output_path=str(output_file),
                )

                result_key = f"processed/{job_id}.mp4"

                storage.upload(
                    local_path=str(output_file),
                    object_key=result_key,
                )

                job_service.update_status(
                    job_id=job_id,
                    status="completed",
                    result_path=result_key,
                    result_type="video/mp4",
                )

                return "Success: Video compressed."

            elif job["operation"] == "audio_extract":
                output_file = tmp_dir / "audio_extract.mp3"
                video_service.extract_audio(
                    input_path=str(input_file),
                    output_path=str(output_file),
                )

                result_key = f"processed/{job_id}.mp3"

                storage.upload(
                    local_path=str(output_file),
                    object_key=result_key,
                )

                job_service.update_status(
                    job_id=job_id,
                    status="completed",
                    result_path=result_key,
                    result_type="audio/mpeg",
                )

                return "Success: Audio extracted."
            else:
                raise Exception(f"Unsupported operation: " f"{job['operation']}")

            result_key = (
                f"processed/" f"{job_id}.jpg"
            )  # We have to change this if add video_compress

            storage.upload(
                local_path=str(output_file),
                object_key=result_key,
            )

        duration = round(time.perf_counter() - started_at, 3)

        job_service.update_status(
            job_id=job_id,
            status="completed",
            result_path=result_key,
            result_type="image/jpeg",
            duration=duration,
        )

        return f"Success: Operation completed."

    except Exception as exc:

        job_service.update_status(
            job_id=job_id,
            status="failed",
            error=str(exc),
        )

        raise
