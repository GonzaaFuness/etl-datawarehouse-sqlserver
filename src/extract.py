import pandas as pd
from pathlib import Path

def extract_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    df = pd.read_csv(path)

    print("✅ Datos cargados correctamente")
    return df