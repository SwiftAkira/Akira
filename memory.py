import json
import os

MEMORY_FILE = 'memory.json'

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(memory, file)

def add_to_memory(text):
    memory = load_memory()
    memory.append(text)
    save_memory(memory)

def search_within_memory(query):
    memory = load_memory()
    results = [entry for entry in memory if query.lower() in entry.lower()]
    return results