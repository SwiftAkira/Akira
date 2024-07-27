# utils.py

import json
import os

# Constants
USER_INFO_DIR = 'User_Specific_Info'
ASSISTANT_NAME = "AKIRA"

def get_user_directory(user_id):
    return os.path.join(USER_INFO_DIR, f"user_{user_id}")

def ensure_user_directory_exists(user_id):
    user_dir = get_user_directory(user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def get_key_moments_filepath(user_id):
    user_dir = ensure_user_directory_exists(user_id)
    return os.path.join(user_dir, 'key_moments.json')

def get_user_settings_filepath(user_id):
    user_dir = ensure_user_directory_exists(user_id)
    return os.path.join(user_dir, 'user_settings.json')

def load_json_file(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_json_file(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file)

def update_context(user_id, key, value):
    user_dir = ensure_user_directory_exists(user_id)
    context_file = get_user_settings_filepath(user_id)
    context = load_json_file(context_file)
    context[key] = value
    save_json_file(context, context_file)

def get_context(user_id, key, default=None):
    context = load_json_file(get_user_settings_filepath(user_id))
    return context.get(key, default)

def append_to_history(user_id, message):
    user_dir = ensure_user_directory_exists(user_id)
    history_file = get_user_settings_filepath(user_id)
    context = load_json_file(history_file)
    if 'history' not in context:
        context['history'] = []
    context['history'].append(message)
    save_json_file(context, history_file)

def get_history(user_id):
    context = load_json_file(get_user_settings_filepath(user_id))
    return context.get('history', [])

def get_assistant_name():
    return ASSISTANT_NAME

def reset_context(user_id):
    context = load_json_file(get_user_settings_filepath(user_id))
    context['history'] = []
    save_json_file(context, get_user_settings_filepath(user_id))

def detect_end_of_conversation(user_input):
    end_phrases = [
        'goodbye', 'bye', 'that\'s all', 'thank you, akira', 'exit', 'stop',
        'thanks, akira', 'thank you so much', 'ok thank you', 'see you', 'farewell',
        'catch you later', 'until next time', 'take care', 'talk to you later', 'later',
        'ciao', 'adios', 'so long', 'I\'m done', 'that\'s it', 'we\'re done', 'I\'m finished',
        'all set', 'enough for now'
    ]
    user_input = user_input.lower()
    for phrase in end_phrases:
        if phrase in user_input:
            return True
    return False

def identify_key_moments(user_input):
    key_phrases = [
        'remember', 'important', 'note', 'key', 'significant', 'highlight', 'vital',
        'crucial', 'essential', 'pivotal', 'central', 'memorable', 'noteworthy',
        'unforgettable', 'remarkable', 'momentous', 'paramount', 'critical',
        'fundamental', 'imperative', 'substantial', 'weighty', 'meaningful',
        'relevant', 'consequential'
    ]
    for phrase in key_phrases:
        if phrase in user_input.lower():
            return True
    return False

def store_key_moment(user_id, moment):
    key_moments = load_key_moments(user_id)
    if not isinstance(key_moments, list):
        key_moments = []
    key_moments.append(moment)
    save_json_file(key_moments, get_key_moments_filepath(user_id))

def load_key_moments(user_id):
    return load_json_file(get_key_moments_filepath(user_id)) or []

def get_key_moments(user_id):
    return load_key_moments(user_id)

def load_user_settings(user_id):
    return load_json_file(get_user_settings_filepath(user_id))