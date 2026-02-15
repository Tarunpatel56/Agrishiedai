import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Dataset path
data_dir = "../../data/plantvillage dataset"

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load dataset
full_dataset = datasets.ImageFolder(root=data_dir, transform=transform)

print("Classes found:", full_dataset.classes)

train_loader = DataLoader(full_dataset, batch_size=16, shuffle=True)

# Load pretrained model
model = models.efficientnet_b0(weights="DEFAULT")

# Freeze base layers
for param in model.parameters():
    param.requires_grad = False

# Get number of features
num_features = model.classifier[1].in_features

# Replace classifier
model.classifier[1] = nn.Linear(num_features, len(full_dataset.classes))

model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

# Training loop
epochs = 5

for epoch in range(epochs):
    model.train()
    running_loss = 0.0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch [{epoch+1}/{epochs}] Loss: {running_loss/len(train_loader):.4f}")

# Save model
os.makedirs("../../models", exist_ok=True)
torch.save(model.state_dict(), "../../models/disease_model.pth")

print("Model saved successfully.")
