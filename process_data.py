import sqlite3
import json_helper

def process_data():
    
    # Connecting to the database  
    connection = sqlite3.connect("Databases.db") 
    cur = connection.cursor()

    """Get top keywords and their occurence"""
    sql_query_1 = """
                select top_keyword_one, COUNT(top_keyword_one) AS MOST_FREQUENT
                from ArticleData
                GROUP BY top_keyword_one
                ORDER BY COUNT(top_keyword_one) DESC
                """    
    cur.execute(sql_query_1)
    data = cur.fetchall()
    keywords = {}
    for tup in data:
        keywords[tup[0]] = keywords.get(tup[0], 0) + tup[1]

    sql_query_2 = """
                select top_keyword_two, COUNT(top_keyword_two) AS MOST_FREQUENT
                from ArticleData
                GROUP BY top_keyword_two
                ORDER BY COUNT(top_keyword_two) DESC
                """
    cur.execute(sql_query_2)
    data = cur.fetchall()
    for tup in data:
        keywords[tup[0]] = keywords.get(tup[0], 0) + tup[1]

    keywords = sorted(list(keywords.items()), key=lambda tup:tup[1], reverse=True)[:10]
    

    f = open("keywords.csv", "w")
    f.write("keyword,occurance\n")

    for words in keywords:
        f.write(f'{words[0]},{words[1]}')
        f.write("\n")

    
    """Get lengths of all playlists and their occurence"""
    playlist_lengths = {"0-20":0,"21-40":0,"41-60":0,"61-80":0,"81-100":0,"100+":0}

    sql_query_3 = """
                select playlist_size from PLAYLISTS
                """
    
    cur.execute(sql_query_3)
    data = cur.fetchall()

    for tup in data:
        amount = tup[0]
        if amount > 100:
            playlist_lengths['100+'] += 1
        elif amount > 80:
            playlist_lengths['81-100'] += 1
        elif amount > 60:
            playlist_lengths['61-80'] += 1
        elif amount > 40:
            playlist_lengths['41-60'] += 1
        elif amount > 20:
            playlist_lengths['21-40'] += 1
        else:
            playlist_lengths['0-20'] += 1

    playlist_lengths = list(playlist_lengths.items())

    f = open("playlist_lengths.csv", "w")
    f.write("playlist_range,total\n")

    for playlist_range in playlist_lengths:
        f.write(f'{playlist_range[0]},{playlist_range[1]}')
        f.write("\n")

    """for word in playlist_lengths:
        
    Processings the top features among the songs in the playlists
    JOIN Tracks and TrackFeatures on song_name 

    for i in range (max in column playlists)
    SELECT * WHERE PLAYLIST_ID = 1 
    FIND MOST COMMON FEATURE
    Add to dictionary: feature: 1
    then next playlist
    FIND MOST COMMON FEATURE: 2
    Should end up with {genre1: 1, genre2: 3, genre3: 4} etc.
    Extra Credit: Processing the top songs in all of the playlists
    """

    print("Processed data")

def main():
    process_data()

if __name__ == '__main__':
    main()