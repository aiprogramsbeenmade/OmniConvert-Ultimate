from pathlib import Path
from .image_conv import ImageConverter
from .document_conv import DocumentConverter
from .audio_video_conv import AudioVideoConverter
from .data_conv import DataConverter


class ConversionDispatcher:
    def __init__(self):
        self.image_conv = ImageConverter()
        self.doc_conv = DocumentConverter()
        self.av_conv = AudioVideoConverter()
        self.data_conv = DataConverter()

        self.map = {
            # Immagini (Aggiunti TIFF, ICO, GIF)
            '.jpg': self.image_conv, '.jpeg': self.image_conv, '.png': self.image_conv,
            '.webp': self.image_conv, '.heic': self.image_conv, '.bmp': self.image_conv,
            '.tiff': self.image_conv, '.ico': self.image_conv, '.gif': self.image_conv,

            # Documenti (Aggiunti EPUB, RTF)
            '.docx': self.doc_conv, '.doc': self.doc_conv, '.odt': self.doc_conv,
            '.pdf': self.doc_conv, '.txt': self.doc_conv, '.epub': self.doc_conv,
            '.rtf': self.doc_conv,

            # Audio/Video (Aggiunti WEBM, FLAC, OGG)
            '.mp4': self.av_conv, '.mkv': self.av_conv, '.mov': self.av_conv,
            '.avi': self.av_conv, '.mp3': self.av_conv, '.wav': self.av_conv,
            '.webm': self.av_conv, '.flac': self.av_conv, '.ogg': self.av_conv,

            # Dati
            '.csv': self.data_conv, '.xlsx': self.data_conv, '.json': self.data_conv,
            '.xls': self.data_conv
        }

    def get_converter(self, file_path: Path):
        return self.map.get(file_path.suffix.lower())