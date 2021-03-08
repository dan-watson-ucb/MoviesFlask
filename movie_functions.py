from api_info import key
import json
import requests
import boto3
from bs4 import BeautifulSoup
from selenium import webdriver


def find_movies(movie_title, api_key=key):
    pull = f'https://api.nytimes.com/svc/movies/v2/reviews/search.json?query={movie_title}&api-key={api_key}'
    r = requests.get(pull)
    output_json = r.json()
    return output_json


def pull_review(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='/home/dan/PycharmProjects/MoviesFlask/chromedriver', options=options)
    driver.get(url)
    page_text = BeautifulSoup(driver.page_source)
    return page_text


def get_review_text(content):
    ps = content.find_all('p')
    lens = []
    for p in ps:
        lens.append(len(p.text))
    longest_p = lens.index(max(lens))
    review_text = ps[longest_p].text
    return review_text

def get_score(review_text):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    output = comprehend.detect_sentiment(Text=review_text, LanguageCode='en')
    sentiment = output['Sentiment']
    positive = output['SentimentScore']['Positive']
    neutral = output['SentimentScore']['Neutral']
    negative = output['SentimentScore']['Negative']
    mixed = output['SentimentScore']['Mixed']
    return sentiment, positive, neutral, negative, mixed
