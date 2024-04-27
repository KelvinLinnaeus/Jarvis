import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import requests

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