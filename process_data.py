import sqlite3
import json_helper

def process_data():
    """Delete the passed in table in the database."""
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor()

    print("Processed data")

def main():
    process_data()

if __name__ == '__main__':
    main()