from PIL import Image, ImageDraw, ImageFont


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

    def add_watermark(
        self,
        input_path: str,
        output_path: str,
        watermark_text: str,
    ):
        image = Image.open(input_path).convert("RGBA")
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        width, height = image.size
        font = ImageFont.load_default()

        for x in range(0, width, 200):
            for y in range(0, height, 120):
                draw.text((x, y), watermark_text, fill=(255, 255, 255, 60), font=font)

        overlay = overlay.rotate(30, expand=False)

        result = Image.alpha_composite(image, overlay)
        result.convert("RGB").save(output_path)


image_service = ImageService()
