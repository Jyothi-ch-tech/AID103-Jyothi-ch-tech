import random

def analyze_crop(image_path, farm_data):
    diseases = ["Leaf Blight", "Powdery Mildew", "Healthy"]
    disease = random.choice(diseases)

    severity = "Low" if disease == "Healthy" else random.choice(["Medium", "High"])

    return {
        "disease": disease,
        "severity": severity,
        "confidence": round(random.uniform(0.75, 0.95), 2)
    }
