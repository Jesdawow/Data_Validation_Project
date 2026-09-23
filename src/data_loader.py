from pathlib import Path

import pandas as pd

def load_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV file and return it as a pandas DataFrame.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}.")

    dataframe = pd.read_csv(path)
    return dataframe
