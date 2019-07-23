from googlesearch import search_news
from newspaper import Article

def download_articles(keyword, query_append="",topdomain="co.in", num_articles=5, rest=2):

    # If there's something to append to our query, append it.
    if query_append:
        keyword = keyword + " " + query_append

    # Builds a newspaper of articles from our keyword search.
    newsPaper = download(keyword, topdomain, num_articles, rest)

    return newsPaper

def download(keyword, topdomain, num_articles, rest):

    # Empty newspaper dictionary to hold downloaded articles
    newsPaper = {
        "articles": []
    }

    for result in search_news(query=keyword, tld=topdomain, lang='en', num=10, stop=num_articles, pause=rest):
        try:
            article = {}
            news = Article(result)
            news.download()
            news.parse()
            news.nlp()
            article['link'] = result
            article['title'] = news.title
            article['firm'] = keyword.lower().split()
            article['text'] = news.text
            article['keywords'] = news.keywords
            if news.publish_date:
                article['published'] = news.publish_date.isoformat()
            else:
                article['published'] = news.publish_date
            article['author'] = news.authors
            print(result)
            print(news.title)
            newsPaper['articles'].append(article)
        except:
            print(result + " \nError: could not be downloaded.")
        print("------------------------------------------------------------")
    return newsPaper

def mark_relevancy(newsPaper):
    # Adds Relevancy Score by comparing our extracted keywords with the firm name.
    # 2 - Exact match between firm name and article keywords
    # 1 - Partial match between firm name and article keywords
    # 0 - No match between firm name and article keywords
    for article in newsPaper['articles']:
        article['relevancy'] = filter(article['firm'], article['keywords'])
    return newsPaper

def filter(term, search_list):
    print("Searching for: ", term)
    print("From: ", search_list)

    relevancy = 0

    key_exact = lambda x: x in search_list
    key_contains = lambda x: subkey_contains(x)
    subkey_contains = lambda y: any(y in s for s in search_list)
    if all(map(key_exact, term)):
        print("This is an exact match to the search phrase")
        relevancy = 2
    elif any(map(key_contains, term)):
        print("This is a partial match to the search phrase")
        relevancy = 1
    else:
        print("This does not match the search phrase")
    print("------------------------------------------------------------")
    return relevancy
