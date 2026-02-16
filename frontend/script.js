async function uploadImage() {

    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("dashboard").classList.remove("hidden");

    // Health
    document.getElementById("status").innerText =
        "Status: " + data.prediction.status;

    document.getElementById("healthScore").innerText =
        "Health Score: " + data.prediction.health_score + "%";

    document.getElementById("healthBar").style.width =
        data.prediction.health_score + "%";

    // Growth
    document.getElementById("growthStage").innerText =
        "Growth Stage: " + data.prediction.growth_stage;

    document.getElementById("estimatedAge").innerText =
        "Estimated Age: " + data.prediction.estimated_age_days + " days";

    // Weather
    document.getElementById("temperature").innerText =
        "Temperature: " + data.weather.temperature + "°C";

    document.getElementById("windSpeed").innerText =
        "Wind Speed: " + data.weather.windspeed + " km/h";

    // Risk
    document.getElementById("cropRisk").innerText =
        "Crop Failure Risk: " + data.risk_analysis.crop_failure_risk_percent + "%";

    document.getElementById("droughtRisk").innerText =
        "Drought Risk: " + data.risk_analysis.drought_risk_percent + "%";

    // Advisory
    document.getElementById("advisoryText").innerText =
        data.advisory;
}
