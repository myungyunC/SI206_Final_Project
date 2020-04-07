import json
import os
import sqlite3
import json_helper
from spotify import Spotify

# for run in {1..10}; do command; done
# Authorization information from Spotify Developer account
CLIENT_ID = "4ca6dc22b6e944d19157c2186c9626ed"
CLIENT_SECRET = "bb2280621c164b7c9b9857571d1ced62"

def get_news_keywords():
    """Retrieve keywords from table created from data from Google News API"""
    # Get list of top keywords from JSON
    cache_dict = json_helper.read_cache()
    category_top_keywords = cache_dict.get("category_top_keywords",
                                           ["Coronavirus", "China", "Trump", "Economy"])

    return category_top_keywords


def create_databases():
    """Create database for Playlists and Tracks."""
    ###
    #   We'll use the playlist_id as the shared key. Tracks table will have
    #   the playlist_id as well. (for Tracks, playlist_id is a FOREIGN KEY)
    #   
    #   Use JOIN!
    #   join playists and tracks to have (track_name, playlist_name)
    #   join tracks and track_features to have (track_name, top_feature)
    #   
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
                         playlist_desc TEXT,
                         playlist_href TEXT UNIQUE);
                  """
    cur.execute(sql_command) 

    # Create Tracks databse
    sql_command = """
                    CREATE TABLE IF NOT EXISTS Tracks 
                        (track_id INTEGER PRIMARY KEY,
                         track_name TEXT UNIQUE,
                         track_artist TEXT,
                         playlist_href TEXT,
                         FOREIGN KEY(playlist_href) REFERENCES Playlists(playlist_href));
                  """
    cur.execute(sql_command) 

    # Create TrackFeatures databse
    sql_command = """
                    CREATE TABLE IF NOT EXISTS TrackFeatures 
                        (feature_id INTEGER PRIMARY KEY,
                         track_name INTEGER UNIQUE,
                         first_feature TEXT,
                         first_feature_value REAL,
                         second_feature TEXT,
                         second_feature_value REAL,
                         FOREIGN KEY(track_name) REFERENCES Playlists(track_name));
                  """
    cur.execute(sql_command) 

    conn.close()

def get_spotify_data(keywords, num_playlists):
    """Master function get retrieve data from Spotify."""
    # Create instance of Spotify class
    SpotifyMaster = Spotify(CLIENT_ID, CLIENT_SECRET)

    # Only retrieve playlists if not at num_playlists
    playlist_table_size = return_table_len("Playlists")
    if playlist_table_size < num_playlists - 10:
        # Pull playlist data a keyword
        print("Getting Spotify playlists")
        cache_dict = json_helper.read_cache()
        keyword_index = cache_dict["keyword_index"]
        keyword = keywords[keyword_index]
        print("Keyword: " + keyword)

        # Get playlists
        json_result = SpotifyMaster.search(keyword, "playlist")
        playlists = json_result["playlists"]["items"]
        
        # Write playlists to database
        write_playlists_to_database(SpotifyMaster, playlists)
        playlist_table_size = return_table_len("Playlists")
        print("Playlist table size: " + str(playlist_table_size))

        return
    
    # Otherwise, start getting tracks until reach limit
    tracks_table_size = return_table_len("Tracks")
    if tracks_table_size != num_playlists * 10:
        print("Getting Spotify Tracks")

        # Get the correct playlist href and increment the index counter
        cache_dict = json_helper.read_cache()
        cache_dict["playlist_href_index"] = cache_dict.get("playlist_href_index", -1) + 1
        playlist_href_index = cache_dict["playlist_href_index"]
        json_helper.write_cache(cache_dict)
        playlist_href = cache_dict["playlist_hrefs"][playlist_href_index]

        # Get track ids from the playlist and write to database
        track_ids = SpotifyMaster.get_tracks_from_playlist(playlist_href)
        write_tracks_and_features_to_database(SpotifyMaster, track_ids, playlist_href)
        print("Tracks table size: " + str(tracks_table_size))
        
        return
    
    # Done getting data, JOIN time.
    print("Done retrieving Spotify playlists and track data.")

def write_playlists_to_database(SpotifyMaster, playlists):
    """Write returned data to table"""
    print("Number of playlists: " + str(len(playlists)))
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor()

    # Cache playlist href to get tracks later
    cache_dict = json_helper.read_cache()
    playlist_hrefs = cache_dict.get("playlist_hrefs", [])
    
    # Write each playlist into the database
    for playlist in playlists:
        # Get necessary playlist metadata
        name = playlist["name"]
        owner = playlist["owner"]["id"]
        desc = playlist["description"]
        href = playlist["href"]
        playlist_data = [name, owner, desc, href]

        # Insert playlist into database
        sql_command = """
                        INSERT OR IGNORE INTO Playlists 
                            (playlist_name, 
                             playlist_owner, 
                             playlist_desc,
                             playlist_href) 
                        values (?,?,?,?)
                    """
        cur.execute(sql_command, playlist_data) 

        # Append playlist href to list of hrefs
        playlist_hrefs.append(href)

    cache_dict["playlist_hrefs"] = playlist_hrefs
    json_helper.write_cache(cache_dict)

    connection.commit()
    connection.close()

def get_top_two_features(track_features):
    """Given the track features response, returns top two and values."""
    # Get features
    danceability = track_features.get("danceability", 0)
    energy = track_features.get("energy", 0)
    loudness = track_features.get("loudness", 0)
    speechiness = track_features.get("speechiness", 0)
    instrumentalness = track_features.get("instrumentalness", 0)
    liveness = track_features.get("liveness", 0)

    features_dict = {
        "danceability": danceability,
        "energy": energy,
        "loudness": loudness,
        "speechiness": speechiness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
    }

    # Sort by top values
    sorted_features = list(sorted(features_dict.items(),
                           key=lambda feature: feature[1],
                           reverse=True))
    top_two = [sorted_features[0][0], sorted_features[0][1], sorted_features[1][0], sorted_features[1][1]]
    return top_two

def write_tracks_and_features_to_database(SpotifyMaster, track_ids, playlist_href):
    """Write tracks to the SQLite database. 10 tracks and 10 track features"""
    print("Number of tracks: " + str(len(track_ids)))

    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor() 
    
    # Write each track and feature data into the database
    for track_id in track_ids:
        # Get necessary track metadata
        json_track_result = SpotifyMaster.get_track_data("track", track_id)
        name = json_track_result["name"]
        artist = json_track_result["artists"][0]["name"]
        track_data = [name, artist, playlist_href]

        # Insert track into databse
        sql_command = """
                        INSERT OR IGNORE INTO Tracks 
                            (track_name, 
                             track_artist, 
                             playlist_href) 
                        values (?,?,?)
                    """
        cur.execute(sql_command, track_data)

        # Get top track feature
        json_features_result = SpotifyMaster.get_track_data("features", track_id)
        features_data = [name] + get_top_two_features(json_features_result)

        # Insert track feature into databse
        sql_command = """
                        INSERT OR IGNORE INTO TrackFeatures 
                            (track_name, 
                             first_feature,
                             first_feature_value,
                             second_feature,
                             second_feature_value)
                        values (?,?,?,?,?)
                    """
        cur.execute(sql_command, features_data)

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