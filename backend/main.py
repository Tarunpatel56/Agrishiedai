from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
import shutil
import os

from database import engine
from models import Base, WeatherData
from predict import predict_image
from weather_engine import fetch_weather
from risk_engine import calculate_risk
from advisory_engine import generate_advisory

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------ ROOT ------------------
@app.get("/")
def root():
    return {"message": "AgriShield Backend Running 🚀"}


# ------------------ WEATHER ------------------
@app.get("/weather")
def get_weather():

    weather_data = fetch_weather()

    db = Session(bind=engine)

    weather_entry = WeatherData(
        temperature=weather_data.get("temperature"),
        rainfall=0,
        humidity=0
    )

    db.add(weather_entry)
    db.commit()
    db.close()

    return weather_data


# ------------------ PREDICT ------------------
@app.post("/predict")
def predict(file: UploadFile = File(...)):

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # AI Prediction
    result = predict_image(file_path)

    # Weather Fetch
    weather_data = fetch_weather()

    # Risk Calculation
    risk = calculate_risk(
        result["health_score"],
        weather_data.get("temperature")
    )

    # Advisory
    advisory = generate_advisory(
        result["status"],
        result["health_score"]
    )

    return {
        "prediction": result,
        "weather": weather_data,
        "risk_analysis": risk,
        "advisory": advisory
    }
