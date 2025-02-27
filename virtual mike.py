import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

print('Loading your AI personal assistant - Mike')

# Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Fixed Voice Selection

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  # Helps with noise reduction
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
            return statement.lower()

        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you repeat?")
            return "None"
        except sr.RequestError:
            speak("Could not request results. Please check your internet connection.")
            return "None"

speak("Loading your AI personal assistant, Mike")
wishMe()

if __name__ == '__main__':
    while True:
        speak("Tell me, how can I help you now?")
        statement = takeCommand()

        if statement == "none":
            continue

        if "goodbye" in statement or "ok bye" in statement or "stop" in statement:
            speak("Your personal assistant Mike is shutting down. Goodbye!")
            print("Your personal assistant Mike is shutting down. Goodbye!")
            break

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            query = statement.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Multiple results found. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find any information on that topic.")

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open now")
            time.sleep(3)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(3)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Google Mail is open now")
            time.sleep(3)

        elif "weather" in statement:
            api_key = os.getenv("OPENWEATHER_API_KEY")  # Secure API Key
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What is the city name?")
            city_name = takeCommand()

            if city_name != "none":
                complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
                response = requests.get(complete_url)
                weather_data = response.json()

                if weather_data["cod"] != "404":
                    main = weather_data["main"]
                    temperature = main["temp"]
                    humidity = main["humidity"]
                    weather_desc = weather_data["weather"][0]["description"]
                    speak(f"The temperature in {city_name} is {temperature} degrees Celsius with {weather_desc}. Humidity is {humidity}%.")
                    print(f"Temperature: {temperature}°C\nHumidity: {humidity}%\nDescription: {weather_desc}")
                else:
                    speak("City not found.")

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak("I am Mike, your personal assistant. I can open websites, search Wikipedia, check weather, tell time, capture photos, "
                  "fetch news headlines, and answer computational or geographical questions.")

        elif "who made you" in statement or "who created you" in statement:
            speak("I was built by Samyak")
            print("I was built by Samyak")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com")
            speak("Here is Stack Overflow")

        elif 'news' in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak("Here are some headlines from The Times of India. Happy reading!")
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "AI Camera", "img.jpg")

        elif 'search' in statement:
            query = statement.replace("search", "")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            time.sleep(3)

        elif 'ask' in statement:
            speak("I can answer computational and geographical questions. What is your question?")
            question = takeCommand()
            if question != "none":
                try:
                    app_id = os.getenv("WOLFRAMALPHA_API_KEY")  # Secure API Key
                    client = wolframalpha.Client(app_id)
                    res = client.query(question)
                    answer = next(res.results).text
                    speak(answer)
                    print(answer)
                except Exception:
                    speak("I could not fetch an answer. Please try again.")

        elif "log off" in statement or "sign out" in statement:
            speak("Are you sure you want to log off? Say 'yes' to confirm or 'no' to cancel.")
            confirmation = takeCommand()
            if "yes" in confirmation:
                speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
                time.sleep(10)
                subprocess.call(["shutdown", "/l"])
            else:
                speak("Log off canceled.")

time.sleep(3)
