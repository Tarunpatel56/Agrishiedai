from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime
from database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    rainfall = Column(Float)
    humidity = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class CropImage(Base):
    __tablename__ = "crop_images"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
