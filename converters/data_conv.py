import pandas as pd
from pathlib import Path
from .base_converter import BaseConverter


class DataConverter(BaseConverter):
    def convert(self, input_path: Path, output_format: str) -> Path:
        output_path = self.get_output_path(input_path, output_format)

        # Caricamento dati in base all'estensione
        ext = input_path.suffix.lower()
        if ext == '.csv':
            df = pd.read_csv(input_path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(input_path)
        elif ext == '.json':
            df = pd.read_json(input_path)
        else:
            raise ValueError("Formato dati non supportato per la lettura.")

        # Salvataggio nel nuovo formato
        fmt = output_format.lower()
        if fmt == 'csv':
            df.to_csv(output_path, index=False)
        elif fmt == 'xlsx':
            df.to_excel(output_path, index=False)
        elif fmt == 'json':
            df.to_json(output_path, orient='records', indent=4)
        else:
            raise ValueError("Formato di destinazione non supportato.")

        return output_path