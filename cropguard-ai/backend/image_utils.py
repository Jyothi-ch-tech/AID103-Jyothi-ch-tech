from PIL import Image
import numpy as np

def preprocess_image(image_path):
    image = Image.open(image_path).resize((224, 224))
    return np.array(image) / 255.0
