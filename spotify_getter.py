import json
import sqlite3
from spotify import Spotify

# Authorization information from Spotify Developer account
CLIENT_ID = "4ca6dc22b6e944d19157c2186c9626ed"
CLIENT_SECRET = "bb2280621c164b7c9b9857571d1ced62"

def get_news_keywords():
    """Retrieve keywords from table created from data from Google News API"""
    

def get_spotify_data():
    """Master function get retrieve data from Spotify."""
    SpotifyMaster = Spotify(CLIENT_ID, CLIENT_SECRET)
    print(json.dumps(SpotifyMaster.search("dance", "playlist")))
    # write_to_table()

def write_to_table():
    """Write returned data to table"""
    # connecting to the database  
    connection = sqlite3.connect("spotifyTable.db") 
    cur = connection.cursor() 
    
    # SQL command to create a table in the database 
    sql_command = """CREATE TABLE songs (song_title VARCHAR(30) PRIMARY KEY,  
                                         artist VARCHAR(20),  
                                         genre VARCHAR(30));"""
    cur.execute(sql_command) 
    
    # Insert songs into table
    sql_command = """INSERT INTO songs VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");"""
    cur.execute(sql_command) 

    connection.commit() 
    connection.close() 


def main():
    keywords = get_news_keywords()
    get_spotify_data()


if __name__ == '__main__':
    main()