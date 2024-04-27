import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import requests
import imdb
import wolframalpha

from decouple import config
from datetime import datetime
from conversation import random_text
from random import choice
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, get_news, weather_forecast

engine = pyttsx3.init("sapi5")
engine.setProperty("volume", 1.5)
engine.setProperty("rate", 200)  # Speed
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

user = config("USER")
hostname = config("BOT")


def speak(text):
  engine.say(text)
  engine.runAndWait()


def greet_me():
  hour = datetime.now().hour
  if (hour >= 4) and (hour < 12):
    speak(f"Good morning {user}")
  elif (hour >= 12) and (hour <= 16):
    speak(f"Good afternoon {user}")
  elif (hour >= 16) and (hour < 19):
    speak(f"Good evening {user}")
  speak(f"Anything I can do?")
  
listening = False
def start_listening():
  global listening
  listening = True
  print("Listening")

def pause_listening():
  global listening
  listening = False
  print("Listening Stopped")

# keyboard.add_hotkey("ctrl+alt+p", pause_listening)
# keyboard.add_hotkey("ctrl+alt+l", start_listening)


def take_command():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening ...")
    r.pause_threshold = 1
    audio = r.listen(source)

  try:
    print("Recognizing ...")

    queri = r.recognize_google(audio, language="en-us")
    print(queri)
    print(queri)
    if not "stop" in queri or "exit" in queri or "cancel" in queri or "it's okay" in queri:
      speak(choice(random_text))
    else:
      hour = datetime.now().hour
      if hour >= 21 and hour < 6:
        speak("Good night boss, take care!")
      else:
        speak("Have a good day sir!")
      exit()

  except Exception:
    speak("Sorry didn't grab that. Could you come again?")
    queri = "None"
  return queri


if __name__ == '__main__':
  greet_me()
  while True:
    if not listening:
      query = take_command().lower()
      if "how are you" in query:
        speak("I good boss. What about you?")

      elif "open command prompt" in query:
        speak("Opening command prompt")
        os.system("start cmd")

      elif "open camera" in query:
        speak("Opening camera sir")
        sp.run("start microsoft.windows.camera:", shell=True)

      elif "open notepad" in query:
        speak("Opening Notepad for you")
        notepad_path = "C:\\Users\\kelvi\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
        os.startfile(notepad_path)

      elif "ip address" in query:
        ip_address = find_my_ip()
        speak(f"Your IP address is {ip_address}")
        print(f"Your IP address is {ip_address}")

      elif "open youtube" in query:
        speak("What do you want to play sir?")
        video = take_command().lower()
        youtube(video)

      elif "open google" in query:
        speak("What would you like to search sir?")
        query = take_command().lower()
        search_on_google(query)

      elif "wikipedia" in query:
        speak("What would you like to search on wikipedia sir?")
        search = take_command().lower()
        results = search_on_wikipedia(search)
        speak(f"According to Wikipedia, {results}")
        speak("I have printed the results for as well.")
        print(results)

      elif "give me news" in query:
        speak("I am reading out the latest headline from apple")
        speak(get_news())
        speak("I have printed a copy for you boss. You could check it out at your free time")
        print(*get_news(),sep="\n")

      elif "weather" in query:
        # speak("Tell me the name of your city")
        # city = input("Enter name of city: ")
        city = "Kasoa"
        speak(f"Getting weather report for {city}")
        weather, temperature, feels_like = weather_forecast(city)
        speak(f"The current temperature is {temperature}, but feel like {feels_like}")
        speak(f"Also the weather report talks about {weather}")
        print(f"Description: {weather} \n Temperature: {temperature} \n Feels like: {feels_like}")

      elif "movie" in query:
        movies_db = imdb.IMDb()
        speak("Tell me the movie name")
        text = take_command().lower() 
        movies = movies_db.search_movie(text)
        speak(f"Searching for {text}")
        speak("I found these")
        for movie in movies:
          title = movie["title"]
          year = movie["year"]
          # speak(f"{title} - {year}")
          info = movie.getID()
          movie_info = movies_db.get_movie(info)
          rating = movie_info["rating"]
          cast = movie_info["cast"]
          actor = cast[0:5]
          plot = movie_info.get("plot outline", "plot summary not available")
          print(f"{title} was released in {year} has imdb ratings of {rating} . It has a cast of {actor}. The plot summary is {plot}")
          speak(f"{title} was released in {year} has imdb ratings of {rating}. The plot summary is {plot}")
          break
      
      elif "calculate" in query:
        app_id = "PU6A5L-KUT9EU9A7Y"
        client = wolframalpha.Client(app_id)
        ind = query.lower().split().index("calculate")
        text = query.split()[ind +1:]
        result = client.query(" ".join(text))
        try:
          ans = next(result.results).text
          print(f"The answer is {ans}")
          speak(f"The answer is {ans}")
        except StopIteration:
          speak("I couldn't find that. Please try again")

      elif "what is" in query or "who is" in query or "which is" in query:
        app_id = "PU6A5L-KUT9EU9A7Y"
        client = wolframalpha.Client(app_id)
        try:
          ind = query.lower().index("what is") if "what is" in query.lower() else \
          query.lower().index("who is") if "who is" in query.lower() else \
          query.lower().index("which is") if "which is" in query.lower() else None
          
          if ind is not None:
            text = query.split()[ind + 2:]
            result = client.query(" ".join(text))
            ans = next(result.results).text
            print(f"The answer is {ans}")
            speak(f"The answer is {ans}")
          else:
            speak("I couldn't find that.")

        except StopIteration:
          speak("I couldn't find that. Please try again")

          