import requests

CITY_COORDS = {
    "NYC": (40.7128, -74.0060),
    "Karachi": (24.8607, 67.0011),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    # add more cities as needed
}

def fetch_weather(city: str):
    """
    Fetch current temperature for a given city.
    """
    if city not in CITY_COORDS:
        raise ValueError(f"Coordinates for city '{city}' not found")
    
    lat, lon = CITY_COORDS[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    temperature = data["current_weather"]["temperature"]

    # Optionally, include wind, precipitation, etc.
    wind = data["current_weather"].get("windspeed", 5)  # default 5 kph
    precip = data["current_weather"].get("precipitation", 0)
    uv_index = data["current_weather"].get("uv_index", 3)
    air_quality = 50  # default, you can integrate a real API if needed

    return {
        "temperature": temperature,
        "wind_kph": wind,
        "precip_mm": precip,
        "uv_index": uv_index,
        "air_quality": air_quality
    }
