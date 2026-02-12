# Quick Start Guide - Get a Trained Model

## 🚀 Fastest Way: Download Pre-trained Model

### Method 1: From Kaggle (Recommended)

**Step 1: Set up Kaggle**
```bash
# Install Kaggle
pip install kaggle

# Get API credentials
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token"
# 3. Save kaggle.json to: C:\Users\chara\.kaggle\kaggle.json
```

**Step 2: Download Dataset**
```bash
# Plant Village Dataset (38 classes, 54k images)
kaggle datasets download -d emmarex/plantdisease

# Rice Disease Dataset
kaggle datasets download -d minhhuy2810/rice-diseases-image-dataset

# Tomato Disease Dataset
kaggle datasets download -d kaustubhb999/tomatoleaf
```

**Step 3: Extract and Use**
```bash
# Extract the downloaded zip
# Look for .h5 or .keras files
# Copy to: cropguard-ai/model/crop_disease_model.h5
```

### Method 2: From TensorFlow Hub
```python
# Download a pre-trained plant disease model
import tensorflow_hub as hub

model = hub.load("https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1")
# Save it
model.save('model/crop_disease_model.h5')
```

---

## 🎓 Train Your Own Model

### Step 1: Get Dataset

**Option A: Download from Kaggle**
```bash
kaggle datasets download -d vipoooool/new-plant-diseases-dataset
unzip new-plant-diseases-dataset.zip
```

**Option B: Collect Your Own**
- Take 100-200 photos per disease class
- Organize into folders by disease name

### Step 2: Organize Dataset

Create this structure:
```
dataset/
├── train/
│   ├── Healthy/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   ├── Bacterial_Blight/
│   │   └── ...
│   └── Brown_Spot/
│       └── ...
├── validation/
│   ├── Healthy/
│   ├── Bacterial_Blight/
│   └── Brown_Spot/
└── test/ (optional)
    └── ...
```

**Split your data**:
- 70% for training
- 20% for validation
- 10% for testing

### Step 3: Run Training Script

```bash
# Make sure you're in the project directory
cd "c:\Users\chara\OneDrive\Desktop\jyothi project\AID103-Jyothi-ch-tech\cropguard-ai"

# Run the training script
python train_model.py
```

**What happens**:
1. Loads your dataset
2. Creates a MobileNetV2-based model
3. Trains for 30 epochs
4. Fine-tunes for 10 more epochs
5. Saves to `model/crop_disease_model.h5`

**Training time**: 
- With GPU: 30-60 minutes
- Without GPU: 2-4 hours

### Step 4: Update Disease Classes

After training, open `backend/services/ai_service.py` and update:

```python
CLASSES = [
    "Healthy",
    "Bacterial_Blight",
    "Brown_Spot",
    # ... your disease classes
]
```

(The training script will print the exact list to copy)

### Step 5: Restart Backend

```bash
# Stop current server (Ctrl+C)
# Start again
python app.py
```

---

## 📦 Recommended Datasets

### 1. PlantVillage Dataset
- **Size**: 54,000+ images
- **Classes**: 38 crop diseases
- **Crops**: Tomato, Potato, Apple, etc.
- **Link**: https://www.kaggle.com/datasets/emmarex/plantdisease

### 2. Rice Disease Dataset
- **Size**: 5,932 images
- **Classes**: 4 rice diseases
- **Link**: https://www.kaggle.com/datasets/minhhuy2810/rice-diseases-image-dataset

### 3. Crop Disease Dataset
- **Size**: 87,000+ images
- **Classes**: 25 diseases
- **Link**: https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install tensorflow keras matplotlib

# Download dataset (example)
kaggle datasets download -d vipoooool/new-plant-diseases-dataset

# Extract
unzip new-plant-diseases-dataset.zip -d dataset

# Train model
python train_model.py

# Check if model exists
dir model\crop_disease_model.h5
```

---

## ✅ Verification

After getting/training a model:

1. **Check file exists**:
   ```bash
   dir model\crop_disease_model.h5
   ```

2. **Check backend logs**:
   - Should see: "Model loaded successfully!"
   - Not: "WARNING: Model file not found"

3. **Test predictions**:
   - Upload different images
   - Should get accurate disease predictions
   - Confidence scores should be realistic

---

## 🆘 Troubleshooting

**"No module named 'tensorflow'"**
```bash
pip install tensorflow
```

**"Dataset not found"**
- Check path in `train_model.py`
- Make sure dataset folder structure is correct

**Training is slow**
- Reduce EPOCHS to 10-15
- Reduce IMG_SIZE to 128
- Use smaller BATCH_SIZE (16 instead of 32)

**Out of memory**
- Reduce BATCH_SIZE to 16 or 8
- Close other applications
- Use MobileNetV2 (already default)

---

## 💡 Pro Tips

1. **Start with a pre-trained model** from Kaggle to test quickly
2. **Then train your own** for better accuracy on your specific crops
3. **Use data augmentation** (already in the script)
4. **Collect more data** if accuracy is low (aim for 200+ images per class)
5. **Balance your dataset** (similar number of images per disease)

---

## 📞 Need Help?

- Check `MODEL_TRAINING_GUIDE.md` for detailed explanations
- Check backend terminal for error messages
- Verify TensorFlow installation: `pip show tensorflow`
