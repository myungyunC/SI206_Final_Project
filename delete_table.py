import sqlite3
import json_helper

def delete_table(table_name):
    """Delete the passed in table in the database."""
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor()

    # Delete table
    cur.execute("DROP table IF EXISTS " + table_name)

    print("Deleted table: " + table_name)
    connection.commit() 
    connection.close() 

def main():
    # Delete tables
    delete_table("Playlists")
    delete_table("Tracks")
    delete_table("TrackFeatures")
    delete_table("ArticleData")

    # Clear JSON data
    cache_dict = json_helper.read_cache()
    cache_dict = {}
    json_helper.write_cache(cache_dict)


if __name__ == '__main__':
    main()