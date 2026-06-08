from pathlib import Path

from PIL import Image


class ImageService:
    def resize(
        self,
        input_path: str,
        output_path: str,
        width: int,
        height: int,
    ):
        image = Image.open(input_path)
        image = image.resize((width, height))
        image.save(output_path)

    def create_thumbnail(self, input_path, output_path):
        image = Image.open(input_path)
        image.thumbnail((200, 200))
        image.save(output_path)


image_service = ImageService()
