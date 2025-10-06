from dataset_handler import load_unclaimed_dataset
from matcher import match_by_isrc
from spotify_client import get_artist_id, get_artist_tracks
from exporter import save_to_excel_incremental
import pandas as pd
import os
from tqdm import tqdm  # progress bar

def main():
    try:
        artist_name = "Taylor Swift"
        data_path = "../data/unclaimedmusicalworkrightshares.tsv"
        output_path = "../output/final_output.xlsx"

        if not os.path.isfile(data_path):
            raise FileNotFoundError(f"Dataset not found at {data_path}")

        print(f"Fetching Spotify catalog for '{artist_name}'...")
        artist_id = get_artist_id(artist_name)
        df_artist = get_artist_tracks(artist_id)
        print(f"✅ Spotify catalog fetched: {len(df_artist)} tracks")

        print("Processing unclaimed dataset in chunks...")
        first_chunk = True
        processed_rows = 0

        for chunk in tqdm(load_unclaimed_dataset(data_path, chunksize=100_000)):
            chunk_matches = match_by_isrc(df_artist, chunk)
            processed_rows += len(chunk)
            print(f"Processed {processed_rows} rows; Matches in this chunk: {len(chunk_matches)}")

            save_to_excel_incremental(df_artist, chunk_matches, artist_name, output_path, first_chunk)
            first_chunk = False

        print(f"✅ Finished processing. Excel file saved at {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
