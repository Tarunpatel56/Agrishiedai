def calculate_risk(health_score, temperature):

    if health_score < 50:
        crop_risk = 80
    elif health_score < 70:
        crop_risk = 50
    else:
        crop_risk = 20

    if temperature and temperature > 38:
        drought_risk = 70
    else:
        drought_risk = 30

    return {
        "crop_failure_risk_percent": crop_risk,
        "drought_risk_percent": drought_risk
    }
