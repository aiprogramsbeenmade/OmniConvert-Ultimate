from abc import ABC, abstractmethod
from pathlib import Path


class BaseConverter(ABC):
    """Classe astratta per definire lo standard di ogni convertitore."""

    @abstractmethod
    def convert(self, input_path: Path, output_format: str) -> Path:
        pass

    def get_output_path(self, input_path: Path, output_format: str) -> Path:
        desktop_path = Path.home() / "Desktop" / "OmniConvert_Output"
        desktop_path.mkdir(exist_ok=True)

        base_name = input_path.stem
        final_path = desktop_path / f"{base_name}.{output_format.lower()}"

        # Se il file esiste già, aggiungiamo un contatore (es. _1, _2...)
        counter = 1
        while final_path.exists():
            final_path = desktop_path / f"{base_name}_{counter}.{output_format.lower()}"
            counter += 1

        return final_path