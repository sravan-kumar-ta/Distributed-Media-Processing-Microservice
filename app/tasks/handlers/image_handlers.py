from app.services.image_service import image_service


def resize(job, input_file, output_file):
    image_service.resize(
        input_path=str(input_file),
        output_path=str(output_file),
        width=job["width"],
        height=job["height"],
    )


def thumbnail(job, input_file, output_file):
    image_service.create_thumbnail(
        input_path=str(input_file),
        output_path=str(output_file),
    )


def watermark(job, input_file, output_file):
    image_service.add_watermark(
        input_path=str(input_file),
        output_path=str(output_file),
        watermark_text=job["watermark_text"],
    )
