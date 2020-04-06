import sqlite3

def delete_table(table_name):
    """Delete the passed in table in the database."""
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor()

    # Delete table
    cur.execute("DROP table " + table_name)

    print("Deleted table: " + table_name)
    connection.commit() 
    connection.close() 

def main():
    table_name = "Playlists"
    delete_table(table_name)


if __name__ == '__main__':
    main()