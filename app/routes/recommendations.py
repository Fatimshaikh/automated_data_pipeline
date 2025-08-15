from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..utils.fetcher import fetch_weather

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# Clothing suggestions based on temperature and wind
def clothing_suggestion(temp_c: float, wind_kph: float) -> str:
    if temp_c <= 0:
        return "Heavy coat, gloves, and scarf"
    elif temp_c <= 10:
        return "Coat and sweater"
    elif temp_c <= 20:
        return "Light jacket or sweater"
    elif temp_c <= 30:
        return "T-shirt and pants/shorts"
    else:
        return "Very light clothing, stay hydrated"

# Activity suggestions based on precipitation and wind
def activity_alerts(precip_mm: float, wind_kph: float) -> str:
    if precip_mm > 2:
        return "Avoid outdoor activities, carry an umbrella"
    elif wind_kph > 25:
        return "Strong wind, outdoor sports not recommended"
    else:
        return "Perfect day for outdoor activities"

# Health alerts based on UV index and air quality
def health_notifications(uv_index: float, air_quality: float) -> str:
    notifications = []
    if uv_index >= 6:
        notifications.append("High UV index: Wear sunscreen")
    if air_quality > 100:
        notifications.append("Poor air quality: Limit outdoor activities")
    return ", ".join(notifications) or "No special health alerts"

@router.get("/{city}")
def get_recommendations(city: str, db: Session = Depends(get_db)):
    # Try to get latest data from the database
    item = crud.get_latest_value(db, city=city)

    if item:
        temp = getattr(item, "value", 0)
        wind = getattr(item, "wind_kph", 5)
        precip = getattr(item, "precip_mm", 0)
        uv_index = getattr(item, "uv_index", 3)
        air_quality = getattr(item, "air_quality", 50)
    else:
        # If not found in DB, fetch from API
        try:
            weather_data = fetch_weather(city)
            temp = weather_data["temperature"]
            wind = weather_data["wind_kph"]
            precip = weather_data["precip_mm"]
            uv_index = weather_data["uv_index"]
            air_quality = weather_data["air_quality"]
        except ValueError:
            return {"message": f"City '{city}' not found in API or database"}

    return {
        "city": city,
        "temperature": temp,
        "clothing": clothing_suggestion(temp, wind),
        "activity": activity_alerts(precip, wind),
        "health": health_notifications(uv_index, air_quality)
    }
