'''
module gathers the news articles

the module utilises the newsapi to search the web for covid news
articles to pass onto another module
'''
import json
import requests
import logging
logging.basicConfig(filename="logfile.log",level=logging.DEBUG)


with open("config.json", encoding="latin-1") as f:
    data = json.load(f)
key = data["News_api_key"]
if not key:
    logging.warning("No NewsAPI key detected")


def news_api_request(covid_terms="Covid, COVID-19, coronavirus"):
    '''
    function fetches news data

    fetches news data from the news api and converts them into
    a json format
    '''

    url = f"""https://newsapi.org/v2/everything?q={covid_terms}&sortBy=
        publishedAt&language=en&apikey={key}"""
    try:
        articles = requests.get(url).json()
        articles = articles["articles"]
        logging.info("api request complete - articles found")
        return articles
    except:
        logging.error("news api request error, check api key.")



def update_news():
    '''
    function filters the news request for the required data

    filters the news request for headlines and descriptions,
    saves them to a dictionary and returns dictionary
    '''
    try:
        articles = news_api_request()
        news = {}
        for acc, article_data in enumerate(articles):
            news.update({article_data["title"]: article_data["description"]})
        return news
