import os
import sys
import datetime
import time
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import webbrowser
import musicLibrary
from openai import OpenAI
from newsapi import NewsApiClient
import threading

# --- Load Environment Variables ---
load_dotenv()

# --- API Key Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# --- Global Reminders List ---
reminders = []

# --- Functions ---

def speak(text):
    """Converts text to speech using gTTS, plays it, and deletes the file."""
    if not text:
        print("Received empty text to speak.")
        return
    try:
        print(f"SPEAKING: {text}")
        tts = gTTS(text=text, lang='en', slow=False)
        temp_audio_file = "temp_speech.mp3"
        tts.save(temp_audio_file)
        playsound(temp_audio_file)
        os.remove(temp_audio_file)
    except Exception as e:
        print(f"gTTS or playsound Error: {e}")

def aiProcess(command):
    """Sends a command to OpenRouter AI and returns the response."""
    if not OPENROUTER_API_KEY:
        return "Error: OpenRouter API key is not set. Please check your .env file."
    try:
        client = OpenAI(
          base_url="https://openrouter.ai/api/v1",
          api_key=OPENROUTER_API_KEY,
        )
        completion = client.chat.completions.create(
          model="openai/gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are Pinky, a concise and helpful virtual assistant."},
            {"role": "user", "content": command}
          ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
        return "Sorry, I ran into an error with the AI service."

def get_latest_news():
    """Fetches the top 5 news headlines from India."""
    if not NEWS_API_KEY:
        return ["Error: News API key is not set."]
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        top_headlines = newsapi.get_top_headlines(country='in', page_size=5)
        if top_headlines['status'] == 'ok' and top_headlines['articles']:
            return [article['title'] for article in top_headlines['articles']]
        else:
            return ["Sorry, I couldn't fetch the news right now."]
    except Exception as e:
        print(f"NewsAPI Error: {e}")
        return ["Sorry, I encountered an error while fetching the news."]

def handle_reminders():
    """Checks for and announces due reminders."""
    while True:
        if reminders:
            now = datetime.datetime.now()
            reminders_to_remove = []
            for i, (remind_time, message) in enumerate(reminders):
                if now >= remind_time:
                    speak(f"Reminder: {message}")
                    reminders_to_remove.append(i)
            
            # Remove announced reminders
            for i in sorted(reminders_to_remove, reverse=True):
                reminders.pop(i)
        time.sleep(1) # Check every second

def processCommand(command):
    """Processes the user's voice command."""
    global reminders
    command = command.lower()

    # Basic Website Commands
    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    elif "open chat gpt" in command:
        speak("Opening ChatGPT.")
        webbrowser.open("https://chat.openai.com")
    elif "open github" in command:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")
    elif "open instagram" in command:
        speak("Opening Instagram.")
        webbrowser.open("https://instagram.com")
    elif "open whatsapp" in command:
        speak("Opening Web WhatsApp.")
        webbrowser.open("https://web.whatsapp.com")
    elif "open udemy" in command:
        speak("Opening Udemy.")
        webbrowser.open("https://www.udemy.com")

    # Time and Date Commands
    elif "the time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "the date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    # Search Command
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Reminder Command
    elif "set a reminder" in command or "remind me to" in command:
        speak("What should I remind you about?")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for reminder message...")
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                message = recognizer.recognize_google(audio)
                speak("When should I remind you? For example, in 10 seconds, 5 minutes, or 1 hour.")
                print("Listening for reminder time...")
                audio_time = recognizer.listen(source, timeout=5)
                time_str = recognizer.recognize_google(audio_time).lower()
                
                delta = None
                if "second" in time_str:
                    seconds = int(time_str.split()[0])
                    delta = datetime.timedelta(seconds=seconds)
                elif "minute" in time_str:
                    minutes = int(time_str.split()[0])
                    delta = datetime.timedelta(minutes=minutes)
                elif "hour" in time_str:
                    hours = int(time_str.split()[0])
                    delta = datetime.timedelta(hours=hours)

                if delta:
                    remind_time = datetime.datetime.now() + delta
                    reminders.append((remind_time, message))
                    speak(f"Okay, I will remind you to {message} at {remind_time.strftime('%I:%M %p')}.")
                else:
                    speak("Sorry, I didn't understand the time. Please try again.")

            except Exception as e:
                print(e)
                speak("Sorry, I couldn't set the reminder.")

    # Music Command
    elif "play" in command:
        song_title = ""
        recognizer = sr.Recognizer()
        if "song" in command and len(command.split()) < 3:
            speak("Which song would you like to play?")
            with sr.Microphone() as source:
                print("Listening for song title...")
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5)
                    song_title = recognizer.recognize_google(audio).lower()
                except Exception:
                    speak("Sorry, I didn't catch that.")
                    return
        else:
            song_title = command.replace("play", "").strip()

        if song_title and hasattr(musicLibrary, 'music') and song_title in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song_title])
            speak(f"Playing {song_title}")
        elif song_title:
            speak(f"Sorry, I couldn't find the song {song_title}.")
            
    # News Command
    elif "news" in command or "headlines" in command:
        speak("Fetching the latest news headlines from India.")
        headlines = get_latest_news()
        news_summary = ". ".join(headlines)
        speak(news_summary)

    # Shutdown Command
    elif "goodbye" in command or "shut down" in command:
        speak("Goodbye!")
        sys.exit()

    # Fallback to AI
    else:
        speak("Let me think...")
        output = aiProcess(command)
        speak(output)

# --- Main Loop ---
if __name__ == "__main__":
    if not OPENROUTER_API_KEY or not NEWS_API_KEY:
        print("CRITICAL ERROR: API keys not found. Please check your .env file.")
        speak("Error, API keys not found, please check the console.")
    else:
        # Start the reminder checking thread
        reminder_thread = threading.Thread(target=handle_reminders, daemon=True)
        reminder_thread.start()

        speak("Initializing Pinky.")
        recognizer = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as source:
                    print("\nListening for wake word 'Pinky'...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)
                word = recognizer.recognize_google(audio)
                print(f"Heard: {word}")

                if "pinky" in word.lower():
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Pinky Active... Listening for a command...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)
            except sr.WaitTimeoutError:
                print("Listening timed out.")
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                speak("Sorry, I'm having trouble connecting to the internet.")
            except Exception as e:
                print(f"An error occurred in the main loop: {e}")
