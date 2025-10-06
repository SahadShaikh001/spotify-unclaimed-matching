import pandas as pd

def load_unclaimed_dataset(path, chunksize=100_000):
    """
    Load unclaimed dataset in chunks for very large files.
    Returns a generator of DataFrames.
    """
    try:
        for chunk in pd.read_csv(path, sep="\t", dtype=str, chunksize=chunksize, engine="python"):
            if 'ISRC' not in chunk.columns:
                raise ValueError("Dataset missing 'ISRC' column")
            chunk['ISRC'] = chunk['ISRC'].astype(str).str.strip()
            yield chunk
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset: {e}")
