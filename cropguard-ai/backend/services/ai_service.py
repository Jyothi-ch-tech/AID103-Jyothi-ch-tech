import numpy as np
from PIL import Image

CLASSES = ["Healthy", "Leaf Blight", "Rust", "Powdery Mildew"]

def infer(file_path):
    img = Image.open(file_path).convert("L")
    arr = np.array(img).astype(np.float32) / 255.0
    mean = float(arr.mean())
    std = float(arr.std())
    if mean > 0.7:
        disease = "Healthy"
    elif mean > 0.5:
        disease = "Powdery Mildew"
    elif mean > 0.3:
        disease = "Leaf Blight"
    else:
        disease = "Rust"
    confidence = round(min(100.0, max(0.0, (1.0 - abs(0.5 - mean)) * 100.0 - std * 50.0)), 2)
    severity = "low"
    if confidence >= 80:
        severity = "high"
    elif confidence >= 50:
        severity = "medium"
    return {"disease": disease, "confidence": confidence, "severity": severity}
