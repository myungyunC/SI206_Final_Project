import sqlite3

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
    delete_table("Playlists")
    delete_table("Tracks")
    delete_table("TrackFeatures")
    delete_table("ArticleData")


if __name__ == '__main__':
    main()