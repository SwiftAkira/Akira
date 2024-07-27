import os
import requests
import pygame
import speech_recognition as sr
from config import ELEVENLABS_API_KEY

ELEVENLABS_VOICE_ID = "" #also change this to ur voice id
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2" #dont change this unless you know what you are doing

pygame.mixer.init()

def speak_text(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream"
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL_ID,
        "voice_settings": {
            "stability": 0.3,            # Lower stability for more variability
            "similarity_boost": 0.9,     # Higher similarity for natural tone
        }
    }
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)

    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("Speech synthesis successful, saved as output.mp3.")
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("output.mp3")
    else:
        print(f"Failed to synthesize speech: {response.text}")

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                if "akira" in command or "hey akira" in command:
                    print("Wake word detected!")
                    return True
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Sorry, my speech service is down.")
                return False

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""