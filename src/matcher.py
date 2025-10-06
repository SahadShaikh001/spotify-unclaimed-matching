import pandas as pd

def match_by_isrc(df_artist: pd.DataFrame, df_unclaimed: pd.DataFrame) -> pd.DataFrame:
    """
    Find ISRC matches between artist catalog and unclaimed dataset.
    """
    if "isrc" not in df_artist.columns:
        raise ValueError("Artist DataFrame missing 'isrc' column")
    if "ISRC" not in df_unclaimed.columns:
        raise ValueError("Unclaimed DataFrame missing 'ISRC' column")
    
    return df_artist.merge(df_unclaimed, left_on="isrc", right_on="ISRC", how="inner")
