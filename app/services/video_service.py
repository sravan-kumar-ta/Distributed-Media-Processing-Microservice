import ffmpeg


class VideoService:
    def generate_thumbnail(
        self,
        input_path: str,
        output_path: str,
        timestamp: int = 1,
    ):
        (
            ffmpeg.input(input_path, ss=timestamp)
            .output(output_path, vframes=1)
            .overwrite_output()
            .run(quiet=True)
        )

    def get_metadata(self, input_path: str):
        return ffmpeg.probe(input_path)

    def compress_video(
        self,
        input_path: str,
        output_path: str,
    ):
        (
            ffmpeg.input(input_path)
            .output(output_path, vcodec="libx264", crf=28)
            .overwrite_output()
            .run(quiet=True)
        )

    def extract_audio(
        self,
        input_path: str,
        output_path: str,
    ):
        (
            ffmpeg.input(input_path)
            .output(output_path, acodec="mp3")
            .overwrite_output()
            .run(quiet=True)
        )


video_service = VideoService()
