from fastapi import FastAPI
from database import engine
from models import Base, WeatherData
from weather_engine import fetch_weather
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
import shutil
import os


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AgriShield Backend Running 🚀"}

@app.get("/weather")
def get_weather():

    temp, rain, humidity = fetch_weather()

    db = Session(bind=engine)

    weather_entry = WeatherData(
        temperature=temp,
        rainfall=rain,
        humidity=humidity
    )

    db.add(weather_entry)
    db.commit()
    db.close()

    return {
        "temperature": temp,
        "rainfall": rain,
        "humidity": humidity
    }
@app.post("/upload")
def upload_image(file: UploadFile = File(...)):

    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_location = os.path.join(upload_folder, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = Session(bind=engine)

    new_image = CropImage(
        file_name=file.filename,
        file_path=file_location
    )

    db.add(new_image)
    db.commit()
    db.close()

    return {"message": "Image uploaded successfully", "file_name": file.filename}

