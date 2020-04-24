import requests
import sqlite3
import json_helper

API_KEY = 'f3761bb4e572493c9f7e9f2d3e9afe57'
URL = "http://newsapi.org/v2/top-headlines"
CATEGORIES = ['business', 'entertainment', 'health',
              'science', 'sports', 'technology']

def create_database():
    """Create database for Google News API."""

    # Create Google News database
    conn = sqlite3.connect("Databases.db")
    cur = conn.cursor()
    sql_command = """
                    CREATE TABLE IF NOT EXISTS ArticleData 
                        (article_id INTEGER PRIMARY KEY,
                         article_title TEXT UNIQUE,  
                         article_category TEXT, 
                         top_keyword_one TEXT,
                         top_keyword_two TEXT);
                  """
    cur.execute(sql_command) 

    conn.close()

def get_google_news_data():
    # Using news_category_index
    print("Getting Google News Top Articles")
    cache_dict = json_helper.read_cache()
    news_category_index = cache_dict["news_category_index"]
    category = CATEGORIES[news_category_index]
    print("Category: " + category)

    # Get 10 top articles per category
    params = {'apiKey': API_KEY,
              'country': 'us',
              'category': category,
              'totalResults':20}
    response = requests.get(URL, params)
    json_response = response.json()

    articles = json_response['articles']

    # Only get data for 20 articles
    connection = sqlite3.connect("Databases.db") 
    top_keyword = ""
    count = 0
    for article in articles:
        if count == 20:
            break
        article_data = get_article_data(article, category)
        if article_data == None:
            continue
        print(article_data)

        cur = connection.cursor()
        top_keyword = article_data[2]
        
        # Insert article data into database
        sql_command = """
                        INSERT OR IGNORE INTO ArticleData 
                            (article_title, 
                             article_category, 
                             top_keyword_one,
                             top_keyword_two) 
                        values (?,?,?,?)
                    """
        cur.execute(sql_command, article_data) 

        count += 1
    
    # Cache to top keyword for each category
    cache_dict = json_helper.read_cache()
    category_top_keywords = cache_dict.get("category_top_keywords", [])
    print("top keyword: " + top_keyword)
    if top_keyword not in category_top_keywords:
        category_top_keywords.append(top_keyword)
    else:
        category_top_keywords.append("virus")
    cache_dict["category_top_keywords"] = category_top_keywords
    json_helper.write_cache(cache_dict) 

    connection.commit()
    connection.close()

def get_article_data(article, category):
    """Return a list representing the data for a row in the database."""
    article_desc = article['description']
    if article_desc == None or article_desc == '':
        return None

    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    wordcount = {}

    for word in article_desc.lower().split():
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

    keywords_dict = {}
    for tup in sorted(wordcount.items(), key=lambda kv: kv[1], reverse=True)[:10]:
        keywords_dict[tup[0]] = tup[1]

    keywords = list(keywords_dict.items())

    # Get article database data
    article_title = article['title']
    top_keyword_one = keywords[0][0]
    top_keyword_two = keywords[1][0]

    return [article_title,
            category,
            top_keyword_one,
            top_keyword_two]


def main():
    # Cache country index
    cache_dict = json_helper.read_cache()
    cache_dict["news_category_index"] = cache_dict.get("news_category_index", -1) + 1
    json_helper.write_cache(cache_dict) 

    if cache_dict["news_category_index"] >= len(CATEGORIES):
        print("No more categories to pull articles from.")
        return

    create_database()
    get_google_news_data()

if __name__ == '__main__':
    main()