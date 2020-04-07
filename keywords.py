import requests
import sqlite3
import json_helper

totalResults = 20

API_KEY = 'f3761bb4e572493c9f7e9f2d3e9afe57'
URL = "http://newsapi.org/v2/top-headlines"
COUNTRIES = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca',
             'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr',
             'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in',
             'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my',
             'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro',
             'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th',
             'tr', 'tw', 'ua', 'us', 've', 'za']

PARAMS = {'apiKey': API_KEY, 'country': 'us', 'totalResults':totalResults}


def get_top_keywords():
    lst = []
    response = requests.get(URL, PARAMS)

    for article in response.json()['articles']:
        lst.append(article['description'])

    words = (' ').join(lst)

    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    wordcount = {}

    for word in words.lower().split():
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        word = word.replace('"',"")
        word = word.replace("…","")
        word = word.replace("'","")
        word = word.replace("’","")
        word = word.replace("/","")
        word = word.replace("(","")
        word = word.replace(")","")
        if word not in stopwords:
            wordcount[word] = wordcount.get(word, 0) + 1

    keywords = {}

    for tup in sorted(wordcount.items(), key=lambda kv: kv[1], reverse=True)[:totalResults]:
        keywords[tup[0]] = tup[1]

    print(keywords)
    return keywords

def create_database():
    """Create database for Google News API."""

    # Create Google News database
    conn = sqlite3.connect("Databases.db")
    cur = conn.cursor()
    sql_command = """
                    CREATE TABLE IF NOT EXISTS ArticleData 
                        (article_id INTEGER PRIMARY KEY,
                         article_title TEXT UNIQUE,  
                         article_country TEXT, 
                         top_keyword_one TEXT,
                         top_keyword_two TEXT);
                  """
    cur.execute(sql_command) 

    conn.close()

def get_google_news_data():
    # Using country_index
    print("Getting Google News Top Articles")
    cache_dict = json_helper.read_cache()
    country_index = cache_dict["country_index"]
    country = COUNTRIES[country_index]
    print("Country: " + country)

    # Get 10 top articles per country

    # Parse data for database and store data

def main():
    # Cache country index
    cache_dict = json_helper.read_cache()
    cache_dict["country_index"] = cache_dict.get("country_index", -1) + 1
    json_helper.write_cache(cache_dict) 

    create_database()
    get_google_news_data()

if __name__ == '__main__':
    main()