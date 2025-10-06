import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# ⚠️ Put your Spotify credentials here
CLIENT_ID = "a57433e06ffe486eae6d01db12646adc"
CLIENT_SECRET = "113bf6c45ce240c892a43c85f3d80840"

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_artist_id(artist_name: str) -> str:
    """Search and return Spotify artist ID."""
    results = sp.search(q=artist_name, type="artist", limit=1)
    if not results['artists']['items']:
        raise ValueError(f"Artist '{artist_name}' not found on Spotify.")
    return results['artists']['items'][0]['id']


def get_artist_tracks(artist_id: str) -> pd.DataFrame:
    """Fetch all tracks from artist albums/singles with ISRC codes."""
    albums = sp.artist_albums(artist_id, album_type="album,single,compilation", limit=50)
    album_ids = [a['id'] for a in albums['items']]
    
    tracks = []
    for album_id in album_ids:
        album = sp.album(album_id)
        album_tracks = sp.album_tracks(album_id)
        for t in album_tracks['items']:
            isrc = t['external_ids'].get('isrc') if 'external_ids' in t else None
            tracks.append({
                "track_name": t['name'],
                "album": album['name'],
                "release_date": album['release_date'],
                "isrc": isrc
            })
    return pd.DataFrame(tracks)
