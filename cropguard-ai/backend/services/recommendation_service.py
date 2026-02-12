def recommend(disease, crop_type, severity):
    organic = ""
    chemical = ""
    if disease == "Healthy":
        organic = "Maintain balanced irrigation and use compost teas."
        chemical = "No chemical action needed."
    elif disease == "Leaf Blight":
        organic = "Remove affected leaves and apply neem oil weekly."
        chemical = "Use copper-based fungicide as per label."
    elif disease == "Rust":
        organic = "Improve air flow and apply sulfur dust."
        chemical = "Apply triazole fungicide rotation."
    elif disease == "Powdery Mildew":
        organic = "Spray potassium bicarbonate solution."
        chemical = "Use systemic fungicide for severe cases."
    if severity == "high":
        chemical += " Increase frequency and ensure full coverage."
    if crop_type:
        organic += " Adjust to " + crop_type + " agronomy."
    return "Organic: " + organic + " | Chemical: " + chemical
