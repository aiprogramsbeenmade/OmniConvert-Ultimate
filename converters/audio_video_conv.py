import ffmpeg
from pathlib import Path
from .base_converter import BaseConverter


class AudioVideoConverter(BaseConverter):
    def convert(self, input_path: Path, output_format: str) -> Path:
        output_path = self.get_output_path(input_path, output_format)

        try:
            # stream = riceve l'input
            stream = ffmpeg.input(str(input_path))
            # output = processa e salva
            stream = ffmpeg.output(stream, str(output_path))
            # run = esegue il comando FFmpeg (overwrite_output=True permette di sovrascrivere)
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"Errore FFmpeg: {e.stderr.decode()}")