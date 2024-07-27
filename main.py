import json
import os
import requests
import pyttsx3
import speech_recognition as sr
import numpy as np
import openai
import pygame
from run import fetch_voices
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY
from utils import (
    update_context, get_context, append_to_history, get_history, 
    get_assistant_name, reset_context, detect_end_of_conversation, 
    identify_key_moments, store_key_moment, get_key_moments, load_user_settings,
    save_json_file, get_user_settings_filepath
)
from memory import search_within_memory, add_to_memory
from tasks import manage_tasks
from weather import get_weather_info
from speech import speak_text, listen_command, listen_for_wake_word

openai.api_key = OPENAI_API_KEY

# Function to get a response from OpenAI with context
def get_openai_response(user_id, user_input):
    history = get_history(user_id)
    key_moments = get_key_moments(user_id)
    user_settings = load_user_settings(user_id)
    humor = user_settings.get('humor', 5)
    sarcasm = user_settings.get('sarcasm', 5)
    empathy = user_settings.get('empathy', 5)
    
    system_message = (
        f"You are an AI assistant named AKIRA. You have a personality with humor level {humor}, "
        f"sarcasm level {sarcasm}, and empathy level {empathy}. Act accordingly in your responses."
    )
    
    messages = [{"role": "system", "content": system_message}]
    for entry in key_moments:
        messages.append({"role": "user", "content": entry})
    for entry in history:
        if "User: " in entry:
            messages.append({"role": "user", "content": entry.replace("User: ", "")})
        elif "AKIRA: " in entry:
            messages.append({"role": "assistant", "content": entry.replace("AKIRA: ", "")})
    messages.append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    ai_response = response.choices[0].message['content'].strip()
    append_to_history(user_id, f"User: {user_input}")
    append_to_history(user_id, f"AKIRA: {ai_response}")
    return ai_response

# Function to convert temperature information to text
def format_weather_info(location, current_temp, high_temp, low_temp):
    return (
        f"The current temperature in {location} is {current_temp} degrees Celsius. "
        f"The high for today is {high_temp} degrees Celsius and the low is {low_temp} degrees Celsius."
    )

# Function to adjust personality settings
def adjust_personality_setting(user_id, setting, value):
    settings = load_user_settings(user_id)
    settings[setting] = value
    save_json_file(settings, get_user_settings_filepath(user_id))
    return f"Alright! I've adjusted my {setting} to {value}."

# Function to report current personality settings
def get_personality_settings(user_id):
    settings = load_user_settings(user_id)
    humor = settings.get('humor', 5)
    sarcasm = settings.get('sarcasm', 5)
    empathy = settings.get('empathy', 5)
    return f"My current settings are: humor level {humor}, sarcasm level {sarcasm}, and empathy level {empathy}."

# Function to parse and adjust personality settings from user input
def parse_and_adjust_personality(user_id, user_input):
    try:
        parts = user_input.lower().split()
        setting = None
        value = None
        if 'empathy' in parts:
            setting = 'empathy'
        elif 'humor' in parts:
            setting = 'humor'
        elif 'sarcasm' in parts:
            setting = 'sarcasm'

        for part in parts:
            if part.isdigit():
                value = int(part)
                break

        if setting and value is not None and 0 <= value <= 10:
            return adjust_personality_setting(user_id, setting, value)
        else:
            return "I couldn't understand the setting or value. Please specify a number between 0 and 10 for empathy, humor, or sarcasm."
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    user_id = "default_user"
    assistant_name = get_assistant_name()
    conversation_active = False
    
    print(f"{assistant_name} is ready. Say 'Hey {assistant_name}' to start.")
    
    while True:
        if not conversation_active:
            if listen_for_wake_word():
                conversation_active = True
        
        if conversation_active:
            user_input = listen_command()
            if detect_end_of_conversation(user_input):
                reset_context(user_id)
                conversation_active = False
                print("Listening for wake word...")
                continue

            if identify_key_moments(user_input):
                store_key_moment(user_id, user_input)

            if user_input.lower() == 'exit':
                break
            elif 'weather' in user_input.lower() or 'temperature' in user_input.lower():
                location = user_input.split("in")[-1].strip() if "in" in user_input else None
                weather_info_raw = '{"current": 15, "high": 20, "low": 10}'  # Example JSON string
                weather_info_raw = json.loads(weather_info_raw)
                weather_info = format_weather_info(location, weather_info_raw['current'], weather_info_raw['high'], weather_info_raw['low'])
                print(f"{assistant_name}: {weather_info}")
                speak_text(weather_info)
                update_context(user_id, "last_weather_query", weather_info)
            elif user_input.lower() == 'tasks':
                manage_tasks()
            elif 'search memory' in user_input.lower():
                query = input("Enter your search query: ")
                results = search_within_memory(query)
                if results:
                    print("Here are the most relevant memory entries:")
                    for result in results:
                        print(f"- {result}")
                else:
                    print("No relevant memory entries found.")
            elif 'fetch voices' in user_input.lower():
                fetch_voices()
            elif 'hello' in user_input.lower() or 'hi' in user_input.lower():
                response = f"Hello! How can I assist you today? My name is {assistant_name}."
                print(f"{assistant_name}: {response}")
                speak_text(response)
                update_context(user_id, "last_greeting", response)
            elif 'your name' in user_input.lower():
                response = f"I am your AI assistant. My name is {assistant_name}."
                print(f"{assistant_name}: {response}")
                speak_text(response)
                update_context(user_id, "last_identity", response)
            elif 'current settings' in user_input.lower():
                response = get_personality_settings(user_id)
                print(f"{assistant_name}: {response}")
                speak_text(response)
            elif 'empathy' in user_input.lower() or 'humor' in user_input.lower() or 'sarcasm' in user_input.lower():
                response = parse_and_adjust_personality(user_id, user_input)
                print(f"{assistant_name}: {response}")
                speak_text(response)
            else:
                response = get_openai_response(user_id, user_input)
                print(f"{assistant_name}: {response}")
                speak_text(response)
                update_context(user_id, "last_response", response)

if __name__ == "__main__":
    main()