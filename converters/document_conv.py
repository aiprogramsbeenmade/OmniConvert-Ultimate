import subprocess
from pathlib import Path
from .base_converter import BaseConverter

# Importiamo le librerie per i PDF
try:
    from pdf2docx import Converter as PDFConverter
except ImportError:
    PDFConverter = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


class DocumentConverter(BaseConverter):
    def convert(self, input_path: Path, output_format: str) -> Path:
        output_format = output_format.lower()
        output_path = self.get_output_path(input_path, output_format)
        output_dir = output_path.parent

        # CASO 1: Da PDF a DOCX (Usa pdf2docx)
        if input_path.suffix.lower() == '.pdf' and output_format == 'docx':
            if PDFConverter is None:
                raise Exception("Esegui: pip install pdf2docx")
            cv = PDFConverter(str(input_path))
            cv.convert(str(output_path))
            cv.close()
            return output_path

        # CASO 2: Da PDF a TXT (Usa PyMuPDF/fitz)
        if input_path.suffix.lower() == '.pdf' and output_format == 'txt':
            if fitz is None:
                raise Exception("Esegui: pip install pymupdf")

            doc = fitz.open(str(input_path))
            text = ""
            for page in doc:
                text += page.get_text()

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            doc.close()
            return output_path

        # TUTTI GLI ALTRI CASI (LibreOffice)
        try:
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', output_format,
                str(input_path),
                '--outdir', str(output_dir)
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return output_path
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else "Errore LibreOffice"
            raise Exception(f"Errore LibreOffice: {error_msg}")