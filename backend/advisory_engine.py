def generate_advisory(status, health_score):

    if status == "Healthy":
        return "Crop is healthy. Maintain irrigation."

    if health_score > 60:
        return "Mild stress detected. Apply balanced fertilizer."

    return "High disease risk. Immediate treatment required."
