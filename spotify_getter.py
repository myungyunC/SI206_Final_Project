import json
import sqlite3
from spotify import Spotify

# Authorization information from Spotify Developer account
CLIENT_ID = "4ca6dc22b6e944d19157c2186c9626ed"
CLIENT_SECRET = "bb2280621c164b7c9b9857571d1ced62"

def get_news_keywords():
    """Retrieve keywords from table created from data from Google News API"""

    # Connect to SQL database with News data

    # Retrieve top keywords

    # Cache

    return ["Coronavirus", "China", "Masks", "Peak"]

def create_databases():
    """Create database for Playlists and Tracks."""
    ###
    #   We'll use the playlist_id as the shared key. Tracks table will have
    #   the playlist_id as well. (for Tracks, playlist_id is a FOREIGN KEY)
    #   
    #   Use JOIN!
    #   maybe a table for artists using join with tracks table and artists?
    ###

    # Create Playlist database
    conn = sqlite3.connect("SpotifyPlaylists.db")
    cur = conn.cursor
    sql_command = """CREATE TABLE IF NOT EXISTS Playlists (playlist_id INTEGER PRIMARY KEY,
                                                           playlist_name TEXT UNIQUE,  
                                                           playlist_desc TEXT,  
                                                           playlist_uri TEXT UNIQUE);"""
    cur.execute(sql_command) 
    conn.close()

    # Create Tracks databse
    conn = sqlite3.connect("SpotifyTracks.db")
    cur = conn.cursor
    sql_command = """CREATE TABLE IF NOT EXISTS Tracks (track_id INTEGER PRIMARY KEY,
                                                        playlist_id INTEGER FOREIGN KEY,
                                                        track_name TEXT,
                                                        track_artist TEXT,  
                                                        track_uri TEXT UNIQUE);"""
    cur.execute(sql_command) 
    conn.close()

def get_spotify_data(keywords):
    """Master function get retrieve data from Spotify."""
    # Create instance of Spotify class
    SpotifyMaster = Spotify(CLIENT_ID, CLIENT_SECRET)

    # Pull data for each keyword
    for keyword in keywords:
    print(json.dumps(SpotifyMaster.search("dance", "playlist")))
    # write_to_table()

def write_playlists_to_table():
    """Write returned data to table"""
    # connecting to the database  
    connection = sqlite3.connect("spotifyPlaylists.db") 
    cur = connection.cursor() 
    
    # SQL command to create a table in the database 
    sql_command = """CREATE TABLE IF NOT EXISTS Playlists (playlist_id INTEGER PRIMARY KEY,
                                                           playlist_name TEXT,  
                                                           playlist_desc TEXT,  
                                                           playlist_uri TEXT UNIQUE);"""
    cur.execute(sql_command) 


    

    cur.execute(sql_command) 

    connection.commit() 
    connection.close() 


def main():
    # If first time running, then cache top keywords
    keywords = get_news_keywords()
    create_databases()
    # get_spotify_data(keywords)


if __name__ == '__main__':
    main()