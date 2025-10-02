import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak a response
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen for the wake word
def listen_for_wake_word(wake_word="jarvis"):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            query = recognizer.recognize_google(audio).lower()
            print(f"You said: {query}")
            if wake_word in query:
                return True
        except sr.UnknownValueError:
            speak("Didn't catch that.")
        except sr.RequestError:
            speak("Speech service error.")
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
    return False

# Listen for the user's command
def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            command = recognizer.recognize_google(audio).lower()
            print(f"Command: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("There was a network error.")
        except sr.WaitTimeoutError:
            speak("Listening timed out.")

# Handle different commands
def process_command(command):
    if "open" in command:
        words = command.split()
        if "open" in words and len(words) > words.index("open") + 1:
            site = words[words.index("open") + 1]
            speak(f"Opening {site}")
            webbrowser.open(f"https://www.{site}.com")
        else:
            speak("Please specify a website to open.")
    elif command.lower().startswith("play"):
        playMusic(command)
    elif "stop" in command or "shutdown" in command:
        speak("Shutting down. Goodbye!")
        return False
    else:
        speak("Sorry, I can't do that yet.")
    return True


# Plays music from music library
def playMusic(command):
    song_name = command.lower().replace("play", "").strip()
    if not song_name:
        speak("Please specify a song name.")
        return
    if song_name not in musicLibrary.music:
        speak("Song not found.")
        return
    speak(f"Playing {song_name}")
    webbrowser.open(musicLibrary.music[song_name])



# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    try:
        while True:
            if listen_for_wake_word():
                speak("Jarvis activated.")
                command = listen_for_command()
                if not process_command(command):
                    break
            time.sleep(1)
    except KeyboardInterrupt:
        speak("Manual shutdown. Goodbye!")