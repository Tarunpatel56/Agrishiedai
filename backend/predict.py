import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Classes
classes = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

# Load model
model = models.efficientnet_b0(weights=None)
num_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_features, len(classes))

model.load_state_dict(torch.load("../models/disease_model.pth", map_location=device))
model = model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def predict_image(image_path):

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    confidence_score = round(confidence.item() * 100, 2)
    predicted_class = classes[predicted.item()]

    # Healthy / Unhealthy
    if "healthy" in predicted_class.lower():
        status = "Healthy"
        health_score = confidence_score
    else:
        status = "Unhealthy"
        health_score = 100 - confidence_score

    # Growth stage + age logic
    if health_score > 80:
        growth_stage = "Vegetative"
        estimated_age_days = 45
    elif health_score > 60:
        growth_stage = "Early Stage"
        estimated_age_days = 35
    else:
        growth_stage = "Stress Stage"
        estimated_age_days = 30

    return {
        "status": status,
        "disease_type": predicted_class,
        "confidence_percent": confidence_score,
        "health_score": health_score,
        "growth_stage": growth_stage,
        "estimated_age_days": estimated_age_days
    }
