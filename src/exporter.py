import pandas as pd
import os

def save_to_excel_incremental(df_artist, chunk_matches, artist_name, output_path, first_chunk=False):
    """
    Save artist catalog and matches incrementally to Excel.
    Works safely with large files and avoids 'At least one sheet must be visible' error.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if first_chunk:
        # Create new Excel with Artist Catalog & first chunk of Matches
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_artist.to_excel(writer, sheet_name="Artist Catalog", index=False)
            chunk_matches.to_excel(writer, sheet_name="Matches", index=False)
            notes = pd.DataFrame({
                "Notes": [
                    f"Artist chosen: {artist_name}",
                    "Matched songs are in 'Matches' sheet",
                    "Unclaimed dataset was cross-checked using ISRC"
                ]
            })
            notes.to_excel(writer, sheet_name="Notes", index=False)
    else:
        # Append new matches to existing Excel using 'mode=a'
        with pd.ExcelWriter(output_path, engine="openpyxl", mode='a', if_sheet_exists='overlay') as writer:
            # Read existing matches
            try:
                existing = pd.read_excel(output_path, sheet_name="Matches")
            except Exception:
                existing = pd.DataFrame()
            combined = pd.concat([existing, chunk_matches], ignore_index=True)
            combined.to_excel(writer, sheet_name="Matches", index=False)
