import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import random
from datetime import date
import webbrowser as wb
import pyautogui as py
from time import sleep as z
from requests_html import HTMLSession
from datetime import datetime
import keyboard
from googletrans import Translator

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Greeting when ran
raven_greetings = [
    "at the ready boss",
    "greetings creator",
    "online and ready",
]
hello = random.choice(raven_greetings)

# This helps you know a command was received
raven_command_responses = [
    "right away boss",
    "will do boss",
    "will do",
    "sure thing boss",
    "executing now",
]
random_response = random.choice(raven_command_responses)

# Said after activation phrase
raven_active_phrases = [
    "What can I do for you",
    "Ready for input",
    "How can I help",
]
at_the_ready = random.choice(raven_active_phrases)

deactivation_phrases = [
    "returning to regular protocols",
    "let me know if you need anything",
]
deactivation = random.choice(deactivation_phrases)

today = date.today()

translater = Translator()

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source, phrase_time_limit=6, timeout=3600)
            command = "waiting"
            command = listener.recognize_google(voice)
            command = command.lower()

    except:
        pass
    return command


# Weather Web Scraper
s = HTMLSession()

# Currently set to my city, looking for a way to auto detect user city
query = "omaha"
url = f"https://www.google.com/search?q=weather+{query}"

r = s.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    },
)
temp = r.html.find("span#wob_tm", first=True).text
weather_desc = r.html.find("div.VQF4g", first=True).find("span#wob_dc", first=True).text
humidity = r.html.find("div.wtsRwe", first=True).find("span#wob_hm", first=True).text
wind_speed = r.html.find("div.wtsRwe", first=True).find("span#wob_ws", first=True).text

def time():
    now = datetime.now()
    time = now.strftime("%I:%M")
    talk("Current time is " + time)

def run_raven():
    talk(at_the_ready)
    command = take_command()

    # Searches youtube and plays the most relevant result
    if "play" in command:
        song = command.replace("play", "")
        talk("playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in command:
        time()

    # Reads wiki articles or runs a search
    elif "look up" in command:
        try:
            topic = command.replace("look up", "")
            info = wikipedia.summary(topic.strip(), 1)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk(
                "sorry boss. for some reason I didn't find any info on that. I'll run a Google search for you"
            )
            pywhatkit.search(topic.strip())
            pass

    elif "go to sleep" in command:
        talk("shutting down. see you later")
        stop_raven()

    elif "date" in command:
        talk(today)

    # These link opening commands are a bit complicated due to an issue with opening the wrong browser
    elif "open" in command:
        talk(random_response)
        website = command.replace("open", "")
        link = website.replace(" ", "") + ".com"
        wb.open("https://www.google.com")
        z(0.15)
        py.keyDown("ctrl")
        py.hotkey("l")
        z(0.15)
        py.keyUp("ctrl")
        z(0.15)
        py.write(link)
        z(0.15)
        py.hotkey("space")
        z(0.15)
        py.hotkey("backspace")
        z(0.15)
        py.hotkey("enter")

    elif "power down" in command:
        talk("powering down boss")
        py.hotkey("win", "x")
        z(0.25)
        py.hotkey("u")
        z(0.25)
        py.hotkey("s")

    elif "new doc" in command:
        talk(random_response)
        wb.open("https://www.google.com")
        z(0.15)
        py.keyDown("ctrl")
        py.hotkey("l")
        z(0.15)
        py.keyUp("ctrl")
        z(0.15)
        py.write("docs.new")
        z(0.15)
        py.hotkey("enter")

    elif "new sheet" in command:
        talk(random_response)
        wb.open("https://www.google.com")
        z(0.15)
        py.keyDown("ctrl")
        py.hotkey("l")
        z(0.15)
        py.keyUp("ctrl")
        z(0.15)
        py.write("sheets.new")
        z(0.15)
        py.hotkey("enter")

    # This obviously only works if the editor is pulled up
    elif "restart" in command:
        talk("will do. see you in a moment")
        py.hotkey("ctrl", "f5")

    elif "google" in command:
        talk(random_response)
        text = command.replace("google", "")
        pywhatkit.search(text.strip())

    elif "close tab" in command:
        talk(random_response)
        py.hotkey("ctrl", "w")

    # Works a bit inconsistently, maybe activation phrase is too long
    elif "3d print" in command:
        talk("What 3d print files would you like to search for")
        command = take_command()
        query = command
        wb.open("https://www.thingiverse.com/")
        z(5)
        py.hotkey("tab")
        z(0.4)
        py.hotkey("tab")
        z(0.4)
        py.write(query.strip())
        z(0.2)
        py.hotkey("enter")


    elif "search youtube" in command:
        talk(random_response)
        text = command.replace("search youtube for", "")
        wb.open("https://www.youtube.com/")
        z(4)
        py.hotkey("tab")
        z(0.2)
        py.hotkey("tab")
        z(0.2)
        py.hotkey("tab")
        z(0.2)
        py.hotkey("tab")
        z(0.2)
        py.write(text.strip())
        z(0.10)
        py.hotkey("enter")

    elif "image search" in command:
        talk(random_response)
        text = command.replace("image search", "")
        wb.open("https://www.google.com/imghp")
        z(0.5)
        py.write(text.strip())
        z(0.10)
        py.hotkey("enter")

    elif "weather" in command:
        talk("it is " + weather_desc)
        z(0.15)
        talk("the current temp is " + temp)
        z(0.3)

    elif "type" in command:
        talk(random_response)
        t2t = command.replace("type", "")
        py.write(t2t.strip())

    # Only works with some keys at the moment
    elif "press" in command:
        talk(random_response)
        key = command.replace("press", "")
        py.hotkey(key.strip())

    elif "launch" in command:
        talk(random_response)
        program = command.replace("launch", "")
        py.hotkey("win")
        z(0.5)
        py.write(program.strip())
        z(0.5)
        py.hotkey("enter")

    elif "translate" in command:
        talk("What is your target language")
        language = take_command()

        if "spanish" in language:
            target = "es"

        elif "english" in language:
            target = "en"

        elif "chinese" in language:  # not working
            target = "zh-tw"

        elif "french" in language:
            target = "fr"

        elif "german" in language:
            target = "de"

        elif "greek" in language:
            target = "el"

        elif "japanese" in language:  # not working
            target = "ja"

        elif "korean" in language:  # not working
            target = "ko"

        elif "russian" in language:  # not working
            target = "ru"

        else:
            talk("no language detected")
            pass

        input = command.replace("translate", "")
        out = translater.translate(input, dest=target)

        talk(out.text)
        print(language)
        print(out.text)

    else:
        talk("No command detected")
        pass

    z(0.5)
    talk(deactivation)

def activation():

#This allows you to call upon your VA. You have to press it a couple times initially. Will hopefully work this out soon
    while True:
        if keyboard.is_pressed("left") and keyboard.is_pressed("right"):
            z(0.75)
            run_raven()

talk(hello)
talk("Press the left and right arrow keys at the same time to reach me")
while True:
    try:
        activation()
    # Had an odd issue where Raven would sometimes shut down, this seemed to fix it
    except UnboundLocalError:
        print("Raven has stopped working")
        talk("shutting down boss")
        break
