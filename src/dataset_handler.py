import pandas as pd
import os

def load_unclaimed_dataset(path: str) -> pd.DataFrame:
    """Load unclaimed TSV dataset."""
    print(f"Reading dataset from: {os.path.abspath(path)}")
    df = pd.read_csv(path, sep="\t", dtype=str)
    print(f"Columns found: {df.columns.tolist()}")
    if 'ISRC' not in df.columns:
        raise ValueError("Dataset missing 'ISRC' column")
    df['ISRC'] = df['ISRC'].astype(str).str.strip()
    print(f"Dataset loaded successfully, {len(df)} rows")
    return df
