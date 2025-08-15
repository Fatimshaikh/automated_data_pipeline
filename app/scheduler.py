from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas
from .utils.fetcher import fetch_weather

def store_weather():
    db: Session = SessionLocal()
    try:
        for city in list(fetch_weather.__globals__["CITY_COORDS"].keys()):
            try:
                weather_data = fetch_weather(city)
                item = schemas.DataItemCreate(
                    name=f"{city} Temperature (°C)",
                    value=weather_data["temperature"],
                    city=city,
                    wind_kph=weather_data["wind_kph"],
                    precip_mm=weather_data["precip_mm"],
                    uv_index=weather_data["uv_index"],
                    air_quality=weather_data["air_quality"]
                )
                crud.create_data_item(db, item)
                print(f"✅ Stored weather for {city}: {weather_data['temperature']}°C")
            except Exception as e:
                print(f"❌ Failed to fetch/store {city}: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(store_weather, "interval", minutes=1)  # Every 1 minute
    scheduler.start()
