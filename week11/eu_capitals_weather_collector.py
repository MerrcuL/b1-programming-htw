import requests
import json
import time
from datetime import datetime

# 1. DATA SETUP
# Cleaned list of EU capitals based on the lab requirements
eu_capitals = [
    {"city": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"city": "Brussels", "country": "Belgium", "lat": 50.8503, "lon": 4.3517},
    {"city": "Sofia", "country": "Bulgaria", "lat": 42.6977, "lon": 23.3219},
    {"city": "Zagreb", "country": "Croatia", "lat": 45.8150, "lon": 15.9819},
    {"city": "Nicosia", "country": "Cyprus", "lat": 35.1856, "lon": 33.3823},
    {"city": "Prague", "country": "Czechia", "lat": 50.0755, "lon": 14.4378},
    {"city": "Copenhagen", "country": "Denmark", "lat": 55.6761, "lon": 12.5683},
    {"city": "Tallinn", "country": "Estonia", "lat": 59.4370, "lon": 24.7536},
    {"city": "Helsinki", "country": "Finland", "lat": 60.1695, "lon": 24.9354},
    {"city": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"city": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"city": "Athens", "country": "Greece", "lat": 37.9838, "lon": 23.7275},
    {"city": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402},
    {"city": "Dublin", "country": "Ireland", "lat": 53.3498, "lon": -6.2603},
    {"city": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"city": "Riga", "country": "Latvia", "lat": 56.9496, "lon": 24.1052},
    {"city": "Vilnius", "country": "Lithuania", "lat": 54.6872, "lon": 25.2797},
    {"city": "Luxembourg", "country": "Luxembourg", "lat": 49.6116, "lon": 6.1319},
    {"city": "Valletta", "country": "Malta", "lat": 35.8989, "lon": 14.5146},
    {"city": "Amsterdam", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041},
    {"city": "Warsaw", "country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"city": "Lisbon", "country": "Portugal", "lat": 38.7223, "lon": -9.1393},
    {"city": "Bucharest", "country": "Romania", "lat": 44.4268, "lon": 26.1025},
    {"city": "Bratislava", "country": "Slovakia", "lat": 48.1486, "lon": 17.1077},
    {"city": "Ljubljana", "country": "Slovenia", "lat": 46.0569, "lon": 14.5058},
    {"city": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
    {"city": "Stockholm", "country": "Sweden", "lat": 59.3293, "lon": 18.0686}
]

# Helper to interpret WMO Weather Codes (Open-Meteo standard)
def get_weather_condition(code):
    codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown")

def collect_weather_data():
    results = {}
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    print(f"Starting weather collection for {len(eu_capitals)} cities...")

    for city_data in eu_capitals:
        city_name = city_data["city"]
        print(f"Fetching data for {city_name}...", end=" ")

        # Parameters requested: current_weather, hourly temp, precip prob, weathercode
        # forecast_days=1 ensures we get only the current day's hourly data (simplifies processing)
        params = {
            "latitude": city_data["lat"],
            "longitude": city_data["lon"],
            "current_weather": "true",
            "hourly": "temperature_2m,precipitation_probability,weathercode",
            "forecast_days": 1
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status() # Raise error for bad status codes (4xx, 5xx)
            data = response.json()

            # Process Current Weather
            current = data.get("current_weather", {})
            
            # Process Hourly Data
            # Open-Meteo returns parallel arrays (e.g. time[], temperature_2m[])
            # We need to zip these into a list of objects as per requirements
            hourly_raw = data.get("hourly", {})
            hourly_structured = []
            
            if hourly_raw:
                times = hourly_raw.get("time", [])
                temps = hourly_raw.get("temperature_2m", [])
                probs = hourly_raw.get("precipitation_probability", [])
                codes = hourly_raw.get("weathercode", [])

                # Zip lists together safely
                for i in range(len(times)):
                    hourly_structured.append({
                        "time": times[i],
                        "temperature": temps[i] if i < len(temps) else None,
                        "precipitation_probability": probs[i] if i < len(probs) else None,
                        "weathercode": codes[i] if i < len(codes) else None
                    })

            # Build final structure for this city
            city_record = {
                "country": city_data["country"],
                "coordinates": {
                    "latitude": city_data["lat"],
                    "longitude": city_data["lon"]
                },
                "current_weather": {
                    "temperature": current.get("temperature"),
                    "windspeed": current.get("windspeed"),
                    "weathercode": current.get("weathercode"),
                    "condition": get_weather_condition(current.get("weathercode")),
                    "time": current.get("time")
                },
                "hourly_forecast": hourly_structured
            }

            results[city_name] = city_record
            print("Success.")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            # Requirements say: Log errors but continue processing
            continue
        
        # Rate limiting delay (0.5 - 1 second)
        time.sleep(0.6)

    # Write to JSON file
    output_filename = "eu_weather_data.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\nData successfully saved to {output_filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    collect_weather_data()