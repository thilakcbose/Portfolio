import re
import pandas as pd 
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy 
import matplotlib.pyplot as plt 
import mysql.connector

# Setting up spotify API credentials
sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(
    client_id = '20939a74b3c14b128a4571d43818af66',
    client_secret = 'e82b6a89882c4b40abf0d8a721cbbcf4'
 ))

 #MYSQL DATABASE CONNCETION

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'thilks',
    'database':'spotify_db'
    
 }
 #Connect to the database

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

#Track URL
track_URL = "https://open.spotify.com/track/5lmgII1wyydsuqXEOvzpSy"

#Extractin ID from URL
track_id = re.search(r'track/([a-zA-Z0-9]+)',track_URL).group(1)

# Fetch track details
track = sp.track(track_id)

print(track.keys())

print(track['href'])

#Extrack Metadata
track_data = {
    'Track Name': track['name'],
    'Artist' : track['artists'][0]['name'],
    'Album' : track['album']['name'],
    'Track Number': track['track_number'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

# Insert data into MySQL

insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, track_number, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.execute(
    insert_query,
    (
     track_data['Track Name'],
     track_data['Artist'],
     track_data['Album'],
     track_data['Track Number'],
     track_data['Duration (minutes)']
    )
)

connection.commit()

print(f"Track'{track_data['Track Name']} by {track_data['Artist']} inserted into database.")

#closing connection
cursor.close()
connection.close()