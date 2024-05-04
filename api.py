import requests # type: ignore
import json
from datetime import datetime
$spms
# Function to fetch weather data from OpenWeatherMap API
def fetch_weather(api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Melbourne,au&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        city = weather_data["name"]
        weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        temperature_max = weather_data["main"]["temp_max"]
        temperature_min = weather_data["main"]["temp_min"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        return city, weather, temperature, temperature_max, temperature_min, humidity, wind_speed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return None, None, None, None, None, None, None, None

# Define energy calculation function
def calculate_energy(max_temperature, min_temperature):
    # Constants for energy calculation
    average_solar_radiation = 3.19  # Average solar radiation for Melbourne
    area_solar_panels = 100  # Area of solar panels in square meters
    efficiency_factor = 0.15  # Efficiency factor of solar panels
    number_of_daylight_hours = 6  # Number of daylight hours

    # Calculate solar irradiance
    solar_irradiance_max = average_solar_radiation * (1 + (max_temperature - min_temperature) / 100)
    solar_irradiance_min = average_solar_radiation * (1 - (max_temperature - min_temperature) / 100)

    # Calculate energy generation potential in kilowatt-hours (kWh)
    energy_generation_max = solar_irradiance_max * area_solar_panels * efficiency_factor * number_of_daylight_hours / 100
    energy_generation_min = solar_irradiance_min * area_solar_panels * efficiency_factor * number_of_daylight_hours / 100

    return energy_generation_max, energy_generation_min

# API key from OpenWeatherMap
api_key = "9ecd341d89b4805fb167f038459f48ea"

# Send request to fetch weather data
city, weather, temperature, temperature_max, temperature_min, humidity, wind_speed, fetch_date = fetch_weather(api_key)

if city is not None:
    # Calculate maximum and minimum energy
    max_energy, min_energy = calculate_energy(temperature_max, temperature_min)

    # Create dictionary for JSON
    melbourne_weather = {
        "fetch_date": fetch_date,
        "city": city,
        "weather": weather,
        "temperature": temperature,
        "maximum_temperature": temperature_max,
        "minimum_temperature": temperature_min,
        "maximum_energy": max_energy,
        "minimum_energy": min_energy,
        "humidity": humidity,
        "wind_speed": wind_speed
    }

    # Convert dictionary to JSON format
    melbourne_weather_json = json.dumps(melbourne_weather, indent=4)

    # Print or save JSON data
    print(melbourne_weather_json)

    # Optional: Save JSON data to a file
    with open("melbourne_weather.json", "w") as json_file:
        json_file.write(melbourne_weather_json)

else:
    print("Error fetching weather data.")

