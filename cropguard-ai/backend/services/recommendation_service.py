def recommend(disease, crop_type, severity):
    """
    Generate treatment recommendations for crop diseases
    Supports all 38 disease classes from the Plant Disease dataset
    """
    organic = ""
    chemical = ""
    
    # Extract crop and disease from the disease name (format: Crop___Disease)
    if "___" in disease:
        crop, disease_name = disease.split("___", 1)
        crop = crop.replace("_", " ").replace("(", "").replace(")", "")
        disease_name = disease_name.replace("_", " ")
    else:
        crop = crop_type if crop_type else "crop"
        disease_name = disease
    
    # Check if healthy
    if "healthy" in disease.lower():
        organic = f"Continue good practices: balanced irrigation, crop rotation, and regular monitoring."
        chemical = "No chemical treatment needed. Maintain preventive care."
    
    # Bacterial diseases
    elif "bacterial" in disease_name.lower() or "spot" in disease_name.lower():
        organic = f"Remove infected leaves, improve air circulation, apply copper-based organic sprays."
        chemical = f"Use copper hydroxide or streptomycin sulfate. Apply every 7-10 days."
        if severity == "high":
            chemical += " Increase application frequency to every 5 days."
    
    # Fungal diseases - Blight
    elif "blight" in disease_name.lower():
        organic = f"Remove affected plant parts, avoid overhead watering, apply neem oil weekly."
        chemical = f"Use chlorothalonil or mancozeb fungicide. Rotate with copper-based products."
        if severity == "high":
            chemical += " Apply preventively to surrounding plants."
    
    # Fungal diseases - Rust
    elif "rust" in disease_name.lower():
        organic = f"Improve air flow, remove infected leaves, spray sulfur-based fungicide."
        chemical = f"Apply triazole or strobilurin fungicides. Rotate products to prevent resistance."
    
    # Fungal diseases - Mildew
    elif "mildew" in disease_name.lower():
        organic = f"Spray potassium bicarbonate solution, ensure good air circulation."
        chemical = f"Use systemic fungicides like myclobutanil or propiconazole."
        if severity == "high":
            chemical += " Apply at first sign and repeat every 7-14 days."
    
    # Fungal diseases - Mold
    elif "mold" in disease_name.lower():
        organic = f"Reduce humidity, prune for better airflow, apply biological fungicides."
        chemical = f"Use chlorothalonil or copper-based fungicides preventively."
    
    # Fungal diseases - Scab
    elif "scab" in disease_name.lower():
        organic = f"Remove fallen leaves, apply lime sulfur during dormancy, use resistant varieties."
        chemical = f"Apply captan or myclobutanil at bud break and petal fall."
    
    # Fungal diseases - Black rot
    elif "black rot" in disease_name.lower() or "rot" in disease_name.lower():
        organic = f"Prune infected areas, improve drainage, apply bordeaux mixture."
        chemical = f"Use mancozeb or captan fungicides. Start at bud break."
    
    # Fungal diseases - Leaf scorch
    elif "scorch" in disease_name.lower():
        organic = f"Ensure adequate watering, mulch to retain moisture, remove affected leaves."
        chemical = f"Apply fungicides containing myclobutanil if fungal. Check for drought stress."
    
    # Viral diseases
    elif "virus" in disease_name.lower() or "mosaic" in disease_name.lower() or "curl" in disease_name.lower():
        organic = f"Remove and destroy infected plants immediately. Control insect vectors with neem oil."
        chemical = f"No cure for viral diseases. Use insecticides to control aphids/whiteflies that spread virus."
        if severity == "high":
            chemical += " Remove infected plants to prevent spread."
    
    # Pest-related (mites, etc.)
    elif "mite" in disease_name.lower():
        organic = f"Spray with insecticidal soap or neem oil. Introduce predatory mites."
        chemical = f"Use miticides like abamectin or spiromesifen. Rotate products."
    
    # Citrus greening
    elif "greening" in disease_name.lower() or "haunglongbing" in disease_name.lower():
        organic = f"Remove infected trees, control psyllid vectors, use disease-free nursery stock."
        chemical = f"No cure available. Apply systemic insecticides to control Asian citrus psyllid."
    
    # Esca (grape disease)
    elif "esca" in disease_name.lower() or "measles" in disease_name.lower():
        organic = f"Prune during dry weather, protect pruning wounds, remove infected wood."
        chemical = f"Apply protective fungicides to pruning wounds. No curative treatment available."
    
    # Cercospora
    elif "cercospora" in disease_name.lower():
        organic = f"Practice crop rotation, remove crop debris, apply copper-based sprays."
        chemical = f"Use azoxystrobin or propiconazole fungicides preventively."
    
    # Generic fallback for any other disease
    else:
        organic = f"Remove affected plant parts, improve cultural practices, apply organic fungicide."
        chemical = f"Consult local extension service for specific fungicide recommendations."
    
    # Add severity-based modifications
    if severity == "high" and "No chemical" not in chemical:
        organic += f" Act immediately - disease is severe."
        if "Apply" in chemical and "every" not in chemical:
            chemical += " Apply thoroughly and repeat as needed."
    elif severity == "medium":
        organic += f" Monitor closely and treat promptly."
    
    # Add crop-specific note
    if crop_type:
        organic += f" Adjust timing for {crop_type} growth stage."
    
    return f"Organic: {organic} | Chemical: {chemical}"

