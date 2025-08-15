# app/main.py
from fastapi import FastAPI
from .database import engine
from . import models
from .routes import data, analytics
from .routes import timeseries  # <-- add
from .scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware
from .routes import recommendations

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automated Data Pipeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(data.router)
app.include_router(analytics.router)
app.include_router(timeseries.router)   # <-- add
app.include_router(recommendations.router)


@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "Automated Data Pipeline with Weather + Analytics + TS"}

@app.get("/recommendations/{city}")
def get_recommendations(city: str):
    # your logic here
    return {
        "city": city,
        "clothing": "Wear a jacket",
        "activity": "Go for a walk",
        "health": "Sunscreen recommended"
    }
