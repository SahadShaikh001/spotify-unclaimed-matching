from dataset_handler import load_unclaimed_dataset
from spotify_client import get_artist_id, get_artist_tracks
from matcher import match_by_isrc
from exporter import save_to_excel
import os

def main():
    try:
        artist_name = "Taylor Swift"
        data_path = "../data/unclaimedmusicalworkrightshares.tsv"
        output_path = "../output/final_output.xlsx"

        if not os.path.isfile(data_path):
            raise FileNotFoundError(f"Dataset not found at {data_path}")

        print("Loading dataset...")
        df_unclaimed = load_unclaimed_dataset(data_path)
        print(f"✅ Dataset loaded: {len(df_unclaimed)} rows")

        print(f"Fetching Spotify catalog for '{artist_name}'...")
        artist_id = get_artist_id(artist_name)
        df_artist = get_artist_tracks(artist_id)
        print(f"✅ Spotify catalog fetched: {len(df_artist)} tracks")

        print("Matching ISRC codes...")
        df_matches = match_by_isrc(df_artist, df_unclaimed)
        print(f"✅ Found {len(df_matches)} matching tracks")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        print("Exporting results to Excel...")
        save_to_excel(df_artist, df_matches, artist_name, output_path)
        print(f"✅ Done! Results saved at {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
