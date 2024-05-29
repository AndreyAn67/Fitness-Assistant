import requests

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def format_weather(weather_data, city):
    if weather_data:
        return (f"Weather in {city}:\n"
                f"Temperature: {weather_data['main']['temp']}°C\n"
                f"Description: {weather_data['weather'][0]['description']}\n"
                f"Humidity: {weather_data['main']['humidity']}%\n"
                f"Wind Speed: {weather_data['wind']['speed']} m/s")
    else:
        return "Failed to get weather data."