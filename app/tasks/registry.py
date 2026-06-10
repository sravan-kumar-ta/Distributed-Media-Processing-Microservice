from app.tasks.handlers.image_handlers import resize, thumbnail, watermark
from app.tasks.handlers.video_handlers import (
    video_thumbnail,
    video_metadata,
    video_compress,
    audio_extract,
)

OPERATIONS = {
    "resize": {
        "handler": resize,
        "extension": ".jpg",
        "content_type": "image/jpeg",
        "metadata_only": False,
    },
    "thumbnail": {
        "handler": thumbnail,
        "extension": ".jpg",
        "content_type": "image/jpeg",
        "metadata_only": False,
    },
    "watermark": {
        "handler": watermark,
        "extension": ".jpg",
        "content_type": "image/jpeg",
        "metadata_only": False,
    },
    "video_thumbnail": {
        "handler": video_thumbnail,
        "extension": ".jpg",
        "content_type": "image/jpeg",
        "metadata_only": False,
    },
    "video_compress": {
        "handler": video_compress,
        "extension": ".mp4",
        "content_type": "video/mp4",
        "metadata_only": False,
    },
    "audio_extract": {
        "handler": audio_extract,
        "extension": ".mp3",
        "content_type": "audio/mpeg",
        "metadata_only": False,
    },
    "video_metadata": {
        "handler": video_metadata,
        "extension": None,
        "content_type": "application/json",
        "metadata_only": True,
    },
}
