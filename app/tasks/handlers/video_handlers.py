from app.services.video_service import video_service


def video_thumbnail(job, input_file, output_file):
    video_service.generate_thumbnail(
        input_path=str(input_file),
        output_path=str(output_file),
    )


def video_metadata(job, input_file):
    return video_service.get_metadata(
        input_path=str(input_file),
    )


def video_compress(job, input_file, output_file):
    video_service.compress_video(
        input_path=str(input_file),
        output_path=str(output_file),
    )


def audio_extract(job, input_file, output_file):
    video_service.extract_audio(
        input_path=str(input_file),
        output_path=str(output_file),
    )
