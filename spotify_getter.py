import json
import os
import sqlite3
import json_helper
from spotify import Spotify

# Authorization information from Spotify Developer account
CLIENT_ID = "4ca6dc22b6e944d19157c2186c9626ed"
CLIENT_SECRET = "bb2280621c164b7c9b9857571d1ced62"

def get_news_keywords():
    """Retrieve keywords from table created from data from Google News API"""

    # Get list of top keywords from JSON

    return ["Coronavirus", "China", "Trump", "Economy"]


def create_databases():
    """Create database for Playlists and Tracks."""
    ###
    #   We'll use the playlist_id as the shared key. Tracks table will have
    #   the playlist_id as well. (for Tracks, playlist_id is a FOREIGN KEY)
    #   
    #   Use JOIN!
    #   maybe a table for artists using join with tracks table and artists?
    #   
    #   create a table using playlist owners with user information
    #
    #   data to represent:  most frequent key words
    #                       most popular track features amongst playlists
    #                       frequent songs in playlists
    ###

    # Create Playlist database
    conn = sqlite3.connect("Databases.db")
    cur = conn.cursor()
    sql_command = """
                    CREATE TABLE IF NOT EXISTS Playlists 
                        (playlist_id INTEGER PRIMARY KEY,
                         playlist_name TEXT UNIQUE,  
                         playlist_owner TEXT, 
                         playlist_uri TEXT UNIQUE);
                  """
    cur.execute(sql_command) 

    # Create Tracks databse
    sql_command = """
                    CREATE TABLE IF NOT EXISTS Tracks 
                        (track_id INTEGER PRIMARY KEY,
                         track_name TEXT,
                         track_artist TEXT,
                         playlist_id INTEGER,
                         FOREIGN KEY(playlist_id) REFERENCES Playlists(playlist_id));
                  """
    cur.execute(sql_command) 
    conn.close()

def get_spotify_data(keywords, num_playlists):
    """Master function get retrieve data from Spotify."""
    # Create instance of Spotify class
    SpotifyMaster = Spotify(CLIENT_ID, CLIENT_SECRET)

    # Only retrieve playlists if not at num_playlists
    playlist_table_size = return_table_len("Playlists")
    if playlist_table_size != num_playlists:
        # Pull playlist data a keyword
        cache_dict = json_helper.read_cache()
        keyword_index = cache_dict["keyword_index"]
        keyword = keywords[keyword_index]
        print("Keyword: " + keyword)

        # # Get playlists
        json_result = SpotifyMaster.search(keyword, "playlist")
        playlists = json_result["playlists"]["items"]
        
        # Write playlists to database
        write_playlists_to_database(SpotifyMaster, playlists)
        playlist_table_size = return_table_len("Playlists")
        print("Playlist table size: " + str(playlist_table_size))
        return
    
    # Otherwise, start getting tracks
    print("get Spotify track data")

def write_playlists_to_database(SpotifyMaster, playlists):
    """Write returned data to table"""
    print("Number of playlists: " + str(len(playlists)))
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor() 
    
    # Write each playlist into the database
    for playlist in playlists:
        # Get necessary playlist metadata
        name = playlist["name"]
        owner = playlist["owner"]["id"]
        uri = playlist["uri"]
        playlist_data = [name, owner, uri]

        # SQL command to create a table in the database 
        sql_command = """
                        INSERT OR IGNORE INTO Playlists 
                            (playlist_name, 
                            playlist_owner, 
                            playlist_uri) 
                        values (?,?,?)
                    """
        cur.execute(sql_command, playlist_data) 
        connection.commit() 
    connection.close()

def write_tracks_to_database(SpotifyMaster, tracks):
    """Write tracks to the SQLite database."""
    print("Number of tracks: " + str(len(tracks)))

    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor() 
    
    # Write each playlist into the database
    # for playlist in playlists:
    playlist = playlists[0]
    # Get necessary playlist metadata
    name = playlist["name"]
    owner = playlist["owner"]["id"]
    uri = playlist["uri"]
    playlist_data = [name, owner, uri]

    # SQL command to create a table in the database 
    sql_command = """
                    INSERT OR IGNORE INTO Playlists 
                        (playlist_name, 
                         playlist_owner, 
                         playlist_uri) 
                    values (?,?,?)
                  """
    cur.execute(sql_command, playlist_data) 

    # List of 20 track ids in the playlist
    # track_ids = SpotifyMaster.get_tracks_from_playlist(playlist["href"])
    # print("Number of tracks: " + str(len(track_ids)))
    # write_tracks_to_database(SpotifyMaster, track_ids)

    connection.commit() 
    connection.close()


def return_table_len(table_name):
    """Returns the number of elements in the passed in table."""
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor() 

    # SQL command to create a table in the database 
    sql_command = """SELECT * FROM """
    sql_command = sql_command + table_name + ";"
    cur.execute(sql_command)
    results = cur.fetchall()

    connection.commit() 
    connection.close() 
    print("Length of TABLE(" + table_name + "): " + str(len(results)))
    return len(results)

def main():
    # If first time running, then cache top keywords
    keywords = get_news_keywords()
    num_playlists = len(keywords) * 20
    print("Total number of expected playlists: " + str(num_playlists))

    # Cache keyword index
    cache_dict = json_helper.read_cache()
    cache_dict["keyword_index"] = cache_dict.get("keyword_index", -1) + 1
    json_helper.write_cache(cache_dict) 

    # Create JSON file if needed
    #
    # JSON file will be used to make sure only 20 items
    # are pulled from an API into the respective table in
    # the databse per code execution
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = dir_path + '/' + "helpers.json"
    os.system("touch " + cache_path)

    # Create Databases
    create_databases()

    # Get Spotify 
    get_spotify_data(keywords, num_playlists)


if __name__ == '__main__':
    main()