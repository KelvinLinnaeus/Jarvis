import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

email = "",
password = ""

def find_my_ip():
  ip_address = requests.get('https://api.ipify.org?format=json').json()
  return ip_address["ip"]

def search_on_wikipedia(query):
  results = wikipedia.summary(query, sentences = 2)
  return results

def search_on_google(query):
  kit.search(query)

def youtube(video):
  kit.playonyt(video)

  # Note: Skipped email send and receive messages 45-52
  
def get_news():
  news_headline =[]
  results = requests.get(f"https://newsapi.org/v2/everything?q=apple&from=2024-04-24&to=2024-04-24&sortBy=popularity&apiKey=08aaddd3577f4816998b5948a486b75b").json()
  articles = results["articles"]
  for article in articles:
    news_headline.append(article["title"])
  return news_headline[:6]