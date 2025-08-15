from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)           # <-- new
    value = Column(Float)
    wind_kph = Column(Float, default=5)        # optional default values
    precip_mm = Column(Float, default=0)
    uv_index = Column(Float, default=3)
    air_quality = Column(Float, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)


