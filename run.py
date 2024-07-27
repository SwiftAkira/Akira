import requests
from config import ELEVENLABS_API_KEY

def fetch_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        voices = response.json()
        for voice in voices['voices']:
            print(f"Name: {voice['name']}, Voice ID: {voice['voice_id']}")
    else:
        print(f"Failed to fetch voices: {response.text}")

if __name__ == "__main__":
    fetch_voices()