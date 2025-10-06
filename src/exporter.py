import pandas as pd

def save_to_excel(df_artist: pd.DataFrame, df_matches: pd.DataFrame, artist_name: str, output_path: str):
    """Save results into an Excel file with multiple sheets."""
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_artist.to_excel(writer, sheet_name="Artist Catalog", index=False)
        df_matches.to_excel(writer, sheet_name="Matches", index=False)
        
        notes = pd.DataFrame({
            "Notes": [
                f"Artist chosen: {artist_name}",
                "Matched songs are in 'Matches' sheet",
                "Unclaimed dataset was cross-checked using ISRC"
            ]
        })
        notes.to_excel(writer, sheet_name="Notes", index=False)
