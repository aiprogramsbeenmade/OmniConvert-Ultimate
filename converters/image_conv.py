from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
from .base_converter import BaseConverter

# Registra il supporto per i file HEIC (iPhone)
register_heif_opener()


class ImageConverter(BaseConverter):
    def convert(self, input_path: Path, output_format: str) -> Path:
        output_path = self.get_output_path(input_path, output_format)

        with Image.open(input_path) as img:
            # Converte in RGB se salviamo come JPG (evita errori con trasparenze PNG)
            if output_format.lower() in ['jpg', 'jpeg']:
                img = img.convert('RGB')

            img.save(output_path, output_format.upper())

        return output_path