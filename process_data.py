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


    """Get most common feature of each playlist"""
    sql_query_4 = """SELECT MAX(playlist_id) FROM Tracks"""
    cur.execute(sql_query_4)
    data = cur.fetchall()
    max_playlists = data[0][0]
    
    features = {}

    for i in range(1, max_playlists + 1):
        sql_query_5 = f"""
                SELECT Tracks.playlist_id, Tracks.track_name, TrackFeatures.first_feature
                FROM Tracks JOIN TrackFeatures ON Tracks.track_name = TrackFeatures.track_name 
                WHERE playlist_id = {i}"""
        cur.execute(sql_query_5)
        data = cur.fetchall()
        current_playlist_features = {}
        for tup in data:
            feature = tup[2]
            current_playlist_features[feature] = current_playlist_features.get(feature, 0) + 1
        most_popular_feature = sorted(list(current_playlist_features.items()),key=lambda tup:tup[1],reverse=True)[0][0]
        features[most_popular_feature] = features.get(most_popular_feature, 0) + 1

    features_list = sorted(list(features.items()), key=lambda tup:tup[1], reverse=True)

    f = open("features.csv", "w")
    f.write("feature,total\n")
    for feature in features_list:
        f.write(f'{feature[0]},{feature[1]}')
        f.write("\n")

    print("Processed data")

def main():
    process_data()

if __name__ == '__main__':
    main()