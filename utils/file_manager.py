import os
from pathlib import Path

def get_unique_path(path: Path) -> Path:
    """Se il file esiste già, aggiunge un numero (es. file_1.jpg)."""
    counter = 1
    original_path = path
    while path.exists():
        path = original_path.with_name(f"{original_path.stem}_{counter}{original_path.suffix}")
        counter += 1
    return path

def clean_outputs(output_dir: Path):
    """Pulisce la cartella output (opzionale)."""
    for file in output_dir.glob("*"):
        if file.is_file():
            os.remove(file)