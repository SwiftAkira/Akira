import requests

def get_location():
    try:
        ip_address = requests.get('https://api64.ipify.org?format=json').json()['ip']
        location = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
        return location['city']
    except Exception as e:
        print(f"Could not get location due to: {e}")
        return "Unable to determine location"

def get_weather_info(location=None):
    if not location:
        location = get_location()
    if location != "Unable to determine location":
        response = requests.get(f"http://wttr.in/{location}?format=j1")
        weather_data = response.json()
        current_temp = weather_data['current_condition'][0]['temp_C']
        high_temp = weather_data['weather'][0]['maxtempC']
        low_temp = weather_data['weather'][0]['mintempC']
        weather_info = (f"The current temperature in {location} is {current_temp}°C. "
                        f"The high for today is {high_temp}°C and the low is {low_temp}°C.")
    else:
        weather_info = "Unable to get weather information."
    return weather_info