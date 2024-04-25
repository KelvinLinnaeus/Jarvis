import pyttsx3
import speech_recognition as sr

from decouple import config
from datetime import datetime
from conversation import random_text
from random import choice

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
  if (hour >= 6) and (hour < 12):
    speak(f"Good morning {user}")
  elif (hour >= 12) and (hour <= 16):
    speak(f"Good afternoon {user}")
  elif (hour >= 16) and (hour < 19):
    speak(f"Good evening {user}")
  speak(f"It's {hostname}. How can I be of assist {user}")


def take_command():
  r = sr.Recognizer()
  with sr.Microphone as source:
    print("Listening ...")
    r.pause_threshold = 1
    audio = r.listen(source)

  try:
    print("Recognizing ...")
    query = r.recognize_google_cloud(audio, language="en-in")
    print(query)
    if not "stop" in query or "exit" in query:
      speak(choice(random_text))
    else:
      hour = datetime.now().hour
      if hour >= 21 and hour < 6:
        speak("Good night boss, take care!")
      else:
        speak("Have a good day sir!")
      exit()

  except Exception:
    speak("Sorry didn't grab that boss. Could you come again?")
    query = "None"
  return query


if __name__ == '__main__':
  # greet_me()
  while True:
    query = take_command().lower()
    if "how are you" in query:
      speak("I good boss. What about you?")
