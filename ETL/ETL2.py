import re
import mysql.connector
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os


load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

print(os.getenv("SPOTIFY_CLIENT_ID"))

db_config= {
    'host': 'localhost',
    'user': 'root',
    'password': 'thilks',
    'database': 'spotify_db'
}
try:
    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor()

    file_path = "track_urls.txt"

    with open(file_path, 'r') as file:

        tracks = file.readlines()

    for track_url in tracks:

        match = re.search(r'track/([a-zA-Z0-9]+)',track_url)

        if match:
            track_id = match.group(1)
        else:
            raise ValueError("Invalid spotify track URL")

        track = sp.track(track_id)

        print(track.keys())

        track_data={
            'Spotify ID': track['id'],
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album' : track['album']['name'],
            'Track Number':track['track_number'],
            'Type':track['type'],
            'Duration (minutes)': round(track['duration_ms'] / 60000,2)
        }

        print("\n Track Details")
        print(track_data)

        insert_query = """
        INSERT INTO spotify_data(spotify_id,track_name,artist,album,track_number,type,duration_minutes)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            track_data['Spotify ID'],
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Track Number'],
            track_data['Type'],
            track_data['Duration (minutes)']
            )

        cursor.execute(insert_query,values)

    connection.commit()

except mysql.connector.Error as err:
    print(f"MySQL error:{err}")

finally:
    if 'cursor' in locals():
        cursor.close()

    if 'connection' in locals() and connection.is_connected():
        connection.close()

print(f"Track'{track_data['Track Name']} by {track_data['Artist']} inserted into database.")



